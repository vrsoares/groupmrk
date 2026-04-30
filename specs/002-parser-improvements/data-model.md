# Data Model: Bookmark Parser Improvements

## Entities

### 1. URL (Value Object)

Represents a validated and normalized URL string.

| Field | Type | Validation | Description |
|-------|------|------------|-------------|
| original | str | Required, non-empty | Original URL from bookmark |
| normalized | str | Derived | Lowercase, no trailing slash |
| scheme | str | In: http, https, file | URL scheme |
| host | str | Required | Domain or IP address |
| is_local | bool | Derived | True if localhost/private IP/file |
| is_ip | bool | Derived | True if host is IP address |

### 2. Bookmark (Entity)

A single saved link with validation status.

| Field | Type | Validation | Description |
|-------|------|------------|-------------|
| title | str | Required | Bookmark title (URL fallback if empty) |
| url | URL | Required, valid | Validated URL object |
| add_date | datetime | Optional | When bookmark was created |
| icon | str | Optional | Favicon icon |
| original_folder | str | Optional | Browser folder name |
| theme | str | Optional | AI-assigned theme |
| validation_status | ValidationResult | Derived | valid/invalid/unreachable |

### 3. ValidationResult (Value Object)

Result of URL security validation.

| Field | Type | Description |
|-------|------|-------------|
| is_valid | bool | True if URL passes validation |
| is_suspicious | bool | True if URL has warning patterns |
| reason | str | Rejection reason or warning type |
| patterns_found | list[str] | List of suspicious patterns matched |

### 4. URLVerificationResult (Value Object)

Result of HTTP HEAD verification.

| Field | Type | Description |
|-------|------|-------------|
| status_code | int | HTTP status code (0 if failed) |
| is_reachable | bool | True if HEAD returned 2xx/3xx |
| error_type | str | timeout/connection/ssl/none |
| verification_skipped | bool | True if local network URL |

### 5. BookmarkCollection (Aggregate Root)

Container holding all bookmarks with processing state.

| Field | Type | Description |
|-------|------|-------------|
| bookmarks | list[Bookmark] | All bookmarks |
| invalid_urls | list[InvalidURLLog] | URLs that failed validation |
| unreachable_urls | list[str] | URLs that failed verification |
| metadata | CollectionMetadata | Processing statistics |

### 6. InvalidURLLog (Value Object)

Log entry for security review.

| Field | Type | Description |
|-------|------|-------------|
| url | str | Invalid URL string |
| reason | str | Why it was rejected |
| timestamp | datetime | When detected |
| original_folder | str | Source folder context |

### 7. CollectionMetadata (Value Object)

Statistics about the collection.

| Field | Type | Description |
|-------|------|-------------|
| total_count | int | Total bookmarks parsed |
| valid_count | int | URLs that passed validation |
| invalid_count | int | URLs with security issues |
| unreachable_count | int | URLs that failed HEAD verification |
| duplicate_count | int | Duplicates removed |
| local_network_count | int | Local/private URLs found |

## Key Relationships

```
BookmarkCollection (1) ---> (many) Bookmark
                            |
                            +---> URL (value object)
                            +---> ValidationResult (value object)
                            +---> URLVerificationResult (value object)

BookmarkCollection (1) ---> (many) InvalidURLLog
```

## State Transitions

### Bookmark Processing Pipeline

1. **Parsing** → Raw HTML to Bookmark (with original URL)
2. **Validation** → Bookmark with ValidationResult (security check)
3. **Deduplication** → BookmarkCollection (remove duplicates)
4. **Categorization** → Bookmark with theme (local network, IP-based)
5. **Verification** → Bookmark with URLVerificationResult (HEAD check)
6. **Output** → Final collection with metadata

## Validation Rules

| Rule | FR Reference | Description |
|------|---------------|-------------|
| Empty URL rejected | FR-002 | URL must not be empty or whitespace |
| Invalid scheme rejected | FR-003 | Only http, https, file allowed |
| SQL injection detected | FR-004 | Log warning, don't block |
| XSS detected | FR-005 | Log warning, don't block |
| Path traversal detected | FR-006 | Log warning, don't block |
| Invalid characters detected | FR-007 | Reject with reason |