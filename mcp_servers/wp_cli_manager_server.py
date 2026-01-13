#!/usr/bin/env python3
"""
MCP Server for WP-CLI Management
Provides direct WP-CLI command execution for remote WordPress operations

This server wraps WP-CLI commands and executes them on remote WordPress sites
via SSH, providing a clean interface for WordPress management.
"""

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

PROJECT_ROOT = Path(__file__).parent.parent

try:
    from dotenv import load_dotenv
    load_dotenv(PROJECT_ROOT / ".env")
except ImportError:
    pass

# Try to import site configs
try:
    sys.path.insert(0, str(PROJECT_ROOT / "ops" / "deployment"))
    from simple_wordpress_deployer import SimpleWordPressDeployer, load_site_configs
    HAS_DEPLOYER = True
except ImportError:
    HAS_DEPLOYER = False
    SimpleWordPressDeployer = None
    load_site_configs = None


def _get_deployer(site_key: str):
    """Get a deployer instance for the site."""
    if not HAS_DEPLOYER:
        return None, "Deployer not available"
    
    try:
        site_configs = load_site_configs()
        if site_key not in site_configs:
            return None, f"Site not found: {site_key}"
        
        deployer = SimpleWordPressDeployer(site_key, site_configs)
        if not deployer.connect():
            return None, "Failed to connect to server"
        
        return deployer, None
    except Exception as e:
        return None, str(e)


def execute_wp_cli(site_key: str, command: str, allow_root: bool = True) -> Dict[str, Any]:
    """Execute a WP-CLI command on remote WordPress site."""
    deployer, error = _get_deployer(site_key)
    if error:
        return {"success": False, "error": error}
    
    try:
        # Build the full command
        wp_command = f"wp {command}"
        if allow_root:
            wp_command += " --allow-root"
        
        # Get remote path from config
        site_configs = load_site_configs()
        config = site_configs.get(site_key, {})
        remote_path = config.get("remote_path", f"domains/{site_key}/public_html")
        
        full_command = f"cd {remote_path} && {wp_command} 2>&1"
        result = deployer.execute_command(full_command)
        
        deployer.disconnect()
        
        return {
            "success": True,
            "site": site_key,
            "command": command,
            "output": result,
        }
    except Exception as e:
        if deployer:
            deployer.disconnect()
        return {"success": False, "error": str(e)}


def wp_core_info(site_key: str) -> Dict[str, Any]:
    """Get WordPress core version and information."""
    return execute_wp_cli(site_key, "core version")


def wp_plugin_list(site_key: str, status: Optional[str] = None) -> Dict[str, Any]:
    """List WordPress plugins."""
    cmd = "plugin list --format=json"
    if status:
        cmd += f" --status={status}"
    
    result = execute_wp_cli(site_key, cmd)
    
    if result.get("success") and result.get("output"):
        try:
            plugins = json.loads(result["output"])
            return {
                "success": True,
                "site": site_key,
                "plugins": plugins,
                "count": len(plugins),
            }
        except json.JSONDecodeError:
            return result
    
    return result


def wp_plugin_activate(site_key: str, plugin: str) -> Dict[str, Any]:
    """Activate a WordPress plugin."""
    return execute_wp_cli(site_key, f"plugin activate {plugin}")


def wp_plugin_deactivate(site_key: str, plugin: str) -> Dict[str, Any]:
    """Deactivate a WordPress plugin."""
    return execute_wp_cli(site_key, f"plugin deactivate {plugin}")


def wp_plugin_install(site_key: str, plugin: str, activate: bool = False) -> Dict[str, Any]:
    """Install a WordPress plugin."""
    cmd = f"plugin install {plugin}"
    if activate:
        cmd += " --activate"
    return execute_wp_cli(site_key, cmd)


def wp_plugin_update(site_key: str, plugin: str = "--all") -> Dict[str, Any]:
    """Update WordPress plugin(s)."""
    return execute_wp_cli(site_key, f"plugin update {plugin}")


def wp_theme_list(site_key: str) -> Dict[str, Any]:
    """List WordPress themes."""
    result = execute_wp_cli(site_key, "theme list --format=json")
    
    if result.get("success") and result.get("output"):
        try:
            themes = json.loads(result["output"])
            return {
                "success": True,
                "site": site_key,
                "themes": themes,
                "count": len(themes),
            }
        except json.JSONDecodeError:
            return result
    
    return result


def wp_theme_activate(site_key: str, theme: str) -> Dict[str, Any]:
    """Activate a WordPress theme."""
    return execute_wp_cli(site_key, f"theme activate {theme}")


def wp_theme_install(site_key: str, theme: str, activate: bool = False) -> Dict[str, Any]:
    """Install a WordPress theme."""
    cmd = f"theme install {theme}"
    if activate:
        cmd += " --activate"
    return execute_wp_cli(site_key, cmd)


def wp_cache_flush(site_key: str) -> Dict[str, Any]:
    """Flush WordPress cache."""
    return execute_wp_cli(site_key, "cache flush")


def wp_transient_delete(site_key: str, transient: str = "--all") -> Dict[str, Any]:
    """Delete WordPress transients."""
    return execute_wp_cli(site_key, f"transient delete {transient}")


def wp_rewrite_flush(site_key: str) -> Dict[str, Any]:
    """Flush WordPress rewrite rules."""
    return execute_wp_cli(site_key, "rewrite flush")


def wp_option_get(site_key: str, option_name: str) -> Dict[str, Any]:
    """Get a WordPress option value."""
    return execute_wp_cli(site_key, f"option get {option_name}")


def wp_option_update(site_key: str, option_name: str, value: str) -> Dict[str, Any]:
    """Update a WordPress option value."""
    # Escape the value for shell
    escaped_value = value.replace("'", "'\\''")
    return execute_wp_cli(site_key, f"option update {option_name} '{escaped_value}'")


def wp_user_list(site_key: str) -> Dict[str, Any]:
    """List WordPress users."""
    result = execute_wp_cli(site_key, "user list --format=json")
    
    if result.get("success") and result.get("output"):
        try:
            users = json.loads(result["output"])
            # Remove sensitive data
            for user in users:
                if "user_pass" in user:
                    del user["user_pass"]
            return {
                "success": True,
                "site": site_key,
                "users": users,
                "count": len(users),
            }
        except json.JSONDecodeError:
            return result
    
    return result


def wp_db_check(site_key: str) -> Dict[str, Any]:
    """Check WordPress database."""
    return execute_wp_cli(site_key, "db check")


def wp_db_optimize(site_key: str) -> Dict[str, Any]:
    """Optimize WordPress database."""
    return execute_wp_cli(site_key, "db optimize")


def wp_search_replace(site_key: str, old: str, new: str) -> Dict[str, Any]:
    """Search and replace in database."""
    return execute_wp_cli(site_key, f"search-replace '{old}' '{new}'")


def wp_cron_event_list(site_key: str) -> Dict[str, Any]:
    """List WordPress cron events."""
    result = execute_wp_cli(site_key, "cron event list --format=json")
    if result.get("success") and result.get("output"):
        try:
            events = json.loads(result["output"])
            return {
                "success": True,
                "site": site_key,
                "events": events,
                "count": len(events),
            }
        except json.JSONDecodeError:
            return result
    return result


def wp_health_check(site_key: str) -> Dict[str, Any]:
    """Get WordPress site health status."""
    results = {}
    
    # Get core version
    core_result = execute_wp_cli(site_key, "core version")
    results["core_version"] = core_result.get("output", "").strip() if core_result.get("success") else "Unknown"
    
    # Check database
    db_result = execute_wp_cli(site_key, "db check")
    results["db_status"] = "OK" if db_result.get("success") else "Error"
    
    # Get active plugins count
    plugins_result = wp_plugin_list(site_key, status="active")
    results["active_plugins"] = plugins_result.get("count", 0) if plugins_result.get("success") else 0
    
    # Get active theme
    theme_result = execute_wp_cli(site_key, "theme list --status=active --field=name")
    results["active_theme"] = theme_result.get("output", "").strip() if theme_result.get("success") else "Unknown"
    
    return {
        "success": True,
        "site": site_key,
        "health": results,
    }


# MCP Server Protocol
def main():
    """MCP server main loop."""
    server_info = {"name": "wp-cli-manager-server", "version": "1.0.0"}
    tools_definitions = {
        "execute_wp_cli": {
            "description": "Execute any WP-CLI command on remote WordPress site",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "site_key": {"type": "string", "description": "Site key (e.g., 'freerideinvestor.com')"},
                    "command": {"type": "string", "description": "WP-CLI command (without 'wp' prefix)"},
                    "allow_root": {"type": "boolean", "default": True, "description": "Add --allow-root flag"},
                },
                "required": ["site_key", "command"],
            },
        },
        "wp_core_info": {
            "description": "Get WordPress core version and information",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "site_key": {"type": "string", "description": "Site key"},
                },
                "required": ["site_key"],
            },
        },
        "wp_plugin_list": {
            "description": "List WordPress plugins",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "site_key": {"type": "string", "description": "Site key"},
                    "status": {"type": "string", "enum": ["active", "inactive", "mustuse", "dropins"], "description": "Filter by status"},
                },
                "required": ["site_key"],
            },
        },
        "wp_plugin_activate": {
            "description": "Activate a WordPress plugin",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "site_key": {"type": "string", "description": "Site key"},
                    "plugin": {"type": "string", "description": "Plugin slug"},
                },
                "required": ["site_key", "plugin"],
            },
        },
        "wp_plugin_deactivate": {
            "description": "Deactivate a WordPress plugin",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "site_key": {"type": "string", "description": "Site key"},
                    "plugin": {"type": "string", "description": "Plugin slug"},
                },
                "required": ["site_key", "plugin"],
            },
        },
        "wp_plugin_install": {
            "description": "Install a WordPress plugin",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "site_key": {"type": "string", "description": "Site key"},
                    "plugin": {"type": "string", "description": "Plugin slug or URL"},
                    "activate": {"type": "boolean", "default": False, "description": "Activate after install"},
                },
                "required": ["site_key", "plugin"],
            },
        },
        "wp_plugin_update": {
            "description": "Update WordPress plugin(s)",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "site_key": {"type": "string", "description": "Site key"},
                    "plugin": {"type": "string", "default": "--all", "description": "Plugin slug or --all"},
                },
                "required": ["site_key"],
            },
        },
        "wp_theme_list": {
            "description": "List WordPress themes",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "site_key": {"type": "string", "description": "Site key"},
                },
                "required": ["site_key"],
            },
        },
        "wp_theme_activate": {
            "description": "Activate a WordPress theme",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "site_key": {"type": "string", "description": "Site key"},
                    "theme": {"type": "string", "description": "Theme slug"},
                },
                "required": ["site_key", "theme"],
            },
        },
        "wp_theme_install": {
            "description": "Install a WordPress theme",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "site_key": {"type": "string", "description": "Site key"},
                    "theme": {"type": "string", "description": "Theme slug or URL"},
                    "activate": {"type": "boolean", "default": False, "description": "Activate after install"},
                },
                "required": ["site_key", "theme"],
            },
        },
        "wp_cache_flush": {
            "description": "Flush WordPress cache",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "site_key": {"type": "string", "description": "Site key"},
                },
                "required": ["site_key"],
            },
        },
        "wp_transient_delete": {
            "description": "Delete WordPress transients",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "site_key": {"type": "string", "description": "Site key"},
                    "transient": {"type": "string", "default": "--all", "description": "Transient name or --all"},
                },
                "required": ["site_key"],
            },
        },
        "wp_rewrite_flush": {
            "description": "Flush WordPress rewrite rules",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "site_key": {"type": "string", "description": "Site key"},
                },
                "required": ["site_key"],
            },
        },
        "wp_option_get": {
            "description": "Get a WordPress option value",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "site_key": {"type": "string", "description": "Site key"},
                    "option_name": {"type": "string", "description": "Option name"},
                },
                "required": ["site_key", "option_name"],
            },
        },
        "wp_option_update": {
            "description": "Update a WordPress option value",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "site_key": {"type": "string", "description": "Site key"},
                    "option_name": {"type": "string", "description": "Option name"},
                    "value": {"type": "string", "description": "New value"},
                },
                "required": ["site_key", "option_name", "value"],
            },
        },
        "wp_user_list": {
            "description": "List WordPress users",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "site_key": {"type": "string", "description": "Site key"},
                },
                "required": ["site_key"],
            },
        },
        "wp_db_check": {
            "description": "Check WordPress database health",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "site_key": {"type": "string", "description": "Site key"},
                },
                "required": ["site_key"],
            },
        },
        "wp_db_optimize": {
            "description": "Optimize WordPress database",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "site_key": {"type": "string", "description": "Site key"},
                },
                "required": ["site_key"],
            },
        },
        "wp_search_replace": {
            "description": "Search and replace in database",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "site_key": {"type": "string", "description": "Site key"},
                    "old": {"type": "string", "description": "Old string"},
                    "new": {"type": "string", "description": "New string"},
                },
                "required": ["site_key", "old", "new"],
            },
        },
        "wp_cron_event_list": {
            "description": "List WordPress cron events",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "site_key": {"type": "string", "description": "Site key"},
                },
                "required": ["site_key"],
            },
        },
        "wp_health_check": {
            "description": "Perform comprehensive WordPress health check",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "site_key": {"type": "string", "description": "Site key"},
                },
                "required": ["site_key"],
            },
        },
    }

    tool_map = {
        "execute_wp_cli": execute_wp_cli,
        "wp_core_info": wp_core_info,
        "wp_plugin_list": wp_plugin_list,
        "wp_plugin_activate": wp_plugin_activate,
        "wp_plugin_deactivate": wp_plugin_deactivate,
        "wp_plugin_install": wp_plugin_install,
        "wp_plugin_update": wp_plugin_update,
        "wp_theme_list": wp_theme_list,
        "wp_theme_activate": wp_theme_activate,
        "wp_theme_install": wp_theme_install,
        "wp_cache_flush": wp_cache_flush,
        "wp_transient_delete": wp_transient_delete,
        "wp_rewrite_flush": wp_rewrite_flush,
        "wp_option_get": wp_option_get,
        "wp_option_update": wp_option_update,
        "wp_user_list": wp_user_list,
        "wp_db_check": wp_db_check,
        "wp_db_optimize": wp_db_optimize,
        "wp_search_replace": wp_search_replace,
        "wp_cron_event_list": wp_cron_event_list,
        "wp_health_check": wp_health_check,
    }

    # Handle requests from stdin
    for line in sys.stdin:
        try:
            request = json.loads(line)
            method = request.get("method")
            params = request.get("params", {})
            request_id = request.get("id")

            if method == "initialize":
                print(json.dumps({
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": tools_definitions},
                        "serverInfo": server_info,
                    },
                }))
                sys.stdout.flush()

            elif method == "tools/list":
                tools_list = [
                    {"name": name, "description": defn["description"], "inputSchema": defn["inputSchema"]}
                    for name, defn in tools_definitions.items()
                ]
                print(json.dumps({
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {"tools": tools_list, "serverInfo": server_info},
                }))
                sys.stdout.flush()

            elif method == "tools/call":
                tool_name = params.get("name")
                arguments = params.get("arguments", {})

                if tool_name in tool_map:
                    result = tool_map[tool_name](**arguments)
                else:
                    result = {"success": False, "error": f"Unknown tool: {tool_name}"}

                print(json.dumps({
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(result)}]},
                }))
                sys.stdout.flush()

            else:
                print(json.dumps({
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {"code": -32601, "message": f"Unknown method: {method}"},
                }))
                sys.stdout.flush()

        except json.JSONDecodeError as e:
            print(json.dumps({
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": f"Parse error: {str(e)}"},
            }))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32603, "message": str(e)},
            }))
            sys.stdout.flush()


if __name__ == "__main__":
    main()
