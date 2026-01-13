#!/usr/bin/env python3
"""Import validation tests to prevent future dead code"""

def test_critical_imports():
    """Test all critical modules import successfully"""
    try:
        import src.ai_automation
        import src.automation
        import src.core
        print("✅ All critical imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import failure: {e}")
        return False

if __name__ == "__main__":
    test_critical_imports()