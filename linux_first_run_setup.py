#!/usr/bin/env python3
"""
Linux First-Run Setup for Dream.os
==================================

This script runs on first startup to configure:
- Agent coordinates for Linux single-monitor setup
- Discord bot integration (optional)
- Twitch bot integration (optional)
- GitHub token configuration (optional)
"""

import os
import json
import sys
from pathlib import Path

def print_banner():
    print("\n🐧 Dream.os Linux First-Run Setup")
    print("=" * 50)
    print("Welcome to Dream.os on Linux!")
    print("Let's configure your agent ecosystem.\n")

def setup_agent_coordinates():
    """Setup agent coordinates for Linux."""
    print("🎯 Agent Coordinate Setup")
    print("-" * 30)
    
    coords_file = Path("cursor_agent_coords_linux.json")
    
    if coords_file.exists():
        use_existing = input("Agent coordinates already exist. Use existing? (Y/n): ").strip().lower()
        if use_existing in ['', 'y', 'yes']:
            print("✅ Using existing coordinates")
            return
    
    print("\nDream.os uses PyAutoGUI to control browser-based agents.")
    print("You'll need 4 browser windows/tabs positioned at specific coordinates.")
    print("Recommended layout (1920x1080 monitor):")
    print("  Agent-A: Top-left     (200, 300)")
    print("  Agent-B: Top-middle   (600, 300)") 
    print("  Agent-C: Top-right    (1000, 300)")
    print("  Agent-D: Bottom-left  (200, 700)")
    
    use_defaults = input("\nUse recommended coordinates? (Y/n): ").strip().lower()
    
    if use_defaults in ['', 'y', 'yes']:
        # Use the coordinates we already set
        print("✅ Using recommended coordinates")
        return
    
    # Manual coordinate setup
    print("\n📍 Manual Coordinate Setup")
    print("Open 4 browser windows and position them, then enter coordinates:")
    
    coords = {}
    agents = ["Agent-A", "Agent-B", "Agent-C", "Agent-D"]
    
    for agent in agents:
        print(f"\n{agent}:")
        try:
            x = int(input("  Chat input X coordinate: "))
            y = int(input("  Chat input Y coordinate: "))
            ox = int(input("  Onboarding X coordinate: "))
            oy = int(input("  Onboarding Y coordinate: "))
            
            coords[agent] = {
                "chat_input": [x, y],
                "onboarding_coords": [ox, oy]
            }
        except ValueError:
            print("❌ Invalid coordinates, using defaults")
            coords[agent] = {
                "chat_input": [200 + (agents.index(agent) * 400), 300],
                "onboarding_coords": [200 + (agents.index(agent) * 400), 200]
            }
    
    # Save coordinates
    config = {
        **coords,
        "screen_bounds": {"width": 1920, "height": 1080},
        "linux_configured": True,
        "agent_count": 4,
        "agent_names": agents
    }
    
    with open("cursor_agent_coords.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("✅ Agent coordinates saved!")

def setup_discord_integration():
    """Setup Discord bot integration."""
    print("\n🤖 Discord Bot Integration")
    print("-" * 30)
    
    setup_discord = input("Set up Discord bot for agent communication? (y/N): ").strip().lower()
    
    if setup_discord not in ['y', 'yes']:
        print("⏭️ Skipping Discord setup")
        return
    
    print("\n📋 Discord Setup Instructions:")
    print("1. Go to https://discord.com/developers/applications")
    print("2. Create 'New Application' named 'Dream.os'")
    print("3. Go to 'Bot' section and 'Add Bot'")
    print("4. Copy the bot token")
    print("5. Use this invite URL with bot permissions:")
    print("   https://discord.com/api/oauth2/authorize?client_id=YOUR_APP_ID&permissions=414464658496&scope=bot")
    
    token = input("\nPaste your Discord bot token: ").strip()
    
    if token:
        # Update .env file
        env_file = Path(".env")
        env_content = ""
        
        if env_file.exists():
            with open(env_file, "r") as f:
                env_content = f.read()
        
        # Replace or add the token
        if "DISCORD_BOT_TOKEN=" in env_content:
            lines = env_content.split('\n')
            for i, line in enumerate(lines):
                if line.startswith("DISCORD_BOT_TOKEN="):
                    lines[i] = f"DISCORD_BOT_TOKEN={token}"
                    break
            env_content = '\n'.join(lines)
        else:
            env_content += f"\nDISCORD_BOT_TOKEN={token}\n"
        
        with open(env_file, "w") as f:
            f.write(env_content)
        
        print("✅ Discord bot token configured!")
        print("💡 Run 'python main.py --discord --background' to start the bot")
    else:
        print("⚠️ No token provided, Discord setup skipped")

def setup_twitch_integration():
    """Setup Twitch bot integration."""
    print("\n�� Twitch Bot Integration")
    print("-" * 30)
    
    setup_twitch = input("Set up Twitch bot for streaming integration? (y/N): ").strip().lower()
    
    if setup_twitch not in ['y', 'yes']:
        print("⏭️ Skipping Twitch setup")
        return
    
    print("\n📋 Twitch Setup Instructions:")
    print("1. Go to https://twitchtokengenerator.com/")
    print("2. Generate OAuth token for your channel")
    print("3. Copy the token (starts with 'oauth:')")
    
    channel = input("Your Twitch channel name: ").strip()
    token = input("Twitch OAuth token: ").strip()
    
    if channel and token:
        # Update .env file
        env_file = Path(".env")
        env_content = ""
        
        if env_file.exists():
            with open(env_file, "r") as f:
                env_content = f.read()
        
        # Add Twitch config
        twitch_config = f"""
# Twitch Integration
TWITCH_CHANNEL={channel}
TWITCH_ACCESS_TOKEN={token}
TWITCH_BOT_USERNAME={channel}
"""
        
        if "TWITCH_CHANNEL=" in env_content:
            print("⚠️ Twitch already configured, skipping")
        else:
            env_content += twitch_config
            
            with open(env_file, "w") as f:
                f.write(env_content)
            
            print("✅ Twitch bot configured!")
            print("💡 Run 'python main.py --twitch --background' to start the bot")
    else:
        print("⚠️ Incomplete Twitch config, setup skipped")

def setup_github_integration():
    """Setup GitHub token for automation."""
    print("\n🔧 GitHub Integration Setup")
    print("-" * 30)
    
    setup_github = input("Configure GitHub token for repository automation? (y/N): ").strip().lower()
    
    if setup_github not in ['y', 'yes']:
        print("⏭️ Skipping GitHub setup")
        return
    
    print("\n📋 GitHub Token Setup:")
    print("1. Go to https://github.com/settings/tokens")
    print("2. Generate new token (classic)")
    print("3. Name: 'Dream.os Agent Automation'")
    print("4. Select scopes: repo, user:email, read:user")
    print("5. Copy the token")
    
    token = input("\nPaste your GitHub token: ").strip()
    
    if token and len(token) > 40:
        # Update .env file
        env_file = Path(".env")
        env_content = ""
        
        if env_file.exists():
            with open(env_file, "r") as f:
                env_content = f.read()
        
        # Replace or add the token
        if "GITHUB_TOKEN=" in env_content:
            lines = env_content.split('\n')
            for i, line in enumerate(lines):
                if line.startswith("GITHUB_TOKEN="):
                    lines[i] = f"GITHUB_TOKEN={token}"
                    break
            env_content = '\n'.join(lines)
        else:
            env_content += f"\nGITHUB_TOKEN={token}\n"
        
        with open(env_file, "w") as f:
            f.write(env_content)
        
        print("✅ GitHub token configured!")
        print("🎯 Agents can now automate repository management")
    else:
        print("⚠️ Invalid token format, GitHub setup skipped")

def main():
    """Run the first-run setup."""
    print_banner()
    
    print("This setup will configure Dream.os for Linux with 4 agents (A, B, C, D).")
    print("You'll be prompted to set up coordinates and optional integrations.\n")
    
    # Mark setup as completed
    setup_complete_file = Path(".linux_setup_complete")
    
    if setup_complete_file.exists():
        rerun = input("Linux setup already completed. Run again? (y/N): ").strip().lower()
        if rerun not in ['y', 'yes']:
            print("✅ Setup already completed. Run 'python main.py --status' to check system.")
            return
    
    try:
        # Run setup steps
        setup_agent_coordinates()
        setup_discord_integration()
        setup_twitch_integration()
        setup_github_integration()
        
        # Mark as complete
        setup_complete_file.touch()
        
        print("\n🎉 Linux Setup Complete!")
        print("=" * 30)
        print("✅ Agent coordinates configured")
        print("✅ Integration options set up")
        print("✅ System ready for operation")
        print("\n🚀 Next steps:")
        print("1. Start services: python main.py --fastapi --background")
        print("2. Test agents: python -m src.services.messaging_cli --start A B C D")
        print("3. Check status: python main.py --status")
        
    except KeyboardInterrupt:
        print("\n⚠️ Setup interrupted. Run this script again to complete setup.")
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        print("You can run this script again to retry.")

if __name__ == "__main__":
    main()
