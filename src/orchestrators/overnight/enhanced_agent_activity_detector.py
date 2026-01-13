<<<<<<< HEAD
<<<<<<< HEAD
#!/usr/bin/env python3
"""
<!-- SSOT Domain: core -->

Enhanced Agent Activity Detector - Main Entry Point
===================================================

Main entry point for enhanced agent activity detection.
Uses modular checkers for comprehensive activity monitoring.

V2 Compliant: <200 lines, modular architecture
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-08
=======
=======
#!/usr/bin/env python3
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
"""
<!-- SSOT Domain: core -->

Enhanced Agent Activity Detector - Main Entry Point
===================================================

Main entry point for enhanced agent activity detection.
Uses modular checkers for comprehensive activity monitoring.

<<<<<<< HEAD
V2 Compliance: <400 lines, single responsibility, comprehensive activity detection.

Author: Agent-2 (Architecture & Design Specialist)
Date: 2025-01-27
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======
V2 Compliant: <200 lines, modular architecture
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-08
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import logging

<<<<<<< HEAD
<<<<<<< HEAD
from .activity_file_checkers import FileSystemActivityChecker
from .activity_git_checkers import GitActivityChecker
from .activity_message_checkers import MessageActivityChecker
=======
from src.core.config.timeout_constants import TimeoutConstants
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======
from .activity_file_checkers import FileSystemActivityChecker
from .activity_git_checkers import GitActivityChecker
from .activity_message_checkers import MessageActivityChecker
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1

logger = logging.getLogger(__name__)


class EnhancedAgentActivityDetector:
    """
<<<<<<< HEAD
<<<<<<< HEAD
    Detects agent activity through multiple modular indicators.
=======
    Detects agent activity through multiple indicators.
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======
    Detects agent activity through multiple modular indicators.
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1

    Tracks:
    - File modifications (status.json, inbox, devlogs, reports)
    - Message operations (queue, inbox processing)
    - Code operations (git commits, file changes)
    - Tool executions
    - Discord activity
<<<<<<< HEAD
<<<<<<< HEAD
    - Inter-agent communications
    """

    def __init__(self, workspace_root: Optional[Path] = None):
        """Initialize activity detector with modular checkers."""
=======
    """

    def __init__(self, workspace_root: Optional[Path] = None):
        """Initialize activity detector."""
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======
    - Inter-agent communications
    """

    def __init__(self, workspace_root: Optional[Path] = None):
        """Initialize activity detector with modular checkers."""
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
        self.workspace_root = workspace_root or Path(".")
        self.agent_workspaces = self.workspace_root / "agent_workspaces"
        self.devlogs_dir = self.workspace_root / "devlogs"

<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
        # Initialize modular checkers
        self.file_checker = FileSystemActivityChecker(self.workspace_root)
        self.git_checker = GitActivityChecker(self.workspace_root)
        self.message_checker = MessageActivityChecker(self.workspace_root)

<<<<<<< HEAD
    def detect_agent_activity(self, agent_id: str) -> Dict[str, Any]:
        """
        Detect all activity indicators for an agent using modular checkers.

        Returns dict with activity indicators and metadata.
        """
        activity_data = {
            "agent_id": agent_id,
            "detection_timestamp": datetime.now().isoformat(),
            "activity_indicators": {},
            "overall_activity_score": 0,
            "is_active": False,
            "last_activity_timestamp": None
        }

        # File system activity checks
        activity_data["activity_indicators"]["status_json"] = self.file_checker.check_status_json(agent_id)
        activity_data["activity_indicators"]["inbox_files"] = self.file_checker.check_inbox_files(agent_id)
        activity_data["activity_indicators"]["devlogs"] = self.file_checker.check_devlogs(agent_id)
        activity_data["activity_indicators"]["reports"] = self.file_checker.check_reports(agent_id)
        activity_data["activity_indicators"]["workspace_files"] = self.file_checker.check_workspace_files(agent_id)

        # Git activity checks
        activity_data["activity_indicators"]["git_commits"] = self.git_checker.check_git_commits(agent_id)
        activity_data["activity_indicators"]["git_status"] = self.git_checker.check_git_status(agent_id)

        # Message and communication checks
        activity_data["activity_indicators"]["message_queue"] = self.message_checker.check_message_queue(agent_id)
        activity_data["activity_indicators"]["discord_posts"] = self.message_checker.check_discord_posts(agent_id)
        activity_data["activity_indicators"]["agent_communications"] = self.message_checker.check_agent_communications(agent_id)

        # Calculate overall activity score and status
        self._calculate_activity_score(activity_data)

        return activity_data

    def _calculate_activity_score(self, activity_data: Dict[str, Any]) -> None:
        """Calculate overall activity score from indicators."""
        indicators = activity_data["activity_indicators"]
        score = 0
        latest_timestamp = None

        # Weight different activity types
        weights = {
            "status_json": 3,  # High weight for status updates
            "git_commits": 4,  # Very high weight for commits
            "inbox_files": 2,  # Medium weight for messages
            "devlogs": 2,      # Medium weight for documentation
            "reports": 2,      # Medium weight for reporting
            "workspace_files": 1,  # Low weight for file changes
            "message_queue": 2,   # Medium weight for messaging
            "discord_posts": 2,   # Medium weight for Discord activity
            "agent_communications": 2,  # Medium weight for inter-agent comms
            "git_status": 1     # Low weight for uncommitted changes
        }

        for indicator_name, indicator_data in indicators.items():
            if indicator_data:
                score += weights.get(indicator_name, 1)

                # Track latest activity timestamp
                if "latest_modification" in indicator_data:
                    timestamp_str = indicator_data["latest_modification"]
                elif "latest_communication" in indicator_data:
                    timestamp_str = indicator_data["latest_communication"]
                elif "last_updated" in indicator_data:
                    timestamp_str = indicator_data["last_updated"]
                else:
                    timestamp_str = None

                if timestamp_str:
                    try:
                        timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                        if latest_timestamp is None or timestamp > latest_timestamp:
                            latest_timestamp = timestamp
                    except:
                        pass

        # Determine if agent is currently active
        is_active = score > 0
        if latest_timestamp:
            time_diff = datetime.now() - latest_timestamp
            # Consider active if activity within last 24 hours
            is_active = is_active and time_diff < timedelta(hours=24)

        activity_data["overall_activity_score"] = score
        activity_data["is_active"] = is_active
        activity_data["last_activity_timestamp"] = latest_timestamp.isoformat() if latest_timestamp else None

    def get_activity_summary(self, agent_ids: List[str]) -> Dict[str, Any]:
        """Get activity summary for multiple agents."""
        summary = {
            "total_agents": len(agent_ids),
            "active_agents": 0,
            "inactive_agents": 0,
            "agent_activities": {},
            "generated_at": datetime.now().isoformat()
        }

        for agent_id in agent_ids:
            activity = self.detect_agent_activity(agent_id)
            summary["agent_activities"][agent_id] = activity

            if activity["is_active"]:
                summary["active_agents"] += 1
            else:
                summary["inactive_agents"] += 1

        return summary

    def detect_recent_activity(self, agent_id: str, hours: int = 24) -> List[Dict[str, Any]]:
        """Detect activity within specified time window."""
        activity = self.detect_agent_activity(agent_id)
        recent_activities = []

        cutoff_time = datetime.now() - timedelta(hours=hours)

        for indicator_name, indicator_data in activity["activity_indicators"].items():
            if indicator_data and "latest_modification" in indicator_data:
                try:
                    activity_time = datetime.fromisoformat(indicator_data["latest_modification"])
                    if activity_time > cutoff_time:
                        recent_activities.append({
                            "indicator": indicator_name,
                            "timestamp": indicator_data["latest_modification"],
                            "details": indicator_data
                        })
                except:
                    pass

        return sorted(recent_activities, key=lambda x: x["timestamp"], reverse=True)


__all__ = ["EnhancedAgentActivityDetector"]
=======
=======
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
    def detect_agent_activity(self, agent_id: str) -> Dict[str, Any]:
        """
        Detect all activity indicators for an agent using modular checkers.

        Returns dict with activity indicators and metadata.
        """
        activity_data = {
            "agent_id": agent_id,
            "detection_timestamp": datetime.now().isoformat(),
            "activity_indicators": {},
            "overall_activity_score": 0,
            "is_active": False,
            "last_activity_timestamp": None
        }

        # File system activity checks
        activity_data["activity_indicators"]["status_json"] = self.file_checker.check_status_json(agent_id)
        activity_data["activity_indicators"]["inbox_files"] = self.file_checker.check_inbox_files(agent_id)
        activity_data["activity_indicators"]["devlogs"] = self.file_checker.check_devlogs(agent_id)
        activity_data["activity_indicators"]["reports"] = self.file_checker.check_reports(agent_id)
        activity_data["activity_indicators"]["workspace_files"] = self.file_checker.check_workspace_files(agent_id)

        # Git activity checks
        activity_data["activity_indicators"]["git_commits"] = self.git_checker.check_git_commits(agent_id)
        activity_data["activity_indicators"]["git_status"] = self.git_checker.check_git_status(agent_id)

        # Message and communication checks
        activity_data["activity_indicators"]["message_queue"] = self.message_checker.check_message_queue(agent_id)
        activity_data["activity_indicators"]["discord_posts"] = self.message_checker.check_discord_posts(agent_id)
        activity_data["activity_indicators"]["agent_communications"] = self.message_checker.check_agent_communications(agent_id)

        # Calculate overall activity score and status
        self._calculate_activity_score(activity_data)

        return activity_data

    def _calculate_activity_score(self, activity_data: Dict[str, Any]) -> None:
        """Calculate overall activity score from indicators."""
        indicators = activity_data["activity_indicators"]
        score = 0
        latest_timestamp = None

        # Weight different activity types
        weights = {
            "status_json": 3,  # High weight for status updates
            "git_commits": 4,  # Very high weight for commits
            "inbox_files": 2,  # Medium weight for messages
            "devlogs": 2,      # Medium weight for documentation
            "reports": 2,      # Medium weight for reporting
            "workspace_files": 1,  # Low weight for file changes
            "message_queue": 2,   # Medium weight for messaging
            "discord_posts": 2,   # Medium weight for Discord activity
            "agent_communications": 2,  # Medium weight for inter-agent comms
            "git_status": 1     # Low weight for uncommitted changes
        }

        for indicator_name, indicator_data in indicators.items():
            if indicator_data:
                score += weights.get(indicator_name, 1)

                # Track latest activity timestamp
                if "latest_modification" in indicator_data:
                    timestamp_str = indicator_data["latest_modification"]
                elif "latest_communication" in indicator_data:
                    timestamp_str = indicator_data["latest_communication"]
                elif "last_updated" in indicator_data:
                    timestamp_str = indicator_data["last_updated"]
                else:
                    timestamp_str = None

                if timestamp_str:
                    try:
                        timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                        if latest_timestamp is None or timestamp > latest_timestamp:
                            latest_timestamp = timestamp
                    except:
                        pass

        # Determine if agent is currently active
        is_active = score > 0
        if latest_timestamp:
            time_diff = datetime.now() - latest_timestamp
            # Consider active if activity within last 24 hours
            is_active = is_active and time_diff < timedelta(hours=24)

        activity_data["overall_activity_score"] = score
        activity_data["is_active"] = is_active
        activity_data["last_activity_timestamp"] = latest_timestamp.isoformat() if latest_timestamp else None

    def get_activity_summary(self, agent_ids: List[str]) -> Dict[str, Any]:
        """Get activity summary for multiple agents."""
        summary = {
            "total_agents": len(agent_ids),
            "active_agents": 0,
            "inactive_agents": 0,
            "agent_activities": {},
            "generated_at": datetime.now().isoformat()
        }

        for agent_id in agent_ids:
            activity = self.detect_agent_activity(agent_id)
            summary["agent_activities"][agent_id] = activity

            if activity["is_active"]:
                summary["active_agents"] += 1
            else:
                summary["inactive_agents"] += 1

        return summary

    def detect_recent_activity(self, agent_id: str, hours: int = 24) -> List[Dict[str, Any]]:
        """Detect activity within specified time window."""
        activity = self.detect_agent_activity(agent_id)
        recent_activities = []

        cutoff_time = datetime.now() - timedelta(hours=hours)

        for indicator_name, indicator_data in activity["activity_indicators"].items():
            if indicator_data and "latest_modification" in indicator_data:
                try:
                    activity_time = datetime.fromisoformat(indicator_data["latest_modification"])
                    if activity_time > cutoff_time:
                        recent_activities.append({
                            "indicator": indicator_name,
                            "timestamp": indicator_data["latest_modification"],
                            "details": indicator_data
                        })
                except:
                    pass

        return sorted(recent_activities, key=lambda x: x["timestamp"], reverse=True)


<<<<<<< HEAD
            try:
                status_data = json.loads(
                    status_file.read_text(encoding="utf-8"))

                # Check for lifecycle indicators
                lifecycle_indicators = {
                    "cycle_count": status_data.get("cycle_count"),
                    "last_cycle": status_data.get("last_cycle"),
                    "fsm_state": status_data.get("fsm_state"),
                }

                # If cycle_count exists, AgentLifecycle is likely being used
                if lifecycle_indicators.get("cycle_count") is not None:
                    # Check last_cycle timestamp
                    last_cycle_str = lifecycle_indicators.get("last_cycle")
                    if last_cycle_str:
                        try:
                            from datetime import datetime
                            # Parse ISO format timestamp
                            last_cycle_time = datetime.fromisoformat(
                                last_cycle_str.replace("Z", "+00:00")
                            ).timestamp()

                            return {
                                "source": "agent_lifecycle",
                                "timestamp": last_cycle_time,
                                "cycle_count": lifecycle_indicators.get("cycle_count"),
                                "fsm_state": lifecycle_indicators.get("fsm_state"),
                                "age_seconds": time.time() - last_cycle_time,
                            }
                        except Exception:
                            pass

                # Fallback: Check status.json modification time if lifecycle indicators exist
                if any(lifecycle_indicators.values()):
                    mtime = status_file.stat().st_mtime
                    return {
                        "source": "agent_lifecycle",
                        "timestamp": mtime,
                        "cycle_count": lifecycle_indicators.get("cycle_count"),
                        "fsm_state": lifecycle_indicators.get("fsm_state"),
                        "age_seconds": time.time() - mtime,
                    }
            except Exception:
                pass

            return None
        except Exception as e:
            logger.debug(f"Could not check Agent lifecycle: {e}")
            return None

    def _check_activity_emitter_events(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Check ActivityEmitter telemetry events (HIGH priority - most reliable)."""
        try:
            event_file = self.workspace_root / "runtime" / \
                "agent_comms" / "activity_events.jsonl"
            if not event_file.exists():
                return None

            # Read last N lines (most recent events)
            try:
                with open(event_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    # Check last 100 lines for agent events
                    recent_lines = lines[-100:] if len(lines) > 100 else lines

                    agent_events = []
                    for line in recent_lines:
                        try:
                            event = json.loads(line.strip())
                            if event.get("agent_id", "").lower() == agent_id.lower():
                                agent_events.append(event)
                        except json.JSONDecodeError:
                            continue

                    if agent_events:
                        # Get most recent event
                        latest_event = max(
                            agent_events,
                            key=lambda e: e.get("timestamp", 0)
                        )
                        event_timestamp = latest_event.get("timestamp", 0)
                        if event_timestamp > 0:
                            return {
                                "source": "activity_emitter",
                                "timestamp": event_timestamp,
                                "event_type": latest_event.get("event_type", ""),
                                "event_count": len(agent_events),
                                "age_seconds": time.time() - event_timestamp,
                            }
            except Exception as e:
                logger.debug(f"Could not read activity events file: {e}")
                return None
        except Exception as e:
            logger.debug(f"Could not check ActivityEmitter events: {e}")
            return None

    def _check_test_execution(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Check pytest/test execution activity (HIGH priority)."""
        try:
            # Check pytest cache
            pytest_cache = self.workspace_root / ".pytest_cache"
            if pytest_cache.exists():
                mtime = pytest_cache.stat().st_mtime
                if time.time() - mtime < 3600:  # Within last hour
                    return {
                        "source": "test_execution",
                        "timestamp": mtime,
                        "cache_type": "pytest_cache",
                        "age_seconds": time.time() - mtime,
                    }

            # Check test result files
            test_results = self.workspace_root / "test_results"
            if test_results.exists():
                result_files = list(test_results.glob(f"*{agent_id}*.json"))
                if result_files:
                    latest = max(result_files, key=lambda p: p.stat().st_mtime)
                    mtime = latest.stat().st_mtime
                    if time.time() - mtime < 3600:
                        return {
                            "source": "test_execution",
                            "timestamp": mtime,
                            "file": latest.name,
                            "age_seconds": time.time() - mtime,
                        }

            # Check coverage reports
            coverage_file = self.workspace_root / ".coverage"
            if coverage_file.exists():
                mtime = coverage_file.stat().st_mtime
                if time.time() - mtime < 3600:
                    return {
                        "source": "test_execution",
                        "timestamp": mtime,
                        "cache_type": "coverage",
                        "age_seconds": time.time() - mtime,
                    }

            # Check htmlcov directory
            htmlcov_dir = self.workspace_root / "htmlcov"
            if htmlcov_dir.exists() and htmlcov_dir.is_dir():
                mtime = htmlcov_dir.stat().st_mtime
                if time.time() - mtime < 3600:
                    return {
                        "source": "test_execution",
                        "timestamp": mtime,
                        "cache_type": "htmlcov",
                        "age_seconds": time.time() - mtime,
                    }
        except Exception as e:
            logger.debug(f"Could not check test execution: {e}")
            return None

        return None

    def _check_passdown_json(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Check passdown.json file modification (Phase 2)."""
        passdown_file = self.agent_workspaces / agent_id / "passdown.json"
        if not passdown_file.exists():
            return None

        mtime = passdown_file.stat().st_mtime

        # Check session_date field in JSON
        session_date = None
        try:
            passdown_data = json.loads(
                passdown_file.read_text(encoding="utf-8"))
            session_date = passdown_data.get("session_date")
        except Exception:
            pass

        return {
            "source": "passdown",
            "timestamp": mtime,
            "file": str(passdown_file),
            "session_date": session_date,
            "age_seconds": time.time() - mtime,
        }

    def _check_artifacts_directory(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Check artifacts directory for agent-specific files (Phase 2)."""
        artifacts_dir = self.workspace_root / "artifacts"
        if not artifacts_dir.exists():
            return None

        # Look for agent-specific artifact files
        patterns = [
            f"*{agent_id.lower()}*",
            f"*{agent_id.replace('-', '_').lower()}*",
            f"*{agent_id}*",
        ]

        artifact_files = []
        for pattern in patterns:
            artifact_files.extend(list(artifacts_dir.glob(f"{pattern}.md")))

        if not artifact_files:
            return None

        # Get most recent artifact
        latest_artifact = max(artifact_files, key=lambda p: p.stat().st_mtime)
        mtime = latest_artifact.stat().st_mtime

        # Only return if recent (within last 7 days)
        age_seconds = time.time() - mtime
        if age_seconds > (7 * 24 * 3600):
            return None

        return {
            "source": "artifacts",
            "timestamp": mtime,
            "file": latest_artifact.name,
            "artifact_count": len(artifact_files),
            "age_seconds": age_seconds,
        }

    def _check_cycle_planner(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Check cycle planner task files (Phase 2)."""
        agent_dir = self.agent_workspaces / agent_id
        if not agent_dir.exists():
            return None

        # Look for cycle planner task files
        cycle_planner_files = list(
            agent_dir.glob("cycle_planner_tasks_*.json"))

        if not cycle_planner_files:
            return None

        # Get most recent cycle planner file
        latest_file = max(cycle_planner_files, key=lambda p: p.stat().st_mtime)
        mtime = latest_file.stat().st_mtime

        return {
            "source": "cycle_planner",
            "timestamp": mtime,
            "file": latest_file.name,
            "file_count": len(cycle_planner_files),
            "age_seconds": time.time() - mtime,
        }

    def _check_notes_directory(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Check notes directory for agent notes (Phase 2)."""
        notes_dir = self.agent_workspaces / agent_id / "notes"
        if not notes_dir.exists():
            return None

        note_files = list(notes_dir.glob("*.md"))
        if not note_files:
            return None

        # Get most recent note
        latest_note = max(note_files, key=lambda p: p.stat().st_mtime)
        mtime = latest_note.stat().st_mtime

        return {
            "source": "notes",
            "timestamp": mtime,
            "file": latest_note.name,
            "note_count": len(note_files),
            "age_seconds": time.time() - mtime,
        }

    def _check_git_working_directory(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Check git working directory for uncommitted changes in agent workspace (Phase 2)."""
        try:
            import subprocess

            agent_dir = self.agent_workspaces / agent_id
            if not agent_dir.exists():
                return None

            # Get relative path from workspace root
            try:
                agent_relative = agent_dir.relative_to(self.workspace_root)
            except ValueError:
                return None

            # Check for uncommitted changes in agent workspace
            result = subprocess.run(
                ["git", "diff", "--name-only", str(agent_relative)],
                capture_output=True,
                text=True,
                timeout=TimeoutConstants.HTTP_QUICK,
                cwd=self.workspace_root,
            )

            if result.returncode != 0 or not result.stdout.strip():
                return None

            # Get most recent modification time of changed files
            changed_files = result.stdout.strip().split("\n")
            if not changed_files:
                return None

            # Get modification times for changed files
            max_mtime = 0
            for file_path_str in changed_files:
                try:
                    file_path = self.workspace_root / file_path_str
                    if file_path.exists():
                        mtime = file_path.stat().st_mtime
                        max_mtime = max(max_mtime, mtime)
                except Exception:
                    continue

            if max_mtime == 0:
                return None

            return {
                "source": "git_working",
                "timestamp": max_mtime,
                "changed_files_count": len(changed_files),
                "age_seconds": time.time() - max_mtime,
            }
        except Exception as e:
            logger.debug(f"Could not check git working directory: {e}")
            return None

    def _check_activity_logs(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Check activity log files (Agent-7 improvement - HIGH priority)."""
        activity_dir = self.agent_workspaces / agent_id / "activity"
        if not activity_dir.exists():
            return None

        activity_files = list(activity_dir.glob("*.md"))
        if not activity_files:
            return None

        latest_file = max(activity_files, key=lambda p: p.stat().st_mtime)
        mtime = latest_file.stat().st_mtime

        # Only return if recent (within 24 hours)
        age_seconds = time.time() - mtime
        if age_seconds > 86400:
            return None

        return {
            "source": "activity_logs",
            "timestamp": mtime,
            "file": latest_file.name,
            "file_count": len(activity_files),
            "age_seconds": age_seconds,
        }
    
    def _check_terminal_activity(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Check terminal/command execution activity (Phase 1 - HIGH priority)."""
        try:
            # Check for terminal history files
            terminal_history_paths = [
                Path.home() / ".bash_history",
                Path.home() / ".zsh_history",
                Path.home() / ".powershell_history",
            ]
            
            latest_activity = None
            for history_path in terminal_history_paths:
                if history_path.exists():
                    mtime = history_path.stat().st_mtime
                    if time.time() - mtime < 3600:  # Within last hour
                        # Check if file contains agent-related commands
                        try:
                            with open(history_path, 'r', encoding='utf-8', errors='ignore') as f:
                                lines = f.readlines()
                                recent_lines = ''.join(lines[-100:]).lower()
                                if agent_id.lower() in recent_lines or 'agent' in recent_lines:
                                    if latest_activity is None or mtime > latest_activity:
                                        latest_activity = mtime
                        except Exception:
                            if latest_activity is None or mtime > latest_activity:
                                latest_activity = mtime
            
            if latest_activity:
                return {
                    "source": "terminal",
                    "timestamp": latest_activity,
                    "age_seconds": time.time() - latest_activity,
                }
        except Exception as e:
            logger.debug(f"Could not check terminal activity: {e}")
        
        return None
    
    def _check_log_file_activity(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Check log file activity (Phase 1 - HIGH priority)."""
        try:
            log_dirs = [
                Path("logs"),
                Path("runtime") / "logs",
                Path("data") / "logs",
                self.agent_workspaces / agent_id / "logs",
            ]
            
            agent_pattern = agent_id.lower().replace('-', '')
            latest_activity = None
            latest_file = None
            
            for log_dir in log_dirs:
                if not log_dir.exists():
                    continue
                
                # Check for log files
                log_files = list(log_dir.rglob("*.log"))
                log_files.extend(list(log_dir.rglob("*.txt")))
                
                for log_file in log_files:
                    try:
                        mtime = log_file.stat().st_mtime
                        if time.time() - mtime > 3600:  # Only last hour
                            continue
                        
                        if latest_activity is None or mtime > latest_activity:
                            # Check if file contains agent references
                            try:
                                with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                                    lines = f.readlines()
                                    recent_lines = ''.join(lines[-50:]).lower()
                                    if agent_pattern in recent_lines or agent_id.lower() in recent_lines:
                                        latest_activity = mtime
                                        latest_file = log_file.name
                            except Exception:
                                # Still count recent modification
                                if latest_activity is None or mtime > latest_activity:
                                    latest_activity = mtime
                                    latest_file = log_file.name
                    except (OSError, PermissionError):
                        continue
            
            if latest_activity:
                return {
                    "source": "log",
                    "timestamp": latest_activity,
                    "file": latest_file,
                    "age_seconds": time.time() - latest_activity,
                }
        except Exception as e:
            logger.debug(f"Could not check log file activity: {e}")
        
        return None
    
    def _check_process_activity(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Check process/application activity (Phase 2 - MEDIUM priority)."""
        try:
            import psutil
        except ImportError:
            return None
        
        try:
            agent_pattern = agent_id.lower().replace('-', '')
            recent_processes = []
            
            for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'create_time']):
                try:
                    proc_info = proc.info
                    cmdline = proc_info.get('cmdline', [])
                    if not cmdline:
                        continue
                    
                    proc_name = proc_info.get('name', '').lower()
                    if 'python' not in proc_name and 'cursor' not in proc_name and 'code' not in proc_name:
                        continue
                    
                    create_time = proc_info.get('create_time', 0)
                    if create_time == 0:
                        continue
                    
                    # Only check processes from last 24 hours
                    if time.time() - create_time > 86400:
                        continue
                    
                    cmdline_str = ' '.join(cmdline).lower()
                    if agent_pattern in cmdline_str or 'agent' in cmdline_str:
                        recent_processes.append({
                            "pid": proc_info.get('pid'),
                            "name": proc_name,
                            "create_time": create_time
                        })
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
            
            if recent_processes:
                latest_proc = max(recent_processes, key=lambda p: p["create_time"])
                return {
                    "source": "process",
                    "timestamp": latest_proc["create_time"],
                    "process_count": len(recent_processes),
                    "process_name": latest_proc["name"],
                    "age_seconds": time.time() - latest_proc["create_time"],
                }
        except Exception as e:
            logger.debug(f"Could not check process activity: {e}")
        
        return None
    
    def _check_ide_activity(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Check IDE/editor activity (Phase 2 - MEDIUM priority)."""
        try:
            agent_dir = self.agent_workspaces / agent_id
            if not agent_dir.exists():
                return None
            
            vscode_storage = Path.home() / ".vscode" / "User" / "workspaceStorage"
            cursor_storage = Path.home() / ".cursor" / "User" / "workspaceStorage"
            
            latest_activity = None
            ide_type = None
            
            for storage_path, ide_name in [(vscode_storage, "vscode"), (cursor_storage, "cursor")]:
                if not storage_path.exists():
                    continue
                
                for workspace_folder in storage_path.iterdir():
                    if not workspace_folder.is_dir():
                        continue
                    
                    state_files = list(workspace_folder.glob("**/*.json"))
                    for state_file in state_files:
                        try:
                            mtime = state_file.stat().st_mtime
                            if latest_activity is None or mtime > latest_activity:
                                # Check if file references agent workspace
                                try:
                                    content = state_file.read_text(encoding='utf-8', errors='ignore')
                                    if agent_id.lower() in content.lower() or str(agent_dir).lower() in content.lower():
                                        latest_activity = mtime
                                        ide_type = ide_name
                                except Exception:
                                    # Still count recent modification
                                    if latest_activity is None or mtime > latest_activity:
                                        latest_activity = mtime
                                        ide_type = ide_name
                        except (OSError, PermissionError):
                            continue
            
            if latest_activity and time.time() - latest_activity < 86400:  # Last 24 hours
                return {
                    "source": "ide",
                    "timestamp": latest_activity,
                    "ide_type": ide_type or "unknown",
                    "age_seconds": time.time() - latest_activity,
                }
        except Exception as e:
            logger.debug(f"Could not check IDE activity: {e}")
        
        return None
    
    def _check_database_activity(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Check database activity (Phase 2 - MEDIUM priority)."""
        try:
            agent_pattern = agent_id.lower().replace('-', '')
            log_dirs = [
                Path("logs"),
                Path("runtime") / "logs",
                Path("data") / "logs",
                Path("data") / "database",
            ]
            
            latest_activity = None
            activity_type = None
            
            # Check database log files
            for log_dir in log_dirs:
                if not log_dir.exists():
                    continue
                
                db_log_patterns = ["*db*.log", "*database*.log", "*query*.log", "*sql*.log"]
                for pattern in db_log_patterns:
                    for log_file in log_dir.rglob(pattern):
                        try:
                            mtime = log_file.stat().st_mtime
                            if time.time() - mtime > 86400:  # Only last 24 hours
                                continue
                            
                            if latest_activity is None or mtime > latest_activity:
                                try:
                                    with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                                        lines = f.readlines()
                                        recent_lines = ''.join(lines[-50:]).lower()
                                        if agent_pattern in recent_lines or agent_id.lower() in recent_lines:
                                            latest_activity = mtime
                                            activity_type = "query_log"
                                except Exception:
                                    latest_activity = mtime
                                    activity_type = "log_file"
                        except (OSError, PermissionError):
                            continue
            
            # Check repository files
            repo_files = [
                Path("data") / "activity_repository.json",
                Path("data") / "message_repository.json",
            ]
            
            for repo_file in repo_files:
                if repo_file.exists():
                    try:
                        mtime = repo_file.stat().st_mtime
                        if time.time() - mtime > 86400:
                            continue
                        
                        if latest_activity is None or mtime > latest_activity:
                            try:
                                with open(repo_file, 'r', encoding='utf-8') as f:
                                    data = json.load(f)
                                    data_str = json.dumps(data).lower()
                                    if agent_pattern in data_str or agent_id.lower() in data_str:
                                        latest_activity = mtime
                                        activity_type = "repository"
                            except Exception:
                                latest_activity = mtime
                                activity_type = "repository"
                    except (OSError, PermissionError):
                        continue
            
            if latest_activity:
                return {
                    "source": "database",
                    "timestamp": latest_activity,
                    "activity_type": activity_type or "unknown",
                    "age_seconds": time.time() - latest_activity,
                }
        except Exception as e:
            logger.debug(f"Could not check database activity: {e}")
        
        return None

    def get_all_agents_activity(self) -> Dict[str, Dict[str, Any]]:
        """Get activity for all agents."""
        all_activity = {}

        if not self.agent_workspaces.exists():
            return all_activity

        for agent_dir in self.agent_workspaces.iterdir():
            if agent_dir.is_dir() and agent_dir.name.startswith("Agent-"):
                agent_id = agent_dir.name
                activity = self.detect_agent_activity(agent_id)
                all_activity[agent_id] = activity

        return all_activity

    def get_stale_agents(
        self,
        max_age_seconds: int = 3600  # 1 hour default
    ) -> List[Tuple[str, float]]:
        """
        Get list of agents with no recent activity.

        Returns list of (agent_id, age_seconds) tuples.
        """
        stale_agents = []
        all_activity = self.get_all_agents_activity()

        for agent_id, activity in all_activity.items():
            latest = activity.get("latest_activity")
            if latest is None:
                stale_agents.append((agent_id, float("inf")))
            else:
                age = time.time() - latest
                if age > max_age_seconds:
                    stale_agents.append((agent_id, age))

        # Sort by age (oldest first)
        stale_agents.sort(key=lambda x: x[1], reverse=True)
        return stale_agents

    def _check_contract_activity(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Check contract system for agent task activity (Agent-5 Phase 1 - HIGH priority)."""
        try:
            from src.services.contract_system.manager import ContractManager
            manager = ContractManager()
            agent_status = manager.get_agent_status(agent_id)

            # Check for active contracts or recent completions
            active_contracts = agent_status.get("active_contracts", 0)
            if active_contracts > 0:
                # Check contract timestamps
                contracts = agent_status.get("contracts", [])
                if contracts:
                    latest_contract = max(
                        contracts,
                        key=lambda c: c.get("assigned_at", 0) or c.get("updated_at", 0) or 0
                    )
                    timestamp = latest_contract.get("assigned_at") or latest_contract.get("updated_at")
                    if timestamp:
                        # Convert to unix timestamp if needed
                        if isinstance(timestamp, str):
                            try:
                                from datetime import datetime
                                timestamp = datetime.fromisoformat(
                                    timestamp.replace("Z", "+00:00")
                                ).timestamp()
                            except Exception:
                                return None
                        return {
                            "source": "contract_system",
                            "timestamp": timestamp,
                            "active_contracts": active_contracts,
                            "age_seconds": time.time() - timestamp,
                        }
        except Exception as e:
            logger.debug(f"Could not check contract activity: {e}")
        return None

    def _check_inbox_processing(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Check inbox message processing activity (Agent-5 Phase 1 - HIGH priority)."""
        inbox_dir = self.agent_workspaces / agent_id / "inbox"
        if not inbox_dir.exists():
            return None

        # Check for processed/read indicators
        processed_files = list(inbox_dir.glob("*_processed.md"))
        read_files = list(inbox_dir.glob("*_read.md"))

        all_processed = processed_files + read_files
        if all_processed:
            latest = max(all_processed, key=lambda p: p.stat().st_mtime)
            mtime = latest.stat().st_mtime
            return {
                "source": "inbox_processing",
                "timestamp": mtime,
                "file": latest.name,
                "age_seconds": time.time() - mtime,
            }

        # Alternative: Check inbox file content for processing markers
        inbox_files = list(inbox_dir.glob("*.md"))
        for inbox_file in sorted(inbox_files, key=lambda p: p.stat().st_mtime, reverse=True)[:5]:
            try:
                content = inbox_file.read_text(encoding="utf-8")
                # Check for processing indicators
                if "✅" in content or "COMPLETE" in content.upper() or "DONE" in content.upper():
                    mtime = inbox_file.stat().st_mtime
                    # Only if recent (within last 24 hours)
                    if time.time() - mtime < (24 * 3600):
                        return {
                            "source": "inbox_processing",
                            "timestamp": mtime,
                            "file": inbox_file.name,
                            "age_seconds": time.time() - mtime,
                        }
            except Exception:
                continue

        return None
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======
__all__ = ["EnhancedAgentActivityDetector"]
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
