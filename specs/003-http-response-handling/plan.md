# Implementation Plan: HTTP Response Handling Feature

## Phase Overview

| Phase | Duration | Focus | Files Changed |
|-------|----------|-------|--------------|
| 1 | Setup | Model updates, constants | `models.py` |
| 2 | Core | verifier.py, HTTP logic | New `verifier.py` |
| 3 | Integration | Wire into CLI flow | `cli.py`, `graph.py` |
| 4 | Fixes | Classification fix | `api.py` |
| 5 | Statistics | Display output | `cli.py` |
| 6 | Testing | Verify acceptance criteria | Tests |

---

## Phase 1: Data Model Setup

**Duration**: 1 hour
**Objective**: Update data models with new fields

### Tasks

#### T1.1 Update Bookmark Model (models.py)

```
Location: src/groupmrk/models.py:8-18
Changes: Add HTTP-related fields
Lines: ~15 new lines
```

- [ ] Add `http_status_code: Optional[int]` field
- [ ] Add `is_reachable: bool = True` field
- [ ] Add `verification_error: Optional[str]` field
- [ ] Add `final_url: Optional[str]` field
- [ ] Add `redirect_chain: list[str]` field
- [ ] Add `is_safe_extension: bool = False` field
- [ ] Add `extension_get_used: bool = False` field

#### T1.2 Update CollectionMetadata (models.py)

```
Location: src/groupmrk/models.py:41-49
Changes: Add statistics fields
Lines: ~25 new lines
```

- [ ] Add `security_valid_count: int = 0`
- [ ] Add `reachable_count: int = 0`
- [ ] Add `filtered_count: int = 0`
- [ ] Add `filtered_4xx: int = 0`, `filtered_5xx: int = 0`
- [ ] Add `filtered_timeout: int = 0`, `filtered_connection: int = 0`
- [ ] Add `filtered_ssrf: int = 0`
- [ ] Add `filtered_redirect_loop: int = 0`
- [ ] Add `redirects_followed: int = 0`
- [ ] Add `extension_get_attempts: int = 0`
- [ ] Add `extension_get_successes: int = 0`

#### T1.3 Add Constants (models.py)

```
Location: models.py end of file
Changes: Add SAFE_EXTENSIONS and PRIVATE_IP_RANGES
Lines: ~30 new lines
```

- [ ] Add `SAFE_EXTENSIONS` constant
- [ ] Add `PRIVATE_IP_RANGES` for SSRF protection

---

## Phase 2: Core Verification

**Duration**: 3 hours
**Objective**: Create verifier.py with HTTP handling

### Tasks

#### T2.1 Create verifier.py

```
Location: src/groupmrk/verifier.py (NEW)
Purpose: Handle all HTTP verification
Lines: ~210 lines
```

**T2.1.1 URLVerifier Class**

- [ ] Create `class URLVerifier` with initialization
- [ ] Add timeout configuration (default 10s)
- [ ] Add max redirects configuration (default 5)

**T2.1.2 HTTP Status Handling**

- [ ] Implement `verify(url)` method
- [ ] Handle 2xx responses (keep)
- [ ] Handle 3xx redirects (follow)
- [ ] Handle 304 (keep)
- [ ] Handle 401 (keep - may need credentials)
- [ ] Handle 403 (special handling)
- [ ] Handle 404 (remove)
- [ ] Handle 5xx (remove)

**T2.1.3 Redirect Handling (SECURITY: Manual per-hop)**

- [ ] Use `allow_redirects=False` - manually follow each hop
- [ ] For each hop: resolve DNS, check IP, then connect
- [ ] Block dangerous protocols in redirects (R1.2.1): javascript:, data:, file://, gopher://, ftp://
- [ ] SSRF protection (R1.2.2) - check IP at EACH hop:
  - Use `socket.getaddrinfo()` to resolve DNS BEFORE connection
  - Check resolved IP against private ranges
  - Block IPv4-mapped IPv6: `::ffff:0:0/96`
- [ ] Limit redirect chain to 5 hops max (R1.2.3)
- [ ] Detect redirect loops (R1.2.4) - track visited URLs
- [ ] Update bookmark URL to final destination (R1.2.5)
- [ ] Set custom User-Agent: `groupmrk/1.0`
- [ ] URL length limit: reject URLs > 2048 chars

**T2.1.4 Extension GET Fallback (NO DOWNLOAD)**

- [ ] Implement special handling for file extensions (R1.1)
- [ ] Check for safe extension (.pdf, .zip, etc.)
- [ ] Try GET if HEAD returns 403/405
- [ ] Use `stream=True` - only check headers, DO NOT download body
- [ ] Read first 1KB max to confirm resource exists
- [ ] Close connection immediately after status check
- [ ] 10s timeout per request

**T2.1.5 Error Handling**

- [ ] Handle timeouts (remove from output)
- [ ] Handle connection errors (remove)

#### T2.2 Private IP Validation

```
Location: verifier.py
Purpose: SSRF protection
Lines: ~40
```

- [ ] Use `ipaddress` module (stdlib)
- [ ] Use `socket.getaddrinfo()` to resolve DNS BEFORE connection
- [ ] Check all redirect destinations (per-hop)
- [ ] Block if private IP detected:
  - 10.0.0.0/8
  - 172.16.0.0/12
  - 192.168.0.0/16
  - 169.254.0.0/16 (link-local)
  - 127.0.0.0/8 (localhost)
  - IPv6: fc00::/7, fe80::/10, ::1
  - IPv4-mapped IPv6: ::ffff:0:0/96

#### T2.2b Concurrency Control

```
Location: verifier.py
Purpose: Limit concurrent requests
Lines: ~15
```

- [ ] Use `asyncio.Semaphore` with limit 5
- [ ] Process URLs in batches of 3-5
- [ ] Respect rate limits with 100ms delay between requests

#### T2.3 Dangerous Protocol Blocking

```
Location: verifier.py
Purpose: Block javascript: etc. in redirects
Lines: ~15
```

- [ ] Block `javascript:` in redirect chain
- [ ] Block `data:` in redirect chain
- [ ] Block `file://` in redirect chain
- [ ] Block `gopher://`, `ftp://` in redirect chain

---

## Phase 3: Integration

**Duration**: 2 hours
**Objective**: Wire verification into workflow

### Tasks

#### T3.1 Add Verification to CLI Flow

```
Location: src/groupmrk/cli.py:import_cmd()
Changes: Add verification step between parse and organize
Lines: ~40
```

- [ ] Add verification step (Step 1.5/4)
- [ ] Call URLVerifier.verify() on each bookmark
- [ ] Filter unreachable bookmarks
- [ ] Update bookmark fields from verification
- [ ] Update collection metadata

**Updated Flow**:

```
Step 1/4: Parse HTML file
Step 1.5/4: Verify URLs (NEW)
Step 2/4: Organize with AI
Step 3/4: Generate HTML output
Step 4/4: Write to file
```

#### T3.2 Update Graph Integration

```
Location: src/groupmrk/graph.py:Orchestrator.organize()
Purpose: Handle verifiable bookmarks only
Lines: ~10
```

- [ ] Filter bookmarks before classification
- [ ] Log number of filtered URLs
- [ ] Update metadata counts

#### T3.3 Output Generator Update

```
Location: src/groupmrk/output.py
Purpose: Filter output to reachable only
Lines: ~10
```

- [ ] Filter `is_reachable=False` bookmarks
- [ ] Only output valid bookmarks

---

## Phase 4: Classification Fix

**Duration**: 1 hour
**Objective**: Fix classification returning "Uncategorized"

### Tasks

#### T4.1 Fix API Response Handling

```
Location: src/groupmrk/api.py:HuggingFaceClient.classify_theme()
Changes: Better response validation
Lines: ~25
```

- [ ] Add proper None checking
- [ ] Add empty string validation
- [ ] Add try-except for safety
- [ ] Log detailed errors

#### T4.2 Add Keyword Fallback

```
Location: src/groupmrk/api.py
Purpose: Reliable fallback classification
Lines: ~30
```

- [ ] Add `_keyword_fallback()` method
- [ ] Map keywords to themes
- [ ] Use as final fallback

#### T4.3 Test Classification Fix

```
Command: groupmrk import bookmarks.html --mock
Expected: Themes other than "Uncategorized"
```

---

## Phase 5: Statistics Display

**Duration**: 1 hour
**Objective**: Show filtering statistics

### Tasks

#### T5.1 Display Statistics in CLI

```
Location: src/groupmrk/cli.py
Changes: Show detailed statistics
Lines: ~20
```

- [ ] Display after verification
- [ ] Show: Parsed → Security Valid → Reachable → Categorized
- [ ] Show: Filtered by reason (4xx, 5xx, timeout, etc.)
- [ ] Show: Redirects followed

#### T5.2 Format Output

```
Example output:
Parsed: 283 → Security Valid: 279 → Reachable: 245 → Categorized: 10 themes
Filtered: 34 (404: 20, 403: 5, Timeout: 9)
Redirects followed: 15 (URLs updated to final destinations)
```

---

## Phase 6: Testing & Verification

**Duration**: 2 hours
**Objective**: Verify all acceptance criteria

### Tasks

#### T6.1 Test AC1: 404/500 URLs NOT in output

```
Test: Run on bookmarks.html, check output
Expected: No 404 or 5xx URLs in output HTML
```

#### T6.2 Test AC2: Extension GET fallback

```
Test: Use test .pdf URL with 403 on HEAD
Expected: GET attempted, URL kept if GET succeeds
```

#### T6.3 Test AC3: Redirects followed

```
Test: Use URL that redirects
Expected: Final URL in output, redirect chain logged
```

#### T6.4 Test AC4: SSRF protection

```
Test: Use URL that redirects to 192.168.x.x
Expected: URL filtered, logged as blocked
```

#### T6.5 Test AC5: Auth-required kept

```
Test: Use 401 or 403 with WWW-Authenticate
Expected: URL kept in output
```

#### T6.6 Test AC6: Real themes

```
Test: Run classification on known bookmarks
Expected: Themes like "Programming", "Development", etc.
```

#### T6.7 Test AC7: Statistics shown

```
Test: Run import command
Expected: Statistics displayed in CLI
```

#### T6.8 Test AC8: Redirect loops blocked

```
Test: Use URL with redirect loop
Expected: Loop detected, chain limited to 5
```

#### T6.9 Test AC9: Sensitive params redacted

```
Test: Check logs for URLs with tokens
Expected: params like token=, session_id= redacted
```

---

## Implementation Order

```
Phase 1: Data Models (T1.1-T1.3)
    ↓
Phase 2: Core - verifier.py (T2.1-T2.3)
    ↓
Phase 3: Integration (T3.1-T3.3)
    ↓
Phase 4: Classification Fix (T4.1-T4.3)
    ↓
Phase 5: Statistics (T5.1-T5.2)
    ↓
Phase 6: Testing (T6.1-T6.9)
```

---

## Dependencies

| Phase | Depends On |
|-------|-----------|
| 2 | 1 (models need fields) |
| 3 | 2 (verifier needs to exist) |
| 4 | 2 (optional - can run parallel) |
| 5 | 2 (statistics from verification) |
| 6 | All previous |

---

## Code Estimate

| Phase | New/Changed Files | Lines |
|-------|------------------|-------|
| 1 | `models.py` | ~70 |
| 2 | NEW `verifier.py` | ~210 |
| 3 | `cli.py`, `graph.py`, `output.py` | ~60 |
| 4 | `api.py` | ~55 |
| 5 | `cli.py` | ~20 |
| 6 | Tests | ~100 |
| **Total** | | **~515** |

---

## Security Considerations (per spec)

### R4: Logging Security

- [ ] Redact sensitive query params (token=, session_id=, key=, auth=, password=, secret=, api_key=)
- [ ] Never log full URLs with auth tokens
- [ ] Log filtered URLs with redacted paths

### Implementation

```python
import re
from urllib.parse import urlparse, parse_qs

SENSITIVE_PARAMS = {
    "token", "session_id", "key", "auth", "password", "secret", "api_key",
    "access_token", "bearer", "session", "sid", "jwt", "nonce", "code", "state"
}

def redact_url(url: str) -> str:
    """Redact sensitive parameters from URL."""
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    for param in SENSITIVE_PARAMS:
        if param in query:
            query[param] = ["[REDACTED]"]
    new_query = "&".join(f"{k}={v[0]}" for k, v in query.items())
    # Redact path segments that look like tokens (long alphanumeric strings)
    path = re.sub(r'/[a-zA-Z0-9]{32,}/', '/[REDACTED]/', parsed.path)
    return parsed._replace(query=new_query, path=path).geturl()
```

---

## Risk Mitigation

| Risk | Phase | Mitigation |
|------|-------|-----------|
| API failures → "Uncategorized" | 4 | Fix response parsing + keyword fallback |
| No verifier code exists | 2 | Build from scratch with tests |
| SSRF vulnerability | 2 | Strict IP checks at each redirect |
| Redirect loops | 2 | Max 5 hops + loop detection |
| Slow processing | 2 | 10s timeout per URL |

---

**Plan Complete**: Implementation sequenced into 6 phases with clear dependencies and acceptance criteria verification.

---

## Glossary (for non-technical readers)

| Term | Simple Explanation |
|------|-------------------|
| **2xx, 3xx, 4xx, 5xx** | HTTP status code ranges: 2xx = success, 3xx = redirect, 4xx = client error, 5xx = server error |
| **HEAD request** | A "light" check - asks the server "does this exist?" without downloading the file |
| **GET request** | Actually downloads the content (used as fallback when HEAD fails) |
| **SSRF** | Server-Side Request Forgery - an attack where someone tricks your server into accessing internal/private networks |
| **Private IPs** | Addresses like 192.168.x.x, 10.x.x.x that are only accessible on local networks, not the internet |
| **IPv4-mapped IPv6** | A way to write IPv4 addresses in IPv6 format (e.g., `::ffff:192.168.1.1`) - used to bypass IP checks |
| **Redirect chain** | The path a URL takes through multiple redirects (e.g., A → B → C) |
| **DNS rebinding** | An attack where a domain name changes what IP it points to after initial check |
| **stream=True** | Download only the headers, not the full file - used to check if a file exists without downloading it |
| **Semaphore** | A way to limit how many things can happen at the same time (e.g., max 5 requests) |
| **Redact** | Hide sensitive information in logs (replace with [REDACTED]) |
| **Uncategorized** | The fallback theme when classification fails - means "we don't know what this bookmark is about" |