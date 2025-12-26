#!/usr/bin/env python3
"""
TradingRobotPlug.com Template Loading Verification Tool
========================================================

Verifies WordPress template hierarchy and template loading for front-page.php.
Checks for template_include filter conflicts and theme activation issues.

V2 Compliance | Author: Agent-3 | Date: 2025-12-25
"""

import sys
from pathlib import Path

# Project root
project_root = Path(__file__).parent.parent
theme_path = Path("D:/websites/websites/tradingrobotplug.com/wp/wp-content/themes/tradingrobotplug-theme")

def check_template_files():
    """Check which template files exist."""
    print("🔍 Checking template files...\n")
    
    templates = {
        "front-page.php": "Front page template (highest priority)",
        "frontpage.php": "Alternative front page (may conflict)",
        "frontpage_new.php": "Another alternative (may conflict)",
        "home.php": "Blog posts index",
        "index.php": "Fallback template",
        "functions.php": "Theme functions",
        "inc/template-helpers.php": "Template loading filter"
    }
    
    found = {}
    for template, description in templates.items():
        template_file = theme_path / template
        exists = template_file.exists()
        found[template] = exists
        status = "✅" if exists else "❌"
        print(f"  {status} {template}: {description}")
    
    return found

def check_template_include_filter():
    """Check template_include filter logic."""
    print("\n🔍 Checking template_include filter...\n")
    
    template_helpers = theme_path / "inc/template-helpers.php"
    if not template_helpers.exists():
        print("  ❌ template-helpers.php not found")
        return False
    
    content = template_helpers.read_text(encoding='utf-8')
    
    issues = []
    
    # Check if filter handles front page
    if 'is_front_page()' not in content and 'is_home()' not in content:
        issues.append("⚠️  Filter doesn't explicitly handle is_front_page() or is_home()")
        print("  ⚠️  template_include filter doesn't check is_front_page() or is_home()")
        print("     This could prevent front-page.php from loading correctly")
    
    # Check filter priority
    if 'add_filter(\'template_include\'' in content:
        if ', 999)' in content:
            print("  ✅ Filter priority: 999 (should run last)")
        else:
            print("  ⚠️  Filter priority may conflict with WordPress template hierarchy")
    
    # Check if filter returns early for front page
    if 'return $template;' in content:
        lines = content.split('\n')
        for i, line in enumerate(lines[:30], 1):  # Check first 30 lines
            if 'return $template;' in line:
                print(f"  ℹ️  Filter has early return at line {i}")
                # Check context
                context_start = max(0, i-5)
                context_end = min(len(lines), i+3)
                context = '\n'.join(lines[context_start:context_end])
                if 'is_admin' in context or 'wp_doing_ajax' in context:
                    print(f"     Context: Early return for admin/AJAX (OK)")
    
    return True

def check_front_page_content():
    """Check front-page.php has required content."""
    print("\n🔍 Checking front-page.php content...\n")
    
    front_page = theme_path / "front-page.php"
    if not front_page.exists():
        print("  ❌ front-page.php not found")
        return False
    
    content = front_page.read_text(encoding='utf-8')
    
    checks = {
        "Hero section": "hero" in content.lower() and "Join the Waitlist" in content,
        "Waitlist form": "waitlist" in content.lower() and "form" in content.lower(),
        "get_header()": "get_header()" in content,
        "get_footer()": "get_footer()" in content,
    }
    
    for check, result in checks.items():
        status = "✅" if result else "❌"
        print(f"  {status} {check}: {'Found' if result else 'Missing'}")
    
    return all(checks.values())

def check_functions_php_includes():
    """Check functions.php includes template-helpers."""
    print("\n🔍 Checking functions.php module loading...\n")
    
    functions = theme_path / "functions.php"
    if not functions.exists():
        print("  ❌ functions.php not found")
        return False
    
    content = functions.read_text(encoding='utf-8')
    
    if 'template-helpers' in content or 'template_helpers' in content:
        print("  ✅ template-helpers.php is included in functions.php")
        return True
    else:
        print("  ⚠️  template-helpers.php may not be included in functions.php")
        print("     Check if module loading system includes it")
        return False

def generate_fix_recommendations():
    """Generate fix recommendations."""
    print("\n📋 Fix Recommendations:\n")
    
    recommendations = [
        {
            "issue": "template_include filter doesn't handle front page",
            "fix": "Add is_front_page() check to return early, allowing WordPress template hierarchy to work",
            "priority": "HIGH"
        },
        {
            "issue": "Multiple front page template files may conflict",
            "fix": "Remove or rename frontpage.php and frontpage_new.php to avoid conflicts",
            "priority": "MEDIUM"
        },
        {
            "issue": "Template filter priority may interfere",
            "fix": "Ensure filter returns original template for front page (don't override front-page.php)",
            "priority": "HIGH"
        },
        {
            "issue": "Cache may be serving old template",
            "fix": "Clear WordPress cache, browser cache, and CDN cache",
            "priority": "MEDIUM"
        }
    ]
    
    for i, rec in enumerate(recommendations, 1):
        priority_icon = "🔴" if rec["priority"] == "HIGH" else "🟡"
        print(f"{i}. {priority_icon} [{rec['priority']}] {rec['issue']}")
        print(f"   Fix: {rec['fix']}\n")

def main():
    """Main execution."""
    print("=" * 60)
    print("TradingRobotPlug.com Template Loading Verification")
    print("=" * 60 + "\n")
    
    # Check template files
    templates = check_template_files()
    
    # Check template_include filter
    has_filter = check_template_include_filter()
    
    # Check front page content
    has_content = check_front_page_content()
    
    # Check functions.php
    has_includes = check_functions_php_includes()
    
    # Generate recommendations
    generate_fix_recommendations()
    
    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    
    issues_found = []
    if not templates.get("front-page.php"):
        issues_found.append("❌ front-page.php missing")
    if not has_content:
        issues_found.append("❌ front-page.php missing required content")
    if has_filter and 'is_front_page()' not in (theme_path / "inc/template-helpers.php").read_text():
        issues_found.append("⚠️  template_include filter may block front-page.php")
    if templates.get("frontpage.php") or templates.get("frontpage_new.php"):
        issues_found.append("⚠️  Multiple front page templates may conflict")
    
    if issues_found:
        print("\n🚨 Issues Found:")
        for issue in issues_found:
            print(f"  {issue}")
    else:
        print("\n✅ All checks passed (but deployment may still be needed)")
    
    print("\n📝 Next Steps:")
    print("  1. Review template-helpers.php and ensure it doesn't override front-page.php")
    print("  2. Remove duplicate front page templates (frontpage.php, frontpage_new.php)")
    print("  3. Verify theme is active on production server")
    print("  4. Clear all caches (WordPress, browser, CDN)")
    print("  5. Test deployment to production server")

if __name__ == "__main__":
    main()

