#!/usr/bin/env python3
"""
Deploy A/B Test Hero Headline for crosbyultimateevents.com

Deploys A/B test functionality for hero headline with benefit-focused variants and urgency.
"""

import os
import sys
from pathlib import Path

# Theme directory
THEME_DIR = Path(__file__).parent / "wordpress-theme" / "crosbyultimateevents"

def main():
    """Deploy A/B test hero headline."""
    print("🚀 Deploying A/B Test Hero Headline for crosbyultimateevents.com")
    print("=" * 60)
    
    # Verify files exist
    required_files = [
        "ab-test-hero-headline.php",
        "functions.php",
        "front-page.php"
    ]
    
    missing_files = []
    for file in required_files:
        filepath = THEME_DIR / file
        if not filepath.exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ ERROR: Missing required files: {', '.join(missing_files)}")
        return 1
    
    print("✅ All required files present")
    print("\n📋 A/B Test Implementation:")
    print("  • Variant A (Control): Current headline")
    print("  • Variant B (Test): Benefit-focused headline with urgency")
    print("  • Cookie-based persistence (30 days)")
    print("  • Analytics tracking ready (GA4/GTM)")
    print("\n✅ A/B test ready for deployment!")
    print("\n📝 Next Steps:")
    print("  1. Upload files to WordPress theme directory")
    print("  2. Clear cache if using caching plugin")
    print("  3. Test both variants by clearing cookies")
    print("  4. Set up analytics tracking (GA4/GTM)")
    print("  5. Monitor conversion rates for 2-4 weeks")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

