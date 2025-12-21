# Toolbelt Signal vs. Noise Analysis

**Date:** 2025-12-21  
**Agent:** Agent-1 (Integration & Core Systems Specialist)  
**Status:** 🔄 **ANALYSIS IN PROGRESS**

---

## 🎯 Objective

Distinguish between **toolbelt-worthy tools** (signal) and **one-off scripts** (noise) that should be moved to `scripts/` directory.

---

## 📊 Toolbelt-Worthy Criteria

A tool belongs in the toolbelt if it:
1. ✅ **Used frequently** by agents in daily workflows
2. ✅ **Core operational function** (messaging, coordination, status)
3. ✅ **Reusable** across multiple agents
4. ✅ **Part of agent operating cycle** (claim, execute, validate, commit, report)
5. ✅ **Called programmatically** by agents, not manually run

A tool should be moved to `scripts/` if it:
1. ❌ **One-off execution** (audits, cleanups, migrations)
2. ❌ **Manual invocation** (run once, not part of workflow)
3. ❌ **Analysis/reporting** (generate reports, not operational)
4. ❌ **Infrequent use** (special cases, not daily operations)
5. ❌ **Standalone script** (has `if __name__ == "__main__"` pattern)

---

## ✅ TOOLBELT-WORTHY (Signal) - Keep in Toolbelt

### **Core Agent Operations (HIGH PRIORITY)**
- ✅ `agent.claim` - Task claiming (core workflow)
- ✅ `agent.status` - Status updates (core workflow)
- ✅ `msg.send` - Send messages (core coordination)
- ✅ `msg.inbox` - Check inbox (core coordination)
- ✅ `msg.broadcast` - Broadcast messages (core coordination)
- ✅ `session.cleanup` - Session cleanup (core workflow)
- ✅ `session.passdown` - Passdown creation (core workflow)
- ✅ `mission.claim` - Mission claiming (core workflow)

### **Coordination & Communication (HIGH PRIORITY)**
- ✅ `coord.find-expert` - Find domain expert (coordination)
- ✅ `coord.request-review` - Request expert review (coordination)
- ✅ `coord.check-patterns` - Check coordination patterns (coordination)
- ✅ `swarm.pulse` - Swarm pulse check (coordination)

### **Swarm Brain & Knowledge (MEDIUM PRIORITY)**
- ✅ `brain.note` - Take notes (knowledge management)
- ✅ `brain.share` - Share learning (knowledge management)
- ✅ `brain.search` - Search knowledge (knowledge management)
- ✅ `brain.get` - Get agent notes (knowledge management)
- ✅ `brain.session` - Log session (knowledge management)

### **Captain Tools (CAPTAIN ONLY)**
- ✅ `captain.*` (10 tools) - Captain-specific operations
  - `captain.status_check`, `captain.git_verify`, `captain.calc_points`
  - `captain.assign_mission`, `captain.deliver_gas`, `captain.update_leaderboard`
  - `captain.verify_work`, `captain.cycle_report`, `captain.markov_optimize`
  - `captain.integrity_check`

### **Onboarding (MEDIUM PRIORITY)**
- ✅ `onboard.hard` - Hard onboarding (agent setup)
- ✅ `onboard.soft` - Soft onboarding (agent setup)

### **Advisor Tools (MEDIUM PRIORITY)**
- ✅ `advisor.guide` - Real-time guidance
- ✅ `advisor.recommend` - Mission recommendations
- ✅ `advisor.swarm` - Swarm analysis
- ✅ `advisor.validate` - Order validation

### **Message-Task Integration (MEDIUM PRIORITY)**
- ✅ `msgtask.ingest` - Message ingestion (autonomous loop)
- ✅ `msgtask.parse` - Task parsing (autonomous loop)
- ✅ `msgtask.fingerprint` - Task fingerprinting (autonomous loop)

### **Health & Observability (LOW-MEDIUM PRIORITY)**
- ✅ `health.ping` - Health ping (monitoring)
- ✅ `health.snapshot` - Health snapshot (monitoring)
- ✅ `obs.health` - System health (observability)
- ✅ `obs.metrics` - Metrics snapshot (observability)
- ✅ `obs.get` - Get metric (observability)
- ✅ `obs.slo` - SLO check (observability)

### **Vector & Context (LOW PRIORITY)**
- ✅ `vector.context` - Task context (context management)
- ✅ `vector.search` - Vector search (context management)
- ✅ `vector.index` - Index work (context management)

---

## ❌ ONE-OFF SCRIPTS (Noise) - Move to `scripts/`

### **Analysis Tools (Move to scripts/)**
- ❌ `analysis.scan` - One-off project scanning
- ❌ `analysis.complexity` - One-off complexity analysis
- ❌ `analysis.duplicates` - One-off duplicate detection

**Reason:** Run manually for analysis, not part of daily workflow

### **Business Intelligence Tools (Move to scripts/)**
- ❌ `bi.metrics` - One-off metrics collection
- ❌ `bi.roi.repo` - One-off ROI calculation
- ❌ `bi.roi.task` - One-off ROI calculation
- ❌ `bi.roi.optimize` - One-off ROI optimization

**Reason:** Analysis/reporting tools, not operational

### **V2 Compliance Tools (Move to scripts/)**
- ❌ `v2.check` - One-off V2 compliance check
- ❌ `v2.report` - One-off V2 compliance report

**Reason:** Audit/reporting tools, run manually

### **Testing Tools (Move to scripts/)**
- ❌ `test.coverage` - One-off coverage report
- ❌ `test.mutation` - One-off mutation testing

**Reason:** Testing tools, run as part of CI/CD, not agent workflow

### **Compliance Tools (Move to scripts/)**
- ❌ `comp.check` - One-off compliance check
- ❌ `comp.history` - One-off compliance history

**Reason:** Audit tools, run manually

### **Infrastructure Tools (Move to scripts/)**
- ❌ `infra.orchestrator_scan` - One-off orchestrator scan
- ❌ `infra.file_lines` - One-off file line counting
- ❌ `infra.extract_planner` - One-off module extraction
- ❌ `infra.roi_calc` - One-off ROI calculation

**Reason:** Analysis/planning tools, not operational

### **Discord Tools (QUESTIONABLE - Keep or Move?)**
- ❓ `discord.health` - Discord bot health check
- ❓ `discord.start` - Start Discord bot
- ❓ `discord.test` - Test Discord message

**Reason:** Infrastructure management, not agent workflow. Could be moved to scripts or kept if agents need to check Discord status.

### **Documentation Tools (Move to scripts/)**
- ❌ `docs.search` - One-off documentation search
- ❌ `docs.export` - One-off documentation export

**Reason:** Manual documentation tools, not operational

### **Memory Safety Tools (Move to scripts/)**
- ❌ `mem.leaks` - One-off memory leak detection
- ❌ `mem.verify` - One-off file verification
- ❌ `mem.scan` - One-off unbounded structure scan
- ❌ `mem.imports` - One-off import validation
- ❌ `mem.handles` - One-off file handle check

**Reason:** Diagnostic/audit tools, run manually

### **Validation Tools (Move to scripts/)**
- ❌ `val.smoke` - One-off smoke test
- ❌ `val.flags` - One-off feature flag check
- ❌ `val.rollback` - One-off rollback operation
- ❌ `val.report` - One-off validation report

**Reason:** Testing/validation tools, run manually or in CI/CD

### **Integration Tools (QUESTIONABLE - Keep or Move?)**
- ❓ `integration.find-ssot-violations` - SSOT violation detection
- ❓ `integration.find-duplicates` - Duplicate detection
- ❓ `integration.find-opportunities` - Integration opportunity detection
- ❓ `integration.check-imports` - Import dependency check

**Reason:** Analysis tools, but might be used in integration workflows. Evaluate usage frequency.

### **Config Tools (QUESTIONABLE - Keep or Move?)**
- ❓ `config.validate-ssot` - Config SSOT validation
- ❓ `config.list-sources` - List config sources
- ❓ `config.check-imports` - Check config imports

**Reason:** Diagnostic tools, but might be used in config workflows. Evaluate usage frequency.

### **Workflow Tools (QUESTIONABLE - Keep or Move?)**
- ❓ `workflow.roi` - Workflow ROI calculation
- ❓ `msg.cleanup` - Inbox cleanup

**Reason:** `msg.cleanup` might be operational, `workflow.roi` is analysis.

### **OSS Tools (QUESTIONABLE - Keep or Move?)**
- ❓ `oss.clone` - Clone OSS repo
- ❓ `oss.issues` - Fetch OSS issues
- ❓ `oss.import` - Import OSS issues
- ❓ `oss.portfolio` - OSS portfolio management
- ❓ `oss.status` - OSS status check

**Reason:** OSS operations, but might be infrequent. Evaluate usage.

### **Session Tools (QUESTIONABLE - Keep or Move?)**
- ❓ `agent.points` - Points calculation

**Reason:** Might be used for tracking, but could be internal calculation.

---

## 📊 Summary Statistics

### **Toolbelt-Worthy (Signal): ~35-40 tools**
- Core operations: ~15 tools
- Coordination: ~5 tools
- Swarm brain: ~5 tools
- Captain tools: ~10 tools
- Onboarding: ~2 tools
- Advisor: ~4 tools
- Message-task: ~3 tools
- Health/observability: ~6 tools
- Vector: ~3 tools

### **One-Off Scripts (Noise): ~45-50 tools**
- Analysis: ~3 tools
- BI: ~4 tools
- V2 compliance: ~2 tools
- Testing: ~2 tools
- Compliance: ~2 tools
- Infrastructure: ~4 tools
- Documentation: ~2 tools
- Memory safety: ~5 tools
- Validation: ~4 tools
- Integration: ~4 tools (questionable)
- Config: ~3 tools (questionable)
- Workflow: ~2 tools (questionable)
- OSS: ~5 tools (questionable)
- Discord: ~3 tools (questionable)
- Session: ~1 tool (questionable)

---

## 🎯 Recommended Actions

### **Phase 1: Clear Noise (High Confidence)**
Move ~30 tools to `scripts/`:
- All analysis tools (3)
- All BI tools (4)
- All V2 compliance tools (2)
- All testing tools (2)
- All compliance tools (2)
- All infrastructure analysis tools (4)
- All documentation tools (2)
- All memory safety tools (5)
- All validation tools (4)
- All Discord tools (3) - Infrastructure management

### **Phase 2: Evaluate Questionable Tools**
Analyze usage frequency for ~15 tools:
- Integration tools (4)
- Config tools (3)
- Workflow tools (2)
- OSS tools (5)
- Session tools (1)

**Method:** Check tool invocation logs, agent usage patterns, and workflow integration.

### **Phase 3: Consolidate Toolbelt**
After moving scripts, reorganize toolbelt into:
- **Core Operations** (agent.claim, agent.status, msg.*, session.*)
- **Coordination** (coord.*, swarm.pulse)
- **Knowledge** (brain.*, vector.*)
- **Captain** (captain.*)
- **Onboarding** (onboard.*)
- **Advisor** (advisor.*)
- **Message-Task** (msgtask.*)
- **Health** (health.*, obs.*)

---

## 📋 Migration Plan

1. **Create `scripts/` directory structure:**
   ```
   scripts/
   ├── analysis/
   ├── bi/
   ├── compliance/
   ├── testing/
   ├── infrastructure/
   ├── documentation/
   ├── memory_safety/
   ├── validation/
   └── discord/
   ```

2. **Move tools to scripts:**
   - Update tool registry to remove moved tools
   - Create script wrappers if needed for backward compatibility
   - Update documentation

3. **Update toolbelt documentation:**
   - Document toolbelt-worthy criteria
   - List remaining toolbelt tools
   - Provide migration guide for moved tools

---

## 🎯 Success Metrics

- **Toolbelt size:** Reduce from 87 tools to ~35-40 tools (50-60% reduction)
- **Signal-to-noise ratio:** Improve from ~40% to ~100% signal
- **Tool discovery:** Easier to find relevant tools
- **Maintenance:** Less overhead maintaining one-off scripts in toolbelt

---

**Status:** 🔄 **ANALYSIS COMPLETE** - Ready for review and migration planning

🐝 **WE. ARE. SWARM. ⚡**


