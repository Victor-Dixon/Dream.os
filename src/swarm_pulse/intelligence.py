"""
<<<<<<< HEAD
<<<<<<< HEAD
Intelligence - Agent Cellphone V2
==================================

SSOT Domain: swarm_brain

Refactored entry point for swarm intelligence operations.
All core logic has been extracted into service architecture for V2 compliance.

Features:
- Partnership suggestion algorithms
- Intelligent routing and coordination
- Collaboration pattern detection
- Coordination efficiency analysis (intelligence_v2.py)

V2 Compliant: Yes (<300 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-07
"""

# Re-export all functions for backward compatibility
from .intelligence_v2 import *

# Re-export intelligence service for advanced usage
from .intelligence_service import IntelligenceService, intelligence_service
=======
<!-- SSOT Domain: swarm_brain -->
=======
Intelligence - Agent Cellphone V2
==================================
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1

SSOT Domain: swarm_brain

Refactored entry point for swarm intelligence operations.
All core logic has been extracted into service architecture for V2 compliance.

Features:
- Partnership suggestion algorithms
- Intelligent routing and coordination
- Collaboration pattern detection
- Coordination efficiency analysis (intelligence_v2.py)

V2 Compliant: Yes (<300 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-07
"""

# Re-export all functions for backward compatibility
from .intelligence_v2 import *

<<<<<<< HEAD
from .intelligence_models import (
    INTELLIGENCE_CONFIG,
    CollaborationPattern,
    CoordinationMetrics,
    PartnershipSuggestion,
)
from .intelligence_scoring import (
    compute_combined_score,
    compute_semantic_similarity,
    create_suggestion,
)
from .models import NotificationLevel, PulseEvent


# ============================================================================
# CORE FUNCTIONS
# ============================================================================
def suggest_partnerships(
    event: PulseEvent,
    *,
    top_k: int = 3,
    threshold: float = 0.6,
) -> List[PartnershipSuggestion]:
    """Suggest bilateral partnerships based on event content."""
    if not INTELLIGENCE_CONFIG["enable_partnership_suggestions"]:
        return []
    try:
        from .vectordb.query import embed_events, get_similar_events

        embeddings = embed_events([event])
        if not embeddings:
            return []

        embedding = embeddings[0]
        similar = get_similar_events(
            embedding,
            top_k=INTELLIGENCE_CONFIG["similarity_top_k"],
            filters={"exclude_agent": event.agent},
        )

        semantic_scores = compute_semantic_similarity(event, similar)
        suggestions: List[PartnershipSuggestion] = []

        for candidate_agent, semantic_sim in semantic_scores.items():
            combined_score = compute_combined_score(
                event, candidate_agent, semantic_sim)
            if combined_score >= threshold:
                suggestion = create_suggestion(
                    event, candidate_agent, combined_score)
                suggestions.append(suggestion)

        suggestions.sort(key=lambda s: s.score, reverse=True)
        return suggestions[:top_k]
    except ImportError:
        return []


def route_with_intelligence(
    event: PulseEvent,
    *,
    use_semantic: bool = True,
    use_tags: bool = True,
) -> Dict[str, NotificationLevel]:
    """Hybrid routing: combine semantic similarity with tag-based rules."""
    if not INTELLIGENCE_CONFIG["enable_semantic_routing"]:
        use_semantic = False

    targets: Dict[str, NotificationLevel] = {}

    if use_tags:
        from .router import _load_tag_matrix, infer_targets

        matrix = _load_tag_matrix()
        tag_targets = infer_targets(event.tags, matrix)
        for agent in tag_targets:
            targets[agent] = event.level

    if use_semantic:
        suggestions = suggest_partnerships(event, top_k=5, threshold=0.5)
        for suggestion in suggestions:
            agent = suggestion.agent_2
            level = suggestion.notification_level
            if agent in targets:
                targets[agent] = max(targets[agent], level,
                                     key=lambda l: l.value)
            else:
                targets[agent] = level

    return targets


def detect_collaboration_patterns(
    time_window: str = "7d",
    *,
    min_events: int = 3,
) -> List[CollaborationPattern]:
    """Detect recurring collaboration patterns (Phase 2C)."""
    if not INTELLIGENCE_CONFIG["enable_pattern_detection"]:
        return []
    return []


def analyze_coordination_efficiency(agent_id: str | None = None) -> CoordinationMetrics:
    """Analyze coordination efficiency metrics (Phase 2C).

    Calculates real metrics from:
    - PulseBus journal (coordination events)
    - Agent status files (bilateral partnerships, gas exchanges)
    - Cycle planner data (ROI tracking)

    Args:
        agent_id: Optional agent ID to filter metrics. If None, calculates swarm-wide metrics.

    Returns:
        CoordinationMetrics with calculated efficiency metrics.
    """
    if not INTELLIGENCE_CONFIG["enable_efficiency_analysis"]:
        return CoordinationMetrics(
            agent_id=agent_id,
            partnership_activation_rate=0.0,
            avg_roi_by_type={},
            avg_coordination_latency=0.0,
            success_rate=0.0,
            force_multiplication_factor=1.0,
        )

    try:
        from datetime import datetime, timedelta
        from pathlib import Path
        import json

        # Load PulseBus journal
        journal_path = Path("swarm_pulse_journal.jsonl")
        coordination_events = []
        partnership_suggestions = []

        if journal_path.exists():
            with journal_path.open("r", encoding="utf-8") as f:
                for line in f:
                    try:
                        event = json.loads(line.strip())
                        event_data = event.get("event", {})
                        event_agent = event_data.get("agent", "")

                        # Filter by agent if specified
                        if agent_id and event_agent != agent_id:
                            continue

                        if event.get("event_type") == "coordination":
                            coordination_events.append(event)
                        elif "partnership" in str(event_data.get("tags", [])).lower():
                            partnership_suggestions.append(event)
                    except (json.JSONDecodeError, KeyError):
                        continue

        # Load agent status files for partnership data
        agent_workspaces = Path("agent_workspaces")
        active_partnerships = set()
        gas_exchanges = []
        roi_by_type: Dict[str, List[float]] = {}

        if agent_workspaces.exists():
            for agent_dir in agent_workspaces.iterdir():
                if not agent_dir.is_dir() or not agent_dir.name.startswith("Agent-"):
                    continue

                status_file = agent_dir / "status.json"
                if not status_file.exists():
                    continue

                try:
                    with status_file.open("r", encoding="utf-8") as f:
                        status_data = json.load(f)

                    # Extract partnerships
                    partnerships = status_data.get(
                        "bilateral_partnerships_active", [])
                    if isinstance(partnerships, list):
                        active_partnerships.update(partnerships)
                    elif isinstance(partnerships, dict):
                        active_partnerships.update(partnerships.keys())

                    # Extract gas exchanges
                    gas_sent = status_data.get("bilateral_gas_sent", [])
                    gas_received = status_data.get("gas_received_from", [])
                    if isinstance(gas_sent, list):
                        gas_exchanges.extend([("sent", g)
                                             for g in gas_sent if g])
                    if isinstance(gas_received, list):
                        gas_exchanges.extend([("received", g)
                                             for g in gas_received if g])

                    # Extract ROI data from cycle deliverables
                    cycle_deliverables = status_data.get(
                        "cycle_30_deliverables", [])
                    if isinstance(cycle_deliverables, list):
                        for deliverable in cycle_deliverables:
                            # Look for ROI mentions in deliverables
                            if isinstance(deliverable, str):
                                if "ROI" in deliverable or "roi" in deliverable:
                                    # Extract ROI values (e.g., "20-35x ROI" -> 27.5)
                                    import re
                                    roi_matches = re.findall(
                                        r'(\d+)[-x](\d+)?x?\s*ROI', deliverable, re.IGNORECASE)
                                    for match in roi_matches:
                                        if len(match) == 2 and match[1]:
                                            avg_roi = (
                                                float(match[0]) + float(match[1])) / 2
                                        else:
                                            avg_roi = float(match[0])

                                        # Categorize by work type
                                        work_type = "general"
                                        if "consolidation" in deliverable.lower():
                                            work_type = "consolidation"
                                        elif "refactoring" in deliverable.lower():
                                            work_type = "refactoring"
                                        elif "analysis" in deliverable.lower():
                                            work_type = "analysis"

                                        if work_type not in roi_by_type:
                                            roi_by_type[work_type] = []
                                        roi_by_type[work_type].append(avg_roi)
                except (json.JSONDecodeError, KeyError, ValueError):
                    continue

        # Calculate metrics
        # 1. Partnership activation rate
        total_suggestions = len(partnership_suggestions)
        activated_partnerships = len(active_partnerships)
        partnership_activation_rate = (
            activated_partnerships / total_suggestions if total_suggestions > 0 else 0.0
        )

        # 2. Average ROI by type
        avg_roi_by_type = {
            work_type: sum(rois) / len(rois) if rois else 0.0
            for work_type, rois in roi_by_type.items()
        }

        # 3. Coordination latency (time between suggestion and response)
        coordination_latencies = []
        if coordination_events:
            # Group coordination events by agent pair
            event_by_pair: Dict[str, List[datetime]] = {}
            for event in coordination_events:
                event_data = event.get("event", {})
                event_agent = event_data.get("agent", "")
                targets = event_data.get("targets", [])
                ts_str = event.get("ts", "")

                try:
                    event_time = datetime.fromisoformat(
                        ts_str.replace("Z", "+00:00"))
                    for target in targets:
                        pair_key = f"{event_agent}↔{target}"
                        if pair_key not in event_by_pair:
                            event_by_pair[pair_key] = []
                        event_by_pair[pair_key].append(event_time)
                except (ValueError, AttributeError):
                    continue

            # Calculate latencies between consecutive events
            for pair, times in event_by_pair.items():
                if len(times) >= 2:
                    times.sort()
                    for i in range(1, len(times)):
                        latency = (times[i] - times[i-1]
                                   ).total_seconds() / 60  # minutes
                        coordination_latencies.append(latency)

        avg_coordination_latency = (
            sum(coordination_latencies) / len(coordination_latencies)
            if coordination_latencies else 0.0
        )

        # 4. Success rate (coordination events with responses)
        total_coordinations = len(coordination_events)
        successful_coordinations = len(
            [e for e in coordination_events if e.get("event", {}).get("targets")])
        success_rate = (
            successful_coordinations / total_coordinations if total_coordinations > 0 else 0.0
        )

        # 5. Force multiplication factor (based on active partnerships)
        # 28 possible bilateral pairs, each active pair contributes to force multiplication
        max_pairs = 28  # 8 agents = 28 bilateral pairs
        active_pairs = len(active_partnerships)
        # Base factor: 1.0 + (active_pairs / max_pairs) * 0.75 (up to 1.75x)
        force_multiplication_factor = 1.0 + (active_pairs / max_pairs) * 0.75

        return CoordinationMetrics(
            agent_id=agent_id,
            partnership_activation_rate=min(partnership_activation_rate, 1.0),
            avg_roi_by_type=avg_roi_by_type,
            avg_coordination_latency=avg_coordination_latency,
            success_rate=min(success_rate, 1.0),
            force_multiplication_factor=force_multiplication_factor,
        )
    except Exception:
        # Fallback to default metrics on any error
        return CoordinationMetrics(
            agent_id=agent_id,
            partnership_activation_rate=0.0,
            avg_roi_by_type={},
            avg_coordination_latency=0.0,
            success_rate=0.0,
            force_multiplication_factor=1.0,
        )


# ============================================================================
# MODULE EXPORTS
# ============================================================================
__all__ = [
    "PartnershipSuggestion",
    "CollaborationPattern",
    "CoordinationMetrics",
    "suggest_partnerships",
    "route_with_intelligence",
    "detect_collaboration_patterns",
    "analyze_coordination_efficiency",
    "INTELLIGENCE_CONFIG",
]
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======
# Re-export intelligence service for advanced usage
from .intelligence_service import IntelligenceService, intelligence_service
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
