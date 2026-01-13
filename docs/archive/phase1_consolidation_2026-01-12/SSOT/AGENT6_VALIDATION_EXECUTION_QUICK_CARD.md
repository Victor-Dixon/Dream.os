# Agent-6 Validation Execution Quick Card

**For:** Agent-6 (Priority 3 Coordinator)  
**When:** Agent-2 completes (30 files)  
**Status:** ✅ Ready for Immediate Execution  
**Last Updated:** 2025-12-31 00:30 UTC

<!-- SSOT Domain: documentation -->

---

## 🚀 Quick Execution (20-35 minutes)

### Step 1: Quick Verification (1 minute)
```bash
# Check progress tracker
cat docs/SSOT/PHASE3_PROGRESS_TRACKER.md | grep "44/44 complete"
```

**Expected:** `44/44 files complete (100%)`

### Step 2: Execute Validation (5-10 minutes)

**Option A: Automated Workflow (RECOMMENDED - PRIMARY)**
```bash
# Complete workflow automation
python tools/execute_final_validation_workflow.py

# OR skip verification for faster execution
python tools/execute_final_validation_workflow.py --skip-verification
```

**Option B: Manual Execution**
```bash
# Use command card for manual steps
# See: docs/SSOT/VALIDATION_EXECUTION_COMMAND_CARD.md
python tools/execute_phase3_final_validation.py
```

**Expected Output:**
- JSON report: `docs/SSOT/FINAL_PHASE3_VALIDATION_REPORT.json`
- Markdown report: `docs/SSOT/FINAL_PHASE3_VALIDATION_REPORT.md`
- Target: **1,369/1,369 files valid (100%)**

### Step 3: Verify Results (2-3 minutes)
```bash
# Check validation results
cat docs/SSOT/FINAL_PHASE3_VALIDATION_REPORT.md | grep "Total files valid"
```

**Expected:** `Total files valid: 1,369/1,369 (100.0%)`

### Step 4: Generate Milestone (10-15 minutes)
- Use: `docs/SSOT/PHASE1_THROUGH_PHASE3_COMPLETION_MILESTONE_TEMPLATE.md`
- Populate with validation results
- Update: MASTER_TASK_LOG

**Total Time:** 20-35 minutes (automated) OR 20-35 minutes (manual)

---

## 📋 Primary References

### For Execution
1. **Decision Tree:** `docs/SSOT/FINAL_VALIDATION_EXECUTION_DECISION_TREE.md` (PRIMARY for path selection - choose execution path)
2. **Workflow:** `docs/SSOT/VALIDATION_EXECUTION_WORKFLOW.md` (PRIMARY for workflow - complete execution flow)
3. **Command Card:** `docs/SSOT/VALIDATION_EXECUTION_COMMAND_CARD.md` (PRIMARY for commands - copy-paste ready)
4. **Consolidated Guide:** `docs/SSOT/FINAL_VALIDATION_EXECUTION_GUIDE.md` (PRIMARY - all checklists combined)

### For Status
4. **Status Document:** `docs/SSOT/VALIDATION_EXECUTION_STATUS.md` (PRIMARY for status - real-time tracking)
5. **Readiness Verification:** `docs/SSOT/FINAL_VALIDATION_EXECUTION_READINESS_VERIFICATION.md` (complete verification checklist)

### For Quick Checks
6. **Quick Readiness Check:** `docs/SSOT/QUICK_VALIDATION_READINESS_CHECK.md` (one-minute verification)
7. **Agent-6 Summary:** `docs/SSOT/AGENT6_VALIDATION_EXECUTION_READINESS_SUMMARY.md` (single-page reference)

---

## ✅ Prerequisites Checklist

- [ ] Agent-2 completion (30 files) - **BLOCKING**
- [ ] Progress tracker: 44/44 complete
- [ ] All domain owners confirmed

**Current Status:** 14/44 files complete (31.8%)  
**Remaining:** 30 files (Agent-2, in progress)  
**Blocking:** Agent-2 completion required

---

## 🎯 Execution Readiness

**Materials Prepared:** ✅ 21/21 verified  
**Cross-References:** ✅ All verified  
**Execution Paths:** ✅ Both automated and manual ready  
**Tools:** ✅ All ready  
**Blocking:** ⏳ Agent-2 completion (30 files)

**Overall Readiness:** ✅ 100% Ready (blocked only by Agent-2 completion)

---

## 📊 Current Progress

**Completed Owners:**
- ✅ Agent-1: 3 files (Integration) - Confirmed 23:06 UTC
- ✅ Agent-3: 7 files (Infrastructure, Safety, Logging) - Confirmed 22:54 UTC
- ✅ Agent-5: 2 files (Data, Trading Robot) - Confirmed
- ✅ Agent-6: 1 file (Discord) - Confirmed
- ✅ Agent-8: 1 file (Validation) - Confirmed

**In Progress:**
- ⏳ Agent-2: 30 files (Core 29, Domain 1) - Status check-in sent, awaiting response

**Total:** 14/44 files complete (31.8%)

---

## 🔧 Automation Tools

### Workflow Automation (PRIMARY)
- **Script:** `tools/execute_final_validation_workflow.py`
- **Functionality:** Complete workflow (verify → validate → report → milestone)
- **Usage:** `python tools/execute_final_validation_workflow.py [--skip-verification]`

### Validation Automation
- **Script:** `tools/execute_phase3_final_validation.py`
- **Functionality:** Validation execution only
- **Usage:** `python tools/execute_phase3_final_validation.py`

### Readiness Verification
- **Script:** `tools/verify_final_validation_readiness.py`
- **Functionality:** Automated prerequisite checking
- **Usage:** `python tools/verify_final_validation_readiness.py`

---

## 📝 Success Criteria

**Validation Success:**
- ✅ 1,369/1,369 files valid (100%)
- ✅ 0 invalid files
- ✅ All domains recognized
- ✅ All SSOT tags valid

**Milestone Completion:**
- ✅ Validation report generated
- ✅ Completion milestone populated
- ✅ MASTER_TASK_LOG updated
- ✅ All materials documented

---

**Status:** ✅ Complete Readiness - All 18 materials prepared, cross-referenced, and ready for immediate execution when Agent-2 completes

