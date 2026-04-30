"""Data models for bookmarks manager."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class URL:
    """Represents a validated and normalized URL string."""

    original: str
    normalized: str
    scheme: str
    host: str
    is_local: bool
    is_ip: bool


@dataclass(frozen=True)
class ValidationResult:
    """Result of URL security validation."""

    is_valid: bool
    is_suspicious: bool
    reason: str
    patterns_found: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class URLVerificationResult:
    """Result of HTTP HEAD verification."""

    status_code: int
    is_reachable: bool
    error_type: str
    verification_skipped: bool


@dataclass
class InvalidURLLog:
    """Log entry for security review of invalid URLs."""

    url: str
    reason: str
    timestamp: datetime = field(default_factory=datetime.now)
    original_folder: Optional[str] = None


@dataclass
class Bookmark:
    """A single bookmark entry."""

    title: str
    url: str
    add_date: Optional[datetime] = None
    icon: Optional[str] = None
    original_folder: Optional[str] = None
    theme: Optional[str] = None
    manual_category: Optional[str] = None

    @property
    def effective_category(self) -> str:
        """Get the effective category (manual override or theme)."""
        return self.manual_category or self.theme or "Uncategorized"


@dataclass
class Theme:
    """A theme category with emoji identifier."""

    name: str
    emoji: str
    bookmarks: list[Bookmark] = field(default_factory=list)

    @property
    def folder_name(self) -> str:
        """Get the folder name with emoji."""
        return f"{self.emoji} {self.name}"


@dataclass
class CollectionMetadata:
    """Metadata about the bookmark collection."""

    total_count: int = 0
    valid_count: int = 0
    invalid_count: int = 0
    unreachable_count: int = 0
    duplicate_count: int = 0
    local_network_count: int = 0
    source_file: Optional[str] = None
    processed_at: Optional[datetime] = None


@dataclass
class BookmarkCollection:
    """Collection of bookmarks with categorization."""

    bookmarks: list[Bookmark] = field(default_factory=list)
    themes: dict[str, Theme] = field(default_factory=dict)
    metadata: CollectionMetadata = field(default_factory=CollectionMetadata)
    invalid_urls: list[InvalidURLLog] = field(default_factory=list)
    unreachable_urls: list[str] = field(default_factory=list)

    def add_bookmark(self, bookmark: Bookmark) -> None:
        """Add a bookmark to the collection."""
        self.bookmarks.append(bookmark)

    def assign_theme(self, bookmark: Bookmark, theme_name: str) -> None:
        """Assign a theme to a bookmark."""
        bookmark.theme = theme_name
        if theme_name not in self.themes:
            self.themes[theme_name] = Theme(name=theme_name, emoji=EMOJI_MAP.get(theme_name, "📁"))
        self.themes[theme_name].bookmarks.append(bookmark)

    def get_themes_list(self) -> list[Theme]:
        """Get sorted list of themes."""
        return sorted(self.themes.values(), key=lambda t: t.name)

    def add_invalid_url(self, url: str, reason: str, folder: Optional[str] = None) -> None:
        """Log an invalid URL for security review."""
        self.invalid_urls.append(
            InvalidURLLog(url=url, reason=reason, original_folder=folder)
        )

    def add_unreachable_url(self, url: str) -> None:
        """Add an unreachable URL to the list."""
        if url not in self.unreachable_urls:
            self.unreachable_urls.append(url)


EMOJI_MAP: dict[str, str] = {
    "Development": "💻",
    "Programming": "🔧",
    "Tutorials": "📚",
    "Documentation": "📖",
    "News": "📰",
    "Entertainment": "🎬",
    "Music": "🎵",
    "Gaming": "🎮",
    "Sports": "⚽",
    "Technology": "⚙️",
    "Science": "🔬",
    "Finance": "💰",
    "Shopping": "🛒",
    "Travel": "✈️",
    "Food": "🍳",
    "Health": "🏥",
    "Education": "🎓",
    "Social": "👥",
    "Work": "💼",
    "Tools": "🔨",
    "Reference": "📋",
    "Images": "🖼️",
    "Videos": "🎥",
    "Local Network": "🔗",
    "IP Address": "🌐",
    "Uncategorized": "📌",
}