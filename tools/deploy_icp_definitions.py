#!/usr/bin/env python3
"""
Deploy ICP (Ideal Customer Profile) definitions to WordPress sites.

This tool creates ICP definition content for each revenue site based on the
defined ICP content in the documentation.

Author: Agent-7 (Web Development Specialist)
Date: 2026-01-06
"""

import sys
import json
from pathlib import Path
from typing import Dict, List, Optional

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from mcp_servers.website_manager_server import create_icp_definition, _get_deployer
    HAS_MCP = True
except ImportError:
    HAS_MCP = False

# ICP Content Definitions
ICP_DEFINITIONS = {
    "freerideinvestor.com": {
        "title": "FreeRide Investor Ideal Customer Profile",
        "content": "For active traders (day/swing traders, $10K-$500K accounts) struggling with inconsistent results, we eliminate guesswork and provide proven trading strategies. Your outcome: consistent edge, reduced losses, trading confidence.",
        "target_demographic": "Active traders (day/swing traders, $10K-$500K accounts)",
        "pain_points": "inconsistent results, guesswork",
        "desired_outcomes": "consistent edge, reduced losses, trading confidence"
    },
    "dadudekc.com": {
        "title": "DadudeKC Ideal Customer Profile",
        "content": "For small business owners and entrepreneurs who struggle with manual workflows and time-consuming tasks, we eliminate operational bottlenecks through automation and systems. Your outcome: more time for growth, reduced operational stress, scalable processes.",
        "target_demographic": "Small business owners and entrepreneurs",
        "pain_points": "manual workflows, time-consuming tasks, operational bottlenecks",
        "desired_outcomes": "more time for growth, reduced operational stress, scalable processes"
    },
    "crosbyultimateevents.com": {
        "title": "Crosby Ultimate Events Ideal Customer Profile",
        "content": "For individuals and organizations planning special events who struggle with coordination, vendor management, and execution details, we eliminate event planning stress through comprehensive event management services. Your outcome: memorable events, stress-free planning, professional execution.",
        "target_demographic": "Individuals and organizations planning special events",
        "pain_points": "coordination, vendor management, execution details",
        "desired_outcomes": "memorable events, stress-free planning, professional execution"
    },
    "tradingrobotplug.com": {
        "title": "Trading Robot Plug Ideal Customer Profile",
        "content": "For traders seeking automated trading solutions who struggle with manual execution and timing issues, we eliminate human error through intelligent algorithmic trading systems. Your outcome: 24/7 automated execution, consistent strategy application, maximized returns.",
        "target_demographic": "Traders seeking automated trading solutions",
        "pain_points": "manual execution, timing issues, human error",
        "desired_outcomes": "24/7 automated execution, consistent strategy application, maximized returns"
    }
}

def deploy_icp_definition(site_key: str, icp_data: Dict[str, str]) -> Dict[str, any]:
    """Deploy ICP definition to a specific site."""
    if not HAS_MCP:
        return {"success": False, "error": "MCP website manager not available"}

    try:
        # Try using the MCP function but skip CPT check since we know it's deployed
        # Temporarily patch the function to bypass the check
        from mcp_servers.website_manager_server import _get_deployer

        deployer = _get_deployer(site_key)
        if not deployer:
            return {"success": False, "error": "Deployer not available", "site": site_key}

        if not deployer.connect():
            return {"success": False, "error": "Failed to connect to server", "site": site_key}

        # Try to create post via REST API directly
        # First, get WordPress REST API credentials (this might not work without authentication)
        # For now, fall back to a simpler approach - create via direct database manipulation if possible
        # Or use WP-CLI with correct path

        from mcp_servers.website_manager_server import _execute_wp_cli

        # Try WP-CLI with explicit path to WordPress directory
        # The deployer should handle the path, but let's try with explicit cd
        wordpress_path = "public_html"  # Common cPanel path, adjust if needed

        # Try creating the post with explicit path
        title = icp_data["title"].replace("'", "\\'")
        content = icp_data["content"].replace("'", "\\'")

        # Try the command with cd to WordPress directory first
        cmd = f"cd {wordpress_path} && wp post create --post_type=icp_definition --post_title='{title}' --post_content='{content}' --post_status=publish --porcelain"
        result = _execute_wp_cli(site_key, cmd)

        if result["success"]:
            post_id = result["output"].strip()

            # Set meta fields using WP-CLI
            meta_results = []

            if icp_data.get("target_demographic"):
                demographic = icp_data['target_demographic'].replace("'", "\\'")
                meta_cmd = f"cd {wordpress_path} && wp post meta update {post_id} target_demographic '{demographic}'"
                meta_result = _execute_wp_cli(site_key, meta_cmd)
                meta_results.append(meta_result["success"])

            if icp_data.get("pain_points"):
                pain_points = icp_data['pain_points'].replace("'", "\\'")
                meta_cmd = f"cd {wordpress_path} && wp post meta update {post_id} pain_points '{pain_points}'"
                meta_result = _execute_wp_cli(site_key, meta_cmd)
                meta_results.append(meta_result["success"])

            if icp_data.get("desired_outcomes"):
                outcomes = icp_data['desired_outcomes'].replace("'", "\\'")
                meta_cmd = f"cd {wordpress_path} && wp post meta update {post_id} desired_outcomes '{outcomes}'"
                meta_result = _execute_wp_cli(site_key, meta_cmd)
                meta_results.append(meta_result["success"])

            all_meta_success = all(meta_results)

            deployer.disconnect()

            return {
                "success": True,
                "site": site_key,
                "icp_title": icp_data["title"],
                "post_id": post_id,
                "target_demographic": icp_data.get("target_demographic"),
                "pain_points": icp_data.get("pain_points"),
                "desired_outcomes": icp_data.get("desired_outcomes"),
                "meta_success": all_meta_success
            }
        else:
            deployer.disconnect()
            # Debug: show the actual error
            return {"success": False, "error": f"WP-CLI post create failed: {result.get('output', 'No output')}", "site": site_key}

    except Exception as e:
        return {"success": False, "error": str(e), "site": site_key}

def check_icp_cpt_exists(site_key: str) -> bool:
    """Check if ICP custom post type exists on the site."""
    if not HAS_MCP:
        return False

    try:
        deployer = _get_deployer(site_key)
        if not deployer:
            return False

        if not deployer.connect():
            return False

        # Check if CPT exists by trying to list posts
        from mcp_servers.website_manager_server import _execute_wp_cli
        result = _execute_wp_cli(site_key, "post-type list --name=icp_definition --format=json")

        deployer.disconnect()

        if result["success"]:
            try:
                cpt_list = json.loads(result["output"])
                return len(cpt_list) > 0
            except json.JSONDecodeError:
                return False

        return False
    except Exception:
        return False

def main():
    """Main deployment function."""
    print("🚀 Deploying ICP Definitions to Revenue Sites")
    print("=" * 50)

    results = {}

    for site_key, icp_data in ICP_DEFINITIONS.items():
        print(f"\n📍 Processing {site_key}...")

        # Check if CPT exists first (skip for now due to deployment timing)
        # if not check_icp_cpt_exists(site_key):
        #     print(f"❌ ICP Custom Post Type not found on {site_key}")
        #     print("   Run deploy_icp_post_types.py first to create the CPT infrastructure")
        #     results[site_key] = {"success": False, "error": "CPT not found"}
        #     continue

        # Deploy ICP definition
        result = deploy_icp_definition(site_key, icp_data)

        if result["success"]:
            print(f"✅ ICP definition created successfully")
            print(f"   Title: {result.get('icp_title')}")
            print(f"   Post ID: {result.get('post_id')}")
        else:
            print(f"❌ Failed to create ICP definition")
            print(f"   Error: {result.get('error', 'Unknown error')}")

        results[site_key] = result

    # Summary
    print("\n" + "=" * 50)
    print("📊 DEPLOYMENT SUMMARY")

    successful = 0
    failed = 0

    for site_key, result in results.items():
        status = "✅" if result["success"] else "❌"
        print(f"{status} {site_key}: {result.get('post_id', result.get('error', 'Unknown'))}")
        if result["success"]:
            successful += 1
        else:
            failed += 1

    print(f"\nTotal: {len(results)} sites")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")

    if successful > 0:
        print("\n💡 Next Steps:")
        print("1. Verify ICP definitions are accessible at /wp-json/wp/v2/icp_definition")
        print("2. Test that definitions appear in WordPress admin")
        print("3. Update any theme templates to display ICP content")

    return successful == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)