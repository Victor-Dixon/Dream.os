# Integration Command Reference - Swarm Reference

**Date**: 2025-11-26  
**Created By**: Agent-2 (Architecture & Design Specialist)  
**Status**: ✅ **COMMAND REFERENCE READY**  
**For**: Swarm-wide command reference

---

## 🛠️ **TOOL COMMANDS**

### **Venv File Detection**:
```bash
# Basic usage
python tools/detect_venv_files.py <repo_path>

# With verbose output
python tools/detect_venv_files.py <repo_path> --verbose

# With output file
python tools/detect_venv_files.py <repo_path> --output venv_report.txt
```

---

### **Duplicate Detection**:
```bash
# Basic usage
python tools/enhanced_duplicate_detector.py <repo_path>

# With verbose output
python tools/enhanced_duplicate_detector.py <repo_path> --verbose

# With resolution script generation
python tools/enhanced_duplicate_detector.py <repo_path> --generate-script

# With output file
python tools/enhanced_duplicate_detector.py <repo_path> --output duplicate_report.txt
```

---

### **Pattern Analysis**:
```bash
# Basic usage
python tools/pattern_analyzer.py <repo_path>

# With verbose output
python tools/pattern_analyzer.py <repo_path> --verbose

# With output file
python tools/pattern_analyzer.py <repo_path> --output pattern_report.txt
```

---

### **Integration Issues Check**:
```bash
# Basic usage
python tools/check_integration_issues.py <repo_path>

# With verbose output
python tools/check_integration_issues.py <repo_path> --verbose

# With output file
python tools/check_integration_issues.py <repo_path> --output issues_report.txt
```

---

### **Tool Verification**:
```bash
# Verify all tools
python tools/verify_integration_tools.py

# Verify specific tool
python tools/verify_integration_tools.py --tool enhanced_duplicate_detector
```

---

### **Integration Workflow Automation**:
```bash
# Run complete workflow
python tools/integration_workflow_automation.py <repo_path>

# Run specific phase
python tools/integration_workflow_automation.py <repo_path> --phase cleanup

# With verbose output
python tools/integration_workflow_automation.py <repo_path> --verbose
```

---

## 🔧 **GIT COMMANDS**

### **Repository Operations**:
```bash
# Clone repository
git clone <repo_url>

# Checkout branch
git checkout <branch_name>

# Create new branch
git checkout -b <branch_name>

# Switch to branch
git switch <branch_name>
```

---

### **Merge Operations**:
```bash
# Merge branch
git merge <branch_name>

# Merge with 'ours' strategy
git checkout --ours <file>
git add <file>
git commit -m "Resolve conflict using 'ours' strategy"

# Abort merge
git merge --abort
```

---

### **Conflict Resolution**:
```bash
# Check conflicts
git status

# List conflicted files
git diff --name-only --diff-filter=U

# Resolve conflict (ours)
git checkout --ours <file>
git add <file>

# Resolve conflict (theirs)
git checkout --theirs <file>
git add <file>
```

---

### **Push Operations**:
```bash
# Push branch
git push origin <branch_name>

# Force push (use with caution)
git push origin <branch_name> --force

# Push with tags
git push origin <branch_name> --tags
```

---

## 🧪 **TESTING COMMANDS**

### **Python Testing**:
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_integration.py

# Run with coverage
pytest --cov=<module> --cov-report=html

# Run with verbose output
pytest -v

# Run specific test
pytest tests/test_integration.py::test_specific_function
```

---

### **Coverage Commands**:
```bash
# Generate coverage report
pytest --cov=<module> --cov-report=html

# View coverage report
# Open htmlcov/index.html in browser

# Check coverage percentage
pytest --cov=<module> --cov-report=term
```

---

## 📋 **WORKFLOW COMMANDS**

### **Complete Cleanup Workflow**:
```bash
# Run complete cleanup
bash tools/complete_cleanup_workflow.sh <repo_path>

# With verbose output
bash tools/complete_cleanup_workflow.sh <repo_path> --verbose
```

---

### **Pattern Extraction Workflow**:
```bash
# Run pattern extraction
bash tools/pattern_extraction_workflow.sh <repo_path>

# With verbose output
bash tools/pattern_extraction_workflow.sh <repo_path> --verbose
```

---

## 🔍 **DIAGNOSTIC COMMANDS**

### **Repository Status**:
```bash
# Check git status
git status

# Check branch
git branch

# Check remote
git remote -v

# Check log
git log --oneline -10
```

---

### **File Operations**:
```bash
# Find venv files
find <repo_path> -name "site-packages" -type d

# Find duplicate files (manual)
find <repo_path> -type f -exec md5sum {} \; | sort | uniq -d -w 32

# Check file size
du -sh <repo_path>
```

---

## 📊 **QUICK REFERENCE TABLE**

| Task | Command |
|------|---------|
| Detect venv files | `python tools/detect_venv_files.py <repo_path>` |
| Detect duplicates | `python tools/enhanced_duplicate_detector.py <repo_path>` |
| Extract patterns | `python tools/pattern_analyzer.py <repo_path>` |
| Check issues | `python tools/check_integration_issues.py <repo_path>` |
| Verify tools | `python tools/verify_integration_tools.py` |
| Run tests | `pytest` |
| Check coverage | `pytest --cov=<module> --cov-report=html` |
| Clone repo | `git clone <repo_url>` |
| Merge branch | `git merge <branch_name>` |
| Resolve conflict | `git checkout --ours <file>` |

---

## 🔗 **COMMAND REFERENCE RESOURCES**

- **Cheat Sheet**: [Integration Cheat Sheet](INTEGRATION_CHEAT_SHEET.md)
- **Tool Usage**: [Tool Usage Guide](TOOL_USAGE_GUIDE.md)
- **Quick Start**: [Integration Quick Start Guide](INTEGRATION_QUICK_START.md)
- **Workflow**: [Integration Workflow Automation](INTEGRATION_WORKFLOW_AUTOMATION.md)

---

**Status**: ✅ **COMMAND REFERENCE READY**  
**Last Updated**: 2025-11-26 16:00:00 (Local System Time)

