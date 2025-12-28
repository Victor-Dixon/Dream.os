"""
Tool Registry
=============

Dynamic tool registry for agent toolbelt operations.
Includes MCP server discovery and metadata for the 20-server architecture.

V2 Compliance: <200 lines
Author: Agent-5 (Business Intelligence Specialist)

SSOT TOOL METADATA
Purpose: Central registry for discovering and resolving tool adapters by name (including MCP-backed tools).
Description: Loads `tool_registry.lock.json`, resolves adapter classes dynamically, and caches resolved adapters for reuse.
Usage:
  - from tools.tool_registry import get_tool_registry; registry = get_tool_registry()
  - adapter_cls = registry.resolve(\"task-manager.get_tasks\")
  - python -c \"from tools.tool_registry import get_tool_registry; print(get_tool_registry().list_tools()[:5])\"
Date: 2025-12-28
Tags: ssot, tooling, registry, mcp
"""

import importlib
import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Handle both module and script execution
# Use absolute imports when package context is unavailable
try:
    from .adapters.base_adapter import IToolAdapter
    from .adapters.error_types import ToolNotFoundError
except ImportError:
    _tools_dir = Path(__file__).parent
    if str(_tools_dir) not in sys.path:
        sys.path.insert(0, str(_tools_dir))
    from adapters.base_adapter import IToolAdapter
    from adapters.error_types import ToolNotFoundError

logger = logging.getLogger(__name__)

# Singleton instance
_registry_instance = None


class ToolRegistry:
    """Dynamic registry for tool discovery and resolution."""

    def __init__(self):
        """Initialize registry."""
        self._cache: dict[str, IToolAdapter] = {}
        self._registry_data = self._load_registry_data()

    def _load_registry_data(self) -> dict[str, list[str]]:
        """Load tool registry data from JSON file."""
        try:
            # Check multiple possible locations for the lock file
            candidate_paths = [
                Path("tools/tool_registry.lock.json"),
                Path("tools_v2/tool_registry.lock.json"),
                Path(__file__).parent / "tool_registry.lock.json"
            ]
            
            lock_path = None
            for path in candidate_paths:
                if path.exists():
                    lock_path = path
                    break
            
            if not lock_path:
                logger.warning("Could not find tool_registry.lock.json")
                return {}
                
            with open(lock_path, "r") as f:
                data = json.load(f)
                return data.get("tools", {})
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.warning(f"Could not load registry data: {e}")
            return {}

    def _resolve_tool_class(self, tool_name: str) -> type[IToolAdapter]:
        """Resolve tool class by name, loading it if necessary."""
        if tool_name in self._cache:
            return self._cache[tool_name]

        if tool_name not in self._registry_data:
            raise ToolNotFoundError(f"Tool '{tool_name}' not found in registry")

        module_path, class_name = self._registry_data[tool_name]

        try:
            module = importlib.import_module(module_path)
            tool_class = getattr(module, class_name)

            self._cache[tool_name] = tool_class
            return tool_class

        except (ImportError, AttributeError) as e:
            raise ToolNotFoundError(f"Could not load tool '{tool_name}': {e}")

    def get_tool_class(self, tool_name: str) -> type[IToolAdapter]:
        """Get tool class by name."""
        return self._resolve_tool_class(tool_name)

    def resolve(self, tool_name: str) -> type[IToolAdapter]:
        """Resolve tool class by name."""
        return self.get_tool_class(tool_name)

    def get_tool(self, tool_name: str) -> IToolAdapter:
        """Get instantiated tool adapter by name."""
        adapter_class = self.resolve(tool_name)
        return adapter_class()

    def list_tools(self) -> list[str]:
        """List all available tools."""
        return sorted(self._registry_data.keys())

    def list_by_category(self, category: str) -> list[str]:
        """List tools by category."""
        tools = []
        for tool_name in self._registry_data.keys():
            try:
                tool = self.get_tool(tool_name)
                if tool.get_spec().category == category:
                    tools.append(tool_name)
            except Exception:
                continue
        return sorted(tools)

    def get_categories(self) -> list[str]:
        """Get all available categories."""
        categories = set()
        for tool_name in self._registry_data.keys():
            try:
                tool = self.get_tool(tool_name)
                categories.add(tool.get_spec().category)
            except Exception:
                continue
        return sorted(categories)

    def clear_cache(self):
        """Clear the tool cache."""
        self._cache.clear()


def get_tool_registry() -> ToolRegistry:
    """Get singleton tool registry instance."""
    global _registry_instance
    if _registry_instance is None:
        _registry_instance = ToolRegistry()
    return _registry_instance


# MCP Server Metadata for 20-Server Architecture
MCP_SERVERS = {
    # NPX-based servers (external)
    "memory": {
        "type": "npx",
        "package": "@modelcontextprotocol/server-memory",
        "description": "Persistent memory and knowledge graph",
        "category": "core",
    },
    "filesystem": {
        "type": "npx",
        "package": "@modelcontextprotocol/server-filesystem",
        "description": "File system operations",
        "category": "core",
    },
    "brave-search": {
        "type": "npx",
        "package": "@modelcontextprotocol/server-brave-search",
        "description": "Web search via Brave API",
        "category": "external",
    },
    "sqlite": {
        "type": "npx",
        "package": "@modelcontextprotocol/server-sqlite",
        "description": "SQLite database operations",
        "category": "core",
    },
    "git": {
        "type": "npx",
        "package": "@modelcontextprotocol/server-git",
        "description": "Git repository operations",
        "category": "core",
    },
    "github": {
        "type": "npx",
        "package": "@modelcontextprotocol/server-github",
        "description": "GitHub API operations",
        "category": "external",
    },
    "discord": {
        "type": "npx",
        "package": "@modelcontextprotocol/server-discord",
        "description": "Discord bot operations",
        "category": "external",
    },
    # Python-based servers (project)
    "swarm-messaging": {
        "type": "python",
        "path": "mcp_servers/messaging_server.py",
        "description": "Swarm messaging system (PyAutoGUI-based agent messaging)",
        "category": "swarm",
        "tools": ["send_agent_message", "broadcast_message", "get_agent_coordinates"],
    },
    "task-manager": {
        "type": "python",
        "path": "mcp_servers/task_manager_server.py",
        "description": "Task management for MASTER_TASK_LOG.md",
        "category": "swarm",
        "tools": ["add_task_to_inbox", "mark_task_complete", "move_task_to_waiting", "get_tasks"],
    },
    "website-manager": {
        "type": "python",
        "path": "mcp_servers/website_manager_server.py",
        "description": "WordPress and website management",
        "category": "wordpress",
        "tools": ["create_wordpress_page", "deploy_file_to_wordpress", "list_wordpress_pages",
                  "purge_wordpress_cache", "activate_theme", "toggle_plugin", "list_plugins",
                  "list_themes", "clear_cache"],
    },
    "swarm-brain": {
        "type": "python",
        "path": "mcp_servers/swarm_brain_server.py",
        "description": "Swarm Brain knowledge base",
        "category": "swarm",
        "tools": ["share_learning", "record_decision", "search_swarm_knowledge",
                  "take_note", "get_agent_notes"],
    },
    "git-operations": {
        "type": "python",
        "path": "mcp_servers/git_operations_server.py",
        "description": "Git work verification",
        "category": "core",
        "tools": ["verify_git_work", "get_commit_details", "verify_work_exists"],
    },
    "v2-compliance": {
        "type": "python",
        "path": "mcp_servers/v2_compliance_server.py",
        "description": "V2 compliance checking",
        "category": "compliance",
        "tools": ["check_compliance", "validate_file", "get_exceptions"],
    },
    "devlog-manager": {
        "type": "python",
        "path": "mcp_servers/devlog_manager_server.py",
        "description": "Devlog creation, posting, validation",
        "category": "documentation",
        "tools": ["post_devlog", "validate_devlog", "create_devlog", "list_devlogs", "generate_devlog_feed"],
    },
    "discord-integration": {
        "type": "python",
        "path": "mcp_servers/discord_integration_server.py",
        "description": "Discord webhook posting and notifications",
        "category": "external",
        "tools": ["post_to_webhook", "post_agent_update", "validate_webhook",
                  "send_embed", "get_configured_webhooks", "post_build_notification"],
    },
    "cleanup-manager": {
        "type": "python",
        "path": "mcp_servers/cleanup_manager_server.py",
        "description": "Workspace and session cleanup",
        "category": "maintenance",
        "tools": ["cleanup_agent_inbox", "cleanup_all_inboxes", "session_cleanup",
                  "archive_completed_tasks", "get_workspace_status", "consolidate_documentation"],
    },
    "deployment-manager": {
        "type": "python",
        "path": "mcp_servers/deployment_manager_server.py",
        "description": "Deployment status and verification",
        "category": "deployment",
        "tools": ["check_deployment_status", "verify_deployment", "list_deployable_sites",
                  "get_deployment_history", "record_deployment", "check_all_sites", "get_sftp_credentials"],
    },
    "wp-cli-manager": {
        "type": "python",
        "path": "mcp_servers/wp_cli_manager_server.py",
        "description": "WP-CLI remote command execution",
        "category": "wordpress",
        "tools": ["execute_wp_cli", "wp_core_version", "wp_plugin_list", "wp_plugin_activate",
                  "wp_plugin_deactivate", "wp_theme_list", "wp_theme_activate", "wp_cache_flush",
                  "wp_rewrite_flush", "wp_option_get", "wp_option_update", "wp_user_list",
                  "wp_db_check", "wp_db_optimize", "wp_site_health"],
    },
    "github-professional": {
        "type": "python",
        "path": "mcp_servers/github_professional_server.py",
        "description": "Professional GitHub operations (repos, PRs, issues, teams)",
        "category": "external",
    },
    "unified-tools": {
        "type": "python",
        "path": "mcp_servers/unified_tool_server.py",
        "description": "Unified tool server via tool registry",
        "category": "core",
    },
    "deployment": {
        "type": "python",
        "path": "mcp_servers/deployment_server.py",
        "description": "Unified deployment operations",
        "category": "deployment",
    },
    "validation-audit": {
        "type": "python",
        "path": "mcp_servers/validation_audit_server.py",
        "description": "Validation and audit operations",
        "category": "compliance",
    },
    "wordpress-theme": {
        "type": "python",
        "path": "mcp_servers/wordpress_theme_server.py",
        "description": "WordPress theme management",
        "category": "wordpress",
    },
    "content-management": {
        "type": "python",
        "path": "mcp_servers/content_management_server.py",
        "description": "WordPress content operations",
        "category": "wordpress",
    },
    "analytics-seo": {
        "type": "python",
        "path": "mcp_servers/analytics_seo_server.py",
        "description": "Analytics and SEO operations",
        "category": "analytics",
    },
    "maintenance-monitoring": {
        "type": "python",
        "path": "mcp_servers/maintenance_monitoring_server.py",
        "description": "WordPress maintenance and monitoring",
        "category": "maintenance",
    },
    "development-testing": {
        "type": "python",
        "path": "mcp_servers/development_testing_server.py",
        "description": "Development and testing workflows",
        "category": "development",
    },
    "coordination": {
        "type": "python",
        "path": "mcp_servers/coordination_server.py",
        "description": "Coordination and status management",
        "category": "swarm",
    },
}


def get_mcp_servers() -> Dict[str, Dict]:
    """Get all MCP server metadata."""
    return MCP_SERVERS


def get_mcp_server(name: str) -> Optional[Dict]:
    """Get metadata for a specific MCP server."""
    return MCP_SERVERS.get(name)


def list_mcp_servers_by_category(category: str) -> List[str]:
    """List MCP servers by category."""
    return [name for name, meta in MCP_SERVERS.items() if meta.get("category") == category]


def get_mcp_categories() -> List[str]:
    """Get all MCP server categories."""
    return sorted(set(meta.get("category", "unknown") for meta in MCP_SERVERS.values()))


def get_all_mcp_tools() -> Dict[str, List[str]]:
    """Get all tools exposed by MCP servers."""
    result = {}
    for name, meta in MCP_SERVERS.items():
        if "tools" in meta:
            result[name] = meta["tools"]
    return result


def count_mcp_tools() -> int:
    """Count total tools across all MCP servers."""
    return sum(len(meta.get("tools", [])) for meta in MCP_SERVERS.values())
