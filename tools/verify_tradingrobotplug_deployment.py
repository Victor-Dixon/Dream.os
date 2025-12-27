#!/usr/bin/env python3
"""
TradingRobotPlug.com Theme Deployment Verification Tool
======================================================

Verifies theme deployment status and runs integration tests.

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-12-26
"""

import sys
import json
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from urllib.parse import urljoin, urlparse

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

# Constants
BASE_URL = "https://tradingrobotplug.com"
TIMEOUT = 10
RESULTS_DIR = project_root / "agent_workspaces" / "Agent-1" / "tradingrobotplug_deployment_tests"


def check_url_exists(url: str) -> bool:
    """Check if URL exists and returns 200."""
    try:
        response = requests.get(url, timeout=TIMEOUT, allow_redirects=True)
        return response.status_code == 200
    except Exception:
        return False


def fetch_page_content(url: str) -> Optional[str]:
    """Fetch page content."""
    try:
        response = requests.get(url, timeout=TIMEOUT, allow_redirects=True)
        if response.status_code == 200:
            return response.text
        return None
    except Exception as e:
        print(f"⚠️  Error fetching {url}: {e}")
        return None


def check_element_in_content(content: str, patterns: List[str], element_name: str) -> Dict[str, Any]:
    """Check if element patterns exist in content."""
    found = []
    missing = []
    
    for pattern in patterns:
        if pattern.lower() in content.lower():
            found.append(pattern)
        else:
            missing.append(pattern)
    
    return {
        "element": element_name,
        "found": len(found),
        "total": len(patterns),
        "found_patterns": found,
        "missing_patterns": missing,
        "status": "PASS" if len(found) == len(patterns) else "FAIL" if len(found) == 0 else "PARTIAL"
    }


def verify_hero_section(content: str) -> Dict[str, Any]:
    """Verify hero section is present."""
    patterns = [
        "hero",
        "trading robot",
        "automated trading",
        "cta",
        "get started",
        "sign up",
        "waitlist"
    ]
    
    result = check_element_in_content(content, patterns, "Hero Section")
    
    # Additional checks
    has_hero_class = "hero" in content.lower() or "hero-section" in content.lower()
    has_cta_button = any(cta in content.lower() for cta in ["button", "btn", "cta", "get started", "sign up"])
    
    result["details"] = {
        "has_hero_class": has_hero_class,
        "has_cta_button": has_cta_button,
        "urgency_text": "Limited Time" in content or "Join Now" in content or "Early Access" in content
    }
    
    return result


def verify_waitlist_form(content: str) -> Dict[str, Any]:
    """Verify waitlist form is present."""
    patterns = [
        "form",
        "email",
        "waitlist",
        "submit",
        "input"
    ]
    
    result = check_element_in_content(content, patterns, "Waitlist Form")
    
    # Additional checks
    has_form_tag = "<form" in content.lower()
    has_email_input = 'type="email"' in content.lower() or 'name="email"' in content.lower()
    has_submit_button = 'type="submit"' in content.lower() or 'button' in content.lower()
    
    result["details"] = {
        "has_form_tag": has_form_tag,
        "has_email_input": has_email_input,
        "has_submit_button": has_submit_button
    }
    
    return result


def verify_contact_form(content: str) -> Dict[str, Any]:
    """Verify contact form is present."""
    patterns = [
        "contact",
        "form",
        "name",
        "email",
        "message"
    ]
    
    result = check_element_in_content(content, patterns, "Contact Form")
    
    # Additional checks
    has_form_tag = "<form" in content.lower()
    has_contact_fields = all(field in content.lower() for field in ["name", "email"])
    
    result["details"] = {
        "has_form_tag": has_form_tag,
        "has_contact_fields": has_contact_fields
    }
    
    return result


def verify_rest_api_endpoints() -> Dict[str, Any]:
    """Verify REST API endpoints are accessible."""
    endpoints = [
        "/wp-json/tradingrobotplug/v1/waitlist",
        "/wp-json/tradingrobotplug/v1/contact",
        "/wp-json/tradingrobotplug/v1/dashboard",
        "/wp-json/tradingrobotplug/v1/performance",
        "/wp-json/tradingrobotplug/v1/strategies",
        "/wp-json/tradingrobotplug/v1/trades"
    ]
    
    results = []
    accessible = 0
    
    for endpoint in endpoints:
        url = urljoin(BASE_URL, endpoint)
        exists = check_url_exists(url)
        results.append({
            "endpoint": endpoint,
            "url": url,
            "accessible": exists,
            "status": "PASS" if exists else "FAIL"
        })
        if exists:
            accessible += 1
    
    return {
        "element": "REST API Endpoints",
        "accessible": accessible,
        "total": len(endpoints),
        "endpoints": results,
        "status": "PASS" if accessible == len(endpoints) else "FAIL" if accessible == 0 else "PARTIAL"
    }


def verify_dark_theme(content: str) -> Dict[str, Any]:
    """Verify dark theme CSS is applied."""
    patterns = [
        "dark",
        "background",
        "color",
        "css",
        "theme"
    ]
    
    result = check_element_in_content(content, patterns, "Dark Theme")
    
    # Check for CSS variables or dark theme classes
    has_dark_vars = "--dark" in content or "dark-theme" in content.lower() or "dark-mode" in content.lower()
    has_css_vars = "--" in content and "color" in content.lower()
    
    result["details"] = {
        "has_dark_vars": has_dark_vars,
        "has_css_vars": has_css_vars
    }
    
    return result


def check_console_errors(content: str) -> Dict[str, Any]:
    """Check for JavaScript errors in content."""
    # Look for actual runtime error patterns, not console.error() calls in code
    # Exclude JavaScript code comments and function definitions
    error_patterns = [
        ("<script[^>]*>.*?error[^<]*</script>", "script_error"),
        ("onerror=", "onerror_handler"),
        ("throw new Error", "thrown_error"),
        ("ReferenceError", "reference_error"),
        ("TypeError", "type_error"),
        ("SyntaxError", "syntax_error"),
    ]
    
    # Also check for common runtime error indicators in HTML comments or visible text
    html_error_indicators = [
        "Fatal error",
        "Parse error",
        "Warning:",
        "Notice:",
    ]
    
    errors_found = []
    import re
    
    # Check for error patterns in script tags (actual runtime errors)
    for pattern, error_type in error_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
        if matches:
            errors_found.append({
                "pattern": error_type,
                "count": len(matches)
            })
    
    # Check for HTML error indicators (PHP errors, etc.)
    for indicator in html_error_indicators:
        if indicator in content:
            count = content.count(indicator)
            errors_found.append({
                "pattern": indicator,
                "count": count
            })
    
    # Note: console.error() calls in JavaScript code are expected for error handling
    # and should not be flagged as errors
    
    return {
        "element": "Console Errors",
        "errors_found": len(errors_found),
        "error_details": errors_found,
        "status": "PASS" if len(errors_found) == 0 else "WARN"
    }


def verify_mobile_responsive(content: str) -> Dict[str, Any]:
    """Verify mobile responsive design."""
    patterns = [
        "viewport",
        "responsive",
        "mobile",
        "media query",
        "@media"
    ]
    
    result = check_element_in_content(content, patterns, "Mobile Responsive")
    
    # Check for viewport meta tag
    has_viewport = 'name="viewport"' in content.lower()
    has_media_queries = "@media" in content
    
    result["details"] = {
        "has_viewport": has_viewport,
        "has_media_queries": has_media_queries
    }
    
    return result


def run_integration_tests() -> Dict[str, Any]:
    """Run comprehensive integration tests."""
    print(f"🔍 Verifying TradingRobotPlug.com deployment...")
    print(f"   Base URL: {BASE_URL}\n")
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "base_url": BASE_URL,
        "tests": {}
    }
    
    # Fetch homepage
    print("📄 Fetching homepage...")
    homepage_content = fetch_page_content(BASE_URL)
    
    if not homepage_content:
        return {
            **results,
            "error": "Failed to fetch homepage",
            "status": "FAIL"
        }
    
    print("✅ Homepage fetched\n")
    
    # Run tests
    print("🧪 Running integration tests...\n")
    
    # 1. Hero Section
    print("   Testing hero section...")
    results["tests"]["hero_section"] = verify_hero_section(homepage_content)
    print(f"      Status: {results['tests']['hero_section']['status']}")
    
    # 2. Waitlist Form
    print("   Testing waitlist form...")
    results["tests"]["waitlist_form"] = verify_waitlist_form(homepage_content)
    print(f"      Status: {results['tests']['waitlist_form']['status']}")
    
    # 3. Dark Theme
    print("   Testing dark theme...")
    results["tests"]["dark_theme"] = verify_dark_theme(homepage_content)
    print(f"      Status: {results['tests']['dark_theme']['status']}")
    
    # 4. Mobile Responsive
    print("   Testing mobile responsive...")
    results["tests"]["mobile_responsive"] = verify_mobile_responsive(homepage_content)
    print(f"      Status: {results['tests']['mobile_responsive']['status']}")
    
    # 5. Console Errors
    print("   Checking console errors...")
    results["tests"]["console_errors"] = check_console_errors(homepage_content)
    print(f"      Status: {results['tests']['console_errors']['status']}")
    
    # 6. REST API Endpoints
    print("   Testing REST API endpoints...")
    results["tests"]["rest_api"] = verify_rest_api_endpoints()
    print(f"      Status: {results['tests']['rest_api']['status']} ({results['tests']['rest_api']['accessible']}/{results['tests']['rest_api']['total']} accessible)")
    
    # 7. Contact Form (check contact page)
    print("   Testing contact form...")
    contact_url = urljoin(BASE_URL, "/contact")
    contact_content = fetch_page_content(contact_url)
    if contact_content:
        results["tests"]["contact_form"] = verify_contact_form(contact_content)
        print(f"      Status: {results['tests']['contact_form']['status']}")
    else:
        results["tests"]["contact_form"] = {
            "element": "Contact Form",
            "status": "FAIL",
            "error": "Contact page not accessible"
        }
        print(f"      Status: FAIL (contact page not accessible)")
    
    print()
    
    # Calculate overall status
    test_statuses = [test.get("status", "UNKNOWN") for test in results["tests"].values()]
    pass_count = test_statuses.count("PASS")
    fail_count = test_statuses.count("FAIL")
    partial_count = test_statuses.count("PARTIAL")
    warn_count = test_statuses.count("WARN")
    
    results["summary"] = {
        "total_tests": len(results["tests"]),
        "passed": pass_count,
        "failed": fail_count,
        "partial": partial_count,
        "warnings": warn_count,
        "overall_status": "PASS" if fail_count == 0 and partial_count == 0 else "PARTIAL" if fail_count == 0 else "FAIL"
    }
    
    return results


def save_results(results: Dict[str, Any]) -> Path:
    """Save test results to file."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"tradingrobotplug_deployment_verification_{timestamp}.json"
    filepath = RESULTS_DIR / filename
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    return filepath


def print_summary(results: Dict[str, Any]):
    """Print test summary."""
    summary = results.get("summary", {})
    
    print("=" * 60)
    print("📊 DEPLOYMENT VERIFICATION SUMMARY")
    print("=" * 60)
    print(f"Overall Status: {summary.get('overall_status', 'UNKNOWN')}")
    print(f"Tests Passed: {summary.get('passed', 0)}/{summary.get('total_tests', 0)}")
    print(f"Tests Failed: {summary.get('failed', 0)}")
    print(f"Tests Partial: {summary.get('partial', 0)}")
    print(f"Warnings: {summary.get('warnings', 0)}")
    print("=" * 60)
    print()
    
    print("📋 DETAILED RESULTS:")
    for test_name, test_result in results.get("tests", {}).items():
        status = test_result.get("status", "UNKNOWN")
        element = test_result.get("element", test_name)
        print(f"   {element}: {status}")
        if status != "PASS":
            if "missing_patterns" in test_result:
                print(f"      Missing: {', '.join(test_result['missing_patterns'][:3])}")
            if "error" in test_result:
                print(f"      Error: {test_result['error']}")
    print()


def main():
    """Main entry point."""
    print("🚀 TradingRobotPlug.com Theme Deployment Verification")
    print("=" * 60)
    print()
    
    # Run integration tests
    results = run_integration_tests()
    
    # Save results
    results_file = save_results(results)
    print(f"💾 Results saved to: {results_file}\n")
    
    # Print summary
    print_summary(results)
    
    # Exit with appropriate code
    summary = results.get("summary", {})
    if summary.get("overall_status") == "PASS":
        print("✅ Deployment verification PASSED")
        sys.exit(0)
    elif summary.get("overall_status") == "PARTIAL":
        print("⚠️  Deployment verification PARTIAL - Some issues found")
        sys.exit(1)
    else:
        print("❌ Deployment verification FAILED")
        sys.exit(1)


if __name__ == "__main__":
    main()

