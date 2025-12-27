# Unified Cycle Accomplishments Report - How It Works

**Tool:** `tools/unified_cycle_accomplishments_report.py`  
**Protocol:** CYCLE_ACCOMPLISHMENTS_REPORT_GENERATION v2.0 (Unified)  
**Status:** ACTIVE

---

## Overview

This is the **single unified tool** for generating cycle accomplishments reports. It merges capabilities from:

1. **`generate_cycle_accomplishments_report.py`** - All-agents comprehensive report
2. **`CycleReportTool` (captain.cycle_report)** - Captain metrics tracking
3. **`generate_daily_episode.py`** - Accomplishments extraction logic

**Result:** One tool that does everything.

---

## How It Works

### 1. Data Collection

The tool collects data from two sources:

#### A. Agent Status Files (Automatic)
- **Location:** `agent_workspaces/Agent-X/status.json`
- **Data Extracted:**
  - `completed_tasks` - List of completed tasks
  - `achievements` - List of achievements
  - `current_tasks` - List of active tasks
  - `current_mission` - Current mission description
  - `status` - Agent status (ACTIVE, etc.)
  - `mission_priority` - Priority level
  - `last_updated` - Last update timestamp

#### B. Captain Metrics (Optional Manual Input)
- **Cycle Number** - Captain's cycle number
- **Missions Assigned** - Number of missions assigned
- **Messages Sent** - Number of messages sent
- **Agents Activated** - List of agents activated
- **Points Awarded** - Points awarded this cycle
- **Notes** - Additional cycle notes

### 2. Report Generation

The tool generates a unified markdown report with:

1. **Summary Section:**
   - Total agents
   - Total completed tasks
   - Total achievements

2. **Captain Metrics Section** (if provided):
   - Cycle number
   - Missions assigned
   - Messages sent
   - Agents activated
   - Points awarded
   - Cycle notes

3. **Per-Agent Sections:**
   - Agent ID and name
   - Status and priority
   - Current mission
   - Completed tasks (up to 20 most recent)
   - Achievements (up to 15 most recent)
   - Active tasks (up to 10 most recent)

4. **Report Metadata:**
   - Generation timestamp
   - Protocol version
   - Format information

### 3. Discord Posting

The tool automatically posts a summary to Discord:

- **Channel:** Agent-4 (Captain's channel)
- **Content:** Summary with totals, Captain metrics (if provided), and report file reference
- **Format:** Discord webhook message

---

## Usage

### Basic Usage (All-Agents Report)

```bash
python tools/unified_cycle_accomplishments_report.py
```

**Output:**
- Markdown report: `reports/cycle_accomplishments_YYYY-MM-DD_HHMMSS.md`
- Discord post: Summary posted to Agent-4 channel

### With Captain Metrics

```bash
python tools/unified_cycle_accomplishments_report.py \
  --captain-metrics \
  --cycle-number 123 \
  --missions 5 \
  --messages 10 \
  --agents Agent-1 Agent-2 Agent-3 \
  --points 150 \
  --notes "Great cycle progress"
```

**Output:**
- Markdown report with Captain metrics section
- Discord post includes Captain metrics

### Specify Date

```bash
python tools/unified_cycle_accomplishments_report.py --date 2025-12-26
```

**Output:**
- Report for specific date (uses that date in report metadata)

---

## Command-Line Arguments

### Required Arguments
- None (all arguments are optional)

### Optional Arguments

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--date` | string | today | Target date (YYYY-MM-DD format) |
| `--captain-metrics` | flag | false | Include Captain metrics section |
| `--cycle-number` | int | - | Cycle number (required if --captain-metrics) |
| `--missions` | int | 0 | Missions assigned |
| `--messages` | int | 0 | Messages sent |
| `--agents` | list | [] | Agents activated (space-separated) |
| `--points` | int | 0 | Points awarded |
| `--notes` | string | "" | Cycle notes |

---

## Data Flow

```
1. Tool Execution
   ↓
2. Scan agent_workspaces/Agent-X/status.json (all agents)
   ↓
3. Extract accomplishments (completed_tasks, achievements, current_tasks)
   ↓
4. (Optional) Include Captain metrics if --captain-metrics provided
   ↓
5. Format unified markdown report
   ↓
6. Save to reports/cycle_accomplishments_YYYY-MM-DD_HHMMSS.md
   ↓
7. Post summary to Discord (Agent-4 channel)
   ↓
8. Done ✅
```

---

## Integration Points

### Automatic Triggers

1. **Soft Onboarding:**
   - Called by `src/services/onboarding/soft/service.py`
   - Triggered when `generate_cycle_report=True` in `soft_onboard_multiple_agents()`

### Manual Triggers

1. **Command Line:**
   - Run directly: `python tools/unified_cycle_accomplishments_report.py`
   - With options: `python tools/unified_cycle_accomplishments_report.py --captain-metrics --cycle-number 123`

2. **Scheduled:**
   - Can be integrated into cron/scheduled tasks
   - Run daily/weekly for cycle summaries

---

## Output Format

### Markdown Report Structure

```markdown
# Cycle Accomplishments Report

**Generated:** 2025-12-26 07:00:00
**Date:** 2025-12-26
**Agents:** 8

---

## Summary

**Total Agents:** 8
**Total Completed Tasks:** 150
**Total Achievements:** 75

---

## 🎯 CAPTAIN'S CYCLE METRICS #123
[If --captain-metrics provided]

---

## Agent-1: Integration & Core Systems
[Agent accomplishments section]

---

## Agent-2: Architecture & Design
[Agent accomplishments section]

[... more agents ...]

---

## Report Metadata
[Generation info]
```

### Discord Post Format

```
📊 Cycle Accomplishments Report Generated

**Date:** 2025-12-26
**Total Agents:** 8
**Total Completed Tasks:** 150
**Total Achievements:** 75

**Captain Metrics:**
- Cycle #123
- Missions Assigned: 5
- Messages Sent: 10
- Agents Activated: 3
- Points Awarded: 150

**Report File:** cycle_accomplishments_20251226_070000.md

Full report available in: reports/cycle_accomplishments_*.md
```

---

## Error Handling

- **Missing Status Files:** Warning logged, agent skipped
- **Corrupted JSON:** Error logged, agent skipped
- **No Accomplishments:** Error logged, no report generated
- **Discord Posting Failure:** Warning logged, report still generated

---

## Merged Capabilities

### From `generate_cycle_accomplishments_report.py`:
✅ All-agents accomplishments aggregation  
✅ Markdown report generation  
✅ Discord posting  
✅ Status.json parsing  

### From `CycleReportTool`:
✅ Captain metrics section  
✅ Cycle number tracking  
✅ Missions/messages/points tracking  
✅ Agents activated list  

### From `generate_daily_episode.py`:
✅ Accomplishments extraction logic  
✅ Date-based filtering  

---

## Deprecated Tools

After approval, these tools will be deleted:

1. ❌ `tools/generate_cycle_accomplishments_report.py` (merged into unified tool)
2. ❌ `tools/categories/captain_tools_monitoring.py` → `CycleReportTool` (merged into unified tool)
3. ⚠️ `tools/generate_daily_episode.py` (keep - different purpose: narrative generation, not reporting)

**Note:** `generate_daily_episode.py` is kept because it serves a different purpose (narrative/blog generation, not reporting).

---

## Protocol Compliance

- **Protocol ID:** CYCLE_ACCOMPLISHMENTS_REPORT_GENERATION
- **Protocol Version:** 2.0 (Unified)
- **Protocol Status:** ACTIVE
- **Documentation:** This file

---

*Unified tool created by Agent-6 | 2025-12-26*




