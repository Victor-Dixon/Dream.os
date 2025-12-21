# messaging_template_texts.py Growth Analysis

**Date:** 2025-12-15  
**File:** `src/core/messaging_template_texts.py`  
**Status:** ⚠️ **NOT V2 COMPLIANT** (exceeds exception limit)

---

## 📊 Growth Summary

| Metric | Value |
|--------|-------|
| **Original Size (Dec 9, 2025)** | 534 lines ✅ (approved exception) |
| **Current Size** | 1,486 lines ❌ |
| **Growth** | +952 lines (+178%) |
| **V2 Limit** | 300 lines |
| **Exception Limit** | 400 lines (general) / 534 lines (approved) |
| **Current Violation** | 1,186 lines over exception limit |

---

## 🔍 Root Cause Analysis

### Timeline of Growth

**Base State (Dec 9, 2025):**
- Commit: `8aeb5bb10` - "refactor: Split messaging models from templates/text to restore V2 compliance"
- Size: **535 lines** ✅
- Status: Approved exception (534 lines)

**Major Growth Periods:**

#### 1. **Swarm Coordination Enhancements (Dec 12, 2025)**
- **Commit:** `c5062ebd7` - "feat: Enhance S2A template to strongly emphasize swarm coordination"
- **Added:** +72 lines
- **Impact:** Expanded STALL_RECOVERY template with:
  - Coordination mandate sections
  - Force multiplier assessment
  - Quick delegation decision framework
  - Daily coordination check metrics
  - 4 concrete coordination examples

#### 2. **Bilateral Coordination & Operating Cycle (Dec 14, 2025)**
- **Commit:** `7a73f110d` - "feat: Enhance C2A and A2A/A2C templates with bilateral coordination and operating cycle"
- **Added:** +269 lines (net)
- **Impact:** Major expansion of C2A template:
  - Mandatory 7-step operating cycle
  - Comprehensive bilateral coordination protocol
  - Swarm force multiplier assessment
  - Architecture search and anti-duplication protocol
  - Technical debt prevention measures

#### 3. **Risk Assessment Protocols (Dec 14, 2025)**
- **Commit:** `6a4cb69c8` - "feat: Add proactive risk assessment and mid-cycle re-assessment to C2A/A2A templates"
- **Added:** +71 lines
- **Impact:** Added:
  - Proactive Risk Assessment Protocol (after SYNC, before SLICE)
  - Mid-Cycle Re-Assessment Protocol (after EXECUTE, before VALIDATE)
  - Technical, scope, coordination, and quality risk categories
  - Mitigation strategies framework

#### 4. **Additional Enhancements**
- **Commit:** `a6140e0ba` - "feat(Agent-3): Strengthen S2A template coordination messaging"
- **Commit:** `9230006da` - "feat(Agent-3): Strengthen S2A template quick delegation section"
- **Commit:** `fa71c21a7` - "fix: Add missing risk assessment and re-assessment sections to C2A template"

---

## 📐 Content Breakdown

### Major Components (Current File)

1. **Constants Section** (~280 lines):
   - `AGENT_OPERATING_CYCLE_TEXT` (~10 lines)
   - `CYCLE_CHECKLIST_TEXT` (~69 lines) - **Expanded with Force Multiplier Assessment**
   - `SWARM_COORDINATION_TEXT` (~113 lines) - **Very long protocol text**
   - `DISCORD_REPORTING_TEXT` (~40 lines)
   - `D2A_RESPONSE_POLICY_TEXT` (~6 lines)
   - `D2A_REPORT_FORMAT_TEXT` (~6 lines)

2. **MESSAGE_TEMPLATES Dictionary** (~1,100 lines):
   - **S2A Templates** (~475 lines):
     - `CONTROL` (~30 lines)
     - `STALL_RECOVERY` (~141 lines) - **Massively expanded**
     - `HARD_ONBOARDING` (~15 lines)
     - `SOFT_ONBOARDING` (~25 lines)
     - `PASSDOWN` (~15 lines)
     - `TELEPHONE_STATUS_GAME` (~15 lines)
     - `TASK_CYCLE` (~15 lines)
     - `FSM_UPDATE` (~15 lines)
     - `DEBATE_CYCLE` (~15 lines)
     - `CYCLE_V2` (~100 lines) - **Large template**
   
   - **D2A Templates** (~25 lines)
   - **C2A Templates** (~280 lines) - **Massively expanded with:**
     - Operating cycle integration
     - Bilateral coordination protocol
     - Risk assessment protocols
     - Swarm force multiplier assessment
   
   - **A2A Templates** (~63 lines) - **Enhanced with coordination protocols**

3. **Helper Functions** (~40 lines):
   - `format_d2a_payload()`
   - `format_s2a_message()`

---

## 🎯 Key Growth Drivers

### 1. **Swarm Coordination Emphasis** (+~200 lines)
- Multiple commits focused on making coordination the default behavior
- Added extensive coordination protocols, examples, and enforcement mechanisms
- Expanded STALL_RECOVERY template from ~30 lines to ~141 lines

### 2. **Template Enhancements** (+~400 lines)
- C2A template expanded significantly with:
  - Operating cycle integration
  - Bilateral coordination protocols
  - Risk assessment frameworks
  - Architecture search protocols

### 3. **Protocol Documentation** (+~350 lines)
- Long-form protocol text in constants (SWARM_COORDINATION_TEXT, CYCLE_CHECKLIST_TEXT)
- Detailed examples and workflows embedded in templates
- Comprehensive guidance text for agents

---

## ⚠️ Compliance Status

### V2 Compliance Check

| Rule | Limit | Current | Status |
|------|-------|---------|--------|
| **File Size** | 300 lines | 1,486 lines | ❌ **VIOLATION** |
| **Exception Limit** | 400 lines | 1,486 lines | ❌ **VIOLATION** |
| **Approved Exception** | 534 lines | 1,486 lines | ❌ **EXCEEDED** |

### Exception Status

- **On Exceptions List:** ✅ Yes (line 100, 153-167 in `V2_COMPLIANCE_EXCEPTIONS.md`)
- **Approved Size:** 534 lines
- **Current Size:** 1,486 lines
- **Over Approved Limit:** +952 lines (+178%)

**Conclusion:** File is **NOT V2 compliant**. Even though it's on the exceptions list, it has exceeded the approved exception size by 952 lines.

---

## 🔧 Recommended Actions

### Immediate Actions

1. **Update Exception Documentation**
   - Update `V2_COMPLIANCE_EXCEPTIONS.md` to reflect current size (1,486 lines)
   - OR remove from exceptions list if refactoring is planned

2. **Execute Refactoring Plan**
   - Follow plan in `docs/architecture/MESSAGING_TEMPLATE_TEXTS_REFACTORING_PLAN_2025-12-14.md`
   - Split into modular files (<300 lines each)
   - Maintain backward compatibility via shim

### Refactoring Strategy

**Target Structure:**
```
src/core/messaging_templates/
├── __init__.py (~50 lines)
├── constants.py (~280 lines) - All text constants
├── s2a_templates.py (~250 lines) - S2A templates
├── d2a_templates.py (~150 lines) - D2A templates
├── c2a_templates.py (~200 lines) - C2A templates
├── a2a_templates.py (~200 lines) - A2A templates
├── a2c_templates.py (~150 lines) - A2C templates
└── formatters.py (~50 lines) - Helper functions
```

**Backward Compatibility:**
- `src/core/messaging_template_texts.py` becomes ~100 line shim
- Re-exports all public APIs
- Maintains exact import paths

---

## 📝 Notes

- Growth was driven by legitimate feature enhancements (swarm coordination, risk assessment)
- Template strings are inherently long (policy text, protocols, examples)
- File serves as SSOT for messaging templates (critical system component)
- Refactoring plan exists but hasn't been executed yet
- File is actively used across messaging system (2+ importing files)

---

**Analysis Date:** 2025-12-15  
**Next Review:** After refactoring execution
