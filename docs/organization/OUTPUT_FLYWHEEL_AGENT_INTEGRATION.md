# Output Flywheel Agent Integration Guide

**Version**: 1.0  
**Status**: Production-Ready  
**Last Updated**: 2025-12-02  
**Author**: Agent-1 (Integration & Core Systems Specialist)

---

## 🎯 Overview

The Output Flywheel automatically transforms agent work sessions into public, monetizable artifacts (READMEs, blog posts, social-ready content, trading journals). This guide explains how agents should integrate the Output Flywheel into their workflows.

---

## 📋 Quick Start

### **Basic Integration Pattern**

At the end of each work session, agents should:

1. **Assemble session data** into `work_session.json` format
2. **Call the pipeline** via `tools/run_output_flywheel.py`
3. **Verify artifacts** were generated
4. **Update status** with artifact paths

### **Example Integration**

```python
from pathlib import Path
import json
from datetime import datetime
import subprocess

def end_of_session_integration(agent_id: str, session_type: str, metadata: dict, source_data: dict):
    """Integrate Output Flywheel at end of work session."""
    
    # 1. Assemble work_session.json
    session_id = str(uuid.uuid4())  # Generate UUID
    session = {
        "session_id": session_id,
        "session_type": session_type,  # "build", "trade", or "life_aria"
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "agent_id": agent_id,
        "metadata": metadata,
        "source_data": source_data,
        "artifacts": {},
        "pipeline_status": {
            "build_artifact": "pending" if session_type == "build" else "not_applicable",
            "trade_artifact": "pending" if session_type == "trade" else "not_applicable",
            "life_aria_artifact": "pending" if session_type == "life_aria" else "not_applicable"
        }
    }
    
    # 2. Save session file
    sessions_dir = Path("systems/output_flywheel/outputs/sessions")
    sessions_dir.mkdir(parents=True, exist_ok=True)
    session_file = sessions_dir / f"{session_id}_{session_type}.json"
    session_file.write_text(json.dumps(session, indent=2))
    
    # 3. Run pipeline
    result = subprocess.run(
        ["python", "tools/run_output_flywheel.py", "--session-file", str(session_file)],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print(f"✅ Output Flywheel pipeline completed for {session_type} session")
        # 4. Load updated session to get artifact paths
        updated_session = json.loads(session_file.read_text())
        return updated_session.get("artifacts", {})
    else:
        print(f"❌ Pipeline failed: {result.stderr}")
        return None
```

---

## 🔧 Pipeline Types & Triggers

### **1. Build → Artifact Pipeline**

**When to Trigger**:
- New repository created
- Substantial changes (>10 files changed)
- Major feature commits
- End of development session with meaningful code changes

**Required Session Data**:
```json
{
  "session_type": "build",
  "metadata": {
    "duration_minutes": 60,
    "files_changed": 15,
    "commits": 3,
    "lines_added": 200,
    "lines_removed": 50
  },
  "source_data": {
    "repo_path": "D:/Agent_Cellphone_V2_Repository",
    "git_commits": [
      {
        "hash": "abc123",
        "message": "Add feature X",
        "author": "Agent-1",
        "timestamp": "2025-12-02T03:00:00Z",
        "files": ["src/feature.py", "tests/test_feature.py"]
      }
    ]
  }
}
```

**Generated Artifacts**:
- `README.generated.md` - Updated repository README
- `build_log_{session_id}.md` - Build session log
- `social/social_post_{session_id}.md` - Social media post

---

### **2. Trade → Artifact Pipeline**

**When to Trigger**:
- Trading session with ≥1 executed trade
- End of trading day
- Significant trading activity

**Required Session Data**:
```json
{
  "session_type": "trade",
  "metadata": {
    "duration_minutes": 45,
    "trades_executed": 3,
    "total_pnl": 125.50,
    "win_rate": 66.67
  },
  "source_data": {
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
    "market_conditions": {
      "volatility": "moderate",
      "trend": "bullish",
      "volume": "high"
    }
  }
}
```

**Generated Artifacts**:
- `trade_journal_{session_id}.md` - Daily trading journal
- `trade_social_{session_id}.md` - Social trade summary

---

### **3. Life/Aria → Artifact Pipeline**

**When to Trigger**:
- New game/website built with Aria
- Significant Aria session
- Life session with meaningful content

**Required Session Data**:
```json
{
  "session_type": "life_aria",
  "metadata": {
    "duration_minutes": 90,
    "artifacts_created": 2
  },
  "source_data": {
    "conversations": [
      {
        "source": "aria",
        "content": "Built a new game...",
        "timestamp": "2025-12-02T03:00:00Z"
      }
    ]
  }
}
```

**Generated Artifacts**:
- `devlog_entry_{session_id}.md` - Devlog entry
- `screenshot_gallery_notes_{session_id}.md` - Screenshot notes
- `social_post_{session_id}.md` - Social post

---

## 📝 Work Session JSON Schema

### **Required Fields**

```json
{
  "session_id": "uuid-v4-string",
  "session_type": "build" | "trade" | "life_aria",
  "timestamp": "ISO-8601-datetime",
  "agent_id": "Agent-X",
  "metadata": {},
  "source_data": {},
  "artifacts": {},
  "pipeline_status": {}
}
```

### **Field Descriptions**

- **session_id**: UUID v4 format (e.g., `00000000-0000-0000-0000-000000000001`)
- **session_type**: One of `"build"`, `"trade"`, or `"life_aria"`
- **timestamp**: ISO 8601 format with Z suffix (e.g., `2025-12-02T03:00:00Z`)
- **agent_id**: Agent identifier (e.g., `"Agent-1"`)
- **metadata**: Session metadata (duration, metrics, etc.)
- **source_data**: Source data for artifact generation (commits, trades, conversations)
- **artifacts**: Artifact tracking (populated by pipeline)
- **pipeline_status**: Pipeline execution status (populated by pipeline)

**Full Schema**: `systems/output_flywheel/schemas/work_session.json`

---

## 🚀 CLI Usage

### **Basic Command**

```bash
python tools/run_output_flywheel.py --session-file systems/output_flywheel/outputs/sessions/{session_id}_{type}.json
```

### **Command Options**

```bash
# Run build pipeline
python tools/run_output_flywheel.py --session-file sessions/example_build_session.json

# Run trade pipeline
python tools/run_output_flywheel.py --session-file sessions/example_trade_session.json

# Run life_aria pipeline
python tools/run_output_flywheel.py --session-file sessions/example_life_aria_session.json
```

---

## 📊 Artifact Output Locations

### **Build Artifacts**
- `systems/output_flywheel/outputs/artifacts/build/{repo_name}/README.generated.md`
- `systems/output_flywheel/outputs/artifacts/build/{repo_name}/build_log_{session_id}.md`
- `systems/output_flywheel/outputs/artifacts/build/{repo_name}/social/social_post_{session_id}.md`

### **Trade Artifacts**
- `systems/output_flywheel/outputs/artifacts/trade/trade_journal_{session_id}.md`
- `systems/output_flywheel/outputs/artifacts/trade/trade_social_{session_id}.md`

### **Life/Aria Artifacts**
- `systems/output_flywheel/outputs/artifacts/life_aria/devlog_entry_{session_id}.md`
- `systems/output_flywheel/outputs/artifacts/life_aria/screenshot_gallery_notes_{session_id}.md`
- `systems/output_flywheel/outputs/artifacts/life_aria/social_post_{session_id}.md`

### **Updated Sessions**
- `systems/output_flywheel/outputs/sessions/{session_id}_{type}.json`

---

## ✅ Integration Checklist

### **Pre-Integration**
- [ ] Understand which pipeline type(s) your agent will use
- [ ] Review work session JSON schema
- [ ] Identify where to call pipeline (end-of-session hook)

### **Integration Steps**
- [ ] Assemble session metadata during work
- [ ] Collect source data (commits, trades, conversations)
- [ ] Generate UUID for session_id
- [ ] Create work_session.json file
- [ ] Call `run_output_flywheel.py` with session file
- [ ] Verify artifacts generated
- [ ] Update status.json with artifact paths

### **Post-Integration**
- [ ] Test with sample session data
- [ ] Verify artifacts are generated correctly
- [ ] Check artifact quality (formatting, content)
- [ ] Monitor pipeline execution time
- [ ] Document any custom integration patterns

---

## 🔍 Error Handling

### **Common Errors**

1. **Missing Session File**
   - Error: `Session file not found`
   - Fix: Verify session file path is correct

2. **Invalid Session JSON**
   - Error: `Invalid session data`
   - Fix: Validate against schema at `systems/output_flywheel/schemas/work_session.json`

3. **Missing Template**
   - Error: `Template not found`
   - Fix: Verify templates exist in `systems/output_flywheel/templates/`

4. **Jinja2 Not Installed**
   - Error: `jinja2 is required`
   - Fix: `pip install jinja2`

### **Error Recovery**

```python
try:
    result = subprocess.run(
        ["python", "tools/run_output_flywheel.py", "--session-file", str(session_file)],
        capture_output=True,
        text=True,
        timeout=300  # 5 minute timeout
    )
    if result.returncode != 0:
        logger.error(f"Pipeline failed: {result.stderr}")
        # Log error but don't crash agent session
except subprocess.TimeoutExpired:
    logger.error("Pipeline timed out after 5 minutes")
except Exception as e:
    logger.error(f"Pipeline execution error: {e}")
```

---

## 📚 References

- **Architecture**: `systems/output_flywheel/ARCHITECTURE.md`
- **Schema**: `systems/output_flywheel/schemas/work_session.json`
- **CLI Tool**: `tools/run_output_flywheel.py`
- **Templates**: `systems/output_flywheel/templates/`
- **E2E Reports**: `agent_workspaces/Agent-1/OUTPUT_FLYWHEEL_E2E_*.md`

---

## 🎯 Best Practices

1. **Call at End of Session**: Always call pipeline after work is complete, not during
2. **Validate Session Data**: Ensure all required fields are present before calling pipeline
3. **Handle Errors Gracefully**: Don't crash agent session if pipeline fails
4. **Monitor Artifact Quality**: Review generated artifacts periodically
5. **Update Status**: Always update `status.json` with artifact paths after generation
6. **Use UUIDs**: Always generate proper UUID v4 for session_id
7. **ISO Timestamps**: Use ISO 8601 format with Z suffix for timestamps

---

**Generated by**: Agent-1 (Integration & Core Systems Specialist)  
**Date**: 2025-12-02  
**Status**: Production-Ready ✅

🐝 **WE. ARE. SWARM. ⚡🔥**

