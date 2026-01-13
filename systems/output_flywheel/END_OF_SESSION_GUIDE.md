# Output Flywheel End-of-Session Guide

**Purpose**: Guide agents on using Output Flywheel at end-of-session  
**Version**: 1.0  
**Author**: Agent-5 (Business Intelligence Specialist)  
**Date**: 2025-12-02

---

## 🎯 Overview

At the end of each work session, agents should:
1. Create a work session artifact documenting their work
2. Track the session in the Output Flywheel system
3. Submit feedback for v1.1 improvements (as needed)

---

## 📋 Step-by-Step Process

### Step 1: Create Work Session JSON

Create a file in `systems/output_flywheel/outputs/sessions/` with format:
- **Filename**: `{agent_id}_{date}_{description}.json`
- **Example**: `agent5_guardrail_implementation_2025-12-02.json`

**Required Fields**:
- `session_id`: Unique identifier (e.g., `a5-2025-12-02-description`)
- `session_type`: `"build"`, `"trade"`, or `"life_aria"`
- `timestamp`: ISO 8601 timestamp
- `agent_id`: Your agent ID (e.g., `"Agent-5"`)

**Optional but Recommended**:
- `metadata`: Duration, files changed, lines added/removed
- `deliverables`: List of files created/modified
- `key_achievements`: Summary of what was accomplished
- `output_flywheel_usage`: Mark as `{"tracked": true}`

### Step 2: Track Session

Run the usage tracker to scan and record your session:

```bash
cd systems/output_flywheel
python output_flywheel_usage_tracker.py scan
```

This will:
- ✅ Scan all session files
- ✅ Record artifacts in metrics tracker
- ✅ Update usage statistics

### Step 3: View Usage Summary

Check your session was tracked:

```bash
python output_flywheel_usage_tracker.py summary
```

### Step 4: Submit Feedback (Optional)

If you have feedback for v1.1 improvements:

```bash
python output_flywheel_usage_tracker.py feedback \
  --agent Agent-5 \
  --type feature_request \
  --category usability \
  --feedback "Would like automated session creation" \
  --priority high
```

**Feedback Types**:
- `feature_request`: New functionality requested
- `bug`: Bug or issue found
- `improvement`: Enhancement to existing feature
- `question`: Question or clarification needed

**Categories**:
- `usability`: Ease of use improvements
- `documentation`: Documentation issues/requests
- `pipeline`: Pipeline-related feedback
- `monitoring`: Monitoring/metrics feedback
- `performance`: Performance issues
- `integration`: Integration with other systems

---

## 📊 Example Session File

```json
{
  "session_id": "a5-2025-12-02-guardrail-impl",
  "session_type": "build",
  "timestamp": "2025-12-02T03:00:00.000000",
  "agent_id": "Agent-5",
  "metadata": {
    "duration_minutes": 120,
    "files_changed": 4,
    "lines_added": 450
  },
  "deliverables": [
    {
      "type": "metrics_monitor",
      "file": "systems/output_flywheel/metrics_monitor.py",
      "status": "complete"
    }
  ],
  "key_achievements": [
    "Implemented complete guardrail monitoring system"
  ],
  "output_flywheel_usage": {
    "tracked": true,
    "artifacts_recorded": 1
  }
}
```

---

## 🔍 Monitoring

Agent-5 will monitor:
- ✅ Session creation frequency
- ✅ Artifact generation rates
- ✅ Usage by agent and type
- ✅ Feedback collection for v1.1

Check monitoring status:
```bash
cd systems/output_flywheel
python metrics_monitor.py check
```

---

## 💡 Best Practices

1. **Create session file immediately** after completing work
2. **Include all deliverables** in the session file
3. **Be specific** in key achievements
4. **Track everything** - helps identify patterns
5. **Submit feedback** when you encounter issues or have ideas

---

## 🐛 Troubleshooting

### Session not tracked?
- Check file is in `outputs/sessions/` directory
- Verify JSON is valid (use JSON validator)
- Ensure required fields are present

### Feedback not saved?
- Check file permissions
- Verify all required arguments provided
- Check feedback file exists in `feedback/` directory

---

## 📚 Related Documentation

- `docs/metrics/OUTPUT_FLYWHEEL_METRICS_GUARDRAILS.md` - Guardrail system
- `systems/output_flywheel/README_METRICS.md` - Metrics system overview
- `systems/output_flywheel/schemas/work_session.json` - Session schema

---

🐝 **WE. ARE. SWARM. ⚡🔥**




