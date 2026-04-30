"""Unit tests for bookmark parser."""

import pytest
from pathlib import Path
from groupmrk.parser import BookmarkParser, MAX_FILE_SIZE
from groupmrk.models import BookmarkCollection


class TestBookmarkParser:
    """Tests for BookmarkParser."""

    @pytest.fixture
    def parser(self):
        """Create parser instance."""
        return BookmarkParser()

    @pytest.fixture
    def sample_html(self):
        """Sample bookmark HTML content."""
        return """<!DOCTYPE NETSCAPE-Bookmark-file-1>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>Bookmarks</H1>
<DL><p>
    <DT><H3 ADD_DATE="1704067200">Development</H3>
    <DL><p>
        <DT><A HREF="https://github.com/python" ADD_DATE="1704067200">Python GitHub</A>
        <DT><A HREF="https://docs.python.org/3/" ADD_DATE="1704067200">Python Documentation</A>
    </DL><p>
    <DT><H3 ADD_DATE="1704067200">Tutorials</H3>
    <DL><p>
        <DT><A HREF="https://www.python.org/tutorial/" ADD_DATE="1704067200">Official Python Tutorial</A>
    </DL><p>
</DL><p>"""

    def test_parse_valid_html(self, parser, sample_html):
        """Test parsing valid HTML bookmark file."""
        collection = parser.parse(sample_html)
        assert len(collection.bookmarks) == 3
        assert collection.metadata.total_count == 3

    def test_parse_extracts_titles(self, parser, sample_html):
        """Test that parsing extracts bookmark titles."""
        collection = parser.parse(sample_html)
        titles = [b.title for b in collection.bookmarks]
        assert "Python GitHub" in titles
        assert "Python Documentation" in titles
        assert "Official Python Tutorial" in titles

    def test_parse_extracts_urls(self, parser, sample_html):
        """Test that parsing extracts bookmark URLs."""
        collection = parser.parse(sample_html)
        urls = [b.url for b in collection.bookmarks]
        assert "https://github.com/python" in urls
        assert "https://docs.python.org/3/" in urls
        assert "https://www.python.org/tutorial/" in urls

    def test_parse_tracks_folder_context(self, parser, sample_html):
        """Test that parsing tracks folder context."""
        collection = parser.parse(sample_html)
        folders = {b.url: b.original_folder for b in collection.bookmarks}
        assert folders["https://github.com/python"] == "Development"
        assert folders["https://www.python.org/tutorial/"] == "Tutorials"

    def test_parse_rejects_javascript_urls(self, parser):
        """Test that parser rejects javascript: URLs."""
        html = """<DL><p>
            <DT><A HREF="javascript:alert('xss')">Malicious</A>
        </DL><p>"""
        collection = parser.parse(html)
        assert len(collection.bookmarks) == 0

    def test_parse_rejects_data_urls(self, parser):
        """Test that parser rejects data: URLs."""
        html = """<DL><p>
            <DT><A HREF="data:text/html,<script>alert(1)</script>">Malicious</A>
        </DL><p>"""
        collection = parser.parse(html)
        assert len(collection.bookmarks) == 0

    def test_parse_rejects_non_http_urls(self, parser):
        """Test that parser rejects non-HTTP(S) URLs."""
        html = """<DL><p>
            <DT><A HREF="ftp://example.com">FTP Link</A>
        </DL><p>"""
        collection = parser.parse(html)
        assert len(collection.bookmarks) == 0

    def test_parse_accepts_https_urls(self, parser):
        """Test that parser accepts https URLs."""
        html = """<DL><p>
            <DT><A HREF="https://example.com">HTTPS Link</A>
        </DL><p>"""
        collection = parser.parse(html)
        assert len(collection.bookmarks) == 1
        assert collection.bookmarks[0].url == "https://example.com"

    def test_parse_accepts_http_urls(self, parser):
        """Test that parser accepts http URLs."""
        html = """<DL><p>
            <DT><A HREF="http://example.com">HTTP Link</A>
        </DL><p>"""
        collection = parser.parse(html)
        assert len(collection.bookmarks) == 1

    def test_parse_handles_empty_html(self, parser):
        """Test that parser handles empty HTML gracefully."""
        html = """<!DOCTYPE NETSCAPE-Bookmark-file-1>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>Bookmarks</H1>
<DL><p>
</DL><p>"""
        collection = parser.parse(html)
        assert len(collection.bookmarks) == 0

    def test_parse_handles_missing_href(self, parser):
        """Test that parser handles anchor tags without href."""
        html = """<DL><p>
            <DT><A>No href</A>
        </DL><p>"""
        collection = parser.parse(html)
        assert len(collection.bookmarks) == 0

    def test_parse_updates_metadata(self, parser, sample_html):
        """Test that parsing updates collection metadata."""
        collection = parser.parse(sample_html)
        assert collection.metadata.total_count == 3
        assert collection.metadata.categorized_count == 0
        assert collection.metadata.uncategorized_count == 3