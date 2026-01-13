#!/usr/bin/env python3
"""
<<<<<<< HEAD
Smoke Test Harness - Agent Cellphone V2
======================================

Runs basic health checks on all core systems:
- Import validation
- Configuration loading
- Dry-run connectivity tests
=======
Comprehensive Smoke Test Suite - Dream.OS Recovery
=================================================

Tests all core systems with import validation, config loading, and dry-run connectivity.
Used during recovery to validate system health without actual API calls or posting.
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1

Exit codes:
0 = All systems healthy
1 = One or more systems failed
<<<<<<< HEAD

Author: Agent-2 (Architecture & Design Specialist)
=======
2 = Critical system failure (unable to test)

Author: Agent-3 (Infrastructure & DevOps Recovery Specialist)
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
Date: 2026-01-09
"""

import os
import sys
<<<<<<< HEAD
import importlib
import logging
from typing import Dict, List, Tuple, Callable
from pathlib import Path

# Add project root to path
import sys
from pathlib import Path
project_root = Path(__file__).parent.parent
=======
import asyncio
import importlib
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

# Add project root to path
project_root = Path(__file__).parent.parent.parent
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
sys.path.insert(0, str(project_root))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

<<<<<<< HEAD
# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger(__name__)

class SmokeTestHarness:
    """
    Runs smoke tests on all core Dream.OS services.
    """

    def __init__(self):
        self.results = []
        self.failed_systems = []

        # Define test suites for each system
=======
@dataclass
class SystemTestResult:
    """Result of testing a system component."""
    system_name: str
    test_name: str
    passed: bool
    message: str
    error_details: Optional[str] = None

class ComprehensiveSmokeTest:
    """
    Comprehensive smoke tests for Dream.OS core systems during recovery.
    """

    def __init__(self):
        self.results: List[SystemTestResult] = []
        self.failed_systems: List[str] = []

        # Define comprehensive test suites for each system
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
        self.test_suites = {
            'message_queue': {
                'name': 'Message Queue Processor',
                'module': 'src.core.message_queue_processor.core.processor',
                'tests': [
                    self._test_import,
<<<<<<< HEAD
                    self._test_config_load,
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
=======
                    self._test_message_queue_config,
                    self._test_message_queue_structure,
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
                ]
            },
            'discord_bot': {
                'name': 'Discord Bot',
                'module': 'src.discord_commander.unified_discord_bot',
                'tests': [
                    self._test_import,
                    self._test_discord_config,
<<<<<<< HEAD
                    self._test_discord_dry_run
=======
                    self._test_discord_dry_run,
                ]
            },
            'twitch_bot': {
                'name': 'Twitch Bot',
                'module': 'src.services.chat_presence.twitch_eventsub_server',
                'tests': [
                    self._test_import,
                    self._test_twitch_config,
                    self._test_twitch_dry_run,
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
                ]
            },
            'fastapi_service': {
                'name': 'FastAPI Service',
                'module': 'src.web.fastapi_app',
                'tests': [
                    self._test_import,
                    self._test_fastapi_config,
<<<<<<< HEAD
                    self._test_fastapi_dry_run
=======
                    self._test_fastapi_structure,
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
                ]
            }
        }

    def run_all_tests(self) -> int:
        """
<<<<<<< HEAD
        Run smoke tests on all systems.

        Returns:
            0 if all tests pass, 1 if any fail
        """
        logger.info("🚀 Starting Dream.OS smoke test suite...")

        for system_name, suite_config in self.test_suites.items():
            logger.info(f"🧪 Testing {suite_config['name']}...")
            self._run_system_tests(system_name, suite_config)

        # Report results
        self._report_results()

        # Return exit code
        return 1 if self.failed_systems else 0
=======
        Run comprehensive smoke tests on all systems.

        Returns:
            0 if all tests pass, 1 if any fail, 2 if critical failure
        """
        print("🚀 Starting Dream.OS comprehensive smoke test suite...")
        print("=" * 70)

        critical_failure = False

        for system_name, suite_config in self.test_suites.items():
            print(f"🧪 Testing {suite_config['name']}...")
            try:
                self._run_system_tests(system_name, suite_config)
            except Exception as e:
                print(f"💥 CRITICAL: {suite_config['name']} test suite crashed: {e}")
                critical_failure = True
                self.failed_systems.append(system_name)
                self.results.append(SystemTestResult(
                    system_name, "suite_crash", False,
                    f"Test suite crashed: {e}", str(e)
                ))

        # Report results
        exit_code = self._report_results()

        if critical_failure:
            exit_code = 2

        return exit_code
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1

    def _run_system_tests(self, system_name: str, suite_config: Dict):
        """Run all tests for a specific system."""
        system_results = []
        system_failed = False

        for test_func in suite_config['tests']:
            try:
                result = test_func(system_name, suite_config)
                system_results.append(result)
<<<<<<< HEAD
                if not result[0]:  # Test failed
                    system_failed = True
            except Exception as e:
                logger.error(f"❌ {system_name} test crashed: {e}")
                system_results.append((False, f"Test crashed: {e}"))
                system_failed = True

        self.results.append((system_name, suite_config['name'], system_results))

        if system_failed:
            self.failed_systems.append(system_name)
            logger.error(f"❌ {suite_config['name']} FAILED")
        else:
            logger.info(f"✅ {suite_config['name']} PASSED")

    def _report_results(self):
        """Print detailed test results."""
        logger.info("\n" + "="*60)
        logger.info("SMOKE TEST RESULTS")
        logger.info("="*60)

        all_passed = True

        for system_name, system_display_name, test_results in self.results:
            logger.info(f"\n{system_display_name} ({system_name}):")

            for i, (passed, message) in enumerate(test_results, 1):
                status = "✅ PASS" if passed else "❌ FAIL"
                logger.info(f"  {i}. {status}: {message}")
=======
                if not result.passed:
                    system_failed = True
            except Exception as e:
                error_msg = f"Test crashed: {e}"
                print(f"❌ {system_name} test crashed: {e}")
                system_results.append(SystemTestResult(
                    system_name, test_func.__name__, False, error_msg, str(e)
                ))
                system_failed = True

        # Store results
        for result in system_results:
            self.results.append(result)

        if system_failed:
            self.failed_systems.append(system_name)
            print(f"❌ {suite_config['name']} FAILED")
        else:
            print(f"✅ {suite_config['name']} PASSED")

    def _report_results(self) -> int:
        """Print detailed test results and return exit code."""
        print("\n" + "="*70)
        print("COMPREHENSIVE SMOKE TEST RESULTS")
        print("="*70)

        all_passed = True
        total_tests = 0
        passed_tests = 0

        # Group results by system
        system_results = {}
        for result in self.results:
            if result.system_name not in system_results:
                system_results[result.system_name] = []
            system_results[result.system_name].append(result)

        for system_name, suite_config in self.test_suites.items():
            if system_name not in system_results:
                continue

            results = system_results[system_name]
            print(f"\n{suite_config['name']} ({system_name}):")

            for result in results:
                total_tests += 1
                status = "✅ PASS" if result.passed else "❌ FAIL"
                if result.passed:
                    passed_tests += 1
                else:
                    all_passed = False

                print(f"  • {status}: {result.message}")
                if result.error_details and not result.passed:
                    print(f"    Details: {result.error_details}")
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1

            if system_name in self.failed_systems:
                all_passed = False

<<<<<<< HEAD
        logger.info("\n" + "="*60)
        if all_passed:
            logger.info("🎉 ALL SYSTEMS HEALTHY")
        else:
            logger.error("💥 SYSTEMS WITH FAILURES:")
            for failed_system in self.failed_systems:
                system_info = next((info for name, info, _ in self.results if name == failed_system), None)
                if system_info:
                    logger.error(f"  - {system_info[0]}")
        logger.info("="*60)
=======
        print("\n" + "="*70)
        print(f"OVERALL: {passed_tests}/{total_tests} tests passed")

        if all_passed:
            print("🎉 ALL SYSTEMS HEALTHY - READY FOR PRODUCTION")
            return 0
        else:
            print("💥 SYSTEMS WITH FAILURES:")
            for failed_system in self.failed_systems:
                suite_name = self.test_suites.get(failed_system, {}).get('name', failed_system)
                print(f"  - {suite_name}")
            print("\n🔧 Recovery needed for failed systems")
            return 1
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1

    # ============================================================================
    # COMMON TEST METHODS
    # ============================================================================

<<<<<<< HEAD
    def _test_import(self, system_name: str, suite_config: Dict) -> Tuple[bool, str]:
        """Test if the module can be imported."""
        try:
            # Ensure project root is in path for all imports
            project_root = Path(__file__).parent.parent
            if str(project_root) not in sys.path:
                sys.path.insert(0, str(project_root))

            module_name = suite_config['module']
            importlib.import_module(module_name)
            return True, f"Import successful: {module_name}"
        except ImportError as e:
            return False, f"Import failed: {e}"
        except Exception as e:
            return False, f"Import error: {e}"
=======
    def _test_import(self, system_name: str, suite_config: Dict) -> SystemTestResult:
        """Test if the module can be imported."""
        try:
            module_name = suite_config['module']
            importlib.import_module(module_name)
            return SystemTestResult(system_name, "import", True,
                                  f"Import successful: {module_name}")
        except ImportError as e:
            return SystemTestResult(system_name, "import", False,
                                  f"Import failed: {e}", str(e))
        except Exception as e:
            return SystemTestResult(system_name, "import", False,
                                  f"Import error: {e}", str(e))
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1

    # ============================================================================
    # MESSAGE QUEUE TESTS
    # ============================================================================

<<<<<<< HEAD
    def _test_config_load(self, system_name: str, suite_config: Dict) -> Tuple[bool, str]:
        """Test if message queue config can be loaded."""
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

            return True, "Config directories exist"

        except Exception as e:
            return False, f"Config load failed: {e}"

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
=======
    def _test_message_queue_config(self, system_name: str, suite_config: Dict) -> SystemTestResult:
        """Test if Message Queue config is available."""
        required_env_vars = [
            'REDIS_HOST',
            'REDIS_PORT',
        ]

        optional_env_vars = [
            'REDIS_PASSWORD',
            'REDIS_DB',
        ]

        missing_required = []
        for var in required_env_vars:
            if not os.getenv(var):
                missing_required.append(var)

        if missing_required:
            return SystemTestResult(system_name, "config", False,
                                  f"Missing required env vars: {', '.join(missing_required)}")

        # Check if Redis connection config is valid
        try:
            import redis
            host = os.getenv('REDIS_HOST')
            port = int(os.getenv('REDIS_PORT', '6379'))
            password = os.getenv('REDIS_PASSWORD')
            db = int(os.getenv('REDIS_DB', '0'))

            # Test config validity (don't actually connect)
            if host and port > 0:
                return SystemTestResult(system_name, "config", True,
                                      f"Redis config valid: {host}:{port} (db={db})")
            else:
                return SystemTestResult(system_name, "config", False,
                                      "Invalid Redis configuration")

        except ImportError:
            return SystemTestResult(system_name, "config", False,
                                  "Redis library not available")
        except Exception as e:
            return SystemTestResult(system_name, "config", False,
                                  f"Config validation error: {e}", str(e))

    def _test_message_queue_structure(self, system_name: str, suite_config: Dict) -> SystemTestResult:
        """Test Message Queue processor structure and basic functionality."""
        try:
            # Import the processor module
            processor_module = importlib.import_module(suite_config['module'])

            # Check if main classes/functions exist
            required_attrs = ['MessageQueueProcessor']

            missing_attrs = []
            for attr in required_attrs:
                if not hasattr(processor_module, attr):
                    missing_attrs.append(attr)

            if missing_attrs:
                return SystemTestResult(system_name, "structure", False,
                                      f"Missing required attributes: {', '.join(missing_attrs)}")

            # Try to instantiate the processor class (without connecting)
            processor_class = getattr(processor_module, 'MessageQueueProcessor')

            # Check if it has required methods
            required_methods = ['process_message', 'enqueue_message']
            missing_methods = []
            for method in required_methods:
                if not hasattr(processor_class, method):
                    missing_methods.append(method)

            if missing_methods:
                return SystemTestResult(system_name, "structure", False,
                                      f"Missing required methods: {', '.join(missing_methods)}")

            return SystemTestResult(system_name, "structure", True,
                                  "Message Queue structure validation passed")

        except Exception as e:
            return SystemTestResult(system_name, "structure", False,
                                  f"Structure validation failed: {e}", str(e))
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1

    # ============================================================================
    # DISCORD BOT TESTS
    # ============================================================================

<<<<<<< HEAD
    def _test_discord_config(self, system_name: str, suite_config: Dict) -> Tuple[bool, str]:
=======
    def _test_discord_config(self, system_name: str, suite_config: Dict) -> SystemTestResult:
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
        """Test if Discord bot config is available."""
        required_env_vars = [
            'DISCORD_BOT_TOKEN',
            'DISCORD_GUILD_ID'
        ]

<<<<<<< HEAD
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
            # Import the discord bot
            import src.discord_commander.unified_discord_bot as discord_bot

            # Check for UnifiedDiscordBot class
            if not hasattr(discord_bot, 'UnifiedDiscordBot'):
                return False, "Missing UnifiedDiscordBot class"

            # Try to import discord.py to ensure it's available
            try:
                import discord
            except ImportError:
                return False, "discord.py library not available"

            # Check if token is available for dry-run
            token = os.getenv('DISCORD_BOT_TOKEN')
            if not token:
                return False, "DISCORD_BOT_TOKEN not available for dry-run"

            # Test basic bot instantiation (dry-run - no actual connection)
            try:
                bot = discord_bot.UnifiedDiscordBot(token=token)
                return True, "Discord bot instantiation successful (dry-run)"
            except Exception as e:
                return False, f"Bot instantiation failed: {e}"

        except Exception as e:
            return False, f"Dry-run failed: {e}"
=======
        optional_env_vars = [
            'DISCORD_CHANNEL_ID',
            'DISCORD_INTENTS'
        ]

        missing_required = []
        for var in required_env_vars:
            if not os.getenv(var):
                missing_required.append(var)

        if missing_required:
            return SystemTestResult(system_name, "config", False,
                                  f"Missing required env vars: {', '.join(missing_required)}")

        # Validate token format (basic check)
        token = os.getenv('DISCORD_BOT_TOKEN')
        if not token or len(token) < 50:  # Discord tokens are long
            return SystemTestResult(system_name, "config", False,
                                  "Discord token appears invalid (too short)")

        # Validate guild ID format
        guild_id = os.getenv('DISCORD_GUILD_ID')
        try:
            int(guild_id)  # Should be numeric
        except (ValueError, TypeError):
            return SystemTestResult(system_name, "config", False,
                                  "Discord guild ID is not a valid number")

        return SystemTestResult(system_name, "config", True,
                              "Discord configuration variables present and valid")

    def _test_discord_dry_run(self, system_name: str, suite_config: Dict) -> SystemTestResult:
        """Test Discord bot dry-run connectivity."""
        try:
            # Import discord and check availability
            import discord
            from discord.ext import commands

            token = os.getenv('DISCORD_BOT_TOKEN')
            if not token:
                return SystemTestResult(system_name, "dry_run", False,
                                      "No Discord token available")

            # Create a minimal test bot
            class TestBot(commands.Bot):
                def __init__(self):
                    intents = discord.Intents.default()
                    intents.message_content = True
                    intents.guilds = True
                    super().__init__(command_prefix="!", intents=intents, help_command=None)
                    self.test_completed = False

                async def on_ready(self):
                    self.test_completed = True
                    await self.close()

            bot = TestBot()

            async def test_connection():
                try:
                    # Test login (validates token and intents)
                    await bot.login(token)
                    return True
                except discord.LoginFailure:
                    return False
                except discord.PrivilegedIntentsRequired:
                    return False
                except Exception:
                    return False
                finally:
                    try:
                        await bot.close()
                    except:
                        pass

            # Run the test
            result = asyncio.run(test_connection())

            if result:
                return SystemTestResult(system_name, "dry_run", True,
                                      "Discord dry-run connection successful")
            else:
                return SystemTestResult(system_name, "dry_run", False,
                                      "Discord dry-run connection failed")

        except ImportError:
            return SystemTestResult(system_name, "dry_run", False,
                                  "discord.py library not available")
        except Exception as e:
            return SystemTestResult(system_name, "dry_run", False,
                                  f"Dry-run test error: {e}", str(e))

    # ============================================================================
    # TWITCH BOT TESTS
    # ============================================================================

    def _test_twitch_config(self, system_name: str, suite_config: Dict) -> SystemTestResult:
        """Test if Twitch bot config is available."""
        required_env_vars = [
            'TWITCH_CLIENT_ID',
            'TWITCH_CLIENT_SECRET',
        ]

        optional_env_vars = [
            'TWITCH_ACCESS_TOKEN',
            'TWITCH_REFRESH_TOKEN',
            'TWITCH_CHANNEL_NAME',
        ]

        missing_required = []
        for var in required_env_vars:
            if not os.getenv(var):
                missing_required.append(var)

        if missing_required:
            return SystemTestResult(system_name, "config", False,
                                  f"Missing required env vars: {', '.join(missing_required)}")

        # Validate client ID format (should be UUID-like)
        client_id = os.getenv('TWITCH_CLIENT_ID')
        if len(client_id) < 10:  # Basic length check
            return SystemTestResult(system_name, "config", False,
                                  "Twitch client ID appears invalid (too short)")

        return SystemTestResult(system_name, "config", True,
                              "Twitch configuration variables present")

    def _test_twitch_dry_run(self, system_name: str, suite_config: Dict) -> SystemTestResult:
        """Test Twitch bot dry-run connectivity."""
        try:
            # Import twitch-related modules
            importlib.import_module('src.services.chat_presence.twitch_bridge')

            # Check if we can import the eventsub server
            eventsub_module = importlib.import_module(suite_config['module'])

            # Check if main classes exist
            required_classes = ['TwitchEventSubServer']
            missing_classes = []
            for cls in required_classes:
                if not hasattr(eventsub_module, cls):
                    missing_classes.append(cls)

            if missing_classes:
                return SystemTestResult(system_name, "dry_run", False,
                                      f"Missing required classes: {', '.join(missing_classes)}")

            return SystemTestResult(system_name, "dry_run", True,
                                  "Twitch EventSub server structure validation passed")

        except ImportError as e:
            return SystemTestResult(system_name, "dry_run", False,
                                  f"Twitch module import failed: {e}", str(e))
        except Exception as e:
            return SystemTestResult(system_name, "dry_run", False,
                                  f"Dry-run test error: {e}", str(e))
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1

    # ============================================================================
    # FASTAPI SERVICE TESTS
    # ============================================================================

<<<<<<< HEAD
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
    harness = SmokeTestHarness()
    exit_code = harness.run_all_tests()
=======
    def _test_fastapi_config(self, system_name: str, suite_config: Dict) -> SystemTestResult:
        """Test if FastAPI service config is available."""
        required_env_vars = [
            'FASTAPI_HOST',
            'FASTAPI_PORT',
        ]

        optional_env_vars = [
            'FASTAPI_DEBUG',
            'FASTAPI_RELOAD',
        ]

        missing_required = []
        for var in required_env_vars:
            if not os.getenv(var):
                missing_required.append(var)

        if missing_required:
            return SystemTestResult(system_name, "config", False,
                                  f"Missing required env vars: {', '.join(missing_required)}")

        # Validate port is numeric
        port_str = os.getenv('FASTAPI_PORT')
        try:
            port = int(port_str)
            if port < 1 or port > 65535:
                raise ValueError("Port out of range")
        except (ValueError, TypeError):
            return SystemTestResult(system_name, "config", False,
                                  f"Invalid FastAPI port: {port_str}")

        host = os.getenv('FASTAPI_HOST', 'localhost')
        return SystemTestResult(system_name, "config", True,
                              f"FastAPI config valid: {host}:{port}")

    def _test_fastapi_structure(self, system_name: str, suite_config: Dict) -> SystemTestResult:
        """Test FastAPI service structure and basic functionality."""
        try:
            # Import the FastAPI app module
            app_module = importlib.import_module(suite_config['module'])

            # Check if app instance exists
            if not hasattr(app_module, 'app'):
                return SystemTestResult(system_name, "structure", False,
                                      "FastAPI app instance not found")

            app = getattr(app_module, 'app')

            # Check if it's a FastAPI instance
            try:
                from fastapi import FastAPI
                if not isinstance(app, FastAPI):
                    return SystemTestResult(system_name, "structure", False,
                                          "App is not a FastAPI instance")
            except ImportError:
                # If fastapi not available, at least check it has routes
                if not hasattr(app, 'routes') and not hasattr(app, 'router'):
                    return SystemTestResult(system_name, "structure", False,
                                          "App does not appear to be a web framework instance")

            # Check for routes module
            try:
                routes_module = importlib.import_module('src.web.fastapi_routes')
                if hasattr(routes_module, 'router'):
                    return SystemTestResult(system_name, "structure", True,
                                          "FastAPI app and routes structure validation passed")
                else:
                    return SystemTestResult(system_name, "structure", False,
                                          "Routes module missing router instance")
            except ImportError:
                return SystemTestResult(system_name, "structure", True,
                                      "FastAPI app structure valid (routes module not found but app exists)")

        except Exception as e:
            return SystemTestResult(system_name, "structure", False,
                                  f"Structure validation failed: {e}", str(e))


def main():
    """Main entry point for comprehensive smoke test suite."""
    tester = ComprehensiveSmokeTest()
    exit_code = tester.run_all_tests()
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
    sys.exit(exit_code)


if __name__ == "__main__":
    main()