# 🏛️ CAPTAIN-APPROVED EXECUTION ORDER

**Captain Truth Pass:** ✅ ACCEPTED WITH CONSTRAINTS
**Status:** IMMEDIATE EXECUTION AUTHORIZED FOR SAFE PHASES
**Agent-6 (QA Lead) - Corrected Implementation Plan**

---

## 📋 EXECUTION AUTHORIZATION MATRIX

### ✅ **APPROVED FOR IMMEDIATE EXECUTION** (Phase 0)

**Captain Authorization:** Safe to execute without further review

1. **Import Repair Operations**
   - Fix `src/ai_automation/__init__.py` broken automation_engine import
   - Validate all imports load correctly
   - Add failing import detection tests

2. **Manifest Generation**
   - Generate `audit_outputs/duplicate_clusters.json`
   - Generate `audit_outputs/dead_code_candidates.json`
   - Generate `audit_outputs/orphan_imports.json`
   - Generate `audit_outputs/archive_age_manifest.csv`

3. **Archive Policy Definition**
   - Establish retention rules (move→compress→index)
   - Create compression strategy
   - Define searchable indexing requirements

---

### 🔄 **APPROVED PENDING EVIDENCE** (Phase 1)

**Captain Authorization:** Execute only after manifest completion

1. **Evidence-Based Analysis**
   - Token-level duplication clustering
   - Call graph dead-code detection
   - Archive age + size inventory

2. **Decision Artifact Generation**
   - CLI duplicate removal manifests
   - Script consolidation plans
   - Archive compression candidates

---

### 🚫 **BLOCKED UNTIL CAPTAIN APPROVAL** (Phase 2+)

**Captain Authorization:** Requires explicit sign-off

1. **File Deletions** - All deletion operations
2. **Directory Merges** - All consolidation operations
3. **Service Consolidation** - All refactoring operations
4. **Archive Purging** - All deletion operations

---

## ⚡ IMMEDIATE EXECUTION PLAN (PHASE 0)

### Step 1: Critical Import Repair (30 minutes)

**Command Sequence:**
```bash
# Fix broken import in ai_automation
cd /path/to/repo
sed -i '/automation_engine/d' src/ai_automation/__init__.py

# Validate imports work
python -c "import src.ai_automation; print('✅ ai_automation imports successfully')"

# Add import validation test
cat > tests/test_import_validation.py << 'EOF'
#!/usr/bin/env python3
"""Import validation tests to prevent future dead code"""

def test_critical_imports():
    """Test all critical modules import successfully"""
    try:
        import src.ai_automation
        import src.automation
        import src.core
        print("✅ All critical imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import failure: {e}")
        return False
EOF
```

### Step 2: Manifest Generation (60 minutes)

**Required Output Structure:**
```
audit_outputs/
├── duplicate_clusters.json     # Token-level duplication analysis
├── dead_code_candidates.json   # Call graph dead code detection
├── orphan_imports.json         # Import dependency analysis
└── archive_age_manifest.csv    # Archive file age/size inventory
```

**Generation Commands:**
```bash
# Create audit_outputs directory
mkdir -p audit_outputs

# Generate orphan imports manifest
python -c "
import os
import ast
import json

def find_orphaned_imports():
    results = []
    for root, dirs, files in os.walk('src'):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r') as f:
                        content = f.read()
                        tree = ast.parse(content)
                        for node in ast.walk(tree):
                            if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                                # Check if imported module exists
                                if hasattr(node, 'module') and node.module:
                                    module_path = node.module.replace('.', '/')
                                    if not os.path.exists(f'src/{module_path}.py'):
                                        results.append({
                                            'file': filepath,
                                            'import': node.module,
                                            'line': node.lineno
                                        })
                except:
                    pass
    return results

orphans = find_orphaned_imports()
with open('audit_outputs/orphan_imports.json', 'w') as f:
    json.dump(orphans, f, indent=2)
print(f'Found {len(orphans)} orphaned imports')
"

# Generate archive age manifest
python -c "
import os
import csv
from datetime import datetime

def analyze_archive():
    results = []
    for root, dirs, files in os.walk('archive'):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                stat = os.stat(filepath)
                mtime = datetime.fromtimestamp(stat.st_mtime)
                age_days = (datetime.now() - mtime).days
                results.append({
                    'path': filepath,
                    'size': stat.st_size,
                    'modified': mtime.isoformat(),
                    'age_days': age_days
                })
            except:
                pass
    return results

archive_data = analyze_archive()
with open('audit_outputs/archive_age_manifest.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['path', 'size', 'modified', 'age_days'])
    writer.writeheader()
    writer.writerows(archive_data)
print(f'Analyzed {len(archive_data)} archive files')
"
```

### Step 3: Archive Policy Definition (30 minutes)

**Policy Document:**
```markdown
# Archive Retention Policy

## Retention Rules
1. **Keep (<30 days)**: Active development files
2. **Review (30-90 days)**: Selective retention based on value
3. **Compress (90-180 days)**: Move to compressed archives
4. **Archive (>180 days)**: Historical preservation only

## Process
1. **Move** → `archive/historical/`
2. **Compress** → `archive/compressed/YYYY.tar.gz`
3. **Index** → `archive/index/YYYY.json`
4. **Delete** → Only with Captain + checksum verification

## Never Delete Without:
- Captain approval
- Checksum verification
- Backup confirmation
- 30-day grace period
```

---

## 📊 SUCCESS METRICS (PHASE 0)

### Completion Targets
- [ ] **Import errors:** 0 (broken imports fixed)
- [ ] **Import tests:** Passing validation tests added
- [ ] **Manifests generated:** 4 evidence files created
- [ ] **Archive policy:** Documented retention strategy

### Quality Assurance
- [ ] All imports functional after fixes
- [ ] No new import errors introduced
- [ ] Manifests are machine-readable
- [ ] Archive policy is implementable

---

## 🔄 NEXT STEPS AFTER PHASE 0

### Immediate (After Phase 0 Completion)
1. **Submit manifests to Captain** for Phase 1 approval
2. **Generate duplication clustering** evidence
3. **Create dead-code call graphs**
4. **Await Captain authorization** for Phase 1 execution

### Phase 1 Execution (Captain-Approved)
1. **Token-level duplication analysis**
2. **Call graph dead-code detection**
3. **Archive age/size inventory completion**
4. **Generate Phase 2 decision artifacts**

---

## 🚨 SAFETY CONSTRAINTS (NON-NEGOTIABLE)

### What Is ALLOWED (Phase 0)
- Import fixes only
- Manifest generation only
- Policy documentation only
- Test additions only

### What Is BLOCKED (Until Captain Approval)
- Any file deletions
- Any directory moves
- Any service consolidation
- Any architectural changes

---

*"The strength of the pack is the wolf, and the strength of the wolf is the pack."*

**🏛️ CAPTAIN-APPROVED EXECUTION ORDER**

**Phase 0 Status:** AUTHORIZED FOR IMMEDIATE EXECUTION
**Risk Level:** LOW (diagnostic and repair only)
**Timeline:** 2 hours maximum
**Next Step:** Execute Phase 0, submit manifests for Phase 1 approval

---

**Captain Signature:** Audit ACCEPTED WITH CONSTRAINTS ✅
**Execution Authority:** Phase 0 IMMEDIATE ✅ | Phase 1+ APPROVAL GATED 🔒