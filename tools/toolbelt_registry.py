"""
Toolbelt Registry - Tool Registry and Management
===============================================

Provides TOOLS_REGISTRY and ToolRegistry for toolbelt operations.

Author: Agent-7 (Web Development Specialist)
Date: 2026-01-04
"""

import logging
from typing import Dict, Any, List, Optional
from pathlib import Path
import sys

logger = logging.getLogger(__name__)

# Import toolbelt core
try:
    from .toolbelt_core import get_toolbelt_core
except ImportError:
    # Fallback for direct import
    sys.path.insert(0, str(Path(__file__).parent))
    from toolbelt_core import get_toolbelt_core


class ToolRegistry:
    """Registry for managing toolbelt tools."""

    def __init__(self):
        """Initialize tool registry."""
        self._core = get_toolbelt_core()
        self._tool_cache = {}

    def list_tools(self) -> List[str]:
        """List all available tools."""
        try:
            return self._core.list_tools()
        except Exception as e:
            logger.warning(f"Failed to list tools: {e}")
            return []

    def list_by_category(self, category: str) -> List[str]:
        """List tools in a specific category."""
        try:
            categories = self._core.list_categories()
            return categories.get(category, [])
        except Exception as e:
            logger.warning(f"Failed to list tools by category {category}: {e}")
            return []

    def get_categories(self) -> List[str]:
        """Get all available categories."""
        try:
            categories = self._core.list_categories()
            return list(categories.keys())
        except Exception as e:
            logger.warning(f"Failed to get categories: {e}")
            return []

    def get_tool_info(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific tool."""
        if tool_name in self._tool_cache:
            return self._tool_cache[tool_name]

        try:
            help_text = self._core.get_tool_help(tool_name)
            info = {
                "name": tool_name,
                "help": help_text,
                "available": True
            }
            self._tool_cache[tool_name] = info
            return info
        except Exception as e:
            logger.warning(f"Failed to get tool info for {tool_name}: {e}")
            return None

    def run_tool(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Run a tool with given parameters."""
        try:
            result = self._core.run(tool_name, params)
            return {
                "success": result.success,
                "output": result.output,
                "exit_code": result.exit_code,
                "error_message": result.error_message,
                "execution_time": result.execution_time
            }
        except Exception as e:
            logger.error(f"Failed to run tool {tool_name}: {e}")
            return {
                "success": False,
                "output": None,
                "exit_code": 1,
                "error_message": str(e),
                "execution_time": 0
            }


# Global registry instance
TOOLS_REGISTRY = ToolRegistry()

# Export the registry instance and class
__all__ = ['TOOLS_REGISTRY', 'ToolRegistry']