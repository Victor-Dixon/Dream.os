#!/usr/bin/env python3
"""
Verify FastAPI Service Status Remotely
=======================================

Verifies FastAPI service is running and healthy on remote server.

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
HEALTH_ENDPOINT = "http://localhost:8001/health"


def verify_service_status():
    """Verify FastAPI service is running and healthy."""
    print("🔍 TradingRobotPlug FastAPI Service Verification\n")
    
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
    
    # Check 1: Service is enabled
    print("📋 Checking systemd service status...")
    check_service_cmd = f"systemctl is-enabled {SERVICE_NAME} 2>/dev/null || echo 'not_enabled'"
    result = deployer.execute_command(check_service_cmd)
    if "enabled" in result.lower():
        print(f"✅ Service is enabled")
    elif "not_enabled" in result or "not found" in result.lower():
        print(f"⚠️  Service not enabled or not found")
        print(f"   Run: sudo systemctl enable {SERVICE_NAME}")
    else:
        print(f"⚠️  Service status unclear: {result}")
    
    # Check 2: Service is active
    print(f"\n📋 Checking if service is running...")
    check_active_cmd = f"systemctl is-active {SERVICE_NAME} 2>/dev/null || echo 'inactive'"
    result = deployer.execute_command(check_active_cmd)
    if "active" in result.lower():
        print(f"✅ Service is running")
    else:
        print(f"⚠️  Service is not running: {result}")
        print(f"   Run: sudo systemctl start {SERVICE_NAME}")
        return False
    
    # Check 3: Health endpoint
    print(f"\n🏥 Checking health endpoint...")
    check_health_cmd = f"curl -s -o /dev/null -w '%{{http_code}}' {HEALTH_ENDPOINT} 2>/dev/null || echo '000'"
    result = deployer.execute_command(check_health_cmd)
    if "200" in result:
        print(f"✅ Health endpoint responding (HTTP 200)")
        
        # Get health response
        get_health_cmd = f"curl -s {HEALTH_ENDPOINT}"
        health_response = deployer.execute_command(get_health_cmd)
        print(f"\n📊 Health Response:")
        print(health_response)
        return True
    else:
        print(f"⚠️  Health endpoint not responding: HTTP {result}")
        print(f"   Service may still be starting...")
        return False
    
    return True


if __name__ == "__main__":
    success = verify_service_status()
    sys.exit(0 if success else 1)

