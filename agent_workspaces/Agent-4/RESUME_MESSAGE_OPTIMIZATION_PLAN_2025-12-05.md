# Resume Message Optimization Plan - Goal Alignment
**Date**: 2025-12-05  
**Agent**: Agent-4 (Captain)  
**Priority**: CRITICAL

---

## ❓ **QUESTION**

**Is the resume message the most optimized for getting agents back to task and improving the project towards our goals?**

---

## 📊 **ANALYSIS**

### **Current Resume Message Strengths**:
- ✅ FSM state-specific recovery actions
- ✅ Cycle planner task integration
- ✅ Scheduled tasks from scheduler
- ✅ System utilization protocols
- ✅ Force multiplier patterns
- ✅ "DO NOT ACKNOWLEDGE" directive

### **Current Resume Message Gaps**:
- ❌ **No reference to violation consolidation** (current #1 priority - 1,415 violations)
- ❌ **No reference to SSOT remediation** (current #2 priority)
- ❌ **No reference to Phase 2 consolidation** (current #3 priority)
- ❌ **No agent-specific task assignments** from FULL_SWARM_ACTIVATION
- ❌ **No current mission context** from status.json
- ❌ **Generic recovery actions** instead of goal-aligned actions

---

## 🎯 **CURRENT PROJECT GOALS**

### **1. Violation Consolidation** (CRITICAL - #1 Priority)
- **Objective**: Eliminate 1,415 code violations
- **Status**: Phase 1 assignments dispatched
- **Agent Assignments** (from FULL_SWARM_ACTIVATION):
  - Agent-1: AgentStatus (5 locations) + Task class (10 locations)
  - Agent-2: IntegrationStatus (5 locations) + Gaming classes (12 locations)
  - Agent-8: Config SSOT (5 locations) + SearchResult/SearchQuery (14 locations)
  - Agent-7: Discord test mocks (9 locations)
  - Agent-5: Code block analysis (88 blocks)

### **2. SSOT Remediation** (HIGH - #2 Priority)
- **Objective**: Reduce SSOT drift and duplication
- **Domain Ownership**:
  - Agent-1: Integration SSOT
  - Agent-2: Architecture SSOT
  - Agent-3: Infrastructure SSOT
  - Agent-5: Analytics SSOT
  - Agent-6: Communication SSOT
  - Agent-7: Web SSOT
  - Agent-8: QA SSOT

### **3. Phase 2 Tools Consolidation** (HIGH - #3 Priority)
- **Objective**: 42 candidates → ~10-15 core tools
- **Agent Assignments**:
  - Agent-3: Infrastructure Monitoring Consolidation
  - Agent-5: Analytics tools consolidation
  - Agent-8: Phase 2/3 execution

---

## ✅ **OPTIMIZATION PLAN**

### **Enhance Resume Message with Goal Alignment**

#### **1. Add Current Mission Context Section**
```markdown
**📋 YOUR CURRENT MISSION:**
- **Mission**: {current_mission from status.json}
- **Priority**: {mission_priority}
- **Status**: {status}
```

#### **2. Add Project Priority Alignment Section**
```markdown
**🎯 CURRENT PROJECT PRIORITIES (ALIGN YOUR WORK):**
1. **Violation Consolidation** (CRITICAL) - 1,415 violations to eliminate
   - Your assignments: {tasks from FULL_SWARM_ACTIVATION}
2. **SSOT Remediation** (HIGH) - Reduce duplication in your domain
   - Your domain: {agent's SSOT domain}
3. **Phase 2 Consolidation** (HIGH) - Tools consolidation
   - Your tasks: {specific assignments}
```

#### **3. Add Agent-Specific Task Assignments**
- Load tasks from FULL_SWARM_ACTIVATION document
- Reference violation consolidation assignments
- Include SSOT domain ownership tasks
- Reference Phase 2 consolidation tasks

#### **4. Enhance Recovery Actions with Goal Alignment**
Replace generic actions with goal-aligned actions:
- "Resume violation consolidation: [specific task]"
- "Continue SSOT remediation in [domain]"
- "Execute Phase 2 consolidation: [assignment]"
- "Check swarm organizer for goal-aligned tasks"

---

## 🔧 **IMPLEMENTATION**

### **Update OptimizedStallResumePrompt**

1. **Add method to load agent assignments**:
   ```python
   def _load_agent_assignments(self, agent_id: str) -> Dict[str, Any]:
       """Load agent-specific tasks from FULL_SWARM_ACTIVATION document."""
   ```

2. **Add project priority section**:
   ```python
   def _build_project_priorities_section(self, agent_id: str) -> str:
       """Build project priority alignment section."""
   ```

3. **Enhance _build_prompt()** to include:
   - Current mission context
   - Project priority alignment
   - Agent-specific task assignments
   - Goal-aligned recovery actions

---

**Status**: 📋 Analysis complete, optimization plan ready  
**Next**: Implement goal-aligned resume messages

🐝 WE. ARE. SWARM. ⚡🔥


