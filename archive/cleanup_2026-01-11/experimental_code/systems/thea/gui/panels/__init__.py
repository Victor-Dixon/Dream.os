"""
Thea GUI Panels
===============

Collection of specialized panels for the Thea MMORPG system.
Currently restored: Analytics, Dashboard, Settings panels.
"""

from .analytics_panel import AnalyticsPanel
from .dashboard_panel import DashboardPanel
from .settings_panel import SettingsPanel

# Placeholder classes for panels not yet restored (Phase 1)
class ConversationsPanel:
    def __init__(self): pass

class ContentAnalyticsPanel:
    def __init__(self): pass

class EnhancedAnalyticsPanel:
    def __init__(self): pass

class ResumePanel:
    def __init__(self): pass

class ScraperPanel:
    def __init__(self): pass

class TaskPanel:
    def __init__(self): pass

class QuestLogPanel:
    def __init__(self): pass

class ExportPanel:
    def __init__(self): pass

class EnhancedDevlogPanel:
    def __init__(self): pass

class SkillTreePanel:
    def __init__(self): pass

class WorkflowPanel:
    def __init__(self): pass

__all__ = ["AnalyticsPanel", "DashboardPanel", "SettingsPanel", "ConversationsPanel", "ContentAnalyticsPanel", "EnhancedAnalyticsPanel", "ResumePanel", "ScraperPanel", "TaskPanel", "QuestLogPanel", "ExportPanel", "EnhancedDevlogPanel", "SkillTreePanel", "WorkflowPanel"]