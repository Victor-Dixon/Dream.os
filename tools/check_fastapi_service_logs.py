#!/usr/bin/env python3
"""
Check FastAPI Service Logs
===========================

Checks systemd service logs for FastAPI service.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-12-31
"""

import sys
from pathlib import Path

# Add ops/deployment to path for SimpleWordPressDeployer
repo_root = Path(__file__).parent.parent
websites_root = Path("D:/websites")
if (repo_root / "websites" / "ops" / "deployment" / "simple_wordpress_deployer.py").exists():
    sys.path.insert(0, str(repo_root / "websites" / "ops" / "deployment"))
elif (websites_root / "ops" / "deployment" / "simple_wordpress_deployer.py").exists():
    sys.path.insert(0, str(websites_root / "ops" / "deployment"))
else:
    print("❌ Could not find simple_wordpress_deployer.py")
    sys.exit(1)

from simple_wordpress_deployer import SimpleWordPressDeployer, load_site_configs

SITE_KEY = "tradingrobotplug.com"
SERVICE_NAME = "tradingrobotplug-fastapi"


def check_service_logs():
    """Check FastAPI service logs."""
    print("📋 TradingRobotPlug FastAPI Service Logs\n")
    
    site_configs = load_site_configs()
    try:
        deployer = SimpleWordPressDeployer(SITE_KEY, site_configs)
    except Exception as e:
        print(f"❌ Failed to initialize deployer: {e}")
        return False
    
    if not deployer.connect():
        print("❌ Failed to connect to server")
        return False
    print(f"✅ Connected to {SITE_KEY}\n")
    
    # Get recent logs (last 50 lines)
    print("📋 Fetching recent service logs...")
    log_cmd = f"journalctl -u {SERVICE_NAME} -n 50 --no-pager 2>/dev/null || echo 'Logs unavailable'"
    logs = deployer.execute_command(log_cmd)
    
    if "Logs unavailable" in logs:
        print("⚠️  Could not access service logs (may require sudo)")
        print("   Run manually: sudo journalctl -u tradingrobotplug-fastapi -n 50")
    else:
        print("📋 Recent Service Logs:")
        print("=" * 70)
        print(logs)
        print("=" * 70)
    
    # Check service status details
    print(f"\n📋 Service Status Details:")
    status_cmd = f"systemctl status {SERVICE_NAME} --no-pager -l 2>/dev/null || echo 'Status unavailable'"
    status = deployer.execute_command(status_cmd)
    print(status)
    
    return True


if __name__ == "__main__":
    check_service_logs()

