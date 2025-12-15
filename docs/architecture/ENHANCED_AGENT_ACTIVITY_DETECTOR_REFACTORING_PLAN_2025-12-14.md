# enhanced_agent_activity_detector.py Refactoring Plan

**Date:** 2025-12-14  
**Author:** Agent-2 (Architecture & Design Specialist)  
**File:** `src/orchestrators/overnight/enhanced_agent_activity_detector.py`  
**Current Size:** 1,367 lines  
**Target:** ~100-150 line backward-compatibility shim + modular files (<300 lines each)  
**Priority:** HIGH (Critical Violation)  
**Status:** ⏳ PLANNING

---

## 📋 Executive Summary

This document provides a comprehensive refactoring plan for `enhanced_agent_activity_detector.py` (1,367 lines), the second-largest Critical violation remaining. The file contains a single class with 30 methods (26 check methods + 4 public methods) that detect agent activity through multiple indicators. The refactoring will split this into modular helper files while maintaining backward compatibility.

**Target:** Eliminate 1 Critical violation (>1000 lines)  
**Approach:** Handler + Helper Module Pattern  
**Pattern:** Activity Detector + Category Helper Modules Pattern  
**Estimated Reduction:** 1,367 lines → ~100 line shim + 6-8 modules (<300 lines each)

---

## 🔍 Current State Analysis

### File Structure:
```
enhanced_agent_activity_detector.py (1,367 lines)
├── EnhancedAgentActivityDetector class
│   ├── __init__() - Initialization
│   ├── detect_agent_activity() - Main public method
│   ├── get_all_agents_activity() - Public method
│   ├── get_stale_agents() - Public method
│   └── 26 _check_* methods (private check methods):
│       ├── File-based checks (10 methods)
│       │   ├── _check_status_json
│       │   ├── _check_inbox_files
│       │   ├── _check_devlogs
│       │   ├── _check_reports
│       │   ├── _check_workspace_files
│       │   ├── _check_passdown_json
│       │   ├── _check_artifacts_directory
│       │   ├── _check_cycle_planner
│       │   ├── _check_notes_directory
│       │   └── _check_inbox_processing
│       ├── System checks (8 methods)
│       │   ├── _check_message_queue
│       │   ├── _check_git_commits
│       │   ├── _check_git_working_directory
│       │   ├── _check_tool_execution
│       │   ├── _check_terminal_activity
│       │   ├── _check_log_file_activity
│       │   ├── _check_process_activity
│       │   └── _check_ide_activity
│       ├── Integration checks (5 methods)
│       │   ├── _check_discord_posts
│       │   ├── _check_swarm_brain
│       │   ├── _check_agent_lifecycle
│       │   ├── _check_activity_emitter_events
│       │   └── _check_contract_activity
│       └── Other checks (3 methods)
│           ├── _check_test_execution
│           ├── _check_activity_logs
│           └── _check_database_activity
```

### Dependencies:
- **Imported by:**
  - `src/orchestrators/overnight/recovery.py`
  - `src/orchestrators/overnight/monitor_state.py`
  - `src/core/agent_self_healing_system.py`
  - `src/orchestrators/overnight/__init__.py`
- **Imports:**
  - `from src.core.config.timeout_constants import TimeoutConstants`
  - Standard library (json, time, datetime, pathlib, logging, typing)

### Content Breakdown:
- **Class**: 1 class (EnhancedAgentActivityDetector)
- **Public Methods**: 4 methods (~150 lines)
- **Check Methods**: 26 methods (~1,200 lines)
- **Total**: 1,367 lines (exceeds V2 limit by 1,067 lines)

---

## 🎯 Target Architecture

### Proposed Structure:
```
src/orchestrators/overnight/activity_detection/
├── __init__.py (~50 lines) - Exports main class
├── detector.py (~150 lines) - EnhancedAgentActivityDetector class (main handler)
├── file_checks.py (~250 lines) - File-based activity checks
├── system_checks.py (~280 lines) - System-level activity checks
├── integration_checks.py (~220 lines) - Integration/service checks
├── execution_checks.py (~200 lines) - Execution/test/activity checks
└── helpers.py (~100 lines) - Shared helper functions
```

### Backward Compatibility:
- `src/orchestrators/overnight/enhanced_agent_activity_detector.py` becomes ~100 line shim
- Re-exports EnhancedAgentActivityDetector class
- Maintains exact import paths for existing code

---

## 📐 Refactoring Strategy

### Pattern: Handler + Helper Module Pattern

**Principle:** Extract check methods into category-based helper modules while maintaining main handler class with public API.

**Benefits:**
- Clear separation by activity source category
- Each module <300 lines (V2 compliant)
- Main handler class stays focused on orchestration
- Helper modules can be tested independently
- Backward compatible (no breaking changes)

### Phase Breakdown:

#### Phase 1: Extract File Checks Helper
- **Target:** `src/orchestrators/overnight/activity_detection/file_checks.py`
- **Content:** 10 file-based check methods
- **Size:** ~250 lines
- **Methods:**
  - `_check_status_json`
  - `_check_inbox_files`
  - `_check_devlogs`
  - `_check_reports`
  - `_check_workspace_files`
  - `_check_passdown_json`
  - `_check_artifacts_directory`
  - `_check_cycle_planner`
  - `_check_notes_directory`
  - `_check_inbox_processing`

#### Phase 2: Extract System Checks Helper
- **Target:** `src/orchestrators/overnight/activity_detection/system_checks.py`
- **Content:** 8 system-level check methods
- **Size:** ~280 lines
- **Methods:**
  - `_check_message_queue`
  - `_check_git_commits`
  - `_check_git_working_directory`
  - `_check_tool_execution`
  - `_check_terminal_activity`
  - `_check_log_file_activity`
  - `_check_process_activity`
  - `_check_ide_activity`

#### Phase 3: Extract Integration Checks Helper
- **Target:** `src/orchestrators/overnight/activity_detection/integration_checks.py`
- **Content:** 5 integration/service check methods
- **Size:** ~220 lines
- **Methods:**
  - `_check_discord_posts`
  - `_check_swarm_brain`
  - `_check_agent_lifecycle`
  - `_check_activity_emitter_events`
  - `_check_contract_activity`

#### Phase 4: Extract Execution Checks Helper
- **Target:** `src/orchestrators/overnight/activity_detection/execution_checks.py`
- **Content:** 3 execution/test/activity check methods
- **Size:** ~200 lines
- **Methods:**
  - `_check_test_execution`
  - `_check_activity_logs`
  - `_check_database_activity`

#### Phase 5: Extract Shared Helpers
- **Target:** `src/orchestrators/overnight/activity_detection/helpers.py`
- **Content:** Shared utility functions (if any)
- **Size:** ~100 lines
- **Functions:** Common helper functions used across check modules

#### Phase 6: Refactor Main Handler Class
- **Target:** `src/orchestrators/overnight/activity_detection/detector.py`
- **Content:** EnhancedAgentActivityDetector class with public methods
- **Size:** ~150 lines
- **Methods:**
  - `__init__` (with helper module initialization)
  - `detect_agent_activity` (orchestrates helper checks)
  - `get_all_agents_activity`
  - `get_stale_agents`

#### Phase 7: Create Backward Compatibility Shim
- **Target:** `src/orchestrators/overnight/enhanced_agent_activity_detector.py` (replacement)
- **Content:** Imports and re-exports EnhancedAgentActivityDetector
- **Size:** ~100 lines
- **Exports:** EnhancedAgentActivityDetector class

---

## 🔧 Implementation Details

### Module Structure:

#### file_checks.py:
```python
"""File-based activity detection helpers."""
from pathlib import Path
from typing import Dict, Any, Optional
import time
import json

def check_status_json(agent_id: str, workspace_root: Path) -> Optional[Dict[str, Any]]:
    """Check status.json modification."""
    # ... implementation

# ... other file check functions
```

#### detector.py:
```python
"""Enhanced Agent Activity Detector - Main Handler."""
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
from .file_checks import (
    check_status_json,
    check_inbox_files,
    # ... other file checks
)
from .system_checks import (
    check_message_queue,
    check_git_commits,
    # ... other system checks
)
from .integration_checks import (
    check_discord_posts,
    check_swarm_brain,
    # ... other integration checks
)
from .execution_checks import (
    check_test_execution,
    check_activity_logs,
    check_database_activity,
)

class EnhancedAgentActivityDetector:
    """Detects agent activity through multiple indicators."""
    
    def __init__(self, workspace_root: Optional[Path] = None):
        """Initialize activity detector."""
        self.workspace_root = workspace_root or Path(".")
        self.agent_workspaces = self.workspace_root / "agent_workspaces"
        self.devlogs_dir = self.workspace_root / "devlogs"
    
    def detect_agent_activity(self, agent_id: str) -> Dict[str, Any]:
        """Detect all activity indicators for an agent."""
        activities = []
        activity_details = {}
        
        # File-based checks
        status_activity = check_status_json(agent_id, self.workspace_root)
        if status_activity:
            activities.append(status_activity)
            activity_details["status_json"] = status_activity
        
        # ... orchestrate all checks
        
        # ... return aggregated results
    
    # ... other public methods
```

#### enhanced_agent_activity_detector.py (shim):
```python
"""Enhanced Agent Activity Detector - Backward Compatibility Shim."""
from __future__ import annotations

# Re-export from modular implementation
from .activity_detection.detector import EnhancedAgentActivityDetector

__all__ = ["EnhancedAgentActivityDetector"]
```

---

## 📊 Expected Results

### File Size Reduction:
- **Before:** 1,367 lines (1 file)
- **After:** ~100 line shim + 7 modular files (<300 lines each)
- **Reduction:** 93% reduction in main file size
- **Compliance:** 100% V2 compliant (all files <300 lines)

### Module Breakdown:
```
enhanced_agent_activity_detector.py: ~100 lines (shim) ✅
activity_detection/
├── __init__.py: ~50 lines ✅
├── detector.py: ~150 lines ✅
├── file_checks.py: ~250 lines ✅
├── system_checks.py: ~280 lines ✅
├── integration_checks.py: ~220 lines ✅
├── execution_checks.py: ~200 lines ✅
└── helpers.py: ~100 lines ✅
```

### Compliance Impact:
- **Before:** 1 Critical violation (>1000 lines)
- **After:** 0 violations (all files <300 lines)
- **Compliance Improvement:** 87.8% → 87.9% (1 violation eliminated)

---

## ⚠️ Risk Assessment

### Identified Risks:

1. **Import Path Changes**
   - **Risk:** Breaking changes to imports
   - **Mitigation:** Backward-compatibility shim maintains exact import paths
   - **Severity:** LOW (shim prevents breaking changes)

2. **Method Signature Changes**
   - **Risk:** Helper functions may need different signatures than methods
   - **Mitigation:** Convert methods to functions with workspace_root parameter
   - **Severity:** LOW (signatures can be adapted)

3. **State Management**
   - **Risk:** Class instance state (workspace_root, agent_workspaces) needs to be passed
   - **Mitigation:** Pass workspace_root as parameter to helper functions
   - **Severity:** LOW (simple parameter passing)

4. **Testing Requirements**
   - **Risk:** Integration tests may need updates
   - **Mitigation:** Maintain same public API, tests should still work
   - **Severity:** MEDIUM (requires verification)

### Dependency Risks:
- ✅ **Breaking Changes:** None (shim maintains API)
- ✅ **Import Paths:** Backward compatible via shim
- ✅ **Public API:** EnhancedAgentActivityDetector class preserved

---

## ✅ Success Criteria

### Completion Criteria:
- [ ] All helper modules created and V2 compliant (<300 lines each)
- [ ] Main detector class refactored (~150 lines)
- [ ] Backward-compatibility shim created (~100 lines)
- [ ] All imports work (recovery.py, monitor_state.py, agent_self_healing_system.py)
- [ ] EnhancedAgentActivityDetector class accessible via original import path
- [ ] All check methods extracted to helpers
- [ ] Public methods work correctly
- [ ] No breaking changes to dependent code
- [ ] V2 compliance verified (0 violations)

### Testing Requirements:
- [ ] Import tests pass
- [ ] Activity detection tests pass
- [ ] Helper function tests pass
- [ ] Integration tests pass

---

## 📅 Implementation Timeline

### Estimated Effort: 3-4 cycles

**Phase 1-2** (Cycle 1): Extract file and system check helpers  
**Phase 3-4** (Cycle 2): Extract integration and execution check helpers  
**Phase 5-6** (Cycle 3): Extract shared helpers and refactor main class  
**Phase 7** (Cycle 4): Create shim and integration testing

---

## 🔗 Related Documents

- V2 Compliance Dashboard: `docs/v2_compliance/V2_COMPLIANCE_DASHBOARD.md`
- Comprehensive Violation Report: `docs/v2_compliance/COMPREHENSIVE_V2_VIOLATION_REPORT_2025-12-14.md`
- Architecture Patterns: Handler + Helper pattern (proven in Batch 2 Phase 2D)

---

## 📝 Notes

- This detector is used by recovery.py, monitor_state.py, and agent_self_healing_system.py
- The 26 check methods can be logically grouped by activity source category
- Helper functions will need workspace_root passed as parameter (instead of self.workspace_root)
- Main class becomes orchestrator that calls helper functions

---

**Architecture Plan:** Agent-2  
**Status:** ✅ **READY FOR EXECUTION**  
**Date:** 2025-12-14

---

**WE. ARE. SWARM!** 🐝⚡
