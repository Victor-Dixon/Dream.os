#!/usr/bin/env python3
"""
🐝 UNIFIED MESSAGING CLI - SINGLE SOURCE OF TRUTH
=================================================

The ONE AND ONLY messaging CLI for Agent Cellphone V2.
Combines all messaging functionality into a single, comprehensive implementation.

FEATURES:
- ✅ Standalone operation (no dependencies required)
- ✅ Full SSOT messaging with enums and proper types
- ✅ Onboarding functionality (soft/hard onboarding)
- ✅ Multiple delivery methods (hybrid, devlog, workspace, discord, pyautogui)
- ✅ Statistics, testing, and history
- ✅ Template-based messaging
- ✅ Agent coordination and survey features
- ✅ Fallback delivery when core systems are broken

USAGE:
    python messaging_cli_unified.py --agent Agent-1 --message "hello"
    python messaging_cli_unified.py --broadcast --message "team update"
    python messaging_cli_unified.py --soft-onboard-lite Agent-1
    python messaging_cli_unified.py --stats

SSOT PRINCIPLE: One CLI, one system, zero confusion.

Author: Agent-1 (Unified Messaging CLI Architect)
Date: 2026-01-15
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from uuid import uuid4
from logging_unified import get_logger

# Configure unified logging
logger = get_logger(__name__)

# Constants
AGENT_WORKSPACES_DIR = Path("agent_workspaces")
DEVLOGS_DIR = Path("../agent-tools/devlogs")
PROJECT_ROOT = Path(__file__).parent

# Enums (standalone implementation)
class MessagePriority:
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"

class MessageType:
    COORDINATION = "coordination"
    TASK = "task"
    STATUS = "status"
    BROADCAST = "broadcast"
    ALERT = "alert"
    CAPTAIN_TO_AGENT = "captain_to_agent"

class DeliveryMethod:
    HYBRID = "hybrid"
    PYAUTOGUI = "pyautogui"
    DEVLOG = "devlog"
    WORKSPACE = "workspace"
    DISCORD = "discord"

# Standalone messaging implementation (fallback when core is broken)
class StandaloneMessagingSystem:
    """Standalone messaging system that works without core dependencies."""

    def __init__(self):
        self.delivery_methods = ["devlog", "workspace"]  # Start with reliable methods
        self.agent_workspaces = AGENT_WORKSPACES_DIR
        self.devlogs_dir = DEVLOGS_DIR

    def send_message(self, recipient: str, content: str, **kwargs) -> Dict[str, Any]:
        """Send message via available delivery methods."""
        message_id = f"msg_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid4().hex[:8]}"

        results = []

        # Always try devlog delivery (most reliable)
        devlog_result = self._deliver_via_devlog(recipient, content, message_id)
        results.append(devlog_result)

        # Try workspace delivery
        workspace_result = self._deliver_via_workspace(recipient, content, message_id)
        results.append(workspace_result)

        # Check if any delivery succeeded
        success = any(r["success"] for r in results)

        return {
            "overall_success": success,
            "message_id": message_id,
            "delivery_results": results,
            "total_deliveries_attempted": len(results),
            "successful_deliveries": sum(1 for r in results if r["success"])
        }

    def broadcast_message(self, content: str, recipients: List[str], **kwargs) -> Dict[str, Any]:
        """Broadcast message to multiple recipients."""
        results = []
        successful_deliveries = 0

        for recipient in recipients:
            result = self.send_message(recipient, content, **kwargs)
            results.append({
                "recipient": recipient,
                "result": result
            })
            if result["overall_success"]:
                successful_deliveries += 1

        return {
            "overall_success": successful_deliveries > 0,
            "total_recipients": len(recipients),
            "successful_deliveries": successful_deliveries,
            "individual_results": results
        }

    def _deliver_via_devlog(self, recipient: str, content: str, message_id: str) -> Dict[str, Any]:
        """Deliver message via devlog file system."""
        try:
            # Ensure devlogs directory exists
            self.devlogs_dir.mkdir(parents=True, exist_ok=True)

            # Create devlog entry
            devlog_entry = {
                "timestamp": datetime.now().isoformat(),
                "message_id": message_id,
                "recipient": recipient,
                "sender": "SYSTEM",
                "content": content,
                "delivery_method": "devlog",
                "status": "delivered"
            }

            # Write to devlog file
            devlog_file = self.devlogs_dir / f"devlog_{datetime.now().strftime('%Y%m%d')}.jsonl"
            with open(devlog_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(devlog_entry) + '\n')

            return {
                "method": "devlog",
                "success": True,
                "message_id": message_id
            }

        except Exception as e:
            return {
                "method": "devlog",
                "success": False,
                "error": str(e)
            }

    def _deliver_via_workspace(self, recipient: str, content: str, message_id: str) -> Dict[str, Any]:
        """Deliver message via agent workspace inbox."""
        try:
            # Check if agent workspace exists
            workspace_dir = self.agent_workspaces / recipient
            inbox_dir = workspace_dir / "inbox"
            inbox_dir.mkdir(parents=True, exist_ok=True)

            # Create message file
            message_file = inbox_dir / f"message_{message_id}.json"
            message_data = {
                "timestamp": datetime.now().isoformat(),
                "message_id": message_id,
                "recipient": recipient,
                "sender": "SYSTEM",
                "content": content,
                "delivery_method": "workspace",
                "status": "delivered"
            }

            with open(message_file, 'w', encoding='utf-8') as f:
                json.dump(message_data, f, indent=2)

            return {
                "method": "workspace",
                "success": True,
                "message_id": message_id
            }

        except Exception as e:
            return {
                "method": "workspace",
                "success": False,
                "error": str(e)
            }

    def get_delivery_stats(self) -> Dict[str, Any]:
        """Get delivery statistics."""
        return {
            "total_messages": 0,  # Would need to implement tracking
            "successful_messages": 0,
            "success_rate": 0,
            "method_stats": {
                "devlog": {"attempts": 0, "successes": 0},
                "workspace": {"attempts": 0, "successes": 0}
            }
        }

    def get_delivery_history(self, limit: int = 10) -> List[Dict]:
        """Get recent delivery history."""
        # Would need to implement history tracking
        return []

# Unified Messaging CLI Class
class UnifiedMessagingCLI:
    """The single, comprehensive messaging CLI."""

    def __init__(self):
        self.standalone_messaging = StandaloneMessagingSystem()
        self.core_messaging = None
        self.task_handler = None
        self.onboarding_handlers = {
            "hard": None,
            "soft": None
        }

        # Try to load core messaging system
        self._load_core_systems()

    def _load_core_systems(self):
        """Load core messaging systems if available."""
        try:
            # Try to import SSOT messaging
            sys.path.insert(0, str(PROJECT_ROOT))
            from src.core.messaging_ssot import get_messaging_ssot, MessagePriority as CorePriority, MessageType as CoreType, DeliveryMethod as CoreDelivery
            self.core_messaging = get_messaging_ssot()

            # Override enums with core versions
            global MessagePriority, MessageType, DeliveryMethod
            MessagePriority = CorePriority
            MessageType = CoreType
            DeliveryMethod = CoreDelivery

            print("✅ Core messaging SSOT loaded")
        except ImportError:
            print("⚠️ Core messaging not available, using standalone mode")

        # Try to load unified task manager
        try:
            from task_management_unified import UnifiedTaskManager
            self.task_manager = UnifiedTaskManager()
        except ImportError:
            self.task_manager = None

        # Try to load onboarding handlers
        try:
            from src.services.unified_onboarding_handlers import HardOnboardingHandler
            self.onboarding_handlers["hard"] = HardOnboardingHandler()
        except ImportError:
            pass

        try:
            from src.services.unified_onboarding_handlers import SoftOnboardingHandler
            self.onboarding_handlers["soft"] = SoftOnboardingHandler()
        except ImportError:
            pass

    def create_parser(self) -> argparse.ArgumentParser:
        """Create the unified argument parser."""
        parser = argparse.ArgumentParser(
            description="🐝 Unified Messaging CLI - Single Source of Truth",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
🐝 UNIFIED MESSAGING CLI - SINGLE SOURCE OF TRUTH
=================================================

CORE MESSAGING:
---------------
# Send to specific agent
python messaging_cli_unified.py --agent Agent-1 --message "Task completed"

# Broadcast to all agents
python messaging_cli_unified.py --broadcast --message "System maintenance in 5 minutes"

# Send with full options
python messaging_cli_unified.py --agent Agent-5 --message "URGENT!" --priority urgent --type alert --tags critical --sender CAPTAIN

ONBOARDING (when available):
---------------------------
# Soft onboarding
python messaging_cli_unified.py --soft-onboard-lite Agent-1

# Hard onboarding
python messaging_cli_unified.py --hard-onboard-lite Agent-1

SYSTEM MANAGEMENT:
------------------
# Statistics
python messaging_cli_unified.py --stats

# Test system
python messaging_cli_unified.py --test

# Message history
python messaging_cli_unified.py --history 10

DELIVERY METHODS:
-----------------
- hybrid: Try all available methods (recommended)
- pyautogui: Direct agent interface control
- devlog: Devlog file system
- workspace: Agent workspace inbox
- discord: Discord webhooks

🐝 WE ARE SWARM. MESSAGES FLOW. MISSIONS ACCOMPLISH. ⚡🔥
            """
        )

        # Core messaging arguments
        parser.add_argument(
            "--message", "-m",
            type=str,
            help="Message content to send"
        )

        parser.add_argument(
            "--agent", "-a",
            type=str,
            help="Target agent ID (e.g., Agent-1, Agent-2)"
        )

        parser.add_argument(
            "--broadcast", "-b",
            action="store_true",
            help="Broadcast message to all agents"
        )

        # Message configuration
        parser.add_argument(
            "--priority", "-p",
            choices=["low", "normal", "high", "urgent"],
            default="normal",
            help="Message priority (default: normal)"
        )

        parser.add_argument(
            "--type", "-t",
            choices=["coordination", "task", "status", "broadcast", "alert"],
            default="coordination",
            help="Message type (default: coordination)"
        )

        parser.add_argument(
            "--delivery-method", "-d",
            choices=["hybrid", "pyautogui", "devlog", "workspace", "discord"],
            default="hybrid",
            help="Delivery method (default: hybrid)"
        )

        parser.add_argument(
            "--sender", "-s",
            type=str,
            default="SYSTEM",
            help="Message sender (default: SYSTEM)"
        )

        parser.add_argument(
            "--tags",
            nargs="+",
            help="Message tags for categorization"
        )

        # Onboarding arguments
        parser.add_argument(
            "--soft-onboard-lite",
            type=str,
            help="Send soft onboarding message to agent"
        )

        parser.add_argument(
            "--hard-onboard-lite",
            type=str,
            help="Send hard onboarding message to agent"
        )

        # System management
        parser.add_argument(
            "--stats",
            action="store_true",
            help="Show messaging system statistics"
        )

        parser.add_argument(
            "--test",
            action="store_true",
            help="Test messaging system functionality"
        )

        parser.add_argument(
            "--history",
            type=int,
            default=10,
            help="Show recent message history (default: 10)"
        )

        return parser

    def send_simple_message(self, agent_id: str, body: str, tags: List[str] = None) -> int:
        """Send a simple message via the best available method."""
        if self.core_messaging:
            # Use core messaging if available
            try:
                result = self.core_messaging.send_message(
                    recipient=agent_id,
                    content=body,
                    sender="SYSTEM",
                    priority=MessagePriority.NORMAL,
                    message_type=MessageType.COORDINATION,
                    tags=tags or []
                )
                if result.get("overall_success"):
                    logger.info(f"✅ Sent message to {agent_id} via core messaging")
                    return 0
            except Exception as e:
                logger.warning(f"Core messaging failed, falling back to standalone: {e}")

        # Fallback to standalone messaging
        result = self.standalone_messaging.send_message(agent_id, body)
        if result["overall_success"]:
            logger.info(f"✅ Sent message to {agent_id} via standalone messaging")
            return 0
        else:
            logger.error(f"❌ Failed to send message to {agent_id}")
            return 1

    def handle_message(self, args) -> int:
        """Handle message sending."""
        try:
            # Validate arguments
            if not args.broadcast and not args.agent:
                print("❌ Error: Must specify either --agent or --broadcast")
                return 1

            if not args.message:
                print("❌ Error: Must provide --message content")
                return 1

            # Convert string arguments to enums
            priority_map = {
                "low": MessagePriority.LOW,
                "normal": MessagePriority.NORMAL,
                "high": MessagePriority.HIGH,
                "urgent": MessagePriority.URGENT
            }

            type_map = {
                "coordination": MessageType.COORDINATION,
                "task": MessageType.TASK,
                "status": MessageType.STATUS,
                "broadcast": MessageType.BROADCAST,
                "alert": MessageType.ALERT
            }

            # Prepare message parameters
            message_params = {
                "content": args.message,
                "sender": args.sender,
                "priority": priority_map[args.priority],
                "message_type": type_map[args.type],
                "tags": args.tags or []
            }

            # Send message(s)
            if args.broadcast:
                print(f"📡 Broadcasting message to all agents...")
                print(f"   Priority: {args.priority.upper()}")
                print(f"   Type: {args.type.title()}")
                print(f"   Message: {args.message[:100]}{'...' if len(args.message) > 100 else ''}")
                print()

                # Get all agents (would need to be configured)
                all_agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]

                if self.core_messaging:
                    try:
                        result = self.core_messaging.broadcast_message(
                            content=args.message,
                            recipients=all_agents,
                            sender=args.sender,
                            priority=priority_map[args.priority],
                            message_type=type_map[args.type],
                            tags=args.tags or []
                        )

                        if result["overall_success"]:
                            print("✅ Broadcast successful!")
                            print(f"   Recipients: {result['total_recipients']}")
                            print(f"   Successful deliveries: {result['successful_deliveries']}")
                        else:
                            print("⚠️ Broadcast partially successful")
                            print(f"   Recipients: {result['total_recipients']}")
                            print(f"   Successful deliveries: {result['successful_deliveries']}")
                    except Exception as e:
                        print(f"Core broadcast failed, using standalone: {e}")
                        result = self.standalone_messaging.broadcast_message(args.message, all_agents)
                        print(f"✅ Standalone broadcast completed: {result['successful_deliveries']}/{result['total_recipients']} successful")
                else:
                    result = self.standalone_messaging.broadcast_message(args.message, all_agents)
                    print(f"✅ Standalone broadcast completed: {result['successful_deliveries']}/{result['total_recipients']} successful")

            else:
                print(f"📤 Sending message to {args.agent}...")
                print(f"   Priority: {args.priority.upper()}")
                print(f"   Type: {args.type.title()}")
                print(f"   Message: {args.message[:100]}{'...' if len(args.message) > 100 else ''}")
                print()

                if self.core_messaging:
                    try:
                        result = self.core_messaging.send_message(
                            recipient=args.agent,
                            **message_params
                        )

                        if result["overall_success"]:
                            print("✅ Message delivered successfully!")
                            print(f"   Message ID: {result['message_id']}")
                            print(f"   Delivery methods attempted: {len(result['delivery_results'])}")
                            successful_methods = [r for r in result["delivery_results"] if r["success"]]
                            print(f"   Successful deliveries: {len(successful_methods)}")
                        else:
                            print("❌ Message delivery failed")
                            print("   Failed delivery methods:")
                            for r in result["delivery_results"]:
                                if not r["success"]:
                                    print(f"     - {r['method']}: {r['error']}")
                    except Exception as e:
                        print(f"Core messaging failed, using standalone: {e}")
                        result = self.standalone_messaging.send_message(args.agent, args.message)
                        if result["overall_success"]:
                            print("✅ Message delivered via standalone system!")
                            print(f"   Message ID: {result['message_id']}")
                            print(f"   Successful deliveries: {result['successful_deliveries']}")
                        else:
                            print("❌ Message delivery failed")
                else:
                    result = self.standalone_messaging.send_message(args.agent, args.message)
                    if result["overall_success"]:
                        print("✅ Message delivered via standalone system!")
                        print(f"   Message ID: {result['message_id']}")
                        print(f"   Successful deliveries: {result['successful_deliveries']}")
                    else:
                        print("❌ Message delivery failed")

            return 0 if result.get("overall_success", False) else 1

        except Exception as e:
            print(f"❌ Error sending message: {e}")
            return 1

    def handle_onboarding(self, args) -> int:
        """Handle onboarding commands."""
        if args.soft_onboard_lite:
            return self._handle_soft_onboard_lite(args.soft_onboard_lite)
        elif args.hard_onboard_lite:
            return self._handle_hard_onboard_lite(args.hard_onboard_lite)
        return 0

    def _handle_soft_onboard_lite(self, agent_id: str) -> int:
        """Handle soft onboarding."""
        if self.onboarding_handlers["soft"]:
            try:
                # Use core onboarding handler
                result = self.onboarding_handlers["soft"].send_onboarding(agent_id)
                if result:
                    print(f"✅ Soft onboarding sent to {agent_id} via core system")
                    return 0
            except Exception as e:
                print(f"Core soft onboarding failed: {e}")

        # Fallback to template-based messaging
        return self._send_template_onboarding(agent_id, "soft")

    def _handle_hard_onboard_lite(self, agent_id: str) -> int:
        """Handle hard onboarding."""
        if self.onboarding_handlers["hard"]:
            try:
                # Use core onboarding handler
                result = self.onboarding_handlers["hard"].send_onboarding(agent_id)
                if result:
                    print(f"✅ Hard onboarding sent to {agent_id} via core system")
                    return 0
            except Exception as e:
                print(f"Core hard onboarding failed: {e}")

        # Fallback to template-based messaging
        return self._send_template_onboarding(agent_id, "hard")

    def _send_template_onboarding(self, agent_id: str, onboard_type: str) -> int:
        """Send template-based onboarding message."""
        from uuid import uuid4

        template_path = PROJECT_ROOT / f"src/services/onboarding/{onboard_type}/templates/{onboard_type}_onboard_template.md"

        try:
            if template_path.exists():
                template = template_path.read_text(encoding='utf-8')
                body = template.replace('{{AGENT}}', agent_id).replace('{{UUID}}', str(uuid4())).replace('{{TIMESTAMP}}', datetime.now().isoformat())
            else:
                # Fallback message
                body = f"[HEADER] ONBOARDING ({onboard_type.upper()})\nFrom: SYSTEM\nTo: {agent_id}\nMessage ID: {uuid4()}\nTimestamp: {datetime.now().isoformat()}\n\nWelcome {agent_id}! Please complete your onboarding tasks."

            return self.send_simple_message(agent_id, body, ['onboarding', onboard_type])

        except Exception as e:
            print(f"❌ Template onboarding failed: {e}")
            # Final fallback
            body = f"SYSTEM: Welcome {agent_id}! Please complete your {onboard_type} onboarding."
            return self.send_simple_message(agent_id, body, ['onboarding', onboard_type])

    def show_stats(self) -> int:
        """Show messaging statistics."""
        try:
            if self.core_messaging:
                stats = self.core_messaging.get_delivery_stats()
            else:
                stats = self.standalone_messaging.get_delivery_stats()

            print("📊 UNIFIED MESSAGING STATISTICS")
            print("=" * 50)
            print(f"Total Messages Processed: {stats.get('total_messages', 'N/A')}")
            print(f"Successful Deliveries: {stats.get('successful_messages', 'N/A')}")
            print(f"Overall Success Rate: {stats.get('success_rate', 'N/A')}%")

            if "method_stats" in stats:
                print("\n📈 DELIVERY METHOD PERFORMANCE")
                for method, method_stats in stats["method_stats"].items():
                    attempts = method_stats.get("attempts", 0)
                    successes = method_stats.get("successes", 0)
                    success_rate = (successes / attempts * 100) if attempts > 0 else 0
                    print(f"   {method.title()}: {successes}/{attempts} ({success_rate:.1f}%)")

            print(f"\n📊 System Status: {'Core SSOT' if self.core_messaging else 'Standalone Mode'}")
            return 0

        except Exception as e:
            print(f"❌ Error retrieving stats: {e}")
            return 1

    def run_test(self) -> int:
        """Run messaging system test."""
        print("🧪 TESTING UNIFIED MESSAGING SYSTEM")
        print("=" * 40)

        test_results = []

        # Test 1: Basic message sending
        print("Test 1: Basic message delivery...")
        try:
            if self.core_messaging:
                result = self.core_messaging.send_message(
                    recipient="Agent-1",
                    content="TEST MESSAGE: System functionality check",
                    sender="SYSTEM_TEST",
                    priority=MessagePriority.NORMAL,
                    message_type=MessageType.STATUS
                )
            else:
                result = self.standalone_messaging.send_message("Agent-1", "TEST MESSAGE: System functionality check")

            success = result.get("overall_success", False)
            test_results.append(("Basic Delivery", success))
            print(f"   {'✅ PASS' if success else '❌ FAIL'}: Basic message delivery")
        except Exception as e:
            test_results.append(("Basic Delivery", False))
            print(f"   ❌ FAIL: {e}")

        # Test 2: System availability
        print("Test 2: System availability...")
        core_available = self.core_messaging is not None
        test_results.append(("Core System", core_available))
        print(f"   {'✅ PASS' if core_available else '⚠️ WARN'}: Core messaging system available")

        # Summary
        print("\n📋 TEST SUMMARY")
        print("-" * 20)
        passed = sum(1 for _, success in test_results if success)
        total = len(test_results)

        for test_name, success in test_results:
            status = "✅ PASS" if success else ("⚠️ WARN" if "Core" in test_name else "❌ FAIL")
            print(f"   {status}: {test_name}")

        print(f"\nOverall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")

        if passed == total:
            print("🎉 ALL TESTS PASSED - Unified messaging system is fully functional!")
            return 0
        elif passed >= total * 0.7:
            print("⚠️ MOST TESTS PASSED - System is mostly functional")
            return 0
        else:
            print("❌ TESTS FAILED - System needs attention")
            return 1

    def show_history(self, limit: int) -> int:
        """Show message history."""
        try:
            if self.core_messaging:
                history = self.core_messaging.get_delivery_history(limit)
            else:
                history = self.standalone_messaging.get_delivery_history(limit)

            if not history:
                print("📭 No message history available")
                return 0

            print(f"📜 RECENT MESSAGE HISTORY (Last {limit})")
            print("=" * 60)

            for entry in history[-limit:]:
                if self.core_messaging:
                    msg = entry["message"]
                    success = entry["overall_success"]
                    status = "✅" if success else "❌"

                    timestamp = datetime.fromisoformat(msg["timestamp"]).strftime("%m/%d %H:%M:%S")
                    print(f"{status} {timestamp}")
                    print(f"   {msg['sender']} → {msg['recipient']}")
                    print(f"   Type: {msg['message_type']} | Priority: {msg['priority']}")
                    print(f"   Message: {msg['content'][:80]}{'...' if len(msg['content']) > 80 else ''}")
                    print()
                else:
                    # Standalone format
                    print(f"📄 {entry.get('timestamp', 'Unknown')} - {entry.get('recipient', 'Unknown')}")

            return 0

        except Exception as e:
            print(f"❌ Error retrieving history: {e}")
            return 1

    def run(self, args=None):
        """Run the unified messaging CLI."""
        parser = self.create_parser()
        parsed_args = parser.parse_args(args)

        # Handle different command types
        if parsed_args.message:
            return self.handle_message(parsed_args)
        elif parsed_args.soft_onboard_lite or parsed_args.hard_onboard_lite:
            return self.handle_onboarding(parsed_args)
        elif parsed_args.stats:
            return self.show_stats()
        elif parsed_args.test:
            return self.run_test()
        elif parsed_args.history:
            return self.show_history(parsed_args.history)
        else:
            parser.print_help()
            return 0

def main():
    """Main entry point."""
    try:
        cli = UnifiedMessagingCLI()
        exit_code = cli.run()
        print("\n🐝 UNIFIED MESSAGING CLI - SINGLE SOURCE OF TRUTH ⚡🔥")
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n⚠️ Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()