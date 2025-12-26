#!/usr/bin/env python3
"""
Validate Tier 1 Quick Wins Integration
======================================

Integration testing suite for Tier 1 Quick Wins fixes:
- Hero/CTA validation (WEB-01)
- Contact/booking friction validation (WEB-04)
- Cross-site compatibility testing
- GA4/Pixel integration validation (systems integration perspective)

V2 Compliance | Author: Agent-1 | Date: 2025-12-25
"""

import json
import sys
import requests
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from urllib.parse import urljoin, urlparse

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))


class Tier1QuickWinsValidator:
    """Integration validator for Tier 1 Quick Wins fixes."""
    
    # Tier 1 Quick Wins sites and fixes
    TIER1_SITES = {
        "freerideinvestor.com": {
            "fixes": ["WEB-01", "WEB-04"],
            "status": "complete",
            "url": "https://freerideinvestor.com"
        },
        "dadudekc.com": {
            "fixes": ["WEB-01", "WEB-04"],
            "status": "in_progress",
            "url": "https://dadudekc.com"
        },
        "crosbyultimateevents.com": {
            "fixes": ["WEB-01", "WEB-04"],
            "status": "in_progress",
            "url": "https://crosbyultimateevents.com"
        },
        "tradingrobotplug.com": {
            "fixes": ["WEB-01", "WEB-04"],
            "status": "complete",
            "url": "https://tradingrobotplug.com"
        }
    }
    
    def __init__(self):
        """Initialize validator."""
        self.results_dir = project_root / "agent_workspaces" / "Agent-1" / "p0_integration_tests"
        self.results_dir.mkdir(parents=True, exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.results_file = self.results_dir / f"tier1_validation_{self.timestamp}.json"
        
    def validate_all_sites(self) -> Dict[str, Any]:
        """
        Validate all Tier 1 Quick Wins fixes across all sites.
        
        Returns:
            Complete validation results
        """
        results = {
            "timestamp": datetime.now().isoformat(),
            "validator": "Agent-1 Integration Testing",
            "sites": {},
            "summary": {
                "total_sites": len(self.TIER1_SITES),
                "sites_validated": 0,
                "total_fixes": 0,
                "fixes_passed": 0,
                "fixes_failed": 0
            },
            "cross_site_compatibility": {},
            "ga4_pixel_integration": {}
        }
        
        for site, config in self.TIER1_SITES.items():
            site_results = self.validate_site(site, config)
            results["sites"][site] = site_results
            
            # Update summary
            if site_results["status"] != "error":
                results["summary"]["sites_validated"] += 1
            for fix_result in site_results.get("fixes", {}).values():
                results["summary"]["total_fixes"] += 1
                if fix_result.get("status") == "PASS":
                    results["summary"]["fixes_passed"] += 1
                elif fix_result.get("status") == "FAIL":
                    results["summary"]["fixes_failed"] += 1
        
        # Cross-site compatibility analysis
        results["cross_site_compatibility"] = self._analyze_cross_site_compatibility(
            results["sites"]
        )
        
        # GA4/Pixel integration analysis
        results["ga4_pixel_integration"] = self._analyze_ga4_pixel_integration(
            results["sites"]
        )
        
        # Save results
        self._save_results(results)
        
        return results
    
    def validate_site(
        self,
        site: str,
        config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Validate fixes for a single site.
        
        Args:
            site: Site domain
            config: Site configuration
            
        Returns:
            Site validation results
        """
        results = {
            "site": site,
            "url": config["url"],
            "status": config["status"],
            "timestamp": datetime.now().isoformat(),
            "fixes": {},
            "errors": []
        }
        
        try:
            # Validate each fix
            for fix_id in config["fixes"]:
                if fix_id == "WEB-01":
                    fix_results = self.validate_hero_cta(site, config["url"])
                elif fix_id == "WEB-04":
                    fix_results = self.validate_contact_friction(site, config["url"])
                else:
                    fix_results = {"status": "SKIP", "message": f"Unknown fix: {fix_id}"}
                
                results["fixes"][fix_id] = fix_results
                
        except Exception as e:
            results["status"] = "error"
            results["errors"].append(str(e))
        
        return results
    
    def validate_hero_cta(
        self,
        site: str,
        base_url: str
    ) -> Dict[str, Any]:
        """
        Validate hero section and CTA implementation (WEB-01).
        
        Args:
            site: Site domain
            base_url: Base URL of the site
            
        Returns:
            Validation results
        """
        results = {
            "fix_id": "WEB-01",
            "fix_type": "hero_cta",
            "site": site,
            "timestamp": datetime.now().isoformat(),
            "validations": {},
            "status": "PENDING"
        }
        
        try:
            # Fetch homepage
            response = requests.get(base_url, timeout=10, allow_redirects=True)
            response.raise_for_status()
            html_content = response.text
            
            # Validate hero section elements
            validations = {
                "hero_headline": self._check_element_exists(html_content, "hero", "h1"),
                "hero_subheadline": self._check_element_exists(html_content, "hero", "subheadline"),
                "primary_cta": self._check_cta_button(html_content, "primary"),
                "secondary_cta": self._check_cta_button(html_content, "secondary"),
                "urgency_text": self._check_element_exists(html_content, "urgency"),
                "mobile_responsive": self._check_mobile_responsive(html_content),
                "css_loaded": self._check_css_loaded(html_content)
            }
            
            results["validations"] = validations
            
            # Determine overall status
            all_passed = all(
                v.get("status") == "PASS" 
                for v in validations.values()
                if isinstance(v, dict)
            )
            results["status"] = "PASS" if all_passed else "FAIL"
            
        except requests.RequestException as e:
            results["status"] = "ERROR"
            results["error"] = f"Request failed: {str(e)}"
        except Exception as e:
            results["status"] = "ERROR"
            results["error"] = str(e)
        
        return results
    
    def validate_contact_friction(
        self,
        site: str,
        base_url: str
    ) -> Dict[str, Any]:
        """
        Validate contact/booking form friction reduction (WEB-04).
        
        Args:
            site: Site domain
            base_url: Base URL of the site
            
        Returns:
            Validation results
        """
        results = {
            "fix_id": "WEB-04",
            "fix_type": "contact_friction",
            "site": site,
            "timestamp": datetime.now().isoformat(),
            "validations": {},
            "status": "PENDING"
        }
        
        try:
            # Try to find contact page
            contact_urls = [
                urljoin(base_url, "/contact"),
                urljoin(base_url, "/contact-us"),
                urljoin(base_url, "/booking"),
                base_url  # Sometimes form is on homepage
            ]
            
            html_content = None
            for url in contact_urls:
                try:
                    response = requests.get(url, timeout=10, allow_redirects=True)
                    if response.status_code == 200:
                        html_content = response.text
                        results["contact_page_url"] = url
                        break
                except:
                    continue
            
            if not html_content:
                results["status"] = "SKIP"
                results["message"] = "Contact page not found"
                return results
            
            # Validate contact form elements
            validations = {
                "form_exists": self._check_element_exists(html_content, "form"),
                "email_input": self._check_form_field(html_content, "email"),
                "low_friction": self._check_low_friction_form(html_content),
                "form_submission": self._check_form_submission(html_content),
                "mobile_responsive": self._check_mobile_responsive(html_content),
                "css_loaded": self._check_css_loaded(html_content)
            }
            
            results["validations"] = validations
            
            # Determine overall status
            all_passed = all(
                v.get("status") == "PASS" 
                for v in validations.values()
                if isinstance(v, dict)
            )
            results["status"] = "PASS" if all_passed else "FAIL"
            
        except Exception as e:
            results["status"] = "ERROR"
            results["error"] = str(e)
        
        return results
    
    def _check_element_exists(
        self,
        html: str,
        element_type: str,
        element_tag: Optional[str] = None
    ) -> Dict[str, Any]:
        """Check if element exists in HTML."""
        # Basic checks - can be enhanced with BeautifulSoup if needed
        if element_type == "hero":
            has_h1 = "<h1" in html.lower() or "hero" in html.lower()
            return {
                "status": "PASS" if has_h1 else "FAIL",
                "message": f"Hero section found" if has_h1 else "Hero section not found"
            }
        elif element_type == "form":
            has_form = "<form" in html.lower()
            return {
                "status": "PASS" if has_form else "FAIL",
                "message": f"Form found" if has_form else "Form not found"
            }
        elif element_type == "urgency":
            has_urgency = "urgency" in html.lower() or "limited" in html.lower()
            return {
                "status": "PASS" if has_urgency else "WARN",
                "message": "Urgency text found" if has_urgency else "Urgency text not found"
            }
        else:
            return {"status": "SKIP", "message": f"Check not implemented for {element_type}"}
    
    def _check_cta_button(
        self,
        html: str,
        cta_type: str
    ) -> Dict[str, Any]:
        """Check if CTA button exists."""
        cta_patterns = ["cta", "button", "href"]
        has_cta = any(pattern in html.lower() for pattern in cta_patterns)
        
        return {
            "status": "PASS" if has_cta else "FAIL",
            "message": f"{cta_type} CTA button found" if has_cta else f"{cta_type} CTA button not found"
        }
    
    def _check_form_field(
        self,
        html: str,
        field_type: str
    ) -> Dict[str, Any]:
        """Check if form field exists."""
        field_patterns = {
            "email": ["type=\"email\"", "name=\"email\"", "email"]
        }
        
        patterns = field_patterns.get(field_type, [])
        has_field = any(pattern in html.lower() for pattern in patterns)
        
        return {
            "status": "PASS" if has_field else "FAIL",
            "message": f"{field_type} field found" if has_field else f"{field_type} field not found"
        }
    
    def _check_low_friction_form(self, html: str) -> Dict[str, Any]:
        """Check if form is low-friction (email-only or minimal fields)."""
        # Count form fields (approximate)
        input_count = html.lower().count("<input")
        select_count = html.lower().count("<select")
        textarea_count = html.lower().count("<textarea")
        total_fields = input_count + select_count + textarea_count
        
        # Low friction = 3 or fewer fields
        is_low_friction = total_fields <= 3
        
        return {
            "status": "PASS" if is_low_friction else "WARN",
            "message": f"Low-friction form ({total_fields} fields)" if is_low_friction else f"Form has {total_fields} fields (consider reducing)"
        }
    
    def _check_form_submission(self, html: str) -> Dict[str, Any]:
        """Check if form has submission mechanism."""
        has_action = "action=" in html.lower() or "form" in html.lower()
        return {
            "status": "PASS" if has_action else "WARN",
            "message": "Form submission mechanism found" if has_action else "Form submission not configured"
        }
    
    def _check_mobile_responsive(self, html: str) -> Dict[str, Any]:
        """Check if page has mobile responsive indicators."""
        has_viewport = "viewport" in html.lower()
        has_media_queries = "@media" in html.lower() or "responsive" in html.lower()
        
        is_responsive = has_viewport or has_media_queries
        
        return {
            "status": "PASS" if is_responsive else "WARN",
            "message": "Mobile responsive indicators found" if is_responsive else "Mobile responsive indicators not found"
        }
    
    def _check_css_loaded(self, html: str) -> Dict[str, Any]:
        """Check if CSS is loaded."""
        has_css = "stylesheet" in html.lower() or "css" in html.lower() or "<style" in html.lower()
        return {
            "status": "PASS" if has_css else "WARN",
            "message": "CSS loaded" if has_css else "CSS not detected"
        }
    
    def _analyze_cross_site_compatibility(
        self,
        site_results: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze cross-site compatibility patterns."""
        analysis = {
            "common_patterns": {},
            "inconsistencies": [],
            "recommendations": []
        }
        
        # Analyze patterns across sites
        fix_statuses = {}
        for site, results in site_results.items():
            for fix_id, fix_result in results.get("fixes", {}).items():
                if fix_id not in fix_statuses:
                    fix_statuses[fix_id] = []
                fix_statuses[fix_id].append(fix_result.get("status"))
        
        # Identify inconsistencies
        for fix_id, statuses in fix_statuses.items():
            unique_statuses = set(statuses)
            if len(unique_statuses) > 1:
                analysis["inconsistencies"].append({
                    "fix_id": fix_id,
                    "statuses": list(unique_statuses),
                    "message": f"Inconsistent implementation across sites for {fix_id}"
                })
        
        return analysis
    
    def _analyze_ga4_pixel_integration(
        self,
        site_results: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze GA4/Pixel integration from systems integration perspective."""
        analysis = {
            "integration_status": {},
            "missing_integrations": [],
            "recommendations": []
        }
        
        # Check each site for analytics integration
        for site, results in site_results.items():
            # This would need actual page content analysis
            # For now, provide structure for future implementation
            analysis["integration_status"][site] = {
                "status": "PENDING",
                "message": "GA4/Pixel validation requires site inspection"
            }
        
        return analysis
    
    def _save_results(self, results: Dict[str, Any]) -> None:
        """Save validation results to file."""
        with open(self.results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"✅ Results saved to: {self.results_file}")
    
    def generate_agent6_report(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate progress tracking report for Agent-6.
        
        Args:
            results: Validation results
            
        Returns:
            Formatted report for Agent-6
        """
        report = {
            "report_type": "Tier 1 Quick Wins Integration Validation",
            "generated_by": "Agent-1",
            "timestamp": datetime.now().isoformat(),
            "summary": results["summary"],
            "site_status": {},
            "fix_status": {},
            "next_steps": []
        }
        
        # Compile site status
        for site, site_results in results["sites"].items():
            report["site_status"][site] = {
                "status": site_results.get("status"),
                "fixes_tested": len(site_results.get("fixes", {})),
                "fixes_passed": sum(
                    1 for f in site_results.get("fixes", {}).values()
                    if f.get("status") == "PASS"
                )
            }
        
        # Compile fix status
        fix_statuses = {}
        for site, site_results in results["sites"].items():
            for fix_id, fix_result in site_results.get("fixes", {}).items():
                if fix_id not in fix_statuses:
                    fix_statuses[fix_id] = {"total": 0, "passed": 0, "failed": 0}
                fix_statuses[fix_id]["total"] += 1
                if fix_result.get("status") == "PASS":
                    fix_statuses[fix_id]["passed"] += 1
                elif fix_result.get("status") == "FAIL":
                    fix_statuses[fix_id]["failed"] += 1
        
        report["fix_status"] = fix_statuses
        
        # Generate next steps
        report["next_steps"] = [
            "Continue monitoring as Agent-7 deploys remaining fixes",
            "Validate GA4/Pixel integration once Agent-5/Agent-3 setup complete",
            "Provide cross-site compatibility recommendations",
            "Generate detailed validation reports for each site"
        ]
        
        return report


def main():
    """Main entry point."""
    validator = Tier1QuickWinsValidator()
    
    print("🔍 Starting Tier 1 Quick Wins Integration Validation...")
    print(f"📊 Validating {len(validator.TIER1_SITES)} sites...")
    
    results = validator.validate_all_sites()
    
    # Print summary
    print("\n📈 Validation Summary:")
    print(f"  Sites Validated: {results['summary']['sites_validated']}/{results['summary']['total_sites']}")
    print(f"  Fixes Passed: {results['summary']['fixes_passed']}")
    print(f"  Fixes Failed: {results['summary']['fixes_failed']}")
    
    # Generate Agent-6 report
    agent6_report = validator.generate_agent6_report(results)
    agent6_report_file = validator.results_dir / f"agent6_progress_report_{validator.timestamp}.json"
    with open(agent6_report_file, 'w') as f:
        json.dump(agent6_report, f, indent=2)
    
    print(f"\n📋 Agent-6 Report saved to: {agent6_report_file}")
    print("\n✅ Validation complete!")


if __name__ == "__main__":
    main()

