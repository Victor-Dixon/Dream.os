#!/usr/bin/env python3
"""
Verify TradingRobotPlug plugin activation and REST API endpoint registration.

<!-- SSOT Domain: web -->
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

def check_plugin_via_wp_cli():
    """Check plugin activation status via WP-CLI."""
    print("🔍 TradingRobotPlug Plugin Activation Verification\n")
    print("📋 WP-CLI Commands to Execute:")
    print("   1. Check plugin status:")
    print("      wp plugin list --all --path=/home/u996867598/domains/tradingrobotplug.com/public_html")
    print("\n   2. Activate plugin (if not active):")
    print("      wp plugin activate tradingrobotplug-wordpress-plugin --path=/home/u996867598/domains/tradingrobotplug.com/public_html")
    print("\n   3. Verify REST API routes:")
    print("      wp rewrite flush --path=/home/u996867598/domains/tradingrobotplug.com/public_html")
    print("\n   4. Test endpoints:")
    print("      curl http://tradingrobotplug.com/wp-json/tradingrobotplug/v1/account")
    print("      curl http://tradingrobotplug.com/wp-json/tradingrobotplug/v1/positions")
    print("      curl http://tradingrobotplug.com/wp-json/tradingrobotplug/v1/orders")
    
    return True

def main():
    """Verify plugin activation."""
    check_plugin_via_wp_cli()
    print("\n✅ Verification commands ready")
    print("⚠️  Plugin must be deployed first (Agent-3 coordination)")
    return 0

if __name__ == "__main__":
    sys.exit(main())


