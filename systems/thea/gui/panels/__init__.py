"""
Thea GUI Panels
===============

Collection of specialized panels for the Thea MMORPG system.
Currently restored: Analytics, Dashboard, Settings panels.
"""

from .analytics_panel import AnalyticsPanel
from .dashboard_panel import DashboardPanel
from .settings_panel import SettingsPanel

__all__ = ["AnalyticsPanel", "DashboardPanel", "SettingsPanel"]