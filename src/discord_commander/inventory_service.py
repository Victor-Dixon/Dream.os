"""
Inventory Service - Agent Cellphone V2
=====================================

SSOT Domain: discord

Core service for managing and displaying systems inventory data.

Features:
- Systems inventory loading and caching
- Tools and services enumeration
- Data formatting and presentation
- Inventory statistics and summaries

V2 Compliant: Yes (<300 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-07
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class InventoryService:
    """
    Service for managing systems inventory data and operations.
    """

    def __init__(self, inventory_file: Optional[Path] = None):
        self.inventory_file = inventory_file or Path("data/systems_inventory.json")
        self._inventory_cache: Optional[Dict[str, Any]] = None

    def load_inventory(self) -> Dict[str, Any]:
        """
        Load and cache the systems inventory.

        Returns:
            Complete inventory dictionary
        """
        if self._inventory_cache is not None:
            return self._inventory_cache

        try:
            if not self.inventory_file.exists():
                logger.warning(f"Inventory file not found: {self.inventory_file}")
                return self._create_empty_inventory()

            with open(self.inventory_file, 'r', encoding='utf-8') as f:
                inventory = json.load(f)

            self._inventory_cache = inventory
            logger.info(f"Loaded inventory with {len(inventory.get('systems', {}))} systems")
            return inventory

        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Error loading inventory: {e}")
            return self._create_empty_inventory()

    def _create_empty_inventory(self) -> Dict[str, Any]:
        """Create empty inventory structure."""
        return {
            "systems": {},
            "tools": [],
            "services": [],
            "version": "2.0",
            "last_updated": None
        }

    def clear_cache(self) -> None:
        """Clear the inventory cache."""
        self._inventory_cache = None
        logger.info("Inventory cache cleared")

    def get_systems_list(self) -> List[Dict[str, Any]]:
        """
        Get list of all systems with basic info.

        Returns:
            List of system dictionaries
        """
        inventory = self.load_inventory()
        systems = inventory.get("systems", {})

        systems_list = []
        for name, data in systems.items():
            systems_list.append({
                "name": name,
                "description": data.get("description", "No description"),
                "category": data.get("category", "Unknown"),
                "status": data.get("status", "Unknown"),
                "version": data.get("version", "Unknown")
            })

        return sorted(systems_list, key=lambda x: x["name"])

    def get_tools_list(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get list of all tools.

        Args:
            limit: Maximum number of tools to return

        Returns:
            List of tool dictionaries
        """
        inventory = self.load_inventory()
        tools = inventory.get("tools", [])

        if limit:
            tools = tools[:limit]

        return tools

    def get_services_list(self) -> List[Dict[str, Any]]:
        """
        Get list of all services.

        Returns:
            List of service dictionaries
        """
        inventory = self.load_inventory()
        services = inventory.get("services", [])

        return services

    def get_system_details(self, system_name: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific system.

        Args:
            system_name: Name of the system

        Returns:
            System details dictionary or None if not found
        """
        inventory = self.load_inventory()
        systems = inventory.get("systems", {})

        return systems.get(system_name)

    def format_systems_overview(self) -> str:
        """
        Format systems list for Discord display.

        Returns:
            Formatted string of systems overview
        """
        systems = self.get_systems_list()

        if not systems:
            return "No systems found in inventory."

        lines = []
        for system in systems:
            status_emoji = "🟢" if system["status"] == "active" else "🟡" if system["status"] == "maintenance" else "🔴"
            lines.append(f"{status_emoji} **{system['name']}** - {system['description'][:50]}...")

        return "\n".join(lines)

    def format_tools_list(self, limit: int = 20) -> str:
        """
        Format tools list for Discord display.

        Args:
            limit: Maximum number of tools to show

        Returns:
            Formatted string of tools list
        """
        tools = self.get_tools_list(limit)

        if not tools:
            return "No tools found in inventory."

        lines = []
        for i, tool in enumerate(tools, 1):
            name = tool.get("name", "Unknown")
            description = tool.get("description", "No description")[:60]
            lines.append(f"{i:2d}. **{name}** - {description}")

        if len(tools) == limit:
            lines.append(f"\n*Showing first {limit} tools. Use limit parameter for more.*")

        return "\n".join(lines)

    def format_services_list(self) -> str:
        """
        Format services list for Discord display.

        Returns:
            Formatted string of services list
        """
        services = self.get_services_list()

        if not services:
            return "No services found in inventory."

        lines = []
        for i, service in enumerate(services, 1):
            name = service.get("name", "Unknown")
            status = service.get("status", "unknown")
            description = service.get("description", "No description")[:50]

            status_emoji = "🟢" if status == "running" else "🟡" if status == "stopped" else "🔴"
            lines.append(f"{i}. {status_emoji} **{name}** - {description}")

        return "\n".join(lines)

    def get_inventory_stats(self) -> Dict[str, Any]:
        """
        Get inventory statistics.

        Returns:
            Statistics dictionary
        """
        inventory = self.load_inventory()

        systems = inventory.get("systems", {})
        tools = inventory.get("tools", [])
        services = inventory.get("services", [])

        # Count active systems
        active_systems = sum(1 for s in systems.values() if s.get("status") == "active")
        active_services = sum(1 for s in services if s.get("status") == "running")

        return {
            "total_systems": len(systems),
            "active_systems": active_systems,
            "total_tools": len(tools),
            "total_services": len(services),
            "active_services": active_services,
            "version": inventory.get("version", "Unknown"),
            "last_updated": inventory.get("last_updated", "Unknown")
        }

# Global service instance
inventory_service = InventoryService()

__all__ = [
    "InventoryService",
    "inventory_service"
]