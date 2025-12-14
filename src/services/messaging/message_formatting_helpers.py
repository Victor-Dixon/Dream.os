#!/usr/bin/env python3
"""
Message Formatting Helpers - Messaging Infrastructure
====================================================

<!-- SSOT Domain: integration -->

Helper functions for message formatting.
Extracted from message_formatters.py for V2 compliance.

V2 Compliance | Author: Agent-1 | Date: 2025-12-14
"""

from __future__ import annotations


def format_multi_agent_request_body(
    message: str,
    collector_id: str,
    request_id: str,
    recipient_count: int,
    timeout_minutes: int,
) -> str:
    """Format the body of multi-agent request message."""
    return f"""{message}

---
📋 **MULTI-AGENT REQUEST** - Response Collection Active
---

**How to Respond:**
1. This is a MULTI-AGENT REQUEST - your response will be combined with other agents
2. Respond normally in this chat (your response will be collected automatically)
3. Collector ID: `{collector_id}`
4. Request ID: `{request_id}`
5. Waiting for {recipient_count} agent(s) to respond
6. Timeout: {timeout_minutes} minutes

**Response Format:**
Just type your response normally. The system will automatically:
- Collect your response
- Combine with other agents' responses
- Send 1 combined message to the sender

**Note:** This is different from normal messages - responses are collected and combined!
🐝 WE. ARE. SWARM. ⚡🔥"""


def format_broadcast_instructions() -> str:
    """Format broadcast message instructions."""
    return """
---
📨 **BROADCAST MESSAGE** - Standard Response
---

**How to Respond:**
1. This is a NORMAL/BROADCAST message
2. Respond directly in this chat (normal response, not collected)
3. Your response goes directly to the sender
4. No response collection - standard one-to-one messaging

**Response Format:**
Just type your response normally. It will be sent directly to the sender.

**Note:** This is a standard message - respond normally, no special handling needed!
🐝 WE. ARE. SWARM. ⚡🔥"""


def format_discord_instructions() -> str:
    """Format Discord message instructions."""
    return """
---
📨 **DISCORD MESSAGE [D2A]** - Respond in Discord
---

**How to Respond:**
1. This is a DISCORD message ([D2A])
2. **CRITICAL**: Your response must be sent BACK to Discord
3. **Use Discord Router**: `python tools/post_to_discord_router.py --agent <your-agent-id> --message "<your response>"`
4. **Example**: `python tools/post_to_discord_router.py --agent Agent-4 --message "Response to Discord user"`
5. Do NOT just respond in this chat - Discord user is waiting for response in Discord

**Response Format:**
Post your response to Discord router channel using post_to_discord_router.py script.

**Note:** Discord messages [D2A] require responses to be posted back to Discord channel!
🐝 WE. ARE. SWARM. ⚡🔥"""


def format_normal_instructions() -> str:
    """Format normal message instructions."""
    return """
---
📨 **STANDARD MESSAGE** - Normal Response
---

**How to Respond:**
1. This is a NORMAL message
2. Respond directly in this chat (normal response)
3. Your response goes directly to the sender
4. No response collection - standard one-to-one messaging

**Response Format:**
Just type your response normally. It will be sent directly to the sender.

**Note:** This is a standard message - respond normally, no special handling needed!
🐝 WE. ARE. SWARM. ⚡🔥"""


def is_discord_message(message: str) -> bool:
    """Check if message is from Discord."""
    return (
        message.strip().startswith("[D2A]") or
        "\n[D2A]" in message or
        (message.startswith("[D2A]") and len(message) > 5)
    )





