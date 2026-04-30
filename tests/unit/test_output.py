"""Unit tests for HTML output generator."""

import pytest
import tempfile
from pathlib import Path
from groupmrk.output import HTMLOutputGenerator
from groupmrk.models import Bookmark, Theme, BookmarkCollection


class TestHTMLOutputGenerator:
    """Tests for HTMLOutputGenerator."""

    @pytest.fixture
    def generator(self):
        """Create generator instance."""
        return HTMLOutputGenerator()

    @pytest.fixture
    def sample_collection(self):
        """Create sample bookmark collection."""
        collection = BookmarkCollection()
        dev_theme = Theme(name="Development", emoji="💻")
        dev_bookmark1 = Bookmark(
            title="Python GitHub",
            url="https://github.com/python",
            theme="Development"
        )
        dev_bookmark2 = Bookmark(
            title="Python Docs",
            url="https://docs.python.org",
            theme="Development"
        )
        dev_theme.bookmarks = [dev_bookmark1, dev_bookmark2]
        collection.themes["Development"] = dev_theme

        tutorial_theme = Theme(name="Tutorials", emoji="📚")
        tutorial_bookmark = Bookmark(
            title="Learn Python",
            url="https://learnpython.org",
            theme="Tutorials"
        )
        tutorial_theme.bookmarks = [tutorial_bookmark]
        collection.themes["Tutorials"] = tutorial_theme

        collection.bookmarks = [dev_bookmark1, dev_bookmark2, tutorial_bookmark]
        return collection

    def test_generate_html_has_doctype(self, generator, sample_collection):
        """Test generated HTML has Netscape bookmark doctype."""
        html = generator._generate_html(sample_collection)
        assert "<!DOCTYPE NETSCAPE-Bookmark-file-1>" in html

    def test_generate_html_has_title(self, generator, sample_collection):
        """Test generated HTML has bookmarks title."""
        html = generator._generate_html(sample_collection)
        assert "<TITLE>Bookmarks</TITLE>" in html

    def test_generate_html_contains_themes(self, generator, sample_collection):
        """Test generated HTML contains theme folders."""
        html = generator._generate_html(sample_collection)
        assert "Development" in html
        assert "Tutorials" in html

    def test_generate_html_contains_bookmark_urls(self, generator, sample_collection):
        """Test generated HTML contains bookmark URLs."""
        html = generator._generate_html(sample_collection)
        assert "https://github.com/python" in html
        assert "https://docs.python.org" in html

    def test_generate_html_contains_bookmark_titles(self, generator, sample_collection):
        """Test generated HTML contains bookmark titles."""
        html = generator._generate_html(sample_collection)
        assert "Python GitHub" in html
        assert "Python Docs" in html

    def test_escape_escapes_ampersand(self, generator):
        """Test HTML escaping handles ampersands."""
        result = generator._escape("A & B")
        assert "&amp;" in result

    def test_escape_escapes_less_than(self, generator):
        """Test HTML escaping handles less-than signs."""
        result = generator._escape("<script>")
        assert "&lt;" in result

    def test_escape_escapes_greater_than(self, generator):
        """Test HTML escaping handles greater-than signs."""
        result = generator._escape("</script>")
        assert "&gt;" in result

    def test_escape_escapes_quotes(self, generator):
        """Test HTML escaping handles quotes."""
        result = generator._escape('He said "hello"')
        assert "&quot;" in result

    def test_escape_escapes_single_quotes(self, generator):
        """Test HTML escaping handles single quotes."""
        result = generator._escape("It's working")
        assert "&#39;" in result

    def test_xss_prevention_in_title(self, generator):
        """Test XSS attempt in title is escaped."""
        malicious_title = '<script>alert("xss")</script>'
        bookmark = Bookmark(title=malicious_title, url="https://example.com", theme="Test")
        theme = Theme(name="Test", emoji="📁")
        theme.bookmarks = [bookmark]
        collection = BookmarkCollection()
        collection.themes["Test"] = theme
        collection.bookmarks = [bookmark]

        html = generator._generate_html(collection)
        assert "<script>" not in html
        assert "&lt;script&gt;" in html

    def test_xss_prevention_in_url(self, generator):
        """Test XSS attempt in URL is escaped."""
        bookmark = Bookmark(title="Test", url='https://example.com?x=<script>', theme="Test")
        theme = Theme(name="Test", emoji="📁")
        theme.bookmarks = [bookmark]
        collection = BookmarkCollection()
        collection.themes["Test"] = theme
        collection.bookmarks = [bookmark]

        html = generator._generate_html(collection)
        assert "<script>" not in html

    def test_write_creates_file(self, generator, sample_collection):
        """Test write method creates output file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
            temp_path = f.name

        try:
            generator.write(sample_collection, temp_path)
            assert Path(temp_path).exists()
            content = Path(temp_path).read_text()
            assert "Bookmarks" in content
        finally:
            Path(temp_path).unlink(missing_ok=True)

    def test_folder_name_includes_emoji(self, generator, sample_collection):
        """Test folder names include emoji prefix."""
        html = generator._generate_html(sample_collection)
        assert "💻 Development" in html
        assert "📚 Tutorials" in html

    def test_empty_collection_generates_valid_html(self, generator):
        """Test generating HTML for empty collection."""
        collection = BookmarkCollection()
        html = generator._generate_html(collection)
        assert "<!DOCTYPE NETSCAPE-Bookmark-file-1>" in html
        assert "<TITLE>Bookmarks</TITLE>" in html