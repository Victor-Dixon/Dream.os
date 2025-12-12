#!/usr/bin/env python3
"""
Extract detailed error information from FreeRideInvestor response.
"""

import requests
import re
from html import unescape

def extract_errors():
    """Extract all error information from the site response."""
    print("=" * 60)
    print("Extracting Error Details from FreeRideInvestor")
    print("=" * 60)
    print()
    
    try:
        r = requests.get('https://freerideinvestor.com', timeout=10)
        html = r.text
        
        print(f"Response Status: {r.status_code}")
        print(f"Response Length: {len(html)} bytes")
        print()
        
        # Look for PHP errors
        print("1. PHP Errors:")
        php_errors = re.findall(
            r'(Fatal error|Parse error|Warning|Notice|Deprecated):\s*(.*?)(?=<|$|\n\n)',
            html,
            re.IGNORECASE | re.DOTALL
        )
        if php_errors:
            for i, (error_type, error_msg) in enumerate(php_errors[:10], 1):
                error_msg = error_msg.strip()[:500]
                print(f"   {i}. [{error_type}] {error_msg}")
        else:
            print("   No PHP errors found in HTML")
        
        print()
        
        # Look for WordPress errors
        print("2. WordPress-Specific Errors:")
        wp_errors = re.findall(
            r'(wp-.*?error|WordPress.*?error|Database.*?error)',
            html,
            re.IGNORECASE
        )
        if wp_errors:
            for i, error in enumerate(set(wp_errors[:10]), 1):
                print(f"   {i}. {error}")
        else:
            print("   No WordPress-specific errors found")
        
        print()
        
        # Look for file paths in errors (might indicate which file is broken)
        print("3. File Paths in Errors:")
        file_paths = re.findall(
            r'(/.*?\.php)(?:\s+on\s+line\s+(\d+))?',
            html,
            re.IGNORECASE
        )
        if file_paths:
            for i, (path, line) in enumerate(set(file_paths[:10]), 1):
                line_info = f" (line {line})" if line else ""
                print(f"   {i}. {path}{line_info}")
        else:
            print("   No file paths found in errors")
        
        print()
        
        # Check for database errors
        print("4. Database Errors:")
        db_errors = re.findall(
            r'(database|mysql|mysqli|wpdb).*?error',
            html,
            re.IGNORECASE
        )
        if db_errors:
            for i, error in enumerate(set(db_errors[:5]), 1):
                print(f"   {i}. {error}")
        else:
            print("   No database errors found")
        
        print()
        
        # Look for plugin/theme names
        print("5. Plugin/Theme References:")
        plugin_refs = re.findall(
            r'(wp-content/(?:plugins|themes)/[^/\s]+)',
            html,
            re.IGNORECASE
        )
        if plugin_refs:
            for i, ref in enumerate(set(plugin_refs[:10]), 1):
                print(f"   {i}. {ref}")
        else:
            print("   No plugin/theme references found")
        
        print()
        
        # Save full HTML for manual inspection
        output_file = "runtime/freeride_error_response.html"
        from pathlib import Path
        Path("runtime").mkdir(exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"✅ Full response saved to: {output_file}")
        print("   (You can open this in a browser to see the full error)")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    extract_errors()

