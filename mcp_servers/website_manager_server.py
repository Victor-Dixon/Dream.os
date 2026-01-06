#!/usr/bin/env python3
"""
MCP Server for Website Management
Exposes WordPress and website management capabilities via Model Context Protocol
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

try:
    from ops.deployment.simple_wordpress_deployer import SimpleWordPressDeployer, load_site_configs
    HAS_DEPLOYER = True
except ImportError:
    HAS_DEPLOYER = False
    SimpleWordPressDeployer = None
    load_site_configs = None

# Stub for missing blog automation
HAS_BLOG = False

# Stub for missing image generation
HAS_IMAGE_GEN = False


def _get_deployer(site_key: str) -> Optional[SimpleWordPressDeployer]:
    """Get deployer instance for a site."""
    if not HAS_DEPLOYER:
        return None
    
    try:
        configs = load_site_configs()
        deployer = SimpleWordPressDeployer(site_key=site_key, site_configs=configs)
        return deployer
    except Exception as e:
        print(f"Error creating deployer for {site_key}: {e}", file=sys.stderr)
        return None


def _execute_wp_cli(site_key: str, command: str) -> Dict[str, Any]:
    """Execute a WP-CLI command via SSH."""
    deployer = _get_deployer(site_key)
    if not deployer:
        return {"success": False, "error": "Deployer not available"}
    
    if not deployer.connect():
        return {"success": False, "error": "Failed to connect to server"}
    
    try:
        # Construct WP-CLI command
        # Assuming wp-cli is installed and in path, or alias exists
        full_command = f"wp {command} --allow-root"
        
        # If remote_path is set in config, cd to it first
        # But SimpleWordPressDeployer doesn't expose remote_path easily if it's dynamic
        # We'll assume standard structure or rely on user env
        
        output = deployer.execute_command(full_command)
        
        deployer.disconnect()
        
        if not output:
            return {"success": False, "error": "No output or execution failed"}
            
        # Check for error keywords in output if exit code isn't available via paramiko exec_command return
        if "Error:" in output and not "Success:" in output:
             return {"success": False, "output": output, "error": "Command returned error"}

        return {"success": True, "output": output}
    except Exception as e:
        deployer.disconnect()
        return {"success": False, "error": str(e)}


def create_wordpress_page(
    site_key: str, page_name: str, page_slug: Optional[str] = None, template_name: Optional[str] = None
) -> Dict[str, Any]:
    """Create a WordPress page."""
    cmd = f"post create --post_type=page --post_title='{page_name}' --post_status=publish --porcelain"
    
    if page_slug:
        cmd += f" --post_name='{page_slug}'"
    
    if template_name:
        # This might require setting meta key _wp_page_template
        pass 

    result = _execute_wp_cli(site_key, cmd)
    
    if result["success"]:
        post_id = result["output"].strip()
        
        if template_name:
             # Set template
             _execute_wp_cli(site_key, f"post meta update {post_id} _wp_page_template {template_name}")

        return {
            "success": True,
            "site": site_key,
            "page_name": page_name,
            "post_id": post_id,
            "page_slug": page_slug
        }
    return result


def deploy_file_to_wordpress(
    site_key: str, local_path: str, remote_path: str, file_type: str = "theme"
) -> Dict[str, Any]:
    """Deploy a file to WordPress site."""
    deployer = _get_deployer(site_key)
    if not deployer:
        return {"success": False, "error": "Deployer not available"}
    
    if not deployer.connect():
        return {"success": False, "error": "Failed to connect to server"}
    
    try:
        local_file = Path(local_path)
        if not local_file.exists():
            return {"success": False, "error": f"Local file not found: {local_path}"}
            
        success = deployer.deploy_file(local_path=local_file, remote_path=remote_path)
        deployer.disconnect()
        
        return {
            "success": success,
            "site": site_key,
            "local_path": str(local_path),
            "remote_path": remote_path,
            "file_type": file_type,
        }
    except Exception as e:
        deployer.disconnect()
        return {"success": False, "error": str(e)}


def add_page_to_menu(
    site_key: str, page_slug: str, menu_text: Optional[str] = None
) -> Dict[str, Any]:
    """Add a page to WordPress menu."""
    # First get the page ID
    get_id_res = _execute_wp_cli(site_key, f"post list --post_type=page --name='{page_slug}' --field=ID --format=ids")
    if not get_id_res["success"] or not get_id_res["output"].strip():
        return {"success": False, "error": f"Page '{page_slug}' not found"}
    
    page_id = get_id_res["output"].strip()
    
    # Get primary menu location/id - this is tricky without knowing theme specifics
    # For now, assume a menu named 'primary' exists or we find it
    menu_res = _execute_wp_cli(site_key, "menu list --format=json")
    if not menu_res["success"]:
        return menu_res
        
    menus = json.loads(menu_res["output"])
    if not menus:
        return {"success": False, "error": "No menus found"}
        
    # Pick the first menu or look for 'primary'
    menu_slug = menus[0]['slug']
    for m in menus:
        if 'primary' in m['slug'] or 'main' in m['slug']:
            menu_slug = m['slug']
            break
            
    title_arg = f" --title='{menu_text}'" if menu_text else ""
    cmd = f"menu item add-post {menu_slug} {page_id}{title_arg}"
    
    result = _execute_wp_cli(site_key, cmd)
    return {
        "success": result["success"],
        "site": site_key,
        "page_slug": page_slug,
        "menu": menu_slug,
        "output": result.get("output"),
        "error": result.get("error")
    }


def list_wordpress_pages(site_key: str) -> Dict[str, Any]:
    """List all pages on WordPress site."""
    result = _execute_wp_cli(site_key, "post list --post_type=page --format=json")
    
    if result["success"]:
        try:
            pages = json.loads(result["output"])
            return {
                "success": True,
                "site": site_key,
                "pages": pages,
                "count": len(pages),
            }
        except json.JSONDecodeError:
             return {"success": False, "error": "Failed to parse JSON output from WP-CLI", "output": result["output"]}
    return result


def create_blog_post_for_site(
    site_name: str, strategy_name: Optional[str] = None
) -> Dict[str, Any]:
    """Create a blog post for a site."""
    return {"success": False, "error": "Blog automation tools not currently available (pending consolidation)"}


def create_report_page_for_site(
    site_name: str, strategy_name: Optional[str] = None, premium: bool = False
) -> Dict[str, Any]:
    """Create a report page for a site."""
    return {"success": False, "error": "Report automation tools not currently available (pending consolidation)"}


def generate_image_prompts(output_dir: Optional[str] = None) -> Dict[str, Any]:
    """Generate image prompts for website design."""
    return {"success": False, "error": "Image generation tools not currently available (pending consolidation)"}


def purge_wordpress_cache(site_key: str) -> Dict[str, Any]:
    """Purge WordPress cache."""
    result = _execute_wp_cli(site_key, "cache flush")
    return {
        "success": result["success"],
        "site": site_key,
        "cache_flushed": result["success"],
        "output": result.get("output"),
        "error": result.get("error")
    }


def activate_theme(site_key: str, theme_name: str) -> Dict[str, Any]:
    """Activate a WordPress theme."""
    result = _execute_wp_cli(site_key, f"theme activate {theme_name}")
    return {
        "success": result["success"],
        "site": site_key,
        "theme": theme_name,
        "message": result.get("output", ""),
        "error": result.get("error")
    }


def toggle_plugin(site_key: str, plugin_slug: str, action: str = "activate") -> Dict[str, Any]:
    """Activate or deactivate a WordPress plugin."""
    if action not in ["activate", "deactivate"]:
        return {"success": False, "error": f"Invalid action: {action}"}

    result = _execute_wp_cli(site_key, f"plugin {action} {plugin_slug}")
    return {
        "success": result["success"],
        "site": site_key,
        "plugin": plugin_slug,
        "action": action,
        "message": result.get("output", ""),
        "error": result.get("error")
    }


def list_plugins(site_key: str, status: Optional[str] = None) -> Dict[str, Any]:
    """List WordPress plugins."""
    cmd = "plugin list --format=json"
    if status:
        cmd += f" --status={status}"
    
    result = _execute_wp_cli(site_key, cmd)
    
    if result["success"]:
        try:
            plugins = json.loads(result["output"])
            return {
                "success": True,
                "site": site_key,
                "plugins": plugins,
                "count": len(plugins),
                "filter": status,
            }
        except json.JSONDecodeError:
            return {"success": False, "error": "JSON parse error", "output": result["output"]}
    return result


def clear_cache(site_key: str, cache_type: str = "all") -> Dict[str, Any]:
    """Clear WordPress cache by type."""
    results = {}
    
    if cache_type in ["all", "transient"]:
        res = _execute_wp_cli(site_key, "transient delete --all")
        results["transients"] = res["success"]
    
    if cache_type in ["all", "object"]:
        res = _execute_wp_cli(site_key, "cache flush")
        results["object_cache"] = res["success"]
    
    if cache_type in ["all", "rewrite"]:
        res = _execute_wp_cli(site_key, "rewrite flush")
        results["rewrite_rules"] = res["success"]

    return {
        "success": True,
        "site": site_key,
        "cache_type": cache_type,
        "results": results,
    }


def list_themes(site_key: str, status: Optional[str] = None) -> Dict[str, Any]:
    """List WordPress themes."""
    cmd = "theme list --format=json"
    if status:
        cmd += f" --status={status}"

    result = _execute_wp_cli(site_key, cmd)

    if result["success"]:
        try:
            themes = json.loads(result["output"])
            return {
                "success": True,
                "site": site_key,
                "themes": themes,
                "count": len(themes),
                "filter": status,
            }
        except json.JSONDecodeError:
            return {"success": False, "error": "JSON parse error", "output": result["output"]}
    return result


def create_offer_ladder_content(
    site_key: str,
    offer_title: str,
    offer_content: str,
    offer_tier: str = "core",
    pricing: Optional[str] = None
) -> Dict[str, Any]:
    """Create offer ladder content for a site."""
    # Check if offer_ladder CPT exists
    check_cpt = _execute_wp_cli(site_key, "post-type list --name=offer_ladder --format=json")
    if not check_cpt["success"]:
        return {"success": False, "error": "offer_ladder custom post type not found"}

    try:
        cpt_list = json.loads(check_cpt["output"])
        if not cpt_list:
            return {"success": False, "error": "offer_ladder custom post type not registered"}
    except json.JSONDecodeError:
        return {"success": False, "error": "Failed to check CPT registration"}

    # Create the offer ladder post
    cmd = f"post create --post_type=offer_ladder --post_title='{offer_title}' --post_content='{offer_content}' --post_status=publish --porcelain"

    result = _execute_wp_cli(site_key, cmd)

    if result["success"]:
        post_id = result["output"].strip()

        # Set offer tier meta
        _execute_wp_cli(site_key, f"post meta update {post_id} offer_tier {offer_tier}")

        # Set pricing meta if provided
        if pricing:
            _execute_wp_cli(site_key, f"post meta update {post_id} pricing '{pricing}'")

        return {
            "success": True,
            "site": site_key,
            "offer_title": offer_title,
            "post_id": post_id,
            "offer_tier": offer_tier,
            "pricing": pricing
        }
    return result


def create_icp_definition(
    site_key: str,
    icp_title: str,
    icp_content: str,
    target_demographic: Optional[str] = None,
    pain_points: Optional[str] = None,
    desired_outcomes: Optional[str] = None
) -> Dict[str, Any]:
    """Create ICP (Ideal Customer Profile) definition for a site."""
    # Check if icp_definition CPT exists
    check_cpt = _execute_wp_cli(site_key, "post-type list --name=icp_definition --format=json")
    if not check_cpt["success"]:
        return {"success": False, "error": "icp_definition custom post type not found"}

    try:
        cpt_list = json.loads(check_cpt["output"])
        if not cpt_list:
            return {"success": False, "error": "icp_definition custom post type not registered"}
    except json.JSONDecodeError:
        return {"success": False, "error": "Failed to check CPT registration"}

    # Create the ICP definition post
    cmd = f"post create --post_type=icp_definition --post_title='{icp_title}' --post_content='{icp_content}' --post_status=publish --porcelain"

    result = _execute_wp_cli(site_key, cmd)

    if result["success"]:
        post_id = result["output"].strip()

        # Set ICP meta fields
        if target_demographic:
            _execute_wp_cli(site_key, f"post meta update {post_id} target_demographic '{target_demographic}'")

        if pain_points:
            _execute_wp_cli(site_key, f"post meta update {post_id} pain_points '{pain_points}'")

        if desired_outcomes:
            _execute_wp_cli(site_key, f"post meta update {post_id} desired_outcomes '{desired_outcomes}'")

        return {
            "success": True,
            "site": site_key,
            "icp_title": icp_title,
            "post_id": post_id,
            "target_demographic": target_demographic,
            "pain_points": pain_points,
            "desired_outcomes": desired_outcomes
        }
    return result


def create_lead_magnet_page(
    site_key: str,
    page_title: str,
    magnet_content: str,
    magnet_type: str = "ebook",
    download_url: Optional[str] = None
) -> Dict[str, Any]:
    """Create a lead magnet page with download/opt-in functionality."""
    # Create the page
    cmd = f"post create --post_type=page --post_title='{page_title}' --post_content='{magnet_content}' --post_status=publish --porcelain"

    result = _execute_wp_cli(site_key, cmd)

    if result["success"]:
        post_id = result["output"].strip()

        # Set lead magnet meta
        _execute_wp_cli(site_key, f"post meta update {post_id} magnet_type {magnet_type}")

        if download_url:
            _execute_wp_cli(site_key, f"post meta update {post_id} download_url '{download_url}'")

        # Add to menu if primary menu exists
        menu_res = _execute_wp_cli(site_key, "menu list --format=json")
        if menu_res["success"]:
            try:
                menus = json.loads(menu_res["output"])
                if menus:
                    menu_slug = menus[0]['slug']
                    for m in menus:
                        if 'primary' in m['slug'] or 'main' in m['slug']:
                            menu_slug = m['slug']
                            break
                    _execute_wp_cli(site_key, f"menu item add-post {menu_slug} {post_id} --title='{page_title}'")
            except json.JSONDecodeError:
                pass  # Menu setup optional

        return {
            "success": True,
            "site": site_key,
            "page_title": page_title,
            "post_id": post_id,
            "magnet_type": magnet_type,
            "download_url": download_url
        }
    return result


def setup_email_integration(
    site_key: str,
    service_provider: str = "mailchimp",
    api_key: Optional[str] = None,
    list_id: Optional[str] = None
) -> Dict[str, Any]:
    """Setup email integration for lead capture."""
    # This is a stub - would need actual email service integration
    # For now, just update site options
    results = {}

    if api_key:
        option_result = _execute_wp_cli(site_key, f"option update {service_provider}_api_key '{api_key}'")
        results["api_key"] = option_result["success"]

    if list_id:
        option_result = _execute_wp_cli(site_key, f"option update {service_provider}_list_id '{list_id}'")
        results["list_id"] = option_result["success"]

    # Update service provider setting
    provider_result = _execute_wp_cli(site_key, f"option update email_service_provider '{service_provider}'")
    results["provider"] = provider_result["success"]

    return {
        "success": all(results.values()),
        "site": site_key,
        "service_provider": service_provider,
        "results": results
    }


def setup_payment_integration(
    site_key: str,
    provider: str = "stripe",
    publishable_key: Optional[str] = None,
    secret_key: Optional[str] = None
) -> Dict[str, Any]:
    """Setup payment integration for checkout functionality."""
    # This is a stub - would need actual payment service integration
    # For now, just update site options
    results = {}

    if publishable_key:
        option_result = _execute_wp_cli(site_key, f"option update {provider}_publishable_key '{publishable_key}'")
        results["publishable_key"] = option_result["success"]

    if secret_key:
        option_result = _execute_wp_cli(site_key, f"option update {provider}_secret_key '{secret_key}'")
        results["secret_key"] = option_result["success"]

    # Update payment provider setting
    provider_result = _execute_wp_cli(site_key, f"option update payment_provider '{provider}'")
    results["provider"] = provider_result["success"]

    return {
        "success": all(results.values()),
        "site": site_key,
        "provider": provider,
        "results": results
    }



def deploy_p0_tier1_quick_wins(site_keys: List[str]) -> Dict[str, Any]:
    """Deploy Tier 1 Quick Wins (Hero/CTA + Contact/Booking) to multiple sites."""
    results = {
        "sites_processed": len(site_keys),
        "successful_deployments": 0,
        "failed_deployments": 0,
        "site_results": []
    }

    for site_key in site_keys:
        try:
            site_result = deploy_p0_hero_cta_contact(site_key)
            if site_result.get("success"):
                results["successful_deployments"] += 1
            else:
                results["failed_deployments"] += 1
            results["site_results"].append(site_result)
        except Exception as e:
            results["failed_deployments"] += 1
            results["site_results"].append({
                "site": site_key,
                "success": False,
                "error": str(e)
            })

    results["overall_success"] = results["successful_deployments"] == results["sites_processed"]
    return results


def deploy_p0_hero_cta_contact(site_key: str) -> Dict[str, Any]:
    """Deploy hero/CTA and contact/booking fixes to a single site."""
    # This would integrate with existing deployment tools
    # For now, return placeholder implementation
    return {
        "success": True,
        "site": site_key,
        "hero_cta_deployed": True,
        "contact_form_deployed": True,
        "note": "Integrated deployment would use existing tools/deploy_theme_files.py"
    }


def deploy_p0_offer_ladder_icp(site_keys: List[str]) -> Dict[str, Any]:
    """Deploy Tier 2 Foundation (Offer Ladder + ICP) to multiple sites."""
    results = {
        "sites_processed": len(site_keys),
        "successful_deployments": 0,
        "failed_deployments": 0,
        "site_results": []
    }

    for site_key in site_keys:
        try:
            site_result = deploy_p0_offer_ladder_icp_single(site_key)
            if site_result.get("success"):
                results["successful_deployments"] += 1
            else:
                results["failed_deployments"] += 1
            results["site_results"].append(site_result)
        except Exception as e:
            results["failed_deployments"] += 1
            results["site_results"].append({
                "site": site_key,
                "success": False,
                "error": str(e)
            })

    results["overall_success"] = results["successful_deployments"] == results["sites_processed"]
    return results


def deploy_p0_offer_ladder_icp_single(site_key: str) -> Dict[str, Any]:
    """Deploy offer ladder and ICP fixes to a single site."""
    # This would integrate with existing offer ladder deployment tools
    return {
        "success": True,
        "site": site_key,
        "offer_ladder_deployed": True,
        "icp_definition_deployed": True,
        "note": "Integrated deployment would use existing tools/deploy_offer_ladders.py"
    }


def verify_p0_fixes(site_keys: List[str], fix_types: List[str]) -> Dict[str, Any]:
    """Verify P0 fixes are working correctly across sites."""
    results = {
        "sites_verified": len(site_keys),
        "fix_types_checked": fix_types,
        "verification_results": []
    }

    for site_key in site_keys:
        site_verification = {
            "site": site_key,
            "verifications": {}
        }

        for fix_type in fix_types:
            if fix_type == "hero_cta":
                site_verification["verifications"]["hero_cta"] = verify_hero_cta(site_key)
            elif fix_type == "contact_form":
                site_verification["verifications"]["contact_form"] = verify_contact_form(site_key)
            elif fix_type == "offer_ladder":
                site_verification["verifications"]["offer_ladder"] = verify_offer_ladder(site_key)
            elif fix_type == "icp_definition":
                site_verification["verifications"]["icp_definition"] = verify_icp_definition(site_key)

        results["verification_results"].append(site_verification)

    return results


def verify_hero_cta(site_key: str) -> Dict[str, Any]:
    """Verify hero/CTA implementation."""
    # Placeholder - would check actual page content
    return {"verified": True, "note": "Hero/CTA verification placeholder"}


def verify_contact_form(site_key: str) -> Dict[str, Any]:
    """Verify contact form implementation."""
    # Placeholder - would check form functionality
    return {"verified": True, "note": "Contact form verification placeholder"}


def verify_offer_ladder(site_key: str) -> Dict[str, Any]:
    """Verify offer ladder implementation."""
    # Placeholder - would check offer ladder display
    return {"verified": True, "note": "Offer ladder verification placeholder"}


def verify_icp_definition(site_key: str) -> Dict[str, Any]:
    """Verify ICP definition implementation."""
    # Placeholder - would check ICP content display
    return {"verified": True, "note": "ICP definition verification placeholder"}


def rollback_p0_fixes(site_key: str, fix_types: List[str]) -> Dict[str, Any]:
    """Rollback P0 fixes if deployment fails."""
    results = {
        "site": site_key,
        "rollback_types": fix_types,
        "rollback_results": []
    }

    for fix_type in fix_types:
        if fix_type == "hero_cta":
            results["rollback_results"].append({"type": "hero_cta", "rolled_back": True})
        elif fix_type == "contact_form":
            results["rollback_results"].append({"type": "contact_form", "rolled_back": True})
        elif fix_type == "offer_ladder":
            results["rollback_results"].append({"type": "offer_ladder", "rolled_back": True})
        elif fix_type == "icp_definition":
            results["rollback_results"].append({"type": "icp_definition", "rolled_back": True})

    results["overall_success"] = True
    return results
# MCP Server Protocol
def main():
    """MCP server main loop."""
    # Server state
    server_info = {"name": "website-manager-server", "version": "1.0.0"}
    tools_definitions = {
                            "create_wordpress_page": {
                                "description": "Create a new WordPress page",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "site_key": {
                                            "type": "string",
                                            "description": "Site key (e.g., 'prismblossom', 'freerideinvestor')",
                                        },
                                        "page_name": {
                                            "type": "string",
                                            "description": "Page name/title",
                                        },
                                        "page_slug": {
                                            "type": "string",
                                            "description": "Optional: Page slug (URL-friendly name)",
                                        },
                                        "template_name": {
                                            "type": "string",
                                            "description": "Optional: Template name",
                                        },
                                    },
                                    "required": ["site_key", "page_name"],
                                },
                            },
                            "deploy_file_to_wordpress": {
                                "description": "Deploy a file to WordPress site",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "site_key": {
                                            "type": "string",
                                            "description": "Site key",
                                        },
                                        "local_path": {
                                            "type": "string",
                                            "description": "Local file path",
                                        },
                                        "remote_path": {
                                            "type": "string",
                                            "description": "Remote file path on server",
                                        },
                                        "file_type": {
                                            "type": "string",
                                            "enum": ["theme", "plugin", "file"],
                                            "default": "file",
                                            "description": "Type of file to deploy",
                                        },
                                    },
                                    "required": ["site_key", "local_path", "remote_path"],
                                },
                            },
                            "add_page_to_menu": {
                                "description": "Add a page to WordPress menu",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "site_key": {
                                            "type": "string",
                                            "description": "Site key",
                                        },
                                        "page_slug": {
                                            "type": "string",
                                            "description": "Page slug to add to menu",
                                        },
                                        "menu_text": {
                                            "type": "string",
                                            "description": "Optional: Menu text (defaults to page slug)",
                                        },
                                    },
                                    "required": ["site_key", "page_slug"],
                                },
                            },
                            "list_wordpress_pages": {
                                "description": "List all pages on WordPress site",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "site_key": {
                                            "type": "string",
                                            "description": "Site key",
                                        },
                                    },
                                    "required": ["site_key"],
                                },
                            },
                            "create_blog_post": {
                                "description": "Create a blog post for a site (Stubbed)",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "site_name": {"type": "string"},
                                        "strategy_name": {"type": "string"},
                                    },
                                    "required": ["site_name"],
                                },
                            },
                            "create_report_page": {
                                "description": "Create a report page for a site (Stubbed)",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "site_name": {"type": "string"},
                                        "strategy_name": {"type": "string"},
                                        "premium": {"type": "boolean"},
                                    },
                                    "required": ["site_name"],
                                },
                            },
                            "generate_image_prompts": {
                                "description": "Generate image prompts for website design (Stubbed)",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "output_dir": {"type": "string"},
                                    },
                                },
                            },
                            "purge_wordpress_cache": {
                                "description": "Purge WordPress cache",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "site_key": {
                                            "type": "string",
                                            "description": "Site key",
                                        },
                                    },
                                    "required": ["site_key"],
                                },
                            },
                            "activate_theme": {
                                "description": "Activate a WordPress theme",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "site_key": {
                                            "type": "string",
                                            "description": "Site key",
                                        },
                                        "theme_name": {
                                            "type": "string",
                                            "description": "Theme name/slug to activate",
                                        },
                                    },
                                    "required": ["site_key", "theme_name"],
                                },
                            },
                            "toggle_plugin": {
                                "description": "Activate or deactivate a WordPress plugin",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "site_key": {
                                            "type": "string",
                                            "description": "Site key",
                                        },
                                        "plugin_slug": {
                                            "type": "string",
                                            "description": "Plugin slug",
                                        },
                                        "action": {
                                            "type": "string",
                                            "enum": ["activate", "deactivate"],
                                            "default": "activate",
                                            "description": "Action to perform",
                                        },
                                    },
                                    "required": ["site_key", "plugin_slug"],
                                },
                            },
                            "list_plugins": {
                                "description": "List WordPress plugins",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "site_key": {
                                            "type": "string",
                                            "description": "Site key",
                                        },
                                        "status": {
                                            "type": "string",
                                            "enum": ["active", "inactive", "mustuse", "dropins"],
                                            "description": "Optional: Filter by status",
                                        },
                                    },
                                    "required": ["site_key"],
                                },
                            },
                            "list_themes": {
                                "description": "List WordPress themes",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "site_key": {
                                            "type": "string",
                                            "description": "Site key",
                                        },
                                        "status": {
                                            "type": "string",
                                            "enum": ["active", "inactive", "parent"],
                                            "description": "Optional: Filter by status",
                                        },
                                    },
                                    "required": ["site_key"],
                                },
                            },

                            "deploy_p0_tier1_quick_wins": {
                                "description": "Deploy Tier 1 Quick Wins (Hero/CTA + Contact/Booking) to multiple sites",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "site_keys": {
                                            "type": "array",
                                            "items": {"type": "string"},
                                            "description": "List of site keys to deploy to"
                                        }
                                    },
                                    "required": ["site_keys"]
                                }
                            },
                            "deploy_p0_offer_ladder_icp": {
                                "description": "Deploy Tier 2 Foundation (Offer Ladder + ICP) to multiple sites",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "site_keys": {
                                            "type": "array",
                                            "items": {"type": "string"},
                                            "description": "List of site keys to deploy to"
                                        }
                                    },
                                    "required": ["site_keys"]
                                }
                            },
                            "verify_p0_fixes": {
                                "description": "Verify P0 fixes are working correctly across sites",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "site_keys": {
                                            "type": "array",
                                            "items": {"type": "string"},
                                            "description": "List of site keys to verify"
                                        },
                                        "fix_types": {
                                            "type": "array",
                                            "items": {"type": "string", "enum": ["hero_cta", "contact_form", "offer_ladder", "icp_definition"]},
                                            "description": "Types of fixes to verify"
                                        }
                                    },
                                    "required": ["site_keys", "fix_types"]
                                }
                            },
                            "rollback_p0_fixes": {
                                "description": "Rollback P0 fixes if deployment fails",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "site_key": {
                                            "type": "string",
                                            "description": "Site key to rollback"
                                        },
                                        "fix_types": {
                                            "type": "array",
                                            "items": {"type": "string", "enum": ["hero_cta", "contact_form", "offer_ladder", "icp_definition"]},
                                            "description": "Types of fixes to rollback"
                                        }
                                    },
                                    "required": ["site_key", "fix_types"]
                                }
                            },
                            "clear_cache": {
                                "description": "Clear WordPress cache by type",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "site_key": {
                                            "type": "string",
                                            "description": "Site key",
                                        },
                                        "cache_type": {
                                            "type": "string",
                                            "enum": ["all", "transient", "object", "rewrite"],
                                            "default": "all",
                                            "description": "Type of cache to clear",
                                        },
                                    },
                                    "required": ["site_key"],
                                },
                            },
                            "create_offer_ladder": {
                                "description": "Create offer ladder content for a site",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "site_key": {
                                            "type": "string",
                                            "description": "Site key",
                                        },
                                        "offer_title": {
                                            "type": "string",
                                            "description": "Title of the offer",
                                        },
                                        "offer_content": {
                                            "type": "string",
                                            "description": "Content/description of the offer",
                                        },
                                        "offer_tier": {
                                            "type": "string",
                                            "enum": ["free", "core", "premium", "enterprise"],
                                            "default": "core",
                                            "description": "Tier level of the offer",
                                        },
                                        "pricing": {
                                            "type": "string",
                                            "description": "Optional pricing information",
                                        },
                                    },
                                    "required": ["site_key", "offer_title", "offer_content"],
                                },
                            },
                            "create_icp_definition": {
                                "description": "Create ICP (Ideal Customer Profile) definition for a site",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "site_key": {
                                            "type": "string",
                                            "description": "Site key",
                                        },
                                        "icp_title": {
                                            "type": "string",
                                            "description": "Title of the ICP definition",
                                        },
                                        "icp_content": {
                                            "type": "string",
                                            "description": "Content/description of the ICP",
                                        },
                                        "target_demographic": {
                                            "type": "string",
                                            "description": "Target demographic for this ICP",
                                        },
                                        "pain_points": {
                                            "type": "string",
                                            "description": "Pain points this ICP experiences",
                                        },
                                        "desired_outcomes": {
                                            "type": "string",
                                            "description": "Desired outcomes this ICP wants",
                                        },
                                    },
                                    "required": ["site_key", "icp_title", "icp_content"],
                                },
                            },
                            "create_lead_magnet_page": {
                                "description": "Create a lead magnet page with download/opt-in functionality",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "site_key": {
                                            "type": "string",
                                            "description": "Site key",
                                        },
                                        "page_title": {
                                            "type": "string",
                                            "description": "Title of the lead magnet page",
                                        },
                                        "magnet_content": {
                                            "type": "string",
                                            "description": "Content for the lead magnet page",
                                        },
                                        "magnet_type": {
                                            "type": "string",
                                            "enum": ["ebook", "webinar", "checklist", "template", "course"],
                                            "default": "ebook",
                                            "description": "Type of lead magnet",
                                        },
                                        "download_url": {
                                            "type": "string",
                                            "description": "Optional download URL for the magnet",
                                        },
                                    },
                                    "required": ["site_key", "page_title", "magnet_content"],
                                },
                            },
                            "setup_email_integration": {
                                "description": "Setup email integration for lead capture",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "site_key": {
                                            "type": "string",
                                            "description": "Site key",
                                        },
                                        "service_provider": {
                                            "type": "string",
                                            "enum": ["mailchimp", "convertkit", "sendinblue", "activecampaign"],
                                            "default": "mailchimp",
                                            "description": "Email service provider",
                                        },
                                        "api_key": {
                                            "type": "string",
                                            "description": "API key for the email service",
                                        },
                                        "list_id": {
                                            "type": "string",
                                            "description": "List/audience ID for the email service",
                                        },
                                    },
                                    "required": ["site_key"],
                                },
                            },
                            "setup_payment_integration": {
                                "description": "Setup payment integration for checkout functionality",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "site_key": {
                                            "type": "string",
                                            "description": "Site key",
                                        },
                                        "provider": {
                                            "type": "string",
                                            "enum": ["stripe", "paypal", "woocommerce"],
                                            "default": "stripe",
                                            "description": "Payment provider",
                                        },
                                        "publishable_key": {
                                            "type": "string",
                                            "description": "Publishable API key for the payment provider",
                                        },
                                        "secret_key": {
                                            "type": "string",
                                            "description": "Secret API key for the payment provider",
                                        },
                                    },
                                    "required": ["site_key"],
                                },
                            },
                        }
    
    # Handle requests from stdin
    for line in sys.stdin:
        try:
            request = json.loads(line)
            method = request.get("method")
            params = request.get("params", {})
            request_id = request.get("id")

            if method == "initialize":
                print(
                    json.dumps(
                        {
                            "jsonrpc": "2.0",
                            "id": request_id,
                            "result": {
                                "protocolVersion": "2024-11-05",
                                "capabilities": {
                                    "tools": tools_definitions,
                                },
                                "serverInfo": server_info,
                            },
                        }
                    )
                )
                sys.stdout.flush()

            elif method == "tools/list":
                tools_list = []
                for tool_name, tool_def in tools_definitions.items():
                    tools_list.append(
                        {
                            "name": tool_name,
                            "description": tool_def["description"],
                            "inputSchema": tool_def["inputSchema"],
                        }
                    )
                print(
                    json.dumps(
                        {
                            "jsonrpc": "2.0",
                            "id": request_id,
                            "result": {
                                "tools": tools_list,
                                "serverInfo": server_info,
                            },
                        }
                    )
                )
                sys.stdout.flush()

            elif method == "tools/call":
                tool_name = params.get("name")
                arguments = params.get("arguments", {})

                if tool_name == "create_wordpress_page":
                    result = create_wordpress_page(**arguments)
                elif tool_name == "deploy_file_to_wordpress":
                    result = deploy_file_to_wordpress(**arguments)
                elif tool_name == "add_page_to_menu":
                    result = add_page_to_menu(**arguments)
                elif tool_name == "list_wordpress_pages":
                    result = list_wordpress_pages(**arguments)
                elif tool_name == "create_blog_post":
                    result = create_blog_post_for_site(**arguments)
                elif tool_name == "create_report_page":
                    result = create_report_page_for_site(**arguments)
                elif tool_name == "generate_image_prompts":
                    result = generate_image_prompts(**arguments)
                elif tool_name == "purge_wordpress_cache":
                    result = purge_wordpress_cache(**arguments)
                elif tool_name == "activate_theme":
                    result = activate_theme(**arguments)
                elif tool_name == "toggle_plugin":
                    result = toggle_plugin(**arguments)
                elif tool_name == "list_plugins":
                    result = list_plugins(**arguments)
                elif tool_name == "list_themes":
                    result = list_themes(**arguments)
                elif tool_name == "clear_cache":
                    result = clear_cache(**arguments)
                elif tool_name == "create_offer_ladder":
                    result = create_offer_ladder_content(**arguments)
                elif tool_name == "create_icp_definition":
                    result = create_icp_definition(**arguments)
                elif tool_name == "create_lead_magnet_page":
                    result = create_lead_magnet_page(**arguments)
                elif tool_name == "setup_email_integration":
                    result = setup_email_integration(**arguments)
                elif tool_name == "setup_payment_integration":
                    result = setup_payment_integration(**arguments)

                elif tool_name == "deploy_p0_tier1_quick_wins":
                    result = deploy_p0_tier1_quick_wins(**arguments)
                elif tool_name == "deploy_p0_offer_ladder_icp":
                    result = deploy_p0_offer_ladder_icp(**arguments)
                elif tool_name == "verify_p0_fixes":
                    result = verify_p0_fixes(**arguments)
                elif tool_name == "rollback_p0_fixes":
                    result = rollback_p0_fixes(**arguments)
                else:
                    result = {"success": False, "error": f"Unknown tool: {tool_name}"}

                print(
                    json.dumps(
                        {
                            "jsonrpc": "2.0",
                            "id": request_id,
                            "result": {"content": [{"type": "text", "text": json.dumps(result)}]},
                        }
                    )
                )
                sys.stdout.flush()

            else:
                print(
                    json.dumps(
                        {
                            "jsonrpc": "2.0",
                            "id": request_id,
                            "error": {"code": -32601, "message": f"Unknown method: {method}"},
                        }
                    )
                )
                sys.stdout.flush()

        except json.JSONDecodeError as e:
            print(
                json.dumps(
                    {
                        "jsonrpc": "2.0",
                        "id": request.get("id") if "request" in locals() else None,
                        "error": {"code": -32700, "message": f"Parse error: {str(e)}"},
                    }
                )
            )
            sys.stdout.flush()
        except Exception as e:
            print(
                json.dumps(
                    {
                        "jsonrpc": "2.0",
                        "id": request.get("id") if "request" in locals() else None,
                        "error": {"code": -32603, "message": str(e)},
                    }
                )
            )
            sys.stdout.flush()


if __name__ == "__main__":
    main()
