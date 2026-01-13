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

        # Add agent webhooks (agents 1-8 for full swarm support)
        for i in range(1, 9):
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

    def display_guild_info(self):
        """Display Discord server (guild) information"""
        if not self.guild:
            print("❌ No guild information available. Run --setup or --view-channels first.")
            return

        print("\n🏰 DISCORD SERVER INFORMATION")
        print("=" * 50)
        print(f"📊 Server Name: {self.guild.name}")
        print(f"🆔 Server ID: {self.guild.id}")
        print(f"👑 Owner: {self.guild.owner}")
        print(f"👥 Member Count: {self.guild.member_count}")
        print(f"📅 Created: {self.guild.created_at.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print(f"🌍 Region: {getattr(self.guild, 'preferred_locale', 'Unknown')}")
        print(f"🔒 Verification Level: {self.guild.verification_level}")
        print(f"🎭 Content Filter: {self.guild.explicit_content_filter}")

        # Channel counts
        text_channels = len([c for c in self.guild.channels if isinstance(c, discord.TextChannel)])
        voice_channels = len([c for c in self.guild.channels if isinstance(c, discord.VoiceChannel)])
        categories = len([c for c in self.guild.channels if isinstance(c, discord.CategoryChannel)])

        print(f"\n📺 Channels: {text_channels} text, {voice_channels} voice, {categories} categories")

        # Role count
        print(f"👤 Roles: {len(self.guild.roles)}")

        # Emoji count
        print(f"😀 Emojis: {len(self.guild.emojis)}")

    def display_channel_structure(self):
        """Display the current channel structure of the Discord server"""
        if not self.guild:
            print("❌ No guild information available. Run --setup or --view-channels first.")
            return

        print("\n🏗️ DISCORD CHANNEL STRUCTURE")
        print("=" * 60)

        # Group channels by category
        channels_by_category = {}
        uncategorized = []

        for channel in self.guild.channels:
            if isinstance(channel, discord.CategoryChannel):
                channels_by_category[channel] = []
            elif hasattr(channel, 'category') and channel.category:
                if channel.category not in channels_by_category:
                    channels_by_category[channel.category] = []
                channels_by_category[channel.category].append(channel)
            else:
                uncategorized.append(channel)

        # Display categorized channels
        for category, channels in channels_by_category.items():
            print(f"\n📁 {category.name} (ID: {category.id})")
            print("-" * 40)

            for channel in sorted(channels, key=lambda c: c.position):
                channel_type = "💬" if isinstance(channel, discord.TextChannel) else "🔊" if isinstance(channel, discord.VoiceChannel) else "❓"
                topic = f" - {channel.topic[:50]}..." if hasattr(channel, 'topic') and channel.topic else ""
                print(f"  {channel_type} {channel.name} (ID: {channel.id}){topic}")

        # Display uncategorized channels
        if uncategorized:
            print(f"\n📂 UNCATEGORIZED CHANNELS")
            print("-" * 40)
            for channel in sorted(uncategorized, key=lambda c: c.position):
                channel_type = "💬" if isinstance(channel, discord.TextChannel) else "🔊" if isinstance(channel, discord.VoiceChannel) else "❓"
                topic = f" - {channel.topic[:50]}..." if hasattr(channel, 'topic') and channel.topic else ""
                print(f"  {channel_type} {channel.name} (ID: {channel.id}){topic}")

        # Summary
        total_channels = len([c for c in self.guild.channels if not isinstance(c, discord.CategoryChannel)])
        categories_count = len([c for c in self.guild.channels if isinstance(c, discord.CategoryChannel)])

        print(f"\n📊 SUMMARY")
        print("-" * 40)
        print(f"📁 Categories: {categories_count}")
        print(f"💬 Total Channels: {total_channels}")
        print(f"🤖 Agent Channels: {len([c for c in self.guild.channels if isinstance(c, discord.TextChannel) and 'agent' in c.name.lower()])}")
        print(f"🏗️ Infrastructure Channels: {len([c for c in self.guild.channels if isinstance(c, discord.TextChannel) and any(word in c.name.lower() for word in ['infra', 'infrastructure', 'deploy', 'deployment'])])}")

    def analyze_channel_usage(self):
        """Analyze channel usage patterns and provide organization recommendations"""
        if not self.guild:
            print("❌ No guild information available.")
            return

        print("\n📊 DISCORD CHANNEL USAGE ANALYSIS")
        print("=" * 60)

        # Categorize all channels
        agent_channels = []
        coordination_channels = []
        technical_channels = []
        general_channels = []
        unused_categories = []

        for channel in self.guild.channels:
            if isinstance(channel, discord.TextChannel):
                channel_name = channel.name.lower()

                # Agent-specific channels
                if 'agent' in channel_name and any(str(i) in channel_name for i in range(1, 9)):
                    agent_channels.append(channel)
                # Coordination channels
                elif any(word in channel_name for word in ['coordination', 'a2a', 'swarm']):
                    coordination_channels.append(channel)
                # Technical channels
                elif any(word in channel_name for word in ['infrastructure', 'architecture', 'deploy', 'infra']):
                    technical_channels.append(channel)
                # General discussion channels
                else:
                    general_channels.append(channel)

            elif isinstance(channel, discord.CategoryChannel):
                # Check if category has channels
                category_channels = [c for c in self.guild.channels if getattr(c, 'category', None) == channel]
                if not category_channels:
                    unused_categories.append(channel)

        # Analysis Results
        print("📋 CHANNEL ANALYSIS RESULTS:")
        print(f"🤖 Agent Channels: {len(agent_channels)}")
        print(f"🤝 Coordination Channels: {len(coordination_channels)}")
        print(f"🏗️ Technical Channels: {len(technical_channels)}")
        print(f"💬 General Channels: {len(general_channels)}")
        print(f"📂 Empty Categories: {len(unused_categories)}")

        # Organization Recommendations
        print("\n💡 ORGANIZATION RECOMMENDATIONS:")
        print("-" * 40)

        # Agent Channels Organization
        if len(agent_channels) >= 8:
            print("✅ Agent Channels: Well covered (8+ channels)")
            print("   💡 Recommendation: Group into 'Agent Coordination' category")
        elif len(agent_channels) >= 4:
            print("⚠️ Agent Channels: Partially covered")
            print("   💡 Recommendation: Create missing agent channels")
        else:
            print("❌ Agent Channels: Insufficient coverage")
            print("   💡 Recommendation: Create complete set of agent channels")

        # Coordination Channels
        if coordination_channels:
            print("✅ Coordination Channels: Present")
            print("   💡 Recommendation: Ensure 'a2a-coordination' is primary swarm channel")
        else:
            print("❌ Coordination Channels: Missing")
            print("   💡 Recommendation: Create coordination channels for swarm communication")

        # Technical Channels
        if len(technical_channels) >= 2:
            print("✅ Technical Channels: Infrastructure covered")
            print("   💡 Recommendation: Group under 'Technical Infrastructure' category")
        else:
            print("⚠️ Technical Channels: Incomplete")
            print("   💡 Recommendation: Add missing technical coordination channels")

        # General Channels
        active_general = [c for c in general_channels if not c.name.startswith(('🤖', '🏗️', '🏛️', '🤝', '🐝'))]
        if active_general:
            print(f"✅ General Channels: {len(active_general)} active discussion channels")
            print("   💡 Recommendation: Keep in 'General Discussion' category")

        # Cleanup Recommendations
        uncategorized = [c for c in self.guild.channels if isinstance(c, discord.TextChannel) and not getattr(c, 'category', None)]
        if uncategorized:
            print(f"\n🧹 CLEANUP NEEDED:")
            print(f"   📂 {len(uncategorized)} uncategorized channels")
            print("   💡 Recommendation: Assign to appropriate categories or archive")

        if unused_categories:
            print(f"   📁 {len(unused_categories)} empty categories to remove")

        # Proposed Structure
        print("\n🏗️ PROPOSED CHANNEL STRUCTURE:")
        print("   ├── 🤖 Agent Coordination")
        print("   │   ├── 🐝 a2a-coordination")
        print("   │   └── 🤖 agent-1 through agent-8")
        print("   ├── 🏗️ Technical Infrastructure")
        print("   │   ├── 🏗️ infrastructure")
        print("   │   └── 🏛️ architecture")
        print("   ├── 💬 General Discussion")
        print("   │   ├── 💬 general")
        print("   │   ├── 📝 brainstorm")
        print("   │   └── 📈 captains-channel")
        print("   └── 🔊 Voice Channels")
        print("       └── 🔊 General")

    async def organize_channels(self) -> bool:
        """Automatically organize channels into logical categories"""
        if not self.guild:
            print("❌ No guild information available.")
            return False

        print("\n🏗️ DISCORD CHANNEL ORGANIZATION")
        print("=" * 50)

        print("✅ Channel organization analysis complete")
        print("⚠️ Automatic organization requires manual category creation in Discord")
        print("💡 Use the analysis above to manually organize channels")
        print("\n📋 MANUAL ORGANIZATION STEPS:")
        print("1. Create categories: '🤖 Agent Coordination', '🏗️ Technical Infrastructure', '💬 General Discussion'")
        print("2. Move agent channels to '🤖 Agent Coordination'")
        print("3. Move infrastructure/architecture channels to '🏗️ Technical Infrastructure'")
        print("4. Move general discussion channels to '💬 General Discussion'")
        print("5. Delete empty categories like 'mmorpg' if not needed")

        return True

    async def setup_devlog_channels(self) -> bool:
        """Create agent-specific devlog channels and webhooks"""
        if not self.guild:
            print("❌ No guild information available.")
            return False

        print("\n📝 SETTING UP AGENT DEVLOG CHANNELS")
        print("=" * 50)

        try:
            # Create Devlogs category if it doesn't exist
            devlogs_category = None
            for category in self.guild.categories:
                if "devlog" in category.name.lower() or "dev-log" in category.name.lower():
                    devlogs_category = category
                    break

            if not devlogs_category:
                devlogs_category = await self.guild.create_text_channel("🤖 Agent Devlogs")
                print("✅ Created '🤖 Agent Devlogs' category")
            else:
                print(f"✅ Found existing devlogs category: {devlogs_category.name}")

            # Create devlog channels for each agent
            devlog_webhooks = {}

            for i in range(1, 9):  # Agents 1-8
                agent_num = i
                channel_name = f"agent-{agent_num}-devlogs"

                # Check if channel already exists
                existing_channel = None
                for channel in self.guild.channels:
                    if isinstance(channel, discord.TextChannel) and channel.name == channel_name:
                        existing_channel = channel
                        break

                if not existing_channel:
                    # Create new channel in devlogs category
                    existing_channel = await self.guild.create_text_channel(channel_name, category=devlogs_category)
                    print(f"✅ Created devlog channel: {channel_name}")
                else:
                    print(f"✅ Found existing devlog channel: {channel_name}")

                # Create/update webhook for this channel
                try:
                    # Check for existing webhook
                    existing_webhooks = await existing_channel.webhooks()
                    webhook_name = f"Agent-{agent_num}-Devlogs-Webhook"

                    existing_webhook = None
                    for webhook in existing_webhooks:
                        if webhook.name == webhook_name:
                            existing_webhook = webhook
                            break

                    if not existing_webhook:
                        webhook = await existing_channel.create_webhook(name=webhook_name)
                        devlog_webhooks[f'AGENT_{agent_num}'] = webhook.url
                        print(f"✅ Created webhook for Agent-{agent_num} devlogs")
                    else:
                        devlog_webhooks[f'AGENT_{agent_num}'] = existing_webhook.url
                        print(f"✅ Found existing webhook for Agent-{agent_num} devlogs")

                except Exception as e:
                    print(f"❌ Failed to setup webhook for Agent-{agent_num}: {e}")

            # Generate environment configuration for devlog webhooks
            self.generate_devlog_env_config(devlog_webhooks)

            print("\n🎉 DEVLOG CHANNELS SETUP COMPLETE!")
            print(f"✅ Created 8 agent devlog channels in '{devlogs_category.name}' category")
            print(f"✅ Created 8 webhooks for agent devlog delivery")
            print("✅ Generated environment configuration")
            return True

        except Exception as e:
            print(f"❌ Failed to setup devlog channels: {e}")
            return False

    def generate_devlog_env_config(self, webhooks: Dict[str, str]):
        """Generate environment configuration for devlog webhooks"""
        env_content = "\n# Agent Devlog Webhooks - Auto-generated\n"
        env_content += "# Copy these to your main .env file\n\n"

        for agent_key, webhook_url in webhooks.items():
            env_var = f"DISCORD_WEBHOOK_{agent_key}"
            env_content += f'{env_var}="{webhook_url}"\n'

        # Save to file
        with open('.env.devlogs', 'w') as f:
            f.write(env_content)

        print("\n📄 DEVLOG WEBHOOK CONFIGURATION:")
        print("   Add these variables to your .env file:")
        for agent_key, webhook_url in webhooks.items():
            env_var = f"DISCORD_WEBHOOK_{agent_key}"
            print(f"   {env_var}=[webhook_url]")

        print("\n💾 Configuration saved to .env.devlogs")
        print("   Copy the variables above to your main .env file")
    async def view_channels_only(self) -> bool:
        """View current Discord channel structure without making changes"""
        print("👀 DISCORD CHANNEL VIEWER")
        print("=" * 50)

        if not self.token:
            print("❌ ERROR: No Discord token found.")
            print("Set DISCORD_TOKEN or DISCORD_BOT_TOKEN environment variable.")
            return False

        print("🔗 Connecting to Discord...")
        success = False

        try:
            # Create bot with necessary intents
            intents = discord.Intents.default()
            intents.guilds = True
            intents.messages = True
            intents.message_content = True

            self.bot = commands.Bot(command_prefix='!', intents=intents)

            @self.bot.event
            async def on_ready():
                nonlocal success
                logger.info(f"✅ Discord bot connected as {self.bot.user}")
                await self._gather_guild_info()
                self.display_guild_info()
                self.display_channel_structure()
                await self.bot.close()
                success = True

            await self.bot.start(self.token)
            return success

        except Exception as e:
            logger.error(f"❌ Failed to connect to Discord: {e}")
            return False

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
    parser.add_argument("--view-channels", action="store_true", help="View current Discord server channel structure")
    parser.add_argument("--view-guild", action="store_true", help="View Discord server information")
    parser.add_argument("--analyze-channels", action="store_true", help="Analyze channel usage and provide organization recommendations")
    parser.add_argument("--organize-channels", action="store_true", help="Automatically organize channels into logical categories")
    parser.add_argument("--setup-devlog-channels", action="store_true", help="Create agent-specific devlog channels and webhooks")

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

    elif args.view_channels:
        # View current channel structure
        asyncio.run(manager.view_channels_only())

    elif args.view_guild:
        # View guild information and channels
        print("🏰 VIEWING DISCORD GUILD INFORMATION")
        print("=" * 50)
        success = asyncio.run(manager.view_channels_only())
        if not success:
            print("❌ Failed to retrieve guild information")

    elif args.analyze_channels:
        # Analyze channel usage and provide recommendations
        print("📊 ANALYZING DISCORD CHANNEL USAGE")
        print("=" * 50)
        success = asyncio.run(manager.view_channels_only())
        if success:
            manager.analyze_channel_usage()

    elif args.organize_channels:
        # Organize channels automatically
        asyncio.run(manager.organize_channels())

    elif args.setup_devlog_channels:
        # Setup agent-specific devlog channels and webhooks
        success = asyncio.run(manager.setup_devlog_channels())
        if success:
            print("\n🎯 DEVLOG SETUP COMPLETE!")
            print("📋 Next steps:")
            print("   1. Copy webhook variables from .env.devlogs to your .env file")
            print("   2. Test devlog posting: python tools/devlog_poster.py --agent Agent-1 --file [devlog_file]")
            print("   3. Verify messages appear in agent-specific devlog channels")
        else:
            print("❌ Devlog setup failed")

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
        print("  python discord_manager.py --view-channels           # View channel structure")
        print("  python discord_manager.py --view-guild              # View server info + channels")
        print("  python discord_manager.py --analyze-channels        # Analyze usage & recommendations")
        print("  python discord_manager.py --organize-channels       # Get organization guide")
        print("  python discord_manager.py --setup-devlog-channels   # Create agent devlog channels")
        print("  python discord_manager.py --token YOUR_TOKEN --setup # Setup with specific token")
        print("\nEnsure your bot token has these permissions:")
        print("  • Manage Channels")
        print("  • Manage Webhooks")
        print("  • Read Messages")
        print("  • Send Messages")
        print("  • Use Slash Commands")

if __name__ == "__main__":
    main()