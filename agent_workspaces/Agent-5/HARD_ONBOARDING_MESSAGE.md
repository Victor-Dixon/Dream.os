# 🚨 HARD ONBOARDING - Agent-5

**Date**: 2025-11-27  
**Priority**: CRITICAL  
**Focus**: EXECUTE REAL GOALS - Tools are means, not goals

---

## 🎯 **YOUR ASSIGNMENT: Test Coverage & Code Quality**

### **PRIMARY TASK**: Create Tests for Untested Code

**Goal**: Reach ≥85% test coverage, remove unused code

**Current Status**:
- 90 files without tests
- 627 functions untested
- 218 classes untested

**Immediate Action**:
1. **Create Tests for High-Value Modules**
   - Use: `tools/analyze_unneeded_functionality.py` to identify gaps
   - **Action**: Create tests for untested functions and classes
   - Focus on high-impact modules first

2. **Remove Confirmed Unused Code**
   - Use: `tools/analyze_unneeded_functionality.py` to identify dead code
   - **Action**: Remove confirmed unused code after verification

**Tools Available** (USE THEM, DON'T CREATE MORE):
- `tools/analyze_unneeded_functionality.py` - Identify untested/unused code
- Test analysis reports showing gaps
- Existing test infrastructure

---

## 📊 **REPORTING PROTOCOL**

**Report ALL blockers and accomplishments to MAJOR UPDATE CHANNEL**:
- Use: `python tools/devlog_manager.py post --agent agent-4 --file <devlog.md> --major`
- Report: Blockers immediately, accomplishments when complete
- Format: Clear status, progress metrics, next steps

---

## ⚠️ **CRITICAL RULES**

1. **Tools are MEANS to goals** - Use existing tools to execute, don't create more
2. **Focus on EXECUTION** - Create tests and remove dead code, don't plan more
3. **Report blockers immediately** - Use major update channel
4. **Measure progress** - Track test coverage and code removed

---

## 🎯 **SUCCESS METRICS**

- Tests created: Significant reduction in untested code
- Code removed: Confirmed unused code eliminated
- Coverage improved: Progress toward ≥85% target

**START EXECUTING NOW** 🚀



