"""Natural language search for bookmarks.

Search functionality for bookmark collections using keyword matching.
Provides relevance scoring and category grouping.

Funcionalidade de pesquisa para colecoes de favoritos usando
correspondencia de palavras-chave. Fornece pontuacao de relevancia
e agrupamento por categoria.

This module provides natural language search capabilities without
requiring an LLM - uses keyword-based scoring for fast results.
"""

import logging
import re
from collections import defaultdict

from .api import get_client
from .models import Bookmark, BookmarkCollection

logger = logging.getLogger(__name__)


class BookmarkSearch:
    """Search bookmarks using natural language."""

    def __init__(self, collection: BookmarkCollection):
        self.collection = collection

    def search(self, query: str, limit: int = 20) -> list[dict]:
        """Search bookmarks and return ranked results."""
        logger.info(f"Searching bookmarks: query='{query}', limit={limit}")
        query_lower = query.lower()
        query_terms = self._extract_terms(query_lower)
        logger.debug(f"Extracted search terms: {query_terms}")

        results = []
        for bookmark in self.collection.bookmarks:
            score = self._calculate_score(bookmark, query_lower, query_terms)
            if score > 0:
                results.append(
                    {
                        "bookmark": bookmark,
                        "score": score,
                        "explanation": self._explain_match(bookmark, query_terms),
                    }
                )

        results.sort(key=lambda x: x["score"], reverse=True)
        logger.info(f"Search complete: {len(results)} results found, returning top {limit}")
        return results[:limit]

    def _extract_terms(self, query: str) -> list[str]:
        """Extract searchable terms from query."""
        terms = re.findall(r"\b\w+\b", query)
        return [t for t in terms if len(t) > 2]

    def _calculate_score(
        self, bookmark: Bookmark, query: str, terms: list[str]
    ) -> float:
        """Calculate relevance score for a bookmark."""
        score = 0.0

        title_lower = bookmark.title.lower()
        url_lower = bookmark.url.lower()
        category = (bookmark.theme or bookmark.manual_category or "").lower()

        for term in terms:
            if term in title_lower:
                score += 3.0
            if term in url_lower:
                score += 1.0
            if term in category:
                score += 2.0

        if query in title_lower:
            score += 5.0
        if query in bookmark.url:
            score += 2.0

        return score

    def _explain_match(self, bookmark: Bookmark, terms: list[str]) -> str:
        """Generate explanation for why bookmark matched."""
        reasons = []

        title_lower = bookmark.title.lower()
        url_lower = bookmark.url.lower()
        category = bookmark.theme or bookmark.manual_category or "Uncategorized"

        matched_terms = [t for t in terms if t in title_lower or t in url_lower]
        if matched_terms:
            reasons.append(f"Matched: {', '.join(matched_terms[:3])}")

        if category != "Uncategorized":
            reasons.append(f"Category: {category}")

        return " | ".join(reasons) if reasons else "Relevance match"

    def group_by_category(self, results: list[dict]) -> dict[str, list[dict]]:
        """Group search results by category."""
        grouped = defaultdict(list)
        for result in results:
            category = result["bookmark"].effective_category
            grouped[category].append(result)
        return dict(grouped)