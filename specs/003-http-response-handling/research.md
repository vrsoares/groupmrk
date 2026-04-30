# Technical Research: HTTP Response Handling Feature

## 1. Current Architecture Analysis

### 1.1 Missing Components

| Component | Status | Location |
|-----------|--------|----------|
| `verifier.py` | **DOES NOT EXIST** | Referenced in spec but not implemented |
| URL verification logic | Missing | No HTTP calls anywhere in codebase |
| HTTP response filtering | Missing | All URLs passed through |
| Statistics tracking | Partial | Only parsing counts, no filtering |

### 1.2 Existing Code Flow

```
cli.py:import_cmd()
    │
    ├─► parser.py:BookmarkParser.parse_file()     [HTML → Bookmark objects]
    ├─► graph.py:Orchestrator.organize()      [Classification]
    └─► output.py:HTMLOutputGenerator      [Write output]
         │
         ▼ NO VERIFICATION HAPPENS BETWEEN PARSE AND OUTPUT
```

**Critical Gap**: No URL verification step exists. The spec requires filtering based on HTTP responses, but there's no code to make HTTP requests or check URL validity.

### 1.3 Classification Issue Analysis

**Location**: `src/groupmrk/api.py:68-86`

```python
def classify_theme(self, title: str, url: str) -> str:
    result = self._client.zero_shot_classification(text, self._candidate_labels)
    if result and hasattr(result, "labels") and result.labels:
        label = result.labels[0]
        return label
    return "Uncategorized"  # Fallback for EVERY failure
```

**Problem Identified**:
1. `bart-large-mnli` is a zero-shot classification model expecting plain text
2. Response format checking is fragile: `hasattr(result, "labels")`
3. When API fails/returns unexpected format → always "Uncategorized"
4. No error logging with specific cause
5. No retry logic or alternative model

**Evidence from Test Data**:
- 283 bookmarks processed
- 279 passed security check (parser.py rejects javascript:/data:)
- All 279 classified as "Uncategorized"
- This indicates API is failing silently or returning fallback

### 1.4 Data Model Gaps

**Location**: `src/groupmrk/models.py:8-18`

```python
@dataclass
class Bookmark:
    title: str
    url: str
    add_date: Optional[datetime]
    icon: Optional[str]
    original_folder: Optional[str]
    theme: Optional[str]
    manual_category: Optional[str]
```

**Missing Fields for HTTP Response Handling**:
- `http_status_code: Optional[int]` - Track response code
- `is_reachable: bool` - URL responded (success or handled error)
- `verification_error: Optional[str]` - Why verification failed
- `final_url: Optional[str]` - After redirect following
- `redirect_chain: list[str]` - Full redirect path for security
- `is_safe_extension: bool` - For GET fallback logic

**Location**: `src/groupmrk/models.py:41-49` (CollectionMetadata)

```python
@dataclass
class CollectionMetadata:
    total_count: int
    categorized_count: int
    uncategorized_count: int
    theme_count: int
    source_file: Optional[str]
    processed_at: Optional[datetime]
```

**Missing Statistics**:
- `security_valid_count` - After security filtering
- `reachable_count` - After HTTP verification
- `filtered_count` - URLs removed
- `filtered_4xx: int` - 4xx errors count
- `filtered_5xx: int` - 5xx errors count
- `filtered_timeout: int` - Timeout count
- `filtered_connection: int` - Connection errors
- `redirects_followed: int` - Redirects handled

### 1.5 Security Validation (Current)

**Location**: `src/groupmrk/parser.py:134-142`

```python
if not url or url.startswith("javascript:") or url.startswith("data:"):
    return None  # Rejected
if not url.startswith(("http://", "https://")):
    return None  # Rejected
```

**Already implemented**:
- Block javascript: and data: protocols
- Only http/https allowed

**Not implemented (spec R1.2)**:
- Block dangerous redirect protocols (javascript:, data:, file:, gopher:, ftp:)
- SSRF protection (private IP ranges)
- Redirect loop detection

## 2. Technical Dependencies

### 2.1 Required Libraries

| Library | Purpose | Current Status |
|---------|--------|---------------|
| `requests` | HTTP calls for verification | Used in `api.py:OllamaClient`, not in core |
| `requests` + `requests-strict` or `httpx` | Handle redirects properly | Not present |
| `urllib3` | Timeout and retries | Built into requests |

**Recommendation**: Use `requests` library (already available via OllamaClient dependency).

### 2.2 HTTP Response Handling Requirements

| Response Code | Action | Implementation |
|-------------|--------|---------------|
| 2xx | Keep | `response.raise_for_status()` not raised |
| 301/302/307/308 | Follow redirect | `requests.get(allow_redirects=True, max_redirects=5)` |
| 304 | Keep original | No error |
| 401 | Keep | May need credentials |
| 403 | Special handling | Check extension, try GET |
| 404 | Remove | Check response code |
| 5xx | Remove | `response.raise_for_status()` |
| Timeout | Remove | Timeout exception |
| Connection | Remove | Connection error exception |

### 2.3 SSRF Protection Requirements

**Private IP Ranges (per spec R1.2.2)**:

| CIDR | Range |
|------|-------|
| 10.0.0.0/8 | 10.0.0.0 - 10.255.255.255 |
| 172.16.0.0/12 | 172.16.0.0 - 172.31.255.255 |
| 192.168.0.0/16 | 192.168.0.0 - 192.168.255.255 |
| 169.254.0.0/16 | Link-local |
| 127.0.0.0/8 | localhost |
| fc00::/7 | IPv6 private |
| fe80::/10 | IPv6 link-local |
| ::1 | IPv6 localhost |

**Implementation Approach**:
- Use `ipaddress` module (Python stdlib)
- Check final URL after each redirect
- Block if redirect goes to private IP

## 3. Implementation Complexity Estimate

### 3.1 New Module: verifier.py

| Component | Lines | Complexity |
|-----------|------|------------|
| URLVerifier class | ~50 | Medium |
| HTTP status handling | ~40 | Low |
| Redirect following | ~50 | Medium |
| SSRF protection | ~30 | Medium |
| GET fallback for extensions | ~30 | Medium |
| Timeout handling | ~10 | Low |
| **Total** | ~210 | Medium |

### 3.2 Model Updates

| File | Changes | Lines |
|------|---------|-------|
| `models.py` | Add Bookmark fields | ~15 |
| `models.py` | Add Metadata fields | ~15 |
| **Total** | | ~30 |

### 3.3 API Fixes

| Issue | Fix | Lines |
|-------|-----|------|
| Classification always fallback | Fix response handling | ~20 |
| Add retry/fallback | Alternative themes | ~20 |
| **Total** | | ~40 |

### 3.4 CLI Integration

| Component | Lines |
|-----------|------|
| Add verification step | ~30 |
| Add statistics display | ~20 |
| **Total** | ~50 |

**Total Estimated**: ~330 lines across 4 modules

## 4. Test Data Analysis

### 4.1 Input File Characteristics

- **File**: `bookmarks_4_28_26.html`
- **Bookmarks**: 283 total
- **After security (parser)**: ~279 (4 rejected: chrome-extension, file://)

### 4.2 Expected Output

| Stage | Count | Notes |
|-------|-------|-------|
| Parsed | 283 | Raw |
| Security valid | ~279 | After javascript:/data: rejection |
| Reachable | ~245-260 | After HTTP filtering |
| Categorized | ~10 themes | After AI classification |

### 4.3 Filtering Estimates

Based on spec test data (95 errors on 279):
- 404: ~20
- 403: ~5 (some with extension GET fallback)
- 5xx: ~5-10
- Timeout: ~9
- Connection: ~5

## 5. Risk Assessment

### 5.1 High Risk

| Risk | Impact | Mitigation |
|------|--------|------------|
| API failures causing "Uncategorized" | Classification doesn't work | Fix response parsing, add fallback |
| No URL verification exists | Core feature missing | Build verifier.py from scratch |
| SSRF vulnerability | Security breach | Implement strict IP checks |

### 5.2 Medium Risk

| Risk | Impact | Mitigation |
|------|--------|------------|
| Redirect loops | Infinite loop | Max 5 hops, loop detection |
| Timeouts slow processing | User experience | 10s timeout per URL |
| Extension false positives | Keep bad URLs | Strict extension list |

### 5.3 Low Risk

| Risk | Impact | Mitigation |
|------|--------|------------|
| Statistics display | Minor UX | Add to CLI output |

## 6. Technology Decisions

### 6.1 HTTP Client

**Choice**: `requests` library (existing in codebase via OllamaClient)

**Rationale**: Already available, handles redirects, timeouts, retries

### 6.2 IP Validation

**Choice**: `ipaddress` module (Python stdlib)

**Rationale**: No external dependency, handles IPv4/IPv6

### 6.3 Classification Fix

**Choice**: Fix response parsing in `api.py`, add keyword fallback

**Rationale**: Minimal code change, improves reliability

---

**Research Complete**: Implementation requires new verifier.py module, model updates, and API fixes. No existing verification code found.