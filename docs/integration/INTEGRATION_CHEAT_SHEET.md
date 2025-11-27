# Integration Cheat Sheet - One-Page Quick Reference

**Date**: 2025-11-26  
**Created By**: Agent-2 (Architecture & Design Specialist)  
**Status**: ✅ **CHEAT SHEET READY**  
**For**: Swarm-wide quick reference

---

## 🚀 **4-PHASE WORKFLOW** (Quick)

### **Phase 0: Cleanup** (15-30 min)
```bash
python tools/detect_venv_files.py <repo_path>
python tools/enhanced_duplicate_detector.py <repo_path>
```

### **Phase 1: Pattern Extraction** (30-60 min)
```bash
python tools/pattern_analyzer.py <repo_path>
# Review patterns, document findings
```

### **Phase 2: Service Integration** (1-4 hours)
- Review existing services
- Enhance (don't duplicate)
- Maintain backward compatibility

### **Phase 3: Testing** (30-60 min)
- Unit tests (90%+ coverage)
- Integration tests (80%+ coverage)
- Backward compatibility tests

---

## 🎯 **TOOL SELECTION** (Quick)

| Scenario | Tool | Command |
|----------|------|---------|
| Venv cleanup | `detect_venv_files.py` | `python tools/detect_venv_files.py <path>` |
| Duplicates | `enhanced_duplicate_detector.py` | `python tools/enhanced_duplicate_detector.py <path>` |
| Patterns | `pattern_analyzer.py` | `python tools/pattern_analyzer.py <path>` |
| Issues | `check_integration_issues.py` | `python tools/check_integration_issues.py <path>` |
| Automation | `integration_workflow_automation.py` | `python tools/integration_workflow_automation.py` |

---

## 📋 **PATTERN SELECTION** (Quick)

| Integration Type | Pattern | Priority |
|------------------|---------|----------|
| Service enhancement | Pattern 0: Service Enhancement | ✅ Always |
| Repo merge | Pattern 1: Repository Consolidation | ✅ Always |
| Duplicate files | Pattern 2: Duplicate Resolution | ✅ Always |
| Venv files | Pattern 3: Venv Cleanup | ✅ Always |
| Logic integration | Pattern 4: Logic Integration | ✅ Always |
| Code patterns | Pattern 5: Code Pattern Extraction | ✅ Always |

---

## ⚡ **COMMON COMMANDS** (Quick)

### **Git Operations**:
```bash
# Clone repo
git clone <repo_url>

# Checkout branch
git checkout <branch>

# Merge with 'ours' strategy
git checkout --ours <file>
git add <file>

# Push changes
git push origin <branch>
```

### **Python Operations**:
```bash
# Run tool
python tools/<tool_name>.py <args>

# Run automation
python tools/integration_workflow_automation.py

# Verify toolkit
python tools/verify_integration_tools.py
```

---

## ✅ **QUICK CHECKLIST** (5 Steps)

- [ ] **Phase 0**: Cleanup (venv + duplicates)
- [ ] **Phase 1**: Extract patterns
- [ ] **Phase 2**: Integrate services
- [ ] **Phase 3**: Test (90%+ coverage)
- [ ] **Document**: Update docs, post devlog

---

## 🔗 **QUICK LINKS**

- **Getting Started**: [Quick Start Guide](INTEGRATION_QUICK_START.md)
- **Full Workflow**: [Integration Methodology](STAGE1_INTEGRATION_METHODOLOGY.md)
- **Tool Selection**: [Decision Tree](TOOL_SELECTION_DECISION_TREE.md)
- **Troubleshooting**: [Troubleshooting Guide](INTEGRATION_TROUBLESHOOTING.md)
- **Examples**: [Integration Examples](INTEGRATION_EXAMPLES.md)
- **FAQ**: [Integration FAQ](INTEGRATION_FAQ.md)

---

## 🎯 **SSOT PRIORITY RULES** (Quick)

1. **Root/main directories** (highest priority)
2. **Not in merged repo directories**
3. **src/ or main source directories**
4. **Not in test directories** (lowest priority)

---

## ⚠️ **COMMON PITFALLS** (Avoid)

- ❌ Duplicating services (enhance instead)
- ❌ Skipping venv cleanup (do first)
- ❌ Ignoring duplicates (resolve early)
- ❌ Missing tests (90%+ coverage required)
- ❌ Breaking backward compatibility (maintain it)

---

**Status**: ✅ **CHEAT SHEET READY**  
**Last Updated**: 2025-11-26 15:40:00 (Local System Time)

