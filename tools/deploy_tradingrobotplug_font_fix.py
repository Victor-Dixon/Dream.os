#!/usr/bin/env python3
"""
⚠️ DEPRECATED - DO NOT USE

This file is deprecated as part of the SSOT consolidation effort.

REPLACEMENT: mcp_servers/deployment_server.py
MIGRATION: Use deploy_wordpress_theme() function instead
DEADLINE: 2026-02-01

For new code, use: mcp_servers/deployment_server.py::deploy_wordpress_theme()

Original docstring:
Deploy TradingRobotPlug.com font fix (Inter font in header.php)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'ops' / 'deployment'))

from simple_wordpress_deployer import SimpleWordPressDeployer, load_site_configs

def deploy_font_fix():
    site_key = 'tradingrobotplug.com'
    site_configs = load_site_configs()
    
    deployer = SimpleWordPressDeployer(site_key, site_configs)
    
    print(f"Connecting to SFTP server...")
    if not deployer.connect():
        print("❌ Failed to connect to SFTP server.")
        return False
    print(f"✅ Connected successfully")

    # Try multiple possible paths
    repo_root = Path(__file__).parent.parent
    local_paths = [
        Path('D:/websites/websites/tradingrobotplug.com/wp/wp-content/themes/tradingrobotplug-theme/header.php'),
        Path('D:/websites/sites/tradingrobotplug.com/wp/theme/tradingrobotplug-theme/header.php'),
        repo_root / 'websites' / 'websites' / 'tradingrobotplug.com' / 'wp' / 'wp-content' / 'themes' / 'tradingrobotplug-theme' / 'header.php',
        repo_root / 'websites' / 'sites' / 'tradingrobotplug.com' / 'wp' / 'theme' / 'tradingrobotplug-theme' / 'header.php',
    ]
    
    # Deploy header.php
    remote_path_header = 'wp-content/themes/tradingrobotplug-theme/header.php'
    header_deployed = False
    
    for local_path in local_paths:
        local_path_obj = Path(local_path) if isinstance(local_path, str) else local_path
        if local_path_obj.exists():
            print(f"Deploying header.php: {local_path_obj.absolute()}")
            result = deployer.deploy_file(local_path_obj, remote_path_header)
            header_deployed = result
            break
    
    # Deploy style.css
    style_paths = [
        Path('D:/websites/websites/tradingrobotplug.com/wp/wp-content/themes/tradingrobotplug-theme/style.css'),
        Path('D:/websites/sites/tradingrobotplug.com/wp/theme/tradingrobotplug-theme/style.css'),
    ]
    remote_path_css = 'wp-content/themes/tradingrobotplug-theme/style.css'
    css_deployed = False
    
    for style_path in style_paths:
        style_path_obj = Path(style_path) if isinstance(style_path, str) else style_path
        if style_path_obj.exists():
            print(f"Deploying style.css: {style_path_obj.absolute()}")
            result = deployer.deploy_file(style_path_obj, remote_path_css)
            css_deployed = result
            break
    
    if header_deployed and css_deployed:
        print("✅ Font fix (Inter font + CSS update) deployed successfully!")
        deployer.disconnect()
        return True
    elif header_deployed:
        print("⚠️ Header.php deployed, but style.css not found or failed.")
        deployer.disconnect()
        return False
    else:
        print("❌ Font fix deployment failed.")
        deployer.disconnect()
        return False
    
    print("❌ Header.php file not found in expected locations.")
    deployer.disconnect()
    return False

if __name__ == "__main__":
    deploy_font_fix()

