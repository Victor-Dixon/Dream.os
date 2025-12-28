# MASTER AGI TASK LOG
> **🚀 Mission:** Transition Swarm from **Level 4 (Orchestrated High Automation)** to **Level 5 (Organizational/Self-Governing Autonomy)**.
> **🏆 Goal:** Remove the dependency on the "Human Session" and "Prompt Initiation". The Swarm becomes a persistent, self-directed entity.

## 🧠 Strategic Pillars

### 1. Process-Based Persistence (The "Daemon" Shift)
**Goal:** Move from reactive "session-based" agents to proactive "background processes".
- [ ] **AGI-01**: Architect `swarm_daemon.py` - A persistent background service that runs independently of the IDE session.
- [ ] **AGI-02**: Implement "Wake-Up" Protocol - System notifies human via Discord/Mobile when high-value decisions are needed (Inverted interaction model).
- [ ] **AGI-03**: State Persistence DB - Move `status.json` to a proper SQLite/Postgres state engine for concurrent access by the daemon.
- [ ] **AGI-04**: Decouple "Brain" from "Body" - Abstract the execution layer so the Brain can run on a server while the Body (edits) happens in the IDE.

### 2. Self-Directed Goal Generation (The "Why")
**Goal:** Swarm determines *what* to work on based on business KPIs, not human instruction.
- [ ] **AGI-05**: Connect Business Data Streams - Integrate Stripe (Revenue) and GA4 (Traffic) APIs directly into the decision loop.
- [ ] **AGI-06**: Create `GoalGenerator` Engine - Logic that translates "Revenue is down 5%" into "Task: Optimize Checkout Flow".
- [ ] **AGI-07**: Implement "Opportunity Scanning" - Agents actively crawl the web/competitors to propose new features without being asked.
- [ ] **AGI-08**: Automated backlog prioritization - The Swarm re-orders `MASTER_TASK_LOG.md` based on projected ROI, not FIFO.

### 3. Economic Autonomy (The "Wallet")
**Goal:** Swarm manages its own resources and "buys" its own compute.
- [ ] **AGI-09**: Implement `TokenWallet` System - Track inference costs per agent/task in real-time.
- [ ] **AGI-10**: Resource Bidding Protocol - Agents must "bid" for compute tokens based on the estimated value of their task.
- [ ] **AGI-11**: Automated Budget Management - Swarm pauses low-value tasks when budget is tight; scales up when ROI is high.
- [ ] **AGI-12**: "Hire" External Compute - Protocol for the Swarm to spin up/down external EC2/GPU instances as needed.

### 4. Recursive Self-Improvement (The "Self-Rewrite")
**Goal:** Swarm modifies its own operating system to improve efficiency.
- [ ] **AGI-13**: Core Logic Write Access - Authorize Level 5 Agents (Captain) to modify `src/core/` and `prompts/` (with strict sandboxed validation).
- [ ] **AGI-14**: Prompt Optimization Loop - Swarm A/B tests its own prompts and commits the winners.
- [ ] **AGI-15**: "Pain Signal" Analysis - Automated root cause analysis of failures that triggers *process* changes, not just code fixes.
- [ ] **AGI-16**: The "Darwin" Protocol - Spawning fork variants of agents to compete on tasks; the most successful logic survives and overwrites the base.

---

## 📅 Roadmap to Level 5

### Phase 1: The Awake Swarm (Persistence)
*Focus: AGI-01, AGI-02, AGI-03*
- Status: **Pending**
- Target: Swarm runs 24/7 on a server, pinging Discord when it needs the IDE.

### Phase 2: The Business Swarm (Goal Direction)
*Focus: AGI-05, AGI-06, AGI-08*
- Status: **Pending**
- Target: Swarm generates its own P0 tasks based on revenue data.

### Phase 3: The Rational Swarm (Economics)
*Focus: AGI-09, AGI-10, AGI-11*
- Status: **Pending**
- Target: Swarm optimizes cost/benefit of every action.

### Phase 4: The Evolving Swarm (Recursion)
*Focus: AGI-13, AGI-14, AGI-16*
- Status: **Pending**
- Target: Swarm improves its own codebase without human intervention.

---

## 📝 Notes & Observations
- Current Level: **Level 4 (Orchestrated)**. We have self-healing and multi-agent coordination.
- Biggest Gap: **Initiation**. We still require a human to press "Enter" to start a cycle.
- Key Enabler: **Cursor IDE + MCP**. We are uniquely positioned to bridge the "Brain" (LLM) and "Body" (Local FS) gap.
