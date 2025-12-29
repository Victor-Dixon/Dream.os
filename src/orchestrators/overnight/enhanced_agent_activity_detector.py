"""
<!-- SSOT Domain: core -->

Enhanced Agent Activity Detector
=================================

Strengthens status monitor by detecting all actions that directly link an agent to activity.
Tracks multiple activity indicators beyond just task assignments.

V2 Compliance: <400 lines, single responsibility, comprehensive activity detection.

Author: Agent-2 (Architecture & Design Specialist)
Date: 2025-01-27
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import logging

from src.core.config.timeout_constants import TimeoutConstants

logger = logging.getLogger(__name__)


class EnhancedAgentActivityDetector:
    """
    Detects agent activity through multiple indicators.

    Tracks:
    - File modifications (status.json, inbox, devlogs, reports)
    - Message operations (queue, inbox processing)
    - Code operations (git commits, file changes)
    - Tool executions
    - Discord activity
    """

    def __init__(self, workspace_root: Optional[Path] = None):
        """Initialize activity detector."""
        self.workspace_root = workspace_root or Path(".")
        self.agent_workspaces = self.workspace_root / "agent_workspaces"
        self.devlogs_dir = self.workspace_root / "devlogs"

    def detect_agent_activity(self, agent_id: str) -> Dict[str, Any]:
        """
        Detect all activity indicators for an agent.

        Returns dict with:
        - latest_activity: Most recent activity timestamp
        - activity_sources: List of activity sources found
        - activity_details: Detailed activity information
        """
        current_time = time.time()
        activities = []
        activity_details = {}

        # 1. Check status.json modification
        status_activity = self._check_status_json(agent_id)
        if status_activity:
            activities.append(status_activity)
            activity_details["status_json"] = status_activity

        # 2. Check inbox file modifications
        inbox_activity = self._check_inbox_files(agent_id)
        if inbox_activity:
            activities.append(inbox_activity)
            activity_details["inbox"] = inbox_activity

        # 3. Check devlog creation/modification
        devlog_activity = self._check_devlogs(agent_id)
        if devlog_activity:
            activities.append(devlog_activity)
            activity_details["devlogs"] = devlog_activity

        # 4. Check report files in workspace
        report_activity = self._check_reports(agent_id)
        if report_activity:
            activities.append(report_activity)
            activity_details["reports"] = report_activity

        # 5. Check message queue activity
        queue_activity = self._check_message_queue(agent_id)
        if queue_activity:
            activities.append(queue_activity)
            activity_details["message_queue"] = queue_activity

        # 6. Check any file modifications in agent workspace
        workspace_activity = self._check_workspace_files(agent_id)
        if workspace_activity:
            activities.append(workspace_activity)
            activity_details["workspace_files"] = workspace_activity

        # 7. Check git commits (if agent name in commit)
        git_activity = self._check_git_commits(agent_id)
        if git_activity:
            activities.append(git_activity)
            activity_details["git_commits"] = git_activity

        # 8. Check Discord devlog posts (Agent-1 proposal - MEDIUM priority)
        discord_activity = self._check_discord_posts(agent_id)
        if discord_activity:
            activities.append(discord_activity)
            activity_details["discord_posts"] = discord_activity

        # 9. Check tool execution (Agent-1 proposal - MEDIUM priority)
        tool_activity = self._check_tool_execution(agent_id)
        if tool_activity:
            activities.append(tool_activity)
            activity_details["tool_execution"] = tool_activity

        # 10. Check Swarm Brain contributions (Agent-1 proposal - LOW priority)
        swarm_brain_activity = self._check_swarm_brain(agent_id)
        if swarm_brain_activity:
            activities.append(swarm_brain_activity)
            activity_details["swarm_brain"] = swarm_brain_activity

        # 11. Check Agent lifecycle events (Agent-1 proposal - MEDIUM priority)
        lifecycle_activity = self._check_agent_lifecycle(agent_id)
        if lifecycle_activity:
            activities.append(lifecycle_activity)
            activity_details["agent_lifecycle"] = lifecycle_activity

        # Phase 1: High-priority signals
        # 12. Check terminal/command execution activity
        terminal_activity = self._check_terminal_activity(agent_id)
        if terminal_activity:
            activities.append(terminal_activity)
            activity_details["terminal"] = terminal_activity
        
        # 13. Check log file activity
        log_activity = self._check_log_file_activity(agent_id)
        if log_activity:
            activities.append(log_activity)
            activity_details["log"] = log_activity
        
        # Phase 2: Medium-priority signals
        # 14. Check process/application activity
        process_activity = self._check_process_activity(agent_id)
        if process_activity:
            activities.append(process_activity)
            activity_details["process"] = process_activity
        
        # 15. Check IDE/editor activity
        ide_activity = self._check_ide_activity(agent_id)
        if ide_activity:
            activities.append(ide_activity)
            activity_details["ide"] = ide_activity
        
        # 16. Check database activity
        database_activity = self._check_database_activity(agent_id)
        if database_activity:
            activities.append(database_activity)
            activity_details["database"] = database_activity

        # 17. Check ActivityEmitter telemetry events (HIGH priority - most reliable)
        activity_emitter_activity = self._check_activity_emitter_events(
            agent_id)
        if activity_emitter_activity:
            activities.append(activity_emitter_activity)
            activity_details["activity_emitter"] = activity_emitter_activity

        # 13. Check test execution activity (HIGH priority)
        test_execution_activity = self._check_test_execution(agent_id)
        if test_execution_activity:
            activities.append(test_execution_activity)
            activity_details["test_execution"] = test_execution_activity

        # 14. Check passdown.json modifications (Phase 2 - HIGH priority)
        passdown_activity = self._check_passdown_json(agent_id)
        if passdown_activity:
            activities.append(passdown_activity)
            activity_details["passdown"] = passdown_activity

        # 13. Check artifacts directory (root level) (Phase 2 - HIGH priority)
        artifacts_activity = self._check_artifacts_directory(agent_id)
        if artifacts_activity:
            activities.append(artifacts_activity)
            activity_details["artifacts"] = artifacts_activity

        # 14. Check cycle planner task files (Phase 2 - HIGH priority)
        cycle_planner_activity = self._check_cycle_planner(agent_id)
        if cycle_planner_activity:
            activities.append(cycle_planner_activity)
            activity_details["cycle_planner"] = cycle_planner_activity

        # 15. Check notes directory (Phase 2 - HIGH priority)
        notes_activity = self._check_notes_directory(agent_id)
        if notes_activity:
            activities.append(notes_activity)
            activity_details["notes"] = notes_activity

        # Phase 1: Agent-5 High-Priority Additional Signals (2025-12-11)
        # 16. Check contract system activity (HIGH priority - direct task indicator)
        contract_activity = self._check_contract_activity(agent_id)
        if contract_activity:
            activities.append(contract_activity)
            activity_details["contract_system"] = contract_activity

        # 17. Check inbox message processing (HIGH priority - direct engagement)
        inbox_processing_activity = self._check_inbox_processing(agent_id)
        if inbox_processing_activity:
            activities.append(inbox_processing_activity)
            activity_details["inbox_processing"] = inbox_processing_activity

        # 16. Check git working directory changes (Phase 2 - HIGH priority)
        git_working_activity = self._check_git_working_directory(agent_id)
        if git_working_activity:
            activities.append(git_working_activity)
            activity_details["git_working"] = git_working_activity

        # 17. Check activity log files (Agent-7 improvement - HIGH priority)
        activity_logs_activity = self._check_activity_logs(agent_id)
        if activity_logs_activity:
            activities.append(activity_logs_activity)
            activity_details["activity_logs"] = activity_logs_activity

        # Determine latest activity
        latest_activity = None
        if activities:
            latest_activity = max(activities, key=lambda x: x["timestamp"])

        return {
            "agent_id": agent_id,
            "latest_activity": latest_activity["timestamp"] if latest_activity else None,
            "latest_activity_source": latest_activity["source"] if latest_activity else None,
            "activity_count": len(activities),
            "activity_sources": [a["source"] for a in activities],
            "activity_details": activity_details,
            "detected_at": current_time,
        }

    def _check_status_json(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Check status.json file modification."""
        status_file = self.agent_workspaces / agent_id / "status.json"
        if not status_file.exists():
            return None

        mtime = status_file.stat().st_mtime

        # Also check last_updated field in JSON
        last_updated_str = None
        try:
            status_data = json.loads(status_file.read_text(encoding="utf-8"))
            last_updated_str = status_data.get("last_updated")
        except Exception:
            pass

        return {
            "source": "status_json",
            "timestamp": mtime,
            "file": str(status_file),
            "last_updated_field": last_updated_str,
            "age_seconds": time.time() - mtime,
        }

    def _check_inbox_files(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Check inbox file modifications."""
        inbox_dir = self.agent_workspaces / agent_id / "inbox"
        if not inbox_dir.exists():
            return None

        inbox_files = list(inbox_dir.glob("*.md"))
        if not inbox_files:
            return None

        # Get most recent inbox file
        latest_file = max(inbox_files, key=lambda p: p.stat().st_mtime)
        mtime = latest_file.stat().st_mtime

        return {
            "source": "inbox",
            "timestamp": mtime,
            "file": latest_file.name,
            "file_count": len(inbox_files),
            "age_seconds": time.time() - mtime,
        }

    def _check_devlogs(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Check devlog creation/modification."""
        devlogs = []

        # Check main devlogs directory
        if self.devlogs_dir.exists():
            patterns = [
                f"*{agent_id.lower()}*",
                f"*{agent_id.replace('-', '_').lower()}*",
                f"*{agent_id}*",
            ]
            for pattern in patterns:
                devlogs.extend(list(self.devlogs_dir.glob(f"{pattern}.md")))

        # Check agent workspace devlogs
        agent_devlogs_dir = self.agent_workspaces / agent_id / "devlogs"
        if agent_devlogs_dir.exists():
            devlogs.extend(list(agent_devlogs_dir.glob("*.md")))

        if not devlogs:
            return None

        latest_devlog = max(devlogs, key=lambda p: p.stat().st_mtime)
        mtime = latest_devlog.stat().st_mtime

        return {
            "source": "devlogs",
            "timestamp": mtime,
            "file": latest_devlog.name,
            "devlog_count": len(devlogs),
            "age_seconds": time.time() - mtime,
        }

    def _check_reports(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Check report files in agent workspace."""
        agent_dir = self.agent_workspaces / agent_id
        if not agent_dir.exists():
            return None

        # Find report files (markdown files in workspace root)
        reports = [f for f in agent_dir.glob("*.md") if f.name != "README.md"]
        if not reports:
            return None

        latest_report = max(reports, key=lambda p: p.stat().st_mtime)
        mtime = latest_report.stat().st_mtime

        return {
            "source": "reports",
            "timestamp": mtime,
            "file": latest_report.name,
            "report_count": len(reports),
            "age_seconds": time.time() - mtime,
        }

    def _check_message_queue(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Check message queue activity for agent."""
        try:
            from src.core.message_queue import MessageQueue

            queue = MessageQueue()
            queue_data = queue.get_queue_status()

            # Check for messages to/from this agent
            entries = queue_data.get("entries", [])
            agent_messages = [
                e for e in entries
                if isinstance(e, dict) and (
                    e.get("recipient") == agent_id or
                    e.get("sender") == agent_id
                )
            ]

            if not agent_messages:
                return None

            # Get most recent message
            latest_message = max(
                agent_messages,
                key=lambda e: e.get("created_at", 0)
            )

            created_at = latest_message.get("created_at", 0)
            if created_at == 0:
                return None

            return {
                "source": "message_queue",
                "timestamp": created_at,
                "message_count": len(agent_messages),
                "latest_status": latest_message.get("status"),
                "age_seconds": time.time() - created_at,
            }
        except Exception as e:
            logger.debug(f"Could not check message queue: {e}")
            return None

    def _check_workspace_files(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Check any file modifications in agent workspace."""
        agent_dir = self.agent_workspaces / agent_id
        if not agent_dir.exists():
            return None

        # Find all files (excluding common directories)
        exclude_dirs = {"__pycache__", ".git", "node_modules", ".venv"}
        all_files = []
        for file_path in agent_dir.rglob("*"):
            if file_path.is_file() and not any(
                exclude in file_path.parts for exclude in exclude_dirs
            ):
                all_files.append(file_path)

        if not all_files:
            return None

        # Get most recent file modification
        latest_file = max(all_files, key=lambda p: p.stat().st_mtime)
        mtime = latest_file.stat().st_mtime

        # Only return if recent (within last 24 hours)
        age_seconds = time.time() - mtime
        if age_seconds > 86400:  # 24 hours
            return None

        return {
            "source": "workspace_files",
            "timestamp": mtime,
            "file": latest_file.name,
            "file_count": len(all_files),
            "age_seconds": age_seconds,
        }

    def _check_git_commits(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Check git commits with agent name."""
        try:
            import subprocess

            # Check if git is available
            result = subprocess.run(
                ["git", "log", "--all", "--format=%H|%ct|%s", "--grep", agent_id],
                capture_output=True,
                text=True,
                timeout=TimeoutConstants.HTTP_QUICK,
                cwd=self.workspace_root,
            )

            if result.returncode != 0 or not result.stdout.strip():
                return None

            # Parse most recent commit
            lines = result.stdout.strip().split("\n")
            if not lines:
                return None

            # Get first commit (most recent)
            parts = lines[0].split("|", 2)
            if len(parts) < 2:
                return None

            commit_timestamp = int(parts[1])
            commit_message = parts[2] if len(parts) > 2 else ""

            return {
                "source": "git_commits",
                "timestamp": commit_timestamp,
                "commit_message": commit_message[:100],
                "age_seconds": time.time() - commit_timestamp,
            }
        except Exception as e:
            logger.debug(f"Could not check git commits: {e}")
            return None

    def _check_discord_posts(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Check Discord devlog posts (Agent-1 proposal - MEDIUM priority)."""
        try:
            # Check devlog manager logs
            devlog_log = Path("logs/devlog_posts.json")
            if devlog_log.exists():
                posts_data = json.loads(devlog_log.read_text(encoding="utf-8"))
                agent_posts = [
                    p for p in posts_data
                    if isinstance(p, dict) and p.get("agent_id", "").lower() == agent_id.lower()
                ]
                if agent_posts:
                    latest_post = max(
                        agent_posts, key=lambda p: p.get("timestamp", 0))
                    post_timestamp = latest_post.get("timestamp", 0)
                    if post_timestamp > 0:
                        return {
                            "source": "discord_posts",
                            "timestamp": post_timestamp,
                            "post_title": latest_post.get("title", "")[:100],
                            "age_seconds": time.time() - post_timestamp,
                        }

            # Check swarm_brain/devlogs for agent-specific devlogs (may have been posted)
            swarm_devlogs = self.workspace_root / "swarm_brain" / "devlogs"
            if swarm_devlogs.exists():
                agent_patterns = [
                    f"*{agent_id.lower()}*",
                    f"*{agent_id.replace('-', '_').lower()}*",
                    f"*{agent_id}*",
                ]
                all_devlogs = []
                for pattern in agent_patterns:
                    all_devlogs.extend(
                        list(swarm_devlogs.rglob(f"{pattern}.md")))

                if all_devlogs:
                    latest_devlog = max(
                        all_devlogs, key=lambda p: p.stat().st_mtime)
                    mtime = latest_devlog.stat().st_mtime
                    # Only return if recent (within 7 days - likely posted to Discord)
                    if time.time() - mtime < (7 * 24 * 3600):
                        return {
                            "source": "discord_posts",
                            "timestamp": mtime,
                            "file": latest_devlog.name,
                            "age_seconds": time.time() - mtime,
                        }

            return None
        except Exception as e:
            logger.debug(f"Could not check Discord posts: {e}")
            return None

    def _check_tool_execution(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Check tool execution activity (Agent-1 proposal - MEDIUM priority)."""
        try:
            # Check tool execution logs
            tool_logs = Path("logs/tool_executions.json")
            if tool_logs.exists():
                executions_data = json.loads(
                    tool_logs.read_text(encoding="utf-8"))
                agent_executions = [
                    e for e in executions_data
                    if isinstance(e, dict) and e.get("agent_id", "").lower() == agent_id.lower()
                ]
                if agent_executions:
                    latest_execution = max(
                        agent_executions, key=lambda e: e.get("timestamp", 0))
                    exec_timestamp = latest_execution.get("timestamp", 0)
                    if exec_timestamp > 0:
                        return {
                            "source": "tool_execution",
                            "timestamp": exec_timestamp,
                            "tool_name": latest_execution.get("tool_name", ""),
                            "age_seconds": time.time() - exec_timestamp,
                        }

            # Check toolbelt registry for recent tool runs
            try:
                from tools.toolbelt_registry import ToolbeltRegistry
                registry = ToolbeltRegistry()
                # This would need registry to track agent-specific executions
                # For now, return None if registry doesn't support this
            except Exception:
                pass

            return None
        except Exception as e:
            logger.debug(f"Could not check tool execution: {e}")
            return None

    def _check_swarm_brain(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Check Swarm Brain contributions (Agent-1 proposal - LOW priority)."""
        try:
            swarm_brain_dir = self.workspace_root / "swarm_brain"
            if not swarm_brain_dir.exists():
                return None

            # Check learning entries
            learning_files = list(swarm_brain_dir.rglob("*learning*.md"))
            agent_patterns = [
                agent_id.lower(),
                agent_id.replace('-', '_').lower(),
                agent_id,
            ]

            agent_learnings = []
            for learning_file in learning_files:
                try:
                    content = learning_file.read_text(encoding="utf-8").lower()
                    if any(pattern.lower() in content for pattern in agent_patterns):
                        agent_learnings.append(learning_file)
                except Exception:
                    continue

            if agent_learnings:
                latest_learning = max(
                    agent_learnings, key=lambda p: p.stat().st_mtime)
                mtime = latest_learning.stat().st_mtime
                return {
                    "source": "swarm_brain",
                    "timestamp": mtime,
                    "file": latest_learning.name,
                    "age_seconds": time.time() - mtime,
                }

            # Check swarm memory data file if it exists
            swarm_memory_file = swarm_brain_dir / "swarm_memory.json"
            if swarm_memory_file.exists():
                try:
                    memory_data = json.loads(
                        swarm_memory_file.read_text(encoding="utf-8"))
                    # Check for agent contributions in memory
                    if isinstance(memory_data, dict):
                        learnings = memory_data.get("learnings", [])
                        agent_contributions = [
                            l for l in learnings
                            if isinstance(l, dict) and agent_id.lower() in str(l.get("agent", "")).lower()
                        ]
                        if agent_contributions:
                            # Get most recent contribution timestamp
                            latest_contrib = max(
                                agent_contributions,
                                key=lambda c: c.get("timestamp", 0)
                            )
                            contrib_timestamp = latest_contrib.get(
                                "timestamp", 0)
                            if contrib_timestamp > 0:
                                return {
                                    "source": "swarm_brain",
                                    "timestamp": contrib_timestamp,
                                    "contribution_type": "learning",
                                    "age_seconds": time.time() - contrib_timestamp,
                                }
                except Exception:
                    pass

            return None
        except Exception as e:
            logger.debug(f"Could not check Swarm Brain: {e}")
            return None

    def _check_agent_lifecycle(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Check AgentLifecycle class events (Agent-1 proposal - MEDIUM priority)."""
        try:
            # Check if AgentLifecycle is being used by checking status.json for lifecycle indicators
            status_file = self.agent_workspaces / agent_id / "status.json"
            if not status_file.exists():
                return None

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
