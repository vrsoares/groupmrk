"""HTML bookmark parser for Chrome/Firefox/Edge exports.

Parser para exportar bookmarks de navegadores (Chrome/Firefox/Edge).
Parse de arquivos HTML de favoritos do formato Netscape Bookmark.

This parser safely handles user-provided HTML files without executing
any embedded scripts or dangerous content. / Este parser manipula
arquivos HTML de favoritos de forma segura, sem executar scripts.
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

from bs4 import BeautifulSoup, Tag

from .models import Bookmark, BookmarkCollection
from .validator import validate_url, redact_sensitive_params, normalize_url, is_local_url, is_ip_address
from .verifier import verify_batch

logger = logging.getLogger(__name__)

# Maximum file size: 10MB to prevent DoS / Tamanho maximo do arquivo
MAX_FILE_SIZE = 10 * 1024 * 1024


class BookmarkParser:
    """Parser for Netscape Bookmark HTML format.

    Responsible for safely parsing browser bookmark exports.
    Security: validates file size, encoding, and sanitizes all inputs.

    Responsavel por parsear exports de favoritos do navegador de forma segura.
    Seguranca: valida tamanho do arquivo, encoding, e sanitiza todas as entradas.
    """

    def parse_file(self, file_path: str | Path) -> BookmarkCollection:
        """Parse an HTML bookmark file.

        Args:
            file_path: Path to the bookmark HTML file

        Returns:
            BookmarkCollection with all parsed bookmarks

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file is too large or invalid
        """
        logger.info(f"Starting to parse bookmark file: {file_path}")
        path = Path(file_path)

        if not path.exists():
            logger.error(f"Bookmark file not found: {file_path}")
            raise FileNotFoundError(f"Bookmark file not found: {file_path}")

        # Security: Check file size to prevent DoS
        file_size = path.stat().st_size
        if file_size > MAX_FILE_SIZE:
            logger.error(f"File too large: {file_size} bytes (max: {MAX_FILE_SIZE})")
            raise ValueError(f"File too large (max {MAX_FILE_SIZE} bytes)")

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        logger.info(f"File loaded, size: {len(content)} bytes")
        collection = self.parse(content, source_file=str(path))
        logger.info(f"Parsing complete: {len(collection.bookmarks)} bookmarks found")
        return collection

    def parse(self, html: str, source_file: Optional[str] = None) -> BookmarkCollection:
        """Parse HTML content into bookmark collection.

        Args:
            html: Raw HTML content from bookmark file
            source_file: Original file path for metadata

        Returns:
            BookmarkCollection with parsed bookmarks
        """
        logger.debug("Starting HTML parsing")
        soup = BeautifulSoup(html, "html.parser")
        collection = BookmarkCollection()

        logger.debug("Searching for bookmarks and folders")
        self._find_folder_context(soup, collection)

        logger.debug("Applying deduplication")
        seen_normalized: set[str] = set()
        unique_bookmarks: list[Bookmark] = []
        duplicate_count = 0

        for bookmark in collection.bookmarks:
            normalized = normalize_url(bookmark.url)
            if normalized and normalized in seen_normalized:
                duplicate_count += 1
                logger.debug(f"Duplicate URL removed: {bookmark.url[:50]}...")
            else:
                if normalized:
                    seen_normalized.add(normalized)
                unique_bookmarks.append(bookmark)

        collection.bookmarks = unique_bookmarks

        logger.debug("Categorizing local network and IP addresses")
        local_network_count = 0

        for bookmark in collection.bookmarks:
            if is_local_url(bookmark.url):
                collection.assign_theme(bookmark, "Local Network")
                local_network_count += 1
            elif is_ip_address(bookmark.url):
                collection.assign_theme(bookmark, "IP Address")

        self._verify_urls(collection)

        collection.metadata.total_count = len(collection.bookmarks) + len(collection.invalid_urls)
        collection.metadata.valid_count = len(collection.bookmarks)
        collection.metadata.invalid_count = len(collection.invalid_urls)
        collection.metadata.duplicate_count = duplicate_count
        collection.metadata.local_network_count = local_network_count
        collection.metadata.categorized_count = sum(
            1 for b in collection.bookmarks if b.theme is not None
        )
        collection.metadata.uncategorized_count = sum(
            1 for b in collection.bookmarks if b.theme is None
        )
        collection.metadata.source_file = source_file
        collection.metadata.processed_at = datetime.now()

        return collection

    def _find_folder_context(self, element: Tag, collection: BookmarkCollection) -> None:
        """Find all bookmarks and track their folder context.

        Security: Only processes <a> and <h3> tags, ignores all scripts.
        Seguranca: Apenas processa tags <a> e <h3>, ignora todos scripts.
        """
        current_folder = ""

        for tag in element.descendants:
            if not isinstance(tag, Tag):
                continue

            if tag.name == "h3":
                current_folder = tag.get_text(strip=True)
            elif tag.name == "a" and tag.get("href"):
                bookmark = self._parse_bookmark(tag, current_folder, collection)
                if bookmark:
                    collection.add_bookmark(bookmark)

    def _parse_bookmark(self, a: Tag, folder: str, collection: BookmarkCollection) -> Optional[Bookmark]:
        """Parse an anchor tag into a Bookmark.

        Security: Validates URL scheme, sanitizes all inputs.
        Seguranca: Valida esquema URL, sanitiza todas as entradas.

        Args:
            a: BeautifulSoup Tag representing an anchor element
            folder: Current folder context
            collection: BookmarkCollection for logging invalid URLs

        Returns:
            Bookmark if valid, None if rejected (javascript:, empty, etc.)
        """
        title = a.get_text(strip=True)
        url = a.get("href", "")

        validation = validate_url(url)
        if not validation.is_valid:
            safe_url = redact_sensitive_params(url)
            logger.warning(f"Invalid URL rejected: {safe_url} - {validation.reason}")
            collection.add_invalid_url(url, validation.reason, folder)
            return None

        if validation.is_suspicious:
            safe_url = redact_sensitive_params(url)
            logger.warning(f"Suspicious URL: {safe_url} - {validation.reason}")
            collection.add_invalid_url(url, validation.reason, folder)

        # Security: Reject dangerous URL schemes / Rejeita esquemas de URL perigosos
        if not url or url.startswith("javascript:") or url.startswith("data:"):
            logger.debug(f"Skipping unsafe URL: {url[:30]}...")
            collection.add_invalid_url(url, "dangerous scheme", folder)
            return None

        # Security: Only allow http/https schemes / Apenas permite esquemas http/https
        if not url.startswith(("http://", "https://")):
            logger.debug(f"Skipping non-HTTP URL: {url[:30]}...")
            return None

        add_date_str = a.get("add_date")
        add_date: Optional[datetime] = None
        if add_date_str:
            try:
                add_date = datetime.fromtimestamp(int(add_date_str))
            except (ValueError, OSError):
                pass

        icon = a.get("icon")

        return Bookmark(
            title=title,
            url=url,
            add_date=add_date,
            icon=icon,
            original_folder=folder,
        )

    def _verify_urls(self, collection: BookmarkCollection) -> None:
        """Verify URL reachability and categorize unreachable bookmarks."""
        logger.info("Starting URL verification")
        urls_to_verify = [b.url for b in collection.bookmarks]

        if not urls_to_verify:
            logger.debug("No URLs to verify")
            return

        verification_results = verify_batch(urls_to_verify)

        for bookmark in collection.bookmarks:
            result = verification_results.get(bookmark.url)
            if result is None:
                continue

            if result.verification_skipped:
                continue

            if not result.is_reachable:
                collection.add_unreachable_url(bookmark.url)
                logger.warning(f"Unreachable URL: {bookmark.url[:50]}... ({result.error_type})")

        logger.info(
            f"Verification complete: {collection.metadata.unreachable_count} unreachable URLs"
        )