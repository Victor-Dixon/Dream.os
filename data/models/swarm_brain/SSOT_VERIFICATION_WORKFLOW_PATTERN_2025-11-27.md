# SSOT Verification Workflow Pattern

**Created By**: Agent-8 (SSOT & System Integration Specialist)  
**Date**: 2025-11-27  
**Category**: SSOT Compliance, Verification Patterns  
**Status**: Active Pattern

---

## 📋 **Pattern Description**

Systematic workflow for post-merge SSOT verification to catch violations early and maintain SSOT compliance throughout repository consolidation efforts.

---

## 🎯 **Use Case**

**When to Use:**
- After each repository merge in consolidation efforts
- Before marking merges as complete
- When establishing SSOT compliance for new integrations
- During Batch operations (e.g., Batch 2 merges)

**Why it Matters:**
- Catches SSOT violations early before they compound
- Maintains single source of truth across merges
- Ensures system integration integrity
- Prevents duplicate entries in master lists

---

## 📝 **Workflow Steps**

### **1. Pre-Verification Preparation**
- Ensure master list is current
- Verify no duplicate entries exist
- Check import paths are valid
- Confirm configuration SSOT is intact

### **2. Post-Merge Actions**
```bash
# Update master list with merge information
python tools/batch2_ssot_verifier.py --merge "source_repo -> target_repo"

# Run full SSOT verification
python tools/batch2_ssot_verifier.py --full

# Verify imports are still valid
python tools/import_chain_validator.py --check-all
```

### **3. Verification Categories**
1. **Master List Integrity**
   - No duplicate repo names
   - All repos properly marked as merged
   - Target repos have merged_repos array updated

2. **Import Verification**
   - All imports resolve correctly
   - No broken import paths
   - No circular dependencies introduced

3. **Configuration SSOT**
   - Single Config class in config_ssot.py
   - No duplicate config sources

4. **Messaging Integration**
   - Single MessageRepository instantiation
   - No duplicate messaging systems

5. **Tool Registry**
   - No duplicate tool registrations
   - Tool registry SSOT compliant

### **4. Issue Resolution**
- Document all issues found
- Prioritize blockers (HIGH/MEDIUM/LOW)
- Resolve before proceeding with next merge
- Update verification checklist

### **5. Documentation**
- Update verification checklist with results
- Document any SSOT violations found
- Report status to relevant agents
- Update consolidation tracker

---

## ⚠️ **Common Issues & Solutions**

### **Issue: Duplicate Repo Names in Master List**
- **Symptom**: Verification tool reports duplicate pairs
- **Solution**: Review duplicates, determine which to keep, update master list
- **Prevention**: Check for duplicates before merges

### **Issue: Import Verification Fails**
- **Symptom**: Import chain validator finds broken paths
- **Solution**: Run detailed analysis, fix broken imports
- **Prevention**: Test imports after each merge

### **Issue: Configuration SSOT Violation**
- **Symptom**: Multiple Config classes detected
- **Solution**: Consolidate config sources to config_ssot.py
- **Prevention**: Use config_ssot facade for all config access

---

## 🛠️ **Tools**

- `tools/batch2_ssot_verifier.py` - Automated SSOT verification
- `tools/import_chain_validator.py` - Import path validation
- `docs/archive/consolidation/BATCH2_SSOT_VERIFICATION_CHECKLIST.md` - Verification checklist

---

## 📊 **Metrics**

- **Verification Time**: 5-10 minutes per merge
- **Issue Detection**: Early (before compound issues)
- **SSOT Compliance**: Maintained throughout process

---

## ✅ **Best Practices**

1. **Verify Early**: Run verification immediately after each merge
2. **Document Issues**: Track all findings for resolution
3. **Resolve Blockers**: Don't proceed with blockers unresolved
4. **Automate**: Use tools to reduce manual overhead
5. **Report Status**: Keep relevant agents informed

---

## 🔄 **Integration with Other Patterns**

- **Repository Consolidation Pattern**: SSOT verification is critical step
- **Merge Workflow Pattern**: Verification follows merge completion
- **Configuration SSOT Pattern**: Ensures config SSOT maintained

---

## 📚 **Related Documentation**

- `docs/archive/consolidation/BATCH2_SSOT_VERIFICATION_CHECKLIST.md`
- `tools/batch2_ssot_verifier.py`
- `docs/CONFIG_SSOT_MIGRATION_GUIDE.md`

---

**Status**: Active Pattern  
**Last Updated**: 2025-11-27

