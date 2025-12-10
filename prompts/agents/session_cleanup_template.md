# 🔄 SESSION TRANSITION - INTROSPECTION DIRECTIVE

**Complete the following before transitioning:**

## ✅ REQUIRED DELIVERABLES:

### 1️⃣ **CLEANUP SWEEP** 🧹
**CRITICAL FIRST STEP**: Before creating passdown, perform cleanup sweep:
- Remove any temporary files you created during this session
- Archive old devlogs if needed (move to `devlogs/archive/`)
- Clean up test files or temporary scripts
- Remove any `.pyc` files or `__pycache__` directories if created
- Check for any leftover temporary files in your workspace
- Remove any temporary analysis files, JSON dumps, or test outputs
- Clean up any temporary directories you created

**Check these locations:**
- Your workspace: `agent_workspaces/{agent_id}/`
- Tools directory: `tools/` (if you created temp tools)
- Root directory: Check for any temp files at project root

### 2️⃣ Create Passdown (passdown.json)
**Location**: `agent_workspaces/{agent_id}/passdown.json`

Update status with: deliverables, next actions, gas pipeline, blockers

### 3️⃣ Write Devlog Entry
Document: accomplishments, challenges, solutions, learnings

### 4️⃣ Post to Discord
Share: key deliverables, insights, coordination updates

### 5️⃣ Update Swarm Brain
Contribute: new patterns, lessons, protocols, best practices

### 6️⃣ Review Code of Conduct
Ensure: V2 compliance, gas protocols, bilateral partnerships

### 7️⃣ Review Thread
Maintain: context, pending responses, coordination needs

### 8️⃣ **UPDATE STATE_OF_THE_PROJECT_REPORT.md** 📊
Update the unified state report with your achievements, progress, and current status. Location: `STATE_OF_THE_PROJECT_REPORT.md` (root directory). Keep the SSOT current!

### 9️⃣ **ADD PENDING TASKS TO CYCLE PLANNER** 🔄
Add any pending or remaining tasks to the cycle planner. Location: `agent_workspaces/{agent_id}/cycle_planner_tasks_YYYY-MM-DD.json`. Create contracts for unfinished work, blockers, or next session priorities. This ensures continuity and structured task management!

### 🔟 **CREATE NEW PRODUCTIVITY TOOL** ⭐
Build something useful: identify gap, create tool, V2 compliant (<400 lines), add to toolbelt, document usage

**This is your contribution to swarm tooling!**

### 1️⃣1️⃣ **CYCLE HANDOFF PROTOCOL (MANDATORY)** 🛰️
Always leave a handoff for the next operator who will act as the same agent (even if sessions are not switching). Include:
- **Identity reminder**: “You are {agent_id}. Act as {agent_id} for this message.”
- **Context recap**: 1–3 bullets of what was done this session.
- **Mission focus (next slice)**: The next concrete tasks.
- **Do / Don’t**: High-signal rules (do: read first/validate; don’t: move creds; don’t enable risky flags without approval).
- **If blocked**: Blocker + proposed fix + owner/ETA.
- **Checklist alignment**: CYCLE START / DURING / END quick reminders.
- **Optional commands**: e.g., validations/health checks the next operator should run.

---

## 📋 **PASSDOWN LOCATION**

**File**: `agent_workspaces/{agent_id}/passdown.json`

**When to Read**: At the start of every new session (after checking inbox and performing cleanup sweep)

**When to Write**: At the end of every session (after cleanup sweep, before transition)

**Purpose**: Handoff document containing:
- Completed missions and tasks
- Critical learnings
- Files created/modified
- Bugs fixed
- Next agent should know items
- Recommendations for next session
- Gas pipeline status
- Blockers

---

**Once complete, you'll receive fresh onboarding in new chat.**

