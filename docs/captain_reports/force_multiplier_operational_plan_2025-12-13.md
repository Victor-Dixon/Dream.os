# Force Multiplier Operational Plan - 4-Agent Mode
**Date:** 2025-12-13  
**Agent:** Agent-4 (Captain)  
**Objective:** Zero agent idleness, maximum parallel execution, efficient swarm utilization

## Strategic Principles

### Force Multiplier Rules
1. **Parallel Execution:** Multiple agents work simultaneously on independent tasks
2. **No Idle Time:** Next task ready before current task completes
3. **Contextual Grouping:** 3 tasks per agent (similar, related work)
4. **Proactive Assignment:** Assign next round before current round completes
5. **Continuous Monitoring:** Real-time idle detection and recovery

---

## Anti-Idleness System

### 1. Task Pipeline Management

**Principle:** Always have next tasks queued before agents finish current work

**Implementation:**
```
Current Tasks (Round N) → Monitor Progress → Prepare Round N+1 → 
Queue Round N+1 → Deliver as Round N completes
```

**Process:**
1. **Monitor Completion Signals:** Status.json updates, commit messages, task completion artifacts
2. **Prepare Next Round:** Create 3 contextually grouped tasks per agent
3. **Queue Assignments:** Pre-load next round in message queue
4. **Deliver Proactively:** Send next round when agent finishes (not after 2 hours!)

---

### 2. Real-Time Idle Detection

**Detection Triggers:**
- Status.json not updated for >30 minutes = WARNING
- Status.json not updated for >1 hour = IDLE (assign recovery task)
- No commits/artifacts for >1 hour = IDLE (assign recovery task)

**Recovery Actions:**
- **<30 min:** Monitor (normal execution time)
- **30-60 min:** Send status check message
- **>60 min:** Assign immediate task (stall recovery)

**Monitoring Frequency:** Every 15 minutes

---

### 3. Task Queue Management

**Queue Structure:**
- **Active Queue:** Current round assignments (4 agents × 3 tasks = 12 tasks)
- **Ready Queue:** Next round prepared (12 tasks ready to assign)
- **Backlog Queue:** Future rounds planned (maintain 2-3 rounds ahead)

**Queue Replenishment:**
- Monitor active queue completion (every 15 min)
- When agent completes 1 task → check if they'll finish soon
- When agent completes all 3 tasks → immediately deliver next round

---

## Force Multiplier Execution Strategy

### Task Grouping Rules

**Contextual Grouping (3 tasks per agent):**
- Similar work type (all refactoring, all testing, all docs)
- Related files/modules (work in same codebase area)
- Sequential dependencies (Task 2 needs Task 1, Task 3 needs Task 2)

**Examples:**
- ✅ Agent-1: messaging_infrastructure.py refactor → synthetic_github.py refactor → integration tests
- ✅ Agent-2: architecture review → SSOT verification → compliance audit
- ✅ Agent-3: SSOT tags → infrastructure refactor → deployment coordination

**Avoid:**
- ❌ Unrelated tasks (refactor + docs + testing all different domains)
- ❌ Competing priorities (urgent + low priority mixed)

---

### Parallel Execution Maximization

**Current 4-Agent Mode Parallelization:**
```
Agent-2 (A2-ARCH-REVIEW) ─┐
                           ├─> Independent tasks (can run simultaneously)
Agent-3 (A3-SSOT-TAGS) ────┘

Agent-1 (A1-REFAC) ────> Depends on Agent-2 ──> Sequential chain
```

**Strategy:**
1. **Identify Independent Work:** Tasks with no dependencies
2. **Assign Simultaneously:** Don't wait for unrelated tasks
3. **Track Dependencies:** Monitor blocking relationships
4. **Unblock Quickly:** Ready to unblock as soon as dependencies resolve

---

### Efficiency Optimization

**1. Batch Similar Operations**
- Group similar refactors together
- Batch SSOT tagging (don't do one at a time)
- Batch testing (run all tests together)

**2. Context Switching Minimization**
- Keep agents in same domain/area
- Avoid jumping between unrelated work
- Complete module before moving to next

**3. Clear Handoff Points**
- Define completion criteria clearly
- Provide next task immediately upon completion
- Avoid "waiting for direction" gaps

---

## Operational Workflow

### Daily Captain Cycle (4x per day = every 6 hours)

**Cycle 1 (Morning):**
1. Check all agent status.json (last updated times)
2. Identify idle/soon-to-be-idle agents
3. Prepare next round assignments
4. Queue assignments for idle agents
5. Monitor dependency chain progress

**Cycle 2 (Midday):**
1. Verify round completion progress
2. Deliver next round to completed agents
3. Check for blockers/dependencies resolved
4. Unblock dependent agents if ready
5. Update force multiplier metrics

**Cycle 3 (Afternoon):**
1. Monitor ongoing work progress
2. Prepare next round (2 rounds ahead)
3. Identify emerging blockers
4. Coordinate cross-agent dependencies
5. Update daily status report

**Cycle 4 (Evening):**
1. Final status check (all agents)
2. Deliver next round to finishing agents
3. Prepare overnight/next-day assignments
4. Generate daily force multiplier report
5. Post consolidated status to Discord

---

## Idle Prevention Mechanisms

### Mechanism 1: Proactive Task Queuing
**Action:** Always maintain 1 round ahead in queue
**Trigger:** When agent completes 2/3 tasks
**Delivery:** Send next round immediately when 3/3 complete

### Mechanism 2: Stall Recovery System
**Action:** Automated idle detection + recovery
**Trigger:** Status.json >60 min old
**Recovery:** Send stall recovery message + immediate task

### Mechanism 3: Completion Prediction
**Action:** Estimate task completion time
**Trigger:** Monitor progress indicators (commits, artifacts)
**Prevention:** Queue next task 15 min before estimated completion

### Mechanism 4: Dependency Unblocking
**Action:** Monitor dependency resolution
**Trigger:** Blocker task completes
**Unblock:** Immediately notify dependent agent + send next task

---

## Force Multiplier Metrics

### Efficiency Metrics
- **Parallel Execution Rate:** % of time multiple agents working simultaneously
- **Idle Time:** Total minutes agents waiting for assignments
- **Task Completion Rate:** Tasks completed per agent per hour
- **Dependency Block Time:** Minutes agents blocked waiting for dependencies

### Target Metrics (4-Agent Mode)
- **Parallel Execution:** >75% of time (3-4 agents working simultaneously)
- **Idle Time:** <5% of total time (15 min max per agent per day)
- **Task Completion:** >2 tasks per agent per hour (with grouping)
- **Dependency Block:** <30 min average wait time

---

## Implementation Tools

### 1. Idle Detection Monitor
**Tool:** Enhanced version of existing monitor
**Function:** Check status.json every 15 minutes, detect >30min idle
**Action:** Trigger recovery assignment

### 2. Task Queue Manager
**Tool:** Queue management system
**Function:** Maintain active/ready/backlog queues
**Action:** Auto-deliver next round when current completes

### 3. Dependency Chain Tracker
**Tool:** Existing dependency monitor (enhance)
**Function:** Track blockers and unblock agents automatically
**Action:** Notify + assign when dependencies resolve

### 4. Force Multiplier Dashboard
**Tool:** Real-time status dashboard
**Function:** Show all agents, current tasks, progress, idle status
**Action:** Visual monitoring for captain

---

## Next Round Assignment Strategy

### Round N+1 Preparation (While Round N Executes)

**Process:**
1. **Monitor Round N Progress:** Track completion % per agent
2. **Identify Completing Agents:** Who's on task 3/3?
3. **Prepare Next Round:** Create 3 tasks for each completing agent
4. **Contextual Grouping:** Ensure tasks are related/similar
5. **Queue Assignments:** Load into ready queue
6. **Deliver Immediately:** Send as soon as agent finishes

**Timing:**
- Start preparing Round N+1 when Round N is 60% complete
- Have Round N+1 ready when first agent finishes Round N
- Maintain 2-3 rounds prepared ahead

---

## Emergency Idle Recovery

### Immediate Actions (Agent Idle Detected)
1. **Assess Situation:** Check why idle (blocked? stalled? finished?)
2. **Recovery Task:** Assign immediate high-value task
3. **Stall Recovery Message:** Send via PyAutoGUI
4. **Monitor Response:** Verify agent picks up task within 15 min

### Recovery Task Types
- **Quick Wins:** Low-effort, high-value tasks (<30 min)
- **Coordination:** Support other agents (unblock dependencies)
- **Documentation:** Update docs, create reports
- **Quality:** Code reviews, test improvements

---

## Continuous Improvement

### Weekly Review
- Analyze idle time patterns
- Optimize task grouping strategies
- Adjust assignment timing
- Refine dependency management

### Metrics Tracking
- Track force multiplier efficiency over time
- Identify bottlenecks in assignment process
- Measure parallel execution improvements
- Optimize based on data

---

## Session Implementation Plan

**Immediate Actions:**
1. ⏳ Create enhanced idle detection monitor (15-min checks)
2. ⏳ Create task queue manager (active/ready/backlog)
3. ⏳ Enhance dependency chain tracker (auto-unblock)
4. ⏳ Create force multiplier dashboard (visual monitoring)

**Short-term (Next Session):**
5. Implement proactive task queuing
6. Set up automated recovery system
7. Start 4x daily captain cycles

**Ongoing:**
8. Monitor metrics continuously
9. Optimize based on patterns
10. Maintain 2-3 rounds ahead

---

## Success Criteria

**Zero Idle Time:**
- No agent idle >30 minutes
- Next task assigned within 15 min of completion
- Stall recovery <5 min response time

**Force Multiplier Efficiency:**
- >75% parallel execution
- >2 tasks/agent/hour
- <30 min dependency block time

**Operational Excellence:**
- 4x daily captain cycles
- 2-3 rounds prepared ahead
- Automated idle detection + recovery


