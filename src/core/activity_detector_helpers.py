#!/usr/bin/env python3
"""
Activity Detector Helpers
=========================

Helper functions for activity detection:
- Signal filtering (noise removal)
- Confidence calculation
- Signal validation

<!-- SSOT Domain: infrastructure -->

V2 Compliance: <300 lines | Author: Agent-3 | Date: 2025-12-15
"""

import json
import logging
import time
from datetime import datetime
from typing import List, Set, Tuple

from .activity_detector_models import (
    ActivityConfidence,
    ActivitySignal,
)

logger = logging.getLogger(__name__)


def filter_noise_signals(
    signals: List[ActivitySignal],
    noise_patterns: Set[str]
) -> List[ActivitySignal]:
    """Filter out noise signals (resume prompts, acknowledgments)."""
    filtered = []

    for signal in signals:
        metadata_str = json.dumps(signal.metadata).lower()
        # Skip if contains noise patterns
        if any(noise in metadata_str for noise in noise_patterns):
            continue
        filtered.append(signal)

    return filtered


def calculate_confidence(
    signals: List[ActivitySignal],
    lookback_time: datetime
) -> Tuple[float, List[str]]:
    """
    Calculate overall confidence score from signals.

    Returns:
        (confidence_score, reasons)
    """
    if not signals:
        return 0.0, ["No activity signals detected"]

    # Group signals by tier
    tier1_signals = [s for s in signals if s.source.tier == 1]
    tier2_signals = [s for s in signals if s.source.tier == 2]
    tier3_signals = [s for s in signals if s.source.tier == 3]

    reasons = []
    confidence = 0.0

    # Tier 1 signals are most reliable
    if tier1_signals:
        # Multiple tier-1 signals = very high confidence
        if len(tier1_signals) >= 2:
            confidence = ActivityConfidence.VERY_HIGH.value
            reasons.append(f"Multiple tier-1 signals ({len(tier1_signals)})")
        else:
            confidence = ActivityConfidence.HIGH.value
            reasons.append(f"Tier-1 signal: {tier1_signals[0].source.name}")

    # Tier 2 signals boost confidence
    elif tier2_signals:
        if len(tier2_signals) >= 2:
            confidence = ActivityConfidence.HIGH.value
            reasons.append(f"Multiple tier-2 signals ({len(tier2_signals)})")
        else:
            confidence = ActivityConfidence.MEDIUM.value
            reasons.append(f"Tier-2 signal: {tier2_signals[0].source.name}")

    # Tier 3 signals provide low confidence
    elif tier3_signals:
        confidence = ActivityConfidence.LOW.value
        reasons.append(f"Tier-3 signal: {tier3_signals[0].source.name}")

    # Apply recency penalty
    if signals:
        most_recent = signals[0]
        age_seconds = time.time() - most_recent.timestamp

        if age_seconds > 3600:  # > 1 hour old
            confidence *= 0.7
            reasons.append("Activity is >1 hour old")
        elif age_seconds > 1800:  # > 30 min old
            confidence *= 0.85
            reasons.append("Activity is >30 min old")

    return min(confidence, 1.0), reasons


def validate_signals(
    signals: List[ActivitySignal],
    lookback_time: datetime
) -> bool:
    """
    Cross-validate signals for consistency.

    Returns:
        True if signals are consistent and valid
    """
    if not signals:
        return False

    # Check temporal consistency (signals should be within reasonable time window)
    timestamps = [s.timestamp for s in signals]
    time_span = max(timestamps) - min(timestamps)

    # If signals span >24 hours, might be stale data
    if time_span > 86400:
        logger.debug("Signals span >24 hours, may be stale")
        return False

    # Check if most recent signal is within lookback window
    most_recent = max(timestamps)
    if most_recent < lookback_time.timestamp():
        return False

    # Require at least one signal from tier 1 or 2
    has_reliable_signal = any(
        s.source.tier <= 2 for s in signals
    )

    return has_reliable_signal
