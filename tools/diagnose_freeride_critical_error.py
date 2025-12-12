#!/usr/bin/env python3
"""
FreeRideInvestor Critical Error Diagnostic & Fix Tool
======================================================
Diagnoses and provides fixes for WordPress critical error (HTTP 500).
"""

import requests
import re
from pathlib import Path
from datetime import datetime

def diagnose_critical_error():
    """Diagnose the critical error and provide actionable fixes."""
    print("=" * 70)
    print("FreeRideInvestor Critical Error Diagnostic")
    print("=" * 70)
    print()
    
    base_url = "https://freerideinvestor.com"
    
    # Check main site
    print("1. Checking site status...")
    try:
        r = requests.get(base_url, timeout=10)
        print(f"   Status: HTTP {r.status_code}")
        
        if r.status_code == 500:
            print("   ⚠️  HTTP 500 - Critical WordPress Error Detected")
            
            # Check for specific error patterns
            html = r.text
            
            if "critical error" in html.lower():
                print("   ❌ WordPress Critical Error confirmed")
            
            # Check if it's a PHP error
            php_errors = re.findall(
                r'(Fatal error|Parse error|Warning|Notice):\s*(.*?)(?=<|$|\n)',
                html,
                re.IGNORECASE | re.DOTALL
            )
            
            if php_errors:
                print("\n   PHP ERRORS FOUND:")
                for error_type, error_msg in php_errors[:5]:
                    print(f"      [{error_type}] {error_msg[:200]}")
            
            # Check for plugin/theme references
            plugin_refs = re.findall(
                r'wp-content/(plugins|themes)/([^/\s"]+)',
                html,
                re.IGNORECASE
            )
            
            if plugin_refs:
                print("\n   PLUGIN/THEME REFERENCES IN ERROR:")
                for ref_type, ref_name in set(plugin_refs[:10]):
                    print(f"      {ref_type}: {ref_name}")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    print("=" * 70)
    print("DIAGNOSIS & RECOMMENDED FIXES")
    print("=" * 70)
    print()
    
    print("🔍 LIKELY CAUSES:")
    print("   1. Plugin conflict (hostinger-reach plugin detected)")
    print("   2. Theme error in functions.php")
    print("   3. PHP fatal error (memory limit, syntax error)")
    print("   4. Database connection issue")
    print("   5. Corrupted WordPress core files")
    print()
    
    print("🛠️  RECOMMENDED FIXES (in order):")
    print()
    print("   FIX 1: Enable WordPress Debug Mode")
    print("   -----------------------------------")
    print("   Add to wp-config.php (via Hostinger File Manager):")
    print("   define('WP_DEBUG', true);")
    print("   define('WP_DEBUG_LOG', true);")
    print("   define('WP_DEBUG_DISPLAY', false);")
    print("   define('SCRIPT_DEBUG', true);")
    print("   Then check: wp-content/debug.log")
    print()
    
    print("   FIX 2: Disable Problematic Plugins")
    print("   -----------------------------------")
    print("   Via Hostinger File Manager, rename plugins folder:")
    print("   wp-content/plugins → wp-content/plugins-disabled")
    print("   Then test site. If it works, re-enable plugins one by one.")
    print()
    
    print("   FIX 3: Switch to Default Theme")
    print("   -------------------------------")
    print("   Rename theme folder:")
    print("   wp-content/themes/freerideinvestor → wp-content/themes/freerideinvestor-disabled")
    print("   WordPress will auto-switch to default theme.")
    print()
    
    print("   FIX 4: Check functions.php for Syntax Errors")
    print("   ---------------------------------------------")
    print("   Review: D:/websites/FreeRideInvestor/functions.php")
    print("   Look for:")
    print("   - Unclosed brackets/parentheses")
    print("   - Missing semicolons")
    print("   - PHP version compatibility issues")
    print("   - Memory-intensive operations")
    print()
    
    print("   FIX 5: Increase PHP Memory Limit")
    print("   --------------------------------")
    print("   Add to wp-config.php:")
    print("   define('WP_MEMORY_LIMIT', '256M');")
    print("   define('WP_MAX_MEMORY_LIMIT', '512M');")
    print()
    
    print("   FIX 6: Check Database Connection")
    print("   --------------------------------")
    print("   Verify wp-config.php database credentials")
    print("   Check Hostinger database status in cPanel")
    print()
    
    print("=" * 70)
    print("IMMEDIATE ACTION PLAN")
    print("=" * 70)
    print()
    print("1. Access Hostinger cPanel → File Manager")
    print("2. Navigate to public_html/wp-config.php")
    print("3. Enable debug mode (see FIX 1 above)")
    print("4. Check wp-content/debug.log for actual error")
    print("5. Based on error, apply appropriate fix above")
    print()
    print("ALTERNATIVE: Use Hostinger's WordPress Toolkit")
    print("  - Access WordPress Toolkit in cPanel")
    print("  - Use 'Repair' or 'Health Check' feature")
    print("  - May auto-fix common issues")
    print()
    
    # Save diagnostic report
    report_path = Path("runtime/freeride_diagnostic_report.txt")
    report_path.parent.mkdir(exist_ok=True)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"FreeRideInvestor Diagnostic Report\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n")
        f.write(f"\nStatus: HTTP 500 - Critical WordPress Error\n")
        f.write(f"\nSee diagnostic output above for fixes.\n")
    
    print(f"✅ Diagnostic report saved: {report_path}")
    print()

if __name__ == "__main__":
    diagnose_critical_error()

