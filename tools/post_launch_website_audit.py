#!/usr/bin/env python3
"""
Post-Launch Website Performance Audit
====================================

Validates website readiness for Agent Cellphone V2 launch.
Checks critical websites for performance, accessibility, and functionality.

Author: Agent-7 (Tools Consolidation & Architecture Lead)
Date: 2026-01-13
"""

import requests
import time
from pathlib import Path
from typing import Dict, List
from urllib.parse import urljoin

class PostLaunchWebsiteAudit:
    def __init__(self):
        self.websites = [
            "https://tradingrobotplug.com",
            "https://weareswarm.online",
            "https://ariajet.site",
            "https://crosbyultimateevents.com",
            "https://dadudekc.com"
        ]

        self.session = requests.Session()
        self.session.timeout = 10

    def audit_website(self, url: str) -> Dict:
        """Audit a single website for post-launch readiness."""
        results = {
            "url": url,
            "status": "unknown",
            "response_time": None,
            "status_code": None,
            "content_length": None,
            "has_title": False,
            "has_navigation": False,
            "mobile_friendly": False,
            "errors": []
        }

        try:
            start_time = time.time()
            response = self.session.get(url, timeout=10)
            response_time = time.time() - start_time

            results["response_time"] = round(response_time, 2)
            results["status_code"] = response.status_code
            results["content_length"] = len(response.content)

            if response.status_code == 200:
                results["status"] = "✅ OK"

                # Check content
                content = response.text.lower()
                results["has_title"] = "<title>" in content
                results["has_navigation"] = "nav" in content or "menu" in content

                # Basic mobile check (viewport meta tag)
                results["mobile_friendly"] = "viewport" in content

            elif response.status_code >= 400:
                results["status"] = f"❌ ERROR ({response.status_code})"
                results["errors"].append(f"HTTP {response.status_code}")

        except requests.exceptions.Timeout:
            results["status"] = "❌ TIMEOUT"
            results["errors"].append("Request timeout")
        except requests.exceptions.ConnectionError:
            results["status"] = "❌ CONNECTION ERROR"
            results["errors"].append("Connection failed")
        except Exception as e:
            results["status"] = "❌ ERROR"
            results["errors"].append(str(e))

        return results

    def run_full_audit(self) -> Dict:
        """Run comprehensive audit on all websites."""
        print("🚀 POST-LAUNCH WEBSITE PERFORMANCE AUDIT")
        print("=" * 60)
        print(f"Auditing {len(self.websites)} websites for launch readiness...")
        print()

        results = {}
        total_sites = len(self.websites)
        healthy_sites = 0

        for url in self.websites:
            print(f"🔍 Auditing: {url}")
            result = self.audit_website(url)
            results[url] = result

            status = result["status"]
            response_time = result["response_time"]

            if response_time:
                print(f"   {status} - {response_time}s")
            else:
                print(f"   {status}")

            if result["errors"]:
                for error in result["errors"]:
                    print(f"   ⚠️  {error}")

            if "✅" in status:
                healthy_sites += 1

            print()

        # Summary
        print("📊 AUDIT SUMMARY")
        print("=" * 60)
        print(f"Total websites: {total_sites}")
        print(f"Healthy websites: {healthy_sites}")
        print(f"Success rate: {healthy_sites/total_sites*100:.1f}%")

        if healthy_sites == total_sites:
            print("🎉 ALL WEBSITES READY FOR LAUNCH!")
        elif healthy_sites >= total_sites * 0.8:
            print("✅ MOSTLY READY - Minor issues to address")
        else:
            print("⚠️  SIGNIFICANT ISSUES - Needs attention before launch")

        return results

def main():
    auditor = PostLaunchWebsiteAudit()
    results = auditor.run_full_audit()

    # Save results
    output_file = Path("post_launch_audit_results.json")
    import json
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n💾 Results saved to: {output_file}")

if __name__ == "__main__":
    main()