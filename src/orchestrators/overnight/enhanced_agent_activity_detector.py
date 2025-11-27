"""
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
                timeout=5,
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
                    latest_post = max(agent_posts, key=lambda p: p.get("timestamp", 0))
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
                    all_devlogs.extend(list(swarm_devlogs.rglob(f"{pattern}.md")))
                
                if all_devlogs:
                    latest_devlog = max(all_devlogs, key=lambda p: p.stat().st_mtime)
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
                executions_data = json.loads(tool_logs.read_text(encoding="utf-8"))
                agent_executions = [
                    e for e in executions_data
                    if isinstance(e, dict) and e.get("agent_id", "").lower() == agent_id.lower()
                ]
                if agent_executions:
                    latest_execution = max(agent_executions, key=lambda e: e.get("timestamp", 0))
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
                latest_learning = max(agent_learnings, key=lambda p: p.stat().st_mtime)
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
                    memory_data = json.loads(swarm_memory_file.read_text(encoding="utf-8"))
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
                            contrib_timestamp = latest_contrib.get("timestamp", 0)
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
                status_data = json.loads(status_file.read_text(encoding="utf-8"))
                
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

