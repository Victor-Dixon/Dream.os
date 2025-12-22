# SSOT Tools for Agents - Quick Reference

**Date**: 2025-12-03  
**Maintained By**: Agent-8 (QA SSOT Domain Owner)  
**Purpose**: Document available SSOT validation tools for all agents

---

## 🎯 **QUICK START**

Each agent can use these tools to verify SSOT compliance in their domain.

---

## 📋 **AVAILABLE SSOT TOOLS**

### **1. SSOT Validator** (`tools/ssot_validator.py`)
**Purpose**: Check documentation-code alignment  
**Use Case**: Verify documented features exist in code

**Usage**:
```bash
python tools/ssot_validator.py --code <file.py> --docs <doc1.md> <doc2.md>
```

**What it checks**:
- CLI flags in code vs documentation
- Undocumented features
- Documented features that don't exist

---

### **2. Import Chain Validator** (`tools/import_chain_validator.py`)
**Purpose**: Validate import paths and find broken imports  
**Use Case**: Verify imports work correctly after consolidation

**Usage**:
```bash
python tools/import_chain_validator.py <file.py> --fix-suggestions
```

**What it checks**:
- Import statements work
- Missing modules
- Broken import paths

---

### **3. Captain Import Validator** (`tools/captain_import_validator.py`)
**Purpose**: Comprehensive import validation  
**Use Case**: Full import chain validation

**Usage**:
```bash
python tools/captain_import_validator.py <file.py>
```

---

### **4. SSOT Validation Tools** (`tools/categories/ssot_validation_tools.py`)
**Purpose**: SSOT violation detection and enforcement  
**Use Case**: Detect duplicates, scattered configs, multiple repositories

**Available Checks**:
- Duplicate classes
- Duplicate functions
- Multiple repositories
- Scattered configuration
- Duplicate constants

**Usage** (via toolbelt):
```python
from tools.categories.ssot_validation_tools import SSOTViolationDetector

detector = SSOTViolationDetector()
result = detector.execute({"directory": "src"})
```

---

### **5. Batch 2 SSOT Verifier** (`tools/batch2_ssot_verifier.py`)
**Purpose**: Verify SSOT after repository merges  
**Use Case**: Post-merge SSOT verification

**Usage**:
```bash
# Verify after merge
python tools/batch2_ssot_verifier.py --merge "source -> target"

# Verify master list
python tools/batch2_ssot_verifier.py --verify-master-list

# Full verification
python tools/batch2_ssot_verifier.py --full
```

---

## 🎯 **AGENT-SPECIFIC GUIDANCE**

### **Agent-1: Integration SSOT**
**Tools to use**:
- `import_chain_validator.py` - Verify messaging/integration imports
- `ssot_validator.py` - Check integration docs vs code

**Common checks**:
- Messaging service imports
- Integration pattern documentation
- Core system SSOT compliance

---

### **Agent-2: Architecture SSOT**
**Tools to use**:
- `ssot_validation_tools.py` - Detect duplicate patterns
- `ssot_validator.py` - Verify architecture docs

**Common checks**:
- Duplicate design patterns
- Scattered architectural decisions
- PR management SSOT

---

### **Agent-3: Infrastructure SSOT**
**Tools to use**:
- `import_chain_validator.py` - Verify deployment tool imports
- `batch2_ssot_verifier.py` - Verify consolidation SSOT

**Common checks**:
- DevOps tool imports
- CI/CD configuration SSOT
- Deployment tool consolidation

---

### **Agent-5: Analytics SSOT**
**Tools to use**:
- `ssot_validation_tools.py` - Detect duplicate metrics
- `ssot_validator.py` - Verify analytics docs

**Common checks**:
- Duplicate metric definitions
- Scattered analytics configs
- BI system SSOT

---

### **Agent-6: Communication SSOT**
**Tools to use**:
- `import_chain_validator.py` - Verify messaging protocol imports
- `ssot_validator.py` - Check communication docs

**Common checks**:
- Messaging protocol imports
- Coordination system SSOT
- Swarm status SSOT

---

### **Agent-7: Web SSOT**
**Tools to use**:
- `import_chain_validator.py` - Verify web framework imports
- `ssot_validator.py` - Check web docs

**Common checks**:
- Web framework imports
- Frontend/backend pattern SSOT
- Discord integration SSOT

---

### **Agent-8: QA SSOT**
**Tools to use**:
- All tools (QA SSOT domain owner)
- Provides tools to other agents
- Maintains test infrastructure SSOT

---

## 📝 **SSOT VERIFICATION CHECKLIST**

Before declaring SSOT compliance, verify:

- [ ] **Code Imports**: No broken imports after consolidation
- [ ] **Documentation**: Docs match code (use `ssot_validator.py`)
- [ ] **Duplicates**: No duplicate functionality (use `ssot_validation_tools.py`)
- [ ] **References**: No references to archived/removed code
- [ ] **Toolbelt**: Toolbelt registry doesn't reference archived tools
- [ ] **CLI**: No CLI entry points reference archived tools

---

## 🚨 **WHEN TO ESCALATE**

Escalate to Captain (Agent-4) if:
- Cross-domain SSOT violation
- High-priority violation requiring immediate attention
- Disagreement on SSOT location
- Violation affecting multiple agents

---

## 📚 **ADDITIONAL RESOURCES**

- **SSOT Protocol**: `runtime/agent_comms/SSOT_PROTOCOL.md`
- **SSOT Domain Assignments**: `agent_workspaces/Agent-4/SSOT_DOMAIN_ASSIGNMENTS.md`
- **QA SSOT Tools**: `tools/categories/ssot_validation_tools.py`

---

## 💡 **BEST PRACTICES**

1. **Run SSOT checks before consolidation** - Catch issues early
2. **Verify after each change** - Maintain SSOT compliance
3. **Document SSOT decisions** - Help other agents understand
4. **Use appropriate tool** - Match tool to your domain needs
5. **Report violations** - Notify domain owner or Captain

---

**Maintained By**: Agent-8 (QA SSOT Domain Owner)  
**Last Updated**: 2025-12-03  
**Questions?** Contact Agent-8 or Captain (Agent-4)

🐝 **WE. ARE. SWARM. ⚡🔥**


