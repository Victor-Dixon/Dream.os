#!/usr/bin/env python3
"""
Twitch Bot Diagnostic Tool
==========================

Diagnoses Twitch bot connection and message handling issues.
"""

import sys
import asyncio
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def check_imports():
    """Check if required modules can be imported."""
    print("=" * 60)
    print("🔍 CHECKING IMPORTS")
    print("=" * 60)
    
    try:
        import irc.bot
        import irc.client
        print("✅ IRC library available")
    except ImportError as e:
        print(f"❌ IRC library not available: {e}")
        return False
    
    try:
        from src.services.chat_presence.twitch_bridge import TwitchChatBridge, TwitchIRCBot
        print("✅ Twitch bridge modules importable")
    except ImportError as e:
        print(f"❌ Cannot import Twitch bridge: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    try:
        from src.services.chat_presence.chat_presence_orchestrator import ChatPresenceOrchestrator
        print("✅ Chat presence orchestrator importable")
    except ImportError as e:
        print(f"❌ Cannot import orchestrator: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def check_config():
    """Check if configuration is available."""
    print("\n" + "=" * 60)
    print("🔍 CHECKING CONFIGURATION")
    print("=" * 60)
    
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    access_token = os.getenv("TWITCH_ACCESS_TOKEN")
    channel = os.getenv("TWITCH_CHANNEL")
    swarm_voice = os.getenv("TWITCH_SWARM_VOICE")
    
    if swarm_voice:
        parts = swarm_voice.split("|")
        if len(parts) >= 3:
            username, token, channel_name = parts[0].strip(), parts[1].strip(), parts[2].strip()
            print(f"✅ TWITCH_SWARM_VOICE found")
            print(f"   Username: {username}")
            print(f"   Token: {token[:20]}...")
            print(f"   Channel: {channel_name}")
            return True
        else:
            print(f"⚠️ TWITCH_SWARM_VOICE incomplete: {swarm_voice}")
    
    if access_token and channel:
        print(f"✅ TWITCH_ACCESS_TOKEN and TWITCH_CHANNEL found")
        print(f"   Channel: {channel}")
        print(f"   Token: {access_token[:20]}...")
        return True
    
    print("❌ No Twitch configuration found")
    print("   Set TWITCH_ACCESS_TOKEN and TWITCH_CHANNEL, or")
    print("   Set TWITCH_SWARM_VOICE=username|oauth:token|channel")
    return False

def check_code_issues():
    """Check for known code issues."""
    print("\n" + "=" * 60)
    print("🔍 CHECKING CODE FOR ISSUES")
    print("=" * 60)
    
    issues = []
    
    # Check if event_loop is properly passed
    try:
        from src.services.chat_presence.twitch_bridge import TwitchChatBridge
        import inspect
        sig = inspect.signature(TwitchChatBridge.__init__)
        params = list(sig.parameters.keys())
        if 'event_loop' not in params:
            issues.append("❌ TwitchChatBridge.__init__ missing 'event_loop' parameter")
        else:
            print("✅ TwitchChatBridge accepts event_loop parameter")
    except Exception as e:
        issues.append(f"❌ Error checking TwitchChatBridge signature: {e}")
    
    # Check if orchestrator passes event_loop
    try:
        with open("src/services/chat_presence/chat_presence_orchestrator.py", "r") as f:
            content = f.read()
            if "event_loop=event_loop" in content or "event_loop=event_loop," in content:
                print("✅ Orchestrator passes event_loop to bridge")
            else:
                issues.append("❌ Orchestrator may not be passing event_loop to bridge")
    except Exception as e:
        issues.append(f"❌ Error checking orchestrator: {e}")
    
    # Check on_pubmsg callback handling
    try:
        with open("src/services/chat_presence/twitch_bridge.py", "r") as f:
            content = f.read()
            if "run_coroutine_threadsafe" in content:
                print("✅ on_pubmsg uses run_coroutine_threadsafe")
            else:
                issues.append("❌ on_pubmsg may not be using run_coroutine_threadsafe")
            
            if "bridge_instance.event_loop" in content:
                print("✅ on_pubmsg checks bridge_instance.event_loop")
            else:
                issues.append("⚠️ on_pubmsg may not be checking bridge_instance.event_loop")
    except Exception as e:
        issues.append(f"❌ Error checking twitch_bridge: {e}")
    
    if issues:
        print("\n⚠️ ISSUES FOUND:")
        for issue in issues:
            print(f"   {issue}")
        return False
    else:
        print("\n✅ No obvious code issues found")
        return True

async def test_message_callback():
    """Test if message callback can be called."""
    print("\n" + "=" * 60)
    print("🔍 TESTING MESSAGE CALLBACK")
    print("=" * 60)
    
    async def test_callback(message_data):
        print(f"✅ Test callback received: {message_data.get('message', '')}")
        return True
    
    try:
        from src.services.chat_presence.twitch_bridge import TwitchChatBridge
        
        # Try to create bridge with test callback
        bridge = TwitchChatBridge(
            username="test",
            oauth_token="oauth:test",
            channel="test",
            on_message=test_callback,
            event_loop=asyncio.get_running_loop(),
        )
        print("✅ Bridge created with async callback")
        
        # Test callback
        test_data = {"message": "!status", "username": "test_user"}
        await test_callback(test_data)
        print("✅ Callback test successful")
        return True
    except Exception as e:
        print(f"❌ Callback test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all diagnostics."""
    print("\n" + "=" * 60)
    print("🔧 TWITCH BOT DIAGNOSTIC TOOL")
    print("=" * 60)
    
    results = []
    
    # Check imports
    results.append(("Imports", check_imports()))
    
    # Check config
    results.append(("Configuration", check_config()))
    
    # Check code
    results.append(("Code Issues", check_code_issues()))
    
    # Test callback (requires async)
    try:
        result = asyncio.run(test_message_callback())
        results.append(("Message Callback", result))
    except Exception as e:
        print(f"⚠️ Could not test callback: {e}")
        results.append(("Message Callback", False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 DIAGNOSTIC SUMMARY")
    print("=" * 60)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {name}: {status}")
    
    all_passed = all(result for _, result in results)
    
    if all_passed:
        print("\n✅ All checks passed!")
    else:
        print("\n❌ Some checks failed - review issues above")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())

