"""Returns the configured AI provider. Defaults to MockAIProvider."""
from functools import lru_cache

from app.ai.base import AIProvider


@lru_cache(maxsize=1)
def get_ai_provider() -> AIProvider:
    from app.config import settings

    provider = getattr(settings, "llm_provider", "mock")
    if provider == "openai":
        from app.ai.openai_provider import OpenAIProvider
        return OpenAIProvider()
    from app.ai.mock_provider import MockAIProvider
    return MockAIProvider()
