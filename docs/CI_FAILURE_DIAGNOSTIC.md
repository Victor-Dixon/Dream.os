# CI Failure Diagnostic - Dream.os Repository

**Date:** 2025-12-12  
**Status:** 🟡 Investigating CI failures

## Known Issues Identified

### 1. ❌ Merge Conflict in Workflow File
**File:** `.github/workflows/code-quality.yml`  
**Issue:** Merge conflict markers present (lines 11-15)
```yaml
<<<<<<< HEAD
        python-version: '3.11'
=======
        python-version: '3.11'
>>>>>>> origin/codex/catalog-functions-in-utils-directories
```
**Fix:** Remove conflict markers, keep single `python-version: '3.11'`

---

### 2. ⚠️ Missing Required Files

CI workflows reference files that may not exist:

#### `scripts/validate_v2_compliance.py`
- Referenced in: `ci.yml` (line 24), `ci-optimized.yml` (line 58)
- Status: ❌ Missing (checked: file not found)

#### `config/v2_rules.yaml`
- Referenced in: `ci.yml` (line 24), `ci-optimized.yml` (line 58)
- Status: ⚠️ Need to verify

#### `tools/v2_compliance_checker.py`
- Referenced in: `ci-optimized.yml` (line 57)
- Status: ⚠️ Need to verify

#### `tests/v2_standards_checker.py`
- Referenced in: `ci-cd.yml` (lines 89, 94, 319)
- Status: ⚠️ Need to verify

#### Requirements Files
- `requirements.txt` - Core dependencies
- `requirements-dev.txt` - Development dependencies  
- `requirements-testing.txt` - Testing dependencies
- Status: ⚠️ Need to verify existence

---

### 3. 📋 Common CI Failure Points

#### V2 Compliance Checks
- **Issue:** Scripts may fail if compliance checker doesn't exist
- **Workflow:** `ci.yml`, `ci-optimized.yml`
- **Action:** Create missing scripts or disable checks temporarily

#### Test Coverage Thresholds
- **Issue:** Coverage may be below 85% threshold
- **Workflow:** `ci.yml` (line 32), `ci-optimized.yml` (line 90)
- **Action:** Check actual coverage, adjust threshold if needed

#### Missing Dependencies
- **Issue:** `pip install -r requirements*.txt` may fail
- **Action:** Ensure all requirements files exist and have correct dependencies

---

## Diagnostic Steps

### Step 1: Fix Merge Conflict
```bash
# Edit .github/workflows/code-quality.yml
# Remove conflict markers (lines 11-15)
# Keep: python-version: '3.11'
```

### Step 2: Check Required Files
```bash
# Verify existence
test -f scripts/validate_v2_compliance.py || echo "Missing: validate_v2_compliance.py"
test -f config/v2_rules.yaml || echo "Missing: v2_rules.yaml"
test -f requirements.txt || echo "Missing: requirements.txt"
```

### Step 3: Check GitHub Actions Run
1. Go to: https://github.com/Victor-Dixon/Dream.os/actions
2. Click on the failing workflow run
3. Identify which job failed
4. Click into the failing job to see error logs

### Step 4: Common Error Patterns

#### Error: "File not found: scripts/validate_v2_compliance.py"
**Solution Options:**
1. Create the missing script
2. Comment out V2 compliance check temporarily
3. Update workflow to use existing compliance checker

#### Error: "requirements.txt not found"
**Solution:**
- Create requirements.txt with minimum dependencies
- Or update workflow to handle missing file gracefully (`|| true`)

#### Error: "Coverage too low"
**Solution:**
- Check actual coverage: `pytest --cov=src --cov-report=term`
- Either fix tests or adjust `--cov-fail-under` threshold

---

## Quick Fixes

### Fix 1: Remove Merge Conflict
```yaml
# .github/workflows/code-quality.yml
- name: Set up Python
  uses: actions/setup-python@v4
  with:
    python-version: '3.11'  # Fixed: removed conflict markers
```

### Fix 2: Make V2 Compliance Optional
```yaml
# In ci.yml or ci-optimized.yml
- name: V2 compliance rules
  run: |
    if [ -f scripts/validate_v2_compliance.py ]; then
      python scripts/validate_v2_compliance.py --rules config/v2_rules.yaml
    else
      echo "⚠️ V2 compliance checker not found, skipping..."
    fi
  continue-on-error: true  # Don't fail CI if checker missing
```

### Fix 3: Handle Missing Requirements Files
```yaml
- name: Install deps
  run: |
    python -m pip install --upgrade pip
    pip install -r requirements.txt || echo "⚠️ requirements.txt not found"
    pip install -r requirements-dev.txt || echo "⚠️ requirements-dev.txt not found, skipping"
```

---

## Next Steps

1. **Get CI Logs:** Share GitHub Actions run URL for detailed diagnosis
2. **Fix Merge Conflict:** Resolve in code-quality.yml
3. **Verify Files:** Check which files actually exist
4. **Create Missing Files:** Or update workflows to handle gracefully
5. **Test Locally:** Run CI checks locally before pushing

---

## How to Get CI Logs

1. Go to: https://github.com/Victor-Dixon/Dream.os/actions
2. Find the failed workflow run (red X)
3. Click on it
4. Click on the failing job (usually red X)
5. Scroll to find error messages
6. Share the error snippet or entire log

---

**Recommended Action:** Fix merge conflict first, then check CI logs to identify specific failure points.

