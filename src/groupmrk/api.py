"""API clients for LLM integration.

Clients for HuggingFace Inference API and Ollama.
Includes mock client for testing without API calls.

Clientes para HuggingFace Inference API e Ollama.
Inclui cliente mock para testes sem chamadas de API.

Security considerations / Consideracoes de seguranca:
- Never log full URLs with query parameters (may contain tokens)
- Sanitize prompts to prevent prompt injection
- Validate LLM output before using in code
- Implement rate limiting for API calls
"""

import logging
import os
import random
from abc import ABC, abstractmethod
from typing import Optional

logger = logging.getLogger(__name__)


class LLMClient(ABC):
    """Abstract base class for LLM clients."""

    @abstractmethod
    def classify_theme(self, title: str, url: str) -> str:
        """Classify a bookmark into a theme."""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if the client is available."""
        pass


class HuggingFaceClient(LLMClient):
    """HuggingFace Inference API client (no API key required)."""

    MODEL_ID = "facebook/bart-large-mnli"

    def __init__(self):
        from huggingface_hub import InferenceClient

        self._client = InferenceClient(model=self.MODEL_ID)
        self._candidate_labels = [
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
            "Uncategorized",
        ]

    def classify_theme(self, title: str, url: str) -> str:
        """Classify bookmark theme using zero-shot classification."""
        logger.debug(f"Classifying bookmark: {title[:30]}...")
        text = f"Title: {title}\nURL: {url}"

        try:
            logger.debug("Calling HuggingFace API for classification")
            result = self._client.zero_shot_classification(
                text, self._candidate_labels
            )
            if result and hasattr(result, "labels") and result.labels:
                label = result.labels[0]
                logger.info(f"Classification result: {label}")
                return label
        except Exception as e:
            logger.warning(f"HuggingFace API error: {e}")

        logger.info("Classification fallback: Uncategorized")
        return "Uncategorized"

    def is_available(self) -> bool:
        """Check if HuggingFace API is available."""
        logger.info("Checking HuggingFace API availability")
        try:
            result = self._client.zero_shot_classification(
                "test", ["test"]
            )
            available = result is not None
            logger.info(f"HuggingFace API available: {available}")
            return available
        except Exception as e:
            logger.warning(f"HuggingFace API check failed: {e}")
            return False


class MockClient(LLMClient):
    """Mock LLM client for testing without API calls."""

    THEMES = [
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

    def __init__(self):
        logger.info("MockClient initialized (no real API calls)")

    def classify_theme(self, title: str, url: str) -> str:
        """Return a random theme for testing."""
        theme = random.choice(self.THEMES)
        logger.debug(f"Mock classification: '{title[:20]}...' -> {theme}")
        return theme

    def is_available(self) -> bool:
        """Always available."""
        logger.info("MockClient always available")
        return True


class OllamaClient(LLMClient):
    """Ollama local LLM client."""

    def __init__(self, endpoint: str = "http://localhost:11434", model: str = "llama3.2"):
        self._endpoint = endpoint
        self._model = model

    def classify_theme(self, title: str, url: str) -> str:
        """Classify bookmark theme using local Ollama model."""
        logger.debug(f"Ollama classifying: {title[:30]}...")
        import requests

        prompt = f"""Classify this bookmark into one of these categories:
Development, Programming, Tutorials, Documentation, News, Entertainment, Technology, Science, Finance, Shopping, Health, Education, Social, Work, Tools, Reference, Uncategorized

Bookmark: Title: {title} URL: {url}

Respond with only the category name."""

        try:
            logger.debug(f"Calling Ollama at {self._endpoint}")
            response = requests.post(
                f"{self._endpoint}/api/generate",
                json={"model": self._model, "prompt": prompt, "stream": False},
                timeout=30,
            )
            if response.status_code == 200:
                result = response.json()
                text = result.get("response", "").strip()
                categories = [
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
                    "Uncategorized",
                ]
                for cat in categories:
                    if cat.lower() in text.lower():
                        logger.info(f"Ollama classification: {cat}")
                        return cat
        except Exception as e:
            logger.warning(f"Ollama classification error: {e}")

        logger.info("Ollama fallback: Uncategorized")
        return "Uncategorized"

    def is_available(self) -> bool:
        """Check if Ollama is running."""
        logger.info(f"Checking Ollama availability at {self._endpoint}")
        import requests

        try:
            response = requests.get(f"{self._endpoint}/api/tags", timeout=5)
            available = response.status_code == 200
            logger.info(f"Ollama available: {available}")
            return available
        except Exception as e:
            logger.warning(f"Ollama check failed: {e}")
            return False


def get_client(
    provider: str = "huggingface", ollama_endpoint: Optional[str] = None, mock: bool = False
) -> LLMClient:
    """Get an LLM client based on provider."""
    logger.info(f"Getting LLM client: provider={provider}, mock={mock}")

    if mock:
        logger.info("Using MockClient for testing")
        return MockClient()

    if provider == "ollama":
        logger.info("Attempting Ollama client")
        client = OllamaClient(endpoint=ollama_endpoint or "http://localhost:11434")
        if client.is_available():
            logger.info("Ollama client selected")
            return client
        logger.info("Ollama not available, falling back to HuggingFace")

    logger.info("Attempting HuggingFace client")
    hf_client = HuggingFaceClient()
    if hf_client.is_available():
        logger.info("HuggingFace client selected")
        return hf_client

    logger.error("No LLM client available")
    raise RuntimeError("No LLM client available")