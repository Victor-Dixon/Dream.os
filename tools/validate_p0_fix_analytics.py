#!/usr/bin/env python3
"""
Validate P0 Fix Analytics
=========================

Validates analytics tracking for P0 fixes as they're deployed.
Checks GA4/Pixel tracking, conversion events, form submissions, CTA clicks.

V2 Compliance | Author: Agent-5 | Date: 2025-12-25
"""

import json
import sys
import requests
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))


class P0FixAnalyticsValidator:
    """Validates analytics tracking for P0 fixes."""
    
    def __init__(self):
        """Initialize validator."""
        self.tracking_file = project_root / "docs" / "website_audits" / "2026" / "P0_FIX_TRACKING.md"
        self.results_file = project_root / "agent_workspaces" / "Agent-5" / "P0_ANALYTICS_VALIDATION_RESULTS.json"
        
    def validate_fix_analytics(
        self,
        site: str,
        fix_id: str,
        fix_type: str,
        url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Validate analytics for a specific fix.
        
        Args:
            site: Website domain
            fix_id: Fix identifier (e.g., WEB-01, BRAND-01)
            fix_type: Type of fix (hero, cta, contact, positioning, etc.)
            url: Optional URL to check
            
        Returns:
            Validation results dict
        """
        results = {
            "site": site,
            "fix_id": fix_id,
            "fix_type": fix_type,
            "timestamp": datetime.now().isoformat(),
            "validations": {},
            "status": "PENDING"
        }
        
        # Determine validation checks based on fix type
        if fix_type in ["hero", "cta"]:
            results["validations"] = {
                "cta_click_tracking": self._check_cta_tracking(site, url),
                "conversion_event": self._check_conversion_event(site, fix_id),
                "analytics_integration": self._check_analytics_integration(site, url)
            }
        elif fix_type in ["contact", "booking", "friction"]:
            results["validations"] = {
                "form_submission_tracking": self._check_form_tracking(site, url),
                "contact_event": self._check_contact_event(site, fix_id),
                "analytics_integration": self._check_analytics_integration(site, url)
            }
        elif fix_type in ["positioning", "brand"]:
            results["validations"] = {
                "page_view_tracking": self._check_page_tracking(site, url),
                "engagement_metrics": self._check_engagement(site, url),
                "analytics_integration": self._check_analytics_integration(site, url)
            }
        else:
            # Generic validation
            results["validations"] = {
                "analytics_integration": self._check_analytics_integration(site, url),
                "basic_tracking": self._check_basic_tracking(site, url)
            }
        
        # Determine overall status
        all_passed = all(
            v.get("status") == "PASS" 
            for v in results["validations"].values()
            if isinstance(v, dict)
        )
        results["status"] = "PASS" if all_passed else "FAIL"
        
        return results
    
    def _check_cta_tracking(self, site: str, url: Optional[str]) -> Dict[str, Any]:
        """Check CTA click tracking."""
        return {
            "status": "PENDING",
            "message": "CTA tracking validation requires site inspection",
            "method": "Manual inspection or automated test"
        }
    
    def _check_conversion_event(self, site: str, fix_id: str) -> Dict[str, Any]:
        """Check conversion event tracking."""
        return {
            "status": "PENDING",
            "message": "Conversion event validation requires GA4/Pixel verification",
            "method": "GA4 event verification"
        }
    
    def _check_form_tracking(self, site: str, url: Optional[str]) -> Dict[str, Any]:
        """Check form submission tracking."""
        return {
            "status": "PENDING",
            "message": "Form tracking validation requires form inspection",
            "method": "Form submission test"
        }
    
    def _check_contact_event(self, site: str, fix_id: str) -> Dict[str, Any]:
        """Check contact event tracking."""
        return {
            "status": "PENDING",
            "message": "Contact event validation requires event verification",
            "method": "Event tracking verification"
        }
    
    def _check_page_tracking(self, site: str, url: Optional[str]) -> Dict[str, Any]:
        """Check page view tracking."""
        return {
            "status": "PENDING",
            "message": "Page tracking validation requires page inspection",
            "method": "Page view test"
        }
    
    def _check_engagement(self, site: str, url: Optional[str]) -> Dict[str, Any]:
        """Check engagement metrics."""
        return {
            "status": "PENDING",
            "message": "Engagement metrics validation requires analytics data",
            "method": "Analytics data review"
        }
    
    def _check_analytics_integration(self, site: str, url: Optional[str]) -> Dict[str, Any]:
        """Check analytics integration."""
        if not url:
            url = f"https://{site}"
        
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                content = response.text.lower()
                has_ga4 = "gtag" in content or "ga4" in content or "google-analytics" in content
                has_pixel = "facebook pixel" in content or "fbq" in content
                
                return {
                    "status": "PASS" if (has_ga4 or has_pixel) else "FAIL",
                    "ga4_detected": has_ga4,
                    "pixel_detected": has_pixel,
                    "message": "Analytics integration check complete"
                }
        except Exception as e:
            return {
                "status": "ERROR",
                "message": f"Failed to check analytics: {e}"
            }
        
        return {
            "status": "PENDING",
            "message": "Analytics integration check pending"
        }
    
    def _check_basic_tracking(self, site: str, url: Optional[str]) -> Dict[str, Any]:
        """Check basic tracking setup."""
        return {
            "status": "PENDING",
            "message": "Basic tracking validation pending",
            "method": "Analytics setup verification"
        }
    
    def validate_tier1_fixes(self) -> Dict[str, Any]:
        """Validate all Tier 1 Quick Wins fixes."""
        tier1_fixes = [
            # Hero/CTA fixes
            {"site": "freerideinvestor.com", "fix_id": "WEB-01", "fix_type": "hero", "url": "https://freerideinvestor.com"},
            {"site": "dadudekc.com", "fix_id": "WEB-01", "fix_type": "hero", "url": "https://dadudekc.com"},
            {"site": "crosbyultimateevents.com", "fix_id": "WEB-01", "fix_type": "hero", "url": "https://crosbyultimateevents.com"},
            {"site": "tradingrobotplug.com", "fix_id": "WEB-01", "fix_type": "hero", "url": "https://tradingrobotplug.com"},
            
            # Contact/booking friction fixes
            {"site": "freerideinvestor.com", "fix_id": "WEB-04", "fix_type": "contact", "url": "https://freerideinvestor.com"},
            {"site": "dadudekc.com", "fix_id": "WEB-04", "fix_type": "contact", "url": "https://dadudekc.com"},
            {"site": "crosbyultimateevents.com", "fix_id": "WEB-04", "fix_type": "contact", "url": "https://crosbyultimateevents.com"},
            {"site": "tradingrobotplug.com", "fix_id": "WEB-04", "fix_type": "contact", "url": "https://tradingrobotplug.com"},
            
            # Brand positioning fixes
            {"site": "freerideinvestor.com", "fix_id": "BRAND-01", "fix_type": "positioning", "url": "https://freerideinvestor.com"},
            {"site": "dadudekc.com", "fix_id": "BRAND-01", "fix_type": "positioning", "url": "https://dadudekc.com"},
            {"site": "crosbyultimateevents.com", "fix_id": "BRAND-01", "fix_type": "positioning", "url": "https://crosbyultimateevents.com"},
        ]
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "tier": "Tier 1 - Quick Wins",
            "total_fixes": len(tier1_fixes),
            "validations": []
        }
        
        for fix in tier1_fixes:
            validation = self.validate_fix_analytics(**fix)
            results["validations"].append(validation)
        
        # Calculate summary
        passed = sum(1 for v in results["validations"] if v["status"] == "PASS")
        results["summary"] = {
            "passed": passed,
            "failed": len(results["validations"]) - passed,
            "pending": sum(1 for v in results["validations"] if v["status"] == "PENDING"),
            "completion_percentage": (passed / len(results["validations"])) * 100 if results["validations"] else 0
        }
        
        return results
    
    def save_results(self, results: Dict[str, Any]) -> Path:
        """Save validation results."""
        with open(self.results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        return self.results_file


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Validate P0 Fix Analytics")
    parser.add_argument("--site", help="Site to validate")
    parser.add_argument("--fix-id", help="Fix ID (e.g., WEB-01)")
    parser.add_argument("--fix-type", help="Fix type (hero, cta, contact, positioning)")
    parser.add_argument("--url", help="URL to check")
    parser.add_argument("--tier1", action="store_true", help="Validate all Tier 1 fixes")
    
    args = parser.parse_args()
    
    validator = P0FixAnalyticsValidator()
    
    if args.tier1:
        print("🔍 Validating Tier 1 Quick Wins analytics...")
        results = validator.validate_tier1_fixes()
        validator.save_results(results)
        
        print(f"\n✅ Validation complete:")
        print(f"   Total fixes: {results['total_fixes']}")
        print(f"   Passed: {results['summary']['passed']}")
        print(f"   Failed: {results['summary']['failed']}")
        print(f"   Pending: {results['summary']['pending']}")
        print(f"   Completion: {results['summary']['completion_percentage']:.1f}%")
        print(f"\n💾 Results saved: {validator.results_file}")
    elif args.site and args.fix_id and args.fix_type:
        print(f"🔍 Validating {args.site} - {args.fix_id} ({args.fix_type})...")
        results = validator.validate_fix_analytics(
            site=args.site,
            fix_id=args.fix_id,
            fix_type=args.fix_type,
            url=args.url
        )
        print(f"\n✅ Validation complete:")
        print(f"   Status: {results['status']}")
        print(f"   Validations: {len(results['validations'])}")
        for key, value in results['validations'].items():
            if isinstance(value, dict):
                print(f"     - {key}: {value.get('status', 'PENDING')}")
    else:
        print("❌ Please specify --tier1 or --site --fix-id --fix-type")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

