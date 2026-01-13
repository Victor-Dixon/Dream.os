# Cycle Report Tools Comparison

**Last Updated:** 2025-12-26  
**Purpose:** Clarify when to use which cycle report tool

---

## Overview

There are multiple cycle-related tools that serve different purposes. This document clarifies when to use each tool.

---

## Tool Comparison

### 1. `generate_cycle_accomplishments_report.py` ⭐ **PRIMARY - All Agents Report**

**Purpose:** Comprehensive cycle accomplishments report for ALL agents  
**Protocol:** `CYCLE_ACCOMPLISHMENTS_REPORT_GENERATION` v1.0  
**Location:** `tools/generate_cycle_accomplishments_report.py`

**What it does:**
- Aggregates accomplishments from ALL agent status.json files
- Extracts: completed_tasks, achievements, current_tasks, current_mission
- Generates full markdown report with agent sections
- Automatically posts summary to Discord (Agent-4 channel)

**Output:**
- File: `reports/cycle_accomplishments_YYYY-MM-DD_HHMMSS.md`
- Discord: Summary posted to Agent-4 (Captain) channel

**When to use:**
- ✅ After significant swarm activity cycles
- ✅ Post-onboarding cycles (automatic via soft_onboard_multiple_agents)
- ✅ Periodic summaries (daily/weekly)
- ✅ Pre-transition summaries
- ✅ **When you need comprehensive all-agents accomplishments**

**Usage:**
```bash
python tools/generate_cycle_accomplishments_report.py
```

**Protocol Documentation:** `docs/CYCLE_ACCOMPLISHMENTS_REPORT_PROTOCOL.md`

---

### 2. `CycleReportTool` (captain.cycle_report) - **Captain Metrics Tool**

**Purpose:** Captain-specific cycle activity metrics  
**Location:** `tools/categories/captain_tools_monitoring.py`  
**Tool Name:** `captain.cycle_report`

**What it does:**
- Generates Captain's own cycle activity report
- Tracks: missions assigned, messages sent, agents activated, points awarded
- Captain-focused metrics (not agent accomplishments)
- Simpler, metrics-focused format

**Output:**
- File: `agent_workspaces/Agent-4/CAPTAIN_CYCLE_{cycle_num}_{timestamp}.md`

**When to use:**
- ✅ Captain's own cycle tracking
- ✅ Metrics-focused reports
- ✅ When you need Captain activity metrics (not agent accomplishments)
- ✅ **When you need Captain's operational metrics**

**Usage:**
```python
# Via tool adapter
tool = CycleReportTool()
result = tool.execute({
    "cycle_number": 123,
    "missions_assigned": 5,
    "messages_sent": 10,
    "agents_activated": ["Agent-1", "Agent-2"],
    "points_awarded": 150,
    "notes": "Cycle summary notes"
})
```

---

### 3. `generate_daily_episode.py` - **Narrative Generator** (Different Purpose)

**Purpose:** Generate narrative/blog post content from accomplishments  
**Location:** `tools/generate_daily_episode.py`

**What it does:**
- Extracts accomplishments for storytelling
- Uses Ollama to generate narrative content
- Creates blog post format for Digital Dreamscape
- **NOT a report tool - narrative generation tool**

**When to use:**
- ✅ Blog post generation
- ✅ Storytelling/narrative content
- ✅ Daily episode creation
- ❌ **NOT for cycle reports**

---

### 4. `check_duplicate_accomplishments.py` - **Validator** (Different Purpose)

**Purpose:** Validates accomplishments (checks for duplicates)  
**Location:** `scripts/check_duplicate_accomplishments.py`

**What it does:**
- Checks for duplicate accomplishments within a single agent
- Analysis/validation tool
- **NOT a report generator**

**When to use:**
- ✅ Data quality validation
- ✅ Duplicate detection
- ❌ **NOT for cycle reports**

---

## Decision Tree

### Need comprehensive all-agents accomplishments?
→ **Use:** `generate_cycle_accomplishments_report.py` ⭐

### Need Captain's operational metrics?
→ **Use:** `CycleReportTool` (captain.cycle_report)

### Need narrative/blog content?
→ **Use:** `generate_daily_episode.py`

### Need to validate accomplishments?
→ **Use:** `check_duplicate_accomplishments.py`

---

## Key Differences

| Feature | generate_cycle_accomplishments_report.py | CycleReportTool |
|---------|------------------------------------------|-----------------|
| **Scope** | All agents | Captain only |
| **Content** | Agent accomplishments | Captain metrics |
| **Format** | Comprehensive agent sections | Metrics-focused |
| **Discord** | ✅ Auto-posts summary | ❌ No auto-posting |
| **Protocol** | ✅ Documented protocol | Tool adapter |
| **Trigger** | Manual or auto (onboarding) | Manual (tool call) |

---

## Recommendations

### For Most Use Cases
**Use:** `generate_cycle_accomplishments_report.py` ⭐
- Most comprehensive
- Includes all agents
- Auto-posts to Discord
- Well-documented protocol

### For Captain Metrics Only
**Use:** `CycleReportTool`
- When you specifically need Captain's operational metrics
- Metrics-focused format
- Captain workspace location

---

## Protocol Status

- ✅ `generate_cycle_accomplishments_report.py` - **PROTOCOL DOCUMENTED** (`docs/CYCLE_ACCOMPLISHMENTS_REPORT_PROTOCOL.md`)
- ⚠️ `CycleReportTool` - Tool adapter (no separate protocol doc)
- ℹ️ `generate_daily_episode.py` - Different purpose (narrative generation)
- ℹ️ `check_duplicate_accomplishments.py` - Different purpose (validation)

---

**Summary:** Use `generate_cycle_accomplishments_report.py` for comprehensive all-agents cycle reports. Use `CycleReportTool` for Captain-specific metrics only.

---

*Last Updated: 2025-12-26*




