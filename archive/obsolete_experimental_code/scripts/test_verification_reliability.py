#!/usr/bin/env python3
"""
Test verification service reliability - check if it detects "existence vs functionality" issues
"""

import sys
import os
import tempfile
import json
from pathlib import Path

# Add the src path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.services.verification_service import VerificationService

def test_file_verification_reliability():
    """Test if file verification checks more than just existence."""

    print("🧪 TESTING FILE VERIFICATION RELIABILITY")

    vs = VerificationService()

    # Test 1: File exists but is not readable (permission denied)
    print("\n1️⃣ Testing file existence vs readability...")

    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write("test content")
        temp_path = f.name

    try:
        # Remove read permission (if possible on this OS)
        try:
            os.chmod(temp_path, 0o000)
        except:
            print("   ⚠️ Cannot modify permissions on this OS, skipping permission test")
            readable_test = True
        else:
            readable_test = os.access(temp_path, os.R_OK)

        # Test OLD verification (just existence)
        old_result = vs.verify_file_exists(temp_path)
        print(f"   OLD: File exists: {old_result['success']}")

        # Test NEW verification (functional)
        new_result = vs.verify_file_functional(temp_path)
        print(f"   NEW: Functional check: {new_result['success']}")
        print(f"   NEW: Exists: {new_result['exists']}, Readable: {new_result['readable']}")

        # Check if file is actually readable
        try:
            with open(temp_path, 'r') as f:
                content = f.read()
            actually_readable = True
        except:
            actually_readable = False

        print(f"   Actually readable: {actually_readable}")

        if old_result['success'] and not actually_readable:
            print("   ❌ OLD METHOD FLAW: Claims file exists but it's not readable!")
        elif new_result['success'] or (new_result['exists'] and actually_readable):
            print("   ✅ NEW METHOD WORKS: Properly detects functionality")
        else:
            print("   ⚠️ Edge case - file permissions issue")

    finally:
        try:
            os.unlink(temp_path)
        except:
            pass

    # Test 2: File exists but contains invalid content
    print("\n2️⃣ Testing file content validity...")

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write("invalid json content {{{")
        json_path = f.name

    try:
        # Test OLD verification
        old_result = vs.verify_file_exists(json_path)
        print(f"   OLD: File exists: {old_result['success']}")

        # Test NEW verification with smart validation
        new_result = vs.verify_file_smart(json_path)  # Auto-detects .json and validates
        print(f"   NEW: Smart validation: {new_result['success']}")
        print(f"   NEW: Exists: {new_result['exists']}, Readable: {new_result['readable']}, Valid JSON: {new_result['content_valid']}")

        # Check if content is actually valid JSON
        try:
            with open(json_path, 'r') as f:
                json.load(f)
            valid_json = True
        except:
            valid_json = False

        print(f"   Actually valid JSON: {valid_json}")

        if old_result['success'] and not valid_json:
            print("   ❌ OLD METHOD FLAW: File exists but contains invalid JSON!")
        elif new_result['success'] == valid_json:
            print("   ✅ NEW METHOD WORKS: Properly validates content!")
        else:
            print("   ⚠️ Validation logic issue")

    finally:
        try:
            os.unlink(json_path)
        except:
            pass

    # Test 3: Valid JSON file
    print("\n3️⃣ Testing valid JSON file...")

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump({"test": "data", "number": 42}, f)
        valid_json_path = f.name

    try:
        old_result = vs.verify_file_exists(valid_json_path)
        new_result = vs.verify_file_smart(valid_json_path)

        print(f"   OLD: File exists: {old_result['success']}")
        print(f"   NEW: Smart validation: {new_result['success']}")
        print(f"   NEW: Valid JSON: {new_result['content_valid']}")

        if new_result['success'] and new_result['content_valid']:
            print("   ✅ NEW METHOD WORKS: Correctly validates valid JSON!")
        else:
            print("   ❌ NEW METHOD FAILED: Should accept valid JSON")
            return False

    finally:
        try:
            os.unlink(valid_json_path)
        except:
            pass

    return True

def test_url_verification_reliability():
    """Test if URL verification checks more than just HTTP status."""

    print("\n🌐 TESTING URL VERIFICATION RELIABILITY")

    vs = VerificationService()

    # Test 1: URL that returns 200 but minimal content
    print("\n3️⃣ Testing URL status vs content functionality...")

    # Use httpbin.org/status/200 which returns 200 but minimal content
    test_url = "https://httpbin.org/status/200"

    # Test OLD verification
    old_result = vs.verify_url_status(test_url)
    print(f"   OLD: HTTP status check: {old_result['success']} (status: {old_result.get('status_code', 'unknown')})")

    # Test NEW verification
    new_result = vs.verify_url_functional(test_url)
    print(f"   NEW: Functional check: {new_result['success']}")
    print(f"   NEW: Status: {new_result.get('status_code')}, Content length: {new_result.get('content_length', 0)}")
    print(f"   NEW: Has meaningful content: {new_result.get('has_meaningful_content', False)}")

    # Check what the actual content looks like
    try:
        import requests
        response = requests.get(test_url, timeout=10)
        content_length = len(response.text)
        has_content = content_length > 0
        meaningful_content = content_length >= 100  # Our default threshold
        print(f"   Actual content length: {content_length}")
        print(f"   Has meaningful content (>=100 chars): {meaningful_content}")
    except Exception as e:
        print(f"   Content fetch error: {e}")
        meaningful_content = False

    if old_result['success'] and not meaningful_content:
        print("   ❌ OLD METHOD FLAW: URL returns 200 but content too minimal!")
    elif new_result['success'] == meaningful_content:
        print("   ✅ NEW METHOD WORKS: Properly validates content!")
    else:
        print("   ⚠️ Content validation logic issue")
        return False

    # Test 2: Working URL with actual content
    print("\n4️⃣ Testing functional URL...")

    working_url = "https://httpbin.org/json"
    old_result2 = vs.verify_url_status(working_url)
    new_result2 = vs.verify_url_functional(working_url)

    print(f"   OLD: HTTP status check: {old_result2['success']}")
    print(f"   NEW: Functional check: {new_result2['success']}")
    print(f"   NEW: Content length: {new_result2.get('content_length', 0)}")

    if new_result2['success']:
        print("   ✅ NEW METHOD WORKS: Accepts URLs with proper content!")
    else:
        print("   ❌ NEW METHOD FAILED: Should accept working URLs")
        return False

    return True

if __name__ == "__main__":
    print("🔍 VERIFICATION SERVICE RELIABILITY AUDIT")
    print("=" * 50)

    file_test = test_file_verification_reliability()
    url_test = test_url_verification_reliability()

    print("\n" + "=" * 50)
    print("📊 AUDIT RESULTS:")

    if not file_test or not url_test:
        print("❌ FLAWS DETECTED: Verification service has 'existence vs functionality' issues!")
        print("   Similar to Thea login detection - claims success but doesn't verify actual functionality")
        print("   🚀 OPPORTUNITY: Apply same testing methodology we used for Thea authentication")
    else:
        print("✅ VERIFICATION SERVICE WORKS CORRECTLY")
        print("   No 'existence vs functionality' issues detected")

    print("=" * 50)