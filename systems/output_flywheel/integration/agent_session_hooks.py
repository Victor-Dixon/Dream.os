"""
Agent End-of-Session Integration Hooks
=======================================

Automatically assembles work_session.json and triggers Output Flywheel
when agents complete work sessions.

Integration points:
- status.json updates
- Git tracking (commits, files changed)
- Agent workflows
- Trading systems
"""

from __future__ import annotations

import json
import logging
import subprocess
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

# Project root for resolving paths
PROJECT_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_ROOT = PROJECT_ROOT / "systems" / "output_flywheel" / "outputs"
SESSIONS_DIR = OUTPUT_ROOT / "sessions"


class AgentSessionHook:
    """
    End-of-session hook for automatic work_session.json assembly and
    Output Flywheel pipeline execution.
    """

    def __init__(self, agent_id: str, workspace_root: Optional[Path] = None):
        """
        Initialize session hook.
        
        Args:
            agent_id: Agent identifier (e.g., "Agent-1")
            workspace_root: Root of workspace (default: PROJECT_ROOT)
        """
        self.agent_id = agent_id
        self.workspace_root = workspace_root or PROJECT_ROOT
        self.agent_workspace = self.workspace_root / "agent_workspaces" / agent_id
        self.status_file = self.agent_workspace / "status.json"
        SESSIONS_DIR.mkdir(parents=True, exist_ok=True)

    def assemble_work_session(
        self,
        session_type: str,
        metadata: Optional[Dict[str, Any]] = None,
        source_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Assemble work_session.json from agent session data.
        
        Args:
            session_type: "build", "trade", or "life_aria"
            metadata: Session metadata (duration, metrics, etc.)
            source_data: Source data (commits, trades, conversations)
        
        Returns:
            Complete work_session.json structure
        """
        session_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat() + "Z"
        
        # Load status.json for agent context
        status_data = self._load_status()
        
        # Auto-collect git data if build session and repo available
        if session_type == "build" and not source_data:
            source_data = self._collect_git_data()
        
        # Auto-collect metadata if not provided
        if not metadata:
            metadata = self._collect_session_metadata(status_data)
        
        session = {
            "session_id": session_id,
            "session_type": session_type,
            "timestamp": timestamp,
            "agent_id": self.agent_id,
            "metadata": metadata or {},
            "source_data": source_data or {},
            "artifacts": {},
            "pipeline_status": {
                "build_artifact": "pending" if session_type == "build" else "not_applicable",
                "trade_artifact": "pending" if session_type == "trade" else "not_applicable",
                "life_aria_artifact": "pending" if session_type == "life_aria" else "not_applicable",
            },
        }
        
        return session

    def save_session(self, session: Dict[str, Any]) -> Path:
        """
        Save work_session.json to disk.
        
        Args:
            session: Work session data
        
        Returns:
            Path to saved session file
        """
        session_id = session["session_id"]
        session_type = session["session_type"]
        session_file = SESSIONS_DIR / f"{session_id}_{session_type}.json"
        
        session_file.write_text(json.dumps(session, indent=2), encoding="utf-8")
        logger.info(f"✅ Saved work_session.json: {session_file}")
        
        return session_file

    def trigger_pipeline(self, session_file: Path) -> bool:
        """
        Trigger Output Flywheel pipeline for session.
        
        Args:
            session_file: Path to work_session.json file
        
        Returns:
            True if pipeline executed successfully
        """
        try:
            result = subprocess.run(
                [
                    "python",
                    str(PROJECT_ROOT / "tools" / "run_output_flywheel.py"),
                    "--session-file",
                    str(session_file),
                ],
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout
                cwd=str(PROJECT_ROOT),
            )
            
            if result.returncode == 0:
                logger.info(f"✅ Output Flywheel pipeline completed for {session_file.name}")
                return True
            else:
                logger.error(f"❌ Pipeline failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error("❌ Pipeline timed out after 5 minutes")
            return False
        except Exception as e:
            logger.error(f"❌ Pipeline execution error: {e}")
            return False

    def end_of_session(
        self,
        session_type: str,
        metadata: Optional[Dict[str, Any]] = None,
        source_data: Optional[Dict[str, Any]] = None,
        auto_trigger: bool = True,
    ) -> Optional[Dict[str, Any]]:
        """
        Complete end-of-session workflow: assemble, save, and trigger pipeline.
        
        Args:
            session_type: "build", "trade", or "life_aria"
            metadata: Optional session metadata
            source_data: Optional source data
            auto_trigger: Whether to automatically trigger pipeline (default: True)
        
        Returns:
            Updated session data with artifacts, or None if failed
        """
        try:
            # 1. Assemble work_session.json
            session = self.assemble_work_session(session_type, metadata, source_data)
            
            # 2. Save session file
            session_file = self.save_session(session)
            
            # 3. Trigger pipeline if requested
            if auto_trigger:
                success = self.trigger_pipeline(session_file)
                if success:
                    # 4. Load updated session to get artifacts
                    updated_session = json.loads(session_file.read_text(encoding="utf-8"))
                    return updated_session
            
            return session
            
        except Exception as e:
            logger.error(f"❌ End-of-session workflow failed: {e}", exc_info=True)
            return None

    def _load_status(self) -> Dict[str, Any]:
        """Load agent status.json."""
        if self.status_file.exists():
            try:
                return json.loads(self.status_file.read_text(encoding="utf-8"))
            except Exception as e:
                logger.warning(f"Failed to load status.json: {e}")
        return {}

    def _collect_session_metadata(self, status_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Auto-collect session metadata from status.json.
        
        Args:
            status_data: Agent status.json data
        
        Returns:
            Session metadata dictionary
        """
        metadata = {
            "agent_name": status_data.get("agent_name", self.agent_id),
            "current_mission": status_data.get("current_mission", ""),
            "completed_tasks": status_data.get("completed_tasks", []),
            "achievements": status_data.get("achievements", []),
        }
        
        # Calculate duration if timestamps available
        last_updated = status_data.get("last_updated")
        if last_updated:
            try:
                last_time = datetime.strptime(last_updated, "%Y-%m-%d %H:%M:%S")
                now = datetime.now()
                duration_minutes = int((now - last_time).total_seconds() / 60)
                metadata["duration_minutes"] = duration_minutes
            except Exception:
                pass
        
        return metadata

    def _collect_git_data(self) -> Dict[str, Any]:
        """
        Auto-collect git data from repository.
        
        Returns:
            Source data dictionary with git commits and repo info
        """
        try:
            # Get repo path (default to workspace root)
            repo_path = str(self.workspace_root)
            
            # Get recent commits (last 10)
            commits = self._get_recent_commits(repo_path, limit=10)
            
            # Get files changed
            files_changed = self._get_files_changed(repo_path)
            
            return {
                "repo_path": repo_path,
                "git_commits": commits,
                "files_changed": files_changed,
            }
        except Exception as e:
            logger.warning(f"Failed to collect git data: {e}")
            return {"repo_path": str(self.workspace_root)}

    def _get_recent_commits(self, repo_path: str, limit: int = 10) -> list[Dict[str, Any]]:
        """Get recent git commits."""
        try:
            result = subprocess.run(
                [
                    "git",
                    "log",
                    f"--max-count={limit}",
                    "--pretty=format:%H|%an|%ad|%s",
                    "--date=iso",
                ],
                capture_output=True,
                text=True,
                cwd=repo_path,
                timeout=10,
            )
            
            if result.returncode != 0:
                return []
            
            commits = []
            for line in result.stdout.strip().split("\n"):
                if not line:
                    continue
                parts = line.split("|", 3)
                if len(parts) == 4:
                    commits.append({
                        "hash": parts[0],
                        "author": parts[1],
                        "timestamp": parts[2],
                        "message": parts[3],
                        "files": [],  # Could be populated with git diff --name-only
                    })
            
            return commits
        except Exception as e:
            logger.warning(f"Failed to get git commits: {e}")
            return []

    def _get_files_changed(self, repo_path: str) -> list[str]:
        """Get list of files changed in recent commits."""
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", "HEAD~5..HEAD"],
                capture_output=True,
                text=True,
                cwd=repo_path,
                timeout=10,
            )
            
            if result.returncode != 0:
                return []
            
            return [f.strip() for f in result.stdout.strip().split("\n") if f.strip()]
        except Exception as e:
            logger.warning(f"Failed to get files changed: {e}")
            return []


def end_of_session_hook(
    agent_id: str,
    session_type: str,
    metadata: Optional[Dict[str, Any]] = None,
    source_data: Optional[Dict[str, Any]] = None,
    auto_trigger: bool = True,
) -> Optional[Dict[str, Any]]:
    """
    Convenience function for end-of-session integration.
    
    Usage:
        from systems.output_flywheel.integration.agent_session_hooks import end_of_session_hook
        
        artifacts = end_of_session_hook(
            agent_id="Agent-1",
            session_type="build",
            auto_trigger=True
        )
    
    Args:
        agent_id: Agent identifier
        session_type: "build", "trade", or "life_aria"
        metadata: Optional session metadata
        source_data: Optional source data
        auto_trigger: Whether to automatically trigger pipeline
    
    Returns:
        Updated session data with artifacts, or None if failed
    """
    hook = AgentSessionHook(agent_id)
    return hook.end_of_session(session_type, metadata, source_data, auto_trigger)

