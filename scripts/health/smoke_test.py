#!/usr/bin/env python3
"""
Smoke Test Harness - Dream.OS Recovery
======================================

Runs basic health checks on core systems during recovery.
Focuses on import validation, configuration loading, and dry-run connectivity.

Exit codes:
0 = All systems healthy
1 = One or more systems failed

Author: Agent-6 (Discord Messaging Recovery Specialist)
Date: 2026-01-09
"""

import os
import sys
import importlib
from pathlib import Path
from typing import Dict, List, Tuple

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

class RecoverySmokeTest:
    """
    Smoke tests for Dream.OS core systems during recovery.
    """

    def __init__(self):
        self.results = []
        self.failed_systems = []

        # Define test suites for each system
        self.test_suites = {
            'message_queue': {
                'name': 'Message Queue Processor',
                'module': 'src.core.message_queue_processor.core.processor',
                'tests': [
                    self._test_import,
                    self._test_message_queue_config,
                    self._test_message_queue_dry_run
                ]
            },
            'twitch_bot': {
                'name': 'Twitch Bot',
                'module': 'src.services.chat_presence.twitch_eventsub_server',
                'tests': [
                    self._test_import,
                    self._test_twitch_config,
                    self._test_twitch_dry_run
                ]
            },
            'discord_bot': {
                'name': 'Discord Bot',
                'module': 'src.discord_commander.unified_discord_bot',
                'tests': [
                    self._test_import,
                    self._test_discord_config,
                    self._test_discord_dry_run
                ]
            },
            'fastapi_service': {
                'name': 'FastAPI Service',
                'module': 'src.web.fastapi_app',
                'tests': [
                    self._test_import,
                    self._test_fastapi_config,
                    self._test_fastapi_dry_run
                ]
            }
        }

    def run_all_tests(self) -> int:
        """
        Run smoke tests on all systems.

        Returns:
            0 if all tests pass, 1 if any fail
        """
        print("🚀 Starting Dream.OS recovery smoke test suite...")
        print("=" * 60)

        for system_name, suite_config in self.test_suites.items():
            print(f"🧪 Testing {suite_config['name']}...")
            self._run_system_tests(system_name, suite_config)

        # Report results
        self._report_results()

        # Return exit code
        return 1 if self.failed_systems else 0

    def _run_system_tests(self, system_name: str, suite_config: Dict):
        """Run all tests for a specific system."""
        system_results = []
        system_failed = False

        for test_func in suite_config['tests']:
            try:
                result = test_func(system_name, suite_config)
                system_results.append(result)
                if not result[0]:  # Test failed
                    system_failed = True
            except Exception as e:
                print(f"❌ {system_name} test crashed: {e}")
                system_results.append((False, f"Test crashed: {e}"))
                system_failed = True

        self.results.append((system_name, suite_config['name'], system_results))

        if system_failed:
            self.failed_systems.append(system_name)
            print(f"❌ {suite_config['name']} FAILED")
        else:
            print(f"✅ {suite_config['name']} PASSED")

    def _report_results(self):
        """Print detailed test results."""
        print("\n" + "="*60)
        print("SMOKE TEST RESULTS")
        print("="*60)

        all_passed = True

        for system_name, system_display_name, test_results in self.results:
            print(f"\n{system_display_name} ({system_name}):")

            for i, (passed, message) in enumerate(test_results, 1):
                status = "✅ PASS" if passed else "❌ FAIL"
                print(f"  {i}. {status}: {message}")

            if system_name in self.failed_systems:
                all_passed = False

        print("\n" + "="*60)
        if all_passed:
            print("🎉 ALL SYSTEMS HEALTHY")
        else:
            print("💥 SYSTEMS WITH FAILURES:")
            for failed_system in self.failed_systems:
                system_info = next((info for name, info, _ in self.results if name == failed_system), None)
                if system_info:
                    print(f"  - {system_info[0]}")
        print("="*60)

    # ============================================================================
    # COMMON TEST METHODS
    # ============================================================================

    def _test_import(self, system_name: str, suite_config: Dict) -> Tuple[bool, str]:
        """Test if the module can be imported."""
        try:
            module_name = suite_config['module']
            importlib.import_module(module_name)
            return True, f"Import successful: {module_name}"
        except ImportError as e:
            return False, f"Import failed: {e}"
        except Exception as e:
            return False, f"Import error: {e}"

    # ============================================================================
    # MESSAGE QUEUE TESTS
    # ============================================================================

    def _test_message_queue_config(self, system_name: str, suite_config: Dict) -> Tuple[bool, str]:
        """Test if message queue config is available."""
        try:
            # Try to import and check for basic config requirements
            from src.utils.unified_utilities import get_project_root

            # Check if required directories exist
            project_root = get_project_root()
            required_dirs = [
                project_root / "message_queue",
                project_root / "agent_workspaces"
            ]

            for dir_path in required_dirs:
                if not dir_path.exists():
                    return False, f"Required directory missing: {dir_path}"

            return True, "Message queue directories exist"

        except Exception as e:
            return False, f"Config check failed: {e}"

    def _test_message_queue_dry_run(self, system_name: str, suite_config: Dict) -> Tuple[bool, str]:
        """Test message queue dry-run connectivity."""
        try:
            # Import the processor module
            import src.core.message_queue_processor.core.processor as mq_processor

            # Check if main function exists (basic smoke test)
            if not hasattr(mq_processor, 'main'):
                return False, "Missing main function"

            # Check for basic processor class
            if not hasattr(mq_processor, 'MessageQueueProcessor'):
                # Try alternative import path
                try:
                    from src.core.message_queue_processor.core.processor import MessageQueueProcessor
                except ImportError:
                    return False, "MessageQueueProcessor class not found"

            return True, "Message queue processor structure valid"

        except Exception as e:
            return False, f"Dry-run failed: {e}"

    # ============================================================================
    # TWITCH BOT TESTS
    # ============================================================================

    def _test_twitch_config(self, system_name: str, suite_config: Dict) -> Tuple[bool, str]:
        """Test if Twitch bot config is available."""
        required_env_vars = [
            'TWITCH_ACCESS_TOKEN',
            'TWITCH_CHANNEL'
        ]

        missing_vars = []
        for var in required_env_vars:
            if not os.getenv(var):
                missing_vars.append(var)

        if missing_vars:
            return False, f"Missing environment variables: {', '.join(missing_vars)}"

        # Validate token format
        token = os.getenv('TWITCH_ACCESS_TOKEN', '')
        if token and not token.startswith('oauth:'):
            return False, "TWITCH_ACCESS_TOKEN should start with 'oauth:'"

        return True, "Twitch configuration variables present"

    def _test_twitch_dry_run(self, system_name: str, suite_config: Dict) -> Tuple[bool, str]:
        """Test Twitch bot dry-run connectivity."""
        try:
            # Import the twitch chat bridge
            import src.services.chat_presence.twitch_chat_bridge as twitch_bridge

            # Check if TwitchChatBridge exists
            if not hasattr(twitch_bridge, 'TwitchChatBridge'):
                return False, "Missing TwitchChatBridge class"

            # Get config from environment
            token = os.getenv('TWITCH_ACCESS_TOKEN', '')
            channel = os.getenv('TWITCH_CHANNEL', '')
            username = os.getenv('TWITCH_BOT_USERNAME', channel)

            if not token or not channel:
                return False, "Missing token or channel for dry-run test"

            # Create bridge instance for validation (dry-run)
            try:
                bridge = twitch_bridge.TwitchChatBridge(
                    username=username,
                    token=token,
                    channel=channel,
                    message_handler=None,
                    connection_handler=None,
                    use_websocket=False  # Use IRC for dry-run
                )

                # Validate configuration (this will raise exception if invalid)
                # We don't call connect() to avoid actual network connection
                return True, "Twitch bot configuration valid for dry-run"

            except Exception as config_error:
                return False, f"Configuration validation failed: {config_error}"

        except Exception as e:
            return False, f"Dry-run failed: {e}"

    # ============================================================================
    # DISCORD BOT TESTS
    # ============================================================================

    def _test_discord_config(self, system_name: str, suite_config: Dict) -> Tuple[bool, str]:
        """Test if Discord bot config is available."""
        required_env_vars = [
            'DISCORD_BOT_TOKEN',
            'DISCORD_GUILD_ID'
        ]

        missing_vars = []
        for var in required_env_vars:
            if not os.getenv(var):
                missing_vars.append(var)

        if missing_vars:
            return False, f"Missing environment variables: {', '.join(missing_vars)}"

        return True, "Discord configuration variables present"

    def _test_discord_dry_run(self, system_name: str, suite_config: Dict) -> Tuple[bool, str]:
        """Test Discord bot dry-run connectivity."""
        try:
            # Run the discord dry-run test
            import subprocess
            result = subprocess.run([
                sys.executable, "scripts/health/discord_dry_run.py"
            ], capture_output=True, text=True, cwd=project_root)

            if result.returncode == 0:
                return True, "Discord dry-run connection successful"
            else:
                return False, f"Discord dry-run failed: {result.stderr.strip()}"

        except Exception as e:
            return False, f"Dry-run test execution failed: {e}"

    # ============================================================================
    # FASTAPI SERVICE TESTS
    # ============================================================================

    def _test_fastapi_config(self, system_name: str, suite_config: Dict) -> Tuple[bool, str]:
        """Test if FastAPI config is available."""
        try:
            # Check if required directories exist
            from src.utils.unified_utilities import get_project_root
            project_root = get_project_root()

            required_dirs = [
                project_root / "src" / "web",
                project_root / "logs"
            ]

            for dir_path in required_dirs:
                if not dir_path.exists():
                    return False, f"Required directory missing: {dir_path}"

            return True, "FastAPI directories exist"

        except Exception as e:
            return False, f"Config check failed: {e}"

    def _test_fastapi_dry_run(self, system_name: str, suite_config: Dict) -> Tuple[bool, str]:
        """Test FastAPI service dry-run."""
        try:
            # Import the FastAPI app
            import src.web.fastapi_app as fastapi_app

            # Check if app exists
            if not hasattr(fastapi_app, 'app'):
                return False, "Missing FastAPI app instance"

            # Check if it's a FastAPI app
            app = fastapi_app.app
            if not hasattr(app, 'routes'):
                return False, "Invalid FastAPI app structure"

            # Try to import uvicorn
            try:
                import uvicorn
            except ImportError:
                return False, "uvicorn library not available"

            return True, "FastAPI service structure valid"

        except Exception as e:
            return False, f"Dry-run failed: {e}"

def main():
    """Main entry point for smoke test harness."""
    harness = RecoverySmokeTest()
    exit_code = harness.run_all_tests()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()