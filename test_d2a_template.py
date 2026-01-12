#!/usr/bin/env python3
"""
Test D2A Template Application
Tests that Discord-to-Agent messages are properly formatted with D2A templates
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_d2a_template_application():
    """Test that D2A templates are properly applied to messages."""

    print("🧪 TESTING D2A TEMPLATE APPLICATION")
    print("=" * 50)

    try:
        from src.core.messaging_models_core import (
            UnifiedMessage,
            MessageCategory,
            UnifiedMessageType,
            UnifiedMessagePriority,
        )
        from src.core.messaging_templates import render_message
        import uuid
        from datetime import datetime

        # Create a test D2A message
        test_message = UnifiedMessage(
            content="Test message from Discord user",
            sender="Discord User (testuser)",
            recipient="Agent-1",
            message_type=UnifiedMessageType.HUMAN_TO_AGENT,
            priority=UnifiedMessagePriority.REGULAR,
            category=MessageCategory.D2A,
            message_id=str(uuid.uuid4()),
            timestamp=datetime.now().isoformat(),
        )

        # Test rendering with devlog command
        devlog_command = (
            "python tools/devlog_poster.py --agent Agent-1 --file <devlog_path>\n"
            "# Fallback:\n"
            "python -m tools.toolbelt --devlog-post --agent Agent-1"
        )

        print("📨 Rendering D2A message...")
        rendered = render_message(test_message, devlog_command=devlog_command)

        print("✅ Message rendered successfully!")
        print(f"📏 Message length: {len(rendered)} characters")

        # Check if D2A template elements are present
        checks = [
            ("D2A HEADER", "[HEADER] D2A DISCORD INTAKE" in rendered),
            ("Sender field", "From: Discord User (testuser)" in rendered),
            ("Recipient field", "To: Agent-1" in rendered),
            ("Priority field", "Priority: regular" in rendered),
            ("Message ID", "Message ID:" in rendered),
            ("Timestamp", "Timestamp:" in rendered),
            ("User Message section", "User Message:" in rendered),
            ("Protocol Update", "PROTOCOL UPDATE" in rendered),
            ("Devlog command", "python tools/devlog_poster.py --agent Agent-1" in rendered),
            ("Discord tags", "#DISCORD #D2A" in rendered),
        ]

        print("\n🔍 TEMPLATE ELEMENT CHECKS:")
        print("-" * 30)

        all_passed = True
        for check_name, passed in checks:
            status = "✅" if passed else "❌"
            print(f"  {status} {check_name}")
            if not passed:
                all_passed = False

        print("\n📄 RENDERED MESSAGE PREVIEW:")
        print("-" * 30)
        # Show first 500 chars
        preview = rendered[:500] + "..." if len(rendered) > 500 else rendered
        print(preview)

        if all_passed:
            print("\n🎉 D2A TEMPLATE TEST PASSED!")
            print("✅ All template elements are present")
            print("✅ D2A messages are properly formatted")
            return True
        else:
            print("\n❌ D2A TEMPLATE TEST FAILED!")
            print("❌ Some template elements are missing")
            return False

    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_discord_message_processing():
    """Test that Discord messages get D2A templates applied."""

    print("\n🔄 TESTING DISCORD MESSAGE PROCESSING")
    print("=" * 50)

    try:
        # Simulate what happens in the Discord event handler
        from src.discord_commander.handlers.message_processing_helpers import (
            parse_message_format,
            create_unified_message,
        )
        from src.core.messaging_templates import render_message
        from src.discord_commander.handlers.discord_event_handlers import build_devlog_command

        # Mock Discord message
        class MockMessage:
            def __init__(self, content, author_name="TestUser"):
                self.content = content
                self.author = type('Author', (), {'name': author_name})()

        # Test message content
        test_content = "[D2A] Agent-1\n\nPlease analyze the codebase structure"

        # Parse the message (simulating Discord handler)
        has_prefix = True
        developer_prefix = "[D2A]"
        recipient, message_content, message_prefix = parse_message_format(
            test_content, has_prefix, developer_prefix)

        print(f"📨 Parsed message: {recipient} <- '{message_content}'")

        # Create unified message
        mock_message = MockMessage(test_content)
        unified_msg = create_unified_message(mock_message, recipient, message_content)

        # Build devlog command
        devlog_cmd = build_devlog_command(recipient)

        # Render message (this should apply D2A template)
        rendered = render_message(unified_msg, devlog_command=devlog_cmd)

        # Check if template was applied
        if "[HEADER] D2A DISCORD INTAKE" in rendered:
            print("✅ D2A template successfully applied to Discord message!")
            return True
        else:
            print("❌ D2A template NOT applied to Discord message")
            print("📄 Rendered content preview:")
            print(rendered[:300] + "...")
            return False

    except Exception as e:
        print(f"❌ Discord message processing test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all D2A template tests."""

    print("🤖 D2A TEMPLATE COMPREHENSIVE TESTING")
    print("=" * 60)

    test1_passed = test_d2a_template_application()
    test2_passed = test_discord_message_processing()

    print("\n" + "=" * 60)
    print("📊 FINAL RESULTS:")
    print(f"  Template Application Test: {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"  Discord Processing Test: {'✅ PASSED' if test2_passed else '❌ FAILED'}")

    if test1_passed and test2_passed:
        print("\n🎉 ALL D2A TEMPLATE TESTS PASSED!")
        print("✅ Discord-to-Agent messages are properly formatted")
        print("✅ Template system is working correctly")
        return True
    else:
        print("\n❌ SOME D2A TEMPLATE TESTS FAILED!")
        print("❌ Template application needs debugging")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)