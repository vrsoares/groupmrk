"""LangGraph orchestration for bookmark categorization.

LangGraph workflow for organizing bookmarks into theme categories.
Uses Orchestrator + Theme Agents pattern.

Fluxo LangGraph para organizar bookmarks em categorias de tema.
Usa padrao Orquestrador + Agentes de Tema.

Architecture / Arquitetura:
- Orchestrator: Coordinates theme agents, aggregates results
- Theme Agent: Classifies bookmarks into specific themes
- Max 10 themes (configurable) / Maximo 10 temas (configuravel)

This module implements the AI orchestration layer following
clean code principles with comprehensive documentation.
"""

import logging
from typing import TypedDict

from langgraph.graph import StateGraph, END

from .api import get_client, LLMClient
from .models import Bookmark, BookmarkCollection

logger = logging.getLogger(__name__)


class GraphState(TypedDict):
    """State for the LangGraph."""

    bookmarks: list[Bookmark]
    themes: dict[str, list[Bookmark]]
    categorized: list[dict]
    errors: list[str]


class ThemeAgent:
    """Theme Agent - classifies bookmarks into a specific theme."""

    def __init__(self, theme: str, client: LLMClient):
        self.theme = theme
        self.client = client

    def classify(self, bookmark: Bookmark) -> bool:
        """Check if bookmark belongs to this theme."""
        theme_lower = self.theme.lower()
        title_lower = bookmark.title.lower()
        url_lower = bookmark.url.lower()

        keywords = self._get_theme_keywords(theme_lower)
        for keyword in keywords:
            if keyword in title_lower or keyword in url_lower:
                return True

        classification = self.client.classify_theme(bookmark.title, bookmark.url)
        return classification.lower() == theme_lower

    def _get_theme_keywords(self, theme: str) -> list[str]:
        """Get keywords for a theme."""
        keywords_map = {
            "development": [
                "github",
                "git",
                "stackoverflow",
                "dev",
                "code",
                "programming",
            ],
            "programming": [
                "python",
                "javascript",
                "java",
                "cpp",
                "rust",
                "golang",
                "ruby",
            ],
            "tutorials": ["tutorial", "learn", "course", "guide", "how-to"],
            "documentation": ["docs", "documentation", "api", "reference"],
            "news": ["news", "blog", "article", "medium", "dev.to"],
            "entertainment": ["youtube", "netflix", "movie", "tv", "spotify"],
            "technology": ["tech", "technology", " gadgets", "software"],
            "science": ["science", "research", "arxiv", "physics"],
            "finance": ["finance", "stock", "crypto", "bank", "investment"],
            "shopping": ["shop", "amazon", "store", "buy", "product"],
            "health": ["health", "medical", "fitness", "wellness"],
            "education": ["edu", "university", "school", "course", "learn"],
            "social": ["twitter", "facebook", "instagram", "linkedin", "social"],
            "work": ["job", "career", "resume", "linkedin", "work"],
            "tools": ["tool", "utility", "converter", "generator"],
            "reference": ["docs", "wiki", "encyclopedia", "dictionary"],
        }
        return keywords_map.get(theme, [])


class Orchestrator:
    """Orchestrator Agent - coordinates theme agents."""

    def __init__(
        self,
        provider: str = "huggingface",
        max_themes: int = 10,
        ollama_endpoint: str | None = None,
        mock: bool = False,
    ):
        self.max_themes = max_themes
        self._client: LLMClient | None = None
        self._provider = provider
        self._ollama_endpoint = ollama_endpoint
        self._mock = mock

    def _get_client(self) -> LLMClient:
        """Get or create the LLM client."""
        if self._client is None:
            self._client = get_client(
                provider=self._provider,
                ollama_endpoint=self._ollama_endpoint,
                mock=self._mock
            )
        return self._client

    def organize(self, collection: BookmarkCollection) -> BookmarkCollection:
        """Organize bookmarks using LangGraph orchestration."""
        logger.info(f"Starting organization: {len(collection.bookmarks)} bookmarks, max_themes={self.max_themes}")

        client = self._get_client()
        logger.info("LLM client initialized")

        state: GraphState = {
            "bookmarks": collection.bookmarks.copy(),
            "themes": {},
            "categorized": [],
            "errors": [],
        }

        logger.info("Building LangGraph")
        graph = self._build_graph(client)

        logger.info("Invoking LangGraph for categorization")
        result = graph.invoke(state)
        logger.info("LangGraph invocation complete")

        logger.info("Assigning themes to bookmarks")
        for item in result.get("categorized", []):
            bookmark = item["bookmark"]
            theme = item["theme"]
            collection.assign_theme(bookmark, theme)

        collection.metadata.theme_count = len(collection.themes)
        collection.metadata.categorized_count = sum(
            len(t.bookmarks) for t in collection.themes.values()
        )

        logger.info(f"Organization complete: {len(collection.themes)} themes, {collection.metadata.categorized_count} categorized")
        return collection

    def _build_graph(self, client: LLMClient):
        """Build the LangGraph workflow."""
        graph = StateGraph(GraphState)

        graph.add_node("classify", lambda state: self._classify_node(state, client))

        graph.set_entry_point("classify")
        graph.add_edge("classify", END)

        return graph.compile()

    def _classify_node(self, state: GraphState, client: LLMClient) -> GraphState:
        """Classify all bookmarks."""
        bookmarks = state["bookmarks"]
        categorized = []
        themes: dict[str, list[Bookmark]] = {}

        available_themes = [
            "Development",
            "Programming",
            "Tutorials",
            "Documentation",
            "News",
            "Entertainment",
            "Technology",
            "Science",
            "Finance",
            "Shopping",
            "Health",
            "Education",
            "Social",
            "Work",
            "Tools",
            "Reference",
        ]

        for bookmark in bookmarks:
            best_theme = "Uncategorized"
            best_score = 0.0

            for theme in available_themes[: self.max_themes]:
                agent = ThemeAgent(theme, client)
                score = 1.0 if agent.classify(bookmark) else 0.0

                if score > best_score:
                    best_score = score
                    best_theme = theme

            if best_score == 0:
                classification = client.classify_theme(bookmark.title, bookmark.url)
                if classification in available_themes:
                    best_theme = classification

            categorized.append({"bookmark": bookmark, "theme": best_theme})

            if best_theme not in themes:
                themes[best_theme] = []
            themes[best_theme].append(bookmark)

        return {
            "bookmarks": bookmarks,
            "themes": themes,
            "categorized": categorized,
            "errors": [],
        }