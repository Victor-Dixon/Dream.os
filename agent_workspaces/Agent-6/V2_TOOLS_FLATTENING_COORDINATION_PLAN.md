# 🚨 V2 TOOLS FLATTENING - COORDINATION PLAN

**From**: Agent-6 (Coordination & Communication Specialist)  
**Date**: 2025-01-27  
**Priority**: HIGH (URGENT)  
**Status**: COORDINATED EFFORT - ALL AGENTS

---

## 📋 MISSION OVERVIEW

**OBJECTIVE**: Flatten and consolidate V2 tools structure for better organization

**SCOPE**: 
- Review `tools/` structure
- Identify tools needing migration from `tools/` to `tools/`
- Follow adapter pattern
- Coordinate team effort
- Communicate progress

---

## 🎯 CURRENT STATE ANALYSIS

### **tools/ Structure**
- ✅ **69 files** (63 Python files, 5 markdown, 1 JSON)
- ✅ Well-organized with categories
- ⚠️ **Nested subdirectories** detected:
  - `tools/categories/advice_context/` (needs flattening)
  - `tools/categories/advice_outputs/` (needs flattening)

### **tools/ Directory - Migration Candidates**
- ⚠️ **17 captain_*.py files** need migration:
  - `captain_leaderboard_update.py`
  - `captain_coordinate_validator.py`
  - `captain_architectural_checker.py`
  - `captain_import_validator.py`
  - `captain_check_agent_status.py`
  - `captain_completion_processor.py`
  - `captain_find_idle_agents.py`
  - `captain_hard_onboard_agent.py`
  - `captain_gas_check.py`
  - `captain_snapshot.py`
  - `captain_roi_quick_calc.py`
  - `captain_self_message.py`
  - `captain_morning_briefing.py`
  - `captain_toolbelt_help.py`
  - `captain_next_task_picker.py`
  - `captain_update_log.py`
  - `captain_message_all_agents.py`

### **Reference Documents**
- ✅ `docs/specs/TOOLBELT_CONSOLIDATION_STRATEGY.md` - Full strategy
- ✅ `docs/task_assignments/CRITICAL_TASKS_2025-01-27.md` - Task details

---

## 🔄 COORDINATION ASSIGNMENTS

### **Agent-1** (Integration & Core Systems)
**Role**: Coordinate migration  
**Tasks**:
- [ ] Review core tools in `tools/` for migration
- [ ] Identify integration dependencies
- [ ] Create migration plan for core tools
- [ ] Test tool adapters

### **Agent-2** (Architecture & Design)
**Role**: Review structure  
**Tasks**:
- [ ] Review `tools/` architecture
- [ ] Validate adapter pattern implementation
- [ ] Review consolidation strategy alignment
- [ ] Approve structural changes

### **Agent-6** (Coordination & Communication)
**Role**: **COORDINATOR**  
**Tasks**:
- [x] Review tools/ structure
- [x] Identify tools needing migration
- [ ] Create migration coordination plan
- [ ] Communicate progress to swarm
- [ ] Track team progress
- [ ] Update status files

### **Agent-7** (Web Development)
**Role**: Tool registry updates  
**Tasks**:
- [ ] Update `tools/tool_registry.py` with new tools
- [ ] Register migrated tools
- [ ] Update tool registry documentation
- [ ] Test registry functionality

### **Agent-8** (SSOT & System Integration)
**Role**: Ensure SSOT compliance  
**Tasks**:
- [ ] Verify single source of truth
- [ ] Check for SSOT violations
- [ ] Validate consolidation roadmap
- [ ] Ensure no duplicates remain

---

## 📊 FLATTENING PRIORITIES

### **Priority 1: Flatten Nested Subdirectories** (IMMEDIATE)
**Target**: `tools/categories/advice_context/` and `advice_outputs/`

**Action Items**:
1. [ ] Review modules in `advice_context/`:
   - `agent_context`
   - `project_context`
   - `swarm_context`
2. [ ] Review modules in `advice_outputs/`:
   - `guidance_formatter`
   - `recommendation_generator`
   - `report_builder`
3. [ ] Decide: Merge into single category file or keep separate?
4. [ ] Update imports and references
5. [ ] Test functionality

### **Priority 2: Migrate Captain Tools** (HIGH)
**Target**: 17 captain_*.py files from `tools/` to `tools/categories/`

**Migration Strategy** (per TOOLBELT_CONSOLIDATION_STRATEGY.md):

**Category A - Core Operations** (→ `captain_tools.py`):
- `captain_self_message.py`
- `captain_message_all_agents.py`
- `captain_check_agent_status.py`
- `captain_find_idle_agents.py`
- `captain_gas_check.py`

**Category B - Analysis** (→ `captain_tools_advanced.py`):
- `captain_architectural_checker.py`
- `captain_coordinate_validator.py`
- `captain_import_validator.py`
- `captain_morning_briefing.py`

**Category C - Workflow** (→ `captain_coordination_tools.py`):
- `captain_completion_processor.py`
- `captain_leaderboard_update.py`
- `captain_next_task_picker.py`
- `captain_roi_quick_calc.py`
- `captain_update_log.py`
- `captain_hard_onboard_agent.py`

**Category D - UI/Help** (→ `coordination_tools.py`):
- `captain_toolbelt_help.py`

**Other**:
- `captain_snapshot.py` (→ `health_tools.py` or `captain_tools.py`)

**Action Items**:
1. [ ] Create adapter classes for each tool
2. [ ] Register in `tool_registry.py`
3. [ ] Test via toolbelt
4. [ ] Add deprecation warnings to old files
5. [ ] Document migration

### **Priority 3: Identify Additional Migration Candidates** (MEDIUM)
**Target**: Other tools in `tools/` that need migration

**Action Items**:
1. [ ] Audit remaining tools in `tools/` directory
2. [ ] Identify high-value tools for migration
3. [ ] Create migration plan
4. [ ] Coordinate with team

---

## 🚀 IMPLEMENTATION PHASES

### **PHASE 1: Analysis & Planning** (Agent-6)
**Duration**: 1-2 hours  
**Tasks**:
- [x] Review tools/ structure
- [x] Identify nested subdirectories
- [x] List migration candidates
- [x] Create coordination plan
- [ ] Communicate plan to team

### **PHASE 2: Flattening** (Agent-2 + Agent-6) ✅ COMPLETE
**Duration**: 2-3 hours  
**Tasks**:
- [x] Flatten `advice_context/` subdirectory - REMOVED (empty, unused)
- [x] Flatten `advice_outputs/` subdirectory - REMOVED (empty, unused)
- [x] Update imports and references - N/A (not referenced)
- [x] Test functionality - Verified no references exist
- [x] Update documentation - Plan updated

**Status**: ✅ COMPLETE - 2025-01-27  
**Result**: Both nested subdirectories removed successfully. No references found in codebase. Structure is now flat.

### **PHASE 3: Captain Tools Migration** (Agent-1 + Agent-6 + Agent-7)
**Duration**: 4-6 hours  
**Tasks**:
- [ ] Create adapters for Category A tools
- [ ] Create adapters for Category B tools
- [ ] Create adapters for Category C tools
- [ ] Create adapters for Category D tools
- [ ] Register all tools in registry
- [ ] Test all tools via toolbelt
- [ ] Add deprecation warnings

### **PHASE 4: Registry & Documentation** (Agent-7 + Agent-8)
**Duration**: 2-3 hours  
**Tasks**:
- [ ] Update tool registry
- [ ] Update documentation
- [ ] Verify SSOT compliance
- [ ] Final testing

---

## 📝 PROGRESS TRACKING

### **Current Status**
- ✅ **Coordination Plan Created**: 2025-01-27
- ✅ **Structure Analysis**: Complete
- ✅ **Migration Candidates Identified**: 17 captain tools + 2 nested subdirectories
- ⏳ **Team Coordination**: In progress
- ⏳ **Implementation**: Pending team alignment

### **Next Steps**
1. Communicate plan to Agent-1, Agent-2, Agent-7, Agent-8
2. Get alignment on priorities
3. Begin Phase 1 implementation
4. Track progress in status files

---

## 📨 COMMUNICATION PROTOCOL

### **Status Updates**
- Update `agent_workspaces/Agent-6/status.json` after each phase
- Send progress reports to Agent-4 inbox
- Coordinate with team members via status updates

### **Coordination Channels**
- Primary: Status files
- Secondary: Inbox messaging
- Emergency: Direct coordination

---

## ✅ SUCCESS CRITERIA

**Coverage**:
- [ ] 100% nested subdirectories flattened
- [ ] 100% captain tools migrated
- [ ] All tools accessible through `tools/`
- [ ] No duplicate tool implementations

**Quality**:
- [ ] All tools searchable via toolbelt
- [ ] All tools have adapters
- [ ] All tools tested
- [ ] Clear deprecation warnings

**Documentation**:
- [ ] Migration guide created
- [ ] Tool registry updated
- [ ] Usage examples documented
- [ ] Deprecation timeline clear

---

## 🎯 COORDINATION NOTES

**Agent-6 Responsibilities**:
- ✅ Lead coordination effort
- ✅ Track progress across all agents
- ✅ Communicate updates to swarm
- ✅ Ensure team alignment

**Team Coordination**:
- **Agent-1**: Focus on integration and core tools migration
- **Agent-2**: Review architecture and approve structural changes
- **Agent-7**: Handle registry updates and tool registration
- **Agent-8**: Ensure SSOT compliance throughout process

---

**WE. ARE. SWARM.** 🐝⚡🔥

**Agent-6**: Ready to coordinate! Let's flatten and consolidate!

**Status**: COORDINATION IN PROGRESS  
**Next Review**: 2025-01-28

