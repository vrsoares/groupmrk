# Feature Specification: Bookmark Parser Improvements

**Feature Branch**: `[002-parser-improvements]`
**Created**: 2026-04-30
**Status**: Draft
**Input**: User description: "vamos melhorar o parser, eliminar entradas duplicadas, agrupar links locais, separar enderecos com ip ao inves de url"

## Clarifications

### Session 2026-04-30

- Q: What is explicitly OUT of scope for this feature? → A: No export/write operations, no changes to output format, but URL verification via HTTP HEAD request is IN scope
- Q: What happens to URLs that FAIL verification? → A: Mark as "unreachable" but keep in collection (warning only)
- Q: Should URL verification be optional or always enabled? → A: Always enabled, with strict security measures to prevent leaking, invasion, injection, or any malicious behavior
- Q: What batch size for URL verification? → A: Process URLs in batches of 10 concurrent requests (matches concurrent connection limit), with 5-second timeout per URL for fast response
- Q: How should verification results be displayed? → A: Console log output with summary of valid/invalid/unreachable counts

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Validate URLs with Security Checks (Priority: P1)

When the user imports a bookmarks file, the system MUST validate each URL for security threats and structural integrity, logging all invalid or suspicious URLs for the user to review.

**Why this priority**: Malformed, suspicious, or potentially dangerous URLs pose security risks. Users must be informed about invalid URLs to take appropriate action (remove or investigate). This is the highest priority as it protects users from potential threats.

**Independent Test**: Can be tested by importing bookmarks with invalid URLs (empty, malformed, suspicious patterns) and verifying they are logged and handled appropriately.

**Acceptance Scenarios**:

1. **Given** a bookmarks file containing an empty URL string, **When** processed, **Then** the URL is marked as invalid and logged with reason "empty"
2. **Given** a bookmarks file containing a URL with missing scheme `www.example.com`, **When** processed, **Then** it is marked as invalid and logged with reason "missing scheme"
3. **Given** a bookmarks file containing a URL with invalid characters like `<script>`, **When** processed, **Then** it is marked as invalid and logged with reason "invalid characters"
4. **Given** a bookmarks file containing a URL with SQL injection pattern `example.com?id=1' OR '1'='1`, **When** processed, **Then** it is marked as suspicious and logged with warning
5. **Given** a bookmarks file containing a URL with XSS pattern `example.com?q=<img onerror=alert(1)>`, **When** processed, **Then** it is marked as suspicious and logged with warning
6. **Given** a bookmarks file containing a valid URL `https://example.com/page`, **When** processed, **Then** it passes validation with no logging
7. **Given** a bookmarks file with 5 invalid URLs mixed with 95 valid URLs, **When** processed, **Then** all 5 invalid URLs are logged in a summary list and the valid 95 are processed normally

---

### User Story 2 - Remove Duplicate Bookmarks (Priority: P2)

When the user imports a bookmarks file that contains duplicate URLs, the system MUST remove all duplicates and keep only the first occurrence, ensuring each unique URL appears only once in the final collection.

**Why this priority**: Duplicate bookmarks create confusion and reduce the usefulness of the organized collection. Removing duplicates is a fundamental data quality improvement that affects all users.

**Independent Test**: Can be tested by importing an HTML file with known duplicates and verifying that output contains only unique URLs.

**Acceptance Scenarios**:

1. **Given** a bookmarks file with two identical URLs `https://example.com/page`, **When** the file is processed, **Then** only one bookmark for that URL appears in the final output
2. **Given** a bookmarks file with same URL but different trailing slashes `https://example.com/` and `https://example.com`, **When** processed, **Then** both are treated as duplicates and only one is kept
3. **Given** a bookmarks file with same URL but different case `https://Example.com/Page` and `https://example.com/page`, **When** processed, **Then** both are treated as duplicates

---

### User Story 3 - Group Local Links Together (Priority: P3)

When the user processes bookmarks containing local and private network links, the system MUST group them into a dedicated "Local Network" category separate from internet bookmarks.

**Why this priority**: Local links (localhost, file://, private IPs) are functionally different from internet URLs. Grouping them separately helps users organize their bookmarks logically.

**Independent Test**: Can be tested by importing bookmarks containing localhost URLs and verifying they appear in a dedicated category.

**Acceptance Scenarios**:

1. **Given** a bookmarks file containing `http://localhost:8080/dashboard`, **When** processed, **Then** the bookmark is placed in a "Local Network" category
2. **Given** a bookmarks file containing `file:///C:/Documents/notes.html`, **When** processed, **Then** the bookmark is placed in a "Local Network" category
3. **Given** a bookmarks file containing `http://192.168.1.100:3000/app`, **When** processed, **Then** the bookmark is placed in a "Local Network" category

---

### User Story 4 - Separate IP Address URLs from Domain URLs (Priority: P4)

When the user processes bookmarks containing URLs with IP addresses as the host (instead of domain names), the system MUST identify and separate these into their own category.

**Why this priority**: URLs with IP addresses instead of domain names often represent local network resources, development servers, or intranet sites. Separating them helps users distinguish between public internet and internal network resources.

**Independent Test**: Can be tested by importing bookmarks with various IP-based URLs and verifying they are categorized separately from domain-based URLs.

**Acceptance Scenarios**:

1. **Given** a bookmark with URL `http://192.168.1.50:8080/api`, **When** processed, **Then** it is identified as an IP-based URL and categorized accordingly
2. **Given** a bookmark with URL `http://10.0.0.1/admin`, **When** processed, **Then** it is categorized as an IP-based URL
3. **Given** a bookmark with URL `http://172.16.0.100/dev`, **When** processed, **Then** it is categorized as an IP-based URL
4. **Given** a bookmark with URL `https://api.example.com`, **When** processed, **Then** it remains as a normal domain URL (not IP-based)

---

### Edge Cases

- What happens when a bookmark has an empty title? (use URL as fallback title)
- How does the system handle malformed URLs that cannot be parsed? (log as invalid with reason)
- What happens when bookmarks have identical titles but different URLs? (keep both as they are unique)
- How are query parameters handled in duplicate detection? (include them in comparison)
- What happens when a URL contains only special characters? (mark as invalid, log with reason)
- What happens when a URL has legitimate apostrophe in path like `example.com/ John's Page`? (validate context - apostrophe in path is valid, in query string is suspicious)
- How many invalid URLs can be logged before performance is impacted? (handle up to 10,000 gracefully)
- What happens when URL verification times out? (log as "timeout", continue processing)
- How does the system handle SSL certificate errors? (log as "SSL error", continue processing)
- Should URL verification run sequentially or in parallel? (parallel with reasonable concurrency limit)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST validate each URL for structural integrity before processing
- **FR-002**: System MUST reject URLs that are empty or contain only whitespace
- **FR-003**: System MUST reject URLs with missing or invalid schemes (only http, https, file are allowed)
- **FR-004**: System MUST detect and log URLs containing potentially malicious patterns including SQL injection attempts (`'`, `OR`, `UNION`, `SELECT`, `DROP`, `--`)
- **FR-005**: System MUST detect and log URLs containing XSS patterns (`<script>`, `javascript:`, `onerror`, `onload`, `<img`)
- **FR-006**: System MUST detect and log URLs containing path traversal patterns (`../`, `..\\`, `/etc/`, `C:\`)
- **FR-007**: System MUST detect and log URLs with invalid characters that could indicate corruption or attack (< > " ' ; non-printable control characters)
- **FR-008**: System MUST present a clear log to the user listing all invalid URLs with the reason for rejection
- **FR-009**: System MUST NOT block processing of valid URLs when invalid URLs are present (continue processing valid bookmarks)
- **FR-010**: System MUST count and report total number of invalid URLs found during validation
- **FR-011**: System MUST detect and eliminate duplicate bookmarks based on URL, treating URLs with different trailing slashes or case as duplicates
- **FR-012**: System MUST normalize URLs before comparison by removing trailing slashes and converting to lowercase
- **FR-013**: System MUST identify local links including localhost, 127.0.0.1, file:// protocol, and private IP ranges (192.168.x.x, 10.x.x.x, 172.16-31.x.x)
- **FR-014**: System MUST group local and private network links into a dedicated "Local Network" category
- **FR-015**: System MUST detect URLs where the hostname is an IP address and categorize them separately from domain-based URLs
- **FR-016**: System MUST handle bookmarks with empty titles by using the URL as the display title
- **FR-017**: System MUST preserve the first occurrence of any duplicate and discard subsequent occurrences
- **FR-018**: System MUST include query parameters and port numbers when comparing URLs for duplicate detection
- **FR-019**: System MUST verify URL accessibility via HTTP HEAD request (safest method - no body download)
- **FR-020**: System MUST timeout URL verification after 5 seconds to prevent hanging
- **FR-021**: System MUST log URLs that fail verification (connection refused, timeout, 4xx/5xx errors)
- **FR-022**: System MUST report verification status for each URL in the output
- **FR-023**: System MUST skip URL verification for local/network URLs (localhost, private IPs, file://)
- **FR-024**: System MUST mark URLs that fail verification as "unreachable" but retain them in the collection with a warning status
- **FR-025**: System MUST limit HTTP requests to maximum 10 concurrent connections (batch size) to prevent port scanning behavior
- **FR-026**: System MUST only send HTTP HEAD requests (never GET/POST) to minimize data exposure
- **FR-027**: System MUST reject URLs pointing to internal network ranges (non-RFC1918 private IPs beyond 192.168/16, 10/8, 172.16/12)
- **FR-028**: System MUST not follow redirects beyond 1 hop to prevent redirect-based scanning
- **FR-029**: System MUST not capture or store any response body from URLs (only status code)
- **FR-030**: System MUST log verification attempts without storing sensitive URL parameters (tokens, credentials)
- **FR-031**: System MUST output verification summary to console showing counts: valid, invalid (security issues), unreachable (verification failed)

### Key Entities

- **URL**: The web address string, must support normalization for comparison and security validation
- **Bookmark**: A single saved link with title, URL, add_date, icon, folder, and category properties
- **BookmarkCollection**: The container holding all bookmarks with deduplication logic
- **Local Network Category**: A special category for local/private URLs identified by IP or localhost
- **InvalidURLLog**: A log entry containing the invalid URL, rejection reason, and timestamp for security review

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of URLs with SQL injection patterns are detected and logged with warning
- **SC-002**: 100% of URLs with XSS patterns are detected and logged with warning
- **SC-003**: All invalid URLs are presented to the user in a clear log with rejection reason
- **SC-004**: System reports accurate count of invalid URLs found during validation
- **SC-005**: Valid bookmarks are processed normally even when invalid URLs exist in the file
- **SC-006**: Users can import a bookmarks file with 1000 duplicates and receive a deduplicated collection with 0 duplicate URLs
- **SC-007**: All local network URLs (localhost, 127.0.0.1, private IPs) are automatically categorized in a dedicated category
- **SC-008**: 100% of URLs with IP address hosts are correctly identified and separated from domain-based URLs
- **SC-009**: No valid bookmarks are lost during deduplication (preservation of first occurrence)
- **SC-010**: Processing time increases by no more than 50% when deduplication is enabled
- **SC-011**: All URLs are verified via HTTP HEAD request and results are logged
- **SC-012**: URL verification timeouts after 5 seconds without hanging
- **SC-013**: Local network URLs (localhost, private IPs, file://) are skipped from verification
- **SC-014**: URL verification uses maximum 10 concurrent connections to prevent abuse
- **SC-015**: Only HTTP HEAD requests are sent (no GET/POST that fetch content)
- **SC-016**: Internal network ranges (non-RFC1918) are blocked from verification
- **SC-017**: Redirects beyond 1 hop are not followed
- **SC-018**: Response bodies are never captured or stored
- **SC-019**: Sensitive URL parameters (auth tokens, passwords) are redacted in logs

## Assumptions

- Users have bookmarks in standard Netscape Bookmark HTML format (Chrome, Firefox, Edge exports)
- Private IP detection will use standard RFC 1918 private address ranges
- File size limits remain at 10MB maximum for the input file
- The parser will continue to reject javascript: and data: URLs for security
- Bookmark themes/categories will be applied after deduplication is complete
- IP address detection happens before theme classification to allow proper categorization
- Security validation runs before any other processing to ensure compromised URLs are flagged early
- URLs containing suspicious patterns are logged but not blocked from processing (warning-only approach for backward compatibility)