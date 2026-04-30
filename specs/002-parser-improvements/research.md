# Research: Bookmark Parser Improvements

## URL Validation Security

### Decision: Use urllib.parse + ipaddress (stdlib) + regex patterns

**Rationale**: The existing codebase uses BeautifulSoup (bs4). Adding new dependencies increases complexity. Using stdlib + custom patterns is sufficient and follows the "Extreme Simplicity" constitutional principle.

**Libraries Used**:
- `urllib.parse` (stdlib) - URL parsing
- `ipaddress` (stdlib) - RFC1918 private IP detection
- `re` (stdlib) - Pattern matching for SQL injection, XSS, path traversal

**Pattern Detection**:
- SQL injection: `('|OR|UNION|SELECT|DROP|--)`
- XSS: `(<script|javascript:|onerror|onload|<img)`
- Path traversal: `(\.\./|\.\.\\|/etc/|C:\\)`

**Local URL Detection**:
- `localhost`, `127.0.0.1`
- Private IPs: `192.168.0.0/16`, `10.0.0.0/8`, `172.16.0.0/12`
- `file://` scheme

---

## HTTP HEAD Verification

### Decision: Use httpx for async batch processing

**Rationale**: httpx provides better async support than requests. It handles connection pooling and has built-in timeout handling.

**Configuration**:
- Timeout: 5 seconds total (3s connect, 5s read)
- Max redirects: 1 hop (prevent redirect scanning)
- Concurrent connections: 10 (batch size)
- SSL verification: enabled (default)

**Security**:
- Only HEAD requests (no GET/POST to fetch body)
- No response body capture (only status code)
- Sensitive query params redacted in logs

---

## URL Deduplication

### Decision: Normalize + hash-based set deduplication

**Rationale**: For bookmark collections (typically <10K URLs), Python set with normalization is efficient and simple.

**Normalization Steps**:
1. Lowercase scheme and host
2. Remove trailing slash
3. Remove default ports (:80, :443)
4. Normalize path (resolve /./ and /../)
5. Keep query params as-is (include in comparison)

**Algorithm**:
1. Parse URL with urllib.parse
2. Apply normalization rules
3. Use normalized URL as key in set
4. Keep first occurrence, discard duplicates

---

## Alternatives Considered

| Alternative | Reason for Rejection |
|-------------|---------------------|
| urlps library | Additional dependency, overkill for this use case |
| ssrf-protect library | Additional dependency, stdlib sufficient |
| Bloom filters | Overkill for typical bookmark file size |
| requests library | httpx has better async support |
| Database storage | Not needed, in-memory sufficient |