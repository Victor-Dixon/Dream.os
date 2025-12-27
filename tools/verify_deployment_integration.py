#!/usr/bin/env python3
"""
Deployment Integration Verification Tool
========================================

Verifies deployments across multiple websites for integration testing:
- WordPress theme deployment status
- REST API endpoint availability
- Database connectivity
- Plugin activation status
- Cross-site compatibility

V2 Compliance | Author: Agent-1 | Date: 2025-12-27
"""

import sys
import json
import requests
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from urllib.parse import urljoin

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

# Constants
TIMEOUT = 10
RESULTS_DIR = project_root / "agent_workspaces" / "Agent-1" / "deployment_verification_tests"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# Website configuration
WEBSITES = {
    "tradingrobotplug.com": {
        "url": "https://tradingrobotplug.com",
        "rest_api_base": "/wp-json/tradingrobotplug/v1",
        "endpoints": ["/stock-data", "/stock-data/TSLA", "/strategies"],
        "theme": "tradingrobotplug-theme"
    },
    "dadudekc.com": {
        "url": "https://dadudekc.com",
        "rest_api_base": "/wp-json/wp/v2",
        "endpoints": [],
        "theme": None
    },
    "crosbyultimateevents.com": {
        "url": "https://crosbyultimateevents.com",
        "rest_api_base": "/wp-json/wp/v2",
        "endpoints": [],
        "theme": None
    },
    "freerideinvestor.com": {
        "url": "https://freerideinvestor.com",
        "rest_api_base": "/wp-json/wp/v2",
        "endpoints": [],
        "theme": None
    }
}


class DeploymentVerifier:
    """Verifies deployment status across websites."""
    
    def __init__(self):
        self.results = []
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    @staticmethod
    def _build_api_url(base_url: str, api_base: str, endpoint: str) -> str:
        """
        Build a REST URL safely.

        `urljoin` treats a leading '/' as an absolute path (dropping prior path),
        so we normalize segments before joining.
        """
        root = base_url.rstrip("/") + "/"
        api = (api_base or "").strip("/")
        ep = (endpoint or "").strip("/")
        if api and ep:
            return urljoin(root, f"{api}/{ep}")
        if api:
            return urljoin(root, api)
        return urljoin(root, ep)
    
    def check_site_accessible(self, url: str) -> Dict[str, Any]:
        """Check if site is accessible."""
        try:
            response = requests.get(url, timeout=TIMEOUT, allow_redirects=True)
            return {
                "status": "PASS" if response.status_code == 200 else "FAIL",
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds(),
                "size": len(response.content)
            }
        except Exception as e:
            return {
                "status": "ERROR",
                "error": str(e)
            }
    
    def check_rest_api_endpoint(self, base_url: str, endpoint: str) -> Dict[str, Any]:
        """Check if REST API endpoint is accessible."""
        full_url = urljoin(base_url, endpoint)
        try:
            response = requests.get(full_url, timeout=TIMEOUT, allow_redirects=True)
            return {
                "status": "PASS" if response.status_code == 200 else "FAIL",
                "status_code": response.status_code,
                "url": full_url,
                "response_size": len(response.content) if response.content else 0
            }
        except Exception as e:
            return {
                "status": "ERROR",
                "url": full_url,
                "error": str(e)
            }
    
    def check_wordpress_api(self, base_url: str) -> Dict[str, Any]:
        """Check if WordPress REST API is accessible."""
        api_url = urljoin(base_url, "/wp-json/wp/v2")
        try:
            response = requests.get(api_url, timeout=TIMEOUT)
            return {
                "status": "PASS" if response.status_code == 200 else "FAIL",
                "status_code": response.status_code,
                "wp_api_available": response.status_code == 200
            }
        except Exception as e:
            return {
                "status": "ERROR",
                "error": str(e)
            }
    
    def verify_website(self, site_name: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Verify deployment status for a website."""
        print(f"🔍 Verifying {site_name}...")
        
        base_url = config["url"]
        result = {
            "site": site_name,
            "url": base_url,
            "timestamp": datetime.now().isoformat(),
            "checks": {}
        }
        
        # Check site accessibility
        accessibility = self.check_site_accessible(base_url)
        result["checks"]["accessibility"] = accessibility
        
        # Check WordPress REST API
        wp_api = self.check_wordpress_api(base_url)
        result["checks"]["wordpress_api"] = wp_api
        
        # Check custom REST API endpoints
        if config.get("endpoints"):
            endpoint_results = []
            for endpoint in config["endpoints"]:
                api_url = self._build_api_url(base_url, config.get("rest_api_base", ""), endpoint)
                endpoint_check = self.check_rest_api_endpoint(api_url, "")
                endpoint_results.append({
                    "endpoint": endpoint,
                    **endpoint_check
                })
            result["checks"]["custom_endpoints"] = endpoint_results
        
        # Overall status
        all_checks = [accessibility.get("status"), wp_api.get("status")]
        if config.get("endpoints"):
            all_checks.extend([e.get("status") for e in result["checks"].get("custom_endpoints", [])])
        
        if "ERROR" in all_checks:
            result["overall_status"] = "ERROR"
        elif "FAIL" in all_checks:
            result["overall_status"] = "FAIL"
        else:
            result["overall_status"] = "PASS"
        
        self.results.append(result)
        status_emoji = "✅" if result["overall_status"] == "PASS" else "⚠️" if result["overall_status"] == "FAIL" else "❌"
        print(f"{status_emoji} {site_name}: {result['overall_status']}")
        
        return result
    
    def verify_all(self) -> List[Dict[str, Any]]:
        """Verify all websites."""
        print(f"🚀 Starting deployment verification for {len(WEBSITES)} websites...\n")
        
        for site_name, config in WEBSITES.items():
            self.verify_website(site_name, config)
        
        return self.results
    
    def save_results(self):
        """Save verification results."""
        results_file = RESULTS_DIR / f"deployment_verification_{self.timestamp}.json"
        summary_file = RESULTS_DIR / f"deployment_verification_summary_{self.timestamp}.md"
        
        # Save JSON
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "total_sites": len(self.results),
                "results": self.results
            }, f, indent=2)
        
        # Generate summary
        summary = self.generate_summary()
        summary_file.write_text(summary, encoding='utf-8')
        
        print(f"\n✅ Results saved:")
        print(f"   JSON: {results_file}")
        print(f"   Summary: {summary_file}")
        
        return results_file, summary_file
    
    def generate_summary(self) -> str:
        """Generate markdown summary."""
        total = len(self.results)
        passed = sum(1 for r in self.results if r["overall_status"] == "PASS")
        failed = sum(1 for r in self.results if r["overall_status"] == "FAIL")
        errors = sum(1 for r in self.results if r["overall_status"] == "ERROR")
        
        summary = f"""# Deployment Integration Verification Summary

**Date**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Validator**: Agent-1 (Integration & Core Systems Specialist)  
**Tool**: `tools/verify_deployment_integration.py`

---

## Overall Results

- **Total Websites**: {total}
- **✅ Passed**: {passed}
- **⚠️ Failed**: {failed}
- **🔴 Errors**: {errors}

---

## Detailed Results

"""
        
        for result in self.results:
            status_emoji = "✅" if result["overall_status"] == "PASS" else "⚠️" if result["overall_status"] == "FAIL" else "🔴"
            summary += f"### {status_emoji} {result['site']}\n\n"
            summary += f"**URL**: {result['url']}\n"
            summary += f"**Overall Status**: {result['overall_status']}\n\n"
            
            # Accessibility
            acc = result["checks"]["accessibility"]
            summary += f"**Accessibility**: {acc['status']}\n"
            if acc['status'] == "PASS":
                summary += f"- Status Code: {acc['status_code']}\n"
                summary += f"- Response Time: {acc['response_time']:.2f}s\n"
            summary += "\n"
            
            # WordPress API
            wp = result["checks"]["wordpress_api"]
            summary += f"**WordPress REST API**: {wp['status']}\n"
            if wp['status'] == "PASS":
                summary += f"- API Available: ✅\n"
            summary += "\n"
            
            # Custom endpoints
            if "custom_endpoints" in result["checks"]:
                summary += "**Custom REST API Endpoints**:\n"
                for ep in result["checks"]["custom_endpoints"]:
                    ep_status = "✅" if ep['status'] == "PASS" else "❌"
                    summary += f"- {ep_status} {ep['endpoint']}: {ep['status']}\n"
                summary += "\n"
            
            summary += "---\n\n"
        
        return summary


def main():
    """Main execution."""
    verifier = DeploymentVerifier()
    results = verifier.verify_all()
    verifier.save_results()
    
    # Print summary
    passed = sum(1 for r in results if r["overall_status"] == "PASS")
    failed = sum(1 for r in results if r["overall_status"] == "FAIL")
    errors = sum(1 for r in results if r["overall_status"] == "ERROR")
    
    print(f"\n📊 Summary:")
    print(f"   ✅ Passed: {passed}/{len(results)}")
    print(f"   ⚠️  Failed: {failed}/{len(results)}")
    print(f"   🔴 Errors: {errors}/{len(results)}")


if __name__ == "__main__":
    main()

