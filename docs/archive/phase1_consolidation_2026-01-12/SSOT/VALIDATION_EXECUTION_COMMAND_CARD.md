# Validation Execution Command Card

**Prepared By:** Agent-4 (Captain)  
**For Use By:** Agent-6 (Priority 3 Coordinator)  
**Date:** 2025-12-30  
**Status:** Ready for Use When Agent-2 Completes

<!-- SSOT Domain: documentation -->

---

## Quick Execution (Copy-Paste Ready)

### Step 1: Verify Completion (30 seconds)
```bash
# Check progress tracker
cat docs/SSOT/PHASE3_PROGRESS_TRACKER.md | grep "44/44 complete"
```

### Step 2: Execute Validation (PRIMARY PATH)
```bash
# Option A: Complete workflow automation (RECOMMENDED - PRIMARY)
python tools/execute_final_validation_workflow.py
# OR skip verification:
python tools/execute_final_validation_workflow.py --skip-verification

# Option B: Manual validation execution
python tools/execute_phase3_final_validation.py
```

**Expected Output:**
- JSON report: `docs/SSOT/FINAL_PHASE3_VALIDATION_REPORT.json`
- Markdown report: `docs/SSOT/FINAL_PHASE3_VALIDATION_REPORT.md`
- Target: 1,369/1,369 files valid (100%)

### Step 3: Verify Results (15 seconds)
```bash
# Check validation results
cat docs/SSOT/FINAL_PHASE3_VALIDATION_REPORT.md | grep "Total files valid"
```

**Expected:** `Total files valid: 1,369/1,369 (100.0%)`

---

## Alternative: Manual Execution

If automation script unavailable:

```bash
# Run validation tool
python tools/validate_all_ssot_files.py > docs/SSOT/FINAL_PHASE3_VALIDATION_REPORT.json 2>&1

# Generate markdown report
python tools/populate_validation_report.py
```

---

## Reference Documents

- **PRIMARY:** `docs/SSOT/FINAL_VALIDATION_EXECUTION_GUIDE.md` (consolidated guide)
- **Complete Readiness:** `docs/SSOT/PHASE3_VALIDATION_EXECUTION_COMPLETE_READINESS_REPORT.md`
- **Quick Check:** `docs/SSOT/QUICK_VALIDATION_READINESS_CHECK.md`
- **Agent-6 Summary:** `docs/SSOT/AGENT6_VALIDATION_EXECUTION_READINESS_SUMMARY.md`

---

**Status:** Ready for execution when Agent-2 completes (30 files)

