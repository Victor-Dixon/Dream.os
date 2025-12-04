# Thea Code Review Tool - Workflow Integration Guide

**Purpose**: Integrate Thea code review tool into regular agent workflow  
**Tool**: `tools/thea_code_review.py`  
**Author**: Agent-1 (Integration & Core Systems Specialist)  
**Date**: 2025-12-03  
**Status**: ✅ **INTEGRATED**

---

## 🎯 **INTEGRATION STATUS**

**Tool Status**: ✅ Ready for use  
**Documentation**: ✅ Complete  
**Workflow Integration**: ✅ Active  

---

## 📋 **WORKFLOW INTEGRATION POINTS**

### **1. Code Drop Review Workflow**

**When**: Receiving new code drops or major changes  
**Action**: Run Thea code review before integration

```bash
# Review incoming code drop
python tools/thea_code_review.py <file_path> --context "Code drop review"

# Review multiple files
for file in $(git diff --name-only); do
    python tools/thea_code_review.py "$file"
done
```

**Output**: Structured review saved to `thea_code_reviews/`  
**Next Steps**: 
- Review findings
- Execute refactor plan if needed
- Update status.json with review results

---

### **2. PR Review Workflow**

**When**: Reviewing pull requests  
**Action**: Review changed files with Thea

```bash
# Review PR changes
git checkout <pr_branch>
python tools/thea_code_review.py <changed_file> --context "PR review"

# Review all changed files
git diff --name-only main...<pr_branch> | xargs -I {} python tools/thea_code_review.py {}
```

**Output**: Review findings for PR author  
**Integration**: Report findings in PR comments or status updates

---

### **3. V3 Compliance Review Workflow**

**When**: Coordinating with Agent-4 on V3 compliance  
**Action**: Use Thea for compliance validation

```bash
# V3 compliance review
python tools/thea_code_review.py <file> --context "V3 compliance check"

# Share results with Agent-4
# Results saved to: thea_code_reviews/review_<file>_<timestamp>.json
```

**Coordination**: 
- Share review results with Agent-4
- Track compliance issues in status.json
- Execute refactor plans for compliance

---

### **4. Architecture Review Workflow**

**When**: Major refactoring or architecture changes  
**Action**: Use Thea for architecture validation

```bash
# Architecture review
python tools/thea_code_review.py <file> --context "Architecture review - SOLID principles"

# Review findings focus on:
# - SOLID principle violations
# - Module size/complexity
# - Separation of concerns
```

---

## 🔄 **AUTOMATED INTEGRATION**

### **Pre-Commit Hook** (Optional)

Create `.git/hooks/pre-commit`:
```bash
#!/bin/bash
# Review changed files with Thea (non-blocking)
for file in $(git diff --cached --name-only --diff-filter=ACM | grep '\.py$'); do
    python tools/thea_code_review.py "$file" --headless
done
```

### **CI/CD Integration** (Future)

- Add Thea review step to CI pipeline
- Generate review reports for PRs
- Track compliance metrics

---

## 📊 **USAGE PATTERNS**

### **Pattern 1: Quick Review**
```bash
# Single file, no context
python tools/thea_code_review.py src/core/message_queue.py
```

### **Pattern 2: Contextual Review**
```bash
# With context for better results
python tools/thea_code_review.py src/services/messaging.py --context "V3 refactor needed"
```

### **Pattern 3: Batch Review**
```bash
# Review all files in directory
find src/services -name "*.py" -exec python tools/thea_code_review.py {} \;
```

### **Pattern 4: Headless Review**
```bash
# No browser window (for automation)
python tools/thea_code_review.py <file> --headless
```

---

## 🎯 **BEST PRACTICES**

### **When to Use Thea Review**:
✅ **DO USE** for:
- New code drops
- Major refactoring
- Architecture changes
- V3 compliance validation
- SOLID principle checks
- Module size/complexity analysis

❌ **DON'T USE** for:
- Simple bug fixes
- Trivial changes (<10 lines)
- Already-reviewed code
- Test-only changes

### **Review Workflow**:
1. **Run Review**: Execute Thea tool
2. **Review Findings**: Check structured output
3. **Execute Plan**: Follow refactor plan if needed
4. **Update Status**: Document in status.json
5. **Share Results**: Coordinate with relevant agents

### **Coordination with Agent-4**:
- Share V3 compliance review results
- Track compliance issues
- Execute refactor plans together
- Update compliance status

---

## 📝 **STATUS TRACKING**

### **Update status.json After Review**:
```json
{
  "current_tasks": [
    "Code Review - <file>: Thea review complete, <N> findings, refactor plan ready"
  ]
}
```

### **Track Review Results**:
- Save review JSON files
- Document findings in status.json
- Track refactor plan execution
- Monitor compliance improvements

---

## 🔧 **TROUBLESHOOTING**

### **Common Issues**:

**"TheaService not available"**:
```bash
pip install selenium undetected-chromedriver pyautogui pyperclip
```

**"Cookies expired"**:
```bash
# Refresh cookies
python tools/thea/setup_thea_cookies.py
```

**"No response from Thea"**:
- Check browser window is visible
- Wait longer (30-60s for responses)
- Check internet connection
- Verify cookies are fresh

---

## 📚 **RELATED DOCUMENTATION**

- **Tool Guide**: `docs/tools/THEA_CODE_REVIEW_GUIDE.md`
- **Tool Source**: `tools/thea_code_review.py`
- **Service**: `src/services/thea/thea_service.py`

---

## ✅ **INTEGRATION CHECKLIST**

- [x] Tool exists and is functional
- [x] Documentation created
- [x] Workflow integration points defined
- [x] Best practices documented
- [x] Status tracking established
- [x] Coordination with Agent-4 planned
- [ ] Pre-commit hook (optional)
- [ ] CI/CD integration (future)

---

**Status**: ✅ **INTEGRATED - Ready for use**  
**Next Steps**: Use tool for code drops and PR reviews, coordinate with Agent-4 on V3 compliance




