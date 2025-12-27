#!/usr/bin/env python3
"""
Automated P0 Analytics Validation Runner
========================================

Runs automated analytics validation on all P0 fixes, checking for GA4/Pixel deployment
and configuration status. Can be run periodically to monitor validation readiness.

Usage:
    python tools/automated_p0_analytics_validation.py [--check-config-only] [--validate-ready]

SSOT: analytics
SSOT_DOMAIN: analytics
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))


def check_configuration_status() -> Dict[str, Any]:
    """Check GA4/Pixel configuration status for all sites."""
    from tools.check_ga4_pixel_configuration import check_site_configuration
    
    sites = [
        "freerideinvestor.com",
        "tradingrobotplug.com",
        "dadudekc.com",
        "crosbyultimateevents.com"
    ]
    
    results = {}
    for site in sites:
        results[site] = check_site_configuration(site)
    
    return results


def run_validation_on_ready_sites(config_status: Dict[str, Any]) -> Dict[str, Any]:
    """Run validation on sites that are ready."""
    from tools.validate_p0_fix_analytics import P0FixAnalyticsValidator
    
    validator = P0FixAnalyticsValidator()
    validation_results = {}
    
    tier1_fixes = [
        {"site": "freerideinvestor.com", "fix_id": "WEB-01", "fix_type": "hero"},
        {"site": "freerideinvestor.com", "fix_id": "WEB-04", "fix_type": "contact"},
        {"site": "freerideinvestor.com", "fix_id": "BRAND-01", "fix_type": "positioning"},
        {"site": "dadudekc.com", "fix_id": "WEB-01", "fix_type": "hero"},
        {"site": "dadudekc.com", "fix_id": "WEB-04", "fix_type": "contact"},
        {"site": "dadudekc.com", "fix_id": "BRAND-01", "fix_type": "positioning"},
        {"site": "crosbyultimateevents.com", "fix_id": "WEB-01", "fix_type": "hero"},
        {"site": "crosbyultimateevents.com", "fix_id": "WEB-04", "fix_type": "contact"},
        {"site": "crosbyultimateevents.com", "fix_id": "BRAND-01", "fix_type": "positioning"},
        {"site": "tradingrobotplug.com", "fix_id": "WEB-01", "fix_type": "hero"},
        {"site": "tradingrobotplug.com", "fix_id": "WEB-04", "fix_type": "contact"},
    ]
    
    for fix in tier1_fixes:
        site = fix["site"]
        
        # Only validate if site is ready
        if config_status.get(site, {}).get("ready_for_validation"):
            print(f"🔍 Validating {site} - {fix['fix_id']} ({fix['fix_type']})...")
            result = validator.validate_fix_analytics(
                site=site,
                fix_id=fix["fix_id"],
                fix_type=fix["fix_type"]
            )
            validation_results[f"{site}_{fix['fix_id']}"] = result
        else:
            status = config_status.get(site, {}).get("status", "UNKNOWN")
            print(f"⏭️  Skipping {site} - {fix['fix_id']} (Status: {status})")
    
    return validation_results


def generate_validation_report(config_status: Dict[str, Any], validation_results: Dict[str, Any]) -> str:
    """Generate validation status report."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    ready_sites = [site for site, status in config_status.items() if status.get("ready_for_validation")]
    pending_sites = [site for site, status in config_status.items() if not status.get("ready_for_validation")]
    
    report = f"""# P0 Analytics Validation Status Report

**Generated:** {timestamp}  
**Agent:** Agent-5  
**Status:** 🟡 ACTIVE

---

## Configuration Status

### ✅ Ready for Validation ({len(ready_sites)}/{len(config_status)})
"""
    
    for site in ready_sites:
        status = config_status[site]
        report += f"""
- **{site}**
  - Code Deployed: ✅
  - GA4 Configured: {'✅' if status.get('ga4_configured') else '❌'}
  - Pixel Configured: {'✅' if status.get('pixel_configured') else '❌'}
"""
    
    report += f"""
### ⏳ Pending Configuration ({len(pending_sites)}/{len(config_status)})
"""
    
    for site in pending_sites:
        status = config_status[site]
        site_status = status.get("status", "UNKNOWN")
        report += f"""
- **{site}** - {site_status}
  - Code Deployed: {'✅' if status.get('code_deployed') else '❌'}
  - GA4 Configured: {'✅' if status.get('ga4_configured') else '❌'}
  - Pixel Configured: {'✅' if status.get('pixel_configured') else '❌'}
"""
    
    if validation_results:
        report += f"""
---

## Validation Results

**Total Validations:** {len(validation_results)}  
**Passed:** {sum(1 for r in validation_results.values() if r.get('status') == 'PASS')}  
**Failed:** {sum(1 for r in validation_results.values() if r.get('status') == 'FAIL')}  
**Pending:** {sum(1 for r in validation_results.values() if r.get('status') == 'PENDING')}

"""
        
        for key, result in validation_results.items():
            site = result.get("site", "unknown")
            fix_id = result.get("fix_id", "unknown")
            status_icon = {"PASS": "✅", "FAIL": "❌", "PENDING": "⏳"}.get(result.get("status"), "❓")
            
            report += f"""
### {status_icon} {site} - {fix_id}
- **Status:** {result.get('status', 'UNKNOWN')}
- **Validations:** {len(result.get('validations', {}))}
"""
    
    report += f"""
---

## Next Steps

1. **Configure GA4/Pixel IDs** for sites with code deployed but IDs missing
   - Sites: {', '.join([s for s, st in config_status.items() if st.get('code_deployed') and not st.get('ready_for_validation')])}
   - Action: Add GA4_MEASUREMENT_ID and FACEBOOK_PIXEL_ID to wp-config.php

2. **Complete Remote Deployment** for sites pending deployment
   - Sites: {', '.join([s for s, st in config_status.items() if not st.get('code_deployed')])}
   - Action: Coordinate with Agent-3 for remote deployment

3. **Run Validation** on ready sites
   - Command: `python tools/automated_p0_analytics_validation.py --validate-ready`

4. **Monitor Progress** - Run this script periodically to check validation readiness

---

**Report Generated By:** Automated P0 Analytics Validation Runner  
**Tool:** tools/automated_p0_analytics_validation.py
"""
    
    return report


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Automated P0 analytics validation runner',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--check-config-only',
        action='store_true',
        help='Only check configuration status, do not run validation'
    )
    
    parser.add_argument(
        '--validate-ready',
        action='store_true',
        help='Run validation on sites that are ready'
    )
    
    args = parser.parse_args()
    
    print("📊 P0 Analytics Validation - Automated Runner\n")
    
    # Check configuration status
    print("🔍 Checking GA4/Pixel configuration status...")
    config_status = check_configuration_status()
    
    ready_count = sum(1 for s in config_status.values() if s.get("ready_for_validation"))
    total_count = len(config_status)
    
    print(f"\n📊 Configuration Status: {ready_count}/{total_count} sites ready for validation\n")
    
    validation_results = {}
    
    if not args.check_config_only:
        if args.validate_ready or ready_count > 0:
            print("🔍 Running validation on ready sites...\n")
            validation_results = run_validation_on_ready_sites(config_status)
        else:
            print("⏳ No sites ready for validation. Skipping validation run.\n")
    
    # Generate report
    report = generate_validation_report(config_status, validation_results)
    
    # Save report
    reports_dir = project_root / "reports"
    reports_dir.mkdir(exist_ok=True)
    
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = reports_dir / f"p0_analytics_validation_{timestamp_str}.md"
    report_file.write_text(report, encoding='utf-8')
    
    print(f"✅ Report generated: {report_file}\n")
    print(report)
    
    sys.exit(0)


if __name__ == '__main__':
    main()


