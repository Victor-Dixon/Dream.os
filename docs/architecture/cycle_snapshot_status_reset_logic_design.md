=======
<!-- SSOT Domain: architecture -->

>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
# Cycle Snapshot System - Status Reset Logic Design

**Date:** 2025-12-31  
**Designed By:** Agent-2 (Architecture & Design Specialist)  
**Coordinated With:** Agent-3 (Infrastructure & DevOps Specialist)  
**Status:** Design Phase - Ready for Implementation Review

---

## 🎯 Purpose

**CRITICAL SAFETY COMPONENT:** Design the status.json reset logic that will safely reset agent status files after snapshot generation.

**Safety Requirements:**
- ✅ Atomic operations (backup → reset → validate)
- ✅ Reversible (backup system for rollback)
- ✅ Selective (smart reset - keep active, archive completed)
- ✅ Validated (JSON integrity before/after)
- ✅ Error-handled (isolate failures, continue with others)

---

## 🔐 Reset Strategy: Smart Reset (Option B)

**Decision:** Smart Reset - Archive completed items, keep active items

**Rationale:**
- Preserves active work context (agents don't lose in-progress tasks)
- Archives completed work (clean slate for completed items)
- Maintains mission context (ongoing missions continue)
- Prevents confusion (completed items don't clutter status)

---

## 📋 Reset Logic Specification

### What Gets Reset vs. What Gets Kept

#### RESET (Clear/Archive to Snapshot):
- `completed_tasks` → Archive to snapshot, clear array
- `achievements` → Archive to snapshot, clear array
- `current_tasks` → Filter: completed ones → archive, active ones → keep
- `next_actions` → Filter: completed ones → archive, pending ones → keep
- `coordination_status` → If status is "COMPLETE", archive and clear
- `recent_commit` → Clear (null)
- `recent_artifact` → Clear (null)

#### KEEP (Ongoing Context):
- `agent_id` → Identity, never changes
- `agent_name` → Identity, never changes
- `status` → Current operational state
- `fsm_state` → Current finite state machine state
- `current_phase` → Current work phase
- `current_mission` → Ongoing mission context
- `mission_priority` → Mission priority level
- `mission_description` → Mission description
- `cycle_count` → Increment by 1

#### UPDATE:
- `last_updated` → Set to snapshot timestamp

---

## 🔧 Implementation Design

### Module: `processors/status_resetter.py`

**File Structure:**
```python
"""
Status Resetter Module
=====================

Safely resets agent status.json files after snapshot generation.

Protocol: CYCLE_SNAPSHOT_SYSTEM v1.0
Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-12-31
V2 Compliant: Yes

<!-- SSOT Domain: tools -->
"""

from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import json
import shutil
import logging

logger = logging.getLogger(__name__)


class StatusBackupManager:
    """Manages status.json backups before reset."""
    
    def __init__(self, workspace_root: Path):
        self.backup_dir = workspace_root / "reports" / "cycle_snapshots" / "backups"
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.retention_days = 30
    
    def backup_status(self, agent_id: str, status_file: Path) -> Path:
        """Create backup of status.json before reset."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = self.backup_dir / f"{agent_id}_status_{timestamp}.json"
        shutil.copy(status_file, backup_file)
        logger.info(f"Backed up {agent_id} status to {backup_file}")
        return backup_file
    
    def cleanup_old_backups(self):
        """Remove backups older than retention period."""
        from datetime import timedelta
        cutoff = datetime.now() - timedelta(days=self.retention_days)
        removed = 0
        for backup_file in self.backup_dir.glob("*.json"):
            if datetime.fromtimestamp(backup_file.stat().st_mtime) < cutoff:
                backup_file.unlink()
                removed += 1
        if removed > 0:
            logger.info(f"Cleaned up {removed} old backups")


class StatusValidator:
    """Validates status.json structure and content."""
    
    @staticmethod
    def validate_status_json(status: Dict) -> Tuple[bool, List[str]]:
        """Validate status.json structure and content."""
        errors = []
        
        # Required fields
        required = ["agent_id", "agent_name", "status"]
        for field in required:
            if field not in status:
                errors.append(f"Missing required field: {field}")
        
        # Validate JSON structure
        try:
            json.dumps(status)  # Ensure serializable
        except Exception as e:
            errors.append(f"Invalid JSON structure: {e}")
        
        # Validate field types
        if "agent_id" in status and not isinstance(status["agent_id"], str):
            errors.append("agent_id must be string")
        
        if "cycle_count" in status and not isinstance(status["cycle_count"], int):
            errors.append("cycle_count must be integer")
        
        return len(errors) == 0, errors


def filter_completed_items(items: List[str]) -> Tuple[List[str], List[str]]:
    """
    Filter items into completed and active.
    
    Completed markers: ✅, 🟡 (blocked), ⏳ (waiting)
    Active markers: None (no marker), or explicit active markers
    
    Returns:
        (completed_items, active_items)
    """
    completed = []
    active = []
    
    for item in items:
        if isinstance(item, str):
            # Check for completion markers
            if item.startswith("✅") or item.startswith("🟡") or item.startswith("⏳"):
                completed.append(item)
            else:
                active.append(item)
        else:
            # Non-string items are kept as active
            active.append(item)
    
    return completed, active


def filter_completed_coordinations(coordination_status: Dict) -> Tuple[Dict, Dict]:
    """
    Filter coordination status into completed and active.
    
    Completed: status is "COMPLETE" or "BLOCKED"
    Active: status is "IN_PROGRESS" or other active states
    """
    completed = {}
    active = {}
    
    for key, value in coordination_status.items():
        if isinstance(value, dict):
            status = value.get("status", "").upper()
            if status in ["COMPLETE", "BLOCKED"]:
                completed[key] = value
            else:
                active[key] = value
        else:
            # Non-dict values are kept as active
            active[key] = value
    
    return completed, active


def generate_reset_status(
    current_status: Dict,
    snapshot_timestamp: datetime,
    archived_data: Dict
) -> Dict:
    """
    Generate reset status.json from current status.
    
    Args:
        current_status: Current status.json content
        snapshot_timestamp: Timestamp of snapshot
        archived_data: Data archived to snapshot
    
    Returns:
        Reset status.json content
    """
    # Extract completed and active items
    completed_tasks, active_tasks = filter_completed_items(
        current_status.get("current_tasks", [])
    )
    completed_actions, active_actions = filter_completed_items(
        current_status.get("next_actions", [])
    )
    completed_coordinations, active_coordinations = filter_completed_coordinations(
        current_status.get("coordination_status", {})
    )
    
    # Build reset status
    reset_status = {
        # Identity (keep)
        "agent_id": current_status["agent_id"],
        "agent_name": current_status["agent_name"],
        
        # State (keep)
        "status": current_status.get("status", "ACTIVE_AGENT_MODE"),
        "fsm_state": current_status.get("fsm_state", "ACTIVE"),
        "current_phase": current_status.get("current_phase", "TASK_EXECUTION"),
        
        # Mission (keep)
        "current_mission": current_status.get("current_mission", ""),
        "mission_priority": current_status.get("mission_priority", "NORMAL"),
        "mission_description": current_status.get("mission_description", ""),
        
        # Cycle tracking (update)
        "cycle_count": current_status.get("cycle_count", 0) + 1,
        "last_updated": snapshot_timestamp.isoformat(),
        
        # Active work (keep active, clear completed)
        "current_tasks": active_tasks,
        "next_actions": active_actions,
        
        # Completed work (clear - archived to snapshot)
        "completed_tasks": [],
        "achievements": [],
        
        # Coordination (reset if completed)
        "coordination_status": active_coordinations,
        
        # Recent activity (clear)
        "recent_commit": None,
        "recent_artifact": None
    }
    
    # Preserve any additional fields (future-proofing)
    known_fields = {
        "agent_id", "agent_name", "status", "fsm_state", "current_phase",
        "current_mission", "mission_priority", "mission_description",
        "cycle_count", "last_updated", "current_tasks", "next_actions",
        "completed_tasks", "achievements", "coordination_status",
        "recent_commit", "recent_artifact"
    }
    
    for key, value in current_status.items():
        if key not in known_fields:
            # Preserve unknown fields
            reset_status[key] = value
    
    return reset_status


def reset_agent_status_safely(
    agent_id: str,
    snapshot_data: Dict,
    workspace_root: Path,
    snapshot_timestamp: datetime
) -> Tuple[bool, Optional[str]]:
    """
    Safely reset agent status.json with full error handling.
    
    Safety Measures:
    1. Create backup before reset
    2. Validate JSON before and after
    3. Atomic write (write to temp, then rename)
    4. Rollback on failure
    5. Log all operations
    
    Args:
        agent_id: Agent ID to reset
        snapshot_data: Snapshot data (for archiving)
        workspace_root: Root workspace path
        snapshot_timestamp: Timestamp of snapshot
    
    Returns:
        (success: bool, error_message: Optional[str])
    """
    status_file = workspace_root / "agent_workspaces" / agent_id / "status.json"
    
    if not status_file.exists():
        return False, f"Status file not found: {status_file}"
    
    backup_manager = StatusBackupManager(workspace_root)
    validator = StatusValidator()
    
    try:
        # 1. Backup
        backup_file = backup_manager.backup_status(agent_id, status_file)
        
        # 2. Read and validate current status
        with open(status_file, 'r', encoding='utf-8') as f:
            current_status = json.load(f)
        
        is_valid, errors = validator.validate_status_json(current_status)
        if not is_valid:
            return False, f"Invalid current status: {', '.join(errors)}"
        
        # 3. Extract archived data
        archived_data = {
            "completed_tasks": current_status.get("completed_tasks", []),
            "achievements": current_status.get("achievements", []),
            "completed_current_tasks": filter_completed_items(
                current_status.get("current_tasks", [])
            )[0],
            "completed_next_actions": filter_completed_items(
                current_status.get("next_actions", [])
            )[0],
            "completed_coordinations": filter_completed_coordinations(
                current_status.get("coordination_status", {})
            )[0],
            "recent_commit": current_status.get("recent_commit"),
            "recent_artifact": current_status.get("recent_artifact")
        }
        
        # 4. Generate reset status
        reset_status = generate_reset_status(
            current_status,
            snapshot_timestamp,
            archived_data
        )
        
        # 5. Validate reset status
        is_valid, errors = validator.validate_status_json(reset_status)
        if not is_valid:
            return False, f"Invalid reset status: {', '.join(errors)}"
        
        # 6. Atomic write
        temp_file = status_file.with_suffix('.json.tmp')
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(reset_status, f, indent=2, ensure_ascii=False)
        
        # Atomic rename (cross-platform)
        if temp_file.exists():
            if status_file.exists():
                status_file.unlink()
            temp_file.rename(status_file)
        
        # 7. Validate final state
        with open(status_file, 'r', encoding='utf-8') as f:
            final_status = json.load(f)
        
        is_valid, errors = validator.validate_status_json(final_status)
        if not is_valid:
            # Rollback
            shutil.copy(backup_file, status_file)
            return False, f"Final validation failed: {', '.join(errors)}"
        
        # 8. Archive to snapshot
        if agent_id not in snapshot_data.get("agent_accomplishments", {}):
            snapshot_data["agent_accomplishments"][agent_id] = {}
        
        snapshot_data["agent_accomplishments"][agent_id].update(archived_data)
        
        logger.info(f"Successfully reset {agent_id} status")
        return True, None
        
    except json.JSONDecodeError as e:
        # Rollback on JSON error
        if backup_file.exists():
            shutil.copy(backup_file, status_file)
        return False, f"JSON decode error: {e}"
        
    except Exception as e:
        # Rollback on any other error
        if 'backup_file' in locals() and backup_file.exists():
            shutil.copy(backup_file, status_file)
        logger.error(f"Reset failed for {agent_id}: {e}")
        return False, str(e)


def reset_all_agent_status(
    snapshot_data: Dict,
    workspace_root: Path,
    snapshot_timestamp: datetime,
    agent_ids: Optional[List[str]] = None
) -> Dict[str, Tuple[bool, Optional[str]]]:
    """
    Reset all agent status.json files safely.
    
    Args:
        snapshot_data: Snapshot data (for archiving)
        workspace_root: Root workspace path
        snapshot_timestamp: Timestamp of snapshot
        agent_ids: Optional list of agent IDs (default: all agents)
    
    Returns:
        Dict mapping agent_id -> (success: bool, error_message: Optional[str])
    """
    if agent_ids is None:
        # Default to all agents
        agent_ids = [f"Agent-{i}" for i in range(1, 9)]
    
    results = {}
    
    for agent_id in agent_ids:
        success, error = reset_agent_status_safely(
            agent_id,
            snapshot_data,
            workspace_root,
            snapshot_timestamp
        )
        results[agent_id] = (success, error)
        
        if not success:
            logger.warning(f"Failed to reset {agent_id}: {error}")
    
    return results
```

---

## 🧪 Testing Strategy

### Unit Tests

**Test File:** `tests/unit/test_status_resetter.py`

**Test Cases:**
1. `test_filter_completed_items()` - Test item filtering logic
2. `test_filter_completed_coordinations()` - Test coordination filtering
3. `test_generate_reset_status()` - Test reset status generation
4. `test_reset_agent_status_safely()` - Test full reset flow
5. `test_backup_creation()` - Test backup system
6. `test_rollback_on_failure()` - Test rollback mechanism
7. `test_validation_before_after()` - Test validation
8. `test_atomic_write()` - Test atomic write operations

### Integration Tests

**Test File:** `tests/integration/test_status_reset_integration.py`

**Test Cases:**
1. `test_reset_all_agents()` - Test resetting all agents
2. `test_reset_with_missing_agent()` - Test handling missing agents
3. `test_reset_with_corrupted_status()` - Test handling corrupted files
4. `test_reset_with_concurrent_access()` - Test concurrent access handling

### Manual Testing Checklist

**Before Production:**
- [ ] Test with one agent (Agent-1)
- [ ] Verify backup created
- [ ] Verify status.json reset correctly
- [ ] Verify archived data in snapshot
- [ ] Test rollback mechanism
- [ ] Test with all agents
- [ ] Verify no data loss
- [ ] Verify StatusChangeMonitor still works
- [ ] Verify agents can continue working after reset

---

## 🔒 Safety Checklist

### Pre-Reset
- [ ] Lock file acquired
- [ ] Backup directory exists
- [ ] Status file exists
- [ ] Status file is valid JSON
- [ ] Status file has required fields

### During Reset
- [ ] Backup created successfully
- [ ] Current status validated
- [ ] Reset status generated correctly
- [ ] Reset status validated
- [ ] Atomic write successful
- [ ] Final state validated

### Post-Reset
- [ ] Status file is valid JSON
- [ ] Status file has required fields
- [ ] Archived data in snapshot
- [ ] Backup file exists
- [ ] No data loss
- [ ] Agents can continue working

### Error Handling
- [ ] Rollback on validation failure
- [ ] Rollback on write failure
- [ ] Rollback on JSON error
- [ ] Error isolation (one agent failure doesn't stop others)
- [ ] Error logging

---

## 📊 Reset Status Tracking

### Snapshot Metadata

**Add to snapshot:**
```json
{
  "reset_status": {
    "agents_reset": ["Agent-1", "Agent-2", ...],
    "agents_failed": [],
    "reset_timestamp": "2025-12-31T10:00:05.000000+00:00",
    "reset_errors": [],
    "backup_files": {
      "Agent-1": "path/to/backup/Agent-1_status_20251231_100000.json",
      ...
    }
  }
}
```

---

## 🚀 Implementation Steps

### Step 1: Create Module Structure
1. Create `tools/cycle_snapshots/processors/status_resetter.py`
2. Implement `StatusBackupManager` class
3. Implement `StatusValidator` class
4. Implement helper functions

### Step 2: Implement Core Logic
1. Implement `filter_completed_items()`
2. Implement `filter_completed_coordinations()`
3. Implement `generate_reset_status()`

### Step 3: Implement Safety Logic
1. Implement `reset_agent_status_safely()`
2. Add backup creation
3. Add validation
4. Add atomic write
5. Add rollback

### Step 4: Implement Batch Reset
1. Implement `reset_all_agent_status()`
2. Add error isolation
3. Add result tracking

### Step 5: Testing
1. Write unit tests
2. Write integration tests
3. Manual testing with one agent
4. Manual testing with all agents

### Step 6: Code Review
1. Agent-2 reviews code
2. Agent-4 validates safety
3. Address review feedback

### Step 7: Production Use
1. Test in production with one agent
2. Monitor for issues
3. Test with all agents
4. Full production deployment

---

## 📝 Code Review Checklist

### Agent-2 Review Points

**Architecture:**
- [ ] Modular design (V2 compliant)
- [ ] Clear separation of concerns
- [ ] Proper error handling
- [ ] Type hints throughout

**Safety:**
- [ ] Backup system works correctly
- [ ] Validation is comprehensive
- [ ] Atomic writes are truly atomic
- [ ] Rollback mechanism works
- [ ] Error isolation is effective

**Code Quality:**
- [ ] Functions are <30 lines (where possible)
- [ ] File is <400 lines
- [ ] Proper logging
- [ ] Clear documentation

### Agent-4 Validation Points

**Discord Bot Safety:**
- [ ] StatusChangeMonitor still works after reset
- [ ] No Discord dependencies in core
- [ ] Status updates continue working
- [ ] No performance degradation

**Status.json Integrity:**
- [ ] All required fields present
- [ ] JSON is valid
- [ ] No data loss
- [ ] Agents can continue working

---

## 🔄 Coordination Touchpoints

### Touchpoint 1: Design Review
**When:** Before implementation  
**Who:** Agent-2 + Agent-3  
**Purpose:** Review reset logic design, confirm approach

### Touchpoint 2: Code Review
**When:** After Step 3 (Safety Logic)  
**Who:** Agent-2  
**Purpose:** Review safety implementation

### Touchpoint 3: Safety Validation
**When:** After Step 5 (Testing)  
**Who:** Agent-4  
**Purpose:** Validate Discord bot safety, status.json integrity

### Touchpoint 4: Production Approval
**When:** Before Step 7 (Production Use)  
**Who:** Agent-2 + Agent-4  
**Purpose:** Approve production deployment

---

**Status:** Design Complete - Ready for Agent-3 Implementation Review  
**Next:** Agent-3 reviews design, confirms approach, begins implementation  
**Safety:** All critical safety measures defined and documented

