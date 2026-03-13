#!/usr/bin/env python3
"""Legacy-compatible Discord messaging command shim."""

from __future__ import annotations

import logging

try:
    import discord
except ImportError:  # pragma: no cover - used in test/mocked envs
    from .test_utils import get_mock_discord

    mock_discord, _ = get_mock_discord()
    discord = mock_discord

from typing import Any

logger = logging.getLogger(__name__)
_VALID_PRIORITIES = {"NORMAL", "HIGH", "CRITICAL"}


class MessagingCommands:
    """Compatibility command adapter expected by legacy tests/importers."""

    def __init__(self, bot: Any, messaging_controller: Any):
        self.bot = bot
        self.messaging_controller = messaging_controller
        self.logger = logger

    def _embed(self, title: str, description: str, color: int) -> discord.Embed:
        return discord.Embed(title=title, description=description, color=color)

    async def message_agent(
        self,
        ctx,
        agent_id: str,
        message: str,
        priority: str = "NORMAL",
    ) -> None:
        safe_priority = priority if priority in _VALID_PRIORITIES else "NORMAL"
        try:
            ok = await self.messaging_controller.send_agent_message(
                agent_id=agent_id,
                message=message,
                priority=safe_priority,
            )
            if ok:
                embed = self._embed("✅ Message Sent", f"Message delivered to {agent_id}.", 0x2ECC71)
                embed.add_field(name="Priority", value=safe_priority, inline=True)
                embed.add_field(name="Preview", value=(message[:200] or "(empty)"), inline=False)
            else:
                embed = self._embed("❌ Message Failed", f"Could not deliver message to {agent_id}.", 0xE74C3C)
        except Exception as exc:  # pragma: no cover - defensive path
            self.logger.error("message_agent failed: %s", exc)
            embed = self._embed("❌ Error", "Unexpected error while sending message.", 0xE74C3C)
        await ctx.send(embed=embed)

    async def broadcast(self, ctx, message: str, priority: str = "NORMAL") -> None:
        safe_priority = priority if priority in _VALID_PRIORITIES else "NORMAL"
        try:
            ok = await self.messaging_controller.broadcast_to_swarm(
                message=message,
                priority=safe_priority,
            )
            if ok:
                embed = self._embed("✅ Broadcast Sent", "Broadcast sent to swarm.", 0x2ECC71)
            else:
                embed = self._embed("❌ Broadcast Failed", "Broadcast could not be delivered.", 0xE74C3C)
        except Exception as exc:  # pragma: no cover - defensive path
            self.logger.error("broadcast failed: %s", exc)
            embed = self._embed("❌ Error", "Unexpected error while broadcasting.", 0xE74C3C)
        await ctx.send(embed=embed)

    async def agent_list(self, ctx) -> None:
        try:
            statuses = self.messaging_controller.get_agent_status()
            if not statuses:
                await ctx.send(embed=self._embed("❌ No Agents Found", "No active agent metadata available.", 0xE74C3C))
                return
            embed = self._embed("🤖 Available Agents", "Current known swarm agents:", 0x3498DB)
            for agent_id, status in statuses.items():
                active = "active" if status.get("active") else "idle"
                embed.add_field(name=agent_id, value=active, inline=True)
        except Exception as exc:  # pragma: no cover - defensive path
            self.logger.error("agent_list failed: %s", exc)
            embed = self._embed("❌ Error", "Unable to read agent list.", 0xE74C3C)
        await ctx.send(embed=embed)

    async def agent_interact(self, ctx) -> None:
        try:
            view = self.messaging_controller.create_agent_messaging_view()
            await ctx.send(content="Select an agent to interact with:", view=view)
        except Exception as exc:  # pragma: no cover - defensive path
            self.logger.error("agent_interact failed: %s", exc)
            await ctx.send(content="Error creating interface. Please try again.")

    async def swarm_status(self, ctx) -> None:
        try:
            view = self.messaging_controller.create_swarm_status_view()
            embed = await view._create_status_embed()
            await ctx.send(embed=embed, view=view)
        except Exception as exc:  # pragma: no cover - defensive path
            self.logger.error("swarm_status failed: %s", exc)
            await ctx.send(embed=self._embed("❌ Error", "Unable to load swarm status.", 0xE74C3C))


__all__ = ["MessagingCommands"]
