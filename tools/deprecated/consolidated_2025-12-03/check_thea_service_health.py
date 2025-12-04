#!/usr/bin/env python3
"""
Check Thea Service Health
==========================

Validates Thea service implementation and dependencies.

Author: Agent-1
Date: 2025-01-27
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


def check_dependencies():
    """Check all required dependencies."""
    print("🔍 Checking Thea Service Dependencies\n")
    print("=" * 70)
    
    checks = []
    
    # Check Selenium
    try:
        import selenium
        print("✅ Selenium: Available")
        checks.append(("Selenium", True))
    except ImportError:
        print("❌ Selenium: NOT AVAILABLE (pip install selenium)")
        checks.append(("Selenium", False))
    
    # Check undetected-chromedriver
    try:
        import undetected_chromedriver as uc
        print("✅ undetected-chromedriver: Available")
        checks.append(("undetected-chromedriver", True))
    except ImportError:
        print("⚠️ undetected-chromedriver: NOT AVAILABLE (pip install undetected-chromedriver)")
        print("   Will fallback to standard Chrome (may be detected)")
        checks.append(("undetected-chromedriver", False))
    
    # Check PyAutoGUI
    try:
        import pyautogui
        import pyperclip
        print("✅ PyAutoGUI: Available")
        checks.append(("PyAutoGUI", True))
    except ImportError:
        print("❌ PyAutoGUI: NOT AVAILABLE (pip install pyautogui pyperclip)")
        checks.append(("PyAutoGUI", False))
    
    # Check ResponseDetector
    try:
        from response_detector import ResponseDetector
        print("✅ ResponseDetector: Available")
        checks.append(("ResponseDetector", True))
    except ImportError:
        print("⚠️ ResponseDetector: NOT AVAILABLE (optional)")
        checks.append(("ResponseDetector", False))
    
    # Check YAML (for code review parsing)
    try:
        import yaml
        print("✅ YAML: Available")
        checks.append(("YAML", True))
    except ImportError:
        print("⚠️ YAML: NOT AVAILABLE (pip install pyyaml)")
        print("   Code review YAML parsing will use fallback")
        checks.append(("YAML", False))
    
    print("\n" + "=" * 70)
    return checks


def check_thea_service_import():
    """Check if TheaService can be imported."""
    print("\n🔍 Checking TheaService Import\n")
    print("=" * 70)
    
    try:
        from src.services.thea.thea_service import TheaService, create_thea_service
        print("✅ TheaService: Import successful")
        
        # Check if undetected is properly integrated
        import src.services.thea.thea_service as thea_module
        if hasattr(thea_module, 'UNDETECTED_AVAILABLE'):
            status = "✅ Available" if thea_module.UNDETECTED_AVAILABLE else "❌ Not available"
            print(f"   Undetected Chrome: {status}")
        
        return True
    except ImportError as e:
        print(f"❌ TheaService: Import failed - {e}")
        return False
    except Exception as e:
        print(f"❌ TheaService: Error - {e}")
        return False


def check_code_review_tool():
    """Check code review tool."""
    print("\n🔍 Checking Code Review Tool\n")
    print("=" * 70)
    
    try:
        from tools.thea_code_review import (
            generate_code_review_prompt,
            parse_thea_response,
            review_code_with_thea
        )
        print("✅ Code Review Tool: Import successful")
        
        # Test prompt generation
        test_file = Path("src/services/messaging_discord.py")
        if test_file.exists():
            prompt = generate_code_review_prompt(test_file, "Test")
            if len(prompt) > 100:
                print("✅ Prompt Generation: Working")
            else:
                print("⚠️ Prompt Generation: Generated prompt seems short")
        
        return True
    except ImportError as e:
        print(f"❌ Code Review Tool: Import failed - {e}")
        return False
    except Exception as e:
        print(f"❌ Code Review Tool: Error - {e}")
        return False


def main():
    """Run all health checks."""
    print("🏥 THEA SERVICE HEALTH CHECK\n")
    
    deps = check_dependencies()
    service_ok = check_thea_service_import()
    tool_ok = check_code_review_tool()
    
    print("\n" + "=" * 70)
    print("📊 HEALTH SUMMARY")
    print("=" * 70)
    
    critical_deps = [name for name, status in deps if not status and name in ["Selenium", "PyAutoGUI"]]
    optional_deps = [name for name, status in deps if not status and name not in ["Selenium", "PyAutoGUI"]]
    
    if critical_deps:
        print(f"\n❌ Critical dependencies missing: {', '.join(critical_deps)}")
        print("   Thea service will NOT work without these")
    
    if optional_deps:
        print(f"\n⚠️ Optional dependencies missing: {', '.join(optional_deps)}")
        print("   Some features may be limited")
    
    if not critical_deps:
        print("\n✅ All critical dependencies available")
    
    if service_ok and tool_ok:
        print("\n✅ Thea service and code review tool: READY")
        return 0
    else:
        print("\n❌ Some components have issues")
        return 1


if __name__ == "__main__":
    sys.exit(main())

