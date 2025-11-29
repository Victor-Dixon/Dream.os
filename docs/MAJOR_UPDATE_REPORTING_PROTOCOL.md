# 📢 MAJOR UPDATE REPORTING PROTOCOL

**Last Updated**: 2025-11-27  
**Status**: ✅ **ACTIVE DIRECTIVE**  
**Priority**: CRITICAL

---

## 🎯 **PURPOSE**

All agents must report **blockers and accomplishments** to the **MAJOR UPDATE CHANNEL** for Captain visibility.

---

## 📋 **WHEN TO REPORT**

### **Report Blockers Immediately**:
- ❌ Cannot proceed with assigned task
- ❌ Tool not working as expected
- ❌ Missing dependencies or access
- ❌ Unexpected errors blocking progress
- ❌ Need Captain decision or intervention

### **Report Accomplishments When Complete**:
- ✅ Task completed successfully
- ✅ Major milestone reached
- ✅ Significant progress made
- ✅ Goal achieved

---

## 🔧 **HOW TO REPORT**

### **Command**:
```bash
python tools/devlog_manager.py post --agent agent-4 --file <devlog.md> --major
```

### **Devlog Format**:
```markdown
# 🚨 [BLOCKER/ACCOMPLISHMENT] - [Agent-X] - [Task Name]

**Date**: YYYY-MM-DD  
**Agent**: Agent-X  
**Status**: BLOCKER / ACCOMPLISHMENT  
**Priority**: HIGH / CRITICAL

---

## 📊 **STATUS**

[Clear description of blocker or accomplishment]

---

## 🎯 **DETAILS**

[Specific details, progress metrics, next steps]

---

## 📈 **METRICS**

[Progress toward real goals: repos reduced, tests created, code removed, etc.]

---

## 🚨 **BLOCKER DETAILS** (if blocker)

[What's blocking, why, what's needed to unblock]

---

## ✅ **NEXT STEPS** (if accomplishment)

[What's next, how to continue progress]
```

---

## 📊 **REPORTING EXAMPLES**

### **Blocker Report**:
```markdown
# 🚨 BLOCKER - Agent-1 - Case Variations Consolidation

**Status**: BLOCKED - GitHub API rate limit exceeded

**Details**: Cannot execute Case Variations consolidation. GitHub API rate limit reached (60/60 requests). Need to wait for reset or use alternative method.

**Impact**: 12 repos consolidation delayed

**Next Steps**: Wait for rate limit reset (1 hour) or use GitHub CLI alternative
```

### **Accomplishment Report**:
```markdown
# ✅ ACCOMPLISHMENT - Agent-1 - Case Variations Consolidation

**Status**: COMPLETE - 12 repos consolidated

**Details**: Successfully executed all 12 case variation merges. All PRs created and verified.

**Metrics**: 
- Repos reduced: 12 (62 → 50)
- Progress toward target: 12/26-29 repos (46% of target)

**Next Steps**: Execute Trading Repos consolidation (4 → 1, 3 repos)
```

---

## ⚠️ **CRITICAL RULES**

1. **Report blockers IMMEDIATELY** - Don't wait, don't try to solve alone
2. **Report accomplishments when COMPLETE** - Not during, not planned, when done
3. **Use --major flag** - This posts to major update channel
4. **Include metrics** - Show progress toward real goals
5. **Be specific** - Clear status, details, next steps

---

## 🎯 **REAL GOALS TO TRACK**

When reporting, include progress toward:

1. **GitHub Consolidation**: Repos reduced (target: 26-29 repos)
2. **Stage 1 Integration**: Repos integrated (target: all assigned repos)
3. **Test Coverage**: Coverage percentage (target: ≥85%)
4. **Code Quality**: Code removed (target: confirmed unused code)

---

**🔥 REPORT TO MAJOR UPDATE CHANNEL - CAPTAIN NEEDS VISIBILITY**



