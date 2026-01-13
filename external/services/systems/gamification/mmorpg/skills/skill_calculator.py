"""
Skill Calculator - XP and Level Calculations
===========================================

This module handles XP calculations and level progression math.
"""

import math
from typing import Dict, Any


class SkillCalculator:
    """Handles skill progression calculations."""
    
    def __init__(self):
        """Initialize skill calculator."""
        self.base_xp_rate = 100
        self.level_scaling = 1.2
    
    def calculate_level(self, experience_points: int) -> int:
        """Calculate level based on experience points."""
        if experience_points <= 0:
            return 0
        return int(math.sqrt(experience_points / self.base_xp_rate))
    
    def xp_for_level(self, level: int) -> int:
        """Calculate XP required for a specific level."""
        if level <= 0:
            return 0
        return level * level * self.base_xp_rate
    
    def xp_to_next_level(self, current_xp: int) -> int:
        """Calculate XP needed to reach next level."""
        current_level = self.calculate_level(current_xp)
        next_level_xp = self.xp_for_level(current_level + 1)
        return next_level_xp - current_xp 