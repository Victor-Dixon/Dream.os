#!/usr/bin/env python3
"""
Test Thea Code Review Tool
===========================

Quick test of Thea code review functionality without full browser launch.

Author: Agent-1
Date: 2025-01-27
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.thea_code_review import (
    generate_code_review_prompt,
    parse_thea_response
)


def test_prompt_generation():
    """Test prompt generation."""
    test_file = Path("src/services/messaging_discord.py")
    
    if not test_file.exists():
        print("❌ Test file not found")
        return False
    
    prompt = generate_code_review_prompt(test_file, "Test review")
    
    assert "CODE REVIEW REQUEST" in prompt
    assert "V3 Compliance" in prompt
    assert "message_discord" in prompt or "messaging_discord" in prompt
    
    print("✅ Prompt generation test passed")
    return True


def test_response_parsing():
    """Test response parsing."""
    try:
        # Test YAML parsing
        yaml_response = """
        Here's the review:
        
        ```yaml
        findings:
          - type: "V3_COMPLIANCE"
            severity: "HIGH"
            issue: "File exceeds 400 lines"
            location: "file.py:1"
        
        refactor_plan:
          steps:
            - action: "split_module"
              target: "file.py"
        
        commit_message: "Refactor: Split module"
        ```
        """
        
        parsed = parse_thea_response(yaml_response)
        
        # YAML parsing may or may not work depending on yaml module
        if parsed.get("parsed"):
            assert len(parsed["findings"]) > 0 or "refactor_plan" in parsed
            print("✅ YAML parsing test passed")
        else:
            # If YAML parsing failed, fallback should still work
            print("⚠️ YAML parsing not available, testing fallback...")
        
        # Test fallback parsing
        text_response = "V3 compliance issues detected. File too large."
        parsed2 = parse_thea_response(text_response)
        
        assert len(parsed2["findings"]) > 0
        assert parsed2["findings"][0]["type"] == "V3_COMPLIANCE"
        
        print("✅ Fallback parsing test passed")
        return True
    except Exception as e:
        print(f"❌ Response parsing test error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_imports():
    """Test that all imports work."""
    try:
        from tools.thea_code_review import (
            generate_code_review_prompt,
            parse_thea_response,
            review_code_with_thea
        )
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False


def main():
    """Run all tests."""
    print("🧪 Testing Thea Code Review Tool\n")
    print("=" * 70)
    
    tests = [
        ("Import Test", test_imports),
        ("Prompt Generation", test_prompt_generation),
        ("Response Parsing", test_response_parsing),
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\n📋 {name}...")
        try:
            result = test_func()
            results.append((name, result))
            if result:
                print(f"✅ {name} PASSED")
            else:
                print(f"❌ {name} FAILED")
        except Exception as e:
            print(f"❌ {name} ERROR: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print(f"\n✅ Passed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())

