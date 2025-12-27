#!/usr/bin/env python3
"""
Check GA4/Pixel Configuration Status
=====================================

Checks if GA4 and Facebook Pixel IDs are configured in wp-config.php for deployed sites.

Usage:
    python tools/check_ga4_pixel_configuration.py [--site <site>] [--all]

SSOT: analytics
SSOT_DOMAIN: analytics
"""

import sys
import re
import argparse
from pathlib import Path
from typing import Dict, List, Optional

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))


def check_wp_config(site_path: Path) -> Dict[str, bool]:
    """
    Check wp-config.php for GA4 and Pixel ID configuration.
    
    Returns:
        dict with ga4_configured and pixel_configured booleans
    """
    wp_config = site_path / "wp" / "wp-config.php"
    
    if not wp_config.exists():
        return {
            "ga4_configured": False,
            "pixel_configured": False,
            "config_file_exists": False
        }
    
    try:
        content = wp_config.read_text(encoding='utf-8')
        
        # Check for GA4 ID
        ga4_patterns = [
            r"define\s*\(\s*['\"]GA4_MEASUREMENT_ID['\"]\s*,\s*['\"](G-[A-Z0-9]+)['\"]",
            r"GA4_MEASUREMENT_ID\s*=\s*['\"](G-[A-Z0-9]+)['\"]",
            r"['\"]GA4_MEASUREMENT_ID['\"]\s*=>\s*['\"](G-[A-Z0-9]+)['\"]"
        ]
        
        ga4_configured = False
        for pattern in ga4_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                ga4_configured = True
                break
        
        # Check for Pixel ID
        pixel_patterns = [
            r"define\s*\(\s*['\"]FACEBOOK_PIXEL_ID['\"]\s*,\s*['\"]([0-9]+)['\"]",
            r"FACEBOOK_PIXEL_ID\s*=\s*['\"]([0-9]+)['\"]",
            r"['\"]FACEBOOK_PIXEL_ID['\"]\s*=>\s*['\"]([0-9]+)['\"]"
        ]
        
        pixel_configured = False
        for pixel_pattern in pixel_patterns:
            if re.search(pixel_pattern, content, re.IGNORECASE):
                pixel_configured = True
                break
        
        return {
            "ga4_configured": ga4_configured,
            "pixel_configured": pixel_configured,
            "config_file_exists": True
        }
        
    except Exception as e:
        return {
            "ga4_configured": False,
            "pixel_configured": False,
            "config_file_exists": True,
            "error": str(e)
        }


def check_functions_php(site_path: Path) -> Dict[str, bool]:
    """
    Check functions.php for analytics code deployment.
    
    Returns:
        dict with analytics_code_deployed boolean
    """
    # Try common theme locations
    theme_paths = [
        site_path / "wp" / "wp-content" / "themes" / "freerideinvestor-modern" / "functions.php",
        site_path / "wp" / "wp-content" / "themes" / "tradingrobotplug-theme" / "functions.php",
    ]
    
    # Also try to find any functions.php in themes
    themes_dir = site_path / "wp" / "wp-content" / "themes"
    if themes_dir.exists():
        for theme_dir in themes_dir.iterdir():
            if theme_dir.is_dir():
                func_file = theme_dir / "functions.php"
                if func_file.exists():
                    theme_paths.append(func_file)
    
    analytics_code_deployed = False
    
    for func_file in theme_paths:
        if func_file.exists():
            try:
                content = func_file.read_text(encoding='utf-8')
                
                # Check for analytics function
                if "add_analytics_tracking" in content or "analytics_tracking" in content:
                    # Check for GA4 or Pixel code
                    if "gtag" in content or "fbq" in content or "GA4_MEASUREMENT_ID" in content:
                        analytics_code_deployed = True
                        break
            except Exception:
                continue
    
    return {
        "analytics_code_deployed": analytics_code_deployed
    }


def check_site_configuration(site: str) -> Dict[str, any]:
    """
    Check complete configuration status for a site.
    
    Returns:
        Complete configuration status dict
    """
    # Try to find site in websites directory
    websites_root = Path("D:/websites/websites")
    if not websites_root.exists():
        websites_root = project_root / "websites"
    
    site_path = websites_root / site
    
    if not site_path.exists():
        return {
            "site": site,
            "status": "NOT_FOUND",
            "message": f"Site directory not found: {site_path}"
        }
    
    wp_config_status = check_wp_config(site_path)
    functions_status = check_functions_php(site_path)
    
    # Determine overall status
    code_deployed = functions_status.get("analytics_code_deployed", False)
    ids_configured = wp_config_status.get("ga4_configured", False) or wp_config_status.get("pixel_configured", False)
    
    if code_deployed and ids_configured:
        status = "READY"
    elif code_deployed and not ids_configured:
        status = "PENDING_IDS"
    elif not code_deployed:
        status = "PENDING_DEPLOYMENT"
    else:
        status = "UNKNOWN"
    
    return {
        "site": site,
        "status": status,
        "code_deployed": code_deployed,
        "ga4_configured": wp_config_status.get("ga4_configured", False),
        "pixel_configured": wp_config_status.get("pixel_configured", False),
        "config_file_exists": wp_config_status.get("config_file_exists", False),
        "ready_for_validation": code_deployed and ids_configured
    }


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Check GA4/Pixel configuration status for sites',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--site',
        type=str,
        help='Check specific site (e.g., freerideinvestor.com)'
    )
    
    parser.add_argument(
        '--all',
        action='store_true',
        help='Check all P0 sites'
    )
    
    args = parser.parse_args()
    
    sites_to_check = []
    
    if args.all:
        sites_to_check = [
            "freerideinvestor.com",
            "tradingrobotplug.com",
            "dadudekc.com",
            "crosbyultimateevents.com"
        ]
    elif args.site:
        sites_to_check = [args.site]
    else:
        # Default: check all P0 sites
        sites_to_check = [
            "freerideinvestor.com",
            "tradingrobotplug.com",
            "dadudekc.com",
            "crosbyultimateevents.com"
        ]
    
    print("🔍 Checking GA4/Pixel Configuration Status\n")
    
    results = []
    for site in sites_to_check:
        result = check_site_configuration(site)
        results.append(result)
        
        status_icon = {
            "READY": "✅",
            "PENDING_IDS": "🟡",
            "PENDING_DEPLOYMENT": "⏳",
            "NOT_FOUND": "❌",
            "UNKNOWN": "⚠️"
        }.get(result["status"], "❓")
        
        print(f"{status_icon} {site}")
        print(f"   Status: {result['status']}")
        print(f"   Code Deployed: {'✅' if result.get('code_deployed') else '❌'}")
        print(f"   GA4 Configured: {'✅' if result.get('ga4_configured') else '❌'}")
        print(f"   Pixel Configured: {'✅' if result.get('pixel_configured') else '❌'}")
        print(f"   Ready for Validation: {'✅' if result.get('ready_for_validation') else '❌'}")
        if result.get("message"):
            print(f"   Note: {result['message']}")
        print()
    
    # Summary
    ready_count = sum(1 for r in results if r.get("ready_for_validation"))
    total_count = len(results)
    
    print(f"📊 Summary: {ready_count}/{total_count} sites ready for validation")
    
    if ready_count > 0:
        ready_sites = [r["site"] for r in results if r.get("ready_for_validation")]
        print(f"✅ Ready sites: {', '.join(ready_sites)}")
        print("\n💡 Next step: Run validation on ready sites:")
        for site in ready_sites:
            print(f"   python tools/validate_p0_fix_analytics.py --site {site} --fix-id WEB-01 --fix-type hero")
    
    sys.exit(0)


if __name__ == '__main__':
    main()


