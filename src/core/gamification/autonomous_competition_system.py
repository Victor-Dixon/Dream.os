#!/usr/bin/env python3
# Header-Variant: full
# Owner: Dream.os Platform
# Purpose: Autonomous competition system.
# SSOT: docs/recovery/recovery_registry.yaml

"""
<!-- SSOT Domain: core -->

Autonomous Development Competition System
=========================================

Gamification system to drive proactive autonomous agent development.
Balances healthy competition with cooperative swarm intelligence.

Based on Captain's insight: Competition drives proactive behavior essential
for autonomous development.

**V2 REFACTORED**: Split into modular components (C-055-4)
- system_core.py: Core competition logic
- achievements.py: Achievement tracking
- leaderboard.py: Leaderboard management
- competition_storage.py: Persistence

Author: Captain Agent-4
Mission: Implement competition for autonomous development
Refactored: C-055-4 V2 Compliance (350L → 3 files <200L each)
License: MIT

@file Autonomous competition system.
@summary Autonomous competition system.
@registry docs/recovery/recovery_registry.yaml#unregistered-src-core-gamification-autonomous-competition-system
"""

# Re-export all public API from refactored modules
from .achievements import Achievement, AchievementType, AgentScore, ScoringCalculator
from .competition_storage import load_scores, save_scores, update_ranks
from .leaderboard import LeaderboardManager
from .system_core import AutonomousCompetitionSystem, CompetitionMode, get_competition_system

__all__ = [
    # Core system
    "AutonomousCompetitionSystem",
    "CompetitionMode",
    "get_competition_system",
    # Achievements
    "Achievement",
    "AchievementType",
    "AgentScore",
    "ScoringCalculator",
    # Leaderboard
    "LeaderboardManager",
    # Storage
    "load_scores",
    "save_scores",
    "update_ranks",
]
