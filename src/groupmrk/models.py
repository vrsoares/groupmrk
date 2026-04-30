"""Data models for bookmarks manager.

These are the building blocks that represent your bookmarks.

Simple language guide:
- URL: A website address that has been checked for safety
- Bookmark: A saved link with its title and address
- Theme: A category (like "Programming" or "News")
- BookmarkCollection: All your bookmarks grouped together
- InvalidURLLog: A record of unsafe URLs that were blocked
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class VerificationOutcome(Enum):
    """Outcome of URL verification."""

    VALID = "valid"
    REDIRECT_FOLLOWED = "redirect_followed"
    KEEP_AUTH_REQUIRED = "keep_auth_required"
    FILTERED_404 = "filtered_404"
    FILTERED_4XX = "filtered_4xx"
    FILTERED_5XX = "filtered_5xx"
    FILTERED_TIMEOUT = "filtered_timeout"
    FILTERED_CONNECTION = "filtered_connection"
    FILTERED_SSRF = "filtered_ssrf"
    FILTERED_CREDENTIAL_URL = "filtered_credential_url"
    FILTERED_LOOP = "filtered_loop"
    FILTERED_PORT = "filtered_port"


@dataclass
class VerificationResult:
    """Result of URL verification."""

    outcome: VerificationOutcome
    status_code: Optional[int] = None
    final_url: Optional[str] = None
    redirect_chain: list[str] = field(default_factory=list)
    error: Optional[str] = None

    @property
    def should_keep(self) -> bool:
        """Whether this bookmark should be kept in output."""
        return self.outcome in (
            VerificationOutcome.VALID,
            VerificationOutcome.REDIRECT_FOLLOWED,
            VerificationOutcome.KEEP_AUTH_REQUIRED,
        )


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
    # HTTP verification fields
    http_status_code: Optional[int] = None
    is_reachable: bool = True
    verification_error: Optional[str] = None
    final_url: Optional[str] = None
    redirect_chain: list[str] = field(default_factory=list)
    is_safe_extension: bool = False
    extension_get_used: bool = False

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
    # HTTP verification statistics
    security_valid_count: int = 0
    reachable_count: int = 0
    filtered_count: int = 0
    filtered_4xx: int = 0
    filtered_5xx: int = 0
    filtered_timeout: int = 0
    filtered_connection: int = 0
    filtered_ssrf: int = 0
    filtered_redirect_loop: int = 0
    filtered_credential_url: int = 0
    filtered_port: int = 0
    redirects_followed: int = 0
    extension_get_attempts: int = 0
    extension_get_successes: int = 0
    requests_made: int = 0


@dataclass
class BookmarkCollection:
    """Collection of bookmarks with categorization."""

    bookmarks: list[Bookmark] = field(default_factory=list)
    themes: dict[str, Theme] = field(default_factory=dict)
    metadata: CollectionMetadata = field(default_factory=CollectionMetadata)

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

# Safe file extensions for GET fallback (when HEAD returns 403/405)
SAFE_EXTENSIONS: set[str] = {
    ".pdf", ".zip", ".doc", ".docx", ".xls", ".xlsx",
    ".ppt", ".pptx", ".jpg", ".jpeg", ".png", ".gif",
    ".txt", ".html", ".htm", ".csv", ".json", ".xml",
}

# Private IP ranges for SSRF protection
PRIVATE_IP_RANGES: list[str] = [
    "10.0.0.0/8",       # RFC 1918
    "172.16.0.0/12",    # RFC 1918
    "192.168.0.0/16",   # RFC 1918
    "169.254.0.0/16",   # Link-local
    "127.0.0.0/8",      # Loopback
    "0.0.0.0/8",        # "This network"
    "224.0.0.0/4",      # Multicast
    "240.0.0.0/4",      # Reserved
    "100.64.0.0/10",    # Carrier-grade NAT
    "198.18.0.0/15",    # Benchmark testing
    "203.0.113.0/24",   # Documentation
]

# IPv6 private ranges
PRIVATE_IPV6_RANGES: list[str] = [
    "fc00::/7",         # Unique local
    "fe80::/10",        # Link-local
    "::1/128",          # Loopback
    "::ffff:0:0/96",    # IPv4-mapped IPv6
]

# Allowed ports for redirects
ALLOWED_PORTS: set[int] = {80, 443}

# Maximum requests per run
MAX_REQUESTS: int = 5000

# Sensitive query parameters to redact
SENSITIVE_PARAMS: set[str] = {
    "token", "session_id", "key", "auth", "password", "secret", "api_key",
    "access_token", "bearer", "session", "sid", "jwt", "nonce", "code", "state",
}

# Dangerous protocol schemes to block in redirects
DANGEROUS_SCHEMES: set[str] = {
    "javascript", "data", "file", "gopher", "ftp",
}