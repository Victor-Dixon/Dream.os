#!/usr/bin/env python3
"""
⚠️ DEPRECATED - DO NOT USE

This file is deprecated as part of the SSOT consolidation effort.

REPLACEMENT: mcp_servers/deployment_server.py
MIGRATION: Use deploy_wordpress_theme() function instead
DEADLINE: 2026-02-01

For new code, use: mcp_servers/deployment_server.py::deploy_wordpress_theme()

Original docstring:
Deploy WeAreswarm Font Fix
==========================

Purpose: Deploy Google Fonts fix to weareswarm.online immediately.
Usage: python tools/deploy_weareswarm_font_fix.py
Author: Agent-7 (Web Development Specialist)
Date: 2025-12-29
Description: Immediate deployment tool for fixing Google Fonts issues on weareswarm.online website.

<!-- SSOT Domain: web -->
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "websites"))

from ops.deployment.simple_wordpress_deployer import SimpleWordPressDeployer, load_site_configs

def main():
    site_key = "weareswarm.online"
    configs = load_site_configs()
    deployer = SimpleWordPressDeployer(site_key, configs)
    
    if not deployer.connect():
        print(f"❌ Failed to connect to {site_key}")
        return 1
    
    print(f"✅ Connected to {site_key}")
    
    theme_dir = Path("D:/websites/websites/weareswarm.online/wp/wp-content/themes/swarm-theme")
    files_to_deploy = ["functions.php", "header.php"]
    
    remote_base = "wp-content/themes/swarm-theme"
    deployed = 0
    
    for file_name in files_to_deploy:
        local_path = theme_dir / file_name
        if not local_path.exists():
            print(f"⚠️  File not found: {local_path}")
            continue
        
        remote_path = f"{remote_base}/{file_name}"
        if deployer.deploy_file(local_path, remote_path):
            print(f"✅ Deployed: {file_name}")
            deployed += 1
        else:
            print(f"❌ Failed: {file_name}")
    
    deployer.disconnect()
    print(f"✅ Deployed {deployed} files for {site_key}")
    return 0

if __name__ == "__main__":
    sys.exit(main())

