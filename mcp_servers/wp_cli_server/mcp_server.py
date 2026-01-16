#!/usr/bin/env python3
"""
WP-CLI MCP Server - MCP Protocol Implementation
===============================================

<!-- SSOT Domain: web -->

MCP server wrapper for WP-CLI operations, exposing WordPress management tools
through the Model Context Protocol for AI agent integration.

V2 Compliance | Author: Agent-1 | Date: 2026-01-16
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from .wp_cli_server import WPCliServer, WPCliError

logger = logging.getLogger(__name__)


class WPCliMCPServer:
    """
    MCP Server for WordPress CLI operations.

    Exposes WP-CLI functionality as MCP tools for AI agents to manage WordPress sites.
    """

    def __init__(self, wordpress_path: Optional[Path] = None):
        """
        Initialize MCP WP-CLI server.

        Args:
            wordpress_path: Path to WordPress installation
        """
        self.server = WPCliServer(wordpress_path)

    def get_available_tools(self) -> List[Dict[str, Any]]:
        """
        Get list of available MCP tools.

        Returns:
            List of tool definitions
        """
        return [
            {
                "name": "wp_cli_install_plugin",
                "description": "Install a WordPress plugin from wordpress.org",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "plugin_slug": {
                            "type": "string",
                            "description": "Plugin slug from wordpress.org"
                        },
                        "activate": {
                            "type": "boolean",
                            "description": "Whether to activate the plugin after installation",
                            "default": False
                        }
                    },
                    "required": ["plugin_slug"]
                }
            },
            {
                "name": "wp_cli_activate_plugin",
                "description": "Activate a WordPress plugin",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "plugin_slug": {
                            "type": "string",
                            "description": "Plugin slug to activate"
                        }
                    },
                    "required": ["plugin_slug"]
                }
            },
            {
                "name": "wp_cli_deactivate_plugin",
                "description": "Deactivate a WordPress plugin",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "plugin_slug": {
                            "type": "string",
                            "description": "Plugin slug to deactivate"
                        }
                    },
                    "required": ["plugin_slug"]
                }
            },
            {
                "name": "wp_cli_update_plugin",
                "description": "Update a WordPress plugin",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "plugin_slug": {
                            "type": "string",
                            "description": "Plugin slug to update"
                        }
                    },
                    "required": ["plugin_slug"]
                }
            },
            {
                "name": "wp_cli_list_plugins",
                "description": "List WordPress plugins with optional status filter",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "status_filter": {
                            "type": "string",
                            "description": "Filter by status (active, inactive, etc.)",
                            "enum": ["active", "inactive", "must-use", "dropin"]
                        }
                    }
                }
            },
            {
                "name": "wp_cli_install_theme",
                "description": "Install a WordPress theme from wordpress.org",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "theme_slug": {
                            "type": "string",
                            "description": "Theme slug from wordpress.org"
                        },
                        "activate": {
                            "type": "boolean",
                            "description": "Whether to activate the theme after installation",
                            "default": False
                        }
                    },
                    "required": ["theme_slug"]
                }
            },
            {
                "name": "wp_cli_activate_theme",
                "description": "Activate a WordPress theme",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "theme_slug": {
                            "type": "string",
                            "description": "Theme slug to activate"
                        }
                    },
                    "required": ["theme_slug"]
                }
            },
            {
                "name": "wp_cli_db_export",
                "description": "Export WordPress database to file",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "output_file": {
                            "type": "string",
                            "description": "Output file path for database dump"
                        }
                    },
                    "required": ["output_file"]
                }
            },
            {
                "name": "wp_cli_db_import",
                "description": "Import WordPress database from file",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "input_file": {
                            "type": "string",
                            "description": "Input file path for database dump"
                        }
                    },
                    "required": ["input_file"]
                }
            },
            {
                "name": "wp_cli_db_search_replace",
                "description": "Search and replace in WordPress database",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "old_value": {
                            "type": "string",
                            "description": "Value to search for"
                        },
                        "new_value": {
                            "type": "string",
                            "description": "Value to replace with"
                        },
                        "table": {
                            "type": "string",
                            "description": "Specific table to operate on (optional)"
                        }
                    },
                    "required": ["old_value", "new_value"]
                }
            },
            {
                "name": "wp_cli_create_post",
                "description": "Create a new WordPress post or page",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "Post title"
                        },
                        "content": {
                            "type": "string",
                            "description": "Post content",
                            "default": ""
                        },
                        "post_type": {
                            "type": "string",
                            "description": "Post type (post, page, etc.)",
                            "default": "post",
                            "enum": ["post", "page", "attachment", "revision", "nav_menu_item"]
                        },
                        "status": {
                            "type": "string",
                            "description": "Post status",
                            "default": "draft",
                            "enum": ["publish", "future", "draft", "pending", "private", "trash"]
                        }
                    },
                    "required": ["title"]
                }
            },
            {
                "name": "wp_cli_update_post",
                "description": "Update an existing WordPress post",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "post_id": {
                            "type": "integer",
                            "description": "Post ID to update"
                        },
                        "title": {
                            "type": "string",
                            "description": "New post title (optional)"
                        },
                        "content": {
                            "type": "string",
                            "description": "New post content (optional)"
                        }
                    },
                    "required": ["post_id"]
                }
            },
            {
                "name": "wp_cli_core_update",
                "description": "Update WordPress core to latest version",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "wp_cli_get_site_info",
                "description": "Get basic WordPress site information",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            }
        ]

    def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute an MCP tool.

        Args:
            tool_name: Name of the tool to execute
            parameters: Tool parameters

        Returns:
            Tool execution result
        """
        try:
            if tool_name == "wp_cli_install_plugin":
                result = self.server.install_plugin(
                    parameters["plugin_slug"],
                    parameters.get("activate", False)
                )
            elif tool_name == "wp_cli_activate_plugin":
                result = self.server.activate_plugin(parameters["plugin_slug"])
            elif tool_name == "wp_cli_deactivate_plugin":
                result = self.server.deactivate_plugin(parameters["plugin_slug"])
            elif tool_name == "wp_cli_update_plugin":
                result = self.server.update_plugin(parameters["plugin_slug"])
            elif tool_name == "wp_cli_list_plugins":
                result = self.server.list_plugins(parameters.get("status_filter"))
            elif tool_name == "wp_cli_install_theme":
                result = self.server.install_theme(
                    parameters["theme_slug"],
                    parameters.get("activate", False)
                )
            elif tool_name == "wp_cli_activate_theme":
                result = self.server.activate_theme(parameters["theme_slug"])
            elif tool_name == "wp_cli_db_export":
                result = self.server.db_export(parameters["output_file"])
            elif tool_name == "wp_cli_db_import":
                result = self.server.db_import(parameters["input_file"])
            elif tool_name == "wp_cli_db_search_replace":
                result = self.server.db_search_replace(
                    parameters["old_value"],
                    parameters["new_value"],
                    parameters.get("table")
                )
            elif tool_name == "wp_cli_create_post":
                result = self.server.create_post(
                    parameters["title"],
                    parameters.get("content", ""),
                    parameters.get("post_type", "post"),
                    parameters.get("status", "draft")
                )
            elif tool_name == "wp_cli_update_post":
                result = self.server.update_post(
                    parameters["post_id"],
                    parameters.get("title"),
                    parameters.get("content")
                )
            elif tool_name == "wp_cli_core_update":
                result = self.server.core_update()
            elif tool_name == "wp_cli_get_site_info":
                result = self.server.get_site_info()
            else:
                return {
                    "error": f"Unknown tool: {tool_name}",
                    "available_tools": [t["name"] for t in self.get_available_tools()]
                }

            return result

        except WPCliError as e:
            logger.error(f"WP-CLI tool execution failed: {e}")
            return {
                "error": str(e),
                "tool": tool_name,
                "parameters": parameters
            }
        except Exception as e:
            logger.error(f"Unexpected error in tool execution: {e}")
            return {
                "error": f"Unexpected error: {e}",
                "tool": tool_name,
                "parameters": parameters
            }

    def get_server_info(self) -> Dict[str, Any]:
        """
        Get server information and capabilities.

        Returns:
            Server information
        """
        return {
            "name": "WP-CLI MCP Server",
            "version": "1.0.0",
            "description": "WordPress CLI operations through MCP protocol",
            "capabilities": ["wp-cli-operations"],
            "tools_count": len(self.get_available_tools()),
            "wp_cli_available": self.server.check_wp_cli_availability(),
            "site_info": self.server.get_site_info()
        }