# Contracts: 001-bookmarks-manager
## Parser Contract
| Input | Output | Edge Cases |
|-------|--------|------------|
| Chrome HTML export | List[Bookmark] | Missing titles → use domain |
| Firefox HTML export | List[Bookmark] | Malformed URLs → skip |
| Edge HTML export | List[Bookmark] | Invalid HTML → raise error |
## API Contract
| Provider | Request | Response | Timeout |
|----------|---------|----------|---------|
| HuggingFace | POST with text | JSON with category | 30s |
| Ollama | POST with prompt | JSON with text | 60s |
## Output Contract
| Input | Output Format | Browser Compatible |
|--------|--------------|------------------|
| Categorized bookmarks | Netscape HTML | Yes (Chrome/Firefox/Edge) |
| Theme list | HTML with DL/P | Yes |
## Performance Contract
| Metric | Target |
|--------|--------|
| 500 bookmarks import | <30s |
| 1000 bookmarks search | <5s |
| Zero-config startup | Yes |
| Categorization rate | >80% |
## CLI Contract
| Command | Exit Code | Output |
|---------|-----------|--------|
| `import file.html` | 0 | Output HTML file |
| `search "query"` | 0 | JSON results |
| `search "query"` | 1 | No bookmarks loaded |
| `import broken.html` | 2 | Parse error |