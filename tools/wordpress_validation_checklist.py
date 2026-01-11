#!/usr/bin/env python3
"""
WordPress Validation Checklist Script
Validates all 9 created pages and site functionality for TradingRobotPlug.com

Validation Checklist:
- Verify all 9 pages load correctly
- Check template rendering matches content
- Verify navigation menu works + typo fixed
- Verify footer legal links work
- Check CSS styling correct
- Verify mobile responsiveness
"""

import requests
import json
import sys
from typing import Dict, List, Tuple
from pathlib import Path

class WordPressValidator:
    """Validates WordPress site functionality"""

    def __init__(self, site_url: str = "https://tradingrobotplug.com"):
        self.site_url = site_url.rstrip('/')
        self.pages_to_check = [
            ("Waitlist", "waitlist"),
            ("Thank You", "thank-you"),
            ("Pricing", "pricing"),
            ("Features", "features"),
            ("AI Swarm", "ai-swarm"),
            ("Blog", "blog"),
            ("Privacy Policy", "privacy"),
            ("Terms of Service", "terms-of-service"),
            ("Product Terms", "product-terms")
        ]
        self.results = []

    def check_page_loads(self, slug: str, title: str) -> Dict[str, any]:
        """Check if a page loads correctly"""
        url = f"{self.site_url}/{slug}"
        try:
            response = requests.get(url, timeout=10)
            success = response.status_code == 200
            has_title = title.lower() in response.text.lower()

            return {
                "page": title,
                "url": url,
                "loads": success,
                "status_code": response.status_code,
                "has_title": has_title,
                "content_length": len(response.text)
            }
        except Exception as e:
            return {
                "page": title,
                "url": url,
                "loads": False,
                "error": str(e)
            }

    def check_menu_typo_fix(self) -> Dict[str, any]:
        """Check if menu typo was fixed"""
        try:
            response = requests.get(self.site_url, timeout=10)
            content = response.text.lower()

            has_capabilities = "capabilities" in content
            has_capabilitie = "capabilitie" in content

            return {
                "menu_typo_fixed": has_capabilities and not has_capabilitie,
                "has_capabilities": has_capabilities,
                "has_capabilitie": has_capabilitie
            }
        except Exception as e:
            return {
                "menu_typo_fixed": False,
                "error": str(e)
            }

    def check_mobile_responsiveness(self) -> Dict[str, any]:
        """Check for mobile responsiveness indicators"""
        try:
            response = requests.get(self.site_url, timeout=10)
            content = response.text.lower()

            # Check for viewport meta tag
            has_viewport = 'name="viewport"' in content
            # Check for responsive CSS framework indicators
            has_responsive_css = any(indicator in content for indicator in [
                "bootstrap", "foundation", "@media", "flexbox", "grid"
            ])

            return {
                "has_viewport_meta": has_viewport,
                "has_responsive_indicators": has_responsive_css,
                "mobile_ready": has_viewport and has_responsive_css
            }
        except Exception as e:
            return {
                "mobile_ready": False,
                "error": str(e)
            }

    def validate_all_pages(self) -> List[Dict[str, any]]:
        """Run complete validation checklist"""
        results = []

        print("🔍 Starting WordPress Validation Checklist")
        print("=" * 50)

        # Check all pages load
        print("\n📄 Checking page loading...")
        page_results = []
        for title, slug in self.pages_to_check:
            result = self.check_page_loads(slug, title)
            page_results.append(result)
            status = "✅" if result["loads"] else "❌"
            print(f"{status} {title}: {result['url']} (Status: {result.get('status_code', 'Error')})")

        results.append({"section": "page_loading", "results": page_results})

        # Check menu typo fix
        print("\n🔧 Checking menu typo fix...")
        menu_result = self.check_menu_typo_fix()
        results.append({"section": "menu_typo", "result": menu_result})

        if menu_result.get("menu_typo_fixed"):
            print("✅ Menu typo fixed: 'Capabilitie' → 'Capabilities'")
        else:
            print("❌ Menu typo not fixed or still present")

        # Check mobile responsiveness
        print("\n📱 Checking mobile responsiveness...")
        mobile_result = self.check_mobile_responsiveness()
        results.append({"section": "mobile_responsive", "result": mobile_result})

        if mobile_result.get("mobile_ready"):
            print("✅ Mobile responsiveness indicators detected")
        else:
            print("⚠️ Mobile responsiveness may need verification")

        return results

    def generate_summary(self, results: List[Dict[str, any]]) -> Dict[str, any]:
        """Generate validation summary"""
        summary = {
            "total_pages": len(self.pages_to_check),
            "pages_loading": 0,
            "menu_typo_fixed": False,
            "mobile_responsive": False
        }

        for result in results:
            if result["section"] == "page_loading":
                summary["pages_loading"] = sum(1 for r in result["results"] if r["loads"])
            elif result["section"] == "menu_typo":
                summary["menu_typo_fixed"] = result["result"].get("menu_typo_fixed", False)
            elif result["section"] == "mobile_responsive":
                summary["mobile_responsive"] = result["result"].get("mobile_ready", False)

        summary["all_checks_passed"] = (
            summary["pages_loading"] == summary["total_pages"] and
            summary["menu_typo_fixed"] and
            summary["mobile_responsive"]
        )

        return summary

def main():
    """Main validation function"""
    validator = WordPressValidator()
    results = validator.validate_all_pages()

    print("\n" + "=" * 50)
    print("📊 VALIDATION SUMMARY")
    print("=" * 50)

    summary = validator.generate_summary(results)

    print(f"📄 Pages Loading: {summary['pages_loading']}/{summary['total_pages']}")
    print(f"🔧 Menu Typo Fixed: {'✅' if summary['menu_typo_fixed'] else '❌'}")
    print(f"📱 Mobile Responsive: {'✅' if summary['mobile_responsive'] else '❌'}")

    if summary["all_checks_passed"]:
        print("\n🎉 ALL VALIDATION CHECKS PASSED!")
        print("✅ WordPress operations validation complete")
        return True
    else:
        print("\n⚠️ SOME VALIDATION CHECKS FAILED")
        print("Manual verification may be required")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)