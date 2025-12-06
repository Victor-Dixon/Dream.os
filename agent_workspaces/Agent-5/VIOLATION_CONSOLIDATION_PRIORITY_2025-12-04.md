# 🎯 VIOLATION CONSOLIDATION PRIORITY PLAN
**Agent-5 Business Intelligence Analysis**  
**Date**: 2025-12-04  
**Total Violations**: 1,415

---

## 📊 EXECUTIVE SUMMARY

**Violation Breakdown:**
- **SSOT Violations**: 56 (HIGHEST IMPACT - Configuration drift)
- **Identical Code Blocks**: 88 (HIGH IMPACT - Maintenance burden)
- **Duplicate Class Names**: 218 (MEDIUM-HIGH IMPACT - Import confusion)
- **Duplicate Function Names**: 1,001 (MEDIUM IMPACT - Context-dependent)
- **Duplicate Filenames**: 52 (LOW-MEDIUM IMPACT - Mostly expected `__init__.py`)

**Priority Order**: SSOT → Code Blocks → Classes → Functions → Filenames

---

## 🚨 TIER 1: CRITICAL SSOT VIOLATIONS (56 violations)

### **Priority 1.1: Timeout Constants (175 + 69 + 53 + 45 + 33 + 29 = 404 instances)**

**Impact**: Configuration drift, inconsistent behavior, maintenance nightmare

#### **1.1.1: `timeout=30` (175 locations) - HIGHEST PRIORITY**
**SSOT Target**: `src/core/config/timeout_constants.py` (CREATE)

**Consolidation Strategy**:
```python
# src/core/config/timeout_constants.py
class TimeoutConstants:
    """SSOT for all timeout values across the system."""
    HTTP_DEFAULT = 30
    HTTP_SHORT = 10
    HTTP_MEDIUM = 60
    HTTP_LONG = 120
    HTTP_EXTENDED = 300
    HTTP_QUICK = 5
```

**Affected Files** (Top 10 by frequency):
1. `tools/repo_safe_merge.py` (17 instances)
2. `tools/resolve_merge_conflicts.py` (14 instances)
3. `tools/resolve_pr_conflicts.py` (14 instances)
4. `src/core/merge_conflict_resolver.py` (10 instances)
5. `tools/complete_merge_into_main.py` (6 instances)
6. `tools/verify_merges.py` (6 instances)
7. `tools/git_based_merge_primary.py` (5 instances)
8. `tools/force_push_consolidations.py` (5 instances)
9. `tools/complete_batch2_remaining_merges.py` (5 instances)
10. `tools/merge_dreambank_pr1_via_git.py` (7 instances)

**Action Plan**:
1. Create `src/core/config/timeout_constants.py`
2. Replace all hardcoded `timeout=30` with `TimeoutConstants.HTTP_DEFAULT`
3. Replace `timeout=10` with `TimeoutConstants.HTTP_SHORT`
4. Replace `timeout=60` with `TimeoutConstants.HTTP_MEDIUM`
5. Replace `timeout=120` with `TimeoutConstants.HTTP_LONG`
6. Replace `timeout=300` with `TimeoutConstants.HTTP_EXTENDED`
7. Replace `timeout=5` with `TimeoutConstants.HTTP_QUICK`

**Estimated Impact**: 
- **Files Affected**: ~150 files
- **Lines Changed**: ~400 lines
- **Risk**: LOW (simple find/replace with import)
- **Time Estimate**: 4-6 hours

#### **1.1.2: Port Configuration (37 + 25 = 62 instances)**
**SSOT Target**: `src/core/config/port_constants.py` (CREATE)

**Consolidation Strategy**:
```python
# src/core/config/port_constants.py
class PortConstants:
    """SSOT for all port configurations."""
    DEFAULT_PORT = 8000
    API_PORT = 8080
    # ... define standard ports
```

**Action Plan**:
1. Create port constants file
2. Replace hardcoded `port=` values
3. Update all affected files

**Estimated Impact**: 37 files, ~60 lines

---

## 🔧 TIER 2: IDENTICAL CODE BLOCKS (88 violations)

### **Priority 2.1: Agent List Duplication (5 occurrences)**

**Block Hash**: `dd569d8d`  
**Locations**:
- `src/core/messaging_core.py:352`
- `src/services/messaging_infrastructure.py:1228`
- `tools/captain_check_agent_status.py:69`

**Consolidation Strategy**:
```python
# src/core/constants/agent_constants.py
AGENT_LIST = [
    "Agent-1",
    "Agent-2",
    "Agent-3",
    "Agent-4",
    "Agent-5",
    "Agent-6",
    "Agent-7",
    "Agent-8",
]
```

**Action Plan**:
1. Create `src/core/constants/agent_constants.py`
2. Replace all hardcoded agent lists
3. Update imports

**Estimated Impact**: 5 files, ~15 lines

### **Priority 2.2: Validation Error Printing (6 occurrences)**

**Block Hash**: `1b58ef4a`  
**Locations**:
- `tools/communication/message_validator.py:177`
- `tools/communication/coordination_validator.py:184`
- `tools/communication/multi_agent_validator.py:115`

**Consolidation Strategy**:
```python
# src/core/utils/validation_utils.py
def print_validation_results(validator):
    """Print validation errors and warnings."""
    if validator.errors:
        print("❌ VALIDATION ERRORS:")
        for error in validator.errors:
            print(f"  • {error}")
    if validator.warnings:
        print("⚠️  WARNINGS:")
        for warning in validator.warnings:
            print(f"  • {warning}")
```

**Action Plan**:
1. Create utility function
2. Replace duplicate blocks
3. Update all validators

**Estimated Impact**: 6 files, ~30 lines

### **Priority 2.3: GitHub Token Extraction (3 occurrences)**

**Block Hash**: `7a8778c5`  
**Locations**:
- `tools/repo_safe_merge.py:83`
- `tools/git_based_merge_primary.py:34`
- `tools/repo_safe_merge_v2.py:49`

**Consolidation Strategy**:
```python
# src/core/utils/github_utils.py
def get_github_token_from_env():
    """Extract GitHub token from .env file."""
    env_file = project_root / ".env"
    if env_file.exists():
        # ... consolidated logic
```

**Action Plan**:
1. Create utility function
2. Replace duplicate blocks

**Estimated Impact**: 3 files, ~20 lines

---

## 📦 TIER 3: DUPLICATE CLASS NAMES (218 violations)

### **Priority 3.1: Task Class (10 locations) - HIGHEST IMPACT**

**Locations**:
1. `src/domain/entities/task.py:16` ⭐ **PRIMARY SSOT**
2. `src/gaming/dreamos/fsm_models.py:35`
3. `src/gaming/dreamos/fsm_orchestrator.py:28`
4. `src/infrastructure/persistence/persistence_models.py:46`
5. `src/orchestrators/overnight/scheduler_models.py:19`
6. `src/services/contract_system/models.py:44`
7. `tools/autonomous_task_engine.py:23`
8. `tools/markov_task_optimizer.py:19`
9. `tools/autonomous/task_models.py:18`
10. `tools_v2/categories/autonomous_workflow_tools.py:32`

**Consolidation Strategy**:
- **Primary**: `src/domain/entities/task.py` (Domain entity - SSOT)
- **Rename others**:
  - `fsm_models.py` → `FSMTask` or import from domain
  - `persistence_models.py` → `TaskPersistenceModel` or use domain entity
  - `scheduler_models.py` → `ScheduledTask` or import from domain
  - `contract_system/models.py` → `ContractTask` or import from domain
  - Tool files → Import from domain or rename to `ToolTask`

**Action Plan**:
1. Audit each `Task` class to determine if it's truly different
2. If same domain concept → Import from `src/domain/entities/task.py`
3. If different concept → Rename to be specific (e.g., `FSMTask`, `ScheduledTask`)
4. Update all imports

**Estimated Impact**: 10 files, ~200 lines of changes

### **Priority 3.2: SearchResult Class (7 locations)**

**Locations**:
1. `src/core/vector_database.py:39` ⭐ **PRIMARY SSOT**
2. `src/core/vector_database.py:215` (duplicate in same file!)
3. `src/core/intelligent_context/context_results.py:24`
4. `src/core/intelligent_context/search_models.py:21`
5. `src/core/intelligent_context/unified_intelligent_context/models.py:48`
6. `src/services/models/vector_models.py:104`
7. `src/web/vector_database/models.py:75`

**Consolidation Strategy**:
- **Primary**: `src/services/models/vector_models.py` (Service layer model)
- Consolidate all to single model
- Update imports across codebase

**Action Plan**:
1. Choose primary model location
2. Consolidate implementations
3. Update all imports
4. Remove duplicates

**Estimated Impact**: 7 files, ~150 lines

### **Priority 3.3: SearchQuery Class (7 locations)**

**Locations**:
1. `src/core/vector_database.py:196` ⭐ **PRIMARY SSOT**
2. `src/services/agent_management.py:46`
3. `src/services/learning_recommender.py:34`
4. `src/services/performance_analyzer.py:32`
5. `src/services/recommendation_engine.py:32`
6. `src/services/swarm_intelligence_manager.py:32`
7. `src/services/models/vector_models.py:93`

**Consolidation Strategy**:
- **Primary**: `src/services/models/vector_models.py` (Service layer model)
- All service files should import from this location

**Action Plan**:
1. Consolidate to `src/services/models/vector_models.py`
2. Update all service imports
3. Remove duplicates

**Estimated Impact**: 7 files, ~100 lines

### **Priority 3.4: Config Class (5 locations)**

**Locations**:
1. `src/ai_training/dreamvault/config.py:11`
2. `src/message_task/schemas.py:28`
3. `src/message_task/schemas.py:47`
4. `src/message_task/schemas.py:75`
5. `src/message_task/schemas.py:92`

**Consolidation Strategy**:
- These appear to be different configs for different domains
- Rename to be specific:
  - `DreamvaultConfig`
  - `MessageTaskConfig` (consolidate 4 in schemas.py)

**Action Plan**:
1. Rename to domain-specific names
2. Consolidate duplicates in `schemas.py`

**Estimated Impact**: 2 files, ~50 lines

---

## 🔄 TIER 4: DUPLICATE FUNCTION NAMES (1,001 violations)

### **Priority 4.1: main() Function (401 locations)**

**Analysis**: Most are legitimate (CLI entry points). Focus on **identical implementations**.

**Identical Implementations Found**:
- `hard_onboard_agent4.py:14` (251 lines)
- `onboard_survey_agents.py:63` (63 lines)
- `simple_agent_onboarding.py:198` (67 lines)

**Action Plan**:
1. Consolidate onboarding scripts
2. Create unified onboarding CLI
3. Remove duplicate implementations

**Estimated Impact**: 3 files, ~380 lines

### **Priority 4.2: validate() Function (170 locations, 10 identical)**

**Identical Implementations**:
- `src/discord_commander/discord_models.py:81` (4 lines)
- `src/core/coordinator_models.py:191` (6 lines)
- `src/core/analytics/models/coordination_analytics_models.py:108` (9 lines)
- `src/core/config/config_manager.py:147` (19 lines)

**Consolidation Strategy**:
```python
# src/core/utils/validation_utils.py
def validate_model(model, schema):
    """Generic model validation."""
    # Consolidated validation logic
```

**Action Plan**:
1. Create generic validation utility
2. Replace identical implementations
3. Keep domain-specific validators separate

**Estimated Impact**: 10 files, ~50 lines

### **Priority 4.3: to_dict() Function (88 locations, 14 identical)**

**Identical Implementations**:
- `src/discord_commander/discord_models.py:99` (9 lines)
- `src/core/coordinator_models.py:84` (10 lines)
- `src/core/coordinator_models.py:109` (10 lines)
- `src/core/coordinator_models.py:139` (15 lines)

**Consolidation Strategy**:
- Use dataclasses or Pydantic models (auto `to_dict()`)
- Create base class with `to_dict()` method
- Or use `dataclasses.asdict()`

**Action Plan**:
1. Audit which models can use dataclasses
2. Create base model class
3. Replace identical implementations

**Estimated Impact**: 14 files, ~150 lines

### **Priority 4.4: get_github_token() Function (29 locations, 6 identical)**

**Identical Implementations**:
- `tools/github_create_and_push_repo.py:27` (18 lines)
- `tools/fetch_repo_names.py:26` (13 lines)
- `tools/repo_safe_merge.py:75` (19 lines)
- `tools/get_repo_chronology.py:30` (11 lines)
- `tools/verify_merges.py:95` (2 lines)

**Consolidation Strategy**:
```python
# src/core/utils/github_utils.py
def get_github_token():
    """Get GitHub token from environment or .env file."""
    # Consolidated logic
```

**Action Plan**:
1. Create utility function
2. Replace all duplicates
3. Update imports

**Estimated Impact**: 6 files, ~80 lines

---

## 📁 TIER 5: DUPLICATE FILENAMES (52 violations)

### **Priority 5.1: models.py (10 locations)**

**Locations**:
1. `agent_workspaces/Agent-2/extracted_logic/ai_framework/models/src/dreamscape/core/mmorpg/models.py`
2. `agent_workspaces/Agent-2/extracted_logic/ai_framework/models/src/dreamscape/core/models.py`
3. `agent_workspaces/Agent-2/extracted_logic/ai_framework/models/src/dreamscape/tools_db/models.py`
4. `src/core/intelligent_context/unified_intelligent_context/models.py`
5. `src/core/ssot/unified_ssot/models.py`
6. `src/core/vector_strategic_oversight/unified_strategic_oversight/models.py`
7. `src/gaming/integration/models.py`
8. `src/services/contract_system/models.py`
9. `src/web/vector_database/models.py`
10. `src/workflows/models.py`

**Analysis**: These are in different domains/modules, so naming is acceptable. However, we should:
1. Ensure no duplicate classes within these files
2. Consider more specific names if modules are related

**Action Plan**: LOW PRIORITY - Review for actual conflicts only

### **Priority 5.2: config.py (4 locations)**

**Locations**:
1. `config.py` (root)
2. `src/ai_training/dreamvault/config.py`
3. `src/services/config.py`
4. `src/shared_utils/config.py`

**Action Plan**: 
1. Consolidate root `config.py` with appropriate module
2. Rename domain-specific configs if needed

**Estimated Impact**: 4 files, ~50 lines

---

## 🎯 CONSOLIDATION ROADMAP

### **Phase 1: SSOT Violations (Week 1)**
- [ ] Create `src/core/config/timeout_constants.py`
- [ ] Replace all `timeout=30` (175 files)
- [ ] Replace all `timeout=10` (69 files)
- [ ] Replace all `timeout=60` (53 files)
- [ ] Replace all `timeout=120` (45 files)
- [ ] Replace all `timeout=300` (33 files)
- [ ] Replace all `timeout=5` (29 files)
- [ ] Create `src/core/config/port_constants.py`
- [ ] Replace port configurations

**Estimated Time**: 6-8 hours  
**Risk**: LOW  
**Impact**: HIGH (prevents configuration drift)

### **Phase 2: Identical Code Blocks (Week 1-2)**
- [ ] Create `src/core/constants/agent_constants.py`
- [ ] Replace agent list duplicates (5 files)
- [ ] Create `src/core/utils/validation_utils.py`
- [ ] Replace validation printing (6 files)
- [ ] Create `src/core/utils/github_utils.py`
- [ ] Replace GitHub token extraction (3 files)
- [ ] Replace other identical blocks (74 remaining)

**Estimated Time**: 8-10 hours  
**Risk**: LOW-MEDIUM  
**Impact**: MEDIUM-HIGH (reduces maintenance burden)

### **Phase 3: Duplicate Classes (Week 2-3)**
- [ ] Consolidate `Task` class (10 files)
- [ ] Consolidate `SearchResult` class (7 files)
- [ ] Consolidate `SearchQuery` class (7 files)
- [ ] Rename `Config` classes (5 files)
- [ ] Address other high-frequency duplicates

**Estimated Time**: 12-16 hours  
**Risk**: MEDIUM (requires careful import updates)  
**Impact**: MEDIUM-HIGH (reduces import confusion)

### **Phase 4: Duplicate Functions (Week 3-4)**
- [ ] Consolidate identical `validate()` implementations (10 files)
- [ ] Consolidate identical `to_dict()` implementations (14 files)
- [ ] Consolidate identical `get_github_token()` implementations (6 files)
- [ ] Review other high-frequency duplicates

**Estimated Time**: 10-12 hours  
**Risk**: MEDIUM  
**Impact**: MEDIUM (improves code reuse)

### **Phase 5: Filename Review (Week 4)**
- [ ] Review `models.py` conflicts
- [ ] Consolidate `config.py` files
- [ ] Address other filename conflicts

**Estimated Time**: 4-6 hours  
**Risk**: LOW  
**Impact**: LOW-MEDIUM

---

## 📊 SUCCESS METRICS

**Before Consolidation**:
- SSOT Violations: 56
- Identical Code Blocks: 88
- Duplicate Classes: 218
- Duplicate Functions: 1,001
- Duplicate Filenames: 52
- **Total**: 1,415 violations

**Target After Phase 1-2**:
- SSOT Violations: 0 (100% reduction)
- Identical Code Blocks: <20 (77% reduction)
- Duplicate Classes: 150 (31% reduction)
- Duplicate Functions: 950 (5% reduction)
- Duplicate Filenames: 52 (0% - acceptable)
- **Total**: ~1,172 violations (17% reduction)

**Target After All Phases**:
- SSOT Violations: 0 (100% reduction)
- Identical Code Blocks: <10 (89% reduction)
- Duplicate Classes: <100 (54% reduction)
- Duplicate Functions: <800 (20% reduction)
- Duplicate Filenames: <30 (42% reduction)
- **Total**: ~840 violations (41% reduction)

---

## 🚨 RISK ASSESSMENT

### **High Risk Items**:
1. **Class Consolidation**: Breaking changes to imports
   - **Mitigation**: Use deprecation warnings, gradual migration
2. **Function Consolidation**: Potential behavior differences
   - **Mitigation**: Comprehensive testing before consolidation

### **Low Risk Items**:
1. **SSOT Constants**: Simple find/replace
2. **Code Block Extraction**: Utility functions, easy to test

---

## 📝 NEXT STEPS

1. **Immediate**: Create SSOT constant files
2. **This Week**: Begin Phase 1 (SSOT violations)
3. **Next Week**: Begin Phase 2 (Code blocks)
4. **Ongoing**: Monitor for new violations

---

**Report Generated By**: Agent-5 (Business Intelligence Specialist)  
**Date**: 2025-12-04  
**Status**: READY FOR EXECUTION

🐝 WE. ARE. SWARM. ⚡🔥


