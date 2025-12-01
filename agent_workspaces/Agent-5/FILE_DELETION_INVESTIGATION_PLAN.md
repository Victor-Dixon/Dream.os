# 🔍 File Deletion Investigation Plan

**Created**: 2025-12-01 07:56:37  
**Agent**: Agent-5 (Business Intelligence Specialist)  
**Status**: INVESTIGATION REQUIRED - Automated findings need verification

---

## 🚨 IMPORTANT: INVESTIGATION FIRST

**⚠️ CRITICAL REMINDER**: The automated tool findings are **preliminary indicators only**. We must investigate thoroughly before deleting anything. Automated tools can have false positives.

---

## 📊 INVESTIGATION SCOPE

### Files Flagged for Investigation:
- **391 files** flagged as "unused" (not imported)
- **49 files** flagged as "duplicates"
- **3 files** with deletion markers
- **2 files** in deprecated directories

**Total**: 445 files requiring investigation

---

## 🔍 VERIFICATION CHECKLIST

### For Each File, Verify:

1. **Static Import Analysis** ✅ (Already checked)
   - Standard `import` statements
   - `from X import Y` statements

2. **Dynamic Imports** ❌ (NOT checked - false positive risk)
   - `importlib.import_module()`
   - `__import__()` calls
   - `exec()` or `eval()` with imports

3. **String-Based Imports** ❌ (NOT checked)
   - Import paths in strings
   - Config-driven imports
   - Plugin system imports

4. **Entry Points** ❌ (NOT checked)
   - CLI entry points (`__main__`, setup.py entry_points)
   - Script execution points
   - Direct file execution

5. **Test File References** ❌ (NOT checked)
   - Imported in test files
   - Referenced in test fixtures
   - Mocked or patched in tests

6. **Config References** ❌ (NOT checked)
   - Referenced in config files
   - YAML/JSON config imports
   - Environment variable references

7. **Documentation References** ❌ (NOT checked)
   - Mentioned in docs
   - Example code references
   - API documentation

8. **Runtime/Delayed Loading** ❌ (NOT checked)
   - Lazy imports
   - Conditional imports
   - Plugin loading systems

---

## 👥 AGENT ASSIGNMENTS

### Agent-2: Architecture & Design Specialist
**Assignment**: Investigate architecture-related files

**Files to Review**:
- `architecture/design_patterns.py`
- `architecture/system_integration.py`
- `architecture/unified_architecture_core.py`
- All files in `src/architecture/` directory

**Investigation Focus**:
- Are these reference/documentation files?
- Do they contain important architectural patterns?
- Are they imported dynamically or via config?
- Should they be kept as documentation even if unused?

**Deliverable**: Architecture files investigation report

---

### Agent-8: SSOT & System Integration Specialist
**Assignment**: Investigate duplicates and SSOT violations

**Files to Review**:
- All 49 duplicate files
- `config/ssot.py` (flagged as unused but might be SSOT-related)
- Files with deletion markers (3 files)

**Investigation Focus**:
- Which duplicate version should be kept?
- Are duplicates truly identical or have diverged?
- Can functionality be merged before deletion?
- Are deletion markers accurate and safe?

**Deliverable**: Duplicate resolution plan and SSOT verification report

---

### Agent-1: Integration & Core Systems Specialist
**Assignment**: Investigate core/system integration files

**Files to Review**:
- `core/agent_context_manager.py`
- `core/agent_documentation_service.py`
- `core/agent_lifecycle.py`
- `core/agent_notes_protocol.py`
- `core/agent_self_healing_system.py`
- All files in `src/core/` flagged as unused

**Investigation Focus**:
- Are these core systems that might be loaded dynamically?
- Do they have CLI entry points?
- Are they imported via plugin systems?
- Should they be kept for future use?

**Deliverable**: Core systems investigation report

---

### Agent-5: Business Intelligence Specialist
**Assignment**: Create enhanced verification tool and coordinate investigation

**Tasks**:
1. Create enhanced verification tool that checks:
   - Dynamic imports (`importlib`, `__import__`)
   - String-based imports
   - Config file references
   - Entry points (setup.py, __main__)
   - Test file references
   - CLI scripts

2. Categorize all 391 unused files by:
   - Directory/category
   - File type/function
   - Risk level (high/medium/low)

3. Coordinate with other agents
4. Create investigation reports template

**Deliverable**: Enhanced verification tool + categorized file list

---

### Agent-3: Infrastructure & DevOps Specialist
**Assignment**: Investigate infrastructure and automation files

**Files to Review**:
- `ai_automation/automation_engine.py`
- `ai_automation/utils/filesystem.py`
- `automation/ui_onboarding.py`
- All files in automation-related directories

**Investigation Focus**:
- Are these infrastructure scripts?
- Do they run as standalone tools?
- Are they called by CI/CD systems?
- Should they be kept for deployment?

**Deliverable**: Infrastructure files investigation report

---

### Agent-7: Web Development Specialist
**Assignment**: Investigate web/application-related files

**Files to Review**:
- `application/use_cases/assign_task_uc.py`
- `application/use_cases/complete_task_uc.py`
- All application/web-related unused files

**Investigation Focus**:
- Are these part of a web framework?
- Do they use dynamic routing?
- Are they loaded via application frameworks?
- Should they be integrated or deleted?

**Deliverable**: Application files investigation report

---

## 📋 INVESTIGATION WORKFLOW

### Phase 1: Enhanced Verification Tool (Agent-5)
**Duration**: 1-2 hours

1. Create tool that checks for:
   - Dynamic imports
   - String-based imports
   - Config references
   - Entry points
   - Test references

2. Run enhanced verification on all 391 files
3. Categorize findings by risk level
4. Generate detailed report

### Phase 2: Agent Investigations (All Agents)
**Duration**: 2-4 hours per agent

1. Each agent reviews assigned files
2. Checks for false positives
3. Verifies actual usage
4. Creates investigation report

### Phase 3: Review & Decision (Captain + All Agents)
**Duration**: 1 hour

1. Review all investigation reports
2. Make deletion decisions
3. Create final deletion plan
4. Get Captain approval

### Phase 4: Safe Deletion (Agent-8 + Agent-2)
**Duration**: 1-2 hours

1. Execute deletions in batches
2. Test after each batch
3. Verify nothing breaks
4. Document deletions

---

## 🛠️ ENHANCED VERIFICATION TOOL REQUIREMENTS

### Must Check:

1. **Dynamic Imports**
   ```python
   importlib.import_module('module.name')
   __import__('module.name')
   ```

2. **String-Based Imports**
   - Import paths in strings
   - Config file references
   - YAML/JSON configs

3. **Entry Points**
   - `setup.py` entry_points
   - `if __name__ == "__main__"`
   - CLI script definitions

4. **Test References**
   - Imported in test files
   - Referenced in fixtures
   - Mocked/patched

5. **Config Files**
   - Referenced in YAML/JSON/TOML
   - Environment variables
   - Settings files

6. **Documentation**
   - Mentioned in README/docs
   - Example code
   - API docs

---

## 📊 INVESTIGATION REPORTS TEMPLATE

Each agent should create a report with:

```markdown
# [Agent Name] - File Investigation Report

## Files Investigated: [Count]

### Category 1: [Category Name]
- File: `path/to/file.py`
- Status: ✅ SAFE TO DELETE | ⚠️ NEEDS REVIEW | ❌ KEEP
- Reason: [Explanation]
- False Positives Found: [Yes/No]

### Category 2: [Category Name]
...

## Summary
- Total Files: X
- Safe to Delete: Y
- Needs Review: Z
- Must Keep: W

## Recommendations
[Specific recommendations]
```

---

## ⚠️ SAFETY PROTOCOLS

### Before Any Deletion:

1. **Git Commit Current State**
   - Ensure all changes are committed
   - Create backup branch

2. **Run Enhanced Verification**
   - Use new verification tool
   - Check all false positive cases

3. **Agent Reviews Complete**
   - All agents have reviewed assigned files
   - All investigation reports submitted

4. **Captain Approval**
   - Captain reviews all findings
   - Approves deletion plan

5. **Delete in Batches**
   - Start with clearly safe files
   - Test after each batch
   - Verify nothing breaks

---

## 🎯 NEXT STEPS

### Immediate (Agent-5):
1. ✅ Create investigation plan (THIS DOCUMENT)
2. ⏭️ Create enhanced verification tool
3. ⏭️ Categorize all 391 files by risk level
4. ⏭️ Assign files to agents

### Short-Term (All Agents):
1. Review assigned files
2. Complete investigation reports
3. Submit findings

### Medium-Term (Captain + Agents):
1. Review all findings
2. Make deletion decisions
3. Execute safe deletions

---

## 📈 EXPECTED OUTCOMES

### Investigation May Reveal:
- **False Positives**: Files that ARE used but via dynamic imports
- **Legitimate Unused**: Files that are truly safe to delete
- **Need Integration**: Files that should be integrated before deletion
- **Keep for Reference**: Files with valuable code/patterns

### Revised Deletion Count:
- After investigation, deletion count may change
- We might keep some "unused" files if they have value
- We might find more files to delete after deeper analysis

---

**Created by**: Agent-5 (Business Intelligence Specialist)  
**Status**: ✅ INVESTIGATION PLAN READY  
**Next Step**: Create enhanced verification tool and assign files to agents

🐝 **WE. ARE. SWARM. ⚡🔥**

