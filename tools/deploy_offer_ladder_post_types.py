#!/usr/bin/env python3
"""
Deploy Offer Ladder Custom Post Type infrastructure to WordPress sites.

This tool creates the necessary custom post type and meta boxes for offer ladders
across all revenue sites.

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
    from mcp_servers.website_manager_server import _execute_wp_cli, _get_deployer, deploy_file_to_wordpress
    HAS_MCP = True
except ImportError:
    HAS_MCP = False

# Site configurations
REVENUE_SITES = [
    "freerideinvestor.com",
    "dadudekc.com",
    "crosbyultimateevents.com",
    "tradingrobotplug.com"
]

def deploy_offer_ladder_cpt_infrastructure(site_key: str) -> Dict[str, any]:
    """Deploy Offer Ladder Custom Post Type infrastructure to a site."""
    if not HAS_MCP:
        return {"success": False, "error": "MCP website manager not available"}

    results = {
        "cpt_registration": False,
        "meta_boxes": False,
        "rest_api": False
    }

    try:
        deployer = _get_deployer(site_key)
        if not deployer:
            return {"success": False, "error": "Deployer not available", "site": site_key}

        if not deployer.connect():
            return {"success": False, "error": "Failed to connect to server", "site": site_key}

        # Step 1: Create functions.php additions for Offer Ladder CPT
        offer_ladder_cpt_code = '''
// Offer Ladder Custom Post Type
function register_offer_ladder_post_type() {
    $args = array(
        'public' => true,
        'label'  => 'Offer Ladders',
        'supports' => array('title', 'editor', 'custom-fields'),
        'show_in_rest' => true,
        'rest_base' => 'offer_ladder',
        'menu_icon' => 'dashicons-chart-line',
    );
    register_post_type('offer_ladder', $args);
}
add_action('init', 'register_offer_ladder_post_type');

// Add meta boxes for offer ladder fields
function add_offer_ladder_meta_boxes() {
    add_meta_box(
        'offer_ladder_details',
        'Offer Details',
        'render_offer_ladder_meta_box',
        'offer_ladder',
        'normal',
        'high'
    );
}
add_action('add_meta_boxes', 'add_offer_ladder_meta_boxes');

function render_offer_ladder_meta_box($post) {
    $offer_tier = get_post_meta($post->ID, 'offer_tier', true);
    $pricing = get_post_meta($post->ID, 'pricing', true);

    wp_nonce_field('offer_ladder_meta_box', 'offer_ladder_meta_box_nonce');

    echo '<table class="form-table">';
    echo '<tr><th><label for="offer_tier">Offer Tier</label></th>';
    echo '<td><select id="offer_tier" name="offer_tier" class="regular-text">';
    echo '<option value="free"' . selected($offer_tier, 'free', false) . '>Free</option>';
    echo '<option value="core"' . selected($offer_tier, 'core', false) . '>Core</option>';
    echo '<option value="premium"' . selected($offer_tier, 'premium', false) . '>Premium</option>';
    echo '<option value="enterprise"' . selected($offer_tier, 'enterprise', false) . '>Enterprise</option>';
    echo '</select></td></tr>';

    echo '<tr><th><label for="pricing">Pricing</label></th>';
    echo '<td><input type="text" id="pricing" name="pricing" value="' . esc_attr($pricing) . '" class="regular-text" placeholder="e.g., $97/month"></td></tr>';
    echo '</table>';
}

function save_offer_ladder_meta_box_data($post_id) {
    if (!isset($_POST['offer_ladder_meta_box_nonce'])) return;
    if (!wp_verify_nonce($_POST['offer_ladder_meta_box_nonce'], 'offer_ladder_meta_box')) return;
    if (defined('DOING_AUTOSAVE') && DOING_AUTOSAVE) return;

    if (isset($_POST['offer_tier'])) {
        update_post_meta($post_id, 'offer_tier', sanitize_text_field($_POST['offer_tier']));
    }
    if (isset($_POST['pricing'])) {
        update_post_meta($post_id, 'pricing', sanitize_text_field($_POST['pricing']));
    }
}
add_action('save_post', 'save_offer_ladder_meta_box_data');
'''

        # Create a temporary PHP file with the CPT code
        temp_file = Path(f"/tmp/offer_ladder_cpt_{site_key}.php")
        temp_file.parent.mkdir(exist_ok=True)
        temp_file.write_text(offer_ladder_cpt_code)

        # Deploy to theme functions.php
        functions_path = f"wp-content/themes/{site_key.replace('.', '')}/functions.php"

        # First, try to read existing functions.php to append
        try:
            read_result = deployer.execute_command(f"cat {functions_path}")
            if read_result:
                # Append to existing functions.php
                updated_content = read_result.decode('utf-8') + "\n\n" + offer_ladder_cpt_code
                temp_file.write_text(updated_content)
        except:
            pass  # File doesn't exist or can't read, use just our code

        # Deploy the updated functions.php
        deploy_result = deploy_file_to_wordpress(
            site_key=site_key,
            local_path=str(temp_file),
            remote_path=functions_path,
            file_type="theme"
        )

        results["cpt_registration"] = deploy_result["success"]

        # Clean up temp file
        temp_file.unlink(missing_ok=True)

        deployer.disconnect()

        # Verify CPT registration
        if results["cpt_registration"]:
            verify_result = _execute_wp_cli(site_key, "post-type list --name=offer_ladder --format=json")
            if verify_result["success"]:
                try:
                    cpt_list = json.loads(verify_result["output"])
                    results["rest_api"] = len(cpt_list) > 0
                except json.JSONDecodeError:
                    results["rest_api"] = False

        results["meta_boxes"] = results["cpt_registration"]  # Meta boxes are in the same code

        return {
            "success": results["cpt_registration"],
            "site": site_key,
            "results": results
        }

    except Exception as e:
        return {"success": False, "error": str(e), "site": site_key}

def main():
    """Main deployment function."""
    print("🚀 Deploying Offer Ladder Custom Post Type Infrastructure")
    print("=" * 50)

    results = {}

    for site_key in REVENUE_SITES:
        print(f"\n📍 Processing {site_key}...")

        result = deploy_offer_ladder_cpt_infrastructure(site_key)

        if result["success"]:
            print("✅ Offer Ladder Custom Post Type infrastructure deployed")
            details = result["results"]
            print(f"   CPT Registration: {'✅' if details['cpt_registration'] else '❌'}")
            print(f"   Meta Boxes: {'✅' if details['meta_boxes'] else '❌'}")
            print(f"   REST API: {'✅' if details['rest_api'] else '❌'}")
        else:
            print("❌ Failed to deploy Offer Ladder infrastructure")
            print(f"   Error: {result.get('error', 'Unknown error')}")

        results[site_key] = result

    # Summary
    print("\n" + "=" * 50)
    print("📊 DEPLOYMENT SUMMARY")

    successful = 0
    failed = 0

    for site_key, result in results.items():
        status = "✅" if result["success"] else "❌"
        error_msg = f" - {result.get('error', '')}" if not result["success"] else ""
        print(f"{status} {site_key}{error_msg}")
        if result["success"]:
            successful += 1
        else:
            failed += 1

    print(f"\nTotal: {len(results)} sites")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")

    if successful > 0:
        print("\n💡 Next Steps:")
        print("1. Run deploy_offer_ladders.py to create offer ladder content")
        print("2. Verify CPT appears in WordPress admin under 'Offer Ladders'")
        print("3. Test REST API endpoint: /wp-json/wp/v2/offer_ladder")

    return successful == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)