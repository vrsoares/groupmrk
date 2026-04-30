"""Unit tests for data models."""

import pytest
from datetime import datetime
from groupmrk.models import Bookmark, Theme, BookmarkCollection, CollectionMetadata


class TestBookmark:
    """Tests for Bookmark model."""

    def test_bookmark_creation(self):
        """Test creating a basic bookmark."""
        bookmark = Bookmark(title="Test", url="https://example.com")
        assert bookmark.title == "Test"
        assert bookmark.url == "https://example.com"
        assert bookmark.theme is None
        assert bookmark.manual_category is None

    def test_effective_category_no_override(self):
        """Test effective_category returns theme when no manual override."""
        bookmark = Bookmark(title="Test", url="https://example.com", theme="Development")
        assert bookmark.effective_category == "Development"

    def test_effective_category_with_override(self):
        """Test effective_category returns manual_category when set."""
        bookmark = Bookmark(
            title="Test",
            url="https://example.com",
            theme="Development",
            manual_category="Custom"
        )
        assert bookmark.effective_category == "Custom"

    def test_effective_category_uncategorized(self):
        """Test effective_category returns Uncategorized when no theme."""
        bookmark = Bookmark(title="Test", url="https://example.com")
        assert bookmark.effective_category == "Uncategorized"


class TestTheme:
    """Tests for Theme model."""

    def test_theme_creation(self):
        """Test creating a theme with emoji."""
        theme = Theme(name="Development", emoji="💻")
        assert theme.name == "Development"
        assert theme.emoji == "💻"
        assert theme.bookmarks == []

    def test_folder_name_includes_emoji(self):
        """Test folder_name combines emoji and name."""
        theme = Theme(name="Development", emoji="💻")
        assert theme.folder_name == "💻 Development"


class TestBookmarkCollection:
    """Tests for BookmarkCollection model."""

    def test_collection_empty_init(self):
        """Test empty collection initialization."""
        collection = BookmarkCollection()
        assert collection.bookmarks == []
        assert collection.themes == {}
        assert collection.metadata.total_count == 0

    def test_add_bookmark(self):
        """Test adding bookmarks to collection."""
        collection = BookmarkCollection()
        bookmark = Bookmark(title="Test", url="https://example.com")
        collection.add_bookmark(bookmark)
        assert len(collection.bookmarks) == 1

    def test_assign_theme_creates_theme(self):
        """Test assigning theme creates new theme entry."""
        collection = BookmarkCollection()
        bookmark = Bookmark(title="Test", url="https://example.com")
        collection.assign_theme(bookmark, "Development")
        assert "Development" in collection.themes
        assert len(collection.themes["Development"].bookmarks) == 1

    def test_assign_theme_adds_to_existing(self):
        """Test assigning theme adds bookmark to existing theme."""
        collection = BookmarkCollection()
        bookmark1 = Bookmark(title="Test1", url="https://example1.com")
        bookmark2 = Bookmark(title="Test2", url="https://example2.com")
        collection.assign_theme(bookmark1, "Development")
        collection.assign_theme(bookmark2, "Development")
        assert len(collection.themes["Development"].bookmarks) == 2

    def test_get_themes_list_sorted(self):
        """Test get_themes_list returns sorted themes."""
        collection = BookmarkCollection()
        collection.themes["Zebra"] = Theme(name="Zebra", emoji="🦓")
        collection.themes["Alpha"] = Theme(name="Alpha", emoji="🐱")
        themes = collection.get_themes_list()
        assert themes[0].name == "Alpha"
        assert themes[1].name == "Zebra"