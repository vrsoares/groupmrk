# Research: 001-bookmarks-manager

## HuggingFace Inference API
- Endpoint: `https://api-inference.huggingface.co/models/<model>/v1/`
- No API key required (free tier)
- Rate limit: ~30 req/min for free tier
- Recommended models for text classification:
  - `facebook/bart-large-mnli` (zero-shot classification)
  - `typeform/distilbert-base-uncased-mnli` (lighter alternative)

## LangGraph Architecture
- StateGraph with custom state (bookmarks list + theme assignments)
- Agent nodes: ThemeAgent(max 10) configured via `max_themes` CLI flag
- Orchestrator: State node that coordinates agent execution
- Edges: Conditional routing based on bookmark count

## Browser HTML Format (Netscape)
- `<DL><P>` for folder containers
- `<DT><H3>` for folder headers
- `<DT><A HREF="..." ADD_DATE="..." ICON="...">` for bookmarks
- Folders nested via DL structure

## Ollama Integration
- Default endpoint: `http://localhost:11434`
- API: POST `/api/generate` with `model` and `prompt`
- Popular models: `llama3.2`, `mistral`, `phi3`
- Fallback triggered on connection error or 5xx response

## CLI Framework
- Click 8.x for user-friendly interface
- Typer as alternative (based on type hints)
- Recommendation: Click for simpler dependency tree