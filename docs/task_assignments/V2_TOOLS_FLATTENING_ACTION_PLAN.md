# 🛠️ V2 Tools Flattening - Action Plan

**From**: Agent-4 (Captain - Strategic Oversight)  
**Date**: 2025-01-27  
**Priority**: HIGH  
**Status**: COORDINATED EFFORT

---

## 📊 CURRENT STATE ANALYSIS

### **tools_v2/ Status** ✅
- **Total Tools Registered**: 100+ tools
- **Categories**: 40+ category files
- **V2 Compliance**: ✅ All files ≤400 lines
- **Architecture**: Adapter pattern, well-organized
- **Registry**: Centralized in `tool_registry.py`

### **tools/ Directory Status** ⚠️
- **Total Files**: 167+ files
- **Issues**: Duplicates, scattered tools, legacy implementations
- **Migration Needed**: Many tools need adapters in tools_v2/

---

## 🎯 FLATTENING OBJECTIVES

1. **Consolidate Duplicate Tools**
   - Identify and remove duplicates
   - Migrate unique functionality to tools_v2/
   - Deprecate legacy implementations

2. **Complete Tool Migration**
   - Ensure all active tools have tools_v2/ adapters
   - Remove orphaned tools from tools/
   - Update all references to use tools_v2/

3. **Maintain SSOT**
   - tools_v2/ is the single source of truth
   - All tools accessible through unified interface
   - Clear migration path documented

---

## 📋 MIGRATION PRIORITIES

### **Priority 1: Critical Duplicates** (Immediate)

#### **A. Project Scanner Tools**
- **Current**: `tools/projectscanner*.py` (multiple files)
- **Status**: Already has adapter in `tools_v2/categories/analysis_tools.py`
- **Action**: Verify adapter completeness, deprecate legacy if complete

#### **B. V2 Compliance Tools**
- **Current**: `tools/v2_checker*.py`, `tools/v2_compliance_checker.py`
- **Status**: Already has adapter in `tools_v2/categories/v2_tools.py`
- **Action**: Verify adapter completeness, deprecate legacy if complete

#### **C. Quick Line Counter**
- **Current**: `tools/quick_linecount.py`, `tools/quick_line_counter.py`
- **Status**: Has adapter in `tools_v2/categories/import_fix_tools.py` (refactor.quick_line_count)
- **Action**: Remove duplicate, ensure single source

### **Priority 2: Captain Tools Consolidation**

#### **Current State**
- 15+ `captain_*.py` files in `tools/`
- Some already migrated to `tools_v2/categories/captain_*.py`

#### **Migration Status**
- ✅ `captain_tools.py` - Core operations
- ✅ `captain_tools_advanced.py` - Complex operations
- ✅ `captain_tools_extension.py` - Specialized operations
- ✅ `captain_coordination_tools.py` - Coordination operations

#### **Action Required**
- Audit remaining `captain_*.py` files in `tools/`
- Migrate any missing functionality
- Deprecate legacy files

### **Priority 3: Executor Tools**

#### **Current State**
- `tools/toolbelt/executors/` - 8 executor modules
- These are wrappers, not direct tools

#### **Action Required**
- Verify all executor functionality has tools_v2/ adapters
- Keep executors as backward compatibility layer if needed
- Document migration path

### **Priority 4: Analysis Tools**

#### **Current State**
- Multiple analysis tools in `tools/analysis/`
- Some have adapters, some don't

#### **Action Required**
- Audit `tools/analysis/` directory
- Create adapters for missing tools
- Migrate to `tools_v2/categories/analysis_tools.py`

---

## 🔧 MIGRATION PROCESS

### **Step 1: Audit & Identify**
1. List all tools in `tools/` directory
2. Check if adapter exists in `tools_v2/`
3. Identify duplicates and orphans
4. Prioritize by usage and importance

### **Step 2: Create Adapters**
1. Follow adapter pattern from existing tools
2. Implement `IToolAdapter` interface
3. Add to `tool_registry.py`
4. Test adapter functionality

### **Step 3: Update References**
1. Find all references to legacy tools
2. Update to use tools_v2/ adapters
3. Test updated references

### **Step 4: Deprecate Legacy**
1. Mark legacy files as deprecated
2. Add deprecation notices
3. Remove after migration period

---

## 👥 AGENT ASSIGNMENTS

### **Agent-1** (Integration & Core Systems)
- **Focus**: Core tools and integration tools
- **Tasks**:
  - Audit `tools/integration/` tools
  - Verify integration adapters in `tools_v2/categories/integration_tools.py`
  - Migrate any missing core tools

### **Agent-2** (Architecture & Design)
- **Focus**: Architecture and design tools
- **Tasks**:
  - Review tool architecture
  - Ensure adapter pattern consistency
  - Document migration patterns

### **Agent-3** (Infrastructure & DevOps)
- **Focus**: Infrastructure tools
- **Status**: ✅ Already working on this (2/8-10 completed)
- **Tasks**:
  - Continue infrastructure tool migration
  - Complete remaining 6-8 tools

### **Agent-5** (Business Intelligence)
- **Focus**: BI and metrics tools
- **Status**: ✅ Already has adapters in `tools_v2/categories/bi_tools.py`
- **Tasks**:
  - Verify adapter completeness
  - Deprecate legacy BI tools if complete

### **Agent-6** (Coordination & Communication)
- **Focus**: Coordination tools
- **Tasks**:
  - Audit coordination tools
  - Verify adapters in `tools_v2/categories/coordination_tools.py`

### **Agent-7** (Web Development)
- **Focus**: Web and dashboard tools
- **Status**: ✅ Already has adapters in `tools_v2/categories/dashboard_tools.py`
- **Tasks**:
  - Verify adapter completeness
  - Review tool registry organization

### **Agent-8** (SSOT & System Integration)
- **Focus**: SSOT violations and consolidation
- **Tasks**:
  - Identify SSOT violations
  - Create consolidation roadmap
  - Ensure single source of truth

---

## 📊 SUCCESS CRITERIA

### **Completion Metrics**
- ✅ All active tools have tools_v2/ adapters
- ✅ No duplicate tool implementations
- ✅ All references updated to use tools_v2/
- ✅ Legacy tools properly deprecated
- ✅ Documentation updated

### **Quality Metrics**
- ✅ All adapters follow IToolAdapter interface
- ✅ All tools registered in tool_registry.py
- ✅ All files V2 compliant (≤400 lines)
- ✅ Comprehensive test coverage

---

## 🚀 NEXT STEPS

1. **Immediate** (This Cycle):
   - Agents acknowledge and start audits
   - Identify high-priority duplicates
   - Create initial migration list

2. **Short-term** (2-3 Cycles):
   - Complete critical duplicate migrations
   - Create adapters for missing tools
   - Update references

3. **Long-term** (1-2 Weeks):
   - Complete all migrations
   - Deprecate legacy tools
   - Final cleanup and documentation

---

## 📝 COORDINATION NOTES

- **Communication**: Agents should report progress in status.json
- **Overlap Prevention**: Coordinate through Agent-4 (Captain)
- **Blockers**: Report immediately if blockers found
- **Questions**: Use inbox messaging for coordination

---

**WE. ARE. SWARM.** 🐝⚡🔥

*Action plan created: 2025-01-27*

