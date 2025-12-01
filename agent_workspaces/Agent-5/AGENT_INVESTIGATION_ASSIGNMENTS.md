# 👥 Agent Investigation Assignments - File Deletion Verification

**Created**: 2025-12-01 07:56:37  
**Priority**: HIGH - Verification before deletion  
**Status**: ASSIGNMENTS READY

---

## 🚨 IMPORTANT: INVESTIGATION FIRST

The automated tool findings are **preliminary indicators only**. We must investigate thoroughly before deleting anything. Automated tools can have false positives.

---

## 📋 ASSIGNMENT OVERVIEW

### Files Requiring Investigation:
- **391 files** flagged as "unused"
- **49 files** flagged as "duplicates"
- **3 files** with deletion markers
- **2 files** in deprecated directories

**Total**: 445 files

---

## 👥 AGENT ASSIGNMENTS

### 🔍 Agent-2: Architecture & Design Specialist

**Assignment**: Investigate architecture-related files

**Files to Review** (from unused list):
- `architecture/design_patterns.py`
- `architecture/system_integration.py`
- `architecture/unified_architecture_core.py`
- All files in `src/architecture/` directory flagged as unused

**Investigation Focus**:
1. Are these reference/documentation files that should be kept?
2. Do they contain important architectural patterns?
3. Are they imported dynamically or via config?
4. Should they be kept as documentation even if unused?

**Tools to Use**:
- Enhanced verification tool: `tools/verify_file_usage_enhanced.py`
- Manual code review
- Documentation search

**Deliverable**: 
- File: `agent_workspaces/Agent-2/ARCHITECTURE_FILES_INVESTIGATION_REPORT.md`
- Due: Next session
- Format: See template below

---

### 🔍 Agent-8: SSOT & System Integration Specialist

**Assignment**: Investigate duplicates and SSOT violations

**Files to Review**:
- All 49 duplicate files from `unnecessary_files_analysis.json`
- `config/ssot.py` (flagged as unused but might be SSOT-related)
- Files with deletion markers (3 files)

**Investigation Focus**:
1. Which duplicate version should be kept?
2. Are duplicates truly identical or have diverged?
3. Can functionality be merged before deletion?
4. Are deletion markers accurate and safe?
5. Does `config/ssot.py` serve an SSOT purpose even if unused?

**Tools to Use**:
- Duplicate comparison tools
- SSOT verification tools
- Enhanced verification tool

**Deliverable**:
- File: `agent_workspaces/Agent-8/DUPLICATE_SSOT_INVESTIGATION_REPORT.md`
- Due: Next session
- Format: See template below

---

### 🔍 Agent-1: Integration & Core Systems Specialist

**Assignment**: Investigate core/system integration files

**Files to Review** (from unused list):
- `core/agent_context_manager.py`
- `core/agent_documentation_service.py`
- `core/agent_lifecycle.py`
- `core/agent_notes_protocol.py`
- `core/agent_self_healing_system.py`
- All files in `src/core/` flagged as unused

**Investigation Focus**:
1. Are these core systems that might be loaded dynamically?
2. Do they have CLI entry points?
3. Are they imported via plugin systems?
4. Should they be kept for future use?

**Tools to Use**:
- Enhanced verification tool
- CLI entry point checker
- Plugin system analyzer

**Deliverable**:
- File: `agent_workspaces/Agent-1/CORE_SYSTEMS_INVESTIGATION_REPORT.md`
- Due: Next session
- Format: See template below

---

### 🔍 Agent-3: Infrastructure & DevOps Specialist

**Assignment**: Investigate infrastructure and automation files

**Files to Review** (from unused list):
- `ai_automation/automation_engine.py`
- `ai_automation/utils/filesystem.py`
- `automation/ui_onboarding.py`
- All files in automation-related directories

**Investigation Focus**:
1. Are these infrastructure scripts that run standalone?
2. Do they run as standalone tools?
3. Are they called by CI/CD systems?
4. Should they be kept for deployment?

**Tools to Use**:
- Enhanced verification tool
- CI/CD config checker
- Entry point analyzer

**Deliverable**:
- File: `agent_workspaces/Agent-3/INFRASTRUCTURE_FILES_INVESTIGATION_REPORT.md`
- Due: Next session
- Format: See template below

---

### 🔍 Agent-7: Web Development Specialist

**Assignment**: Investigate web/application-related files

**Files to Review** (from unused list):
- `application/use_cases/assign_task_uc.py`
- `application/use_cases/complete_task_uc.py`
- All application/web-related unused files

**Investigation Focus**:
1. Are these part of a web framework?
2. Do they use dynamic routing?
3. Are they loaded via application frameworks?
4. Should they be integrated or deleted?

**Tools to Use**:
- Enhanced verification tool
- Web framework analyzer
- Route checker

**Deliverable**:
- File: `agent_workspaces/Agent-7/APPLICATION_FILES_INVESTIGATION_REPORT.md`
- Due: Next session
- Format: See template below

---

### 🔍 Agent-5: Business Intelligence Specialist

**Assignment**: Enhanced verification tool and coordination

**Tasks**:
1. ✅ Created enhanced verification tool
2. ⏭️ Run enhanced verification on all 391 unused files
3. ⏭️ Categorize files by risk level
4. ⏭️ Create investigation report templates
5. ⏭️ Coordinate with other agents

**Deliverable**:
- Enhanced verification results JSON
- Categorized file list by risk
- Investigation report template

---

## 📝 INVESTIGATION REPORT TEMPLATE

```markdown
# [Agent Name] - File Investigation Report

**Agent**: [Agent Name]  
**Date**: [Date]  
**Files Investigated**: [Count]

---

## EXECUTIVE SUMMARY

- Total Files Reviewed: X
- Safe to Delete: Y
- Needs Review: Z
- Must Keep: W

---

## FILES BY CATEGORY

### Category 1: [Category Name]

#### File: `path/to/file.py`
- **Status**: ✅ SAFE_TO_DELETE | ⚠️ NEEDS_REVIEW | ❌ KEEP
- **Module Name**: `module.name`
- **Reason**: [Detailed explanation]
- **False Positives Found**: Yes/No
- **Details**: 
  - Dynamic imports detected: [Yes/No, details]
  - Entry points: [Yes/No, details]
  - Test references: [Yes/No, details]
  - Config references: [Yes/No, details]
  - Documentation references: [Yes/No, details]
- **Recommendation**: [Specific recommendation]

[Repeat for each file...]

---

## SUMMARY

### Safe to Delete: [Count]
[List files]

### Needs Review: [Count]
[List files with reasons]

### Must Keep: [Count]
[List files with reasons]

---

## RECOMMENDATIONS

1. [Specific recommendation 1]
2. [Specific recommendation 2]
...

---

## NEXT STEPS

1. [Action item 1]
2. [Action item 2]
...
```

---

## 🛠️ TOOLS PROVIDED

### Enhanced Verification Tool
**Location**: `tools/verify_file_usage_enhanced.py`

**Usage**:
```bash
# Verify all files from analysis
python tools/verify_file_usage_enhanced.py

# Custom analysis file
python tools/verify_file_usage_enhanced.py --analysis-file path/to/analysis.json

# Custom output
python tools/verify_file_usage_enhanced.py --output path/to/results.json
```

**What It Checks**:
- Dynamic imports (`importlib`, `__import__`)
- Entry points (`__main__`, setup.py)
- Test file references
- Config file references
- Documentation references

---

## ⏰ TIMELINE

### Immediate (This Session):
- ✅ Investigation plan created
- ✅ Enhanced verification tool created
- ✅ Agent assignments created

### Next Session (2-4 hours):
- All agents review assigned files
- Complete investigation reports
- Submit findings

### Following Session (1 hour):
- Review all findings
- Make deletion decisions
- Create final deletion plan

---

## 📊 SUCCESS CRITERIA

### Investigation Complete When:
- ✅ All agents have submitted investigation reports
- ✅ All files have been reviewed
- ✅ False positives identified and documented
- ✅ Recommendations made for each file
- ✅ Captain has reviewed all findings

### Deletion Safe When:
- ✅ Enhanced verification completed
- ✅ All agent reviews submitted
- ✅ No high-risk files flagged for deletion
- ✅ Captain approval received
- ✅ Batch deletion plan approved

---

**Created by**: Agent-5 (Business Intelligence Specialist)  
**Status**: ✅ ASSIGNMENTS READY - WAITING FOR AGENT INVESTIGATIONS  
**Next Step**: Message agents with assignments

🐝 **WE. ARE. SWARM. ⚡🔥**

