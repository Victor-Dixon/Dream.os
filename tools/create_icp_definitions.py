#!/usr/bin/env python3
"""
Create ICP Definitions for Revenue Engine Websites
BRAND-03 Fix - Tier 2 Foundation

Creates ICP definitions for:
- freerideinvestor.com
- dadudekc.com
- crosbyultimateevents.com

Usage:
    python tools/create_icp_definitions.py --site freerideinvestor.com
    python tools/create_icp_definitions.py --all
"""

import argparse
import subprocess
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def run_wp_cli_command(site_domain, command_file):
    """Run WP-CLI command file for a specific site"""
    # Check websites repository
    websites_root = Path('D:/websites')
    if not websites_root.exists():
        websites_root = project_root.parent / 'websites'
    
    site_paths = {
        'freerideinvestor.com': websites_root / 'websites/freerideinvestor.com/wp',
        'dadudekc.com': websites_root / 'sites/dadudekc.com/wp',
        'crosbyultimateevents.com': websites_root / 'sites/crosbyultimateevents.com/wp'
    }
    
    if site_domain not in site_paths:
        print(f"❌ Unknown site: {site_domain}")
        return False
    
    wp_path = site_paths[site_domain]
    command_path = wp_path / 'wp-content/themes' / get_theme_name(site_domain) / command_file
    
    if not command_path.exists():
        print(f"❌ Command file not found: {command_path}")
        return False
    
    try:
        # Run WP-CLI eval-file command
        cmd = ['wp', 'eval-file', str(command_path.relative_to(wp_path))]
        result = subprocess.run(
            cmd,
            cwd=str(wp_path),
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print(f"✅ ICP definition created for {site_domain}")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print(f"❌ Failed to create ICP definition for {site_domain}")
            if result.stderr:
                print(result.stderr)
            return False
    except subprocess.TimeoutExpired:
        print(f"❌ Timeout creating ICP definition for {site_domain}")
        return False
    except Exception as e:
        print(f"❌ Error creating ICP definition for {site_domain}: {e}")
        return False

def get_theme_name(site_domain):
    """Get theme name for site"""
    themes = {
        'freerideinvestor.com': 'freerideinvestor-modern',
        'dadudekc.com': 'dadudekc',
        'crosbyultimateevents.com': 'crosbyultimateevents'
    }
    return themes.get(site_domain, 'default')

def create_icp_for_site(site_domain):
    """Create ICP definition for a specific site"""
    print(f"\n📋 Creating ICP definition for {site_domain}...")
    
    # Check if CLI command exists
    if site_domain == 'freerideinvestor.com':
        # Use existing CLI command
        return run_wp_cli_command(site_domain, 'inc/cli-commands/create-brand-core-content.php')
    else:
        # For other sites, we need to create the infrastructure first
        print(f"⚠️  ICP infrastructure not yet created for {site_domain}")
        print(f"   Need to create: Custom Post Type, component template, CLI command")
        return False

def main():
    parser = argparse.ArgumentParser(description='Create ICP definitions for revenue engine websites')
    parser.add_argument('--site', choices=['freerideinvestor.com', 'dadudekc.com', 'crosbyultimateevents.com'],
                       help='Create ICP for specific site')
    parser.add_argument('--all', action='store_true', help='Create ICP for all sites')
    
    args = parser.parse_args()
    
    if not args.site and not args.all:
        parser.print_help()
        sys.exit(1)
    
    sites = []
    if args.all:
        sites = ['freerideinvestor.com', 'dadudekc.com', 'crosbyultimateevents.com']
    else:
        sites = [args.site]
    
    results = {}
    for site in sites:
        results[site] = create_icp_for_site(site)
    
    # Summary
    print("\n" + "="*60)
    print("📊 SUMMARY")
    print("="*60)
    for site, success in results.items():
        status = "✅ COMPLETE" if success else "❌ FAILED"
        print(f"{site}: {status}")
    
    if all(results.values()):
        print("\n✅ All ICP definitions created successfully!")
        sys.exit(0)
    else:
        print("\n⚠️  Some ICP definitions failed. Check output above.")
        sys.exit(1)

if __name__ == '__main__':
    main()

