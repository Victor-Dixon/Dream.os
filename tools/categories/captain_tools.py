"""
Captain Operations Tools V2 - Consolidated Facade
===================================================

PHASE 4 CONSOLIDATION: Unified facade for consolidated Captain tool modules.
Reduced from 9 separate files to 4 consolidated modules + facade.

Consolidated Modules:
- captain_tools_core_v2.py: Core operations + architectural checking
- captain_tools_advanced_v2.py: Points calculation + mission assignment + optimization
- captain_tools_monitoring_v2.py: Gas delivery + reporting + briefings
- captain_tools_operations_v2.py: Multi-agent coordination + messaging + dashboards
- captain_tools_utilities_v2.py: Utilities + validation tools

This facade maintains backward compatibility by re-exporting all classes.

V2 Compliance: <400 lines (consolidated facade module)
Author: Agent-2 (Architecture & Design) - Phase 4 Consolidation 2026-01-06

<!-- SSOT Domain: tools -->
"""

# Consolidated core operations (Status, Git, Work, Integrity, Architecture)
from .captain_tools_core_v2 import (
    ArchitecturalCheckerTool,
    GitVerifyTool,
    IntegrityCheckTool,
    StatusCheckTool,
    WorkVerifyTool,
)

# Consolidated advanced operations (Points, Mission, Markov)
from .captain_tools_advanced_v2 import (
    MarkovOptimizerTool,
    MissionAssignTool,
    PointsCalculatorTool,
)

# Consolidated monitoring operations (Gas, Leaderboard, Cycle, Morning Briefing)
from .captain_tools_monitoring_v2 import (
    CycleReportTool,
    GasDeliveryTool,
    LeaderboardUpdateTool,
    MorningBriefingTool,
)

# Consolidated operations tools (Multi-fuel, ROI, Dashboard, Messaging)
from .captain_tools_operations_v2 import (
    MarkovROIRunner,
    MessageAllAgentsTool,
    MultiFuelDelivery,
    SelfMessageTool,
    SwarmStatusDashboard,
)

# Consolidated utilities and validation tools
from .captain_tools_utilities_v2 import (
    FileExistenceValidator,
    FindIdleAgentsTool,
    GasCheckTool,
    PhantomTaskDetector,
    ProjectScanRunner,
    ToolbeltHelpTool,
    UpdateLogTool,
)

# Re-export for backward compatibility (all 24 tools)
__all__ = [
    # Core Operations (5 tools)
    "StatusCheckTool",
    "GitVerifyTool",
    "WorkVerifyTool",
    "IntegrityCheckTool",
    "ArchitecturalCheckerTool",
    # Advanced Operations (3 tools)
    "PointsCalculatorTool",
    "MissionAssignTool",
    "MarkovOptimizerTool",
    # Monitoring Operations (4 tools)
    "GasDeliveryTool",
    "LeaderboardUpdateTool",
    "CycleReportTool",
    "MorningBriefingTool",
    # Operations Tools (5 tools)
    "MultiFuelDelivery",
    "MarkovROIRunner",
    "SwarmStatusDashboard",
    "SelfMessageTool",
    "MessageAllAgentsTool",
    # Utilities & Validation (7 tools)
    "FindIdleAgentsTool",
    "GasCheckTool",
    "UpdateLogTool",
    "ToolbeltHelpTool",
    "FileExistenceValidator",
    "ProjectScanRunner",
    "PhantomTaskDetector",
]
