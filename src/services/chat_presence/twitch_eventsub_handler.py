#!/usr/bin/env python3
"""
<!-- SSOT Domain: integration -->

Twitch EventSub Webhook Handler
================================

Handles Twitch EventSub webhook notifications for channel point redemptions.

V2 Compliance: <400 lines, single responsibility
Author: Agent-4 (Captain)
License: MIT
"""

import hashlib
import hmac
import json
import logging
from typing import Dict, Any, Optional, Callable, Tuple
from datetime import datetime
from flask import Flask, request, jsonify

from .channel_points_rewards import (
    get_reward_by_id,
    get_reward_by_name,
    ChannelPointReward,
)

logger = logging.getLogger(__name__)


class TwitchEventSubHandler:
    """
    Handles Twitch EventSub webhook events.
    
    Supports channel point redemption notifications.
    """
    
    def __init__(
        self,
        webhook_secret: str,
        on_redemption: Optional[Callable[[str, Dict[str, Any]], str]] = None,
    ):
        """
        Initialize EventSub handler.
        
        Args:
            webhook_secret: Webhook secret from Twitch (for signature verification)
            on_redemption: Callback when redemption is processed (user_name, redemption_data) -> response_message
        """
        self.webhook_secret = webhook_secret.encode('utf-8')
        self.on_redemption = on_redemption
        self.last_redemptions: Dict[str, datetime] = {}  # For rate limiting
        
    def verify_signature(self, signature: str, body: bytes) -> bool:
        """
        Verify Twitch webhook signature.
        
        Args:
            signature: Signature header from Twitch (format: sha256=<hash>)
            body: Raw request body
            
        Returns:
            True if signature is valid
        """
        if not signature or not signature.startswith("sha256="):
            logger.warning("Invalid signature format")
            return False
            
        expected_hash = signature[7:]  # Remove "sha256=" prefix
        calculated_hash = hmac.new(
            self.webhook_secret,
            body,
            hashlib.sha256
        ).hexdigest()
        
        # Use constant-time comparison to prevent timing attacks
        return hmac.compare_digest(expected_hash, calculated_hash)
    
    def handle_webhook(self, request_obj) -> Tuple[Dict[str, Any], int]:
        """
        Handle incoming EventSub webhook request.
        
        Args:
            request_obj: Flask request object
            
        Returns:
            Tuple of (response_dict, status_code)
        """
        # Get signature from headers
        signature = request_obj.headers.get("Twitch-Eventsub-Message-Signature")
        if not signature:
            logger.warning("Missing signature header")
            return {"error": "Missing signature"}, 401
        
        # Get raw body for signature verification
        body = request_obj.get_data()
        
        # Verify signature
        if not self.verify_signature(signature, body):
            logger.warning("Invalid webhook signature")
            return {"error": "Invalid signature"}, 401
        
        # Parse JSON payload
        try:
            payload = json.loads(body.decode('utf-8'))
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON payload: {e}")
            return {"error": "Invalid JSON"}, 400
        
        # Handle subscription verification (initial challenge)
        message_type = request_obj.headers.get("Twitch-Eventsub-Message-Type")
        
        if message_type == "webhook_callback_verification":
            challenge = payload.get("challenge")
            if challenge:
                logger.info("✅ Webhook verification successful")
                return {"challenge": challenge}, 200
            else:
                logger.error("Missing challenge in verification payload")
                return {"error": "Missing challenge"}, 400
        
        # Handle notification (actual event)
        if message_type == "notification":
            return self._handle_notification(payload)
        
        # Handle revocation
        if message_type == "revocation":
            logger.warning("Webhook subscription revoked")
            return {"status": "revocation received"}, 200
        
        logger.warning(f"Unknown message type: {message_type}")
        return {"error": "Unknown message type"}, 400
    
    def _handle_notification(self, payload: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
        """
        Handle notification event.
        
        Args:
            payload: EventSub notification payload
            
        Returns:
            Tuple of (response_dict, status_code)
        """
        event = payload.get("event", {})
        subscription = payload.get("subscription", {})
        event_type = subscription.get("type", "")
        
        # Handle channel points redemption
        if event_type == "channel.channel_points_custom_reward_redemption.add":
            return self._handle_redemption(event)
        
        logger.info(f"Unhandled event type: {event_type}")
        return {"status": "event received, not handled"}, 200
    
    def _handle_redemption(
        self,
        event_data: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], int]:
        """
        Handle channel point redemption event.
        
        Args:
            event_data: Redemption event data from Twitch
            
        Returns:
            Tuple of (response_dict, status_code)
        """
        redemption_id = event_data.get("id", "")
        reward_id = event_data.get("reward", {}).get("id", "")
        reward_title = event_data.get("reward", {}).get("title", "")
        user_id = event_data.get("user_id", "")
        user_name = event_data.get("user_login", "")
        user_input = event_data.get("user_input", "").strip()
        
        logger.info(
            f"Channel point redemption: {user_name} redeemed '{reward_title}' "
            f"(reward_id={reward_id}, redemption_id={redemption_id})"
        )
        
        # Find reward configuration
        reward_config = get_reward_by_id(reward_id)
        if not reward_config:
            # Try matching by name (Twitch doesn't always give us the ID we set)
            reward_config = get_reward_by_name(reward_title)
        
        if not reward_config:
            logger.warning(
                f"Unknown reward: {reward_title} (id={reward_id}). "
                "Make sure reward is configured in channel_points_rewards.py"
            )
            return {
                "status": "reward not configured",
                "reward_title": reward_title,
                "reward_id": reward_id,
            }, 200
        
        # Check rate limiting
        if reward_config.rate_limit_seconds > 0:
            last_time = self.last_redemptions.get(user_id)
            if last_time:
                from datetime import timedelta
                time_since = (datetime.now() - last_time).total_seconds()
                if time_since < reward_config.rate_limit_seconds:
                    remaining = int(reward_config.rate_limit_seconds - time_since)
                    logger.info(
                        f"Rate limit: {user_name} must wait {remaining}s "
                        f"before redeeming '{reward_title}' again"
                    )
                    return {
                        "status": "rate_limited",
                        "message": f"Please wait {remaining} seconds",
                    }, 429
        
        # Check if approval required (future: implement approval queue)
        if reward_config.requires_approval:
            logger.info(f"Reward '{reward_title}' requires approval (not yet implemented)")
            # Future: Add to approval queue
        
        # Execute reward handler
        try:
            response_message = reward_config.handler_func(
                user_name=user_name,
                user_id=user_id,
                redemption_id=redemption_id,
                reward_data={
                    "reward_id": reward_id,
                    "reward_title": reward_title,
                    "user_input": user_input,
                    "redemption_id": redemption_id,
                    "event_data": event_data,
                }
            )
            
            # Update rate limit tracking
            if reward_config.rate_limit_seconds > 0:
                self.last_redemptions[user_id] = datetime.now()
            
            # Call optional callback
            if self.on_redemption:
                try:
                    self.on_redemption(user_name, event_data)
                except Exception as e:
                    logger.error(f"Error in redemption callback: {e}", exc_info=True)
            
            logger.info(f"✅ Reward '{reward_title}' handled: {response_message}")
            
            return {
                "status": "success",
                "reward": reward_title,
                "user": user_name,
                "message": response_message,
            }, 200
            
        except Exception as e:
            logger.error(
                f"Error handling reward '{reward_title}': {e}",
                exc_info=True
            )
            return {
                "status": "error",
                "error": str(e),
            }, 500


def create_eventsub_flask_app(
    webhook_secret: str,
    on_redemption: Optional[Callable[[str, Dict[str, Any]], str]] = None,
) -> Flask:
    """
    Create Flask app for EventSub webhook endpoint.
    
    Args:
        webhook_secret: Webhook secret for signature verification
        on_redemption: Optional callback when redemption is processed
        
    Returns:
        Configured Flask app
    """
    app = Flask(__name__)
    handler = TwitchEventSubHandler(webhook_secret, on_redemption)
    
    @app.route("/twitch/eventsub", methods=["POST"])
    def eventsub_webhook():
        """EventSub webhook endpoint."""
        response, status_code = handler.handle_webhook(request)
        return jsonify(response), status_code
    
    @app.route("/twitch/eventsub", methods=["GET"])
    def eventsub_health():
        """Health check endpoint."""
        return jsonify({"status": "ok", "service": "twitch_eventsub"}), 200
    
    return app


__all__ = [
    "TwitchEventSubHandler",
    "create_eventsub_flask_app",
]

