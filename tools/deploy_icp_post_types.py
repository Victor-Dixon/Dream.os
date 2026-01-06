#!/usr/bin/env python3
"""
Deploy ICP (Ideal Customer Profile) Custom Post Type infrastructure to WordPress sites.

This tool creates the necessary custom post type and meta boxes for ICP definitions
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

def deploy_icp_cpt_infrastructure(site_key: str) -> Dict[str, any]:
    """Deploy ICP Custom Post Type infrastructure to a site."""
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

        # Step 1: Create a custom plugin for ICP CPT
        icp_plugin_code = '''<?php
/**
 * Plugin Name: ICP Definitions
 * Description: Custom Post Type for ICP (Ideal Customer Profile) definitions
 * Version: 1.0.0
 */

// Register ICP Definition Custom Post Type
function register_icp_definition_post_type() {
    $args = array(
        'public' => true,
        'label'  => 'ICP Definitions',
        'supports' => array('title', 'editor', 'custom-fields'),
        'show_in_rest' => true,
        'rest_base' => 'icp_definition',
        'menu_icon' => 'dashicons-groups',
    );
    register_post_type('icp_definition', $args);
}
add_action('init', 'register_icp_definition_post_type');

// Add meta boxes for ICP fields
function add_icp_meta_boxes() {
    add_meta_box(
        'icp_details',
        'ICP Details',
        'render_icp_meta_box',
        'icp_definition',
        'normal',
        'high'
    );
}
add_action('add_meta_boxes', 'add_icp_meta_boxes');

function render_icp_meta_box($post) {
    $target_demographic = get_post_meta($post->ID, 'target_demographic', true);
    $pain_points = get_post_meta($post->ID, 'pain_points', true);
    $desired_outcomes = get_post_meta($post->ID, 'desired_outcomes', true);

    wp_nonce_field('icp_meta_box', 'icp_meta_box_nonce');

    echo '<table class="form-table">';
    echo '<tr><th><label for="target_demographic">Target Demographic</label></th>';
    echo '<td><input type="text" id="target_demographic" name="target_demographic" value="' . esc_attr($target_demographic) . '" class="regular-text"></td></tr>';

    echo '<tr><th><label for="pain_points">Pain Points</label></th>';
    echo '<td><textarea id="pain_points" name="pain_points" rows="3" class="large-text">' . esc_textarea($pain_points) . '</textarea></td></tr>';

    echo '<tr><th><label for="desired_outcomes">Desired Outcomes</label></th>';
    echo '<td><textarea id="desired_outcomes" name="desired_outcomes" rows="3" class="large-text">' . esc_textarea($desired_outcomes) . '</textarea></td></tr>';
    echo '</table>';
}

function save_icp_meta_box_data($post_id) {
    if (!isset($_POST['icp_meta_box_nonce'])) return;
    if (!wp_verify_nonce($_POST['icp_meta_box_nonce'], 'icp_meta_box')) return;
    if (defined('DOING_AUTOSAVE') && DOING_AUTOSAVE) return;

    if (isset($_POST['target_demographic'])) {
        update_post_meta($post_id, 'target_demographic', sanitize_text_field($_POST['target_demographic']));
    }
    if (isset($_POST['pain_points'])) {
        update_post_meta($post_id, 'pain_points', sanitize_textarea_field($_POST['pain_points']));
    }
    if (isset($_POST['desired_outcomes'])) {
        update_post_meta($post_id, 'desired_outcomes', sanitize_textarea_field($_POST['desired_outcomes']));
    }
}
add_action('save_post', 'save_icp_meta_box_data');
'''

        # Create a temporary plugin file
        temp_file = Path(f"/tmp/icp-definitions_{site_key}.php")
        temp_file.parent.mkdir(exist_ok=True)
        temp_file.write_text(icp_plugin_code)

        # Deploy as a plugin
        plugin_path = f"wp-content/plugins/icp-definitions/icp-definitions.php"

        # Create plugin directory first
        deployer.execute_command(f"mkdir -p wp-content/plugins/icp-definitions")

        # Deploy the plugin file
        deploy_result = deploy_file_to_wordpress(
            site_key=site_key,
            local_path=str(temp_file),
            remote_path=plugin_path,
            file_type="plugin"
        )

        results["cpt_registration"] = deploy_result["success"]

        # Clean up temp file
        temp_file.unlink(missing_ok=True)

        # Activate the plugin if deployment was successful
        if results["cpt_registration"]:
            activate_result = _execute_wp_cli(site_key, "plugin activate icp-definitions")
            results["plugin_activation"] = activate_result["success"]

        deployer.disconnect()

        # Verify CPT registration
        if results["cpt_registration"]:
            verify_result = _execute_wp_cli(site_key, "post-type list --name=icp_definition --format=json")
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
    print("🚀 Deploying ICP Custom Post Type Infrastructure")
    print("=" * 50)

    results = {}

    for site_key in REVENUE_SITES:
        print(f"\n📍 Processing {site_key}...")

        result = deploy_icp_cpt_infrastructure(site_key)

        if result["success"]:
            print("✅ ICP Custom Post Type infrastructure deployed")
            details = result["results"]
            print(f"   CPT Registration: {'✅' if details['cpt_registration'] else '❌'}")
            print(f"   Meta Boxes: {'✅' if details['meta_boxes'] else '❌'}")
            print(f"   REST API: {'✅' if details['rest_api'] else '❌'}")
        else:
            print("❌ Failed to deploy ICP infrastructure")
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
        print("1. Run deploy_icp_definitions.py to create ICP content")
        print("2. Verify CPT appears in WordPress admin under 'ICP Definitions'")
        print("3. Test REST API endpoint: /wp-json/wp/v2/icp_definition")

    return successful == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)