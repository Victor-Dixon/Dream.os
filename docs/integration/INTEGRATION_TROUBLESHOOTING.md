# Integration Troubleshooting Guide - Swarm Reference

**Date**: 2025-11-26  
**Created By**: Agent-2 (Architecture & Design Specialist)  
**Status**: ✅ **TROUBLESHOOTING GUIDE READY**  
**For**: Swarm-wide troubleshooting reference

---

## 🚨 **COMMON ISSUES & SOLUTIONS**

### **Issue 1: Too Many Duplicates Found**

**Symptoms**:
- Thousands of duplicate files detected
- Most are virtual environment files

**Solution**:
1. Run `detect_venv_files.py` first
2. Remove venv files
3. Update .gitignore
4. Re-run duplicate detector

**Prevention**: Always run venv detection before duplicate detection

---

### **Issue 2: SSOT Version Unclear**

**Symptoms**:
- Multiple files with same name
- Not sure which to keep

**Solution**:
1. Use enhanced duplicate detector (SSOT priority rules)
2. Priority: Root > Main dirs > Not in merged repos > src/ > Not in tests
3. Review SSOT recommendations
4. Test after keeping SSOT version

**Tool**: `enhanced_duplicate_detector.py` with SSOT determination

---

### **Issue 3: Service Enhancement Conflicts**

**Symptoms**:
- Existing service has conflicting methods
- Not sure how to enhance

**Solution**:
1. Review Service Architecture Patterns
2. Use Service Enhancement Pattern
3. Add new methods (don't modify existing)
4. Maintain backward compatibility
5. Test both old and new methods

**Reference**: `docs/architecture/SERVICE_ARCHITECTURE_PATTERNS.md`

---

### **Issue 4: Integration Tests Failing**

**Symptoms**:
- Tests pass individually
- Integration tests fail

**Solution**:
1. Check service dependencies
2. Verify data models unified
3. Check error handling
4. Review integration test template
5. Test incrementally

**Reference**: `docs/integration/INTEGRATION_TEMPLATES.md` (Test Template)

---

### **Issue 5: Pattern Extraction Overwhelming**

**Symptoms**:
- Too many patterns extracted
- Not sure which to integrate

**Solution**:
1. Categorize patterns by priority
2. Start with HIGH priority patterns
3. Integrate incrementally
4. Test after each pattern
5. Document decisions

**Reference**: Integration Patterns Catalog (priority matrix)

---

## 🔧 **TOOL TROUBLESHOOTING**

### **Tool: Enhanced Duplicate Detector**

**Issue**: Tool takes too long
- **Solution**: Exclude venv patterns, use smaller repo subsets

**Issue**: SSOT determination unclear
- **Solution**: Review SSOT priority rules, manually verify

**Issue**: Resolution script not working
- **Solution**: Review script, uncomment removal commands carefully

---

### **Tool: Pattern Analyzer**

**Issue**: Too many patterns found
- **Solution**: Filter by pattern type, prioritize by functionality

**Issue**: Patterns not categorized
- **Solution**: Use pattern extraction template, categorize manually

---

## 📋 **TROUBLESHOOTING CHECKLIST**

### **Before Integration**:
- [ ] Venv files removed?
- [ ] Duplicates resolved?
- [ ] Integration issues checked?
- [ ] Tools working correctly?

### **During Integration**:
- [ ] Patterns extracted?
- [ ] Services reviewed?
- [ ] Enhancement plan clear?
- [ ] Backward compatibility maintained?

### **After Integration**:
- [ ] Tests passing?
- [ ] Functionality verified?
- [ ] Documentation updated?
- [ ] Issues resolved?

---

## 🎯 **GETTING HELP**

### **Documentation**:
- Integration Patterns Catalog
- Service Architecture Patterns
- Integration Templates
- Best Practices Guide

### **Tools**:
- Enhanced duplicate detector
- Pattern analyzer
- Integration issues checker

### **Support**:
- Agent-2 support available
- Swarm coordination active
- Tool sharing active

---

**Status**: ✅ **TROUBLESHOOTING GUIDE READY**  
**Last Updated**: 2025-11-26 14:55:00 (Local System Time)

