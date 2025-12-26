#!/usr/bin/env python3
"""
Remote GA4/Pixel Analytics Deployment Tool
===========================================

Deploys GA4/Pixel analytics code to remote WordPress sites via:
1. SSH + WP-CLI (preferred)
2. SFTP (fallback)
3. Manual instructions (if automated methods unavailable)

V2 Compliance | Author: Agent-3 | Date: 2025-12-25
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, Tuple
import subprocess
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Project root
project_root = Path(__file__).parent.parent


# Remote sites requiring deployment
REMOTE_SITES = {
    "dadudekc.com": {
        "site_url": "https://dadudekc.com",
        "theme_name": None,  # Will be detected
    },
    "crosbyultimateevents.com": {
        "site_url": "https://crosbyultimateevents.com",
        "theme_name": None,  # Will be detected
    }
}


def load_analytics_template() -> str:
    """Load the combined GA4/Pixel analytics template."""
    template_path = project_root / "agent_workspaces/Agent-5/GA4_PIXEL_CODE_TEMPLATES.md"
    
    if not template_path.exists():
        logger.error(f"❌ Template not found: {template_path}")
        return None
    
    # Read template and extract PHP code
    content = template_path.read_text(encoding='utf-8')
    
    # Find the "Combined Template" section
    combined_section_marker = "## Combined Template (GA4 + Pixel)"
    combined_start = content.find(combined_section_marker)
    
    if combined_start == -1:
        logger.error("❌ Combined Template section not found in template")
        return None
    
    # Extract the PHP code block within the Combined Template section
    # Look for ```php after the section marker
    section_content = content[combined_start:]
    start_marker = "```php"
    end_marker = "```"
    
    start_idx = section_content.find(start_marker)
    if start_idx == -1:
        logger.error("❌ PHP code block not found in Combined Template section")
        return None
    
    start_idx += len(start_marker)
    end_idx = section_content.find(end_marker, start_idx)
    if end_idx == -1:
        logger.error("❌ PHP code block not properly closed")
        return None
    
    php_code = section_content[start_idx:end_idx].strip()
    
    return php_code


def generate_analytics_code(site_name: str) -> str:
    """Generate analytics code for a specific site."""
    template = load_analytics_template()
    if not template:
        return None
    
    # Replace placeholders
    code = template.replace("{SITE_NAME}", site_name)
    
    return code


def check_ssh_access(host: str, username: str = None) -> bool:
    """Check if SSH access is available."""
    try:
        # Test SSH connection
        ssh_cmd = ["ssh", "-o", "ConnectTimeout=5", "-o", "BatchMode=yes"]
        if username:
            ssh_cmd.extend([f"{username}@{host}"])
        else:
            ssh_cmd.append(host)
        ssh_cmd.append("echo 'SSH_OK'")
        
        result = subprocess.run(
            ssh_cmd,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        return result.returncode == 0 and "SSH_OK" in result.stdout
    except Exception as e:
        logger.debug(f"SSH check failed: {e}")
        return False


def check_wp_cli_available(host: str, wp_path: str, username: str = None) -> bool:
    """Check if WP-CLI is available on remote server."""
    try:
        ssh_cmd = ["ssh"]
        if username:
            ssh_cmd.append(f"{username}@{host}")
        else:
            ssh_cmd.append(host)
        
        ssh_cmd.append(f"cd {wp_path} && wp --info")
        
        result = subprocess.run(
            ssh_cmd,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        return result.returncode == 0
    except Exception as e:
        logger.debug(f"WP-CLI check failed: {e}")
        return False


def get_active_theme(host: str, wp_path: str, username: str = None) -> Optional[str]:
    """Get the active WordPress theme name."""
    try:
        ssh_cmd = ["ssh"]
        if username:
            ssh_cmd.append(f"{username}@{host}")
        else:
            ssh_cmd.append(host)
        
        ssh_cmd.append(f"cd {wp_path} && wp theme list --status=active --field=name --format=json")
        
        result = subprocess.run(
            ssh_cmd,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            theme_name = result.stdout.strip().strip('"')
            return theme_name
        
        return None
    except Exception as e:
        logger.error(f"Failed to get active theme: {e}")
        return None


def deploy_via_ssh_wpcli(
    site_name: str,
    host: str,
    wp_path: str,
    analytics_code: str,
    username: str = None
) -> Tuple[bool, str]:
    """Deploy analytics code via SSH + WP-CLI."""
    logger.info(f"📦 Deploying via SSH + WP-CLI to {site_name}...")
    
    try:
        # Get active theme
        theme_name = get_active_theme(host, wp_path, username)
        if not theme_name:
            return False, "Could not determine active theme"
        
        theme_path = f"{wp_path}/wp-content/themes/{theme_name}"
        functions_file = f"{theme_path}/functions.php"
        
        # Create backup
        backup_cmd = ["ssh"]
        if username:
            backup_cmd.append(f"{username}@{host}")
        else:
            backup_cmd.append(host)
        backup_cmd.append(
            f"cp {functions_file} {functions_file}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
        
        result = subprocess.run(backup_cmd, capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            logger.warning(f"⚠️  Backup failed (continuing anyway): {result.stderr}")
        
        # Check if analytics function already exists
        check_cmd = ["ssh"]
        if username:
            check_cmd.append(f"{username}@{host}")
        else:
            check_cmd.append(host)
        check_cmd.append(f"grep -q 'function add_analytics_tracking' {functions_file} && echo 'EXISTS' || echo 'NOT_EXISTS'")
        
        result = subprocess.run(check_cmd, capture_output=True, text=True, timeout=10)
        if result.returncode == 0 and "EXISTS" in result.stdout:
            logger.info(f"   ⏭️  Analytics function already exists, skipping")
            return True, "Analytics function already exists"
        
        # Append analytics code to functions.php
        # Use heredoc to safely append code
        append_cmd = f"""
cat >> {functions_file} << 'ANALYTICS_EOF'

{analytics_code}
ANALYTICS_EOF
"""
        
        ssh_cmd = ["ssh"]
        if username:
            ssh_cmd.append(f"{username}@{host}")
        else:
            ssh_cmd.append(host)
        ssh_cmd.append(append_cmd)
        
        result = subprocess.run(ssh_cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            return False, f"Failed to append code: {result.stderr}"
        
        logger.info(f"   ✅ Analytics code deployed to {site_name}")
        return True, "Deployed successfully"
        
    except Exception as e:
        logger.error(f"❌ SSH/WP-CLI deployment failed: {e}")
        return False, str(e)


def generate_manual_instructions(site_name: str, site_url: str, analytics_code: str) -> str:
    """Generate manual deployment instructions."""
    instructions = f"""
# Manual Deployment Instructions for {site_name}

## Option 1: WordPress Admin → Appearance → Theme Editor
1. Log in to WordPress admin: {site_url}/wp-admin
2. Navigate to: Appearance → Theme Editor
3. Select: functions.php (from active theme)
4. Scroll to the end of the file
5. Paste the following code:

```php
{analytics_code}
```

6. Click "Update File"
7. Verify: Check page source for analytics scripts

## Option 2: SFTP/File Manager
1. Connect to your hosting via SFTP or File Manager
2. Navigate to: wp-content/themes/{site_name or '[ACTIVE_THEME]'}/functions.php
3. Download functions.php (backup first!)
4. Open in text editor
5. Paste the analytics code at the end (before closing ?> if present)
6. Upload the modified functions.php
7. Verify: Check page source for analytics scripts

## Option 3: Hosting Control Panel File Manager
1. Log in to hosting control panel (cPanel, etc.)
2. Open File Manager
3. Navigate to: public_html/wp-content/themes/[ACTIVE_THEME]/functions.php
4. Edit the file
5. Paste analytics code at the end
6. Save and verify

## Analytics Code to Deploy:
```php
{analytics_code}
```

## Configuration Required:
After deployment, add these lines to wp-config.php (before "That's all, stop editing!"):
```php
define('GA4_MEASUREMENT_ID', 'G-XXXXXXXXXX');
define('FACEBOOK_PIXEL_ID', '123456789012345');
```

Replace the IDs with your actual GA4 Measurement ID and Facebook Pixel ID.
"""
    return instructions


def deploy_to_remote_site(
    site_name: str,
    site_config: Dict,
    credentials: Dict = None
) -> Dict:
    """Deploy analytics code to a remote WordPress site."""
    logger.info(f"\n🚀 Deploying GA4/Pixel analytics to {site_name}...")
    
    result = {
        "site": site_name,
        "site_url": site_config["site_url"],
        "status": "pending",
        "method": None,
        "message": "",
        "timestamp": datetime.now().isoformat()
    }
    
    # Generate analytics code
    analytics_code = generate_analytics_code(site_name)
    if not analytics_code:
        result["status"] = "error"
        result["message"] = "Failed to load analytics template"
        return result
    
    # Check credentials availability
    if not credentials:
        # Generate manual instructions
        instructions = generate_manual_instructions(
            site_name,
            site_config["site_url"],
            analytics_code
        )
        
        # Save instructions
        instructions_path = project_root / f"docs/website_audits/2026/{site_name}_MANUAL_DEPLOYMENT_INSTRUCTIONS.md"
        instructions_path.parent.mkdir(parents=True, exist_ok=True)
        instructions_path.write_text(instructions, encoding='utf-8')
        
        result["status"] = "manual_required"
        result["message"] = "No credentials provided - manual deployment required"
        result["instructions_file"] = str(instructions_path)
        logger.info(f"   ⚠️  Manual deployment instructions saved to: {instructions_path}")
        return result
    
    # Extract credentials
    host = credentials.get("host") or site_name
    username = credentials.get("username")
    wp_path = credentials.get("wp_path", "/var/www/html")
    
    # Try SSH + WP-CLI deployment
    if credentials.get("ssh_available", False):
        success, message = deploy_via_ssh_wpcli(
            site_name,
            host,
            wp_path,
            analytics_code,
            username
        )
        
        if success:
            result["status"] = "success"
            result["method"] = "ssh_wpcli"
            result["message"] = message
            return result
        else:
            logger.warning(f"   ⚠️  SSH/WP-CLI deployment failed: {message}")
    
    # Fallback to manual instructions
    instructions = generate_manual_instructions(
        site_name,
        site_config["site_url"],
        analytics_code
    )
    
    instructions_path = project_root / f"docs/website_audits/2026/{site_name}_MANUAL_DEPLOYMENT_INSTRUCTIONS.md"
    instructions_path.parent.mkdir(parents=True, exist_ok=True)
    instructions_path.write_text(instructions, encoding='utf-8')
    
    result["status"] = "manual_required"
    result["message"] = "Automated deployment not available - manual deployment required"
    result["instructions_file"] = str(instructions_path)
    logger.info(f"   ⚠️  Manual deployment instructions saved to: {instructions_path}")
    
    return result


def load_credentials() -> Dict:
    """Load remote deployment credentials."""
    # Try environment variables
    import os
    creds = {}
    
    # Try config file
    config_paths = [
        Path("D:/websites/configs/remote_deployment_credentials.json"),
        Path("D:/websites/.deploy_credentials/remote_wordpress.json"),
        project_root / "config/remote_deployment_credentials.json"
    ]
    
    for config_path in config_paths:
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    creds = json.load(f)
                    logger.info(f"✅ Loaded credentials from: {config_path}")
                    return creds
            except Exception as e:
                logger.debug(f"Failed to load {config_path}: {e}")
    
    return {}


def main():
    """Main execution."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Deploy GA4/Pixel analytics to remote WordPress sites"
    )
    parser.add_argument(
        "--site",
        choices=list(REMOTE_SITES.keys()),
        help="Deploy to specific site only"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Generate deployment instructions without deploying"
    )
    parser.add_argument(
        "--credentials",
        type=Path,
        help="Path to credentials JSON file"
    )
    
    args = parser.parse_args()
    
    # Load credentials
    if args.credentials:
        with open(args.credentials, 'r', encoding='utf-8') as f:
            credentials = json.load(f)
    else:
        credentials = load_credentials()
    
    # Determine sites to deploy
    sites_to_deploy = [args.site] if args.site else list(REMOTE_SITES.keys())
    
    # Deploy to each site
    results = []
    for site_name in sites_to_deploy:
        site_config = REMOTE_SITES[site_name]
        site_creds = credentials.get(site_name, {})
        
        if args.dry_run:
            logger.info(f"\n🔍 DRY RUN: Would deploy to {site_name}")
            analytics_code = generate_analytics_code(site_name)
            if analytics_code:
                instructions = generate_manual_instructions(
                    site_name,
                    site_config["site_url"],
                    analytics_code
                )
                instructions_path = project_root / f"docs/website_audits/2026/{site_name}_MANUAL_DEPLOYMENT_INSTRUCTIONS.md"
                instructions_path.parent.mkdir(parents=True, exist_ok=True)
                instructions_path.write_text(instructions, encoding='utf-8')
                logger.info(f"   ✅ Instructions generated: {instructions_path}")
        else:
            result = deploy_to_remote_site(site_name, site_config, site_creds)
            results.append(result)
    
    if not args.dry_run:
        # Generate report
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_sites": len(results),
            "success": sum(1 for r in results if r["status"] == "success"),
            "manual_required": sum(1 for r in results if r["status"] == "manual_required"),
            "errors": sum(1 for r in results if r["status"] == "error"),
            "sites": results
        }
        
        reports_dir = project_root / "reports"
        reports_dir.mkdir(exist_ok=True)
        report_file = reports_dir / f"ga4_pixel_remote_deployment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_file.write_text(json.dumps(report, indent=2), encoding='utf-8')
        
        logger.info(f"\n📊 Deployment report: {report_file}")
        
        # Summary
        logger.info("\n📋 Deployment Summary:")
        for result in results:
            status_icon = "✅" if result["status"] == "success" else "⚠️" if result["status"] == "manual_required" else "❌"
            logger.info(f"   {status_icon} {result['site']}: {result['status']} - {result['message']}")


if __name__ == "__main__":
    main()

