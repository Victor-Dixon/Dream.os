#!/usr/bin/env python3
"""
Comprehensive Site Health Fix Plan
===================================

Automated and manual fixes for all site issues.
Priority: Fix broken links and connectivity problems.

Author: Agent-5 (Business Intelligence Specialist)
"""

import json
from pathlib import Path
from typing import Dict, List, Any

def generate_site_fix_plan():
    """Generate a comprehensive plan to fix all site issues."""

    # Load current broken links data
    audit_file = Path('docs/site_audit/broken_links.json')
    if not audit_file.exists():
        print("❌ Audit file not found")
        return

    with open(audit_file, 'r') as f:
        audit_data = json.load(f)

    print("🚀 COMPREHENSIVE SITE HEALTH FIX PLAN")
    print("=" * 60)
    print(f"Generated: {audit_data['generated_at']}")
    print()

    # Count issues
    total_sites = len(audit_data['sites'])
    sites_with_issues = sum(1 for site in audit_data['sites'].values()
                           if len(site.get('broken_links', [])) > 0)
    total_broken_links = sum(len(site.get('broken_links', []))
                           for site in audit_data['sites'].values())

    print(f"📊 CURRENT STATUS:")
    print(f"   Total sites: {total_sites}")
    print(f"   Sites with issues: {sites_with_issues}")
    print(f"   Total broken links: {total_broken_links}")
    print()

    # PHASE 1: Automated Fixes
    print("🔧 PHASE 1: AUTOMATED FIXES")
    print("-" * 40)

    automated_fixes = []

    # Check for sites with WordPress API credentials
    site_configs_file = Path('site_configs.json')
    if site_configs_file.exists():
        with open(site_configs_file, 'r') as f:
            site_configs = json.load(f)

        api_sites = []
        for site_name, config in site_configs.items():
            rest_api = config.get('rest_api', {})
            if rest_api.get('username') and rest_api.get('app_password'):
                api_sites.append(site_name)

        if api_sites:
            print("✅ WordPress API Available for:")
            for site in api_sites:
                if site in audit_data['sites'] and audit_data['sites'][site]['broken_links']:
                    automated_fixes.append(site)
                    print(f"   - {site}: Can fix {len(audit_data['sites'][site]['broken_links'])} broken links")
        else:
            print("❌ No sites have WordPress API credentials configured")
    print()

    # PHASE 2: Manual WordPress Admin Fixes
    print("🖱️ PHASE 2: MANUAL WORDPRESS ADMIN FIXES")
    print("-" * 40)

    manual_fixes = {
        'weareswarm.online': {
            'description': 'Remove broken GitHub footer link',
            'steps': [
                '1. Log into WordPress admin: https://weareswarm.online/wp-admin/',
                '2. Go to Appearance → Menus',
                '3. Find Footer menu',
                '4. Remove GitHub link (points to 404)',
                '5. Save menu'
            ]
        }
    }

    # Analyze missing pages that need to be created
    missing_pages = {}

    for site, info in audit_data['sites'].items():
        broken_links = info.get('broken_links', [])
        if not broken_links:
            continue

        site_missing_pages = []
        for link in broken_links:
            url = link['url']
            if site in url:  # Internal link
                path = url.replace(f'https://{site}/', '').replace(f'https://{site}', '')
                if path and '/' not in path and path not in ['contact', 'blog']:  # Simple pages
                    if path not in site_missing_pages:
                        site_missing_pages.append(path)

        if site_missing_pages:
            missing_pages[site] = site_missing_pages

    # Add missing page creation tasks
    for site, pages in missing_pages.items():
        if site not in manual_fixes:
            manual_fixes[site] = {'description': f'Create missing pages: {", ".join(pages)}'}

        manual_fixes[site]['steps'] = [
            '1. Log into WordPress admin',
            '2. Go to Pages → Add New',
            f'3. Create pages: {", ".join(pages)}',
            '4. Add basic content or placeholders',
            '5. Publish pages',
            '6. Update navigation menus if needed'
        ]

    for site, fix_info in manual_fixes.items():
        print(f"📝 {site.upper()}")
        print(f"   {fix_info['description']}")
        for step in fix_info.get('steps', []):
            print(f"   {step}")
        print()

    # PHASE 3: Infrastructure Fixes
    print("🔌 PHASE 3: INFRASTRUCTURE FIXES")
    print("-" * 40)

    print("🔧 SFTP Connectivity Issues (All Sites)")
    print("   Status: All sites showing SFTP connection failures")
    print("   Impact: Prevents automated deployments and theme updates")
    print()
    print("   Immediate Actions:")
    print("   1. Verify Hostinger SFTP credentials are current")
    print("   2. Check if IP addresses changed")
    print("   3. Test SFTP connection manually:")
    print("      sftp -P 65002 u996867598@157.173.214.121")
    print("   4. Update site_configs.json with correct SFTP details")
    print("   5. Test wordpress_manager.py connectivity")
    print()

    # PHASE 4: Monitoring and Verification
    print("📊 PHASE 4: MONITORING & VERIFICATION")
    print("-" * 40)

    print("🔍 Verification Commands:")
    print("   # Check all sites:")
    print("   python tools/comprehensive_website_audit.py")
    print()
    print("   # Check specific site:")
    print("   python tools/comprehensive_website_audit.py --site weareswarm.online --check-links")
    print()
    print("   # Verify Hostinger manager:")
    print("   python tools/hostinger_wordpress_manager.py --site weareswarm.online --health")
    print()

    # PHASE 5: Success Metrics
    print("🎯 PHASE 5: SUCCESS METRICS")
    print("-" * 40)

    print("📈 Target Improvements:")
    print(f"   Broken links: {total_broken_links} → 0 (100% reduction)")
    print(f"   Sites with issues: {sites_with_issues} → 0 (100% healthy)")
    print("   SFTP connectivity: 0 working → All sites working")
    print("   WordPress API access: Limited → Full access")
    print()

    # Generate action checklist
    print("✅ ACTION CHECKLIST")
    print("-" * 40)

    checklist = [
        ("Fix weareswarm.online GitHub link", "manual", "HIGH"),
        ("Create missing pages on tradingrobotplug.com", "manual", "HIGH"),
        ("Create missing pages on freerideinvestor.com", "manual", "MEDIUM"),
        ("Fix crosbyultimateevents.com blog link", "manual", "MEDIUM"),
        ("Fix SFTP connectivity for all sites", "infrastructure", "HIGH"),
        ("Test automated deployment tools", "verification", "MEDIUM"),
        ("Run final comprehensive audit", "verification", "HIGH")
    ]

    for i, (task, category, priority) in enumerate(checklist, 1):
        priority_icon = "🔴" if priority == "HIGH" else "🟡" if priority == "MEDIUM" else "🟢"
        category_icon = "🖱️" if category == "manual" else "🔧" if category == "infrastructure" else "✅"
        print("2d")

    print()
    print("🚀 Ready to execute fixes! Start with HIGH priority manual fixes.")

if __name__ == "__main__":
    generate_site_fix_plan()
