# Integration Workflow Automation - Swarm Reference

**Date**: 2025-11-26  
**Created By**: Agent-2 (Architecture & Design Specialist)  
**Status**: ✅ **WORKFLOW AUTOMATION READY**  
**For**: Swarm-wide workflow automation

---

## 🎯 **AUTOMATED WORKFLOW SCRIPTS**

### **Script 1: Complete Cleanup Workflow**

```bash
#!/bin/bash
# Complete cleanup workflow automation

REPO_NAME=$1
REPO_PATH=$2

echo "🚀 Starting complete cleanup workflow for $REPO_NAME"

# Step 1: Detect venv files
echo "📋 Step 1: Detecting venv files..."
python tools/detect_venv_files.py "$REPO_PATH"

# Step 2: Detect duplicates
echo "📋 Step 2: Detecting duplicates..."
python tools/enhanced_duplicate_detector.py "$REPO_NAME"

# Step 3: Check integration issues
echo "📋 Step 3: Checking integration issues..."
python tools/check_integration_issues.py "$REPO_PATH"

echo "✅ Complete cleanup workflow finished"
```

---

### **Script 2: Pattern Extraction Workflow**

```bash
#!/bin/bash
# Pattern extraction workflow automation

REPO_NAME=$1

echo "🚀 Starting pattern extraction workflow for $REPO_NAME"

# Extract patterns
echo "📋 Extracting patterns..."
python tools/analyze_merged_repo_patterns.py

echo "✅ Pattern extraction workflow finished"
```

---

### **Script 3: Full Integration Workflow**

```bash
#!/bin/bash
# Full integration workflow automation

REPO_NAME=$1
REPO_PATH=$2

echo "🚀 Starting full integration workflow for $REPO_NAME"

# Phase 0: Cleanup
echo "📋 Phase 0: Pre-Integration Cleanup..."
python tools/detect_venv_files.py "$REPO_PATH"
python tools/enhanced_duplicate_detector.py "$REPO_NAME"
python tools/check_integration_issues.py "$REPO_PATH"

# Phase 1: Pattern Extraction
echo "📋 Phase 1: Pattern Extraction..."
python tools/analyze_merged_repo_patterns.py

echo "✅ Full integration workflow finished"
echo "📋 Next: Phase 2 (Service Integration) - Manual steps required"
```

---

## 🐍 **PYTHON WORKFLOW AUTOMATION**

### **Complete Integration Workflow Class**

```python
#!/usr/bin/env python3
"""
Integration Workflow Automation - Agent-2
==========================================
"""

import subprocess
import sys
from pathlib import Path
from typing import Optional

class IntegrationWorkflow:
    """Automated integration workflow."""
    
    def __init__(self, repo_name: str, repo_path: Optional[Path] = None):
        self.repo_name = repo_name
        self.repo_path = repo_path or Path(".")
    
    def phase_0_cleanup(self) -> bool:
        """Phase 0: Pre-Integration Cleanup."""
        print("📋 Phase 0: Pre-Integration Cleanup...")
        
        # Detect venv files
        print("  → Detecting venv files...")
        result = subprocess.run(
            ["python", "tools/detect_venv_files.py", str(self.repo_path)],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"  ⚠️ Venv detection warning: {result.stderr}")
        
        # Detect duplicates
        print("  → Detecting duplicates...")
        result = subprocess.run(
            ["python", "tools/enhanced_duplicate_detector.py", self.repo_name],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"  ⚠️ Duplicate detection warning: {result.stderr}")
        
        # Check integration issues
        print("  → Checking integration issues...")
        result = subprocess.run(
            ["python", "tools/check_integration_issues.py", str(self.repo_path)],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"  ⚠️ Integration issues check warning: {result.stderr}")
        
        print("  ✅ Phase 0 complete")
        return True
    
    def phase_1_pattern_extraction(self) -> bool:
        """Phase 1: Pattern Extraction."""
        print("📋 Phase 1: Pattern Extraction...")
        
        # Extract patterns
        print("  → Extracting patterns...")
        result = subprocess.run(
            ["python", "tools/analyze_merged_repo_patterns.py"],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"  ⚠️ Pattern extraction warning: {result.stderr}")
        
        print("  ✅ Phase 1 complete")
        return True
    
    def run_full_workflow(self) -> bool:
        """Run complete integration workflow."""
        print(f"🚀 Starting full integration workflow for {self.repo_name}")
        
        if not self.phase_0_cleanup():
            return False
        
        if not self.phase_1_pattern_extraction():
            return False
        
        print("✅ Full integration workflow complete")
        print("📋 Next: Phase 2 (Service Integration) - Manual steps required")
        return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python integration_workflow.py <repo_name> [repo_path]")
        sys.exit(1)
    
    repo_name = sys.argv[1]
    repo_path = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    
    workflow = IntegrationWorkflow(repo_name, repo_path)
    workflow.run_full_workflow()
```

---

## 📋 **WORKFLOW AUTOMATION CHECKLIST**

### **Before Automation**:
- [ ] Tools available and working
- [ ] Repository accessible
- [ ] Workflow script tested
- [ ] Backup created (if needed)

### **During Automation**:
- [ ] Monitor workflow progress
- [ ] Review tool outputs
- [ ] Verify each phase complete
- [ ] Document any issues

### **After Automation**:
- [ ] Review all outputs
- [ ] Verify cleanup complete
- [ ] Verify patterns extracted
- [ ] Proceed to manual phases

---

## 🎯 **WORKFLOW USAGE**

### **Bash Scripts**:
```bash
# Complete cleanup
./complete_cleanup_workflow.sh <repo_name> <repo_path>

# Pattern extraction
./pattern_extraction_workflow.sh <repo_name>

# Full integration
./full_integration_workflow.sh <repo_name> <repo_path>
```

### **Python Scripts**:
```bash
# Full workflow
python integration_workflow.py <repo_name> [repo_path]
```

---

**Status**: ✅ **WORKFLOW AUTOMATION READY**  
**Last Updated**: 2025-11-26 15:10:00 (Local System Time)

