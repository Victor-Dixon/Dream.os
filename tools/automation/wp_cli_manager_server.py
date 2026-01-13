#!/usr/bin/env python3
"""
WP-CLI Manager MCP Server
Remote WordPress operations via WP-CLI over SSH

Provides tools for:
- Plugin management (install, activate, deactivate, update)
- Theme management (install, activate, update)
- Cache management (flush various caches)
- Database operations (check, optimize, search-replace)
- Option management (get, update)
- Core operations (version info, health checks)
- Cron management (list, run)

<!-- SSOT Domain: infrastructure -->
"""

import os
import sys
import json
import logging
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass

# Add repository root to path for imports
repo_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(repo_root))

try:
    import paramiko
    PARAMIKO_AVAILABLE = True
except ImportError:
    PARAMIKO_AVAILABLE = False

from mcp import Tool
from mcp.server import Server
from mcp.types import TextContent, PromptMessage

logger = logging.getLogger(__name__)

@dataclass
class SiteConfig:
    """WordPress site configuration for SSH access."""
    host: str
    username: str
    password: str
    port: int = 22
    wp_path: str = "/public_html"
    php_path: str = "/usr/bin/php"

class WPCliManagerServer:
    """MCP Server for WP-CLI operations over SSH."""

    def __init__(self):
        self.site_configs = self._load_site_configs()
        self.server = Server("wp-cli-manager")

    def _load_site_configs(self) -> Dict[str, SiteConfig]:
        """Load site configurations from credentials."""
        configs = {}

        # Load from environment variables (Hostinger)
        host = os.getenv("HOSTINGER_HOST")
        username = os.getenv("HOSTINGER_USER")
        password = os.getenv("HOSTINGER_PASS")
        port = int(os.getenv("HOSTINGER_PORT", "65002"))

        if all([host, username, password]):
            configs["default"] = SiteConfig(
                host=host,
                username=username,
                password=password,
                port=port
            )

        # Load from deploy credentials if available
        creds_file = repo_root / ".deploy_credentials" / "sites.json"
        if creds_file.exists():
            try:
                with open(creds_file, 'r') as f:
                    creds_data = json.load(f)
                    for site_key, site_config in creds_data.items():
                        configs[site_key] = SiteConfig(**site_config)
            except Exception as e:
                logger.warning(f"Failed to load site credentials: {e}")

        return configs

    def _get_site_config(self, site_key: str) -> Optional[SiteConfig]:
        """Get site configuration for the given site key."""
        return self.site_configs.get(site_key) or self.site_configs.get("default")

    def _execute_wp_cli(self, site_key: str, command: str, allow_root: bool = True) -> Dict[str, Any]:
        """
        Execute WP-CLI command over SSH.

        Args:
            site_key: Site identifier
            command: WP-CLI command (without 'wp' prefix)
            allow_root: Whether to add --allow-root flag

        Returns:
            Dict with success, output, error fields
        """
        if not PARAMIKO_AVAILABLE:
            return {
                "success": False,
                "output": "",
                "error": "paramiko not available. Install with: pip install paramiko"
            }

        config = self._get_site_config(site_key)
        if not config:
            return {
                "success": False,
                "output": "",
                "error": f"No configuration found for site: {site_key}"
            }

        try:
            # Establish SSH connection
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(
                hostname=config.host,
                username=config.username,
                password=config.password,
                port=config.port
            )

            # Build WP-CLI command
            wp_command = f"cd {config.wp_path} && {config.php_path} wp {command}"
            if allow_root:
                wp_command += " --allow-root"

            logger.info(f"Executing WP-CLI: {wp_command}")

            # Execute command
            stdin, stdout, stderr = client.exec_command(wp_command)

            # Read output
            output = stdout.read().decode('utf-8').strip()
            error = stderr.read().decode('utf-8').strip()

            client.close()

            return {
                "success": True,
                "output": output,
                "error": error
            }

        except Exception as e:
            logger.error(f"WP-CLI execution failed: {e}")
            return {
                "success": False,
                "output": "",
                "error": str(e)
            }

    # WP-CLI Tools

    async def wp_core_info(self, site_key: str) -> str:
        """Get WordPress core version and information."""
        result = self._execute_wp_cli(site_key, "core version")
        if result["success"]:
            return f"WordPress Core Version: {result['output']}"
        else:
            return f"Error getting core info: {result['error']}"

    async def wp_plugin_list(self, site_key: str, status: Optional[str] = None) -> str:
        """List WordPress plugins with optional status filter."""
        command = "plugin list --format=json"
        if status:
            command += f" --status={status}"

        result = self._execute_wp_cli(site_key, command)
        if result["success"]:
            try:
                plugins = json.loads(result["output"])
                return json.dumps(plugins, indent=2)
            except:
                return result["output"]
        else:
            return f"Error listing plugins: {result['error']}"

    async def wp_plugin_activate(self, site_key: str, plugin: str) -> str:
        """Activate a WordPress plugin."""
        result = self._execute_wp_cli(site_key, f"plugin activate {plugin}")
        if result["success"]:
            return f"Plugin '{plugin}' activated successfully"
        else:
            return f"Error activating plugin '{plugin}': {result['error']}"

    async def wp_plugin_deactivate(self, site_key: str, plugin: str) -> str:
        """Deactivate a WordPress plugin."""
        result = self._execute_wp_cli(site_key, f"plugin deactivate {plugin}")
        if result["success"]:
            return f"Plugin '{plugin}' deactivated successfully"
        else:
            return f"Error deactivating plugin '{plugin}': {result['error']}"

    async def wp_plugin_install(self, site_key: str, plugin: str, activate: bool = False) -> str:
        """Install a WordPress plugin."""
        command = f"plugin install {plugin}"
        if activate:
            command += " --activate"

        result = self._execute_wp_cli(site_key, command)
        if result["success"]:
            status = "installed and activated" if activate else "installed"
            return f"Plugin '{plugin}' {status} successfully"
        else:
            return f"Error installing plugin '{plugin}': {result['error']}"

    async def wp_plugin_update(self, site_key: str, plugin: str = "--all") -> str:
        """Update WordPress plugin(s)."""
        result = self._execute_wp_cli(site_key, f"plugin update {plugin}")
        if result["success"]:
            return f"Plugin(s) updated successfully: {result['output']}"
        else:
            return f"Error updating plugins: {result['error']}"

    async def wp_theme_list(self, site_key: str, status: Optional[str] = None) -> str:
        """List WordPress themes with optional status filter."""
        command = "theme list --format=json"
        if status:
            command += f" --status={status}"

        result = self._execute_wp_cli(site_key, command)
        if result["success"]:
            try:
                themes = json.loads(result["output"])
                return json.dumps(themes, indent=2)
            except:
                return result["output"]
        else:
            return f"Error listing themes: {result['error']}"

    async def wp_theme_activate(self, site_key: str, theme: str) -> str:
        """Activate a WordPress theme."""
        result = self._execute_wp_cli(site_key, f"theme activate {theme}")
        if result["success"]:
            return f"Theme '{theme}' activated successfully"
        else:
            return f"Error activating theme '{theme}': {result['error']}"

    async def wp_theme_install(self, site_key: str, theme: str, activate: bool = False) -> str:
        """Install a WordPress theme."""
        command = f"theme install {theme}"
        if activate:
            command += " --activate"

        result = self._execute_wp_cli(site_key, command)
        if result["success"]:
            status = "installed and activated" if activate else "installed"
            return f"Theme '{theme}' {status} successfully"
        else:
            return f"Error installing theme '{theme}': {result['error']}"

    async def wp_cache_flush(self, site_key: str) -> str:
        """Flush WordPress cache."""
        result = self._execute_wp_cli(site_key, "cache flush")
        if result["success"]:
            return "WordPress cache flushed successfully"
        else:
            return f"Error flushing cache: {result['error']}"

    async def wp_transient_delete(self, site_key: str, transient: str = "--all") -> str:
        """Delete WordPress transients."""
        result = self._execute_wp_cli(site_key, f"transient delete {transient}")
        if result["success"]:
            return f"Transient(s) deleted successfully: {result['output']}"
        else:
            return f"Error deleting transients: {result['error']}"

    async def wp_rewrite_flush(self, site_key: str) -> str:
        """Flush WordPress rewrite rules."""
        result = self._execute_wp_cli(site_key, "rewrite flush")
        if result["success"]:
            return "Rewrite rules flushed successfully"
        else:
            return f"Error flushing rewrite rules: {result['error']}"

    async def wp_option_get(self, site_key: str, option_name: str) -> str:
        """Get a WordPress option value."""
        result = self._execute_wp_cli(site_key, f"option get {option_name}")
        if result["success"]:
            return f"Option '{option_name}': {result['output']}"
        else:
            return f"Error getting option '{option_name}': {result['error']}"

    async def wp_option_update(self, site_key: str, option_name: str, value: str) -> str:
        """Update a WordPress option value."""
        result = self._execute_wp_cli(site_key, f"option update {option_name} '{value}'")
        if result["success"]:
            return f"Option '{option_name}' updated successfully"
        else:
            return f"Error updating option '{option_name}': {result['error']}"

    async def wp_user_list(self, site_key: str) -> str:
        """List WordPress users."""
        result = self._execute_wp_cli(site_key, "user list --format=json")
        if result["success"]:
            try:
                users = json.loads(result["output"])
                return json.dumps(users, indent=2)
            except:
                return result["output"]
        else:
            return f"Error listing users: {result['error']}"

    async def wp_db_check(self, site_key: str) -> str:
        """Check WordPress database health."""
        result = self._execute_wp_cli(site_key, "db check")
        if result["success"]:
            return f"Database check completed: {result['output']}"
        else:
            return f"Error checking database: {result['error']}"

    async def wp_db_optimize(self, site_key: str) -> str:
        """Optimize WordPress database."""
        result = self._execute_wp_cli(site_key, "db optimize")
        if result["success"]:
            return f"Database optimization completed: {result['output']}"
        else:
            return f"Error optimizing database: {result['error']}"

    async def wp_search_replace(self, site_key: str, old: str, new: str) -> str:
        """Search and replace in database."""
        result = self._execute_wp_cli(site_key, f"search-replace '{old}' '{new}'")
        if result["success"]:
            return f"Search-replace completed: {result['output']}"
        else:
            return f"Error performing search-replace: {result['error']}"

    async def wp_cron_event_list(self, site_key: str) -> str:
        """List WordPress cron events."""
        result = self._execute_wp_cli(site_key, "cron event list --format=json")
        if result["success"]:
            try:
                events = json.loads(result["output"])
                return json.dumps(events, indent=2)
            except:
                return result["output"]
        else:
            return f"Error listing cron events: {result['error']}"

    async def wp_health_check(self, site_key: str) -> str:
        """Perform comprehensive WordPress health check."""
        result = self._execute_wp_cli(site_key, "doctor check --format=json")
        if result["success"]:
            try:
                checks = json.loads(result["output"])
                return json.dumps(checks, indent=2)
            except:
                return result["output"]
        else:
            return f"Error performing health check: {result['error']}"

def main():
    """Main entry point for MCP server."""
    server = WPCliManagerServer()

    # Register tools
    @server.server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="wp_core_info",
                description="Get WordPress core version and information",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "site_key": {
                            "type": "string",
                            "description": "Site key (e.g., 'freerideinvestor.com')"
                        }
                    },
                    "required": ["site_key"]
                }
            ),
            Tool(
                name="wp_plugin_list",
                description="List WordPress plugins",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "site_key": {
                            "type": "string",
                            "description": "Site key"
                        },
                        "status": {
                            "type": "string",
                            "enum": ["active", "inactive", "mustuse", "dropins"],
                            "description": "Optional: Filter by status"
                        }
                    },
                    "required": ["site_key"]
                }
            ),
            Tool(
                name="wp_plugin_activate",
                description="Activate a WordPress plugin",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "site_key": {
                            "type": "string",
                            "description": "Site key"
                        },
                        "plugin": {
                            "type": "string",
                            "description": "Plugin slug"
                        }
                    },
                    "required": ["site_key", "plugin"]
                }
            ),
            Tool(
                name="wp_plugin_deactivate",
                description="Deactivate a WordPress plugin",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "site_key": {
                            "type": "string",
                            "description": "Site key"
                        },
                        "plugin": {
                            "type": "string",
                            "description": "Plugin slug"
                        }
                    },
                    "required": ["site_key", "plugin"]
                }
            ),
            Tool(
                name="wp_plugin_install",
                description="Install a WordPress plugin",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "site_key": {
                            "type": "string",
                            "description": "Site key"
                        },
                        "plugin": {
                            "type": "string",
                            "description": "Plugin slug or URL"
                        },
                        "activate": {
                            "type": "boolean",
                            "default": False,
                            "description": "Activate after install"
                        }
                    },
                    "required": ["site_key", "plugin"]
                }
            ),
            Tool(
                name="wp_plugin_update",
                description="Update WordPress plugin(s)",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "site_key": {
                            "type": "string",
                            "description": "Site key"
                        },
                        "plugin": {
                            "type": "string",
                            "default": "--all",
                            "description": "Plugin slug or --all"
                        }
                    },
                    "required": ["site_key"]
                }
            ),
            Tool(
                name="wp_theme_list",
                description="List WordPress themes",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "site_key": {
                            "type": "string",
                            "description": "Site key"
                        },
                        "status": {
                            "type": "string",
                            "enum": ["active", "inactive", "parent"],
                            "description": "Optional: Filter by status"
                        }
                    },
                    "required": ["site_key"]
                }
            ),
            Tool(
                name="wp_theme_activate",
                description="Activate a WordPress theme",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "site_key": {
                            "type": "string",
                            "description": "Site key"
                        },
                        "theme": {
                            "type": "string",
                            "description": "Theme slug"
                        }
                    },
                    "required": ["site_key", "theme"]
                }
            ),
            Tool(
                name="wp_theme_install",
                description="Install a WordPress theme",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "site_key": {
                            "type": "string",
                            "description": "Site key"
                        },
                        "theme": {
                            "type": "string",
                            "description": "Theme slug or URL"
                        },
                        "activate": {
                            "type": "boolean",
                            "default": False,
                            "description": "Activate after install"
                        }
                    },
                    "required": ["site_key", "theme"]
                }
            ),
            Tool(
                name="wp_cache_flush",
                description="Flush WordPress cache",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "site_key": {
                            "type": "string",
                            "description": "Site key"
                        }
                    },
                    "required": ["site_key"]
                }
            ),
            Tool(
                name="wp_transient_delete",
                description="Delete WordPress transients",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "site_key": {
                            "type": "string",
                            "description": "Site key"
                        },
                        "transient": {
                            "type": "string",
                            "default": "--all",
                            "description": "Transient name or --all"
                        }
                    },
                    "required": ["site_key"]
                }
            ),
            Tool(
                name="wp_rewrite_flush",
                description="Flush WordPress rewrite rules",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "site_key": {
                            "type": "string",
                            "description": "Site key"
                        }
                    },
                    "required": ["site_key"]
                }
            ),
            Tool(
                name="wp_option_get",
                description="Get a WordPress option value",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "site_key": {
                            "type": "string",
                            "description": "Site key"
                        },
                        "option_name": {
                            "type": "string",
                            "description": "Option name"
                        }
                    },
                    "required": ["site_key", "option_name"]
                }
            ),
            Tool(
                name="wp_option_update",
                description="Update a WordPress option value",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "site_key": {
                            "type": "string",
                            "description": "Site key"
                        },
                        "option_name": {
                            "type": "string",
                            "description": "Option name"
                        },
                        "value": {
                            "type": "string",
                            "description": "New value"
                        }
                    },
                    "required": ["site_key", "option_name", "value"]
                }
            ),
            Tool(
                name="wp_user_list",
                description="List WordPress users",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "site_key": {
                            "type": "string",
                            "description": "Site key"
                        }
                    },
                    "required": ["site_key"]
                }
            ),
            Tool(
                name="wp_db_check",
                description="Check WordPress database health",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "site_key": {
                            "type": "string",
                            "description": "Site key"
                        }
                    },
                    "required": ["site_key"]
                }
            ),
            Tool(
                name="wp_db_optimize",
                description="Optimize WordPress database",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "site_key": {
                            "type": "string",
                            "description": "Site key"
                        }
                    },
                    "required": ["site_key"]
                }
            ),
            Tool(
                name="wp_search_replace",
                description="Search and replace in database",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "site_key": {
                            "type": "string",
                            "description": "Site key"
                        },
                        "old": {
                            "type": "string",
                            "description": "Old string"
                        },
                        "new": {
                            "type": "string",
                            "description": "New string"
                        }
                    },
                    "required": ["site_key", "old", "new"]
                }
            ),
            Tool(
                name="wp_cron_event_list",
                description="List WordPress cron events",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "site_key": {
                            "type": "string",
                            "description": "Site key"
                        }
                    },
                    "required": ["site_key"]
                }
            ),
            Tool(
                name="wp_health_check",
                description="Perform comprehensive WordPress health check",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "site_key": {
                            "type": "string",
                            "description": "Site key"
                        }
                    },
                    "required": ["site_key"]
                }
            ),
        ]

    @server.server.call_tool()
    async def call_tool(name: str, arguments: dict):
        try:
            if name == "wp_core_info":
                result = await server.wp_core_info(arguments["site_key"])
            elif name == "wp_plugin_list":
                result = await server.wp_plugin_list(
                    arguments["site_key"],
                    arguments.get("status")
                )
            elif name == "wp_plugin_activate":
                result = await server.wp_plugin_activate(
                    arguments["site_key"],
                    arguments["plugin"]
                )
            elif name == "wp_plugin_deactivate":
                result = await server.wp_plugin_deactivate(
                    arguments["site_key"],
                    arguments["plugin"]
                )
            elif name == "wp_plugin_install":
                result = await server.wp_plugin_install(
                    arguments["site_key"],
                    arguments["plugin"],
                    arguments.get("activate", False)
                )
            elif name == "wp_plugin_update":
                result = await server.wp_plugin_update(
                    arguments["site_key"],
                    arguments.get("plugin", "--all")
                )
            elif name == "wp_theme_list":
                result = await server.wp_theme_list(
                    arguments["site_key"],
                    arguments.get("status")
                )
            elif name == "wp_theme_activate":
                result = await server.wp_theme_activate(
                    arguments["site_key"],
                    arguments["theme"]
                )
            elif name == "wp_theme_install":
                result = await server.wp_theme_install(
                    arguments["site_key"],
                    arguments["theme"],
                    arguments.get("activate", False)
                )
            elif name == "wp_cache_flush":
                result = await server.wp_cache_flush(arguments["site_key"])
            elif name == "wp_transient_delete":
                result = await server.wp_transient_delete(
                    arguments["site_key"],
                    arguments.get("transient", "--all")
                )
            elif name == "wp_rewrite_flush":
                result = await server.wp_rewrite_flush(arguments["site_key"])
            elif name == "wp_option_get":
                result = await server.wp_option_get(
                    arguments["site_key"],
                    arguments["option_name"]
                )
            elif name == "wp_option_update":
                result = await server.wp_option_update(
                    arguments["site_key"],
                    arguments["option_name"],
                    arguments["value"]
                )
            elif name == "wp_user_list":
                result = await server.wp_user_list(arguments["site_key"])
            elif name == "wp_db_check":
                result = await server.wp_db_check(arguments["site_key"])
            elif name == "wp_db_optimize":
                result = await server.wp_db_optimize(arguments["site_key"])
            elif name == "wp_search_replace":
                result = await server.wp_search_replace(
                    arguments["site_key"],
                    arguments["old"],
                    arguments["new"]
                )
            elif name == "wp_cron_event_list":
                result = await server.wp_cron_event_list(arguments["site_key"])
            elif name == "wp_health_check":
                result = await server.wp_health_check(arguments["site_key"])
            else:
                result = f"Unknown tool: {name}"

            return [TextContent(type="text", text=result)]
        except Exception as e:
            logger.error(f"Tool execution failed: {e}")
            return [TextContent(type="text", text=f"Error: {str(e)}")]

    # Run the server
    import asyncio
    asyncio.run(server.server.run())

if __name__ == "__main__":
    main()