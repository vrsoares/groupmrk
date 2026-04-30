# Data Model: HTTP Response Handling Feature

## 1. Bookmark Model Changes

### 1.1 Current Model (models.py:8-18)

```python
@dataclass
class Bookmark:
    title: str
    url: str
    add_date: Optional[datetime] = None
    icon: Optional[str] = None
    original_folder: Optional[str] = None
    theme: Optional[str] = None
    manual_category: Optional[str] = None
```

### 1.2 Updated Model

```python
@dataclass
class Bookmark:
    title: str
    url: str
    add_date: Optional[datetime] = None
    icon: Optional[str] = None
    original_folder: Optional[str] = None
    theme: Optional[str] = None
    manual_category: Optional[str] = None
    
    # New fields for HTTP Response Handling
    http_status_code: Optional[int] = None        # E.g., 200, 403, 404, 500
    is_reachable: bool = True                      # False if filtered (5xx, timeout, etc)
    verification_error: Optional[str] = None        # Reason if filtered
    final_url: Optional[str] = None             # After redirect following
    redirect_chain: list[str] = field(default_factory=list)  # Full redirect path
    is_safe_extension: bool = False              # For GET fallback logic
    extension_get_used: bool = False           # If GET fallback was attempted
```

### 1.3 Field Descriptions

| Field | Type | Purpose |
|-------|------|---------|
| `http_status_code` | `Optional[int]` | HTTP response code from verification |
| `is_reachable` | `bool` | False if URL should be filtered from output |
| `verification_error` | `Optional[str]` | Error reason: "timeout", "5xx", "404", "ssrf_blocked" |
| `final_url` | `Optional[str]` | Final URL after following redirects |
| `redirect_chain` | `list[str]` | All URLs in redirect chain (for security audit) |
| `is_safe_extension` | `bool` | True if URL has safe file extension (.pdf, .zip, etc.) |
| `extension_get_used` | `bool` | True if GET fallback was used after 403/405 on HEAD |

## 2. CollectionMetadata Changes

### 2.1 Current Model (models.py:41-49)

```python
@dataclass
class CollectionMetadata:
    total_count: int = 0
    categorized_count: int = 0
    uncategorized_count: int = 0
    theme_count: int = 0
    source_file: Optional[str] = None
    processed_at: Optional[datetime] = None
```

### 2.2 Updated Model

```python
@dataclass
class CollectionMetadata:
    # Existing fields
    total_count: int = 0
    categorized_count: int = 0
    uncategorized_count: int = 0
    theme_count: int = 0
    source_file: Optional[str] = None
    processed_at: Optional[datetime] = None
    
    # New fields for HTTP Response Handling
    security_valid_count: int = 0            # Passed security checks
    reachable_count: int = 0                 # Passed HTTP verification
    filtered_count: int = 0                    # Total filtered URLs
    
    # Filtering breakdown
    filtered_4xx: int = 0                    # 4xx errors
    filtered_5xx: int = 0                    # 5xx errors
    filtered_timeout: int = 0                 # Timeouts
    filtered_connection: int = 0               # Connection errors
    filtered_ssrf: int = 0                     # Blocked SSRF attempts
    filtered_redirect_loop: int = 0           # Redirect loop blocked
    
    redirects_followed: int = 0                # Total redirects handled
    extension_get_attempts: int = 0            # GET fallback attempts
    extension_get_successes: int = 0            # GET fallback worked
```

### 2.3 Statistics Calculations

**Pipeline Flow**:

```
Input:               283 bookmarks (total_count)
     │
     ▼ Security Check (parser.py)
         - Blocks: javascript:, data:, file://, chrome-extension:
         │
         ▼ 279 security valid (security_valid_count)
              │
              ▼ HTTP Verification (verifier.py - new)
                   - 2xx: Keep
                   - 3xx: Follow redirect
                   - 4xx: Special handling
                   - 5xx: Remove
                   - Timeout: Remove
                   │
                   ▼ ~245 reachable (reachable_count)
                        │
                        ▼ Classification (graph.py)
                             - AI theme assignment
                             │
                             ▼ Output
                                  ~245 categorized
```

**Statistics Display Example**:

```
Parsed: 283 → Security Valid: 279 → Reachable: 245 → Categorized: 10 themes
Filtered: 34 (404: 20, 403: 5, Timeout: 9)
Redirects followed: 15 (updated to final URLs)
```

## 3. URL Verification Result

### 3.1 VerificationOutcome Enum

```python
from enum import Enum

class VerificationOutcome(Enum):
    """Result of URL verification."""
    VALID = "valid"                     # 2xx - include in output
    REDIRECT_FOLLOWED = "redirect_followed"   # 3xx - updated to final URL
    KEEP_AUTH_REQUIRED = "keep_auth_required"  # 401 - may have credentials
    KEEP_AUTH_403 = "keep_auth_403"  # 403 with WWW-Authenticate
    EXTENSION_GET_FALLBACK = "extension_get_fallback"  # Tried GET for extension
    REMOVED_404 = "removed_404"      # Not found
    REMOVED_5XX = "removed_5xx"     # Server error
    REMOVED_TIMEOUT = "removed_timeout"  # Timeout
    REMOVED_CONNECTION = "removed_connection"  # Connection failed
    BLOCKED_SSRF = "blocked_ssrf"    # Redirect to private IP
    BLOCKED_REDIRECT_LOOP = "blocked_redirect_loop"  # Redirect loop
    BLOCKED_DANGEROUS_PROTOCOL = "blocked_dangerous_protocol"  # javascript: in redirect
```

### 3.2 VerificationResult Class

```python
@dataclass
class VerificationResult:
    """Result of URL verification."""
    outcome: VerificationOutcome
    status_code: Optional[int]
    final_url: Optional[str]
    redirect_chain: list[str]
    error_message: Optional[str] = None
    
    @property
    def should_keep(self) -> bool:
        """Whether URL should be included in output."""
        return self.outcome in [
            VerificationOutcome.VALID,
            VerificationOutcome.REDIRECT_FOLLOWED,
            VerificationOutcome.KEEP_AUTH_REQUIRED,
            VerificationOutcome.KEEP_AUTH_403,
            VerificationOutcome.EXTENSION_GET_FALLBACK,
        ]
```

## 4. Safe Extension List

### 4.1 Supported Extensions (per spec R1.1.1)

```python
SAFE_EXTENSIONS: set[str] = {
    ".pdf",
    ".zip",
    ".doc",
    ".docx",
    ".xls",
    ".xlsx",
    ".ppt",
    ".pptx",
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".txt",
    ".html",
    ".htm",
}
```

### 4.2 Extension Check Logic

```python
def has_safe_extension(url: str) -> bool:
    """Check if URL has a safe file extension."""
    parsed = urlparse(url)
    path = parsed.path.lower()
    for ext in SAFE_EXTENSIONS:
        if path.endswith(ext):
            return True
    return False
```

## 5. Private IP Ranges

### 5.1 SSRF Protection Ranges (per spec)

```python
PRIVATE_IP_RANGES: list[tuple[str, str]] = [
    ("10.0.0.0", "10.255.255.255"),           # 10.0.0.0/8
    ("172.16.0.0", "172.31.255.255"),       # 172.16.0.0/12
    ("192.168.0.0", "192.168.255.255"),     # 192.168.0.0/16
    ("169.254.0.0", "169.254.255.255"),     # Link-local
    ("127.0.0.0", "127.255.255.255"),         # Localhost
    ("::1", "::1"),                        # IPv6 localhost
    ("fc00::", "fdff:ffff:ffff:ffff:ffff"),  # IPv6 private
    ("fe80::", "febf:ffff:ffff:ffff:ffff"),  # IPv6 link-local
]
```

### 5.2 Implementation Using ipaddress

```python
import ipaddress
from urllib.parse import urlparse

def is_private_ip(url: str) -> bool:
    """Check if URL resolves to a private IP."""
    try:
        parsed = urlparse(url)
        host = parsed.hostname
        if not host:
            return False
        ip = ipaddress.ip_address(host)
        return (
            ip.is_private or
            ip.is_loopback or
            ip.is_link_local
        )
    except ValueError:
        return False  # Not an IP, allow (will need DNS)
```

## 6. API Response Changes

### 6.1 Classification API Fix

**Current** (problematic):
```python
result = self._client.zero_shot_classification(text, labels)
if result and hasattr(result, "labels") and result.labels:
    return result.labels[0]  # Fragile - may be None
return "Uncategorized"
```

**Fixed**:
```python
try:
    result = self._client.zero_shot_classification(text, labels)
    # Validate response properly
    if result is None:
        logger.warning("API returned None")
        return self._keyword_fallback(title, url)
    if hasattr(result, "labels") and result.labels:
        label = result.labels[0]
        if label and label.strip():
            return label.strip()
    if hasattr(result, "labels") and hasattr(result, "scores"):
        # Alternative: pick highest score
        scores = result.scores
        labels = result.labels
        if scores and labels:
            max_idx = scores.index(max(scores))
            return labels[max_idx]
except Exception as e:
    logger.warning(f"Classification error: {e}")

return self._keyword_fallback(title, url)
```

### 6.2 Keyword Fallback Method

```python
def _keyword_fallback(self, title: str, url: str) -> str:
    """Fallback classification using keywords."""
    title_lower = title.lower()
    url_lower = url.lower()
    combined = f"{title_lower} {url_lower}"
    
    keywords = {
        "github": "Development",
        "stackoverflow": "Development",
        "python": "Programming",
        "javascript": "Programming",
        "tutorial": "Tutorials",
        "course": "Tutorials",
        "documentation": "Documentation",
        "docs": "Documentation",
        "news": "News",
        "blog": "News",
        "youtube": "Entertainment",
        "netflix": "Entertainment",
        "amazon": "Shopping",
    }
    
    for keyword, theme in keywords.items():
        if keyword in combined:
            return theme
    
    return "Uncategorized"
```

## 7. Backward Compatibility

### 7.1 Default Values

All new fields use default values to maintain backward compatibility:

```python
http_status_code: Optional[int] = None
is_reachable: bool = True  # Default True, filtered URLs set to False
```

### 7.2 Output Filtering

In output generation:

```python
# Only include reachable bookmarks
valid_bookmarks = [b for b in collection.bookmarks if b.is_reachable]
```

---

**Data Model Complete**: All fields defined with defaults for backward compatibility.