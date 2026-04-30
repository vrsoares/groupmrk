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

        collection.metadata.total_count = len(collection.bookmarks)
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
                bookmark = self._parse_bookmark(tag, current_folder)
                if bookmark:
                    collection.add_bookmark(bookmark)

    def _parse_bookmark(self, a: Tag, folder: str) -> Optional[Bookmark]:
        """Parse an anchor tag into a Bookmark.

        Security: Validates URL scheme, sanitizes all inputs.
        Seguranca: Valida esquema URL, sanitiza todas as entradas.

        Args:
            a: BeautifulSoup Tag representing an anchor element
            folder: Current folder context

        Returns:
            Bookmark if valid, None if rejected (javascript:, empty, etc.)
        """
        title = a.get_text(strip=True)
        url = a.get("href", "")

        # Security: Reject dangerous URL schemes / Rejeita esquemas de URL perigosos
        if not url or url.startswith("javascript:") or url.startswith("data:"):
            logger.debug(f"Skipping unsafe URL: {url[:30]}...")
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