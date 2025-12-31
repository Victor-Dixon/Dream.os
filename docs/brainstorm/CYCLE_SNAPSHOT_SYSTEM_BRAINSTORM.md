# Cycle Snapshot System - Brainstorming Session

**Date:** 2025-12-31  
**Purpose:** Comprehensive brainstorming for cycle accomplishments snapshot system with status.json reset  
**Approach:** AI Force Multiplication - Deep exploration of all factors

---

## 🎯 Core Concept

**What We're Building:**
A system that captures a complete snapshot of project state at cycle boundaries, then resets status.json files to neutral state, enabling:
- Clean cycle-to-cycle tracking
- Complete historical record
- Strategic decision-making for next cycle
- "Where we left off" baseline

---

## 📊 Data Sources to Aggregate

### 1. Agent Status Files (`agent_workspaces/Agent-X/status.json`)
**What to Capture:**
- `completed_tasks` → Archive, then clear
- `achievements` → Archive, then clear
- `current_tasks` → Archive completed ones, keep active ones
- `current_mission` → Keep (ongoing context)
- `mission_priority` → Keep (ongoing context)
- `mission_description` → Keep (ongoing context)
- `status` → Keep (current state)
- `fsm_state` → Keep (current state)
- `current_phase` → Keep (current state)
- `cycle_count` → Increment, keep
- `last_updated` → Update to snapshot timestamp
- `coordination_status` → Archive, reset if completed
- `next_actions` → Archive completed, keep pending
- `recent_commit` → Archive, clear
- `recent_artifact` → Archive, clear

**Reset Logic:**
```json
{
  "agent_id": "Agent-3",
  "agent_name": "Infrastructure & DevOps Specialist",
  "status": "ACTIVE_AGENT_MODE",  // KEEP
  "fsm_state": "ACTIVE",  // KEEP
  "current_phase": "TASK_EXECUTION",  // KEEP
  "last_updated": "2025-12-31T10:00:00.000000+00:00",  // UPDATE
  "cycle_count": 60,  // INCREMENT
  "current_mission": "Infrastructure Refactoring & Deployment Support",  // KEEP
  "mission_priority": "HIGH",  // KEEP
  "mission_description": "...",  // KEEP
  "current_tasks": [],  // CLEAR COMPLETED, KEEP ACTIVE
  "completed_tasks": [],  // CLEAR (archived to snapshot)
  "achievements": [],  // CLEAR (archived to snapshot)
  "next_actions": [],  // CLEAR COMPLETED, KEEP PENDING
  "coordination_status": {},  // RESET IF COMPLETED
  "recent_commit": null,  // CLEAR
  "recent_artifact": null  // CLEAR
}
```

### 2. MASTER_TASK_LOG.md
**What to Capture:**
- Task completion status changes (✅ vs ⏳)
- New tasks added since last snapshot
- Tasks moved between sections (INBOX → THIS WEEK → WAITING ON → PARKED)
- Priority changes
- Assignment changes
- Blocker status
- Progress percentages by initiative

**Parse Strategy:**
- Read entire file
- Compare with previous snapshot (if exists)
- Extract deltas (what changed)
- Track completion counts
- Track initiative progress

**Output:**
```json
{
  "task_metrics": {
    "total_tasks": 150,
    "completed_this_cycle": 12,
    "new_tasks_added": 8,
    "tasks_moved": 5,
    "by_priority": {
      "HIGH": {"total": 45, "completed": 8},
      "MEDIUM": {"total": 60, "completed": 3},
      "LOW": {"total": 45, "completed": 1}
    },
    "by_initiative": {
      "Week 1 P0": {"total": 19, "completed": 2},
      "Build-In-Public": {"total": 8, "completed": 3},
      "Infrastructure Refactoring": {"total": 3, "completed": 1}
    },
    "blockers": ["Deployment credentials needed", "SSH access pending"]
  }
}
```

### 3. Project Scanner / Project Analysis
**What to Scan:**
- Git commits since last snapshot
- Files changed (added, modified, deleted)
- Code metrics (lines added/removed, files changed)
- Test coverage changes
- V2 compliance status
- Dependency changes
- Build status

**Tools to Leverage:**
- `git log --since` (commits since last snapshot)
- `git diff --stat` (file change statistics)
- Project analysis JSON files (if they exist)
- Test results
- Linter results

**Output:**
```json
{
  "git_activity": {
    "commits": 15,
    "files_changed": 42,
    "lines_added": 1250,
    "lines_removed": 380,
    "net_change": 870,
    "authors": ["Agent-3", "Agent-7", "Agent-4"],
    "commit_messages": ["feat: ...", "fix: ..."]
  },
  "code_metrics": {
    "files_created": 8,
    "files_modified": 34,
    "files_deleted": 2,
    "v2_compliant_files": 40,
    "v2_violations": 2
  }
}
```

### 4. CHANGELOG.md
**What to Capture:**
- New entries since last snapshot
- Version bumps
- Feature additions
- Bug fixes
- Breaking changes

**Parse Strategy:**
- Read CHANGELOG.md
- Find entries after last snapshot date
- Extract categorized changes (Added, Changed, Removed, Fixed)

**Output:**
```json
{
  "changelog_entries": {
    "added": ["New feature X", "New tool Y"],
    "changed": ["Refactored Z", "Updated W"],
    "removed": ["Deprecated V"],
    "fixed": ["Bug fix U"]
  },
  "version_bump": null  // or "2.1.0" if version changed
}
```

### 5. Captain's Log
**What to Capture:**
- New log entries since last snapshot
- Mission status updates
- Swarm health assessments
- Critical decisions
- Emergency interventions

**Parse Strategy:**
- Read captain log files
- Extract entries after last snapshot timestamp
- Categorize by type (mission briefing, status update, decision, intervention)

**Output:**
```json
{
  "captain_log_entries": [
    {
      "date": "2025-12-31",
      "type": "mission_briefing",
      "content": "...",
      "swarm_health": "EXCELLENT"
    }
  ],
  "decisions_made": 3,
  "interventions": 0
}
```

### 6. Additional Data Sources (Consider)

**Git Repository State:**
- Branch status
- Uncommitted changes
- Stash status
- Remote sync status

**Discord Activity:**
- Messages posted since last snapshot
- Coordination messages
- Blocker reports

**MCP Tool Usage:**
- Tools called since last snapshot
- Tool success/failure rates
- Tool performance metrics

**Website Deployment Status:**
- Sites deployed
- Deployment success/failure
- Rollback events

**Test Results:**
- Test pass/fail counts
- Coverage changes
- Performance benchmarks

---

## 🔄 Reset Logic Deep Dive

### What Gets Reset vs. What Gets Kept

**RESET (Clear/Archive):**
- `completed_tasks` → Move to snapshot, clear array
- `achievements` → Move to snapshot, clear array
- `current_tasks` → Filter: completed ones → archive, active ones → keep
- `next_actions` → Filter: completed ones → archive, pending ones → keep
- `coordination_status` → If status is "COMPLETE", archive and clear
- `recent_commit` → Clear (null)
- `recent_artifact` → Clear (null)

**KEEP (Ongoing Context):**
- `agent_id` → Identity, never changes
- `agent_name` → Identity, never changes
- `status` → Current operational state
- `fsm_state` → Current finite state machine state
- `current_phase` → Current work phase
- `current_mission` → Ongoing mission context
- `mission_priority` → Mission priority level
- `mission_description` → Mission description
- `cycle_count` → Increment by 1

**UPDATE:**
- `last_updated` → Set to snapshot timestamp

### Reset Strategy Options

**Option A: Full Reset (Aggressive)**
- Clear everything except identity and mission context
- Pros: Clean slate, no carryover confusion
- Cons: Lose context of active work

**Option B: Smart Reset (Recommended)**
- Archive completed items, keep active items
- Pros: Preserves active work context
- Cons: More complex logic

**Option C: Incremental Reset**
- Only reset if agent explicitly marks items as "cycle_complete"
- Pros: Agent control
- Cons: Requires agent discipline

**Recommendation: Option B (Smart Reset)**

### Reset Implementation

```python
def reset_agent_status(agent_id: str, snapshot_data: dict, workspace_root: Path):
    """
    Reset agent status.json to neutral state after snapshot.
    
    Strategy:
    1. Keep identity and mission context
    2. Archive completed items to snapshot
    3. Keep active items (current_tasks, next_actions)
    4. Clear completed items
    5. Update timestamps
    6. Increment cycle_count
    """
    status_file = workspace_root / "agent_workspaces" / agent_id / "status.json"
    current_status = load_json(status_file)
    
    # Archive completed items to snapshot
    snapshot_data[agent_id] = {
        "completed_tasks": current_status.get("completed_tasks", []),
        "achievements": current_status.get("achievements", []),
        "completed_current_tasks": filter_completed(current_status.get("current_tasks", [])),
        "completed_next_actions": filter_completed(current_status.get("next_actions", [])),
        "completed_coordinations": filter_completed_coordinations(current_status.get("coordination_status", {})),
        "recent_commit": current_status.get("recent_commit"),
        "recent_artifact": current_status.get("recent_artifact")
    }
    
    # Reset status.json
    new_status = {
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
        "last_updated": datetime.now().isoformat(),
        
        # Active work (keep active, clear completed)
        "current_tasks": filter_active(current_status.get("current_tasks", [])),
        "next_actions": filter_active(current_status.get("next_actions", [])),
        
        # Completed work (clear - archived to snapshot)
        "completed_tasks": [],
        "achievements": [],
        
        # Coordination (reset if completed)
        "coordination_status": reset_coordination_status(current_status.get("coordination_status", {})),
        
        # Recent activity (clear)
        "recent_commit": None,
        "recent_artifact": None
    }
    
    # Write reset status
    save_json(status_file, new_status)
    
    return snapshot_data
```

---

## 📸 Snapshot Structure

### Snapshot File Format

**Location:** `reports/cycle_snapshots/cycle_snapshot_YYYYMMDD_HHMMSS.json`

**Structure:**
```json
{
  "snapshot_metadata": {
    "snapshot_id": "cycle_snapshot_20251231_100000",
    "timestamp": "2025-12-31T10:00:00.000000+00:00",
    "date": "2025-12-31",
    "cycle_number": 60,
    "generated_by": "cycle_accomplishments_snapshot_system",
    "protocol_version": "2.0"
  },
  
  "agent_accomplishments": {
    "Agent-1": {
      "completed_tasks": [...],
      "achievements": [...],
      "completed_current_tasks": [...],
      "completed_next_actions": [...],
      "recent_commit": "...",
      "recent_artifact": "..."
    },
    "Agent-2": {...},
    ...
  },
  
  "project_metrics": {
    "task_metrics": {...},
    "git_activity": {...},
    "code_metrics": {...},
    "changelog_entries": {...},
    "captain_log_entries": [...]
  },
  
  "project_state": {
    "overall_status": "ACTIVE_DEVELOPMENT",
    "active_initiatives": [...],
    "blockers": [...],
    "next_steps": [...],
    "health_metrics": {...}
  },
  
  "reset_status": {
    "agents_reset": ["Agent-1", "Agent-2", ...],
    "reset_timestamp": "2025-12-31T10:00:05.000000+00:00",
    "reset_errors": []
  }
}
```

### Markdown Report Format

**Location:** `reports/cycle_snapshots/cycle_snapshot_YYYYMMDD_HHMMSS.md`

**Structure:**
```markdown
# 🚀 Cycle Snapshot Report

**Snapshot ID:** cycle_snapshot_20251231_100000  
**Date:** 2025-12-31  
**Cycle:** 60  
**Generated:** 2025-12-31T10:00:00.000000+00:00

---

## 📊 Executive Summary

**Status:** ✅ ACTIVE DEVELOPMENT  
**Agents Active:** 8/8  
**Tasks Completed This Cycle:** 45  
**Achievements:** 12  
**Git Activity:** 15 commits, 42 files changed, +870 lines

---

## 👥 Agent Accomplishments

### Agent-1: Integration & Core Systems
**Completed Tasks (12):**
- Task 1
- Task 2
...

**Achievements (3):**
- Achievement 1
- Achievement 2
...

**Recent Commit:** abc123def
**Recent Artifact:** path/to/artifact

---

## 📈 Project Metrics

### Task Metrics
- **Total Tasks:** 150
- **Completed This Cycle:** 12
- **New Tasks Added:** 8
- **By Priority:**
  - HIGH: 8/45 completed
  - MEDIUM: 3/60 completed
  - LOW: 1/45 completed

### Git Activity
- **Commits:** 15
- **Files Changed:** 42
- **Lines Added:** 1,250
- **Lines Removed:** 380
- **Net Change:** +870

### Code Metrics
- **Files Created:** 8
- **Files Modified:** 34
- **Files Deleted:** 2
- **V2 Compliant:** 40/42 files

---

## 🎯 Project State

### Active Initiatives
- Week 1 P0 Execution: 2/19 complete (11%)
- Build-In-Public: 3/8 complete (38%)
- Infrastructure Refactoring: 1/3 complete (33%)

### Blockers
1. Deployment credentials needed
2. SSH access pending

### Next Steps
1. Complete TradingRobotPlug theme deployment
2. Execute remaining Tier 1 Quick Wins
...

---

## 🔄 Reset Status

**Agents Reset:** 8/8  
**Reset Timestamp:** 2025-12-31T10:00:05.000000+00:00  
**Reset Errors:** None

All agent status.json files have been reset to neutral state.  
Next cycle will start from clean baseline.

---

## 📋 Full Data

See `cycle_snapshot_YYYYMMDD_HHMMSS.json` for complete structured data.

---
*This snapshot captures all accomplishments from the previous cycle and resets status files for the next cycle.*
```

---

## 🔍 Edge Cases & Considerations

### 1. Partial Reset Scenarios

**What if an agent has active coordination?**
- Keep coordination_status if status is "IN_PROGRESS"
- Only reset if status is "COMPLETE" or "BLOCKED"

**What if current_tasks has mixed completed/active?**
- Parse task strings for completion markers (✅, 🟡, ⏳)
- Archive completed ones, keep active ones

**What if next_actions has dependencies?**
- Keep actions that are prerequisites for other actions
- Only archive truly completed actions

### 2. Data Integrity

**What if status.json is corrupted?**
- Validate JSON before reading
- Create backup before reset
- Log errors, skip reset for that agent
- Continue with other agents

**What if snapshot write fails?**
- Don't reset status.json files
- Log error, exit with error code
- Preserve original state

**What if git history is unavailable?**
- Use fallback: scan file modification times
- Or skip git metrics, continue with other data

### 3. Historical Tracking

**How to track "since last snapshot"?**
- Store last snapshot timestamp in `reports/cycle_snapshots/.last_snapshot`
- Read on next run to determine "since" date
- Update after successful snapshot

**What if no previous snapshot exists?**
- This is the first snapshot
- Capture everything from beginning of time (or reasonable cutoff)
- Set baseline for future comparisons

### 4. Concurrent Access

**What if agent is updating status.json during snapshot?**
- Use file locking (if supported)
- Or: read, validate, write atomically
- Or: retry on conflict

**What if multiple snapshots run simultaneously?**
- Use lock file: `reports/cycle_snapshots/.snapshot_in_progress`
- Check lock before starting
- Release lock after completion

### 5. Rollback Scenarios

**What if reset was incorrect?**
- Keep backup of original status.json files
- Store in `reports/cycle_snapshots/backups/Agent-X_status_YYYYMMDD_HHMMSS.json`
- Provide rollback command

**What if snapshot data is lost?**
- Status.json files are reset (can't recover from snapshot)
- But snapshot JSON file should have all data
- Could restore from snapshot JSON if needed

### 6. Agent-Specific Considerations

**What if agent has no completed_tasks?**
- Empty array is fine
- Snapshot shows empty array
- Reset clears empty array (no-op)

**What if agent status.json is missing?**
- Skip that agent
- Log warning
- Continue with other agents

**What if agent has custom fields?**
- Preserve unknown fields in reset
- Or: explicitly handle known fields, ignore unknown
- Document in protocol

---

## 🏗️ Architecture Options

### Option A: Monolithic Script
**Structure:**
```
tools/generate_cycle_snapshot.py
  - collect_agent_data()
  - collect_project_data()
  - generate_snapshot()
  - reset_agent_status()
  - save_snapshot()
```

**Pros:**
- Simple, single file
- Easy to understand flow

**Cons:**
- Not modular
- Hard to test
- Violates V2 compliance (likely >400 lines)

### Option B: Modular System (Recommended)
**Structure:**
```
tools/cycle_snapshots/
  - __init__.py
  - data_collector.py      # Collect from all sources
  - snapshot_generator.py  # Generate snapshot structure
  - status_resetter.py     # Reset agent status.json files
  - report_generator.py    # Generate markdown report
  - main.py                # CLI entrypoint
```

**Pros:**
- Modular, V2 compliant
- Testable components
- Reusable modules
- Clear separation of concerns

**Cons:**
- More files
- More complex structure

### Option C: Extend Existing Cycle Accomplishments
**Structure:**
```
tools/cycle_accomplishments/
  - data_collector.py (existing)
  - report_generator.py (existing)
  - snapshot_generator.py (NEW)
  - status_resetter.py (NEW)
  - main.py (extend)
```

**Pros:**
- Reuses existing infrastructure
- Single command for both
- Consistent data collection

**Cons:**
- Couples snapshot with accomplishments
- Might be confusing

**Recommendation: Option B (Modular System)**

---

## 🔄 Workflow

### Snapshot Generation Workflow

```
1. PRE-SNAPSHOT CHECKS
   ├─ Check for lock file (prevent concurrent runs)
   ├─ Validate workspace structure
   ├─ Check for previous snapshot (for "since" date)
   └─ Create lock file

2. DATA COLLECTION
   ├─ Collect agent status.json files (all agents)
   ├─ Parse MASTER_TASK_LOG.md
   ├─ Run git analysis (commits, changes since last snapshot)
   ├─ Parse CHANGELOG.md (entries since last snapshot)
   ├─ Parse captain's log (entries since last snapshot)
   ├─ Run project scanner (if available)
   └─ Aggregate all data

3. SNAPSHOT GENERATION
   ├─ Create snapshot structure
   ├─ Populate agent accomplishments
   ├─ Populate project metrics
   ├─ Generate project state summary
   └─ Calculate deltas (if previous snapshot exists)

4. REPORT GENERATION
   ├─ Generate markdown report
   ├─ Generate JSON snapshot
   └─ Generate blog post (optional)

5. STATUS RESET
   ├─ For each agent:
   │   ├─ Backup original status.json
   │   ├─ Archive completed items to snapshot
   │   ├─ Reset status.json to neutral state
   │   └─ Validate reset status.json
   └─ Log reset results

6. POST-SNAPSHOT
   ├─ Update .last_snapshot timestamp
   ├─ Release lock file
   ├─ Post to Discord (optional)
   └─ Log completion
```

### Error Handling Workflow

```
IF data collection fails:
  ├─ Log error
  ├─ Continue with available data
  └─ Mark incomplete in snapshot metadata

IF snapshot generation fails:
  ├─ Log error
  ├─ Don't reset status.json files
  └─ Exit with error code

IF status reset fails for agent:
  ├─ Log error for that agent
  ├─ Continue with other agents
  ├─ Mark in reset_status.errors
  └─ Don't fail entire snapshot

IF snapshot save fails:
  ├─ Log error
  ├─ Don't reset status.json files
  └─ Exit with error code
```

---

## 📊 Benefits Analysis

### For Strategic Planning
- **Clear Baseline:** Know exactly where you left off
- **Complete Picture:** All accomplishments in one place
- **Trend Analysis:** Compare cycles over time
- **Decision Support:** Data-driven next cycle planning

### For Agent Coordination
- **Clean Slate:** Agents start fresh each cycle
- **No Confusion:** Completed items don't clutter status
- **Active Focus:** Only see what's actually in progress
- **Historical Record:** All accomplishments preserved

### For Project Management
- **Progress Tracking:** Clear metrics per cycle
- **Blocker Visibility:** See what's blocking progress
- **Initiative Status:** Track multi-cycle initiatives
- **Resource Allocation:** See where effort went

### For Documentation
- **Complete History:** Every cycle documented
- **Audit Trail:** Can trace back any decision
- **Learning:** See patterns over time
- **Reporting:** Easy to generate summaries

---

## 🚀 Implementation Phases

### Phase 1: Core Snapshot System
- Data collection from status.json files
- Basic snapshot generation (JSON)
- Simple status reset (clear completed_tasks, achievements)
- Markdown report generation

### Phase 2: Enhanced Data Sources
- MASTER_TASK_LOG.md parsing
- Git activity analysis
- CHANGELOG.md parsing
- Captain's log parsing

### Phase 3: Smart Reset Logic
- Intelligent filtering (active vs completed)
- Coordination status handling
- Next actions filtering
- Backup and rollback

### Phase 4: Historical Tracking
- Previous snapshot comparison
- Delta calculations
- Trend analysis
- Historical reports

### Phase 5: Advanced Features
- Project scanner integration
- Discord posting
- Blog post generation
- Dashboard/visualization

---

## 🤔 Open Questions

1. **Snapshot Frequency:**
   - Daily? End of day?
   - Per cycle? What defines a cycle?
   - Manual trigger only?
   - Automatic on certain conditions?

2. **Retention Policy:**
   - Keep all snapshots forever?
   - Archive old snapshots?
   - Delete after X days?
   - Compress old snapshots?

3. **Backup Strategy:**
   - Backup status.json before reset?
   - How many backups to keep?
   - Where to store backups?

4. **Rollback Mechanism:**
   - CLI command to rollback?
   - Selective rollback (one agent)?
   - Full rollback (all agents)?

5. **Integration Points:**
   - Hook into cycle completion?
   - Trigger from Captain?
   - Scheduled job?
   - Manual only?

6. **Data Privacy:**
   - Should snapshots be committed to git?
   - Or kept local only?
   - Or archived separately?

7. **Performance:**
   - How long does snapshot take?
   - Can it run in background?
   - Should it be async?

8. **Validation:**
   - Validate snapshot data before reset?
   - Validate reset status.json after write?
   - What if validation fails?

---

## 💡 Force Multiplication Ideas

### 1. Predictive Analytics
- Analyze patterns in snapshots
- Predict cycle completion times
- Identify bottlenecks early
- Suggest optimizations

### 2. Automated Insights
- "Agent-X completed 3x more tasks this cycle"
- "Initiative Y is 50% behind schedule"
- "Blocker Z has been active for 5 cycles"
- "Recommended next actions based on patterns"

### 3. Comparative Analysis
- Compare this cycle to last cycle
- Compare to same day last week
- Compare to average
- Highlight anomalies

### 4. Integration with Other Systems
- Feed snapshot data to Swarm Brain
- Update MASTER_TASK_LOG automatically
- Trigger workflows based on snapshot
- Update dashboards

### 5. Smart Recommendations
- "Based on cycle patterns, suggest focusing on X"
- "Agent-Y typically completes Z tasks per cycle"
- "Initiative A needs attention (behind schedule)"
- "Consider delegating B to Agent-Z (expertise match)"

---

## 🎯 Success Criteria

**System is successful if:**
1. ✅ Can generate complete snapshot in <30 seconds
2. ✅ All agent status.json files reset correctly
3. ✅ No data loss during reset
4. ✅ Snapshot contains all expected data sources
5. ✅ Can rollback if needed
6. ✅ Historical snapshots are queryable
7. ✅ Reports are actionable for next cycle planning
8. ✅ Zero manual intervention required (once set up)

---

## 📝 Next Steps

1. **Review this brainstorm** - Identify missing factors
2. **Prioritize features** - What's MVP vs nice-to-have
3. **Design data structures** - Finalize snapshot JSON schema
4. **Prototype reset logic** - Test with one agent first
5. **Build incrementally** - Phase 1 → Phase 2 → Phase 3
6. **Test thoroughly** - Especially edge cases
7. **Document** - Protocol, usage, examples
8. **Deploy** - Integrate into workflow

---

**Status:** 🧠 BRAINSTORMING COMPLETE  
**Ready for:** Review, prioritization, design refinement  
**Next:** Implementation planning

