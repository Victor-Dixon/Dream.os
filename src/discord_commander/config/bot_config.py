#!/usr/bin/env python3
"""
Bot Configuration

=================

Configuration management for Discord bot.

V2 Compliance | Author: Agent-1 | Date: 2025-12-14
"""

import json
import logging
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.discord_commander.unified_discord_bot import UnifiedDiscordBot

logger = logging.getLogger(__name__)


class BotConfig:
    """Manages bot configuration."""

    def __init__(self, bot: "UnifiedDiscordBot"):
        """Initialize bot configuration."""
        self.bot = bot
        self.logger = logging.getLogger(__name__)
        self.discord_user_map = load_discord_user_map(self.logger)

    def get_developer_prefix(self, discord_user_id: str) -> str:
        """Get developer prefix from Discord user ID mapping."""
        return get_developer_prefix(discord_user_id, self.discord_user_map)


def load_discord_user_map(logger: logging.Logger) -> dict[str, str]:
    """Load Discord user ID to developer name mapping from profiles."""
    user_map = {}
    workspace_dir = Path("agent_workspaces")

    if workspace_dir.exists():
        user_map.update(_load_from_agent_profiles(workspace_dir, logger))

    config_file = Path("config/discord_user_map.json")
    if config_file.exists():
        user_map.update(_load_from_config_file(config_file, logger))

    return user_map


def _load_from_agent_profiles(workspace_dir: Path, logger: logging.Logger) -> dict[str, str]:
    """Load Discord user mappings from agent profiles."""
    user_map = {}
    for agent_dir in workspace_dir.iterdir():
        if agent_dir.is_dir() and agent_dir.name.startswith("Agent-"):
            profile_file = agent_dir / "profile.json"
            if profile_file.exists():
                try:
                    profile_data = json.loads(
                        profile_file.read_text(encoding="utf-8"))
                    discord_user_id = profile_data.get("discord_user_id")
                    developer_name = (
                        profile_data.get("discord_username") or
                        profile_data.get("developer_name")
                    )

                    if discord_user_id and developer_name:
                        user_map[str(discord_user_id)] = developer_name.upper()
                        logger.debug(
                            f"Loaded Discord mapping: {discord_user_id} → {developer_name}")
                except Exception as e:
                    logger.warning(f"Failed to load profile from {profile_file}: {e}")
    return user_map


def _load_from_config_file(config_file: Path, logger: logging.Logger) -> dict[str, str]:
    """Load Discord user mappings from config file."""
    user_map = {}
    try:
        config_data = json.loads(config_file.read_text(encoding="utf-8"))
        valid_mappings = {
            k: v for k, v in config_data.items()
            if not k.startswith("_") and isinstance(v, str)
        }
        user_map.update(valid_mappings)
        if valid_mappings:
            logger.info(f"Loaded {len(valid_mappings)} Discord user mappings from config")
    except Exception as e:
        logger.warning(f"Failed to load Discord user map config: {e}")
    return user_map


def get_developer_prefix(discord_user_id: str, user_map: dict[str, str]) -> str:
    """Get developer prefix from Discord user ID mapping."""
    developer_name = user_map.get(str(discord_user_id))
    if developer_name:
        if isinstance(developer_name, str):
            valid_prefixes = ['CHRIS', 'ARIA', 'VICTOR', 'CARYMN', 'CHARLES']
            developer_name_upper = developer_name.upper()
            if developer_name_upper in valid_prefixes:
                return f"[{developer_name_upper}]"
    return "[D2A]"

