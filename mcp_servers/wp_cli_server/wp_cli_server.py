#!/usr/bin/env python3
"""
WP-CLI MCP Server Implementation
=================================

<!-- SSOT Domain: web -->

MCP server that provides WordPress CLI operations through standardized tools.
Enables automated WordPress management, plugin/theme operations, and content handling.

V2 Compliance | Author: Agent-1 | Date: 2026-01-16
"""

import json
import logging
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class WPCliError(Exception):
    """Error during WP-CLI operations."""


class WPCliServer:
    """
    MCP Server for WordPress CLI operations.

    Provides tools for:
    - Plugin management (install, activate, deactivate, update)
    - Theme management (install, activate, update)
    - Database operations (export, import, search-replace)
    - Content management (post operations, user management)
    - Core WordPress operations (updates, maintenance)
    """

    def __init__(self, wordpress_path: Optional[Path] = None):
        """
        Initialize WP-CLI server.

        Args:
            wordpress_path: Path to WordPress installation root
        """
        self.wordpress_path = wordpress_path or Path("websites")
        self.wp_cli_command = "wp"

    def _run_wp_cli(self, args: List[str], cwd: Optional[Path] = None) -> Dict[str, Any]:
        """
        Execute WP-CLI command.

        Args:
            args: WP-CLI command arguments
            cwd: Working directory for command execution

        Returns:
            Command result with stdout, stderr, and return code

        Raises:
            WPCliError: If WP-CLI command fails
        """
        command = [self.wp_cli_command] + args

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                cwd=cwd or self.wordpress_path,
                timeout=300  # 5 minute timeout
            )

            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }

        except subprocess.TimeoutExpired:
            raise WPCliError("WP-CLI command timed out after 5 minutes")
        except FileNotFoundError:
            raise WPCliError("WP-CLI not found. Please install WP-CLI.")
        except Exception as e:
            raise WPCliError(f"WP-CLI execution failed: {e}")

    def check_wp_cli_availability(self) -> bool:
        """
        Check if WP-CLI is available and functional.

        Returns:
            True if WP-CLI is available, False otherwise
        """
        try:
            result = self._run_wp_cli(['--version'])
            return result['success']
        except WPCliError:
            return False

    # Plugin Management Tools

    def install_plugin(self, plugin_slug: str, activate: bool = False) -> Dict[str, Any]:
        """
        Install a WordPress plugin.

        Args:
            plugin_slug: Plugin slug from wordpress.org
            activate: Whether to activate after installation

        Returns:
            Installation result
        """
        args = ['plugin', 'install', plugin_slug]

        if activate:
            args.append('--activate')

        result = self._run_wp_cli(args)

        return {
            'tool': 'install_plugin',
            'plugin': plugin_slug,
            'activated': activate,
            'result': result
        }

    def activate_plugin(self, plugin_slug: str) -> Dict[str, Any]:
        """
        Activate a WordPress plugin.

        Args:
            plugin_slug: Plugin slug to activate

        Returns:
            Activation result
        """
        result = self._run_wp_cli(['plugin', 'activate', plugin_slug])

        return {
            'tool': 'activate_plugin',
            'plugin': plugin_slug,
            'result': result
        }

    def deactivate_plugin(self, plugin_slug: str) -> Dict[str, Any]:
        """
        Deactivate a WordPress plugin.

        Args:
            plugin_slug: Plugin slug to deactivate

        Returns:
            Deactivation result
        """
        result = self._run_wp_cli(['plugin', 'deactivate', plugin_slug])

        return {
            'tool': 'deactivate_plugin',
            'plugin': plugin_slug,
            'result': result
        }

    def update_plugin(self, plugin_slug: str) -> Dict[str, Any]:
        """
        Update a WordPress plugin.

        Args:
            plugin_slug: Plugin slug to update

        Returns:
            Update result
        """
        result = self._run_wp_cli(['plugin', 'update', plugin_slug])

        return {
            'tool': 'update_plugin',
            'plugin': plugin_slug,
            'result': result
        }

    def list_plugins(self, status_filter: Optional[str] = None) -> Dict[str, Any]:
        """
        List WordPress plugins.

        Args:
            status_filter: Filter by status (active, inactive, etc.)

        Returns:
            List of plugins
        """
        args = ['plugin', 'list', '--format=json']

        if status_filter:
            args.extend(['--status', status_filter])

        result = self._run_wp_cli(args)

        plugins = []
        if result['success']:
            try:
                plugins = json.loads(result['stdout'])
            except json.JSONDecodeError:
                logger.warning("Failed to parse plugin list JSON")

        return {
            'tool': 'list_plugins',
            'filter': status_filter,
            'plugins': plugins,
            'result': result
        }

    # Theme Management Tools

    def install_theme(self, theme_slug: str, activate: bool = False) -> Dict[str, Any]:
        """
        Install a WordPress theme.

        Args:
            theme_slug: Theme slug from wordpress.org
            activate: Whether to activate after installation

        Returns:
            Installation result
        """
        args = ['theme', 'install', theme_slug]

        if activate:
            args.append('--activate')

        result = self._run_wp_cli(args)

        return {
            'tool': 'install_theme',
            'theme': theme_slug,
            'activated': activate,
            'result': result
        }

    def activate_theme(self, theme_slug: str) -> Dict[str, Any]:
        """
        Activate a WordPress theme.

        Args:
            theme_slug: Theme slug to activate

        Returns:
            Activation result
        """
        result = self._run_wp_cli(['theme', 'activate', theme_slug])

        return {
            'tool': 'activate_theme',
            'theme': theme_slug,
            'result': result
        }

    def update_theme(self, theme_slug: str) -> Dict[str, Any]:
        """
        Update a WordPress theme.

        Args:
            theme_slug: Theme slug to update

        Returns:
            Update result
        """
        result = self._run_wp_cli(['theme', 'update', theme_slug])

        return {
            'tool': 'update_theme',
            'theme': theme_slug,
            'result': result
        }

    # Database Tools

    def db_export(self, output_file: str) -> Dict[str, Any]:
        """
        Export WordPress database.

        Args:
            output_file: Output file path for database dump

        Returns:
            Export result
        """
        result = self._run_wp_cli(['db', 'export', output_file])

        return {
            'tool': 'db_export',
            'output_file': output_file,
            'result': result
        }

    def db_import(self, input_file: str) -> Dict[str, Any]:
        """
        Import WordPress database.

        Args:
            input_file: Input file path for database dump

        Returns:
            Import result
        """
        result = self._run_wp_cli(['db', 'import', input_file])

        return {
            'tool': 'db_import',
            'input_file': input_file,
            'result': result
        }

    def db_search_replace(self, old_value: str, new_value: str,
                         table: Optional[str] = None) -> Dict[str, Any]:
        """
        Search and replace in database.

        Args:
            old_value: Value to search for
            new_value: Value to replace with
            table: Specific table to operate on (optional)

        Returns:
            Search-replace result
        """
        args = ['search-replace', old_value, new_value]

        if table:
            args.extend(['--table', table])

        result = self._run_wp_cli(args)

        return {
            'tool': 'db_search_replace',
            'old_value': old_value,
            'new_value': new_value,
            'table': table,
            'result': result
        }

    # Content Management Tools

    def create_post(self, title: str, content: str = "",
                   post_type: str = 'post', status: str = 'draft') -> Dict[str, Any]:
        """
        Create a new WordPress post.

        Args:
            title: Post title
            content: Post content
            post_type: Post type (post, page, etc.)
            status: Post status (draft, publish, etc.)

        Returns:
            Post creation result
        """
        args = [
            'post', 'create',
            '--post_title', title,
            '--post_content', content,
            '--post_type', post_type,
            '--post_status', status,
            '--porcelain'  # Return only post ID
        ]

        result = self._run_wp_cli(args)

        post_id = None
        if result['success']:
            try:
                post_id = int(result['stdout'].strip())
            except ValueError:
                logger.warning("Failed to parse post ID from WP-CLI output")

        return {
            'tool': 'create_post',
            'title': title,
            'post_type': post_type,
            'status': status,
            'post_id': post_id,
            'result': result
        }

    def update_post(self, post_id: int, title: Optional[str] = None,
                   content: Optional[str] = None) -> Dict[str, Any]:
        """
        Update an existing WordPress post.

        Args:
            post_id: Post ID to update
            title: New title (optional)
            content: New content (optional)

        Returns:
            Post update result
        """
        args = ['post', 'update', str(post_id)]

        if title:
            args.extend(['--post_title', title])
        if content:
            args.extend(['--post_content', content])

        result = self._run_wp_cli(args)

        return {
            'tool': 'update_post',
            'post_id': post_id,
            'title': title,
            'content': content,
            'result': result
        }

    # Core Operations

    def core_update(self) -> Dict[str, Any]:
        """
        Update WordPress core.

        Returns:
            Core update result
        """
        result = self._run_wp_cli(['core', 'update'])

        return {
            'tool': 'core_update',
            'result': result
        }

    def core_check_update(self) -> Dict[str, Any]:
        """
        Check for WordPress core updates.

        Returns:
            Update check result
        """
        result = self._run_wp_cli(['core', 'check-update'])

        return {
            'tool': 'core_check_update',
            'result': result
        }

    # Utility Methods

    def get_site_info(self) -> Dict[str, Any]:
        """
        Get basic WordPress site information.

        Returns:
            Site information
        """
        # Get site URL
        url_result = self._run_wp_cli(['option', 'get', 'siteurl'])
        site_url = url_result['stdout'].strip() if url_result['success'] else 'unknown'

        # Get site title
        title_result = self._run_wp_cli(['option', 'get', 'blogname'])
        site_title = title_result['stdout'].strip() if title_result['success'] else 'unknown'

        # Get WordPress version
        version_result = self._run_wp_cli(['core', 'version'])
        wp_version = version_result['stdout'].strip() if version_result['success'] else 'unknown'

        return {
            'site_url': site_url,
            'site_title': site_title,
            'wordpress_version': wp_version,
            'wp_cli_available': self.check_wp_cli_availability()
        }