"""Ollama integration stub for Jarvis."""

from typing import Any, Dict, List


class OllamaIntegration:
    """Minimal integration stub for Ollama."""

    def __init__(self, base_url: str | None = None):
        self.base_url = base_url or "http://localhost:11434"

    def list_models(self) -> List[Dict[str, Any]]:
        """Return an empty model list placeholder."""
        return []

    def generate(self, prompt: str, model: str | None = None) -> Dict[str, Any]:
        """Return a placeholder response."""
        return {"model": model or "unknown", "response": ""}
