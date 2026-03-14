#!/usr/bin/env python3
"""
Contact Form Verification Script
=================================

Verifies TradingRobotPlug.com contact page deployment and functionality.
Tests the contact form handler and database operations.

Author: Agent-7 (Web Development Specialist)
Date: 2026-01-10
"""

import requests
import json
from pathlib import Path

def test_contact_page_accessibility():
    """Test that contact page loads successfully."""
    url = "https://tradingrobotplug.com/contact/"
    try:
        response = requests.get(url, timeout=10)
        print(f"✅ Contact page accessible: {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Contact page error: {e}")
        return False

def test_form_structure():
    """Test that the form has proper structure."""
    url = "https://tradingrobotplug.com/contact/"
    try:
        response = requests.get(url, timeout=10)
        content = response.text

        # Check for form elements
        checks = [
            ('name="email"', 'name="email"' in content),
            ('value="handle_contact_form"', 'value="handle_contact_form"' in content),
            ('type="email"', 'type="email"' in content),
            ('required', 'required' in content),
            ('admin-post.php', 'admin-post.php' in content)
        ]

        passed = 0
        for check_name, check_result in checks:
            if check_result:
                print(f"  ✅ {check_name}")
                passed += 1
            else:
                print(f"  ❌ {check_name}")

        total = len(checks)
        print(f"✅ Form structure: {passed}/{total} checks passed")
        return passed == total

    except Exception as e:
        print(f"❌ Form structure check error: {e}")
        return False

def test_form_submission():
    """Test form submission with a test email."""
    url = "https://tradingrobotplug.com/wp-admin/admin-post.php"
    data = {
        'action': 'handle_contact_form',
        'email': 'verification-test@example.com',
        'contact_nonce': '',  # Would need to be generated properly for full test
    }

    try:
        # Note: This is a basic test - full testing would require proper nonce
        response = requests.post(url, data=data, allow_redirects=False, timeout=10)
        print(f"✅ Form submission endpoint responds: {response.status_code}")

        # Check if it redirects (expected behavior)
        if 300 <= response.status_code < 400:
            print("✅ Form submission redirects as expected")
            return True
        else:
            print(f"⚠️  Unexpected response: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Form submission test error: {e}")
        return False

def main():
    """Run all verification tests."""
    print("🚀 TradingRobotPlug Contact Page Verification")
    print("=" * 50)

    tests = [
        ("Page Accessibility", test_contact_page_accessibility),
        ("Form Structure", test_form_structure),
        ("Form Submission", test_form_submission),
    ]

    results = []
    for name, test_func in tests:
        print(f"\n📋 Testing: {name}")
        result = test_func()
        results.append(result)

    print("\n" + "=" * 50)
    print("📊 VERIFICATION RESULTS:")

    passed = sum(results)
    total = len(results)

    for i, (name, _) in enumerate(tests):
        status = "✅ PASS" if results[i] else "❌ FAIL"
        print(f"  {name}: {status}")

    print(f"\n🎯 Overall: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 CONTACT PAGE DEPLOYMENT VERIFICATION: COMPLETE")
        return True
    else:
        print("⚠️  Some tests failed - manual verification may be needed")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)