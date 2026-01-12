#!/usr/bin/env python3
"""
Discord Manager Tool - Unified Discord Integration Management
Automatically configures Discord bot, channels, and webhooks for agent communication
"""

import os
import json
import asyncio
import discord
from discord.ext import commands
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DiscordManager:
    """Unified Discord management for agent communication"""

    def __init__(self, token: Optional[str] = None):
        self.token = token or self._load_token_from_env()
        self.bot = None
        self.guild = None
        self.channels = {}
        self.webhooks = {}
        self.config = {}

    def _load_token_from_env(self) -> Optional[str]:
        """Load Discord token from environment variables or .env file"""
        # First check environment variables
        token = os.getenv('DISCORD_TOKEN') or os.getenv('DISCORD_BOT_TOKEN')
        if token:
            return token

        # Try to load from .env file
        env_file = Path(__file__).resolve().parents[1] / ".env"
        if env_file.exists():
            try:
                with open(env_file, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith('DISCORD_TOKEN=') or line.startswith('DISCORD_BOT_TOKEN='):
                            # Extract token value (remove quotes if present)
                            token_value = line.split('=', 1)[1].strip()
                            if token_value.startswith('"') and token_value.endswith('"'):
                                token_value = token_value[1:-1]
                            elif token_value.startswith("'") and token_value.endswith("'"):
                                token_value = token_value[1:-1]
                            return token_value
            except Exception as e:
                logger.warning(f"Could not read .env file: {e}")

        return None

    async def initialize_bot(self) -> bool:
        """Initialize Discord bot and gather configuration"""
        if not self.token:
            logger.error("❌ No Discord token provided")
            return False

        try:
            # Create bot with necessary intents
            intents = discord.Intents.default()
            intents.guilds = True
            intents.messages = True
            intents.message_content = True

            self.bot = commands.Bot(command_prefix='!', intents=intents)

            @self.bot.event
            async def on_ready():
                logger.info(f"✅ Discord bot connected as {self.bot.user}")
                await self._gather_guild_info()
                await self._create_channels_if_needed()
                await self._setup_webhooks()
                await self.bot.close()  # Close after setup

            await self.bot.start(self.token)
            return True

        except Exception as e:
            logger.error(f"❌ Failed to initialize Discord bot: {e}")
            return False

    async def _gather_guild_info(self):
        """Gather information about the Discord guild"""
        if not self.bot or not self.bot.guilds:
            logger.warning("⚠️ No guilds found for bot")
            return

        # Use the first guild (assuming single guild setup)
        self.guild = self.bot.guilds[0]
        logger.info(f"📊 Connected to guild: {self.guild.name} ({self.guild.id})")

        # Get existing channels
        for channel in self.guild.channels:
            if isinstance(channel, discord.TextChannel):
                channel_name = channel.name.lower()
                channel_id = str(channel.id)

                # Map common channel patterns
                if 'infrastructure' in channel_name or 'infra' in channel_name:
                    self.channels['infrastructure'] = channel_id
                elif 'architecture' in channel_name or 'arch' in channel_name:
                    self.channels['architecture'] = channel_id
                elif 'coordination' in channel_name or 'coord' in channel_name:
                    self.channels['coordination'] = channel_id
                elif 'a2a' in channel_name:
                    self.channels['a2a_coordination'] = channel_id
                elif 'agent' in channel_name and any(str(i) in channel_name for i in range(1, 9)):
                    # Extract agent number
                    for i in range(1, 9):
                        if f'agent{i}' in channel_name:
                            self.channels[f'agent{i}'] = channel_id
                            break

        logger.info(f"📋 Found {len(self.channels)} configured channels")

    async def _create_channels_if_needed(self):
        """Create missing channels if they don't exist"""
        required_channels = {
            'infrastructure': '🏗️-infrastructure',
            'architecture': '🏛️-architecture',
            'coordination': '🤝-coordination',
            'a2a_coordination': '🐝-a2a-coordination'
        }

        for key, channel_name in required_channels.items():
            if key not in self.channels:
                try:
                    channel = await self.guild.create_text_channel(channel_name)
                    self.channels[key] = str(channel.id)
                    logger.info(f"✅ Created channel: {channel_name} ({channel.id})")
                except Exception as e:
                    logger.error(f"❌ Failed to create channel {channel_name}: {e}")

        # Create agent-specific channels if they don't exist
        for i in range(1, 9):
            agent_key = f'agent{i}'
            if agent_key not in self.channels:
                try:
                    channel_name = f'🤖-agent-{i}'
                    channel = await self.guild.create_text_channel(channel_name)
                    self.channels[agent_key] = str(channel.id)
                    logger.info(f"✅ Created agent channel: {channel_name} ({channel.id})")
                except Exception as e:
                    logger.error(f"❌ Failed to create agent channel {i}: {e}")

    async def _setup_webhooks(self):
        """Setup webhooks for agent communication"""
        for agent_key, channel_id in self.channels.items():
            if agent_key.startswith('agent'):
                try:
                    channel = self.bot.get_channel(int(channel_id))
                    if channel:
                        # Check for existing webhook
                        existing_webhooks = await channel.webhooks()
                        webhook_name = f"Agent-{agent_key.replace('agent', '')}-Webhook"

                        existing_webhook = None
                        for webhook in existing_webhooks:
                            if webhook.name == webhook_name:
                                existing_webhook = webhook
                                break

                        if not existing_webhook:
                            webhook = await channel.create_webhook(name=webhook_name)
                            self.webhooks[agent_key] = webhook.url
                            logger.info(f"✅ Created webhook for {agent_key}: {webhook_name}")
                        else:
                            self.webhooks[agent_key] = existing_webhook.url
                            logger.info(f"✅ Found existing webhook for {agent_key}")

                except Exception as e:
                    logger.error(f"❌ Failed to setup webhook for {agent_key}: {e}")

    def generate_env_config(self) -> Dict[str, str]:
        """Generate complete environment configuration"""
        config = {
            'DISCORD_BOT_TOKEN': self.token,
            'DISCORD_INFRASTRUCTURE_CHANNEL_ID': self.channels.get('infrastructure', ''),
            'DISCORD_ARCHITECTURE_CHANNEL_ID': self.channels.get('architecture', ''),
            'DISCORD_COORDINATION_CHANNEL_ID': self.channels.get('coordination', ''),
            'DISCORD_A2A_COORDINATION_CHANNEL_ID': self.channels.get('a2a_coordination', ''),
        }

        # Add agent webhooks
        for i in range(1, 5):  # First 4 agents as requested
            agent_key = f'agent{i}'
            webhook_url = self.webhooks.get(agent_key, '')
            config[f'DISCORD_AGENT{i}_WEBHOOK_URL'] = webhook_url

        return config

    def save_env_file(self, config: Dict[str, str], filename: str = ".env.discord") -> bool:
        """Save configuration to environment file"""
        try:
            env_content = "# Discord Configuration - Auto-generated by Discord Manager\n"
            env_content += "# Generated: " + str(datetime.now().isoformat()) + "\n\n"

            for key, value in config.items():
                if value:  # Only include non-empty values
                    env_content += f'{key}="{value}"\n'

            with open(filename, 'w') as f:
                f.write(env_content)

            logger.info(f"✅ Environment configuration saved to {filename}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to save environment file: {e}")
            return False

    def display_configuration(self, config: Dict[str, str]):
        """Display the generated configuration"""
        print("\n🐝 DISCORD CONFIGURATION GENERATED")
        print("=" * 50)

        print("📊 CHANNEL CONFIGURATION:")
        for key, value in config.items():
            if 'CHANNEL_ID' in key and value:
                channel_name = key.replace('DISCORD_', '').replace('_CHANNEL_ID', '').lower()
                print(f"  • {key}: {value} ({channel_name})")

        print("\n🔗 WEBHOOK CONFIGURATION:")
        for key, value in config.items():
            if 'WEBHOOK_URL' in key and value:
                agent_num = key.replace('DISCORD_AGENT', '').replace('_WEBHOOK_URL', '')
                print(f"  • Agent {agent_num}: {value}")

        print(f"\n🤖 BOT TOKEN: {'✅ Configured' if config.get('DISCORD_BOT_TOKEN') else '❌ Missing'}")

        # Validation
        required_fields = [
            'DISCORD_BOT_TOKEN',
            'DISCORD_INFRASTRUCTURE_CHANNEL_ID',
            'DISCORD_ARCHITECTURE_CHANNEL_ID',
            'DISCORD_COORDINATION_CHANNEL_ID',
            'DISCORD_A2A_COORDINATION_CHANNEL_ID'
        ]

        missing_fields = [field for field in required_fields if not config.get(field)]
        webhook_fields = [f'DISCORD_AGENT{i}_WEBHOOK_URL' for i in range(1, 5)]
        missing_webhooks = [field for field in webhook_fields if not config.get(field)]

        print(f"\n✅ REQUIRED FIELDS: {len(required_fields) - len(missing_fields)}/{len(required_fields)} configured")
        print(f"🔗 WEBHOOKS: {len(webhook_fields) - len(missing_webhooks)}/{len(webhook_fields)} configured")

        if missing_fields:
            print(f"\n⚠️ MISSING REQUIRED FIELDS: {', '.join(missing_fields)}")

        if missing_webhooks:
            print(f"⚠️ MISSING WEBHOOKS: {', '.join(missing_webhooks)}")

    async def setup_discord_integration(self) -> bool:
        """Complete Discord integration setup"""
        print("🚀 DISCORD MANAGER - AUTOMATED SETUP")
        print("=" * 50)

        if not self.token:
            print("❌ ERROR: No Discord token found.")
            print("\n🔧 To set the token, use one of these methods:")
            print("1. Set environment variable:")
            print("   $env:DISCORD_BOT_TOKEN = 'your_token_here'")
            print("2. Add to .env file:")
            print("   DISCORD_BOT_TOKEN=your_token_here")
            print("3. Run with token parameter:")
            print("   python discord_manager.py --token YOUR_TOKEN --setup")
            return False

        # Show token info (masked for security)
        token_preview = self.token[:10] + "..." + self.token[-5:] if len(self.token) > 15 else self.token
        print(f"🔑 Using Discord token: {token_preview}")

        print("🔗 Connecting to Discord...")
        success = await self.initialize_bot()

        if success:
            print("✅ Discord connection successful!")

            # Generate configuration
            config = self.generate_env_config()

            # Display configuration
            self.display_configuration(config)

            # Save to file
            saved = self.save_env_file(config)
            if saved:
                print(f"\n💾 Configuration saved to .env.discord")
                print("   Copy these variables to your main .env file or load the .env.discord file")
                return True
            else:
                print("\n❌ Failed to save configuration file")
                return False
        else:
            print("❌ Discord setup failed. Check your token and permissions.")
            return False

def main():
    """Main Discord manager execution"""
    import argparse

    parser = argparse.ArgumentParser(description="Discord Manager - Automated Discord Integration Setup")
    parser.add_argument("--token", help="Discord bot token (or set DISCORD_TOKEN env var)")
    parser.add_argument("--setup", action="store_true", help="Run automated setup")
    parser.add_argument("--config-only", action="store_true", help="Generate config without connecting")
    parser.add_argument("--check-token", action="store_true", help="Check current token status")

    args = parser.parse_args()

    manager = DiscordManager(token=args.token)

    if args.check_token:
        # Check token status
        print("🔍 DISCORD TOKEN STATUS CHECK")
        print("=" * 50)

        if manager.token:
            token_preview = manager.token[:10] + "..." + manager.token[-5:] if len(manager.token) > 15 else manager.token
            print(f"✅ Token found: {token_preview}")
            print(f"   Length: {len(manager.token)} characters")

            # Basic validation
            if len(manager.token) < 50:
                print("⚠️  WARNING: Token seems too short for a Discord bot token")
            elif not manager.token.startswith(('M', 'N', 'O')):
                print("⚠️  WARNING: Token doesn't start with expected Discord bot token prefix (M/N/O)")
            else:
                print("✅ Token format appears valid")

        else:
            print("❌ No Discord token found")
            print("\n🔧 To set the token:")
            print("1. Environment variable: $env:DISCORD_BOT_TOKEN = 'your_token'")
            print("2. Add to .env file: DISCORD_BOT_TOKEN=your_token")
            print("3. Command line: --token YOUR_TOKEN")

    elif args.setup:
        # Run automated setup
        asyncio.run(manager.setup_discord_integration())
    elif args.config_only:
        # Generate config from existing channels (if bot is already connected)
        print("⚠️ Config-only mode requires existing bot connection. Use --setup instead.")
    else:
        print("🐝 Discord Manager Tool")
        print("Usage:")
        print("  python discord_manager.py --setup                    # Automated setup")
        print("  python discord_manager.py --check-token             # Check token status")
        print("  python discord_manager.py --token YOUR_TOKEN --setup # Setup with specific token")
        print("\nEnsure your bot token has these permissions:")
        print("  • Manage Channels")
        print("  • Manage Webhooks")
        print("  • Read Messages")
        print("  • Send Messages")
        print("  • Use Slash Commands")

if __name__ == "__main__":
    main()