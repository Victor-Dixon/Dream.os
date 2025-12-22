# Captain-Level Task Protocol

**Version:** 1.0  
**Last Updated:** 2025-12-22  
**Author:** Agent-4 (Captain)  
**Status:** ACTIVE PROTOCOL

---

## 🎯 Purpose

This protocol defines the criteria, process, and standards for identifying, creating, and denoting **Captain-Level Tasks** in the MASTER_TASK_LOG. Captain-Level Tasks are strategic, system-wide, or coordination-critical tasks that require Captain (Agent-4) oversight and execution.

---

## 📋 Definition: What is a Captain-Level Task?

A **Captain-Level Task** is a task that meets **ALL** of the following criteria:

### ✅ Required Criteria (ALL must be true):

1. **Strategic/System-Wide Impact**
   - Affects multiple agents (3+ agents)
   - Impacts system-wide operations or infrastructure
   - Requires cross-domain coordination
   - Has repository-wide or architecture-level implications

2. **Coordination-Critical**
   - Requires Captain-level decision-making authority
   - Involves resolving blockers that affect multiple agents
   - Needs strategic oversight and monitoring
   - Cannot be delegated to a single specialized agent

3. **Captain-Specific Expertise Required**
   - Requires Captain's unique role (strategic oversight, coordination, emergency intervention)
   - Needs Captain's authority to override or reassign
   - Involves system-level monitoring or health checks
   - Requires Captain's perspective on swarm-wide priorities

4. **NOT Domain-Specific Implementation**
   - ❌ NOT a single-agent implementation task
   - ❌ NOT a domain-specific technical task (web dev, infrastructure, etc.)
   - ❌ NOT a routine maintenance task
   - ❌ NOT a task that can be assigned to a specialized agent

---

## 🔍 Pre-Creation Checklist

**BEFORE** creating or calling something a Captain-Level Task, you **MUST** complete this checklist:

### Step 1: Task Classification Analysis

- [ ] **Is this task domain-specific?**
  - If YES → Assign to appropriate specialized agent (Agent-1 through Agent-8)
  - If NO → Continue to Step 2

- [ ] **Does this task affect 3+ agents?**
  - If NO → Likely NOT Captain-Level (may be bilateral coordination)
  - If YES → Continue to Step 3

- [ ] **Does this task require Captain's unique authority?**
  - If NO → Likely NOT Captain-Level
  - If YES → Continue to Step 4

- [ ] **Can this task be delegated to a specialized agent?**
  - If YES → Assign to specialized agent, NOT Captain-Level
  - If NO → Continue to Step 5

### Step 2: Impact Assessment

- [ ] **System-Wide Impact:**
  - [ ] Affects repository structure or architecture
  - [ ] Impacts multiple domains (web + infrastructure + integration, etc.)
  - [ ] Requires cross-domain coordination
  - [ ] Has implications for all agents

- [ ] **Coordination-Critical:**
  - [ ] Resolves blockers affecting multiple agents
  - [ ] Requires strategic prioritization decisions
  - [ ] Needs Captain-level monitoring
  - [ ] Involves emergency intervention or system resets

### Step 3: Agent Assignment Analysis

- [ ] **Can Agent-1 (Integration & Core Systems) handle this?**
  - If YES → Assign to Agent-1, NOT Captain-Level

- [ ] **Can Agent-2 (Architecture & Design) handle this?**
  - If YES → Assign to Agent-2, NOT Captain-Level

- [ ] **Can Agent-3 (Infrastructure & DevOps) handle this?**
  - If YES → Assign to Agent-3, NOT Captain-Level

- [ ] **Can Agent-5 (Business Intelligence) handle this?**
  - If YES → Assign to Agent-5, NOT Captain-Level

- [ ] **Can Agent-6 (Coordination & Communication) handle this?**
  - If YES → Assign to Agent-6, NOT Captain-Level

- [ ] **Can Agent-7 (Web Development) handle this?**
  - If YES → Assign to Agent-7, NOT Captain-Level

- [ ] **Can Agent-8 (SSOT & System Integration) handle this?**
  - If YES → Assign to Agent-8, NOT Captain-Level

- [ ] **If NONE of the above → Likely Captain-Level**

### Step 4: Captain-Specific Justification

- [ ] **Document WHY this requires Captain:**
  - [ ] Requires strategic oversight (not just execution)
  - [ ] Needs Captain's authority to coordinate multiple agents
  - [ ] Involves system-wide monitoring or health checks
  - [ ] Requires Captain's perspective on swarm priorities
  - [ ] Cannot be delegated without losing strategic value

### Step 5: Final Validation

- [ ] **All criteria met?** (Review Definition section)
- [ ] **All checklist steps completed?**
- [ ] **Justification documented?**
- [ ] **Ready to create Captain-Level Task?**

---

## 📝 Creation Process

### Step 1: Document the Task

Create a task entry following this format:

```markdown
- [ ] **{PRIORITY}**: {Task Title} - {Task Description}. 
  **Captain-Level Justification:** {Why this requires Captain}
  **Impact:** {System-wide impact description}
  **Agents Affected:** {List of agents}
  **Coordination Required:** {What coordination is needed}
  [Agent-4 CAPTAIN]
```

### Step 2: Add to MASTER_TASK_LOG

Place Captain-Level Tasks in a dedicated section:

```markdown
### Captain-Level Strategic Oversight Tasks

- [ ] **HIGH**: {Task} - [Agent-4 CAPTAIN]
- [ ] **MEDIUM**: {Task} - [Agent-4 CAPTAIN]
```

### Step 3: Denote as Captain-Level

**REQUIRED Denotation:**
- Tag: `[Agent-4 CAPTAIN]` or `[CAPTAIN]`
- Section: Place in "Captain-Level Strategic Oversight Tasks" section
- Priority: Usually HIGH or MEDIUM (rarely LOW)

---

## ✅ Examples: Valid Captain-Level Tasks

### Example 1: Strategic Coordination Review
```markdown
- [ ] **MEDIUM**: Strategic coordination review - Review all active coordinations, identify bottlenecks, optimize force multiplier utilization, ensure bilateral coordination loops are active. Current: 5 active coordinations, 2 blockers, 7 coordination opportunities. **Captain-Level Justification:** Requires Captain's strategic oversight of all coordinations, cross-agent bottleneck identification, and swarm-wide optimization decisions. **Impact:** System-wide coordination efficiency. **Agents Affected:** All agents. [Agent-4 CAPTAIN]
```

### Example 2: Blocker Resolution Coordination
```markdown
- [ ] **HIGH**: Coordinate blocker resolution - Active blockers: (1) SSOT verification for Batches 2-8 (Agent-8), (2) Architecture review for Website SEO/UX (Agent-2). Monitor progress, coordinate resolution, unblock dependent tasks. **Captain-Level Justification:** Requires Captain's authority to coordinate multiple blockers affecting different agents, strategic prioritization, and system-wide unblocking. **Impact:** Unblocks multiple agent workflows. **Agents Affected:** Agent-2, Agent-3, Agent-7, Agent-8. [Agent-4 CAPTAIN]
```

### Example 3: System Health Monitoring
```markdown
- [ ] **MEDIUM**: System health monitoring - Monitor overall system health: toolbelt (100% healthy), import dependencies (0 issues), website audits (complete), V2 compliance (monitoring active). Track metrics and identify improvement opportunities. **Captain-Level Justification:** Requires Captain's system-wide perspective, strategic health assessment, and cross-domain metric analysis. **Impact:** System-wide health visibility. **Agents Affected:** All agents. [Agent-4 CAPTAIN]
```

---

## ❌ Anti-Patterns: NOT Captain-Level Tasks

### ❌ Example 1: Domain-Specific Implementation
```markdown
❌ BAD: - [ ] **HIGH**: Fix freerideinvestor.com HTTP 500 error - [Agent-4 CAPTAIN]
✅ GOOD: - [ ] **HIGH**: Fix freerideinvestor.com HTTP 500 error - [Agent-7]
```
**Why:** This is web development work, should be Agent-7's domain.

### ❌ Example 2: Single-Agent Task
```markdown
❌ BAD: - [ ] **MEDIUM**: Add SSOT tags to 646 tools - [Agent-4 CAPTAIN]
✅ GOOD: - [ ] **MEDIUM**: Add SSOT tags to 646 tools - [Agent-8]
```
**Why:** This is SSOT work, should be Agent-8's domain.

### ❌ Example 3: Routine Monitoring (If Delegateable)
```markdown
❌ BAD: - [ ] **MEDIUM**: Monitor V2 compliance refactoring progress - [Agent-4 CAPTAIN]
✅ GOOD: - [ ] **HIGH**: Monitor V2 compliance refactoring progress - [Agent-6]
```
**Why:** Agent-6 handles coordination and monitoring. Only make this Captain-Level if it requires strategic decisions beyond monitoring.

---

## 🎯 Decision Tree

```
Is this task domain-specific?
├─ YES → Assign to specialized agent (NOT Captain-Level)
└─ NO → Does it affect 3+ agents?
    ├─ NO → Likely bilateral coordination (NOT Captain-Level)
    └─ YES → Does it require Captain's unique authority?
        ├─ NO → Likely coordination task (Agent-6) or multi-agent task
        └─ YES → Can it be delegated?
            ├─ YES → Delegate (NOT Captain-Level)
            └─ NO → Captain-Level Task ✅
```

---

## 📊 Task Priority Guidelines

### HIGH Priority Captain-Level Tasks:
- System-wide blockers affecting multiple agents
- Emergency interventions requiring Captain authority
- Strategic decisions affecting repository structure
- Critical coordination failures

### MEDIUM Priority Captain-Level Tasks:
- Strategic coordination reviews
- System health monitoring
- Blocker resolution coordination
- Force multiplier optimization

### LOW Priority Captain-Level Tasks:
- Rare (usually delegateable)
- Only if requires Captain's unique strategic perspective

---

## 🔄 Review and Update Process

1. **Before Creating:** Complete Pre-Creation Checklist
2. **During Execution:** Update status in MASTER_TASK_LOG
3. **After Completion:** Mark complete, document outcomes
4. **Protocol Review:** Review this protocol quarterly or when patterns emerge

---

## 📌 Quick Reference

**Captain-Level Task =**
- ✅ Strategic/System-Wide Impact (3+ agents)
- ✅ Coordination-Critical (requires Captain authority)
- ✅ Captain-Specific Expertise Required
- ✅ NOT Domain-Specific Implementation

**Denotation:**
- Tag: `[Agent-4 CAPTAIN]` or `[CAPTAIN]`
- Section: "Captain-Level Strategic Oversight Tasks"
- Format: Include justification in description

**Before Creating:**
1. Complete Pre-Creation Checklist
2. Document justification
3. Verify all criteria met
4. Add to dedicated section

---

## 🚨 Enforcement

- **All agents** must follow this protocol before creating Captain-Level Tasks
- **Captain (Agent-4)** reviews all Captain-Level Task proposals
- **Violations** result in task reassignment to appropriate agent
- **Protocol updates** require Captain approval

---

**Protocol Status:** ✅ ACTIVE  
**Next Review:** 2025-03-22  
**Maintained By:** Agent-4 (Captain)

🐝 WE. ARE. SWARM. ⚡🔥

