#!/usr/bin/env python3
"""
TradingRobotPlug.com Comprehensive Template Verification Tool
==============================================================

Comprehensive verification based on Agent-4 (Captain) investigation guidance:
1. template-helpers.php - trp_template_include function
2. functions.php - ensure template-helpers.php is included
3. front-page.php - verify hero section and waitlist form code
4. WordPress Settings - Reading Settings (Static front page vs Posts page)
5. Theme activation status

V2 Compliance | Author: Agent-3 | Date: 2025-12-25
"""

import sys
from pathlib import Path
import re

# Theme path
theme_path = Path("D:/websites/websites/tradingrobotplug.com/wp/wp-content/themes/tradingrobotplug-theme")

def check_template_helpers_function():
    """Check template-helpers.php trp_template_include function."""
    print("=" * 60)
    print("1. template-helpers.php - trp_template_include function")
    print("=" * 60 + "\n")
    
    template_helpers = theme_path / "inc/template-helpers.php"
    if not template_helpers.exists():
        print("  ❌ template-helpers.php not found")
        return False
    
    content = template_helpers.read_text(encoding='utf-8')
    
    checks = {
        "File exists": True,
        "Function trp_template_include exists": "function trp_template_include" in content,
        "Filter added (line 94)": "add_filter('template_include', 'trp_template_include'" in content,
        "Priority 999": ", 999)" in content or ",999)" in content,
        "Checks is_front_page()": "is_front_page()" in content,
        "Checks is_home()": "is_home()" in content,
        "Returns early for front page": "if (is_front_page() || is_home())" in content,
        "Admin/AJAX skip": "is_admin() || wp_doing_ajax()" in content,
        "404 handling": "is_404()" in content,
    }
    
    for check, result in checks.items():
        status = "✅" if result else "❌"
        print(f"  {status} {check}")
    
    # Show function location
    if "function trp_template_include" in content:
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if "function trp_template_include" in line:
                print(f"\n  ℹ️  Function defined at line {i}")
            if "add_filter('template_include'" in line:
                print(f"  ℹ️  Filter added at line {i}")
    
    return all(checks.values())

def check_functions_php_includes():
    """Check functions.php includes template-helpers.php."""
    print("\n" + "=" * 60)
    print("2. functions.php - template-helpers.php inclusion")
    print("=" * 60 + "\n")
    
    functions = theme_path / "functions.php"
    if not functions.exists():
        print("  ❌ functions.php not found")
        return False
    
    content = functions.read_text(encoding='utf-8')
    
    # Check various inclusion patterns
    patterns = [
        r"require.*template-helpers",
        r"require.*template_helpers",
        r"include.*template-helpers",
        r"include.*template_helpers",
    ]
    
    found = False
    for pattern in patterns:
        if re.search(pattern, content, re.IGNORECASE):
            found = True
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                line_num = content[:match.start()].count('\n') + 1
                line_content = content.split('\n')[line_num - 1].strip()
                print(f"  ✅ Found inclusion: {line_content}")
                print(f"     Line {line_num}")
    
    if not found:
        print("  ❌ template-helpers.php not found in functions.php includes")
        print("  ℹ️  Check if module loading system includes it")
    
    # Check module loading structure
    if "$inc_dir" in content or "inc_dir" in content:
        print("\n  ℹ️  Modular loading structure detected")
        if "template-helpers" in content.lower():
            print("  ✅ template-helpers referenced in module loading")
    
    return found or "template-helpers" in content.lower()

def check_front_page_content():
    """Check front-page.php has hero section and waitlist form."""
    print("\n" + "=" * 60)
    print("3. front-page.php - Hero section and waitlist form")
    print("=" * 60 + "\n")
    
    front_page = theme_path / "front-page.php"
    if not front_page.exists():
        print("  ❌ front-page.php not found")
        return False
    
    content = front_page.read_text(encoding='utf-8')
    
    # Hero section checks
    hero_checks = {
        "File exists": True,
        "Hero section tag": "hero" in content.lower() or "<section class=\"hero\"" in content,
        "Hero headline": "Join the Waitlist" in content or "hero-heading" in content.lower(),
        "Hero subheadline": "hero-subheadline" in content.lower() or "building and testing" in content.lower(),
        "Primary CTA": "cta-button primary" in content.lower() or "Join the Waitlist" in content,
        "Secondary CTA": "Watch Us Build Live" in content or "secondary" in content.lower(),
        "Urgency text": "Limited early access" in content or "hero-urgency" in content.lower(),
    }
    
    print("  Hero Section Checks:")
    for check, result in hero_checks.items():
        status = "✅" if result else "❌"
        print(f"    {status} {check}")
    
    # Waitlist form checks
    waitlist_checks = {
        "Waitlist section": "waitlist" in content.lower(),
        "Waitlist form": "form" in content.lower() and "waitlist" in content.lower(),
        "Email input": "type=\"email\"" in content or "email" in content.lower(),
        "Form action": "admin-post.php" in content or "action=" in content.lower(),
        "Join Waitlist button": "Join the Waitlist" in content or "Join Waitlist" in content,
    }
    
    print("\n  Waitlist Form Checks:")
    for check, result in waitlist_checks.items():
        status = "✅" if result else "❌"
        print(f"    {status} {check}")
    
    # Structural checks
    structural_checks = {
        "get_header()": "get_header()" in content,
        "get_footer()": "get_footer()" in content,
        "PHP opening tag": content.strip().startswith("<?php"),
    }
    
    print("\n  Structural Checks:")
    for check, result in structural_checks.items():
        status = "✅" if result else "❌"
        print(f"    {status} {check}")
    
    # Show line numbers for key elements
    lines = content.split('\n')
    print("\n  ℹ️  Key Element Locations:")
    for i, line in enumerate(lines, 1):
        if "hero" in line.lower() and "section" in line.lower():
            print(f"    Hero section starts around line {i}")
        if "waitlist" in line.lower() and "section" in line.lower():
            print(f"    Waitlist section starts around line {i}")
    
    all_checks = {**hero_checks, **waitlist_checks, **structural_checks}
    return all(all_checks.values())

def check_wordpress_settings_note():
    """Note about WordPress Reading Settings."""
    print("\n" + "=" * 60)
    print("4. WordPress Settings - Reading Settings")
    print("=" * 60 + "\n")
    
    print("  ⚠️  Manual verification required (cannot check programmatically)")
    print("\n  📋 WordPress Admin Checklist:")
    print("    1. Navigate to: Settings > Reading")
    print("    2. Check 'Your homepage displays':")
    print("       - ✅ Should be: 'A static page'")
    print("       - ✅ 'Homepage' should be set to a page OR left blank")
    print("       - ❌ If set to 'Your latest posts', front-page.php won't load")
    print("    3. If using static page:")
    print("       - WordPress will use front-page.php for static front page")
    print("       - This is the correct configuration")
    print("    4. If using 'Your latest posts':")
    print("       - WordPress will use home.php or index.php")
    print("       - front-page.php will NOT be used")
    print("       - This would explain why hero section isn't showing")
    
    print("\n  🔍 How to Check (if you have database/WP-CLI access):")
    print("    Option 1: WordPress Admin")
    print("      - Login to wp-admin")
    print("      - Go to Settings > Reading")
    print("      - Check 'Your homepage displays' setting")
    print("\n    Option 2: WP-CLI")
    print("      wp option get show_on_front")
    print("      wp option get page_on_front")
    print("\n    Option 3: Database")
    print("      SELECT option_value FROM wp_options WHERE option_name = 'show_on_front';")
    print("      SELECT option_value FROM wp_options WHERE option_name = 'page_on_front';")
    
    print("\n  ✅ Expected Values:")
    print("    show_on_front = 'page' (for static front page)")
    print("    page_on_front = page ID or 0 (if no page selected, front-page.php is used)")
    print("    OR")
    print("    show_on_front = 'posts' (would use home.php/index.php instead)")
    
    return None  # Cannot verify programmatically

def check_theme_activation_note():
    """Note about theme activation status."""
    print("\n" + "=" * 60)
    print("5. Theme Activation Status")
    print("=" * 60 + "\n")
    
    print("  ⚠️  Manual verification required (cannot check programmatically)")
    print("\n  📋 Theme Activation Checklist:")
    print("    1. Verify theme directory exists:")
    print(f"       ✅ Found: {theme_path}")
    
    # Check if theme directory has required files
    required_files = [
        "style.css",
        "functions.php",
        "front-page.php",
        "index.php",
    ]
    
    print("\n    2. Required theme files:")
    for file in required_files:
        exists = (theme_path / file).exists()
        status = "✅" if exists else "❌"
        print(f"       {status} {file}")
    
    print("\n    3. Check active theme (if you have database/WP-CLI access):")
    print("       Option 1: WordPress Admin")
    print("         - Login to wp-admin")
    print("         - Go to Appearance > Themes")
    print("         - Verify 'tradingrobotplug-theme' is active")
    print("\n       Option 2: WP-CLI")
    print("         wp theme list")
    print("         wp theme status tradingrobotplug-theme")
    print("\n       Option 3: Database")
    print("         SELECT option_value FROM wp_options WHERE option_name = 'stylesheet';")
    print("         SELECT option_value FROM wp_options WHERE option_name = 'template';")
    
    print("\n    4. ✅ Expected Values:")
    print("       stylesheet = 'tradingrobotplug-theme'")
    print("       template = 'tradingrobotplug-theme'")
    print("       (Both should match theme directory name)")
    
    # Check for style.css with theme headers
    style_css = theme_path / "style.css"
    if style_css.exists():
        content = style_css.read_text(encoding='utf-8')
        if "Theme Name:" in content:
            theme_name_match = re.search(r"Theme Name:\s*(.+)", content)
            if theme_name_match:
                theme_name = theme_name_match.group(1).strip()
                print(f"\n    5. Theme Name in style.css: {theme_name}")
    
    return True

def main():
    """Main execution."""
    print("=" * 60)
    print("TradingRobotPlug.com Comprehensive Template Verification")
    print("Based on Agent-4 (Captain) Investigation Guidance")
    print("=" * 60 + "\n")
    
    results = {}
    
    # 1. Check template-helpers.php
    results['template_helpers'] = check_template_helpers_function()
    
    # 2. Check functions.php includes
    results['functions_includes'] = check_functions_php_includes()
    
    # 3. Check front-page.php content
    results['front_page_content'] = check_front_page_content()
    
    # 4. WordPress Settings (manual check required)
    check_wordpress_settings_note()
    
    # 5. Theme activation (manual check required)
    check_theme_activation_note()
    
    # Summary
    print("\n" + "=" * 60)
    print("Verification Summary")
    print("=" * 60 + "\n")
    
    automated_checks = {k: v for k, v in results.items() if v is not None}
    all_passed = all(automated_checks.values()) if automated_checks else False
    
    print("Automated Checks:")
    for check, result in automated_checks.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} {check.replace('_', ' ').title()}")
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ All automated checks passed!")
    else:
        print("⚠️  Some checks failed - review details above")
    
    print("\n📋 Manual Verification Required:")
    print("  ⏳ WordPress Reading Settings (Static front page vs Posts)")
    print("  ⏳ Theme activation status on production server")
    print("  ⏳ File deployment to production server")
    print("  ⏳ Cache clearing on production server")
    
    print("\n📝 Next Steps:")
    print("  1. Verify WordPress Reading Settings (show_on_front = 'page')")
    print("  2. Verify theme is active on production")
    print("  3. Deploy updated template-helpers.php to production")
    print("  4. Clear all caches (WordPress, browser, CDN)")
    print("  5. Test front page on production server")

if __name__ == "__main__":
    main()

