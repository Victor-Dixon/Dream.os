#!/usr/bin/env python3
"""
Agent Activity Detector - Multi-Source Activity Monitoring
==========================================================

Monitors agent activity from multiple sources to detect when agents are active or inactive.
Integrates with resumer prompt system to send prompts when agents are inactive.

Activity Sources:
- status.json updates (last_updated timestamp)
- File modifications in agent workspace
- Devlog creation (devlogs/ directory)
- Inbox messages sent/received
- Task claims (cycle planner)
- Git commits (if agent workspace is a git repo)
- Message queue activity (if agent has messages)

Author: Agent-6 (Coordination & Communication Specialist)
Created: 2025-11-30
Priority: HIGH - Improves agent activity detection
V2 Compliant: Yes
<!-- SSOT Domain: infrastructure -->
"""

import json
import logging
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)

ACTIVITY_EVENT_FILE = Path("runtime") / "agent_comms" / "activity_events.jsonl"
DEFAULT_EVENT_WINDOW_SECONDS = 3600
EVENT_WEIGHTS = {
    "TASK_COMPLETED": 5,
    "GIT_PUSH": 5,
    "MONEY_METRIC": 5,
    "TOOL_RUN_SUCCESS": 2,
    "TOOL_RUN_FAILURE": 4,
    "BRAIN_WRITE": 3,
    "TASK_CLAIMED": 1,
    "DEVLOG_CREATED": 1,
}
TIER1_EVENT_TYPES = {"TASK_COMPLETED", "GIT_PUSH", "MONEY_METRIC", "TOOL_RUN_FAILURE"}


@dataclass
class AgentActivity:
    """Represents agent activity from a single source."""
    agent_id: str
    source: str  # 'status', 'file', 'devlog', 'inbox', 'task', 'git', 'message'
    timestamp: datetime
    action: str  # Description of the action
    metadata: Optional[Dict] = None


@dataclass
class AgentActivitySummary:
    """Summary of agent activity across all sources."""
    agent_id: str
    last_activity: Optional[datetime]
    activity_sources: List[str]  # Which sources detected activity
    is_active: bool
    inactivity_duration_minutes: float
    recent_actions: List[str]  # Recent action descriptions


@dataclass
class ActivityEvent:
    """Represents a single telemetry event emitted by ActivityEmitter."""
    agent_id: str
    event_type: str
    source: str
    summary: str
    artifact: Optional[Dict]
    timestamp: datetime


@dataclass
class ActivitySignal:
    """Calculated activity signal derived from telemetry events."""
    active: bool
    score: float
    tier1_hits: int
    tier2_hits: int
    last_event: Optional[datetime]
    inactivity_minutes: float
    activities: List[AgentActivity]
    event_count: int
    used_events: bool


class AgentActivityDetector:
    """Detects agent activity from multiple sources."""
    
    def __init__(self, workspace_root: Optional[Path] = None):
        """Initialize activity detector.
        
        Args:
            workspace_root: Root directory for agent workspaces
        """
        self.workspace_root = Path(workspace_root) if workspace_root else Path("agent_workspaces")
        self.devlogs_dir = Path("devlogs")
        self.cycle_planner_dir = self.workspace_root / "swarm_cycle_planner" / "cycles"
        self.activity_event_file = ACTIVITY_EVENT_FILE
        
    def detect_agent_activity(
        self,
        agent_id: str,
        lookback_minutes: int = 60,
        use_events: bool = True,
        activity_threshold: int = 3
    ) -> AgentActivitySummary:
        """
        Detect agent activity from all sources.
        
        Args:
            agent_id: Agent identifier
            lookback_minutes: How far back to look for activity
            use_events: Include ActivityEmitter telemetry when available
            activity_threshold: Minimum score to consider agent active from telemetry
            
        Returns:
            AgentActivitySummary with activity information
        """
        lookback_time = datetime.now() - timedelta(minutes=lookback_minutes)
        activities: List[AgentActivity] = []

        event_signal = self._build_event_signal(
            agent_id,
            lookback_time,
            activity_threshold=activity_threshold,
        ) if use_events else ActivitySignal(
            active=False,
            score=0,
            tier1_hits=0,
            tier2_hits=0,
            last_event=None,
            inactivity_minutes=float("inf"),
            activities=[],
            event_count=0,
            used_events=False,
        )

        # ActivityEmitter telemetry events (preferred)
        if event_signal.activities:
            activities.extend(event_signal.activities)

        # Check all activity sources
        activities.extend(self._check_status_updates(agent_id, lookback_time))
        activities.extend(self._check_file_modifications(agent_id, lookback_time))
        activities.extend(self._check_devlog_creation(agent_id, lookback_time))
        activities.extend(self._check_inbox_activity(agent_id, lookback_time))
        activities.extend(self._check_task_claims(agent_id, lookback_time))
        activities.extend(self._check_git_commits(agent_id, lookback_time))
        activities.extend(self._check_message_queue_activity(agent_id, lookback_time))
        
        # Sort by timestamp (most recent first)
        activities.sort(key=lambda x: x.timestamp, reverse=True)
        
        # Determine meaningful activity (filters out chat/noise)
        meaningful_activities = [
            a for a in activities if self._is_meaningful_activity(a)
        ]
        last_activity = meaningful_activities[0].timestamp if meaningful_activities else None
        is_active = last_activity is not None and last_activity >= lookback_time
        inactivity_duration = (
            (datetime.now() - last_activity).total_seconds() / 60
            if last_activity else float("inf")
        )

        # Prefer ActivityEmitter telemetry for activity signal when available
        if event_signal.used_events and event_signal.event_count > 0:
            last_activity = event_signal.last_event or last_activity
            inactivity_duration = event_signal.inactivity_minutes
            is_active = event_signal.active

        # Get unique activity sources (full picture) and recent actions (prioritize meaningful)
        activity_sources = list(set(a.source for a in activities))
        
        recent_pool = meaningful_activities if meaningful_activities else activities
        recent_actions = [a.action for a in recent_pool[:5]]
        
        return AgentActivitySummary(
            agent_id=agent_id,
            last_activity=last_activity,
            activity_sources=activity_sources,
            is_active=is_active,
            inactivity_duration_minutes=inactivity_duration,
            recent_actions=recent_actions
        )
    
    def is_active(
        self,
        agent_id: str,
        window_s: int = DEFAULT_EVENT_WINDOW_SECONDS,
        activity_threshold: int = 3
    ) -> bool:
        """
        Return True if agent is considered active within the window using telemetry first.

        Args:
            agent_id: Agent identifier
            window_s: Time window (seconds) to inspect telemetry
            activity_threshold: Minimum score to consider active when no tier1 events
        """
        lookback_time = datetime.now() - timedelta(seconds=window_s)
        event_signal = self._build_event_signal(
            agent_id,
            lookback_time,
            activity_threshold=activity_threshold,
        )
        if event_signal.used_events and event_signal.event_count > 0:
            return event_signal.active

        # Fallback to legacy heuristics if telemetry not available
        fallback_minutes = max(1, int(window_s / 60))
        summary = self.detect_agent_activity(
            agent_id,
            lookback_minutes=fallback_minutes,
            use_events=False,
            activity_threshold=activity_threshold,
        )
        return summary.is_active

    def _check_status_updates(
        self,
        agent_id: str,
        lookback_time: datetime
    ) -> List[AgentActivity]:
        """Check status.json updates."""
        activities = []
        status_file = self.workspace_root / agent_id / "status.json"
        
        if not status_file.exists():
            return activities
        
        try:
            mtime = datetime.fromtimestamp(status_file.stat().st_mtime)
            if mtime >= lookback_time:
                # Read status to get last_updated field
                with open(status_file, 'r', encoding='utf-8') as f:
                    status = json.load(f)
                    last_updated_str = status.get("last_updated", "")
                    
                    # Parse last_updated timestamp
                    try:
                        last_updated = datetime.strptime(last_updated_str, "%Y-%m-%d %H:%M:%S")
                        if last_updated >= lookback_time:
                            activities.append(AgentActivity(
                                agent_id=agent_id,
                                source="status",
                                timestamp=last_updated,
                                action=f"Status updated: {status.get('current_mission', 'Unknown')[:50]}",
                                metadata={"status": status.get("status"), "mission": status.get("current_mission")}
                            ))
                    except ValueError:
                        # Fallback to file mtime
                        activities.append(AgentActivity(
                            agent_id=agent_id,
                            source="status",
                            timestamp=mtime,
                            action="Status file modified",
                            metadata={"file_mtime": mtime.isoformat()}
                        ))
        except Exception as e:
            logger.warning(f"Error checking status updates for {agent_id}: {e}")
        
        return activities
    
    def _check_file_modifications(
        self,
        agent_id: str,
        lookback_time: datetime
    ) -> List[AgentActivity]:
        """Check file modifications in agent workspace."""
        activities = []
        agent_dir = self.workspace_root / agent_id
        
        if not agent_dir.exists():
            return activities
        
        try:
            # Check files in workspace (excluding status.json which is checked separately)
            for file_path in agent_dir.rglob("*"):
                if file_path.is_file() and file_path.name != "status.json":
                    try:
                        mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                        if mtime >= lookback_time:
                            relative_path = file_path.relative_to(agent_dir)
                            activities.append(AgentActivity(
                                agent_id=agent_id,
                                source="file",
                                timestamp=mtime,
                                action=f"File modified: {relative_path}",
                                metadata={"file": str(relative_path), "size": file_path.stat().st_size}
                            ))
                    except (OSError, PermissionError):
                        continue
        except Exception as e:
            logger.warning(f"Error checking file modifications for {agent_id}: {e}")
        
        return activities
    
    def _check_devlog_creation(
        self,
        agent_id: str,
        lookback_time: datetime
    ) -> List[AgentActivity]:
        """Check devlog creation."""
        activities = []
        
        if not self.devlogs_dir.exists():
            return activities
        
        try:
            # Look for devlogs with agent ID in filename
            pattern = f"*{agent_id.lower()}*.md"
            for devlog_file in self.devlogs_dir.glob(pattern):
                try:
                    mtime = datetime.fromtimestamp(devlog_file.stat().st_mtime)
                    if mtime >= lookback_time:
                        activities.append(AgentActivity(
                            agent_id=agent_id,
                            source="devlog",
                            timestamp=mtime,
                            action=f"Devlog created: {devlog_file.name}",
                            metadata={"file": devlog_file.name}
                        ))
                except (OSError, PermissionError):
                    continue
        except Exception as e:
            logger.warning(f"Error checking devlog creation for {agent_id}: {e}")
        
        return activities
    
    def _check_inbox_activity(
        self,
        agent_id: str,
        lookback_time: datetime
    ) -> List[AgentActivity]:
        """Check inbox message activity (sent/received)."""
        activities = []
        inbox_dir = self.workspace_root / agent_id / "inbox"
        
        if not inbox_dir.exists():
            return activities
        
        try:
            # Check for new messages in inbox
            for message_file in inbox_dir.glob("*.md"):
                try:
                    mtime = datetime.fromtimestamp(message_file.stat().st_mtime)
                    if mtime >= lookback_time:
                        # Try to read message to determine if sent or received
                        try:
                            with open(message_file, 'r', encoding='utf-8') as f:
                                content = f.read(500)  # Read first 500 chars
                                if f"To: {agent_id}" in content:
                                    action = f"Message received: {message_file.name}"
                                elif f"From: {agent_id}" in content:
                                    action = f"Message sent: {message_file.name}"
                                else:
                                    action = f"Inbox activity: {message_file.name}"
                        except Exception:
                            action = f"Inbox file modified: {message_file.name}"
                        
                        activities.append(AgentActivity(
                            agent_id=agent_id,
                            source="inbox",
                            timestamp=mtime,
                            action=action,
                            metadata={"file": message_file.name}
                        ))
                except (OSError, PermissionError):
                    continue
        except Exception as e:
            logger.warning(f"Error checking inbox activity for {agent_id}: {e}")
        
        return activities
    
    def _check_task_claims(
        self,
        agent_id: str,
        lookback_time: datetime
    ) -> List[AgentActivity]:
        """Check task claims from cycle planner."""
        activities = []
        
        if not self.cycle_planner_dir.exists():
            return activities
        
        try:
            # Look for cycle planner files with agent ID
            pattern = f"*_{agent_id.lower()}_*.json"
            for cycle_file in self.cycle_planner_dir.glob(pattern):
                try:
                    mtime = datetime.fromtimestamp(cycle_file.stat().st_mtime)
                    if mtime >= lookback_time:
                        # Read cycle file to check for claimed tasks
                        try:
                            with open(cycle_file, 'r', encoding='utf-8') as f:
                                data = json.load(f)
                                contracts = data.get("contracts", [])
                                claimed = [c for c in contracts if c.get("status", "").upper() == "CLAIMED"]
                                if claimed:
                                    activities.append(AgentActivity(
                                        agent_id=agent_id,
                                        source="task",
                                        timestamp=mtime,
                                        action=f"Task claimed: {claimed[0].get('title', 'Unknown')[:50]}",
                                        metadata={"contracts": len(claimed), "file": cycle_file.name}
                                    ))
                        except Exception:
                            activities.append(AgentActivity(
                                agent_id=agent_id,
                                source="task",
                                timestamp=mtime,
                                action="Cycle planner file modified",
                                metadata={"file": cycle_file.name}
                            ))
                except (OSError, PermissionError):
                    continue
        except Exception as e:
            logger.warning(f"Error checking task claims for {agent_id}: {e}")
        
        return activities
    
    def _check_git_commits(
        self,
        agent_id: str,
        lookback_time: datetime
    ) -> List[AgentActivity]:
        """Check git commits in agent workspace (if it's a git repo)."""
        activities = []
        agent_dir = self.workspace_root / agent_id
        
        if not (agent_dir / ".git").exists():
            return activities
        
        try:
            import subprocess
            # Get recent commits
            result = subprocess.run(
                ["git", "log", "--since", lookback_time.isoformat(), "--format=%H|%ai|%s"],
                cwd=agent_dir,
                capture_output=True,
                text=True,
                timeout=TimeoutConstants.HTTP_QUICK
            )
            
            if result.returncode == 0:
                for line in result.stdout.strip().split("\n"):
                    if line:
                        parts = line.split("|", 2)
                        if len(parts) >= 3:
                            commit_hash, commit_date, commit_msg = parts
                            try:
                                commit_time = datetime.strptime(commit_date, "%Y-%m-%d %H:%M:%S %z")
                                # Remove timezone for comparison
                                commit_time = commit_time.replace(tzinfo=None)
                                if commit_time >= lookback_time:
                                    activities.append(AgentActivity(
                                        agent_id=agent_id,
                                        source="git",
                                        timestamp=commit_time,
                                        action=f"Git commit: {commit_msg[:50]}",
                                        metadata={"hash": commit_hash[:8], "message": commit_msg}
                                    ))
                            except ValueError:
                                continue
        except Exception as e:
            # Git not available or not a git repo - silently skip
            pass
        
        return activities
    
    def _check_message_queue_activity(
        self,
        agent_id: str,
        lookback_time: datetime
    ) -> List[AgentActivity]:
        """Check message queue activity for agent."""
        activities = []
        
        # Check if message queue exists
        queue_file = Path("data") / "message_queue.json"
        if not queue_file.exists():
            return activities
        
        try:
            with open(queue_file, 'r', encoding='utf-8') as f:
                queue_data = json.load(f)
            
            messages = queue_data.get("messages", [])
            resume_markers = {"RESUMER PROMPT", "Inactivity Detected", "STALL-RECOVERY", "NO-ACKNOWLEDGMENTS"}
            for msg in messages:
                # Check if message is for this agent
                recipient = msg.get("recipient", "")
                if agent_id.lower() in recipient.lower():
                    # Check message timestamp
                    msg_time_str = msg.get("timestamp", "")
                    msg_text = msg.get("message", "") or ""
                    msg_type = (msg.get("message_type") or "").lower()
                    # Skip resumer/control messages to avoid counting as progress
                    if any(marker in msg_text for marker in resume_markers) or "resume" in msg_type:
                        continue
                    try:
                        msg_time = datetime.fromisoformat(msg_time_str.replace("Z", "+00:00"))
                        msg_time = msg_time.replace(tzinfo=None)
                        if msg_time >= lookback_time:
                            activities.append(AgentActivity(
                                agent_id=agent_id,
                                source="message",
                                timestamp=msg_time,
                                action=f"Message queued: {msg.get('message_type', 'unknown')}",
                                metadata={"message_id": msg.get("message_id"), "type": msg.get("message_type")}
                            ))
                    except (ValueError, AttributeError):
                        continue
        except Exception as e:
            logger.warning(f"Error checking message queue activity for {agent_id}: {e}")
        
        return activities

    def _is_meaningful_activity(self, activity: AgentActivity) -> bool:
        """Return True if activity represents real progress (not chat/ack)."""
        if activity.source == "activity_event":
            meta = activity.metadata or {}
            tier = meta.get("tier")
            weight = meta.get("weight", 0)
            return tier == 1 or weight >= 2
        if activity.source in {"file", "devlog", "task", "git"}:
            return True
        if activity.source == "status":
            # Require structured metadata and non-empty mission/status to count
            meta = activity.metadata or {}
            mission = meta.get("mission") or ""
            status_val = meta.get("status") or ""
            return bool(mission.strip() or status_val.strip())
        # Inbox/message queue events are considered noise for progress
        return False

    def _load_activity_events(
        self,
        agent_id: str,
        lookback_time: datetime
    ) -> List[ActivityEvent]:
        """Load ActivityEmitter events for the agent within the lookback window."""
        if not self.activity_event_file.exists():
            return []

        events: List[ActivityEvent] = []
        try:
            with open(self.activity_event_file, "r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip():
                        continue
                    try:
                        raw = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    if raw.get("agent", "").lower() != agent_id.lower():
                        continue

                    ts_raw = raw.get("ts")
                    if not ts_raw:
                        continue
                    try:
                        ts = datetime.fromisoformat(
                            str(ts_raw).replace("Z", "+00:00")
                        ).replace(tzinfo=None)
                    except Exception:
                        continue

                    if ts < lookback_time:
                        continue

                    events.append(ActivityEvent(
                        agent_id=agent_id,
                        event_type=(raw.get("type") or "").upper(),
                        source=raw.get("source") or "",
                        summary=raw.get("summary") or "",
                        artifact=raw.get("artifact"),
                        timestamp=ts,
                    ))
        except Exception as e:
            logger.warning(f"Error reading activity events for {agent_id}: {e}")

        events.sort(key=lambda e: e.timestamp, reverse=True)
        return events

    def _normalize_event(
        self,
        event: ActivityEvent
    ) -> Tuple[str, int, int]:
        """Normalize event type into weighted category and tier."""
        base_type = (event.event_type or "").upper()
        normalized_type = base_type
        tier = 2

        if base_type == "TOOL_RUN":
            artifact = event.artifact or {}
            outcome_text = (
                str(artifact.get("outcome") or artifact.get("status") or "") or event.summary
            )
            outcome_lower = outcome_text.lower()
            if "fail" in outcome_lower or "error" in outcome_lower or "timeout" in outcome_lower:
                normalized_type = "TOOL_RUN_FAILURE"
                tier = 1
            else:
                normalized_type = "TOOL_RUN_SUCCESS"
                tier = 2
        elif base_type in TIER1_EVENT_TYPES:
            normalized_type = base_type
            tier = 1
        else:
            normalized_type = base_type or "UNKNOWN"
            tier = 2

        weight = EVENT_WEIGHTS.get(normalized_type, EVENT_WEIGHTS.get(base_type, 0))
        return normalized_type, weight, tier

    def _event_to_activity(
        self,
        event: ActivityEvent,
        normalized_type: str,
        weight: int,
        tier: int
    ) -> AgentActivity:
        """Convert ActivityEvent into AgentActivity for unified summaries."""
        action = f"{normalized_type}: {event.summary or event.source or 'activity detected'}"
        metadata = {
            "type": normalized_type,
            "raw_type": event.event_type,
            "source": event.source,
            "weight": weight,
            "tier": tier,
        }
        if event.artifact is not None:
            metadata["artifact"] = event.artifact

        return AgentActivity(
            agent_id=event.agent_id,
            source="activity_event",
            timestamp=event.timestamp,
            action=action[:120],
            metadata=metadata,
        )

    def _build_event_signal(
        self,
        agent_id: str,
        lookback_time: datetime,
        activity_threshold: int = 3
    ) -> ActivitySignal:
        """Compute activity signal from telemetry events."""
        events = self._load_activity_events(agent_id, lookback_time)
        score = 0
        tier1_hits = 0
        tier2_hits = 0
        activity_records: List[AgentActivity] = []

        for event in events:
            normalized_type, weight, tier = self._normalize_event(event)
            score += weight
            if tier == 1:
                tier1_hits += 1
            else:
                tier2_hits += 1

            activity_records.append(self._event_to_activity(
                event,
                normalized_type,
                weight,
                tier,
            ))

        last_event = events[0].timestamp if events else None
        inactivity_minutes = (
            (datetime.now() - last_event).total_seconds() / 60
            if last_event else float("inf")
        )
        active = bool(events) and (tier1_hits > 0 or score >= activity_threshold)

        return ActivitySignal(
            active=active,
            score=score,
            tier1_hits=tier1_hits,
            tier2_hits=tier2_hits,
            last_event=last_event,
            inactivity_minutes=inactivity_minutes,
            activities=activity_records,
            event_count=len(events),
            used_events=True,
        )
    
    def find_inactive_agents(
        self,
        inactivity_threshold_minutes: float = 30.0,
        lookback_minutes: int = 60
    ) -> List[AgentActivitySummary]:
        """
        Find agents that are inactive.
        
        Args:
            inactivity_threshold_minutes: Minutes of inactivity to consider agent inactive
            lookback_minutes: How far back to look for activity
            
        Returns:
            List of inactive agents with activity summaries
        """
        inactive_agents = []
        
        for i in range(1, 9):
            agent_id = f"Agent-{i}"
            summary = self.detect_agent_activity(agent_id, lookback_minutes)
            
            if not summary.is_active or summary.inactivity_duration_minutes >= inactivity_threshold_minutes:
                inactive_agents.append(summary)
        
        return inactive_agents
    
    def get_activity_report(self, agent_id: str, lookback_minutes: int = 60) -> str:
        """Get human-readable activity report for an agent."""
        summary = self.detect_agent_activity(agent_id, lookback_minutes)
        
        report = f"""
{'=' * 80}
AGENT ACTIVITY REPORT: {agent_id}
{'=' * 80}

Status: {'🟢 ACTIVE' if summary.is_active else '🔴 INACTIVE'}
Last Activity: {summary.last_activity.strftime('%Y-%m-%d %H:%M:%S') if summary.last_activity else 'Never'}
Inactivity Duration: {summary.inactivity_duration_minutes:.1f} minutes

Activity Sources Detected: {', '.join(summary.activity_sources) if summary.activity_sources else 'None'}

Recent Actions:
"""
        if summary.recent_actions:
            for i, action in enumerate(summary.recent_actions, 1):
                report += f"  {i}. {action}\n"
        else:
            report += "  No recent actions detected\n"
        
        report += f"\n{'=' * 80}\n"
        
        return report


def main():
    """CLI entry point."""
    import argparse
    from src.core.config.timeout_constants import TimeoutConstants
    
    parser = argparse.ArgumentParser(description="Agent Activity Detector")
    parser.add_argument("--agent", help="Check specific agent")
    parser.add_argument("--inactive", action="store_true", help="Find inactive agents")
    parser.add_argument("--threshold", type=float, default=30.0, help="Inactivity threshold (minutes)")
    parser.add_argument("--lookback", type=int, default=60, help="Lookback period (minutes)")
    parser.add_argument("--report", action="store_true", help="Generate detailed report")
    
    args = parser.parse_args()
    
    detector = AgentActivityDetector()
    
    if args.agent:
        if args.report:
            print(detector.get_activity_report(args.agent, args.lookback))
        else:
            summary = detector.detect_agent_activity(args.agent, args.lookback)
            print(f"Agent: {summary.agent_id}")
            print(f"Active: {summary.is_active}")
            print(f"Last Activity: {summary.last_activity}")
            print(f"Inactivity: {summary.inactivity_duration_minutes:.1f} minutes")
            print(f"Sources: {', '.join(summary.activity_sources)}")
    elif args.inactive:
        inactive = detector.find_inactive_agents(args.threshold, args.lookback)
        print(f"\n{'=' * 80}")
        print(f"INACTIVE AGENTS (threshold: {args.threshold} minutes)")
        print(f"{'=' * 80}\n")
        
        if inactive:
            for summary in inactive:
                print(f"🔴 {summary.agent_id}: Inactive for {summary.inactivity_duration_minutes:.1f} minutes")
                print(f"   Last activity: {summary.last_activity}")
                print(f"   Sources: {', '.join(summary.activity_sources) if summary.activity_sources else 'None'}")
                print()
        else:
            print("✅ All agents are active!")
    else:
        # Check all agents
        print(f"\n{'=' * 80}")
        print("AGENT ACTIVITY SUMMARY")
        print(f"{'=' * 80}\n")
        
        for i in range(1, 9):
            agent_id = f"Agent-{i}"
            summary = detector.detect_agent_activity(agent_id, args.lookback)
            status = "🟢" if summary.is_active else "🔴"
            print(f"{status} {agent_id}: {summary.inactivity_duration_minutes:.1f} min inactive")
            if summary.last_activity:
                print(f"   Last: {summary.last_activity.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   Sources: {', '.join(summary.activity_sources) if summary.activity_sources else 'None'}")
            print()


if __name__ == "__main__":
    main()

