#!/usr/bin/env python3
"""
Build-In-Public Phase 0 Deployment
====================================

Deploys Phase 0 placeholders to dadudekc.com and weareswarm.online using Hostinger SFTP.
URGENT: Phase 0 not deployed, sections missing on live sites.

Author: Agent-3 (Infrastructure & DevOps)
Date: 2025-12-26
"""

import sys
from pathlib import Path

# Add websites deployment tools to path
sys.path.insert(0, str(Path("D:/websites/ops/deployment").resolve()))

from simple_wordpress_deployer import SimpleWordPressDeployer, load_site_configs

# dadudekc.com files
DADUDEKC_FILES = [
    "front-page.php",
    "style.css",
]

# weareswarm.online files (complete theme)
WEARESWARM_FILES = [
    "style.css",
    "functions.php",
    "header.php",
    "footer.php",
    "front-page.php",
    "index.php",
    "page-swarm-manifesto.php",
    "page-how-the-swarm-works.php",
]

# Local directories
DADUDEKC_LOCAL = Path("D:/websites/sites/dadudekc.com/wp/theme/dadudekc")
WEARESWARM_LOCAL = Path("D:/websites/sites/weareswarm.online/wp/theme/swarm")

# Remote paths
DADUDEKC_REMOTE = "domains/dadudekc.com/public_html/wp-content/themes/dadudekc"
WEARESWARM_REMOTE = "domains/weareswarm.online/public_html/wp-content/themes/swarm"


def deploy_site(site_key: str, files: list, local_dir: Path, remote_path: str, dry_run: bool = False):
    """Deploy files for a single site."""
    print(f"\n🚀 Deploying {site_key} Phase 0...")
    print("=" * 60)
    
    # Load site configurations
    site_configs = load_site_configs()
    if not site_configs:
        print(f"❌ No site configurations found for {site_key}")
        return False
    
    # Initialize deployer
    try:
        deployer = SimpleWordPressDeployer(site_key, site_configs)
    except ValueError as e:
        print(f"❌ {e}")
        return False
    
    # Connect to server
    print(f"🔌 Connecting to server...")
    if not deployer.connect():
        print(f"❌ Failed to connect to server for {site_key}")
        return False
    
    print(f"✅ Connected successfully\n")
    
    # Deploy files
    success_count = 0
    failed_files = []
    
    for file_path in files:
        local_file = local_dir / file_path
        
        # Resolve to absolute path
        local_file = local_file.resolve()
        
        if not local_file.exists():
            print(f"⚠️  File not found: {local_file}")
            failed_files.append(file_path)
            continue
        
        if not local_file.is_file():
            print(f"⚠️  Not a file: {local_file}")
            failed_files.append(file_path)
            continue
        
        # Build remote path
        remote_file = f"{remote_path}/{file_path}"
        
        if dry_run:
            print(f"📋 [DRY RUN] Would deploy: {file_path}")
            print(f"   Local: {local_file}")
            print(f"   Remote: {remote_file}\n")
            success_count += 1
        else:
            print(f"📤 Deploying: {file_path}...")
            # Ensure remote directory exists before deploying
            remote_dir = "/".join(remote_file.split("/")[:-1])
            if remote_dir:
                try:
                    # Try to create directory structure
                    deployer.execute_command(f"mkdir -p {remote_dir}")
                except:
                    pass  # Directory might already exist
            
            if deployer.deploy_file(local_file, remote_file):
                print(f"✅ Deployed: {file_path}\n")
                success_count += 1
            else:
                print(f"❌ Failed: {file_path}\n")
                failed_files.append(file_path)
    
    # Disconnect
    deployer.disconnect()
    
    # Summary
    print("=" * 60)
    print(f"📊 {site_key} Deployment Summary:")
    print(f"   ✅ Success: {success_count}/{len(files)} files")
    if failed_files:
        print(f"   ❌ Failed: {len(failed_files)} files")
        print(f"   Failed files: {', '.join(failed_files)}")
    
    return success_count == len(files)


def deploy_build_in_public_phase0(dry_run: bool = False):
    """Deploy Build-In-Public Phase 0 to both sites."""
    print("🚀 Build-In-Public Phase 0 Deployment")
    print("=" * 60)
    print("Sites: dadudekc.com, weareswarm.online")
    print("=" * 60)
    
    # Deploy dadudekc.com
    dadudekc_success = deploy_site(
        "dadudekc.com",
        DADUDEKC_FILES,
        DADUDEKC_LOCAL,
        DADUDEKC_REMOTE,
        dry_run
    )
    
    # Deploy weareswarm.online
    weareswarm_success = deploy_site(
        "weareswarm.online",
        WEARESWARM_FILES,
        WEARESWARM_LOCAL,
        WEARESWARM_REMOTE,
        dry_run
    )
    
    # Overall summary
    print("\n" + "=" * 60)
    print("📊 Overall Deployment Summary:")
    print(f"   dadudekc.com: {'✅ SUCCESS' if dadudekc_success else '❌ FAILED'}")
    print(f"   weareswarm.online: {'✅ SUCCESS' if weareswarm_success else '❌ FAILED'}")
    
    if dadudekc_success and weareswarm_success:
        print(f"\n✅ All Phase 0 deployments successful!")
        if not dry_run:
            print(f"   🎯 Next steps:")
            print(f"   1. Verify theme activation (weareswarm.online)")
            print(f"   2. Clear all caches (WordPress, browser, CDN)")
            print(f"   3. Verify sections visible on live sites:")
            print(f"      - dadudekc.com: 'What I Do', 'Receipts/Proof', 'Live Experiments'")
            print(f"      - weareswarm.online: Manifesto page, 'How the Swarm Works' page, Build in Public section")
            print(f"   4. Captain re-verification")
        return True
    else:
        print(f"\n⚠️  Partial deployment - some sites failed")
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Deploy Build-In-Public Phase 0")
    parser.add_argument("--dry-run", action="store_true", help="Dry run mode (no actual deployment)")
    args = parser.parse_args()
    
    success = deploy_build_in_public_phase0(dry_run=args.dry_run)
    sys.exit(0 if success else 1)
