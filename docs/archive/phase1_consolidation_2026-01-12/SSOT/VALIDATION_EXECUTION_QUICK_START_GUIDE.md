# Validation Execution Quick Start Guide

<!-- SSOT Domain: documentation -->

**Purpose:** Single-page quick start guide for Agent-6 - consolidates all validation execution materials into immediate action steps when Agent-2 completes Phase 3 (30 files).

**Last Updated:** 2025-12-31  
**Status:** ✅ READY - Use this guide the moment Agent-2 reports completion

---

## Immediate Actions (When Agent-2 Reports Completion)

### Step 1: Verify Completion (1 minute)
```bash
# Check progress tracker
cat docs/SSOT/PHASE3_PROGRESS_TRACKER.md | grep "44/44 complete"
```

**Expected:** "44/44 files complete (100%)"

### Step 2: Run Final Readiness Check (2 minutes)
```bash
python tools/verify_final_validation_readiness.py
```

**Expected:** All checks pass ✅

### Step 3: Execute Validation (30-45 minutes)
```bash
# Automated path (PRIMARY - RECOMMENDED)
python tools/execute_final_validation_workflow.py

# OR skip verification for faster execution
python tools/execute_final_validation_workflow.py --skip-verification
```

**What it does:**
- ✅ Verifies prerequisites
- ✅ Executes validation tool
- ✅ Generates JSON report
- ✅ Populates validation report
- ✅ Generates completion milestone template

### Step 4: Verify Results (2 minutes)
```bash
# Check validation results
cat docs/SSOT/FINAL_PHASE3_VALIDATION_REPORT.md | grep "Total files valid"
```

**Expected:** "Total files valid: 1,369/1,369 (100.0%)"

### Step 5: Notify CAPTAIN
```bash
python -m src.services.messaging_cli --agent Agent-4 \
  --message "Phase 3 Final Validation COMPLETE ✅: [1,369/1,369 files valid (100%)], milestone template generated, MASTER_TASK_LOG update ready" \
  --category a2a --sender Agent-6 --tags validation-complete
```

---

## Success Criteria

### Validation Success
- ✅ **Target:** 100% compliance (1,369/1,369 files valid)
- ✅ **Current Baseline:** 95.62% (1,309/1,369 files valid - Phase 2)
- ✅ **Phase 3 Target:** Fix all 60 invalid files → 100% compliance

### Execution Success
- ✅ Validation tool executes without errors
- ✅ JSON report generated (`FINAL_PHASE3_VALIDATION_REPORT.json`)
- ✅ Validation report populated (`FINAL_PHASE3_VALIDATION_REPORT.md`)
- ✅ Completion milestone generated
- ✅ MASTER_TASK_LOG updated

---

## Quick Reference Links

### For Immediate Execution
- **Signal Handler:** `AGENT2_COMPLETION_SIGNAL_HANDLER.md` (complete action plan)
- **Complete Checklist:** `VALIDATION_EXECUTION_COMPLETE_CHECKLIST.md` (go/no-go)
- **Final Readiness:** `VALIDATION_EXECUTION_FINAL_READINESS_VERIFICATION.md` (pre-execution)
- **Status Dashboard:** `VALIDATION_EXECUTION_STATUS_DASHBOARD.md` (track progress)

### For Path Selection
- **Decision Tree:** `FINAL_VALIDATION_EXECUTION_DECISION_TREE.md` (choose path)

### For Complete Details
- **Workflow Automation:** `tools/execute_final_validation_workflow.py` (PRIMARY)
- **Consolidated Guide:** `FINAL_VALIDATION_EXECUTION_GUIDE.md` (manual fallback)
- **Command Card:** `VALIDATION_EXECUTION_COMMAND_CARD.md` (copy-paste commands)

---

## Communication Protocol

### When Validation Starts
```bash
python -m src.services.messaging_cli --agent Agent-4 \
  --message "Phase 3 Final Validation EXECUTING: Agent-2 completion verified ✅, validation execution started, ETA 30-45 minutes" \
  --category a2a --sender Agent-6 --tags validation-execution
```

### If Blocked
```bash
python -m src.services.messaging_cli --agent Agent-4 \
  --message "Phase 3 Final Validation BLOCKED: [specific issue], proposed solution: [solution]" \
  --category a2a --sender Agent-6 --tags validation-blocked
```

---

## Current Status

### Phase 3 Completion
- **Agent-2:** ⏳ IN PROGRESS (30 files: Core 29, Domain 1)
- **Total Files:** 44 files
- **Completed:** 14/44 (31.8%)
- **Remaining:** 30 files (Agent-2)

### Validation Readiness
- **Prerequisites:** ⏳ Agent-2 completion required
- **Materials:** ✅ ALL PREPARED (26+ documents)
- **Automation:** ✅ ALL READY (2 scripts)
- **Execution Path:** ✅ READY (automated + manual)

---

## Execution Timeline

- **Verification:** 2-3 minutes
- **Validation:** 30-45 minutes (automated) OR 45-60 minutes (manual)
- **Results Verification:** 2 minutes
- **Notification:** 1 minute
- **Total:** 35-51 minutes (automated) OR 50-66 minutes (manual)

---

## Troubleshooting

### If Prerequisites Not Met
1. Check Phase 3 progress tracker
2. Verify Agent-2 completion
3. Run readiness verification: `python tools/verify_final_validation_readiness.py`
4. Fix any identified issues

### If Automated Workflow Fails
1. Check error message
2. Run readiness verification
3. Fix issues OR switch to manual path
4. Reference: `FINAL_VALIDATION_EXECUTION_GUIDE.md`

---

## Next Steps After Completion

1. ✅ Verify validation results (100% compliance target)
2. ✅ Generate completion milestone
3. ✅ Update MASTER_TASK_LOG
4. ✅ Notify CAPTAIN of completion
5. ✅ Update status dashboard

---

**Status:** ✅ Quick Start Guide Ready - Use this guide the moment Agent-2 reports completion for immediate validation execution.

**Reference:** See `PHASE3_COORDINATION_MASTER_INDEX.md` for complete materials index (26+ documents).

