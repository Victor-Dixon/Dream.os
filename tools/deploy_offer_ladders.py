#!/usr/bin/env python3
"""
Deploy Offer Ladder content to WordPress sites.

This tool creates offer ladder content for each revenue site based on the
defined offer structures in the documentation.

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
    from mcp_servers.website_manager_server import create_offer_ladder_content, _get_deployer
    HAS_MCP = True
except ImportError:
    HAS_MCP = False

# Offer Ladder Content Definitions
OFFER_LADDERS = {
    "freerideinvestor.com": [
        {
            "title": "Free Trading Education",
            "content": "Access our free trading education library with basic strategies, market analysis, and educational resources to get started.",
            "tier": "free",
            "pricing": "Free"
        },
        {
            "title": "Premium Trading Signals",
            "content": "Get daily trading signals with entry/exit points, risk management guidelines, and performance tracking.",
            "tier": "core",
            "pricing": "$97/month"
        },
        {
            "title": "Elite Trading Mastery",
            "content": "Complete trading system with automated execution, advanced analytics, and personal coaching sessions.",
            "tier": "premium",
            "pricing": "$497/month"
        },
        {
            "title": "Institutional Trading Suite",
            "content": "Full-service trading management with custom strategies, dedicated account manager, and institutional-grade tools.",
            "tier": "enterprise",
            "pricing": "Custom pricing"
        }
    ],
    "dadudekc.com": [
        {
            "title": "Free Business Resources",
            "content": "Access our free library of business templates, checklists, and educational content for entrepreneurs.",
            "tier": "free",
            "pricing": "Free"
        },
        {
            "title": "Business Automation Tools",
            "content": "Essential automation tools and templates to streamline your business operations and save time.",
            "tier": "core",
            "pricing": "$197/month"
        },
        {
            "title": "Complete Business System",
            "content": "End-to-end business management system with custom automation, reporting dashboards, and consulting support.",
            "tier": "premium",
            "pricing": "$497/month"
        },
        {
            "title": "Enterprise Solutions",
            "content": "Custom enterprise-grade solutions with dedicated development, training, and 24/7 support.",
            "tier": "enterprise",
            "pricing": "Custom pricing"
        }
    ],
    "crosbyultimateevents.com": [
        {
            "title": "Free Event Planning Guide",
            "content": "Download our comprehensive event planning checklist and basic templates for your next event.",
            "tier": "free",
            "pricing": "Free"
        },
        {
            "title": "Event Planning Package",
            "content": "Complete event planning package with vendor coordination, timeline management, and execution support.",
            "tier": "core",
            "pricing": "$497/event"
        },
        {
            "title": "Premium Event Management",
            "content": "Full-service event management with dedicated coordinator, premium vendor network, and post-event analysis.",
            "tier": "premium",
            "pricing": "$1,497/event"
        },
        {
            "title": "Enterprise Event Solutions",
            "content": "Custom enterprise event solutions with multi-event coordination, brand integration, and strategic consulting.",
            "tier": "enterprise",
            "pricing": "Custom pricing"
        }
    ],
    "tradingrobotplug.com": [
        {
            "title": "Free Strategy Backtests",
            "content": "Access our library of free strategy backtests and basic trading algorithm demonstrations.",
            "tier": "free",
            "pricing": "Free"
        },
        {
            "title": "Automated Trading Bot",
            "content": "Deploy our proven automated trading algorithms with 24/7 execution and basic performance monitoring.",
            "tier": "core",
            "pricing": "$297/month"
        },
        {
            "title": "Advanced Trading System",
            "content": "Complete automated trading system with custom strategies, advanced analytics, and optimization tools.",
            "tier": "premium",
            "pricing": "$797/month"
        },
        {
            "title": "Institutional Trading Platform",
            "content": "Enterprise-grade trading platform with custom development, institutional connectivity, and dedicated support.",
            "tier": "enterprise",
            "pricing": "Custom pricing"
        }
    ]
}

def deploy_offer_ladder(site_key: str, offers: List[Dict[str, str]]) -> Dict[str, any]:
    """Deploy offer ladder content to a specific site."""
    if not HAS_MCP:
        return {"success": False, "error": "MCP website manager not available"}

    from mcp_servers.website_manager_server import _get_deployer, _execute_wp_cli

    deployer = _get_deployer(site_key)
    if not deployer:
        return {"success": False, "error": "Deployer not available", "site": site_key}

    if not deployer.connect():
        return {"success": False, "error": "Failed to connect to server", "site": site_key}

    results = []
    wordpress_path = "public_html"  # Common cPanel path

    for offer in offers:
        try:
            # Create the post using WP-CLI
            title = offer["title"].replace("'", "\\'")
            content = offer["content"].replace("'", "\\'")

            cmd = f"wp post create --post_type=offer_ladder --post_title='{title}' --post_content='{content}' --post_status=publish --porcelain --path={wordpress_path}"
            result = _execute_wp_cli(site_key, cmd)

            if result["success"]:
                post_id = result["output"].strip()

                # Set meta fields using WP-CLI
                meta_results = []

                if offer.get("tier"):
                    tier_cmd = f"wp post meta update {post_id} offer_tier '{offer['tier']}' --path={wordpress_path}"
                    meta_result = _execute_wp_cli(site_key, tier_cmd)
                    meta_results.append(meta_result["success"])

                if offer.get("pricing"):
                    pricing = offer['pricing'].replace("'", "\\'")
                    pricing_cmd = f"wp post meta update {post_id} pricing '{pricing}' --path={wordpress_path}"
                    meta_result = _execute_wp_cli(site_key, pricing_cmd)
                    meta_results.append(meta_result["success"])

                all_meta_success = all(meta_results)

                results.append({
                    "title": offer["title"],
                    "success": True,
                    "post_id": post_id,
                    "meta_success": all_meta_success
                })
            else:
                results.append({
                    "title": offer["title"],
                    "success": False,
                    "error": f"WP-CLI failed: {result.get('output', 'No output')}"
                })

        except Exception as e:
            results.append({
                "title": offer["title"],
                "success": False,
                "error": str(e)
            })

    deployer.disconnect()

    successful = sum(1 for r in results if r["success"])
    total = len(results)

    return {
        "success": successful == total,
        "site": site_key,
        "results": results,
        "successful": successful,
        "total": total
    }

def check_offer_ladder_cpt_exists(site_key: str) -> bool:
    """Check if offer_ladder custom post type exists on the site."""
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
        result = _execute_wp_cli(site_key, "post-type list --name=offer_ladder --format=json")

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
    print("🚀 Deploying Offer Ladder Content to Revenue Sites")
    print("=" * 50)

    results = {}

    for site_key, offers in OFFER_LADDERS.items():
        print(f"\n📍 Processing {site_key}...")

        # Check if CPT exists first (skip for now)
        # if not check_offer_ladder_cpt_exists(site_key):
        #     print(f"❌ Offer Ladder Custom Post Type not found on {site_key}")
        #     print("   Run deploy_offer_ladder_post_types.py first to create the CPT infrastructure")
        #     results[site_key] = {"success": False, "error": "CPT not found"}
        #     continue

        # Deploy offer ladder content
        result = deploy_offer_ladder(site_key, offers)

        if result["success"]:
            print(f"✅ Offer ladder deployed successfully ({result['successful']}/{result['total']} offers)")
            for offer_result in result["results"]:
                status = "✅" if offer_result["success"] else "❌"
                print(f"   {status} {offer_result['title']}")
        else:
            print(f"❌ Failed to deploy offer ladder ({result['successful']}/{result['total']} offers)")
            for offer_result in result["results"]:
                if not offer_result["success"]:
                    print(f"   ❌ {offer_result['title']}: {offer_result.get('error', 'Unknown error')}")

        results[site_key] = result

    # Summary
    print("\n" + "=" * 50)
    print("📊 DEPLOYMENT SUMMARY")

    total_sites = len(results)
    successful_sites = sum(1 for r in results.values() if r["success"])

    for site_key, result in results.items():
        status = "✅" if result["success"] else "❌"
        if result["success"]:
            successful_offers = result.get("successful", 0)
            total_offers = result.get("total", 0)
            print(f"{status} {site_key}: {successful_offers}/{total_offers} offers")
        else:
            error_msg = result.get("error", "Unknown error")
            print(f"{status} {site_key}: {error_msg}")

    print(f"\nTotal: {total_sites} sites")
    print(f"Successful: {successful_sites}")
    print(f"Failed: {total_sites - successful_sites}")

    if successful_sites > 0:
        print("\n💡 Next Steps:")
        print("1. Verify offer ladders are accessible at /wp-json/wp/v2/offer_ladder")
        print("2. Test that offers appear in WordPress admin")
        print("3. Update pricing pages to display offer ladder content")

    return successful_sites == total_sites

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)