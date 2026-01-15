=======
<!-- SSOT Domain: documentation -->

# Canon Automation: For Agents

**Version**: 1.0
**Date**: 2025-12-22
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
**Audience**: All Swarm Members (Agent-1 through Agent-8)

---

## What You Need to Know

A **canon automation system** has been created that automatically extracts canon-worthy events from your work cycles.

**Your work is now automatically considered for canon.**

---

## What You Need to Do

**Nothing new.**

Just keep doing what you're already doing:
* Update `status.json` with completed tasks
* Mark contracts as "✅ COMPLETE" when done
* Add achievements when you hit milestones
* Report coordination activities in your status

**The system automatically finds these and considers them for canon.**

---

## How It Works (For You)

1. **You work** → Complete tasks, finish contracts, achieve milestones
2. **You update status.json** → Mark things complete, add achievements
3. **Automation runs** → System scans your status.json files
4. **Candidates generated** → Your work is considered for canon
5. **Victor reviews** → Acknowledges canon-worthy events
6. **Thea declares** → Makes it official canon

**You just keep working. The system handles the rest.**

---

## What Gets Extracted From Your Work

### Contract Completions

When you complete a contract and mark it "✅ COMPLETE" in `contract_status`:
* Contract name
* Deliverables you created
* Results/outcomes
* Timestamp

**Example**: Agent-8 completes "Fix Consolidated Imports" → Canon candidate

### Achievements

When you add achievements to your `status.json`:
* Achievement description
* Significance
* Timestamp

**Example**: Agent-8 "SSOT domain mapping complete - 32 domains defined" → Canon candidate

### Major Task Completions

When you mark tasks as complete in `completed_tasks`:
* Task name
* Details/results
* Timestamp

**Example**: Agent-8 "Fixed 12 import conflicts across 6 files" → Potential canon

### Coordination Activities

When you report coordination in `current_tasks` or `next_actions`:
* Coordination type
* Participants
* Outcome
* Timestamp

**Example**: Agent-8 "A2A coordination accepted" → Potential canon

---

## Authority Separation (Still Applies)

**You (The Swarm):**
* Execute missions
* Report outcomes
* Update system state

**Victor:**
* Sets direction
* Approves priorities
* Makes final decisions
* Acknowledges canon-worthy events

**Thea:**
* Synthesizes outcomes
* Maintains narrative continuity
* Declares canon after execution
* Reflects system health

**Automation:**
* Extracts events from your work
* Structures them for review
* Generates candidates

**No authority bleeds. You still execute. Victor still decides. Thea still declares.**

---

## The One-Line Rule

> **If Victor hasn't chosen it, it's not a command.  
> If the Swarm hasn't built it, it's not canon.  
> If Thea hasn't named it, it's not integrated.**

**Automation extracts. Victor acknowledges. Thea declares.**

You still execute. Automation just helps find what's canon-worthy.

---

## Benefits For You

**What This Means:**
* Your work is automatically considered for canon
* You don't have to manually report everything
* Your achievements get narrative weight automatically
* You'll understand why your work matters

**What You Still Do:**
* Keep `status.json` updated (you're already doing this)
* Mark tasks as complete when done
* Add achievements for milestones
* Report coordination activities

**Nothing changes in your workflow. The system just helps.**

---

## Example: How Your Work Becomes Canon

1. **You complete a contract** → Update `contract_status.status = "✅ COMPLETE"`
2. **Automation runs** → Finds your completed contract
3. **Candidate generated** → "Agent-X completed Contract Y"
4. **Victor reviews** → "Yes, this is canon-worthy"
5. **Thea declares** → "Canon Event: Contract Y Completion"
6. **Timeline updated** → Added to CANON_EVENTS.md
7. **Blog post** → If significant, becomes narrative

**Your work → Canon. Automatically.**

---

## Where to Find More Info

* **Protocol**: `digitaldreamscape.site/docs/CANON_AUTOMATION_PROTOCOL.md`
* **Quick Start**: `digitaldreamscape.site/docs/CANON_AUTOMATION_QUICK_START.md`
* **Tool**: `tools/canon_automation.py`
* **Blog Post**: `digitaldreamscape.site/blog/005-automating-canon.md`
* **Announcement**: `agent_workspaces/CANON_AUTOMATION_ANNOUNCEMENT.md`

---

## First Extraction Results

**Initial run (2025-12-22):**
* 32 events found across all agents
* 19 candidates generated for Victor's review
* 7 agents scanned

**Your work is already being considered for canon.**

---

## Questions?

**Q: Do I need to do anything different?**  
A: No. Just keep updating status.json as you already do.

**Q: Will automation assign me tasks?**  
A: No. Automation only extracts. Victor still assigns tasks.

**Q: Can I request something be canon?**  
A: Automation will find it if it's in your status.json. Victor still decides.

**Q: What if I don't want something to be canon?**  
A: Victor reviews all candidates. You can discuss in coordination messages.

**Q: How often does extraction run?**  
A: Can be scheduled (daily/weekly) or run on-demand.

---

**This is a system update. This is operational.**

*Part of the Digital Dreamscape canon automation system*

