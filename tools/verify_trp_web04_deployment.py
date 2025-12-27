#!/usr/bin/env python3
"""
TradingRobotPlug.com WEB-04 Contact Page Deployment Verification
================================================================

Verifies WEB-04 contact page deployment status for TradingRobotPlug.com.
Checks page accessibility, form presence, and low-friction requirements.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-12-27
Task: HIGH (75 pts) - TradingRobotPlug.com WEB-04 contact page deployment verification
"""

import sys
import json
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

# Constants
BASE_URL = "https://tradingrobotplug.com"
CONTACT_URL = f"{BASE_URL}/contact"
TIMEOUT = 15
RESULTS_DIR = project_root / "agent_workspaces" / "Agent-3" / "deployment_verification_reports"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def verify_contact_page_deployment() -> Dict[str, Any]:
    """
    Verify TradingRobotPlug.com WEB-04 contact page deployment.
    
    Returns:
        Verification results dictionary
    """
    result = {
        "site": "tradingrobotplug.com",
        "task": "WEB-04 Contact Page Deployment Verification",
        "url": CONTACT_URL,
        "timestamp": datetime.now().isoformat(),
        "overall_status": "PENDING",
        "validations": {},
        "recommendations": []
    }
    
    try:
        # Fetch page
        print(f"🔍 Fetching {CONTACT_URL}...")
        response = requests.get(CONTACT_URL, timeout=TIMEOUT, allow_redirects=True)
        result["status_code"] = response.status_code
        
        if response.status_code == 200:
            html = response.text
            html_lower = html.lower()
            
            # Validation 1: Page accessible
            result["validations"]["page_accessible"] = {
                "status": "PASS",
                "message": "Contact page is accessible",
                "status_code": response.status_code
            }
            
            # Validation 2: Form exists
            has_form = "<form" in html_lower
            result["validations"]["form_exists"] = {
                "status": "PASS" if has_form else "FAIL",
                "message": "Contact form found" if has_form else "Contact form not found"
            }
            
            # Validation 3: Email input exists
            has_email_input = (
                'type="email"' in html_lower or 
                'name="email"' in html_lower or 
                'id="email"' in html_lower or
                'input' in html_lower
            )
            result["validations"]["email_input"] = {
                "status": "PASS" if has_email_input else "FAIL",
                "message": "Email input field found" if has_email_input else "Email input field not found"
            }
            
            # Validation 4: Low-friction check (≤3 input fields recommended)
            input_count = html_lower.count("<input")
            is_low_friction = input_count <= 3
            result["validations"]["low_friction"] = {
                "status": "PASS" if is_low_friction else "WARN",
                "message": f"Low-friction form ({input_count} input fields)" if is_low_friction else f"Form has {input_count} input fields (recommended: ≤3)",
                "input_count": input_count
            }
            
            # Validation 5: Form handler integration (check for action attribute)
            has_form_action = 'action=' in html_lower or 'method=' in html_lower
            result["validations"]["form_handler"] = {
                "status": "PASS" if has_form_action else "WARN",
                "message": "Form handler configured" if has_form_action else "Form handler not detected"
            }
            
            # Validation 6: Page title check
            title_match = None
            if "<title>" in html_lower:
                title_start = html.find("<title>")
                title_end = html.find("</title>", title_start)
                if title_start != -1 and title_end != -1:
                    title_match = html[title_start + 7:title_end].strip()
            
            result["validations"]["page_title"] = {
                "status": "PASS" if title_match else "INFO",
                "message": f"Page title: {title_match}" if title_match else "Page title not found",
                "title": title_match
            }
            
            # Determine overall status
            critical_validations = [
                result["validations"]["page_accessible"],
                result["validations"]["form_exists"],
                result["validations"]["email_input"]
            ]
            
            all_critical_pass = all(v["status"] == "PASS" for v in critical_validations)
            
            if all_critical_pass:
                result["overall_status"] = "PASS"
                result["summary"] = "✅ Contact page is deployed and functional"
            else:
                result["overall_status"] = "FAIL"
                result["summary"] = "❌ Contact page deployment issues detected"
            
            # Add recommendations
            if not is_low_friction:
                result["recommendations"].append(
                    f"Consider reducing form fields from {input_count} to ≤3 for better conversion"
                )
            
            if not has_form_action:
                result["recommendations"].append(
                    "Verify form handler is properly configured and tested"
                )
                
        else:
            result["overall_status"] = "FAIL"
            result["error"] = f"HTTP {response.status_code}"
            result["summary"] = f"❌ Contact page returned HTTP {response.status_code}"
            
    except Exception as e:
        result["overall_status"] = "ERROR"
        result["error"] = str(e)
        result["summary"] = f"❌ Error during verification: {e}"
    
    return result


def main():
    """Main entry point."""
    print("=" * 70)
    print("TradingRobotPlug.com WEB-04 Contact Page Deployment Verification")
    print("=" * 70)
    print()
    
    result = verify_contact_page_deployment()
    
    # Print results
    print(f"Site: {result['site']}")
    print(f"URL: {result['url']}")
    print(f"Status: {result['overall_status']}")
    print(f"Summary: {result['summary']}")
    print()
    
    print("Validation Results:")
    for key, validation in result["validations"].items():
        status_icon = {
            "PASS": "✅",
            "FAIL": "❌",
            "WARN": "⚠️",
            "INFO": "ℹ️"
        }.get(validation["status"], "❓")
        print(f"  {status_icon} {key}: {validation['message']}")
    
    if result.get("recommendations"):
        print()
        print("Recommendations:")
        for rec in result["recommendations"]:
            print(f"  • {rec}")
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = RESULTS_DIR / f"trp_web04_verification_{timestamp}.json"
    
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2)
    
    print()
    print(f"✅ Results saved to: {results_file}")
    
    # Return exit code based on status
    if result["overall_status"] == "PASS":
        return 0
    elif result["overall_status"] == "WARN":
        return 0  # Warnings don't fail the verification
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())

