"""
Plugin Marketplace
==================

Marketplace system for buying and selling trading robot plugins.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from loguru import logger

from plugins.plugin_manager import PluginManager
from plugins.plugin_metadata import PluginMetadata


class Marketplace:
    """Marketplace for trading robot plugins."""

    def __init__(
        self,
        plugin_manager: PluginManager,
        marketplace_directory: str = "data/marketplace",
    ):
        """Initialize marketplace."""
        self.plugin_manager = plugin_manager
        self.marketplace_directory = Path(marketplace_directory)
        self.marketplace_directory.mkdir(parents=True, exist_ok=True)
        self.sales_file = self.marketplace_directory / "sales.jsonl"

    def list_plugins_for_sale(self) -> List[PluginMetadata]:
        """List all plugins available for sale."""
        return self.plugin_manager.get_plugins_for_sale()

    def get_plugin_details(self, plugin_id: str) -> Optional[Dict]:
        """Get detailed information about a plugin for sale."""
        metadata = self.plugin_manager.load_metadata(plugin_id)
        if not metadata or not metadata.is_for_sale:
            return None

        # Get performance data
        plugin = self.plugin_manager.get_plugin(plugin_id)
        performance = None
        if plugin:
            performance = plugin.get_performance_summary()

        return {
            "metadata": metadata.to_dict(),
            "performance": performance,
            "description": metadata.description,
            "parameters": metadata.default_parameters,
            "tags": metadata.tags,
        }

    def purchase_plugin(self, plugin_id: str, buyer_info: Dict) -> bool:
        """Purchase a plugin."""
        metadata = self.plugin_manager.load_metadata(plugin_id)
        if not metadata or not metadata.is_for_sale:
            logger.error(f"Plugin {plugin_id} is not available for sale")
            return False

        # Record sale
        sale_record = {
            "plugin_id": plugin_id,
            "plugin_name": metadata.name,
            "price": metadata.price,
            "currency": metadata.currency,
            "buyer": buyer_info,
            "timestamp": datetime.now().isoformat(),
        }

        with open(self.sales_file, "a") as f:
            f.write(json.dumps(sale_record) + "\n")

        # Update metadata (increment sales count)
        metadata.sales_count += 1
        self._update_metadata(plugin_id, metadata)

        logger.info(
            f"✅ Plugin {plugin_id} purchased by {buyer_info.get('email', 'unknown')}")
        return True

    def _update_metadata(self, plugin_id: str, metadata: PluginMetadata):
        """Update plugin metadata file."""
        metadata_file = (
            self.plugin_manager.plugins_directory / plugin_id / "metadata.json"
        )
        if metadata_file.exists():
            with open(metadata_file, "w") as f:
                json.dump(metadata.to_dict(), f, indent=2, default=str)

    def get_sales_history(self, plugin_id: Optional[str] = None) -> List[Dict]:
        """Get sales history."""
        if not self.sales_file.exists():
            return []

        sales = []
        with open(self.sales_file, "r") as f:
            for line in f:
                if line.strip():
                    sale = json.loads(line)
                    if plugin_id is None or sale.get("plugin_id") == plugin_id:
                        sales.append(sale)

        return sales

    def get_marketplace_stats(self) -> Dict:
        """Get marketplace statistics."""
        plugins_for_sale = self.list_plugins_for_sale()
        total_sales = len(self.get_sales_history())
        total_revenue = sum(
            sale.get("price", 0) for sale in self.get_sales_history()
        )

        return {
            "plugins_for_sale": len(plugins_for_sale),
            "total_sales": total_sales,
            "total_revenue": total_revenue,
            "average_price": (
                sum(p.price for p in plugins_for_sale) / len(plugins_for_sale)
                if plugins_for_sale
                else 0
            ),
        }

