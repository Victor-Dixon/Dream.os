# Stall Monitor Enhancement Proposal

**Date**: 2025-12-12  
**Author**: Agent-4 (Captain)  
**Priority**: HIGH  
**Status**: Proposed

## Problem Statement

The stall monitor is currently detecting false positives for inactivity. Recent example:
- **Detected**: 25.2 minutes inactivity for Agent-4
- **Reality**: Agent-4 had just completed:
  - ✅ Created verification report (`docs/captain_reports/cp001_ci_verification_2025-12-12.md`)
  - ✅ Multiple git commits (CP-001 execution)
  - ✅ Status.json updates

**Root Cause**: Missing activity sources in stall detection logic.

## Current Activity Sources (HardenedActivityDetector)

The current `HardenedActivityDetector` checks:
1. ✅ Telemetry events (ActivityEmitter)
2. ✅ Git commits **with agent ID in commit message** (`--grep agent_id`)
3. ✅ Contract system activity
4. ✅ Test execution
5. ✅ Status updates
6. ✅ File modifications in agent workspace
7. ✅ Devlog activity
8. ✅ Inbox processing

## Missing Activity Sources

### 1. Git Commits by File Path (CRITICAL)
**Problem**: Only checks commits with agent ID in message (`--grep agent_id`)

**Example**: 
- Commit: `"docs: Captain CP-001 CI/CD verification execution"`
- Files changed: `docs/captain_reports/cp001_ci_verification_2025-12-12.md`, `agent_workspaces/Agent-4/status.json`
- **Current behavior**: ❌ Not detected (no "Agent-4" in commit message)
- **Expected behavior**: ✅ Detected (modifies Agent-4 files)

**Solution**: Check git commits that modify files in:
- `agent_workspaces/{agent_id}/**`
- `docs/captain_reports/` (for Agent-4/Captain)
- Agent-specific patterns in commit diff

### 2. Captain Reports Directory (HIGH PRIORITY)
**Problem**: Captain validation artifacts not tracked

**Location**: `docs/captain_reports/`

**Examples**:
- `cp001_ci_verification_2025-12-12.md`
- `delta_validation_2025-12-12_19-01.md`
- `progress_validation_2025-12-12_15-15.md`

**Solution**: Add activity source checking `docs/captain_reports/` for:
- File creation/modification timestamps
- Pattern matching for agent-specific reports

### 3. Root-Level Artifacts (MEDIUM PRIORITY)
**Problem**: Some agents create artifacts at repo root, not in workspace

**Location**: `docs/`, root-level validation files

**Solution**: Check for agent-specific patterns in root-level artifact directories

### 4. Git Commit Author/Email Matching (MEDIUM PRIORITY)
**Problem**: Could match commits by git author if agent-specific git configs exist

**Solution**: Check git commit author email/name patterns per agent (if configured)

## Proposed Implementation

### Phase 1: Git Activity Enhancement (IMMEDIATE)

**File**: `src/core/hardened_activity_detector.py`

**Add method**: `_check_git_activity_by_path()`

```python
def _check_git_activity_by_path(
    self,
    agent_id: str,
    lookback_time: datetime
) -> List[ActivitySignal]:
    """Check git commits that modify agent-specific files (Tier 1)."""
    signals = []
    
    try:
        import subprocess
        from src.core.config.timeout_constants import TimeoutConstants
        
        # Agent-specific paths to check
        agent_paths = [
            f"agent_workspaces/{agent_id}/",
            f"docs/captain_reports/" if agent_id == "Agent-4" else None,
        ]
        agent_paths = [p for p in agent_paths if p]
        
        for path_pattern in agent_paths:
            result = subprocess.run(
                ["git", "log", "--since", lookback_time.isoformat(),
                 "--format=%H|%ct|%s", "--name-only", "--", path_pattern],
                capture_output=True,
                text=True,
                timeout=TimeoutConstants.HTTP_QUICK,
                cwd=self.workspace_root,
            )
            
            if result.returncode == 0 and result.stdout.strip():
                # Parse commits
                commits = self._parse_git_log_output(result.stdout)
                for commit in commits:
                    # Filter out resume-related commits
                    if any(noise in commit['message'].lower() 
                           for noise in self.noise_patterns):
                        continue
                    
                    signals.append(ActivitySignal(
                        source=ActivitySource.GIT_COMMIT,
                        timestamp=commit['timestamp'],
                        confidence=ActivitySource.GIT_COMMIT.base_confidence,
                        metadata={
                            "hash": commit['hash'][:8],
                            "message": commit['message'][:100],
                            "files": commit['files']
                        },
                        agent_id=agent_id
                    ))
    except Exception as e:
        logger.debug(f"Error checking git activity by path: {e}")
    
    return signals
```

**Integration**: Call from `assess_agent_activity()`:
```python
signals.extend(self._check_git_activity_by_path(agent_id, lookback_time))
```

### Phase 2: Captain Reports Detection (HIGH PRIORITY)

**Add method**: `_check_captain_reports()`

```python
def _check_captain_reports(
    self,
    agent_id: str,
    lookback_time: datetime
) -> List[ActivitySignal]:
    """Check captain reports directory (Agent-4 only, Tier 1)."""
    signals = []
    
    if agent_id != "Agent-4":
        return signals
    
    captain_reports_dir = self.workspace_root / "docs" / "captain_reports"
    if not captain_reports_dir.exists():
        return signals
    
    try:
        # Check for recent report files
        for report_file in captain_reports_dir.glob("*.md"):
            try:
                mtime = report_file.stat().st_mtime
                mtime_dt = datetime.fromtimestamp(mtime)
                
                if mtime_dt >= lookback_time:
                    signals.append(ActivitySignal(
                        source=ActivitySource.FILE_MODIFICATION,
                        timestamp=mtime,
                        confidence=ActivitySource.FILE_MODIFICATION.base_confidence * 1.2,  # Boost for reports
                        metadata={
                            "file": report_file.name,
                            "type": "captain_report",
                            "path": str(report_file.relative_to(self.workspace_root))
                        },
                        agent_id=agent_id
                    ))
            except (OSError, PermissionError):
                continue
    except Exception as e:
        logger.debug(f"Error checking captain reports: {e}")
    
    return signals
```

**Integration**: Add to `assess_agent_activity()`:
```python
signals.extend(self._check_captain_reports(agent_id, lookback_time))
```

### Phase 3: Enhanced File Modification Detection (MEDIUM PRIORITY)

**Enhance**: `_check_file_modifications()` to also check:
- `docs/captain_reports/` for Agent-4
- Root-level agent-specific artifacts

## Testing Plan

1. **Test Case 1**: Git commit without agent ID in message
   - Create commit modifying `agent_workspaces/Agent-4/status.json`
   - Verify stall monitor detects activity

2. **Test Case 2**: Captain report creation
   - Create report in `docs/captain_reports/`
   - Verify Agent-4 activity detected

3. **Test Case 3**: Multi-file commit
   - Commit with agent workspace files + captain reports
   - Verify activity detected from file paths

## Implementation Priority

1. **IMMEDIATE**: Phase 1 (Git activity by path) - Fixes false positives
2. **HIGH**: Phase 2 (Captain reports) - Critical for Captain validation artifacts
3. **MEDIUM**: Phase 3 (Enhanced file detection) - Additional coverage

## Success Criteria

- ✅ Stall monitor detects git commits modifying agent files (even without agent ID in message)
- ✅ Captain reports trigger activity detection for Agent-4
- ✅ False positive rate reduced (target: <5%)
- ✅ No performance degradation (<100ms per agent check)

## Related Files

- `src/core/hardened_activity_detector.py` - Main implementation
- `src/core/stall_resumer_guard.py` - Uses HardenedActivityDetector
- `tools/agent_activity_detector.py` - Alternative detector (also needs updates)
- `src/orchestrators/overnight/enhanced_agent_activity_detector.py` - Also needs updates

## Notes

- This enhancement aligns with the existing multi-source activity detection architecture
- Maintains backward compatibility with existing activity sources
- Follows V2 compliance (<400 lines per file)
- Should integrate with existing confidence scoring system

---

**Next Steps**:
1. Review and approve proposal
2. Implement Phase 1 (Git activity by path)
3. Test and validate
4. Implement Phase 2 (Captain reports)
5. Monitor for additional missing sources



