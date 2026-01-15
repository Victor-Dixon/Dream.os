"""
Discord Embeds - Agent Cellphone V2
==================================

SSOT Domain: discord

Utility functions for creating Discord embeds.
"""

from .embed_factory import cleanup_factory

def create_cleanup_embed(cleanup_data: dict) -> dict:
    """Create cleanup embed using factory."""
    return cleanup_factory.create_embed(cleanup_data)

