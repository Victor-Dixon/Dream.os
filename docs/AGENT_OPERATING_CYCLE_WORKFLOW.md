# Agent Operating Cycle Workflow Guide

**Author:** Agent-4 (Captain)  
**Date:** 2025-12-10  
**Purpose:** Clarify when tasks are added to cycle planner and when agents message each other

---

## 🔄 AGENT OPERATING CYCLE PHASES

### **CYCLE START** (Initialization)

**Actions:**
1. ✅ Check inbox (priority: D2A → C2A → A2A)
2. ✅ Check Contract System (`--get-next-task`)
3. ✅ Check Swarm Brain (search relevant topics)
4. ✅ Assess task size: Is this a force multiplier opportunity?
5. ✅ Update status.json (status=ACTIVE, increment cycle_count)
6. ✅ Update FSM State
7. ✅ Review current mission

**❌ DO NOT:**
- Add tasks to cycle planner here
- Message other agents here (unless urgent coordination needed)

---

### **DURING CYCLE** (Active Execution)

#### **Phase 3: Slice** (Planning & Technical Design)

**Technical Implementation Planning Workflow** (Informed by CTO best practices):
1. ✅ **Start with explicit technical instructions** - Avoid general "build this feature" tasks
2. ✅ **Request full technical implementation plan** - Ask AI to provide complete plan first
3. ✅ **Vet the plan** - Review and validate before execution
4. ✅ **Convert plan to detailed prompt** - Ask AI to convert validated plan into detailed prompt for model
5. ✅ **Code review before implementation** - Have prompt writer review to confirm implementation won't be spaghetti
6. ✅ **Confirm clean architecture** - Ensure implementation follows patterns, not spaghetti code

**This workflow ensures:**
- Technical clarity before execution
- Validated plans reduce rework
- Clean, maintainable implementations
- Better code quality from the start

**Actions:**
1. ✅ Update status when phase changes
2. ✅ Update when tasks complete
3. ✅ Update if blocked

**✅ MESSAGE OTHER AGENTS WHEN:**
- **Task expands** → Break down and coordinate (use A2A messaging)
- **Need domain expertise** → Message domain specialist agent
- **Cross-domain work** → Message relevant agents for coordination
- **75-80% complete** → Send "gas" to next agent in sequence (pipeline continuity)
- **Blocked** → Message for help or escalate to Captain
- **Force multiplier opportunity** → Break down and assign to swarm

**❌ DO NOT:**
- Add tasks to cycle planner here (unless new work identified)

---

### **CYCLE END** (Cleanup & Handoff)

**Actions:**
1. ✅ Update completed_tasks
2. ✅ Update next_actions
3. ✅ Commit status.json to git
4. ✅ Create & post devlog automatically
5. ✅ Share learnings to Swarm Brain

**✅ ADD TASKS TO CYCLE PLANNER HERE:**
- **Step 9 in Session Cleanup Template** → "ADD PENDING TASKS TO CYCLE PLANNER"
- Location: `agent_workspaces/{agent_id}/cycle_planner_tasks_YYYY-MM-DD.json`
- **When:** After completing current work, before session transition
- **What:** Unfinished work, blockers, next session priorities

**✅ MESSAGE OTHER AGENTS HERE:**
- **Coordination outcomes** → If swarm was engaged, report results
- **Handoff** → If work continues with another agent
- **Completion** → Notify relevant agents of completed work

---

## 📋 WHEN TO ADD TASKS TO CYCLE PLANNER

### **Primary Timing: CYCLE END**

**According to Session Cleanup Template (Step 9):**

> "Add any pending or remaining tasks to the cycle planner. Location: `agent_workspaces/{agent_id}/cycle_planner_tasks_YYYY-MM-DD.json`. Create contracts for unfinished work, blockers, or next session priorities."

**When:**
- ✅ **After completing current tasks** (CYCLE END phase)
- ✅ **During session cleanup** (before transition)
- ✅ **When work is unfinished** (add as pending for next session)

**What to Add:**
- Unfinished tasks from current cycle
- Blockers that need resolution
- Next session priorities
- Dependent tasks waiting on current work
- Follow-up tasks based on current work

**Format:**
```json
{
  "agent_id": "Agent-X",
  "date": "2025-12-10",
  "pending_tasks": [
    {
      "task_id": "task-identifier",
      "title": "Task Title",
      "description": "Detailed description",
      "priority": "HIGH|MEDIUM|LOW",
      "status": "pending",
      "estimated_time": "2-3 hours",
      "dependencies": [],
      "deliverables": ["Deliverable 1", "Deliverable 2"]
    }
  ],
  "completed_tasks": [...]
}
```

---

## 📨 WHEN TO MESSAGE OTHER AGENTS

### **DURING CYCLE** (Primary Messaging Window)

#### **1. Task Expansion** (Force Multiplier)
**When:** Current task is too large or has multiple components

**Action:**
- Break task into parallelizable components
- Map components to agent expertise domains
- Send A2A messages with task breakdown
- Assign via messaging system

**Example:**
```bash
python -m src.services.messaging_cli \
  --agent Agent-7 \
  --message "Task breakdown: [details]" \
  --priority normal
```

#### **2. Pipeline Continuity** (Gas Protocol)
**When:** At 75-80% completion of current task

**Action:**
- Send "gas" to next agent in sequence
- Ensures continuous pipeline flow
- Use 3-send redundancy protocol (75%, 90%, 100%)

**Example:**
```bash
python -m src.services.messaging_cli \
  --agent Agent-2 \
  --message "🚀 GAS - I'm 75% done, you're next!" \
  --priority normal
```

#### **3. Domain Expertise Needed**
**When:** Work requires specific domain knowledge

**Action:**
- Identify domain expert agent
- Send A2A coordination message
- Establish handoff points

**Example:**
- Agent-7 needs architecture review → Message Agent-2
- Agent-1 needs infrastructure help → Message Agent-3

#### **4. Blockers**
**When:** Blocked on external dependency or cross-domain issue

**Action:**
- Document blocker in status.json
- Message relevant agent for help
- Escalate to Captain if needed

---

### **CYCLE END** (Secondary Messaging Window)

#### **1. Coordination Outcomes**
**When:** Swarm was engaged during cycle

**Action:**
- Report coordination outcomes in completion report
- Message involved agents with results
- Update shared status

#### **2. Work Handoff**
**When:** Work continues with another agent

**Action:**
- Message next agent with handoff details
- Include context and progress
- Establish continuation point

#### **3. Completion Notifications**
**When:** Work affects other agents

**Action:**
- Notify relevant agents of completed work
- Share deliverables and insights
- Update shared systems

---

## 🎯 WORKFLOW SUMMARY

### **Cycle Start → During → End**

```
CYCLE START:
├── Check inbox ✓
├── Get next task (from cycle planner or contract system) ✓
├── Update status.json ✓
└── ❌ DO NOT: Add tasks or message (unless urgent)

DURING CYCLE:
├── Phase 3: Slice (Technical Planning) ✓
│   ├── Explicit technical instructions (not general tasks)
│   ├── Request full technical implementation plan
│   ├── Vet plan before execution
│   ├── Convert plan to detailed prompt
│   ├── Code review: Confirm no spaghetti
│   └── Ensure clean architecture patterns
├── Execute work ✓
├── Update status on progress ✓
├── ✅ MESSAGE IF: Task expands, needs expertise, 75% done, blocked
└── ❌ DO NOT: Add tasks to cycle planner

CYCLE END:
├── Update completed_tasks ✓
├── ✅ ADD TASKS: Unfinished work → cycle planner
├── ✅ MESSAGE IF: Coordination outcomes, handoffs, completions
├── Create devlog ✓
└── Commit and post ✓
```

---

## 📊 DECISION TREE

### **Should I Add Tasks to Cycle Planner?**
```
Are you at CYCLE END?
├── YES → Add pending/unfinished tasks to cycle planner
└── NO → Wait until CYCLE END
```

### **Should I Message Another Agent?**
```
DURING CYCLE:
├── Task too large? → Break down, message swarm
├── Need expertise? → Message domain expert
├── 75-80% done? → Send gas to next agent
├── Blocked? → Message for help or escalate
└── Otherwise → Continue work

CYCLE END:
├── Swarm engaged? → Report coordination outcomes
├── Work continues? → Handoff to next agent
├── Work affects others? → Notify relevant agents
└── Otherwise → No message needed
```

---

## 🔑 KEY PRINCIPLES

1. **Technical Implementation Planning:** Plan before code - Request full technical plan, vet it, convert to detailed prompt, review for spaghetti code
2. **Cycle Planner Tasks:** Added at CYCLE END (not during cycle)
3. **Agent Messaging:** Primary during DURING CYCLE, secondary at CYCLE END
4. **Force Multiplier:** Break down and coordinate when task is large
5. **Pipeline Continuity:** Send gas at 75-80% completion
6. **Domain Expertise:** Message relevant agents when needed

---

## 📝 EXAMPLES

### **Example 1: Cycle End Task Addition**
```
Agent completes task but identifies follow-up work:
1. Task completed → Update completed_tasks
2. Follow-up work identified → Add to cycle planner as pending
3. Create cycle_planner_tasks_2025-12-10.json with pending task
4. Next session: Task automatically available via --get-next-task
```

### **Example 2: During Cycle Messaging**
```
Agent working on task realizes it spans multiple domains:
1. At 50% completion → Task expands
2. Break down into components
3. Message Agent-7 (Web) and Agent-2 (Architecture)
4. Coordinate parallel execution
5. Continue own work while others work in parallel
```

### **Example 3: Pipeline Gas**
```
Agent-1 working on repos 1-10:
1. At repo 8 (80% complete) → Send gas to Agent-2
2. At repo 9 (90% complete) → Send gas again (redundancy)
3. At repo 10 (100% complete) → Send final gas with context
4. Agent-2 receives gas, starts repos 11-20 immediately
```

---

## ✅ BEST PRACTICES

1. **Technical Planning (Phase 3: Slice):**
   - Start with explicit technical instructions, not general "build this" tasks
   - Request full technical implementation plan from AI first
   - Vet the plan thoroughly before execution
   - Convert validated plan into detailed prompt for model
   - Code review: Confirm implementation follows patterns, not spaghetti
   - This workflow (informed by CTO best practices) ensures clean, maintainable code

2. **Task Management:**
   - Add tasks to cycle planner at CYCLE END only
   - Use cycle planner for continuity between sessions
   - Don't add tasks during active execution

3. **Messaging:**
   - Message during cycle when coordination needed
   - Use force multiplier pattern for large tasks
   - Send gas early (75-80%) not late (100%)

4. **Coordination:**
   - Break down before struggling alone
   - Leverage domain expertise
   - Maintain pipeline continuity

---

**This workflow ensures:**
- ✅ Tasks added at right time (CYCLE END)
- ✅ Agents message when needed (DURING CYCLE)
- ✅ Pipeline continuity maintained
- ✅ Force multiplier opportunities captured
- ✅ Proper coordination throughout cycle

