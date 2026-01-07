#!/usr/bin/env python3
"""
Activity Source Checkers (Tier 1)
==================================

Tier 1 activity source checkers for hardened activity detector.
These checkers detect the most reliable activity signals:
- Telemetry events
- Git commits
- Contract system activity
- Test execution

<!-- SSOT Domain: infrastructure -->

V2 Compliance | Author: Agent-3 | Date: 2025-12-14
"""

import json
import logging
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from .activity_detector_models import (
    ActivitySource,
    ActivitySignal,
)

logger = logging.getLogger(__name__)


class ActivitySourceCheckers:
    """Tier 1 activity source checkers."""

    def __init__(
        self,
        workspace_root: Path,
        agent_workspaces: Path,
        activity_event_file: Path,
        noise_patterns: Optional[Set[str]] = None,
    ):
        """Initialize activity source checkers."""
        self.workspace_root = workspace_root
        self.agent_workspaces = agent_workspaces
        self.activity_event_file = activity_event_file
        self.noise_patterns = noise_patterns or {
            "resumer", "stall-recovery", "no-acknowledgments",
            "inactivity detected", "[c2a]", "#no-reply", "#progress-only"
        }

    def check_telemetry_events(
        self,
        agent_id: str,
        lookback_time: datetime
    ) -> List[ActivitySignal]:
        """Check ActivityEmitter telemetry events (Tier 1)."""
        signals = []

        if not self.activity_event_file.exists():
            return signals

        try:
            with open(self.activity_event_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                # Check last 200 lines for performance
                recent_lines = lines[-200:] if len(lines) > 200 else lines

                for line in recent_lines:
                    if not line.strip():
                        continue

                    try:
                        event = json.loads(line.strip())
                        if event.get("agent", "").lower() != agent_id.lower():
                            continue

                        ts_raw = event.get("ts")
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

                        # Determine event type and confidence
                        event_type = (event.get("type") or "").upper()
                        confidence = self._get_telemetry_confidence(event_type)

                        signals.append(ActivitySignal(
                            source=ActivitySource.TELEMETRY_EVENT,
                            timestamp=ts.timestamp(),
                            confidence=confidence,
                            metadata={
                                "event_type": event_type,
                                "source": event.get("source", ""),
                                "summary": event.get("summary", "")
                            },
                            agent_id=agent_id
                        ))
                    except json.JSONDecodeError:
                        continue
        except Exception as e:
            logger.debug(f"Error reading telemetry events: {e}")

        return signals

    def _get_telemetry_confidence(self, event_type: str) -> float:
        """Get confidence score for telemetry event type."""
        tier1_events = {
            "TASK_COMPLETED", "GIT_PUSH", "MONEY_METRIC",
            "TOOL_RUN_FAILURE", "VALIDATION_PASS"
        }
        tier2_events = {
            "TOOL_RUN_SUCCESS", "BRAIN_WRITE", "TASK_CLAIMED"
        }

        if event_type in tier1_events:
            return ActivitySource.TELEMETRY_EVENT.base_confidence
        elif event_type in tier2_events:
            return ActivitySource.TELEMETRY_EVENT.base_confidence * 0.8
        else:
            return ActivitySource.TELEMETRY_EVENT.base_confidence * 0.6

    def check_git_activity(
        self,
        agent_id: str,
        lookback_time: datetime
    ) -> List[ActivitySignal]:
        """Check git commits (Tier 1)."""
        signals = []

        try:
            from src.core.config.timeout_constants import TimeoutConstants

            result = subprocess.run(
                ["git", "log", "--since", lookback_time.isoformat(),
                 "--format=%H|%ct|%s", "--grep", agent_id, "--all"],
                capture_output=True,
                text=True,
                timeout=TimeoutConstants.HTTP_QUICK,
                cwd=self.workspace_root,
            )

            if result.returncode == 0 and result.stdout.strip():
                for line in result.stdout.strip().split("\n"):
                    if not line:
                        continue
                    parts = line.split("|", 2)
                    if len(parts) >= 2:
                        try:
                            commit_time = int(parts[1])
                            commit_msg = parts[2] if len(parts) > 2 else ""

                            # Filter out resume-related commits
                            if any(noise in commit_msg.lower() for noise in self.noise_patterns):
                                continue

                            signals.append(ActivitySignal(
                                source=ActivitySource.GIT_COMMIT,
                                timestamp=commit_time,
                                confidence=ActivitySource.GIT_COMMIT.base_confidence,
                                metadata={
                                    "hash": parts[0][:8],
                                    "message": commit_msg[:100]
                                },
                                agent_id=agent_id
                            ))
                        except (ValueError, IndexError):
                            continue
        except Exception as e:
            logger.debug(f"Error checking git activity: {e}")

        return signals

    def check_git_activity_by_path(
        self,
        agent_id: str,
        lookback_time: datetime,
        existing_signals: Optional[List[ActivitySignal]] = None
    ) -> List[ActivitySignal]:
        """
        Check git commits that modify agent-specific files (Tier 1).

        This complements check_git_activity by detecting commits that modify
        agent files even if the agent ID isn't in the commit message.
        """
        signals = []
        existing_hashes = set()
        if existing_signals:
            existing_hashes = {
                s.metadata.get("hash", "")[:8]
                for s in existing_signals
                if s.metadata.get("hash")
            }

        try:
            from src.core.config.timeout_constants import TimeoutConstants

            # Agent-specific paths to check
            agent_paths = [f"agent_workspaces/{agent_id}/"]

            # Add captain reports for Agent-4
            if agent_id == "Agent-4":
                agent_paths.append("docs/captain_reports/")

            for path_pattern in agent_paths:
                try:
                    result = subprocess.run(
                        ["git", "log", "--since", lookback_time.isoformat(),
                         "--format=%H|%ct|%s", "--name-only", "--", path_pattern],
                        capture_output=True,
                        text=True,
                        timeout=TimeoutConstants.HTTP_QUICK,
                        cwd=self.workspace_root,
                    )

                    if result.returncode != 0 or not result.stdout.strip():
                        continue

                    # Parse git log output with file names
                    commits = self._parse_git_log_with_files(result.stdout)

                    for commit in commits:
                        commit_time = commit['timestamp']
                        commit_msg = commit['message']

                        # Skip if before lookback time
                        if commit_time < lookback_time.timestamp():
                            continue

                        # Filter out resume-related commits
                        if any(noise in commit_msg.lower()
                               for noise in self.noise_patterns):
                            continue

                        # Only add if we haven't already detected this commit
                        commit_hash = commit['hash']
                        if commit_hash[:8] in existing_hashes:
                            continue

                        signals.append(ActivitySignal(
                            source=ActivitySource.GIT_COMMIT,
                            timestamp=commit_time,
                            confidence=ActivitySource.GIT_COMMIT.base_confidence,
                            metadata={
                                "hash": commit_hash[:8],
                                "message": commit_msg[:100],
                                # Limit file list
                                "files": commit.get('files', [])[:5],
                                "detection_method": "file_path"
                            },
                            agent_id=agent_id
                        ))
                except Exception as e:
                    logger.debug(
                        f"Error checking git activity by path {path_pattern} "
                        f"for {agent_id}: {e}"
                    )
                    continue
        except Exception as e:
            logger.debug(
                f"Error in git activity by path check for {agent_id}: {e}")

        return signals

    def _parse_git_log_with_files(self, output: str) -> List[Dict[str, Any]]:
        """
        Parse git log output with --name-only format.

        Format:
        commit_hash|timestamp|message
        file1
        file2
        file3

        commit_hash|timestamp|message
        ...
        """
        commits = []
        lines = output.strip().split("\n")

        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if not line:
                i += 1
                continue

            # Check if this is a commit line (has | separator)
            if "|" in line:
                parts = line.split("|", 2)
                if len(parts) >= 2:
                    commit_hash = parts[0]
                    try:
                        commit_time = int(parts[1])
                        commit_msg = parts[2] if len(parts) > 2 else ""

                        # Collect files for this commit
                        files = []
                        i += 1
                        while i < len(lines):
                            file_line = lines[i].strip()
                            if not file_line:
                                i += 1
                                break
                            if "|" in file_line:
                                # Next commit, go back one line
                                i -= 1
                                break
                            files.append(file_line)
                            i += 1

                        commits.append({
                            "hash": commit_hash,
                            "timestamp": commit_time,
                            "message": commit_msg,
                            "files": files
                        })
                    except (ValueError, IndexError):
                        pass
            i += 1

        return commits

    def check_contract_activity(
        self,
        agent_id: str,
        lookback_time: datetime
    ) -> List[ActivitySignal]:
        """Check contract system activity (Tier 1)."""
        signals = []

        try:
            from src.services.unified_service_managers import UnifiedContractManager
            manager = UnifiedContractManager()
            agent_status = manager.get_agent_status(agent_id)

            contracts = agent_status.get("contracts", [])
            active_contracts = agent_status.get("active_contracts", 0)

            if active_contracts > 0 and contracts:
                latest_contract = max(
                    contracts,
                    key=lambda c: c.get("assigned_at", 0) or c.get(
                        "updated_at", 0) or 0
                )

                timestamp = latest_contract.get(
                    "assigned_at") or latest_contract.get("updated_at")
                if timestamp:
                    try:
                        if isinstance(timestamp, str):
                            ts = datetime.fromisoformat(
                                timestamp.replace("Z", "+00:00")
                            ).replace(tzinfo=None)
                        else:
                            ts = datetime.fromtimestamp(timestamp)

                        if ts >= lookback_time:
                            signals.append(ActivitySignal(
                                source=ActivitySource.CONTRACT_CLAIMED,
                                timestamp=ts.timestamp(),
                                confidence=ActivitySource.CONTRACT_CLAIMED.base_confidence,
                                metadata={
                                    "contract_id": latest_contract.get("contract_id", ""),
                                    "title": latest_contract.get("title", "")[:50],
                                    "status": latest_contract.get("status", "")
                                },
                                agent_id=agent_id
                            ))
                    except Exception:
                        pass
        except Exception as e:
            logger.debug(f"Error checking contract activity: {e}")

        return signals

    def check_test_execution(
        self,
        agent_id: str,
        lookback_time: datetime
    ) -> List[ActivitySignal]:
        """Check test execution activity (Tier 1)."""
        signals = []

        # Check pytest cache
        pytest_cache = self.workspace_root / ".pytest_cache"
        if pytest_cache.exists():
            try:
                mtime = pytest_cache.stat().st_mtime
                if mtime >= lookback_time.timestamp():
                    signals.append(ActivitySignal(
                        source=ActivitySource.TEST_EXECUTION,
                        timestamp=mtime,
                        confidence=ActivitySource.TEST_EXECUTION.base_confidence,
                        metadata={"type": "pytest_cache"},
                        agent_id=agent_id
                    ))
            except Exception:
                pass

        # Check coverage files
        coverage_file = self.workspace_root / ".coverage"
        if coverage_file.exists():
            try:
                mtime = coverage_file.stat().st_mtime
                if mtime >= lookback_time.timestamp():
                    signals.append(ActivitySignal(
                        source=ActivitySource.TEST_EXECUTION,
                        timestamp=mtime,
                        confidence=ActivitySource.TEST_EXECUTION.base_confidence * 0.9,
                        metadata={"type": "coverage"},
                        agent_id=agent_id
                    ))
            except Exception:
                pass

        return signals


__all__ = ["ActivitySourceCheckers"]
