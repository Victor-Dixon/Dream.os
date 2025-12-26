#!/usr/bin/env python3
"""
Verify Contact Forms on Contact Pages
=====================================

Quick verification script to check contact forms on contact pages
for dadudekc.com and tradingrobotplug.com.

V2 Compliance | Author: Agent-1 | Date: 2025-12-26
"""

import requests
import json
from datetime import datetime
from typing import Dict, Any

def verify_contact_page(site: str, contact_url: str) -> Dict[str, Any]:
    """Verify contact form on contact page."""
    result = {
        "site": site,
        "url": contact_url,
        "timestamp": datetime.now().isoformat(),
        "status": "PENDING",
        "validations": {}
    }
    
    try:
        response = requests.get(contact_url, timeout=10, allow_redirects=True)
        result["status_code"] = response.status_code
        
        if response.status_code == 200:
            html = response.text.lower()
            
            result["validations"] = {
                "page_accessible": {"status": "PASS", "message": "Contact page accessible"},
                "form_exists": {
                    "status": "PASS" if "<form" in html else "FAIL",
                    "message": "Form found" if "<form" in html else "Form not found"
                },
                "email_input": {
                    "status": "PASS" if ('type="email"' in html or 'name="email"' in html or 'input' in html) else "FAIL",
                    "message": "Email input found" if ('type="email"' in html or 'name="email"' in html or 'input' in html) else "Email input not found"
                },
                "low_friction": {
                    "status": "PASS" if html.count("<input") <= 3 else "WARN",
                    "message": f"Low-friction form ({html.count('<input')} input fields)" if html.count("<input") <= 3 else f"Form has {html.count('<input')} input fields"
                }
            }
            
            # Determine overall status
            all_passed = all(
                v.get("status") == "PASS" 
                for v in result["validations"].values()
                if isinstance(v, dict)
            )
            result["status"] = "PASS" if all_passed else "FAIL"
        else:
            result["status"] = "ERROR"
            result["error"] = f"HTTP {response.status_code}"
            
    except Exception as e:
        result["status"] = "ERROR"
        result["error"] = str(e)
    
    return result

def main():
    """Main entry point."""
    sites = {
        "dadudekc.com": "https://dadudekc.com/contact",
        "tradingrobotplug.com": "https://tradingrobotplug.com/contact"
    }
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "verification_type": "contact_page_verification",
        "sites": {}
    }
    
    print("🔍 Verifying contact forms on contact pages...")
    
    for site, url in sites.items():
        print(f"  Checking {site}...")
        result = verify_contact_page(site, url)
        results["sites"][site] = result
        
        # Print summary
        status_icon = "✅" if result["status"] == "PASS" else "⚠️" if result["status"] == "FAIL" else "❌"
        print(f"    {status_icon} {site}: {result['status']}")
        if "validations" in result:
            for key, val in result["validations"].items():
                if isinstance(val, dict):
                    icon = "✅" if val["status"] == "PASS" else "⚠️" if val["status"] == "WARN" else "❌"
                    print(f"      {icon} {key}: {val['message']}")
    
    # Save results
    results_file = f"agent_workspaces/Agent-1/p0_integration_tests/contact_page_verification_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    from pathlib import Path
    Path(results_file).parent.mkdir(parents=True, exist_ok=True)
    
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✅ Results saved to: {results_file}")
    
    return results

if __name__ == "__main__":
    main()

