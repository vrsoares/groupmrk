# Feature Specification: HTTP Response Handling

## 1. Overview

| Attribute | Value |
|-----------|-------|
| **Feature Name** | HTTP Response Handling |
| **Feature Number** | 003 |
| **Type** | Bug Fix + Enhancement |
| **Summary** | Handle all HTTP response types correctly and fix bookmark classification |

---

## 2. Problems (from test)

### Problem 1: Non-200 URLs included in output
- **Observed:** 279 valid URLs, ~95 returned errors (403, 404, timeout)
- **Current:** These are logged but still included in output
- **Expected:** Remove them from final output

### Problem 2: Classification returns "Uncategorized" for all
- **Observed:** All 279 bookmarks classified as "Uncategorized"
- **Current:** AI classifier returns fallback for every bookmark
- **Expected:** Proper theme names based on content

---

## 3. Goals

1. **Handle all HTTP responses correctly** - Filter, follow, or keep based on type
2. **Fix classification** - Get real theme names instead of "Uncategorized"
3. **Show statistics** - Clear count of filtered vs kept URLs
4. **Security first** - Maximum security when following redirects

---

## 4. Requirements

### R1: Handle HTTP Responses by Type

| Response | Action |
|----------|--------|
| **2xx (200, 201, 204)** | Keep URL |
| **301/302/307/308 (Redirect)** | Follow with security - update URL to final destination |
| **304 (Not Modified)** | Keep original URL |
| **4xx (400, 401, 403, 404, 405)** | Special handling (see R1.1) |
| **5xx (500, 502, 503)** | Remove - server error |
| **Timeout** | Remove - unreachable |
| **Connection Error** | Remove - unreachable |

**R1.1: Special 4xx Handling**
- R1.1.1 If URL has file extension (safe list: .pdf, .zip, .doc, .docx, .xls, .xlsx, .ppt, .pptx, .jpg, .png, .gif, .txt, .html) and HEAD returns 403/405 → try GET as fallback (discard body, max 1MB, timeout 10s)
- R1.1.2 If URL returns 403 with "WWW-Authenticate" header or login form detected → Keep (user may have access)
- R1.1.3 404 (Not Found) → Remove
- R1.1.4 401 (Unauthorized) → Keep (may have credentials)

**R1.2: Redirect Handling (Security First)**
- R1.2.1 Block dangerous protocols in redirects: javascript:, data:, file://, gopher://, ftp://
- R1.2.2 SSRF protection - do NOT follow redirects to private IPs:
  - 10.0.0.0/8
  - 172.16.0.0/12 (172.16-31.x.x)
  - 192.168.0.0/16
  - 169.254.0.0/16 (link-local)
  - 127.0.0.0/8 (localhost)
  - IPv6 fc00::/7, fe80::/10, ::1
- R1.2.3 Limit redirect chain to 5 hops max (timeout: 10s per hop, 30s total max)
- R1.2.4 Detect and block redirect loops (A→B→A)
- R1.2.5 Update bookmark URL to final destination after following

### R2: Fix Classification
- R2.1 Investigate why classifier returns fallback always
- R2.2 Fix prompt or model for classification
- R2.3 Validate output format
- R2.4 Fallback: If classifier cannot be fixed, use keyword-based grouping (extract domain, title keywords)

### R3: Statistics
- R3.1 Show: Parsed → Security Valid → Reachable → Categorized
- R3.2 Show count of filtered URLs by reason:
  - 4xx errors
  - 5xx errors
  - Timeout
  - Connection failed
  - Redirects followed (show new URL)

### R4: Logging Security
- R4.1 Redact sensitive query params in logs: token=, session_id=, key=, auth=, password=, secret=, api_key=
- R4.2 Never log full URLs with auth tokens
- R4.3 Log filtered URLs with redacted paths

---

## 5. Constraints

- **C1** Keep local network URLs (192.168.x.x, 10.x.x.x) in initial request only (not in redirects)
- **C2** Keep security validation (chrome-extension, file:// blocked)
- **C3** Maintain output format compatibility
- **C4** Maximum cybersecurity for redirects (no SSRF, no internal IPs)
- **C5** Do not expose sensitive data in logs (redact tokens in URLs)

---

## 6. Acceptance Criteria

| ID | Criterion | Test |
|----|-----------|------|
| AC1 | 404/500 URLs NOT in output | Run test |
| AC2 | Extension URLs with 403 on HEAD try GET (safe extensions only) | Test with .pdf URL |
| AC3 | 301/302 followed, URL updated | Check output |
| AC4 | No SSRF - internal IPs blocked in redirects | Security test |
| AC5 | Auth-required 403 kept in output | Test with protected URL |
| AC6 | Bookmarks in real themes | Check output |
| AC7 | Statistics shown | Check CLI |
| AC8 | Redirect loops detected and blocked | Test with loop URL |
| AC9 | Sensitive params redacted in logs | Check logs |

---

## 7. Out of Scope

- New CLI flags
- New export formats
- Rate limit changes

---

## 8. Dependencies

- `src/groupmrk/verifier.py` - handle redirects, GET fallback, SSRF protection
- `src/groupmrk/api.py` - fix classification
- `src/groupmrk/parser.py` - add filtering logic

---

## 9. User-Facing Explanations (for docs)

### What are "themes"?
Groups like: "Programming", "Machine Learning", "Recipes", "News", "Shopping". Bookmarks about similar topics go into the same folder.

### What does the output look like?
An HTML file with your bookmarks organized into folders by topic. The tool also shows a summary on screen:
```
Parsed: 283 → Security Valid: 279 → Reachable: 245 → Categorized: 10 themes
Filtered: 34 (404/410: 20, 403: 5, Timeout: 9)
```

### What happens to filtered URLs?
They are silently excluded (not shown in output). Statistics show how many were removed and why, but specific URLs are not listed to protect privacy.