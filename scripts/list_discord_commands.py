#!/usr/bin/env python3
"""
List All Discord Commands
=========================

Lists all available Discord bot commands for documentation and testing.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

def list_commands():
    """List all Discord commands."""
    print("=" * 60)
    print("Discord Bot Commands")
    print("=" * 60)
    print()
    
    print("📨 MESSAGING COMMANDS:")
    print("  !message <agent-id> <message>")
    print("    - Send message to specific agent")
    print("    - Example: !message Agent-1 Hello, please review the system")
    print()
    
    print("  !broadcast <message>")
    print("    - Broadcast message to all agents")
    print("    - Example: !broadcast All agents: Complete your tasks!")
    print()
    
    print("🎛️ GUI COMMANDS:")
    print("  !control (or !panel, !menu)")
    print("    - Open main control panel with interactive buttons")
    print()
    
    print("  !gui")
    print("    - Open messaging GUI interface")
    print()
    
    print("📊 STATUS COMMANDS:")
    print("  !status")
    print("    - View detailed swarm status")
    print()
    
    print("  !agents")
    print("    - List all agents with their roles")
    print()
    
    print("📚 HELP:")
    print("  !help")
    print("    - Show help information")
    print()
    
    print("🤖 SYSTEM COMMANDS:")
    print("  !shutdown")
    print("    - Gracefully shutdown the bot (with confirmation)")
    print()
    
    print("  !restart")
    print("    - Restart the Discord bot (with confirmation)")
    print()
    
    print("📨 MESSAGE FORMATS:")
    print("  [C2A] Agent-X")
    print("  <message content>")
    print("    - Send message using C2A format")
    print("    - Example:")
    print("      [C2A] Agent-1")
    print("      Please review the messaging system")
    print()
    
    print("  [D2A] Agent-X")
    print("  <message content>")
    print("    - Send urgent message using D2A format")
    print("    - Example:")
    print("      [D2A] Agent-4")
    print("      Urgent: System needs attention")
    print()
    
    print("=" * 60)
    print("All commands are case-insensitive")
    print("GUI commands (!control, !gui) are preferred for ease of use")
    print("=" * 60)

if __name__ == "__main__":
    list_commands()

