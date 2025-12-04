# Integration Tools Usage Guide

**Date**: 2025-11-26  
**Created By**: Agent-2 (Architecture & Design Specialist)  
**Status**: ✅ **TOOL GUIDE READY**  
**For**: Swarm-wide tool usage

---

## 🛠️ **AVAILABLE TOOLS**

### **1. Enhanced Duplicate Detector**
**File**: `tools/enhanced_duplicate_detector.py`  
**Created By**: Agent-2

**Purpose**: Detect duplicate files using content-based (SHA256) and name-based detection.

**Usage**:
```bash
python tools/enhanced_duplicate_detector.py [repo_name]
```

**Features**:
- Content-based duplicate detection (SHA256 hashing)
- Name-based duplicate detection
- SSOT version determination
- Enhanced reporting

**Output**:
- List of duplicate files
- SSOT version recommendations
- Duplicate categories
- Resolution suggestions

**When to Use**:
- Before integration (Phase 0)
- After merging repos
- When cleaning up duplicates

---

### **2. Virtual Environment File Detector**
**File**: `tools/detect_venv_files.py`  
**Created By**: Agent-5

**Purpose**: Detect virtual environment files that shouldn't be in repository.

**Usage**:
```bash
python tools/detect_venv_files.py [repo_path]
```

**Features**:
- Detects venv patterns
- Lists venv files
- Suggests .gitignore updates

**Output**:
- List of venv files
- .gitignore suggestions
- Cleanup recommendations

**When to Use**:
- Before integration (Phase 0)
- When cleaning up repos
- Before committing changes

---

### **3. Integration Validator** (Consolidated Tool)
**File**: `tools/communication/integration_validator.py`  
**Created By**: Agent-6 (consolidates `check_integration_issues.py` + `integration_health_checker.py`)

**Purpose**: Unified integration validator - checks integration issues, health, and readiness for merged repos.

**Usage**:
```bash
python tools/communication/integration_validator.py --repo-path [repo_path]
# Or via toolbelt:
agent_toolbelt --check-integration [repo_path]
```

**Features**:
- Detects integration issues (venv, duplicates, code duplication)
- Validates repository state (git cleanliness)
- Checks integration readiness (tools, docs)
- Validates integration environment

**Output**:
- List of integration issues
- Repository state validation
- Integration readiness assessment
- Environment validation

**When to Use**:
- After merging repos
- Before integration
- When troubleshooting
- Validating integration environment

---

### **4. Pattern Analyzer**
**File**: `tools/analyze_merged_repo_patterns.py`  
**Created By**: Agent-2

**Purpose**: Extract patterns from merged repositories.

**Usage**:
```bash
python tools/analyze_merged_repo_patterns.py
```

**Features**:
- Pattern extraction
- Pattern categorization
- Integration point identification

**Output**:
- Extracted patterns
- Pattern categories
- Integration recommendations

**When to Use**:
- Phase 1: Pattern Extraction
- Before service integration
- When planning integration

---

### **5. Service Integration Template**
**File**: `agent_workspaces/Agent-2/SERVICE_INTEGRATION_TEMPLATE.md`  
**Created By**: Agent-2

**Purpose**: Step-by-step service integration template.

**Usage**:
- Copy template for each service integration
- Follow step-by-step process
- Document decisions

**Features**:
- Service analysis checklist
- Service enhancement planning
- Implementation steps
- Testing requirements

**When to Use**:
- Phase 2: Service Integration
- When enhancing services
- When creating new services

---

## 📋 **TOOL WORKFLOW**

### **Phase 0: Pre-Integration Cleanup**

**Tool Sequence**:
1. `detect_venv_files.py` - Detect venv files
2. `enhanced_duplicate_detector.py` - Detect duplicates
3. Cleanup scripts - Remove venv and duplicates
4. `tools/communication/integration_validator.py` - Unified integration validation (consolidates check_integration_issues.py + integration_health_checker.py)

---

### **Phase 1: Pattern Extraction**

**Tool Sequence**:
1. `analyze_merged_repo_patterns.py` - Extract patterns
2. Document patterns
3. Map patterns to services

---

### **Phase 2: Service Integration**

**Tool Sequence**:
1. Use `SERVICE_INTEGRATION_TEMPLATE.md`
2. Review existing services
3. Enhance services
4. Test integration

---

## 🎯 **TOOL SELECTION GUIDE**

### **For Duplicate Detection**:
- **Name-based duplicates**: `enhanced_duplicate_detector.py`
- **Content-based duplicates**: `enhanced_duplicate_detector.py`
- **SSOT determination**: `enhanced_duplicate_detector.py`

### **For Cleanup**:
- **Venv files**: `detect_venv_files.py` + cleanup scripts
- **Duplicates**: `enhanced_duplicate_detector.py` + resolution scripts

### **For Integration**:
- **Pattern extraction**: `analyze_merged_repo_patterns.py`
- **Service integration**: `SERVICE_INTEGRATION_TEMPLATE.md`
- **Issue checking**: `tools/communication/integration_validator.py` (unified validator)

---

## 📊 **TOOL COMBINATIONS**

### **Complete Integration Workflow**:
1. `detect_venv_files.py` → Cleanup venv
2. `enhanced_duplicate_detector.py` → Resolve duplicates
3. `tools/communication/integration_validator.py` → Unified integration validation
4. `analyze_merged_repo_patterns.py` → Extract patterns
5. `SERVICE_INTEGRATION_TEMPLATE.md` → Integrate services

---

## ✅ **BEST PRACTICES**

### **Tool Usage**:
- ✅ Run tools in correct sequence
- ✅ Document tool outputs
- ✅ Use tools before manual work
- ✅ Verify tool results

### **Tool Maintenance**:
- ✅ Keep tools updated
- ✅ Share tool improvements
- ✅ Document tool changes
- ✅ Test tools regularly

---

**Status**: ✅ **TOOL GUIDE READY**  
**Last Updated**: 2025-11-26 14:20:00 (Local System Time)

