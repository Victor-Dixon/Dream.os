# Integration Troubleshooting Scenarios - Swarm Reference

**Date**: 2025-11-26  
**Created By**: Agent-2 (Architecture & Design Specialist)  
**Status**: ✅ **TROUBLESHOOTING SCENARIOS READY**  
**For**: Swarm-wide troubleshooting scenarios

---

## 🔧 **COMMON TROUBLESHOOTING SCENARIOS**

### **Scenario 1: Venv Files Not Detected**

**Symptoms**:
- Tool reports 0 venv files, but you see venv directories
- Venv files still in repo after cleanup

**Diagnosis**:
```bash
# Check tool configuration
python tools/detect_venv_files.py <repo_path> --verbose

# Manual check
find <repo_path> -name "site-packages" -type d
```

**Solution**:
1. Verify tool patterns match your venv structure
2. Check .gitignore patterns
3. Manually remove venv directories if needed
4. Update tool patterns if necessary

**Prevention**: Use standard venv patterns, update .gitignore early

---

### **Scenario 2: Duplicate Detection False Positives**

**Symptoms**:
- Tool reports duplicates that aren't actually duplicates
- SSOT determination incorrect

**Diagnosis**:
```bash
# Check duplicate report
python tools/enhanced_duplicate_detector.py <repo_path> --verbose

# Review SSOT priority rules
# Check file content manually
```

**Solution**:
1. Review duplicate report details
2. Verify file content (not just names)
3. Check SSOT priority rules
4. Manually verify SSOT decisions
5. Update priority rules if needed

**Prevention**: Use content-based detection, review SSOT rules

---

### **Scenario 3: Pattern Extraction Returns No Patterns**

**Symptoms**:
- Pattern analyzer reports 0 patterns found
- Expected patterns not detected

**Diagnosis**:
```bash
# Run pattern analyzer with verbose output
python tools/pattern_analyzer.py <repo_path> --verbose

# Check pattern detection rules
# Review code structure manually
```

**Solution**:
1. Verify pattern detection rules
2. Check code structure (may need manual extraction)
3. Review pattern categories
4. Manually extract patterns if needed
5. Update pattern detection rules

**Prevention**: Use comprehensive pattern detection, manual review

---

### **Scenario 4: Service Integration Breaks Backward Compatibility**

**Symptoms**:
- Existing APIs fail after integration
- Backward compatibility tests fail
- Existing integrations break

**Diagnosis**:
```bash
# Run backward compatibility tests
pytest tests/test_backward_compatibility.py

# Check API contracts
# Review service changes
```

**Solution**:
1. Review service changes
2. Restore backward compatible APIs
3. Add deprecation warnings if needed
4. Update tests
5. Document breaking changes (if necessary)

**Prevention**: Always enhance services, maintain API contracts, test backward compatibility

---

### **Scenario 5: Test Coverage Below Target**

**Symptoms**:
- Unit coverage < 90%
- Integration coverage < 80%
- Coverage report shows gaps

**Diagnosis**:
```bash
# Run coverage report
pytest --cov=<module> --cov-report=html

# Review coverage gaps
# Check untested code paths
```

**Solution**:
1. Identify coverage gaps
2. Add unit tests for uncovered code
3. Add integration tests for uncovered paths
4. Target ≥ 90% unit, ≥ 80% integration
5. Re-run coverage report

**Prevention**: Write tests during integration, maintain coverage targets

---

### **Scenario 6: Merge Conflicts During Integration**

**Symptoms**:
- Git merge conflicts
- Conflict resolution fails
- Integration blocked

**Diagnosis**:
```bash
# Check merge status
git status

# Review conflicts
git diff --name-only --diff-filter=U
```

**Solution**:
1. Use 'ours' strategy for SSOT
2. Resolve conflicts manually if needed
3. Test after conflict resolution
4. Document conflict decisions
5. Verify integration after resolution

**Prevention**: Use 'ours' strategy, resolve conflicts early, test after resolution

---

### **Scenario 7: Integration Tools Fail or Error**

**Symptoms**:
- Tool execution fails
- Error messages unclear
- Tool not found

**Diagnosis**:
```bash
# Check tool availability
python tools/verify_integration_tools.py

# Check tool requirements
# Review error messages
```

**Solution**:
1. Verify tool installation
2. Check tool requirements
3. Review error messages
4. Check repository access
5. Update tools if needed

**Prevention**: Verify tools before use, check requirements, maintain tools

---

## 🎯 **TROUBLESHOOTING WORKFLOW**

### **Step 1: Identify Symptoms**
- Document symptoms
- Check error messages
- Review tool outputs

### **Step 2: Diagnose Issue**
- Run diagnostic commands
- Review logs
- Check configurations

### **Step 3: Apply Solution**
- Follow solution steps
- Test solution
- Verify fix

### **Step 4: Prevent Recurrence**
- Update prevention measures
- Document solution
- Share with swarm

---

## 📋 **TROUBLESHOOTING CHECKLIST**

### **Before Troubleshooting**:
- [ ] Document symptoms
- [ ] Check error messages
- [ ] Review tool outputs
- [ ] Check configurations

### **During Troubleshooting**:
- [ ] Run diagnostic commands
- [ ] Review logs
- [ ] Apply solution steps
- [ ] Test solution

### **After Troubleshooting**:
- [ ] Verify fix
- [ ] Update prevention measures
- [ ] Document solution
- [ ] Share with swarm

---

## 🔗 **TROUBLESHOOTING RESOURCES**

- **Troubleshooting Guide**: [Integration Troubleshooting Guide](INTEGRATION_TROUBLESHOOTING.md)
- **Tool Verification**: [Tool Verification](../../tools/verify_integration_tools.py)
- **FAQ**: [Integration FAQ](INTEGRATION_FAQ.md)
- **Risk Assessment**: [Integration Risk Assessment](INTEGRATION_RISK_ASSESSMENT.md)

---

**Status**: ✅ **TROUBLESHOOTING SCENARIOS READY**  
**Last Updated**: 2025-11-26 15:45:00 (Local System Time)

