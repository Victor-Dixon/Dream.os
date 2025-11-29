# Thea Code Review Guide - Agent Usage

**Purpose**: Use Thea (ChatGPT custom GPT) for Dream.OS-compliant code reviews  
**Tool**: `tools/thea_code_review.py`  
**Author**: Agent-1  
**Date**: 2025-01-27

---

## 🎯 **WHEN TO USE**

**Use Thea code review for**:
- New code drops requiring V3 compliance validation
- Major refactoring work
- Architecture reviews
- SOLID principle validation
- Module size/complexity analysis

**Don't use for**:
- Simple bug fixes
- Trivial changes
- Already-reviewed code

---

## 🚀 **QUICK START**

### **Basic Usage**:
```bash
# Review a single file
python tools/thea_code_review.py src/core/message_queue.py

# With context
python tools/thea_code_review.py src/core/message_queue.py --context "V3 refactor needed"

# Headless mode (no browser window)
python tools/thea_code_review.py src/core/message_queue.py --headless
```

---

## 📋 **REVIEW PROCESS**

### **Step 1: Run Review**
```bash
python tools/thea_code_review.py <file_path>
```

### **Step 2: Review Output**
The tool generates:
- **Findings**: V3 compliance violations, architecture issues
- **Refactor Plan**: YAML-structured refactoring steps
- **Commit Message**: Ready-to-use commit message
- **Next Steps**: Task assignments for agents

### **Step 3: Save Results**
Results saved to: `thea_code_reviews/review_<filename>_<timestamp>.json`

---

## 📊 **REVIEW OUTPUT FORMAT**

### **Structured Response**:
```yaml
findings:
  - type: "V3_COMPLIANCE"
    severity: "HIGH"
    issue: "Module exceeds 400 lines (790+ lines)"
    location: "message_queue.py:1"
  
  - type: "SRP_VIOLATION"
    severity: "HIGH"
    issue: "Multiple responsibilities in single module"
    location: "message_queue.py"

refactor_plan:
  steps:
    - action: "split_module"
      target: "message_queue.py"
      into: 
        - "queue_config.py"
        - "queue_core.py"
        - "queue_persistence.py"
        - "queue_metrics.py"

commit_message: "Refactor: Split MessageQueue into V3-compliant modules"

next_steps:
  - task: "Create queue_config.py (<400 lines)"
    assigned_to: "Agent-1"
  - task: "Create queue_core.py (<400 lines)"
    assigned_to: "Agent-1"
```

---

## 🔧 **INTEGRATION WITH AGENT WORKFLOW**

### **For Code Drops**:
1. Receive code drop
2. Run: `python tools/thea_code_review.py <file>`
3. Review findings
4. Execute refactor plan
5. Update status.json

### **For PR Reviews**:
1. Checkout PR branch
2. Review changed files with Thea
3. Report findings to PR author
4. Track fixes in status.json

---

## ⚙️ **CONFIGURATION**

### **Thea Service Setup**:
- **Cookies**: Saved to `thea_cookies.json`
- **Responses**: Saved to `thea_responses/`
- **Reviews**: Saved to `thea_code_reviews/`

### **First Time Setup**:
1. Run tool (will prompt for login)
2. Login to ChatGPT in browser window
3. Cookies saved automatically
4. Future runs use saved cookies

---

## 🐛 **TROUBLESHOOTING**

### **"TheaService not available"**:
```bash
pip install selenium pyautogui pyperclip
```

### **"Failed to login"**:
- Check `thea_cookies.json` exists
- Delete and re-login if expired
- Ensure ChatGPT account is active

### **"No response from Thea"**:
- Check browser window is visible
- Wait longer (responses can take 30-60s)
- Check internet connection

---

## 📝 **EXAMPLE WORKFLOW**

### **Agent-1 receives code drop**:
```bash
# 1. Review the code
python tools/thea_code_review.py src/core/message_queue.py

# 2. Review output
cat thea_code_reviews/review_message_queue_*.json

# 3. Execute refactor plan
# (Follow YAML steps from review)

# 4. Update status
# (Update agent_workspaces/Agent-1/status.json)
```

---

## ✅ **BEST PRACTICES**

1. **Always review before major refactors**
2. **Save review results** for tracking
3. **Follow refactor plans** from Thea
4. **Update status.json** after reviews
5. **Report blockers** immediately

---

**🐝 WE. ARE. SWARM. ⚡🔥🚀**

*Use Thea for quality code reviews - maintain V3 compliance standards*

