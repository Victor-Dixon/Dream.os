#!/usr/bin/env python3
"""
SSH Utilities for WordPress Operations
Shared utilities for SSH connections and WordPress CLI operations
"""

import json
import paramiko
import logging
from pathlib import Path
from typing import Dict, Optional, Any, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class SSHConfig:
    """SSH connection configuration"""
    host: str
    username: str
    password: str
    port: int = 22
    wp_path: str = ""

class SSHManager:
    """Manages SSH connections and WordPress CLI operations"""

    def __init__(self, site_key: str = "tradingrobotplug.com"):
        self.site_key = site_key
        self.config = self._load_config()
        self.client: Optional[paramiko.SSHClient] = None

    def _load_config(self) -> Optional[SSHConfig]:
        """Load SSH configuration from credentials file"""
        try:
            repo_root = Path(__file__).resolve().parents[1]
            creds_file = repo_root / ".deploy_credentials" / "sites.json"

            with open(creds_file, 'r') as f:
                creds_data = json.load(f)

            if self.site_key in creds_data:
                config_data = creds_data[self.site_key]
                return SSHConfig(
                    host=config_data["host"],
                    username=config_data["username"],
                    password=config_data["password"],
                    port=config_data.get("port", 22),
                    wp_path=config_data.get("remote_path", "")
                )
        except Exception as e:
            logger.error(f"Failed to load SSH config: {e}")

        return None

    def connect(self) -> bool:
        """Establish SSH connection"""
        if not self.config:
            logger.error("No SSH configuration available")
            return False

        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(
                hostname=self.config.host,
                username=self.config.username,
                password=self.config.password,
                port=self.config.port
            )
            logger.info(f"Connected to {self.config.host}")
            return True
        except Exception as e:
            logger.error(f"SSH connection failed: {e}")
            return False

    def disconnect(self):
        """Close SSH connection"""
        if self.client:
            self.client.close()
            self.client = None
            logger.info("SSH connection closed")

    def execute_wp_cli(self, command: str, allow_root: bool = True) -> Tuple[bool, str, str]:
        """
        Execute WordPress CLI command

        Args:
            command: WP-CLI command (without 'wp' prefix)
            allow_root: Whether to allow root execution

        Returns:
            Tuple of (success, stdout, stderr)
        """
        if not self.client or not self.config:
            return False, "", "No SSH connection"

        try:
            full_command = f"cd {self.config.wp_path} && wp {command}"
            logger.info(f"Executing: {full_command}")

            stdin, stdout, stderr = self.client.exec_command(full_command)
            output = stdout.read().decode()
            error = stderr.read().decode()

            success = len(error.strip()) == 0
            return success, output.strip(), error.strip()

        except Exception as e:
            logger.error(f"WP-CLI execution failed: {e}")
            return False, "", str(e)

    def execute_command(self, command: str) -> Tuple[bool, str, str]:
        """
        Execute arbitrary SSH command

        Args:
            command: Command to execute

        Returns:
            Tuple of (success, stdout, stderr)
        """
        if not self.client:
            return False, "", "No SSH connection"

        try:
            logger.info(f"Executing: {command}")
            stdin, stdout, stderr = self.client.exec_command(command)
            output = stdout.read().decode()
            error = stderr.read().decode()

            success = len(error.strip()) == 0
            return success, output.strip(), error.strip()

        except Exception as e:
            logger.error(f"Command execution failed: {e}")
            return False, "", str(e)

    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.disconnect()


# High-level WordPress operations
def create_wp_page(title: str, slug: str, content: str = "", ssh_manager: Optional[SSHManager] = None) -> bool:
    """Create a WordPress page"""
    if not ssh_manager:
        ssh_manager = SSHManager()

    with ssh_manager:
        success, output, error = ssh_manager.execute_wp_cli(
            f'post create --post_type=page --post_title="{title}" --post_name="{slug}" --post_content="{content}" --post_status=publish'
        )

        if success:
            logger.info(f"Created page: {title}")
            return True
        else:
            logger.error(f"Failed to create page {title}: {error}")
            return False

def update_wp_page(page_id: int, content: str, ssh_manager: Optional[SSHManager] = None) -> bool:
    """Update a WordPress page content"""
    if not ssh_manager:
        ssh_manager = SSHManager()

    with ssh_manager:
        success, output, error = ssh_manager.execute_wp_cli(
            f'post update {page_id} --post_content="{content}"'
        )

        if success:
            logger.info(f"Updated page {page_id}")
            return True
        else:
            logger.error(f"Failed to update page {page_id}: {error}")
            return False

def add_menu_item(menu_slug: str, page_id: int, title: str, ssh_manager: Optional[SSHManager] = None) -> bool:
    """Add page to WordPress menu"""
    if not ssh_manager:
        ssh_manager = SSHManager()

    with ssh_manager:
        success, output, error = ssh_manager.execute_wp_cli(
            f'menu item add-post {menu_slug} {page_id} --title="{title}"'
        )

        if success:
            logger.info(f"Added {title} to {menu_slug} menu")
            return True
        else:
            logger.error(f"Failed to add menu item: {error}")
            return False