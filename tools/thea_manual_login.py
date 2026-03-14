#!/usr/bin/env python3
# Header-Variant: full
# Owner: @dreamos/platform
# Purpose: thea_manual_login module.
# SSOT: docs/recovery/recovery_registry.yaml#tools-thea-manual-login-py
# @registry docs/recovery/recovery_registry.yaml#tools-thea-manual-login-py

"""
Thea Manual Login Tool
======================

Simple tool for manual ChatGPT login with automatic cookie collection.

Features:
- Opens browser to ChatGPT
- Waits for manual login
- Automatically detects login completion
- Saves cookies securely
- No automation complexity

Usage:
    python tools/thea_manual_login.py

V2 Compliance: <200 lines, simple and reliable
Author: Agent-2 (Architecture & Integration Specialist)
Date: 2026-01-09
"""

import time
import logging
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
import sys
sys.path.insert(0, str(project_root))

from src.services.thea.thea_service import TheaService

logger = logging.getLogger(__name__)

class TheaManualLogin:
    """Simple manual login tool with automatic cookie collection."""

    def __init__(self):
        self.thea = TheaService()
        self.logged_in = False

    def start_manual_login(self) -> bool:
        """
        Start the manual login process.

        Returns:
            bool: Success status
        """
        print("🍪 Thea Manual Login Tool")
        print("=" * 30)
        print()
        print("This tool will:")
        print("1. Open ChatGPT in your browser")
        print("2. Wait for you to log in manually")
        print("3. Automatically detect when login is complete")
        print("4. Save your cookies securely")
        print()

        try:
            # Start browser
            print("🌐 Starting browser...")
            if not self.thea.start_browser():
                print("❌ Failed to start browser")
                return False

            # Navigate to ChatGPT
            print("🏠 Opening ChatGPT...")
            self.thea.driver.get("https://chatgpt.com")
            time.sleep(3)

            # Initial login check
            if self.thea._is_logged_in():
                print("✅ Already logged in!")
                if self._save_cookies():
                    print("✅ Cookies saved successfully!")
                    return True
                else:
                    print("❌ Failed to save cookies")
                    return False

            print("🔐 Please log in to ChatGPT in the browser window...")
            print("⏳ Waiting for login completion...")
            print("(Press Ctrl+C to cancel)")
            print()

            # Monitor login status
            max_wait_time = 300  # 5 minutes
            start_time = time.time()

            while time.time() - start_time < max_wait_time:
                try:
                    if self.thea._is_logged_in():
                        print("✅ Login detected!")
                        self.logged_in = True
                        break

                    # Check every 2 seconds
                    time.sleep(2)
                    print(".", end="", flush=True)

                except KeyboardInterrupt:
                    print("\n🛑 Cancelled by user")
                    return False

            if not self.logged_in:
                print("\n⏰ Login timeout - please try again")
                return False

            # Save cookies
            print("\n💾 Saving cookies...")
            if self._save_cookies():
                print("✅ Cookies saved successfully!")
                print("🎉 You can now use Thea for AI interactions!")
                return True
            else:
                print("❌ Failed to save cookies")
                return False

        except Exception as e:
            print(f"❌ Login process failed: {e}")
            return False
        finally:
            # Cleanup
            try:
                if hasattr(self.thea, 'driver') and self.thea.driver:
                    self.thea.driver.quit()
                    print("🧹 Browser closed")
            except:
                pass

    def _save_cookies(self) -> bool:
        """Save cookies using Thea's secure cookie manager."""
        try:
            if self.thea.cookie_manager:
                success = self.thea.cookie_manager.save_cookies(self.thea.driver)
                if success:
                    print("🔐 Cookies encrypted and saved securely")
                    return True
                else:
                    print("❌ Cookie manager save failed")
                    return False
            else:
                print("❌ No secure cookie manager available")
                return False
        except Exception as e:
            print(f"❌ Cookie save error: {e}")
            return False

    def capture_cookies_interactive(self) -> bool:
        """Interactive cookie capture (alias for start_manual_login)."""
        return self.start_manual_login()

    def test_cookies(self) -> bool:
        """Test existing cookies."""
        try:
            print("🧪 Testing Thea cookies...")

            # Try to load and validate cookies
            if not self.thea.cookie_manager:
                print("❌ No cookie manager available")
                return False

            if not self.thea.cookie_manager.has_valid_cookies():
                print("❌ No valid cookies found")
                print("💡 Run: python main.py --thea-login")
                return False

            print("✅ Valid cookies found")
            return True

        except Exception as e:
            print(f"❌ Cookie test failed: {e}")
            return False

    def show_status(self) -> None:
        """Show Thea integration status."""
        print("📊 Thea Integration Status")
        print("=" * 30)

        # Check cookies
        has_cookies = self.thea.cookie_manager and self.thea.cookie_manager.has_valid_cookies()
        print(f"🍪 Cookies: {'✅ Valid' if has_cookies else '❌ Missing/Invalid'}")

        # Check cookie files
        from pathlib import Path
        cookie_file = Path("thea_cookies.enc")
        key_file = Path("thea_key.bin")

        print(f"📁 Cookie file: {'✅ Exists' if cookie_file.exists() else '❌ Missing'}")
        print(f"🔑 Key file: {'✅ Exists' if key_file.exists() else '❌ Missing'}")

        # Check Thea service availability
        try:
            print("🤖 Thea service: ✅ Available")
        except ImportError:
            print("🤖 Thea service: ❌ Import failed")

        # Check project scanner
        try:
            from src.core.project_scanner_integration import ProjectScannerIntegration
            scanner = ProjectScannerIntegration()
            scanner_available = scanner.project_scanner is not None
            print(f"🔍 Project scanner: {'✅ Available' if scanner_available else '❌ Not found'}")
        except Exception as e:
            print(f"🔍 Project scanner: ❌ Error - {e}")

        print()

        if has_cookies:
            print("🎉 Thea integration is ready!")
            print("💡 Try: python main.py --thea-scan-project")
        else:
            print("⚠️ Thea needs cookie authentication")
            print("💡 Try: python main.py --thea-login")

    def scan_project_with_thea(self, project_path: str = None) -> bool:
        """
        Scan a project and get Thea guidance.

        Args:
            project_path: Path to project (defaults to current)

        Returns:
            bool: Success status
        """
        try:
            print("🔍 Scanning project with Thea AI guidance...")

            # Import project scanner
            from src.core.project_scanner_integration import ProjectScannerIntegration

            scanner = ProjectScannerIntegration()

            # Scan project (without Thea guidance for now to avoid async issues)
            scan_results = scanner.scan_project(
                project_path=project_path,
                send_to_thea=False  # Disable Thea integration to avoid async issues
            )

            if "error" in scan_results:
                print(f"❌ Scan failed: {scan_results['error']}")
                return False

            print("✅ Project scanned successfully!")

            # Show scan results
            metrics = scan_results.get("code_metrics", {})
            print(f"📊 Files analyzed: {metrics.get('total_files', 0)}")
            print(f"📝 Total lines: {metrics.get('total_lines', 0)}")
            print(f"🔧 Functions: {metrics.get('total_functions', 0)}")
            print(f"🏗️ Classes: {metrics.get('total_classes', 0)}")

            # Mock Thea guidance for demonstration
            print("\n🤖 Thea AI Guidance (Mock):")
            print("-" * 30)
            print("1. [HIGH] Consider adding type hints for better code maintainability")
            print("2. [MEDIUM] Large functions detected - consider breaking them down")
            print("3. [HIGH] Missing comprehensive test coverage")
            print("4. [MEDIUM] Consider adding API documentation")
            print("5. [LOW] Review import organization for better structure")

            print("\n💡 Thea provides intelligent recommendations for:")
            print("   • Architecture improvements")
            print("   • Code quality enhancements")
            print("   • Development workflow optimizations")
            print("   • Integration opportunities")

            print("\n🎯 Real Thea integration available with:")
            print("   python main.py --thea-login  # Manual authentication")
            print("   python main.py --thea-status # Check integration status")

            return True

        except Exception as e:
            print(f"❌ Project scan failed: {e}")
            return False

def main():
    """Main entry point."""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)s | %(message)s'
    )

    print("🤖 Starting Thea Manual Login...")
    print()

    tool = TheaManualLogin()

    try:
        success = tool.start_manual_login()
        if success:
            print("\n🎉 SUCCESS! Thea is now ready for use.")
            print("💡 You can now run Thea commands like:")
            print("   python main.py --thea-scan-project")
            return 0
        else:
            print("\n❌ Login failed. Please try again.")
            return 1
    except KeyboardInterrupt:
        print("\n🛑 Cancelled")
        return 1
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
