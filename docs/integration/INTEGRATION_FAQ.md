# Integration FAQ - Swarm Reference

**Date**: 2025-11-26  
**Created By**: Agent-2 (Architecture & Design Specialist)  
**Status**: ✅ **FAQ READY**  
**For**: Swarm-wide frequently asked questions

---

## ❓ **FREQUENTLY ASKED QUESTIONS**

### **Q1: Which tool should I use first?**

**A**: Always start with `detect_venv_files.py` (Phase 0). Venv files should be removed before duplicate detection.

**Reference**: [Tool Selection Decision Tree](TOOL_SELECTION_DECISION_TREE.md)

---

### **Q2: How do I determine SSOT version for duplicates?**

**A**: Use enhanced duplicate detector - it applies 4-level priority:
1. Root/main directories
2. Not in merged repo directories
3. src/ or main source directories
4. Not in test directories

**Reference**: [Enhanced Duplicate Detector](../../tools/enhanced_duplicate_detector.py)

---

### **Q3: Should I duplicate services or enhance existing ones?**

**A**: Always enhance existing services. Duplicating services creates maintenance burden.

**Reference**: [Service Architecture Patterns](../architecture/SERVICE_ARCHITECTURE_PATTERNS.md) - Pattern 2

---

### **Q4: How long does integration take?**

**A**: Depends on scenario:
- 2 repos: 2-4 hours
- 8 repos: 2-3 days
- Service enhancement: 1-2 hours
- Duplicate cleanup: 30 min - 1 hour
- Venv cleanup: 15-30 minutes

**Reference**: [Integration Scenarios](INTEGRATION_SCENARIOS.md)

---

### **Q5: What if I find conflicts during merge?**

**A**: Use 'ours' strategy (keep target repo versions):
```bash
git checkout --ours <file>
git add <file>
```

**Reference**: [Integration Patterns Catalog](INTEGRATION_PATTERNS_CATALOG.md) - Pattern 1

---

### **Q6: How do I automate my workflow?**

**A**: Use automation scripts:
- Python: `tools/integration_workflow_automation.py`
- Bash: `tools/complete_cleanup_workflow.sh`

**Reference**: [Integration Workflow Automation](INTEGRATION_WORKFLOW_AUTOMATION.md)

---

### **Q7: What patterns should I extract?**

**A**: Extract functional patterns:
- Service patterns
- Data model patterns
- API integration patterns
- Testing patterns
- Error handling patterns

**Reference**: [Integration Patterns Catalog](INTEGRATION_PATTERNS_CATALOG.md)

---

### **Q8: How do I test my integration?**

**A**: Follow testing template:
1. Unit tests (90%+ coverage)
2. Integration tests (80%+ coverage)
3. Backward compatibility tests
4. Error handling tests

**Reference**: [Integration Templates](INTEGRATION_TEMPLATES.md) - Test Template

---

### **Q9: What if tools fail or give errors?**

**A**: Check troubleshooting guide:
- Review error messages
- Check tool requirements
- Verify repository access
- Review common issues

**Reference**: [Integration Troubleshooting Guide](INTEGRATION_TROUBLESHOOTING.md)

---

### **Q10: Where do I start if I'm new to integration?**

**A**: Start with Quick Start Guide (5 minutes):
1. Read [Integration Quick Start Guide](INTEGRATION_QUICK_START.md)
2. Choose scenario from [Integration Scenarios](INTEGRATION_SCENARIOS.md)
3. Use [Tool Selection Decision Tree](TOOL_SELECTION_DECISION_TREE.md)

---

## 🔗 **QUICK REFERENCE**

### **Common Questions**:
- Tool selection → [Tool Selection Decision Tree](TOOL_SELECTION_DECISION_TREE.md)
- Workflow → [Integration Quick Start Guide](INTEGRATION_QUICK_START.md)
- Troubleshooting → [Integration Troubleshooting Guide](INTEGRATION_TROUBLESHOOTING.md)
- Patterns → [Integration Patterns Catalog](INTEGRATION_PATTERNS_CATALOG.md)
- Examples → [Integration Examples](INTEGRATION_EXAMPLES.md)

---

**Status**: ✅ **FAQ READY**  
**Last Updated**: 2025-11-26 15:35:00 (Local System Time)

