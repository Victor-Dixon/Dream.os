"""
Hardened Agent Activity Detector
=================================

Multi-source activity detection with confidence scoring and cross-validation.
Designed to prevent false positives when determining if agents are active.

Key Features:
- Multi-source validation (status.json, file mods, telemetry, contracts)
- Confidence scoring (0.0-1.0) based on source reliability
- Cross-validation between detection methods
- Noise filtering (resume prompts, acknowledgments)
- Temporal validation (activity recency checks)

V2 Compliance: <400 lines, single responsibility
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-01-27
Priority: CRITICAL - Prevents false resume prompts
"""

import json
import logging
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class ActivityConfidence(Enum):
    """Confidence levels for activity detection."""
    VERY_HIGH = 0.9  # Multiple tier-1 sources agree
    HIGH = 0.7  # Single tier-1 source or multiple tier-2
    MEDIUM = 0.5  # Single tier-2 source
    LOW = 0.3  # Weak signal, needs validation
    VERY_LOW = 0.1  # Unreliable signal


class ActivitySource(Enum):
    """Activity source types with reliability tiers."""
    # Tier 1: Most reliable (direct agent actions)
    TELEMETRY_EVENT = (1, 0.9)  # ActivityEmitter events
    GIT_COMMIT = (1, 0.85)  # Git commits with agent name
    CONTRACT_CLAIMED = (1, 0.85)  # Contract system activity
    TEST_EXECUTION = (1, 0.8)  # Test runs
    
    # Tier 2: Reliable (file modifications)
    STATUS_UPDATE = (2, 0.7)  # status.json with meaningful content
    FILE_MODIFICATION = (2, 0.65)  # Workspace file changes
    DEVLOG_CREATED = (2, 0.7)  # Devlog creation
    INBOX_PROCESSING = (2, 0.6)  # Inbox message processing
    
    # Tier 3: Less reliable (indirect signals)
    MESSAGE_QUEUE = (3, 0.4)  # Message queue activity
    WORKSPACE_ACCESS = (3, 0.3)  # File access patterns
    
    def __init__(self, tier: int, base_confidence: float):
        self.tier = tier
        self.base_confidence = base_confidence


@dataclass
class ActivitySignal:
    """Detected activity signal with metadata."""
    source: ActivitySource
    timestamp: float
    confidence: float
    metadata: Dict[str, Any]
    agent_id: str


@dataclass
class ActivityAssessment:
    """Final assessment of agent activity."""
    agent_id: str
    is_active: bool
    confidence: float
    last_activity: Optional[datetime]
    inactivity_minutes: float
    signals: List[ActivitySignal]
    validation_passed: bool
    reasons: List[str]


class HardenedActivityDetector:
    """
    Hardened activity detector with multi-source validation.
    
    Uses multiple detection methods and cross-validates results
    to prevent false positives.
    """
    
    def __init__(self, workspace_root: Optional[Path] = None):
        """Initialize hardened activity detector."""
        self.workspace_root = workspace_root or Path(".")
        self.agent_workspaces = self.workspace_root / "agent_workspaces"
        self.activity_event_file = Path("runtime") / "agent_comms" / "activity_events.jsonl"
        
        # Noise patterns to filter out
        self.noise_patterns = {
            "resumer", "stall-recovery", "no-acknowledgments",
            "inactivity detected", "[c2a]", "#no-reply", "#progress-only"
        }
        
        # Minimum confidence threshold to consider agent active
        self.min_confidence_threshold = 0.5
        
        # Time windows for activity validation
        self.tier1_window_seconds = 3600  # 1 hour for tier-1 sources
        self.tier2_window_seconds = 1800  # 30 min for tier-2 sources
        self.tier3_window_seconds = 900  # 15 min for tier-3 sources
    
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
        
        # Collect signals from all sources
        signals.extend(self._check_telemetry_events(agent_id, lookback_time))
        signals.extend(self._check_git_activity(agent_id, lookback_time))
        signals.extend(self._check_git_activity_by_path(agent_id, lookback_time))
        signals.extend(self._check_contract_activity(agent_id, lookback_time))
        signals.extend(self._check_test_execution(agent_id, lookback_time))
        signals.extend(self._check_status_updates(agent_id, lookback_time))
        signals.extend(self._check_file_modifications(agent_id, lookback_time))
        signals.extend(self._check_devlog_activity(agent_id, lookback_time))
        signals.extend(self._check_inbox_processing(agent_id, lookback_time))
        
        # Filter out noise
        signals = self._filter_noise(signals)
        
        # Sort by timestamp (most recent first)
        signals.sort(key=lambda s: s.timestamp, reverse=True)
        
        # Calculate overall confidence
        confidence, reasons = self._calculate_confidence(signals, lookback_time)
        
        # Determine if agent is active
        last_activity = None
        if signals:
            last_activity = datetime.fromtimestamp(signals[0].timestamp)
        
        inactivity_minutes = (
            (datetime.now() - last_activity).total_seconds() / 60
            if last_activity else float("inf")
        )
        
        # Cross-validation: Check if signals are consistent
        validation_passed = self._validate_signals(signals, lookback_time)
        
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
    
    def _check_telemetry_events(
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
    
    def _check_git_activity(
        self,
        agent_id: str,
        lookback_time: datetime
    ) -> List[ActivitySignal]:
        """Check git commits (Tier 1)."""
        signals = []
        
        try:
            import subprocess
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
    
    def _check_git_activity_by_path(
        self,
        agent_id: str,
        lookback_time: datetime
    ) -> List[ActivitySignal]:
        """
        Check git commits that modify agent-specific files (Tier 1).
        
        This complements _check_git_activity by detecting commits that modify
        agent files even if the agent ID isn't in the commit message.
        """
        signals = []
        
        try:
            import subprocess
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
                    # Format: commit_hash|timestamp|message\nfile1\nfile2\n\ncommit_hash|...
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
                        # (avoid duplicates from _check_git_activity)
                        commit_hash = commit['hash']
                        duplicate = any(
                            s.metadata.get("hash") == commit_hash[:8]
                            for s in signals
                        )
                        
                        if not duplicate:
                            signals.append(ActivitySignal(
                                source=ActivitySource.GIT_COMMIT,
                                timestamp=commit_time,
                                confidence=ActivitySource.GIT_COMMIT.base_confidence,
                                metadata={
                                    "hash": commit_hash[:8],
                                    "message": commit_msg[:100],
                                    "files": commit.get('files', [])[:5],  # Limit file list
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
            logger.debug(f"Error in git activity by path check for {agent_id}: {e}")
        
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
    
    def _check_contract_activity(
        self,
        agent_id: str,
        lookback_time: datetime
    ) -> List[ActivitySignal]:
        """Check contract system activity (Tier 1)."""
        signals = []
        
        try:
            from src.services.contract_system.manager import ContractManager
            manager = ContractManager()
            agent_status = manager.get_agent_status(agent_id)
            
            contracts = agent_status.get("contracts", [])
            active_contracts = agent_status.get("active_contracts", 0)
            
            if active_contracts > 0 and contracts:
                latest_contract = max(
                    contracts,
                    key=lambda c: c.get("assigned_at", 0) or c.get("updated_at", 0) or 0
                )
                
                timestamp = latest_contract.get("assigned_at") or latest_contract.get("updated_at")
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
    
    def _check_test_execution(
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
    
    def _check_status_updates(
        self,
        agent_id: str,
        lookback_time: datetime
    ) -> List[ActivitySignal]:
        """Check status.json updates (Tier 2)."""
        signals = []
        status_file = self.agent_workspaces / agent_id / "status.json"
        
        if not status_file.exists():
            return signals
        
        try:
            mtime = status_file.stat().st_mtime
            if mtime < lookback_time.timestamp():
                return signals
            
            # Read status to validate meaningful content
            with open(status_file, 'r', encoding='utf-8') as f:
                status = json.load(f)
            
            # Check if status has meaningful content (not just noise)
            last_updated_str = status.get("last_updated", "")
            mission = status.get("current_mission", "")
            current_tasks = status.get("current_tasks", [])
            
            # Require meaningful content to count as activity
            if not (mission.strip() or current_tasks):
                return signals
            
            # Parse last_updated timestamp
            try:
                if 'T' in last_updated_str:
                    last_updated = datetime.fromisoformat(
                        last_updated_str.replace("Z", "+00:00")
                    ).replace(tzinfo=None)
                else:
                    last_updated = datetime.strptime(
                        last_updated_str, "%Y-%m-%d %H:%M:%S"
                    )
                
                if last_updated >= lookback_time:
                    signals.append(ActivitySignal(
                        source=ActivitySource.STATUS_UPDATE,
                        timestamp=last_updated.timestamp(),
                        confidence=ActivitySource.STATUS_UPDATE.base_confidence,
                        metadata={
                            "status": status.get("status", ""),
                            "mission": mission[:50],
                            "task_count": len(current_tasks)
                        },
                        agent_id=agent_id
                    ))
            except Exception:
                # Fallback to file mtime
                signals.append(ActivitySignal(
                    source=ActivitySource.STATUS_UPDATE,
                    timestamp=mtime,
                    confidence=ActivitySource.STATUS_UPDATE.base_confidence * 0.7,
                    metadata={"file_mtime": True},
                    agent_id=agent_id
                ))
        except Exception as e:
            logger.debug(f"Error checking status updates: {e}")
        
        return signals
    
    def _check_file_modifications(
        self,
        agent_id: str,
        lookback_time: datetime
    ) -> List[ActivitySignal]:
        """Check file modifications in workspace (Tier 2)."""
        signals = []
        agent_dir = self.agent_workspaces / agent_id
        
        if not agent_dir.exists():
            return signals
        
        try:
            exclude_dirs = {"__pycache__", ".git", "node_modules", ".venv", "inbox"}
            exclude_files = {"status.json"}  # Checked separately
            
            latest_mtime = 0
            file_count = 0
            
            for file_path in agent_dir.rglob("*"):
                if file_path.is_file():
                    if any(exclude in file_path.parts for exclude in exclude_dirs):
                        continue
                    if file_path.name in exclude_files:
                        continue
                    
                    try:
                        mtime = file_path.stat().st_mtime
                        if mtime >= lookback_time.timestamp():
                            latest_mtime = max(latest_mtime, mtime)
                            file_count += 1
                    except (OSError, PermissionError):
                        continue
            
            if latest_mtime > 0 and file_count > 0:
                signals.append(ActivitySignal(
                    source=ActivitySource.FILE_MODIFICATION,
                    timestamp=latest_mtime,
                    confidence=ActivitySource.FILE_MODIFICATION.base_confidence,
                    metadata={"file_count": file_count},
                    agent_id=agent_id
                ))
        except Exception as e:
            logger.debug(f"Error checking file modifications: {e}")
        
        return signals
    
    def _check_devlog_activity(
        self,
        agent_id: str,
        lookback_time: datetime
    ) -> List[ActivitySignal]:
        """Check devlog creation (Tier 2)."""
        signals = []
        devlogs_dir = Path("devlogs")
        
        if not devlogs_dir.exists():
            return signals
        
        try:
            patterns = [
                f"*{agent_id.lower()}*",
                f"*{agent_id.replace('-', '_').lower()}*",
            ]
            
            for pattern in patterns:
                for devlog_file in devlogs_dir.glob(f"{pattern}.md"):
                    try:
                        mtime = devlog_file.stat().st_mtime
                        if mtime >= lookback_time.timestamp():
                            signals.append(ActivitySignal(
                                source=ActivitySource.DEVLOG_CREATED,
                                timestamp=mtime,
                                confidence=ActivitySource.DEVLOG_CREATED.base_confidence,
                                metadata={"file": devlog_file.name},
                                agent_id=agent_id
                            ))
                            break  # Only need one recent devlog
                    except (OSError, PermissionError):
                        continue
        except Exception as e:
            logger.debug(f"Error checking devlog activity: {e}")
        
        return signals
    
    def _check_inbox_processing(
        self,
        agent_id: str,
        lookback_time: datetime
    ) -> List[ActivitySignal]:
        """Check inbox message processing (Tier 2)."""
        signals = []
        inbox_dir = self.agent_workspaces / agent_id / "inbox"
        
        if not inbox_dir.exists():
            return signals
        
        try:
            # Check for processed/read indicators
            processed_files = list(inbox_dir.glob("*_processed.md"))
            read_files = list(inbox_dir.glob("*_read.md"))
            
            all_processed = processed_files + read_files
            if all_processed:
                latest = max(all_processed, key=lambda p: p.stat().st_mtime)
                mtime = latest.stat().st_mtime
                
                if mtime >= lookback_time.timestamp():
                    signals.append(ActivitySignal(
                        source=ActivitySource.INBOX_PROCESSING,
                        timestamp=mtime,
                        confidence=ActivitySource.INBOX_PROCESSING.base_confidence,
                        metadata={"file": latest.name},
                        agent_id=agent_id
                    ))
        except Exception as e:
            logger.debug(f"Error checking inbox processing: {e}")
        
        return signals
    
    def _filter_noise(self, signals: List[ActivitySignal]) -> List[ActivitySignal]:
        """Filter out noise signals (resume prompts, acknowledgments)."""
        filtered = []
        
        for signal in signals:
            metadata_str = json.dumps(signal.metadata).lower()
            # Skip if contains noise patterns
            if any(noise in metadata_str for noise in self.noise_patterns):
                continue
            filtered.append(signal)
        
        return filtered
    
    def _calculate_confidence(
        self,
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
    
    def _validate_signals(
        self,
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


__all__ = ["HardenedActivityDetector", "ActivityAssessment", "ActivityConfidence"]

