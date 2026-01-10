"""
Discord Webhook Posting Utilities.

<!-- SSOT Domain: trading_robot -->
"""

import requests


def post_to_discord(webhook_url: str, content: str) -> None:
    """Post a message to a Discord webhook."""
    response = requests.post(webhook_url, json={"content": content}, timeout=15)
    response.raise_for_status()
