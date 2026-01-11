#!/usr/bin/env python3
"""
WordPress Page Operations Script
Creates the 9 required pages and fixes menu typo for TradingRobotPlug.com

Pages to create:
- Content pages: waitlist, thank-you, pricing, features, ai-swarm, blog (6 pages)
- Legal pages: privacy, terms-of-service, product-terms (3 pages)

Menu fix: 'Capabilitie' → 'Capabilities'
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional

# Add repository root to path
repo_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(repo_root))

try:
    import paramiko
    PARAMIKO_AVAILABLE = True
except ImportError:
    PARAMIKO_AVAILABLE = False
    print("❌ Paramiko not available. Install with: pip install paramiko")

class WordPressPageCreator:
    """Creates WordPress pages via SSH and WP-CLI"""

    def __init__(self, site_key: str = "tradingrobotplug.com"):
        self.site_key = site_key
        self.site_config = self._load_site_config()
        if not self.site_config:
            raise ValueError(f"❌ No configuration found for site: {site_key}")

    def _load_site_config(self) -> Optional[Dict]:
        """Load site configuration from credentials file"""
        creds_file = repo_root / ".deploy_credentials" / "sites.json"
        if creds_file.exists():
            try:
                with open(creds_file, 'r') as f:
                    creds_data = json.load(f)
                    config = creds_data.get(self.site_key)
                    if config:
                        # Ensure wp_path is set correctly
                        if "remote_path" in config and "wp_path" not in config:
                            config["wp_path"] = config["remote_path"]
                        elif "wp_path" not in config:
                            config["wp_path"] = "/public_html"  # fallback
                        return config
            except Exception as e:
                print(f"⚠️ Failed to load credentials: {e}")

        return None

    def execute_wp_cli(self, command: str) -> Dict[str, str]:
        """Execute WP-CLI command over SSH"""
        if not PARAMIKO_AVAILABLE:
            return {"success": False, "error": "Paramiko not available"}

        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(
                hostname=self.site_config["host"],
                username=self.site_config["username"],
                password=self.site_config["password"],
                port=self.site_config["port"]
            )

            # Build WP-CLI command
            wp_path = self.site_config.get("wp_path", "/public_html")
            wp_command = f"cd {wp_path} && wp {command}"

            stdin, stdout, stderr = ssh.exec_command(wp_command)
            output = stdout.read().decode()
            error = stderr.read().decode()

            ssh.close()

            return {
                "success": len(error) == 0,
                "output": output,
                "error": error
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def create_page(self, title: str, slug: str, content: str = "") -> Dict[str, str]:
        """Create a WordPress page"""
        command = f'post create --post_type=page --post_title="{title}" --post_name="{slug}" --post_content="{content}" --post_status=publish'
        print(f"📄 Creating page: {title} (slug: {slug})")
        result = self.execute_wp_cli(command)
        if result["success"]:
            print(f"✅ Created page: {title}")
        else:
            print(f"❌ Failed to create page {title}: {result['error']}")
        return result

    def fix_menu_typo(self) -> Dict[str, str]:
        """Fix menu typo: 'Capabilitie' → 'Capabilities'"""
        print("🔧 Fixing menu typo: 'Capabilitie' → 'Capabilities'")
        command = 'search-replace "Capabilitie" "Capabilities"'
        result = self.execute_wp_cli(command)
        if result["success"]:
            print("✅ Menu typo fixed")
        else:
            print(f"❌ Failed to fix menu typo: {result['error']}")
        return result

    def create_all_pages(self) -> List[Dict[str, str]]:
        """Create all 9 required pages"""
        results = []

        # Content pages (6 pages)
        content_pages = [
            ("Waitlist", "waitlist", "Join our waitlist to get early access to TradingRobotPlug features."),
            ("Thank You", "thank-you", "Thank you for your interest in TradingRobotPlug!"),
            ("Pricing", "pricing", "Choose the perfect plan for your trading needs."),
            ("Features", "features", "Discover all the powerful features of TradingRobotPlug."),
            ("AI Swarm", "ai-swarm", "Experience the power of AI-driven trading with our swarm intelligence."),
            ("Blog", "blog", "Stay updated with the latest trading insights and platform updates.")
        ]

        # Legal pages (3 pages)
        legal_pages = [
            ("Privacy Policy", "privacy", "Your privacy is important to us. Learn how we protect your data."),
            ("Terms of Service", "terms-of-service", "Terms and conditions for using TradingRobotPlug."),
            ("Product Terms", "product-terms", "Specific terms for our trading products and services.")
        ]

        all_pages = content_pages + legal_pages

        for title, slug, content in all_pages:
            result = self.create_page(title, slug, content)
            results.append({"page": title, "result": result})

        return results

def main():
    """Main execution function"""
    print("🚀 Starting WordPress Page Operations for TradingRobotPlug.com")
    print("=" * 60)

    try:
        creator = WordPressPageCreator()

        # Create all pages
        print("\n📄 Creating 9 WordPress pages...")
        page_results = creator.create_all_pages()

        # Fix menu typo
        print("\n🔧 Fixing menu typo...")
        menu_result = creator.fix_menu_typo()

        # Summary
        print("\n" + "=" * 60)
        print("📊 OPERATION SUMMARY")
        print("=" * 60)

        success_count = sum(1 for r in page_results if r["result"]["success"])
        print(f"✅ Pages created successfully: {success_count}/9")

        if menu_result["success"]:
            print("✅ Menu typo fixed successfully")
        else:
            print("❌ Menu typo fix failed")

        print("\n🎯 WordPress operations complete!")
        print("Next: Run validation checklist to verify all pages load correctly")

        return success_count == 9 and menu_result["success"]

    except Exception as e:
        print(f"❌ Error during WordPress operations: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)