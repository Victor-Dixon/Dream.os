<!-- SSOT Domain: core -->
"""
Hardened Agent Activity Detector - V2 Refactored (Handler+Helper Pattern)
==========================================================================

Multi-source activity detection with confidence scoring and cross-validation.
Refactored to use extracted modules:
- ActivitySourceCheckers: Tier 1 checkers (telemetry, git, contracts, tests)
- ActivitySourceCheckersTier2: Tier 2 checkers (status, files, devlogs, inbox)
- activity_detector_helpers: Helper functions (filtering, confidence, validation)

Key Features:
- Multi-source validation (status.json, file mods, telemetry, contracts)
- Confidence scoring (0.0-1.0) based on source reliability
- Cross-validation between detection methods
- Noise filtering (resume prompts, acknowledgments)
- Temporal validation (activity recency checks)

V2 Compliance: Refactored using Handler+Helper pattern
Author: Agent-1 (Integration & Core Systems) / Agent-3 (V2 Refactoring Batch 3)
Date: 2025-01-27 / 2025-12-15
Priority: CRITICAL - Prevents false resume prompts
"""

import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional, Set

from .activity_detector_models import (
    ActivityAssessment,
    ActivitySignal,
)
from .activity_source_checkers import ActivitySourceCheckers
from .activity_source_checkers_tier2 import ActivitySourceCheckersTier2
from .activity_detector_helpers import (
    filter_noise_signals,
    calculate_confidence,
    validate_signals,
)

logger = logging.getLogger(__name__)


class HardenedActivityDetector:
    """
    Hardened activity detector with multi-source validation.

    Uses Handler+Helper pattern:
    - Handler: Orchestrates detection using checker modules
    - Helpers: Provide filtering, confidence calculation, validation
    """

    def __init__(self, workspace_root: Optional[Path] = None):
        """Initialize hardened activity detector."""
        self.workspace_root = workspace_root or Path(".")
        self.agent_workspaces = self.workspace_root / "agent_workspaces"
        self.activity_event_file = Path(
            "runtime") / "agent_comms" / "activity_events.jsonl"

        # Noise patterns to filter out
        self.noise_patterns: Set[str] = {
            "resumer", "stall-recovery", "no-acknowledgments",
            "inactivity detected", "[c2a]", "#no-reply", "#progress-only"
        }

        # Minimum confidence threshold to consider agent active
        self.min_confidence_threshold = 0.5

        # Time windows for activity validation
        self.tier1_window_seconds = 3600  # 1 hour for tier-1 sources
        self.tier2_window_seconds = 1800  # 30 min for tier-2 sources
        self.tier3_window_seconds = 900  # 15 min for tier-3 sources

        # Initialize checker modules
        self.tier1_checkers = ActivitySourceCheckers(
            workspace_root=self.workspace_root,
            agent_workspaces=self.agent_workspaces,
            activity_event_file=self.activity_event_file,
            noise_patterns=self.noise_patterns,
        )

        self.tier2_checkers = ActivitySourceCheckersTier2(
            agent_workspaces=self.agent_workspaces,
            workspace_root=self.workspace_root,
        )

    def assess_agent_activity(
        self,
        agent_id: str,
        lookback_minutes: int = 60
    ) -> ActivityAssessment:
        """
        Assess agent activity with multi-source validation.

        Args:
            agent_id: Agent identifier
            lookback_minutes: How far back to look for activity

        Returns:
            ActivityAssessment with confidence score and validation status
        """
        lookback_time = datetime.now() - timedelta(minutes=lookback_minutes)
        signals: List[ActivitySignal] = []

        # Collect signals from Tier 1 sources (most reliable)
        signals.extend(self.tier1_checkers.check_telemetry_events(
            agent_id, lookback_time))
        signals.extend(self.tier1_checkers.check_git_activity(
            agent_id, lookback_time))
        signals.extend(self.tier1_checkers.check_git_activity_by_path(
            agent_id, lookback_time))
        signals.extend(self.tier1_checkers.check_contract_activity(
            agent_id, lookback_time))
        signals.extend(self.tier1_checkers.check_test_execution(
            agent_id, lookback_time))

        # Collect signals from Tier 2 sources (moderately reliable)
        signals.extend(self.tier2_checkers.check_status_updates(
            agent_id, lookback_time))
        signals.extend(self.tier2_checkers.check_file_modifications(
            agent_id, lookback_time))
        signals.extend(self.tier2_checkers.check_devlog_activity(
            agent_id, lookback_time))
        signals.extend(self.tier2_checkers.check_inbox_processing(
            agent_id, lookback_time))

        # Filter out noise using helper
        signals = filter_noise_signals(signals, self.noise_patterns)

        # Sort by timestamp (most recent first)
        signals.sort(key=lambda s: s.timestamp, reverse=True)

        # Calculate overall confidence using helper
        confidence, reasons = calculate_confidence(signals, lookback_time)

        # Determine if agent is active
        last_activity = None
        if signals:
            last_activity = datetime.fromtimestamp(signals[0].timestamp)

        inactivity_minutes = (
            (datetime.now() - last_activity).total_seconds() / 60
            if last_activity else float("inf")
        )

        # Cross-validation: Check if signals are consistent using helper
        validation_passed = validate_signals(signals, lookback_time)

        # Final determination
        is_active = (
            confidence >= self.min_confidence_threshold and
            validation_passed and
            last_activity is not None and
            last_activity >= lookback_time
        )

        return ActivityAssessment(
            agent_id=agent_id,
            is_active=is_active,
            confidence=confidence,
            last_activity=last_activity,
            inactivity_minutes=inactivity_minutes,
            signals=signals,
            validation_passed=validation_passed,
            reasons=reasons
        )


__all__ = [
    "HardenedActivityDetector",
    "ActivityAssessment",
]
