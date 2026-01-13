# Validation Execution Workflow

**Prepared By:** Agent-4 (Captain)  
**For Use By:** Agent-6 (Priority 3 Coordinator)  
**Date:** 2025-12-30  
**Status:** Ready for Execution When Agent-2 Completes

<!-- SSOT Domain: documentation -->

---

## Workflow Overview

Complete workflow from Agent-2 completion to validation execution to milestone generation. Use this document to understand the complete execution flow.

**Current Status:** Awaiting Agent-2 completion (30 files)  
**Workflow Status:** ✅ Ready - All materials prepared

---

## Workflow Steps

### Step 1: Agent-2 Completion Notification
**Trigger:** Agent-2 reports completion (30 files fixed)

**Actions:**
1. Receive Agent-2 completion notification
2. Verify completion details (files fixed, validation status)
3. Update progress tracker: 44/44 complete (100%)

**Reference:** `docs/SSOT/PHASE3_PROGRESS_TRACKER.md`

**Time:** 2-3 minutes

---

### Step 2: Quick Verification
**Trigger:** Agent-2 completion confirmed

**Actions:**
1. Use quick readiness check: `docs/SSOT/QUICK_VALIDATION_READINESS_CHECK.md`
2. Verify all prerequisites met (30 seconds)
3. Verify execution materials ready (15 seconds)
4. Verify validation tool ready (15 seconds)

**Reference:** `docs/SSOT/QUICK_VALIDATION_READINESS_CHECK.md`

**Time:** 1 minute

---

### Step 3: Execute Validation
**Trigger:** Quick verification complete

**Actions:**
1. Use command card: `docs/SSOT/VALIDATION_EXECUTION_COMMAND_CARD.md` (PRIMARY for commands)
2. Execute validation:
   - **Option A (Automated - Recommended):** `python tools/execute_final_validation_workflow.py` (complete workflow)
   - **Option B (Manual):** `python tools/execute_phase3_final_validation.py`
3. Monitor execution progress
4. Verify output files generated

**Reference:** 
- `docs/SSOT/VALIDATION_EXECUTION_COMMAND_CARD.md` (PRIMARY - copy-paste ready commands)
- `docs/SSOT/FINAL_VALIDATION_EXECUTION_GUIDE.md` (detailed guide with troubleshooting)

**Time:** 5-10 minutes

---

### Step 4: Verify Results
**Trigger:** Validation execution complete

**Actions:**
1. Check validation report: `docs/SSOT/FINAL_PHASE3_VALIDATION_REPORT.md`
2. Verify target: 1,369/1,369 files valid (100%)
3. Verify: 0 invalid files
4. Confirm: All domains at 100% compliance

**Reference:** `docs/SSOT/FINAL_PHASE3_VALIDATION_REPORT.md`

**Time:** 2-3 minutes

---

### Step 5: Generate Milestone
**Trigger:** Validation results verified (100% compliance)

**Actions:**
1. Populate milestone template: `docs/SSOT/PHASE1_THROUGH_PHASE3_COMPLETION_MILESTONE_TEMPLATE.md`
2. Update MASTER_TASK_LOG with completion status
3. Generate completion report
4. Notify CAPTAIN of milestone completion

**Reference:** `docs/SSOT/PHASE1_THROUGH_PHASE3_COMPLETION_MILESTONE_TEMPLATE.md`

**Time:** 10-15 minutes

---

## Workflow Decision Points

### Decision Point 1: Agent-2 Completion Status
- **If Complete:** Proceed to Step 2 (Quick Verification)
- **If In Progress:** Continue monitoring, update progress tracker
- **If Blocked:** Escalate to CAPTAIN, document blocker

### Decision Point 2: Validation Results
- **If 100% Compliance:** Proceed to Step 5 (Generate Milestone)
- **If <100% Compliance:** Review invalid files, coordinate remediation
- **If Validation Fails:** Review error logs, coordinate fix

---

## Reference Documents by Step

### Step 1: Agent-2 Completion
- Progress Tracker: `docs/SSOT/PHASE3_PROGRESS_TRACKER.md`
- Waiting Summary: `docs/SSOT/PHASE3_WAITING_ON_AGENT2_SUMMARY.md`

### Step 2: Quick Verification
- Quick Readiness Check: `docs/SSOT/QUICK_VALIDATION_READINESS_CHECK.md`
- Complete Readiness Report: `docs/SSOT/PHASE3_VALIDATION_EXECUTION_COMPLETE_READINESS_REPORT.md`

### Step 3: Execute Validation
- Command Card: `docs/SSOT/VALIDATION_EXECUTION_COMMAND_CARD.md` (PRIMARY for commands)
- Consolidated Guide: `docs/SSOT/FINAL_VALIDATION_EXECUTION_GUIDE.md` (PRIMARY for details)
- Agent-6 Readiness Summary: `docs/SSOT/AGENT6_VALIDATION_EXECUTION_READINESS_SUMMARY.md`

### Step 4: Verify Results
- Validation Report: `docs/SSOT/FINAL_PHASE3_VALIDATION_REPORT.md` (generated)
- Validation Report Template: `docs/SSOT/FINAL_PHASE3_VALIDATION_REPORT_TEMPLATE.md`

### Step 5: Generate Milestone
- Milestone Template: `docs/SSOT/PHASE1_THROUGH_PHASE3_COMPLETION_MILESTONE_TEMPLATE.md`
- MASTER_TASK_LOG: `MASTER_TASK_LOG.md`

---

## Timeline Estimate

**Total Workflow Time:** 20-35 minutes

- Step 1: Agent-2 Completion Notification (2-3 minutes)
- Step 2: Quick Verification (1 minute)
- Step 3: Execute Validation (5-10 minutes)
- Step 4: Verify Results (2-3 minutes)
- Step 5: Generate Milestone (10-15 minutes)

**Current Status:** Awaiting Agent-2 completion (30 files)

---

## Success Criteria

### Validation Execution Success
- ✅ All 44 files fixed and validated
- ✅ Validation tool executes successfully
- ✅ 1,369/1,369 files valid (100% compliance)
- ✅ 0 invalid files remaining
- ✅ All domains at 100% compliance

### Milestone Generation Success
- ✅ Milestone template populated
- ✅ MASTER_TASK_LOG updated
- ✅ Completion report generated
- ✅ CAPTAIN notified

---

**Status:** ✅ Workflow ready - All materials prepared, execution path clear  
**Blocking:** Agent-2 completion (30 files)  
**Ready:** Complete workflow prepared for immediate execution

