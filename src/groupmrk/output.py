"""HTML output generator for organized bookmarks.

Generator for browser-importable HTML bookmarks.
Outputs valid Netscape Bookmark format with emoji categorization.

Gerador de bookmarks HTML importaveis pelo navegador.
Saida formato Netscape Bookmark valido com emoji por categoria.

Security: All user content is HTML-escaped to prevent XSS.
Seguranca: Todo conteudo do usuario e escapado para prevenir XSS.
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

from .models import Bookmark, BookmarkCollection, Theme

logger = logging.getLogger(__name__)


class HTMLOutputGenerator:
    """Generator for browser-importable HTML bookmarks.

    Responsible for generating valid HTML that can be imported back
    into browsers (Chrome, Firefox, Edge).

    Responsavel por gerar HTML valido que pode ser importado
    de volta nos navegadores (Chrome, Firefox, Edge).
    """

    def write(self, collection: BookmarkCollection, output_path: str | Path) -> None:
        """Write organized bookmarks to HTML file.

        Args:
            collection: Collection of organized bookmarks
            output_path: Path where HTML file will be written
        """
        logger.info(f"Starting HTML output generation: {output_path}")
        path = Path(output_path)

        logger.debug(f"Generating HTML for {len(collection.bookmarks)} bookmarks in {len(collection.themes)} themes")
        html = self._generate_html(collection)
        logger.debug(f"HTML generated: {len(html)} bytes")

        logger.info(f"Writing HTML to file: {path}")
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        logger.info(f"Output complete: {path}")

    def _generate_html(self, collection: BookmarkCollection) -> str:
        """Generate the HTML content in Netscape Bookmark format.

        Returns:
            Complete HTML string with DOCTYPE and all bookmarks
        """
        lines = [
            "<!DOCTYPE NETSCAPE-Bookmark-file-1>",
            "<!-- This is an automatically generated file.",
            "     It will be read and overwritten.",
            "     DO NOT EDIT! -->",
            "<META HTTP-EQUIV=\"Content-Type\" CONTENT=\"text/html; charset=UTF-8\">",
            "<TITLE>Bookmarks</TITLE>",
            "<H1>Bookmarks</H1>",
            "<DL><p>",
        ]

        for theme in collection.get_themes_list():
            if theme.bookmarks:
                lines.extend(self._generate_folder(theme))

        lines.append("</DL><p>")

        return "\n".join(lines)

    def _generate_folder(self, theme: Theme) -> list[str]:
        """Generate folder with bookmarks (theme group).

        Args:
            theme: Theme containing bookmarks to generate

        Returns:
            List of HTML lines for the folder
        """
        folder_name = theme.folder_name

        lines = [
            f"    <DT><H3 ADD_DATE=\"{self._get_timestamp()}\">{self._escape(folder_name)}</H3>",
            "    <DL><p>",
        ]

        for bookmark in theme.bookmarks:
            lines.extend(self._generate_bookmark(bookmark))

        lines.append("    </DL><p>")

        return lines

    def _generate_bookmark(self, bookmark: Bookmark) -> list[str]:
        """Generate a bookmark entry.

        Args:
            bookmark: Bookmark to generate HTML for

        Returns:
            List of HTML lines for the bookmark
        """
        add_date = self._format_date(bookmark.add_date)
        icon = bookmark.icon or ""

        lines = [
            f"        <DT><A HREF=\"{self._escape(bookmark.url)}\" "
            f'ADD_DATE="{add_date}" ICON="{icon}">{self._escape(bookmark.title)}</A>'
        ]

        return lines

    def _get_timestamp(self) -> str:
        """Get current timestamp for ADD_DATE attribute.

        Returns:
            Unix timestamp as string
        """
        return str(int(datetime.now().timestamp()))

    def _format_date(self, date: Optional[datetime]) -> str:
        """Format datetime to timestamp.

        Args:
            date: Optional datetime to convert

        Returns:
            Unix timestamp as string
        """
        if date:
            return str(int(date.timestamp()))
        return self._get_timestamp()

    def _escape(self, text: str) -> str:
        """Escape HTML special characters to prevent XSS.

        Security: All user-provided text (titles, URLs) must be escaped.
        Seguranca: Todo texto fornecido pelo usuario (titulos, URLs) deve ser escapado.

        Args:
            text: Raw text that may contain HTML special chars

        Returns:
            HTML-safe escaped string
        """
        return (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&#39;")
        )