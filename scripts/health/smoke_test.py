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
            'discord_messenger': {
                'name': 'Discord Messenger',
                'module': 'src.discord_commander.unified_discord_bot',
                'tests': [
                    self._test_import,
                    self._test_discord_config,
                    self._test_discord_dry_run
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
    # DISCORD MESSENGER TESTS
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

def main():
    """Main entry point for smoke test harness."""
    harness = RecoverySmokeTest()
    exit_code = harness.run_all_tests()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()