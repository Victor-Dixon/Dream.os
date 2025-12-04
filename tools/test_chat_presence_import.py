#!/usr/bin/env python3
"""
Quick test to verify chat_presence imports and basic initialization.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

print("Testing chat_presence imports...")

try:
    print("1. Testing unified_logging_system import...")
    from src.core.unified_logging_system import get_logger, configure_logging
    print("   ✅ Unified logging system imported")
    
    print("2. Testing twitch_bridge import...")
    from src.services.chat_presence.twitch_bridge import TwitchChatBridge
    print("   ✅ TwitchChatBridge imported")
    
    print("3. Testing chat_presence_orchestrator import...")
    from src.services.chat_presence.chat_presence_orchestrator import ChatPresenceOrchestrator
    print("   ✅ ChatPresenceOrchestrator imported")
    
    print("4. Testing orchestrator instantiation...")
    orchestrator = ChatPresenceOrchestrator()
    print("   ✅ Orchestrator created successfully")
    
    print("\n✅ All imports and basic initialization successful!")
    print("   The bot should start cleanly.")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

