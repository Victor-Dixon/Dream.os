#!/usr/bin/env python3
"""
<!-- SSOT Domain: integration -->

Twitch EventSub Webhook Server
==============================

Standalone Flask server for receiving Twitch EventSub webhooks.

Run this server to handle channel point redemptions.

Usage:
    python -m src.services.chat_presence.twitch_eventsub_server

V2 Compliance: <400 lines, single responsibility
Author: Agent-4 (Captain)
License: MIT
"""

import os
import sys
import logging
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from flask import Flask
from .twitch_eventsub_handler import create_eventsub_flask_app

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def on_redemption_callback(user_name: str, event_data: dict) -> None:
    """
    Callback when a reward is redeemed.
    
    Can be used to log, notify Discord, etc.
    """
    reward_title = event_data.get("reward", {}).get("title", "Unknown")
    logger.info(f"🎁 Redemption processed: {user_name} → {reward_title}")


def main():
    """Run EventSub webhook server."""
<<<<<<< HEAD
    # Get webhook secret from environment, use default for development
    webhook_secret = os.getenv("TWITCH_EVENTSUB_WEBHOOK_SECRET", "dev-webhook-secret-12345")

=======
    # Get webhook secret from environment
    webhook_secret = os.getenv("TWITCH_EVENTSUB_WEBHOOK_SECRET")
    
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
    if not webhook_secret:
        logger.error(
            "❌ TWITCH_EVENTSUB_WEBHOOK_SECRET environment variable not set!\n"
            "Set it with: export TWITCH_EVENTSUB_WEBHOOK_SECRET='your-secret'"
        )
        sys.exit(1)
    
    # Get port from environment (default: 5000)
    port = int(os.getenv("PORT", "5000"))
    host = os.getenv("HOST", "0.0.0.0")
    
    # Create Flask app
    app = create_eventsub_flask_app(
        webhook_secret=webhook_secret,
        on_redemption=on_redemption_callback
    )
    
    logger.info("🚀 Starting Twitch EventSub webhook server...")
    logger.info(f"📡 Listening on {host}:{port}")
    logger.info(f"🔗 Webhook endpoint: http://{host}:{port}/twitch/eventsub")
    logger.info("⚠️  For production, use a reverse proxy (nginx) with HTTPS")
    
    # Run server
    app.run(host=host, port=port, debug=False)


if __name__ == "__main__":
    main()

