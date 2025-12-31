# Cycle Snapshot System

**Version:** 0.1.0 (Phase 1)  
**Author:** Agent-3 (Infrastructure & DevOps Specialist)  
**Architecture:** Agent-2 (Architecture & Design Specialist)  
**Created:** 2025-12-31

---

## 🎯 Overview

The Cycle Snapshot System is the **central hub** for capturing complete project state at cycle boundaries. It collects data from all agents, task logs, git activity, and other systems to generate comprehensive snapshots for strategic decision-making.

**Phase 1 Status:** Core foundation complete (read-only operations)

---

## 📁 Module Structure

```
tools/cycle_snapshots/
├── __init__.py
├── main.py                    # CLI entrypoint
├── data_collectors/           # Data collection modules
│   ├── agent_status_collector.py
│   ├── task_log_collector.py
│   └── git_collector.py
├── aggregators/               # Data aggregation modules
│   └── snapshot_aggregator.py
├── processors/                # Data processing modules
│   └── report_generator.py
├── core/                      # Core utilities
│   └── snapshot_models.py
└── README.md                  # This file
```

---

## 🚀 Usage

### Basic Usage

```bash
# Generate snapshot from current directory
python -m tools.cycle_snapshots.main

# Specify workspace root
python -m tools.cycle_snapshots.main --workspace-root /path/to/workspace

# Specify output directory
python -m tools.cycle_snapshots.main --output-dir /path/to/output

# Analyze since specific timestamp
python -m tools.cycle_snapshots.main --since "2025-12-30T10:00:00"

# Enable verbose logging
python -m tools.cycle_snapshots.main --verbose
```

### CLI Arguments

- `--workspace-root` (optional): Root workspace path (default: current directory)
- `--output-dir` (optional): Output directory (default: `reports/cycle_snapshots/`)
- `--since` (optional): Timestamp to analyze since (ISO format, defaults to 24 hours ago or last snapshot)
- `--verbose` (optional): Enable verbose logging

---

## 📊 Output Format

### Snapshot JSON

Saved to: `reports/cycle_snapshots/cycle_snapshot_{cycle}_{timestamp}.json`

**Structure:**
```json
{
  "snapshot_metadata": {
    "cycle": 10,
    "date": "2025-12-31T10:00:00",
    "previous_cycle": 9,
    "previous_snapshot_timestamp": "2025-12-30T10:00:00",
    "workspace_root": "/path/to/workspace"
  },
  "agent_accomplishments": {
    "Agent-1": {
      "agent_id": "Agent-1",
      "agent_name": "Integration & Core Systems Specialist",
      "completed_tasks": ["Task 1", "Task 2"],
      "achievements": ["Achievement 1"],
      "current_tasks": ["Task 3"],
      "current_mission": "Mission description",
      "mission_priority": "HIGH",
      "cycle_count": 10
    }
  },
  "project_metrics": {
    "total_agents": 8,
    "total_completed_tasks": 45,
    "total_achievements": 12,
    "active_tasks_count": 20,
    "git_commits": 15,
    "git_files_changed": 42,
    "task_log_metrics": {
      "inbox_count": 5,
      "this_week_count": 10
    }
  },
  "raw_data": {
    "agent_status": {...},
    "task_log": {...},
    "git_activity": {...}
  }
}
```

### Markdown Report

Saved to: `reports/cycle_snapshots/cycle_snapshot_{cycle}_{timestamp}.md`

**Sections:**
- Executive Summary
- Agent Accomplishments (per agent)
- Project Metrics
- Task Log Metrics
- Git Activity

---

## 🔧 Integration Points

### Data Collectors

**Agent Status Collector:**
- Reads `agent_workspaces/Agent-X/status.json` files
- Validates JSON structure
- Handles missing files gracefully

**Task Log Collector:**
- Parses `MASTER_TASK_LOG.md`
- Extracts task counts by priority
- Extracts task counts by section (INBOX, THIS WEEK, etc.)

**Git Collector:**
- Analyzes git commits since last snapshot
- Extracts commit count, authors, messages
- Handles git not available gracefully

### Future Integrations (Phase 2+)

- MCP server integrations (Swarm Brain, Task Manager, etc.)
- Status.json reset logic
- Blog post generation
- Discord posting
- Multi-system distribution

---

## 🧪 Testing

Run unit tests:

```bash
pytest tests/unit/tools/test_cycle_snapshots_phase1.py -v
```

**Test Coverage:**
- Agent status collector (validation, collection, error handling)
- Task log collector (parsing, metrics extraction)
- Git collector (commit analysis, error handling)
- Snapshot aggregator (data aggregation, metadata generation)
- Report generator (markdown formatting)
- Error handling (invalid JSON, missing files)
- Edge cases (empty data, no agents)

---

## 📋 Phase 1 Limitations

**Phase 1 is read-only:**
- ✅ Data collection
- ✅ Snapshot generation
- ✅ Report generation
- ❌ Status.json reset (Phase 2)
- ❌ Discord integration (Phase 3)
- ❌ Blog publishing (Phase 4)
- ❌ MCP server integrations (Phase 3)

---

## 🔒 Safety

**Phase 1 Safety:**
- ✅ Read-only operations (no file modifications)
- ✅ Error isolation (one collector failure doesn't break snapshot)
- ✅ Graceful degradation (missing dependencies handled)
- ✅ Validation before processing
- ✅ Comprehensive error logging

---

## 📝 Development

### Adding New Data Collectors

1. Create module in `data_collectors/`
2. Implement collection function
3. Add error handling and logging
4. Integrate in `main.py`
5. Add unit tests

### Extending Snapshot Models

1. Update `core/snapshot_models.py`
2. Update `aggregators/snapshot_aggregator.py`
3. Update `processors/report_generator.py`
4. Update unit tests

---

## 🐛 Troubleshooting

**Issue: "Not a git repository"**
- Solution: Run from workspace root or specify `--workspace-root`

**Issue: "MASTER_TASK_LOG.md not found"**
- Solution: Ensure task log exists or collector will return empty metrics

**Issue: "Agent status file not found"**
- Solution: Collector handles missing files gracefully, continues with other agents

---

## 📚 Related Documentation

- Architecture Design: `docs/architecture/cycle_snapshot_system_architecture_design.md`
- Implementation Checklist: `docs/coordination/cycle_snapshot_phase1_implementation_checklist.md`
- Code Review Checklists: `docs/coordination/cycle_snapshot_code_review_checklist.md`
- Status Reset Design: `docs/architecture/cycle_snapshot_status_reset_logic_design.md`

---

## 🎯 Next Steps (Phase 2+)

1. **Phase 2:** Status.json reset logic (with safety measures)
2. **Phase 3:** MCP server integrations
3. **Phase 4:** Blog publishing and Discord integration
4. **Phase 5:** Advanced features (progression tracking, grade cards)

---

**Status:** Phase 1 Complete ✅  
**Version:** 0.1.0  
**Last Updated:** 2025-12-31

