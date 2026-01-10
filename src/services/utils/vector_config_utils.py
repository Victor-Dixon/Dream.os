# <!-- SSOT Domain: integration -->
"""Utility helpers for vector configuration (SSOT)."""

from typing import Any


def load_simple_config(agent_id: str, config_path: str | None = None) -> dict[str, Any]:
    """Return simplified configuration for vector integration.

    Args:
        agent_id: Identifier for the agent using the vector integration.
        config_path: Optional path to a configuration file (currently unused).

    Returns:
        Configuration payload for the vector integration.

    Examples:
        >>> load_simple_config("alpha")["collection_name"]
        'agent_alpha'
    """
    return {
        "collection_name": f"agent_{agent_id}",
        "embedding_model": "default",
        "max_results": 10,
    }
