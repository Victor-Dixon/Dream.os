# Output Flywheel Integration Module

**Version**: 1.0  
**Status**: Production-Ready  
**Last Updated**: 2025-12-02  
**Author**: Agent-1 (Integration & Core Systems Specialist)

---

## 🎯 Overview

This module provides **automatic integration hooks** for agents to seamlessly generate artifacts from work sessions without manual intervention.

---

## 🚀 Quick Start

### **Basic Usage**

```python
from systems.output_flywheel.integration.agent_session_hooks import end_of_session_hook

# At end of work session:
artifacts = end_of_session_hook(
    agent_id="Agent-1",
    session_type="build",  # or "trade" or "life_aria"
    auto_trigger=True
)

if artifacts:
    print(f"✅ Generated artifacts: {artifacts.get('artifacts', {})}")
```

### **With Custom Metadata**

```python
from systems.output_flywheel.integration.agent_session_hooks import end_of_session_hook

artifacts = end_of_session_hook(
    agent_id="Agent-1",
    session_type="build",
    metadata={
        "duration_minutes": 60,
        "files_changed": 15,
        "commits": 3,
    },
    source_data={
        "repo_path": "D:/Agent_Cellphone_V2_Repository",
        "git_commits": [...],  # Optional: auto-collected if not provided
    },
    auto_trigger=True
)
```

---

## 📋 Integration Options

### **1. Manual End-of-Session Hook**

Use when you want explicit control over when artifacts are generated:

```python
from systems.output_flywheel.integration.agent_session_hooks import AgentSessionHook

hook = AgentSessionHook("Agent-1")

# Assemble and save session
session = hook.assemble_work_session(
    session_type="build",
    metadata={"duration_minutes": 45},
)
session_file = hook.save_session(session)

# Trigger pipeline
success = hook.trigger_pipeline(session_file)
```

### **2. Automatic Status.json Integration**

Automatically trigger Output Flywheel when status.json is updated:

```python
from systems.output_flywheel.integration.status_json_integration import auto_trigger_on_status_update

# Call after updating status.json
artifacts = auto_trigger_on_status_update("Agent-1")
```

### **3. Full Integration Class**

For advanced usage with status.json monitoring:

```python
from systems.output_flywheel.integration.status_json_integration import StatusJsonIntegration

integration = StatusJsonIntegration("Agent-1")

# Check status.json and trigger if needed
artifacts = integration.check_and_trigger()

# Update status.json with generated artifacts
if artifacts:
    integration.update_status_with_artifacts(artifacts.get("artifacts", {}))
```

---

## 🔧 Features

### **Automatic Data Collection**

The integration system automatically collects:

- **Git Data** (for build sessions):
  - Recent commits (last 10)
  - Files changed
  - Repository path

- **Session Metadata** (from status.json):
  - Agent name
  - Current mission
  - Completed tasks
  - Achievements
  - Duration (calculated from timestamps)

### **Smart Session Type Detection**

Automatically infers session type from status.json:
- **"trade"**: If mission contains "trade", "trading", "market", "stock"
- **"life_aria"**: If mission contains "aria", "life", "game", "website"
- **"build"**: Default for all other work

### **Automatic Pipeline Triggering**

When `auto_trigger=True`:
1. Assembles `work_session.json`
2. Saves to `systems/output_flywheel/outputs/sessions/`
3. Runs `tools/run_output_flywheel.py`
4. Returns updated session with artifact paths

---

## 📊 Integration Points

### **1. Agent Workflows**

Hook into existing agent completion flows:

```python
# In agent completion workflow
def complete_task(agent_id: str, task_data: dict):
    # ... complete task logic ...
    
    # Trigger Output Flywheel
    from systems.output_flywheel.integration.agent_session_hooks import end_of_session_hook
    artifacts = end_of_session_hook(agent_id, "build", auto_trigger=True)
    
    return artifacts
```

### **2. Status.json Updates**

Automatically trigger on status.json changes:

```python
# After updating status.json
def update_status(agent_id: str, status_updates: dict):
    # ... update status.json ...
    
    # Check and trigger Output Flywheel
    from systems.output_flywheel.integration.status_json_integration import auto_trigger_on_status_update
    artifacts = auto_trigger_on_status_update(agent_id)
    
    return artifacts
```

### **3. Git Tracking**

Automatic git data collection for build sessions:

```python
from systems.output_flywheel.integration.agent_session_hooks import AgentSessionHook

hook = AgentSessionHook("Agent-1")
git_data = hook._collect_git_data()

# git_data contains:
# {
#     "repo_path": "...",
#     "git_commits": [...],
#     "files_changed": [...]
# }
```

### **4. Trading Systems**

For trade sessions, provide trade data:

```python
artifacts = end_of_session_hook(
    agent_id="Agent-1",
    session_type="trade",
    source_data={
        "trades": [
            {
                "symbol": "AAPL",
                "action": "buy",
                "quantity": 10,
                "price": 175.50,
                "timestamp": "2025-12-02T03:15:00Z",
                "profit_loss": 25.00
            }
        ],
        "market_conditions": {...}
    },
    auto_trigger=True
)
```

---

## ✅ Integration Checklist

### **For Agents**

- [ ] Import integration module: `from systems.output_flywheel.integration import end_of_session_hook`
- [ ] Call `end_of_session_hook()` at end of work session
- [ ] Specify correct `session_type` ("build", "trade", or "life_aria")
- [ ] Optionally provide custom `metadata` and `source_data`
- [ ] Handle return value (artifacts dictionary)
- [ ] Update status.json with artifact paths if needed

### **For System Integration**

- [ ] Test with real agent workflow
- [ ] Verify artifacts generated correctly
- [ ] Check publication queue populated
- [ ] Monitor pipeline execution time
- [ ] Handle errors gracefully (don't crash agent session)

---

## 🔍 Error Handling

The integration system handles errors gracefully:

- **Git collection failures**: Falls back to basic repo path
- **Pipeline failures**: Logs error but doesn't crash agent session
- **Status.json errors**: Logs warning and continues
- **Timeout protection**: 5-minute timeout for pipeline execution

All errors are logged but don't interrupt agent workflows.

---

## 📚 API Reference

### **`end_of_session_hook()`**

Convenience function for end-of-session integration.

**Parameters**:
- `agent_id` (str): Agent identifier
- `session_type` (str): "build", "trade", or "life_aria"
- `metadata` (dict, optional): Session metadata
- `source_data` (dict, optional): Source data
- `auto_trigger` (bool): Whether to trigger pipeline (default: True)

**Returns**: Updated session data with artifacts, or None if failed

### **`AgentSessionHook`**

Full-featured session hook class.

**Methods**:
- `assemble_work_session()`: Assemble work_session.json
- `save_session()`: Save session to disk
- `trigger_pipeline()`: Run Output Flywheel pipeline
- `end_of_session()`: Complete workflow (assemble + save + trigger)

### **`StatusJsonIntegration`**

Status.json monitoring and auto-triggering.

**Methods**:
- `check_and_trigger()`: Check status.json and trigger if needed
- `update_status_with_artifacts()`: Update status.json with artifact paths

---

## 🎯 Best Practices

1. **Call at End of Session**: Always call integration hooks after work is complete
2. **Use Auto-Trigger**: Set `auto_trigger=True` for seamless workflow
3. **Handle Errors**: Don't crash agent session if pipeline fails
4. **Update Status**: Update status.json with artifact paths after generation
5. **Monitor Performance**: Track pipeline execution time
6. **Test Integration**: Test with sample sessions before production use

---

## 📖 Examples

See `docs/organization/OUTPUT_FLYWHEEL_AGENT_INTEGRATION.md` for detailed examples and usage patterns.

---

**Generated by**: Agent-1 (Integration & Core Systems Specialist)  
**Date**: 2025-12-02  
**Status**: Production-Ready ✅

🐝 **WE. ARE. SWARM. ⚡🔥**

