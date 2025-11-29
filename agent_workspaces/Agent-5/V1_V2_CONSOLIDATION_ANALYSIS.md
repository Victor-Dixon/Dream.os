# V1→V2 Consolidation Analysis - Agent-5

**Date**: 2025-01-28  
**Status**: IN PROGRESS  
**Priority**: URGENT

## Executive Summary

**V1 Repository**: `D:\Agent_Cellphone`  
**V2 Repository**: `D:\Agent_Cellphone_V2_Repository`

### Inventory Results

**V1 overnight_runner**: 16 Python files  
**V2 orchestrators/overnight**: 20 Python files

## Key Findings

### ✅ Already in V2
- Core orchestrator structure (`orchestrator.py`)
- Monitoring system (`monitor.py`, `monitor_metrics.py`, `monitor_state.py`)
- Recovery system (`recovery.py`, `recovery_handlers.py`, `recovery_escalation.py`)
- Scheduler system (`scheduler.py`, `scheduler_*.py`)

### ❌ Missing from V2 (Need Extraction)

#### 1. FSM Bridge (`fsm_bridge.py`)
- **V1 Location**: `D:\Agent_Cellphone\overnight_runner\fsm_bridge.py`
- **Purpose**: Bridges overnight runner with FSM system
- **Key Functions**:
  - `handle_fsm_request()` - Assigns queued tasks to agents
  - `handle_fsm_update()` - Persists task state updates
  - `process_fsm_update()` - Processes agent FSM updates
  - `seed_fsm_tasks()` - Seeds FSM from TASK_LIST.md files
- **V2 Target**: `src/orchestrators/overnight/fsm_bridge.py`

#### 2. Inbox Consumer (`inbox_consumer.py`)
- **V1 Location**: `D:\Agent_Cellphone\overnight_runner\inbox_consumer.py`
- **Purpose**: Bridges agent responses to FSM system
- **Key Functions**:
  - `to_fsm_event()` - Converts captured responses to FSM events
  - `process_inbox()` - Processes all inbox files
- **V2 Target**: `src/orchestrators/overnight/inbox_consumer.py`

#### 3. Listener (`listener.py`)
- **V1 Location**: `D:\Agent_Cellphone\overnight_runner\listener.py`
- **Purpose**: Monitors agent inboxes and processes responses
- **Key Features**:
  - State management (`state.json`)
  - Discord devlog integration
  - Contract updates
  - TASK_LIST.md patching
- **V2 Target**: `src/orchestrators/overnight/listener.py`

#### 4. Runner (`runner.py`)
- **V1 Location**: `D:\Agent_Cellphone\overnight_runner\runner.py`
- **Purpose**: Master controller for overnight operations
- **Key Features**:
  - Message plan building (contracts, autonomous-dev, etc.)
  - Agent coordination
  - FSM integration
  - Response capture
- **V2 Target**: `src/orchestrators/overnight/runner.py` (or integrate into `orchestrator.py`)

### 📋 FSM_UPDATES Directory
- **V1 Location**: `D:\Agent_Cellphone\FSM_UPDATES/`
- **Contents**: JSON update files from agents
- **V2 Integration**: Process these into FSM system

### 🛠️ Tools & Protocols
- **V1 Location**: `D:\Agent_Cellphone\overnight_runner/tools/` and `protocols/`
- **Contents**: PowerShell scripts, Python tools, protocol documentation
- **V2 Target**: `src/orchestrators/overnight/tools/` and `docs/overnight_protocols/`

## Extraction Plan

### Phase 1: Core Components (IMMEDIATE)
1. ✅ Extract `fsm_bridge.py` → V2 structure
2. ✅ Extract `inbox_consumer.py` → V2 structure
3. ✅ Extract `listener.py` → V2 structure
4. ⏳ Analyze `runner.py` patterns → Integrate into V2 orchestrator

### Phase 2: Integration (TODAY)
1. Integrate FSM_UPDATES processing
2. Extract tools and protocols
3. Update V2 orchestrator with V1 patterns

### Phase 3: Testing & Documentation (TODAY)
1. Test extracted components
2. Create devlog with real progress
3. Update status.json

## Code Patterns to Extract

### FSM Bridge Pattern
```python
# V1 pattern: Direct FSM task management
def handle_fsm_request(payload):
    # Assign queued tasks to agents
    # Write to agent inboxes
    # Update task state
```

### Inbox Consumer Pattern
```python
# V1 pattern: Convert agent responses to FSM events
def to_fsm_event(envelope):
    # Convert response → FSM update format
    # Write to outbox
```

### Listener Pattern
```python
# V1 pattern: Monitor inboxes, update state, trigger actions
def on_message(data):
    # Update state.json
    # Process contracts
    # Patch TASK_LIST.md
    # Devlog to Discord
```

## Next Actions

1. **NOW**: Extract `fsm_bridge.py` to V2
2. **NOW**: Extract `inbox_consumer.py` to V2
3. **NOW**: Extract `listener.py` to V2
4. **TODAY**: Integrate FSM_UPDATES processing
5. **TODAY**: Post devlog with real code changes

---

**Status**: Extraction in progress - Real code being moved NOW

