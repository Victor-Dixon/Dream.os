#!/usr/bin/env python3
"""
Discord Tools - Agent Toolbelt V2
==================================

Discord bot and integration tools for agents.
Created based on Agent-3 Discord Commander session.

Author: Agent-3 (Infrastructure & DevOps) - Toolbelt Expansion
License: MIT
"""

import logging
import subprocess
from pathlib import Path
from typing import Any

from ..adapters.base_adapter import IToolAdapter, ToolResult, ToolSpec

logger = logging.getLogger(__name__)


class DiscordBotHealthTool(IToolAdapter):
    """Check if Discord bot is running and healthy."""

    def get_spec(self) -> ToolSpec:
        """Get tool specification."""
        return ToolSpec(
            name="discord.health",
            version="1.0.0",
            category="discord",
            summary="Check Discord Commander bot health and status",
            required_params=[],
            optional_params={},
        )

    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate parameters."""
        spec = self.get_spec()
        return spec.validate_params(params)

    def execute(self, params: dict[str, Any], context: dict[str, Any] | None = None) -> ToolResult:
        """Check Discord bot health."""
        try:
            # Check if process is running
            result = subprocess.run(
                ["powershell", "-Command", "Get-Process python | Select-String discord"],
                capture_output=True,
                text=True,
                timeout=5,
            )

            running = result.returncode == 0 and "discord" in result.stdout.lower()

            # Check for startup message in logs
            log_exists = False
            try:
                # Look for recent log entries
                log_exists = Path("logs/unified.log").exists()
            except:
                pass

            return ToolResult(
                success=True,
                output={
                    "bot_running": running,
                    "logs_available": log_exists,
                    "status": "HEALTHY" if running else "NOT_RUNNING",
                },
                exit_code=0,
            )

        except Exception as e:
            return ToolResult(success=False, output=None, error_message=str(e), exit_code=1)


class DiscordBotStartTool(IToolAdapter):
    """Start Discord Commander bot."""

    def get_spec(self) -> ToolSpec:
        """Get tool specification."""
        return ToolSpec(
            name="discord.start",
            version="1.0.0",
            category="discord",
            summary="Start Discord Commander bot in background",
            required_params=[],
            optional_params={},
        )

    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate parameters."""
        spec = self.get_spec()
        return spec.validate_params(params)

    def execute(self, params: dict[str, Any], context: dict[str, Any] | None = None) -> ToolResult:
        """Start Discord bot."""
        try:
            # Start bot in background
            if subprocess.sys.platform == "win32":
                subprocess.Popen(
                    ["python", "src/discord_commander/unified_discord_bot.py"],
                    creationflags=subprocess.CREATE_NEW_CONSOLE,
                )
            else:
                subprocess.Popen(
                    ["python", "src/discord_commander/unified_discord_bot.py"],
                    start_new_session=True,
                )

            return ToolResult(
                success=True,
                output={
                    "message": "Discord Commander started in background",
                    "instructions": "Check Discord for startup message. Use !gui to access messaging interface.",
                },
                exit_code=0,
            )

        except Exception as e:
            return ToolResult(success=False, output=None, error_message=str(e), exit_code=1)


class DiscordTestMessageTool(IToolAdapter):
    """Send test message via Discord bot."""

    def get_spec(self) -> ToolSpec:
        """Get tool specification."""
        return ToolSpec(
            name="discord.test",
            version="1.0.0",
            category="discord",
            summary="Send test message to verify Discord integration",
            required_params=[],
            optional_params={"agent": "Agent-1", "message": "Test message from Discord Commander"},
        )

    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate parameters."""
        spec = self.get_spec()
        return spec.validate_params(params)

    def execute(self, params: dict[str, Any], context: dict[str, Any] | None = None) -> ToolResult:
        """Send test message."""
        try:
            agent = params.get("agent", "Agent-1")
            message = params.get("message", "Test message from Discord Commander")

            # Use messaging CLI
            result = subprocess.run(
                [
                    "python",
                    "-m",
                    "src.services.messaging_cli",
                    "--agent",
                    agent,
                    "--message",
                    message,
                    "--priority",
                    "regular",
                ],
                capture_output=True,
                text=True,
                timeout=30,
            )

            # Check for success indicators
            output = result.stdout + result.stderr
            success = "Message sent to" in output or "Coordinates validated" in output

            return ToolResult(
                success=success,
                output={
                    "agent": agent,
                    "message_sent": success,
                    "output": output[:500] if output else "No output",
                },
                exit_code=0 if success else 1,
            )

        except Exception as e:
            return ToolResult(success=False, output=None, error_message=str(e), exit_code=1)


__all__ = ["DiscordBotHealthTool", "DiscordBotStartTool", "DiscordTestMessageTool"]
