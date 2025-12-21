# 4-Agent Mode Task Assignments
**Date:** 2025-12-13  
**Mode:** 4-agent (Agents 1-4 only)  
**Prepared By:** Agent-4 (Captain)

## Objective

**Unblock V2 refactors, finish infra SSOT tags, keep CI green baseline, keep captain oversight tight.**

## Active Agents
- Agent-1: Integration & Core Systems
- Agent-2: Architecture & Design
- Agent-3: Infrastructure & DevOps
- Agent-4: Captain (Strategic Oversight)

## Paused Agents
- Agent-5, Agent-6, Agent-7, Agent-8 (no new work)

## Task Assignments

### A2-ARCH-REVIEW-001 (P0) - Agent-2
**Priority:** P0 (Critical - Blocks Agent-1 refactors)

**Task:** Architecture review for Agent-1 refactor plans:
- messaging_infrastructure.py (1922 lines) → V2 compliant modules
- synthetic_github.py (1043 lines) → V2 compliant modules

**Actions:**
1. Review module boundaries + import graph
2. Confirm shims strategy + verify no circular dependencies
3. Return APPROVED or REQUIRED_CHANGES with exact edits

**Acceptance Criteria:**
- Approval notes sent to Agent-1 inbox
- If changes needed: bullet list + file/section targets

**Commit:** `docs: architecture approval notes for Agent-1 V2 refactor plans`

**Status:** 🟡 pending - START IMMEDIATELY

---

### A1-REFAC-EXEC-001 (P0) - Agent-1
**Priority:** P0 (Critical - Depends on A2-ARCH-REVIEW-001)

**Task:** Execute V2 refactor: messaging_infrastructure.py (1922 lines) → compliant modules + shims

**Actions:**
1. Split by responsibility (routing/coordinator/templates/utils)
2. Preserve public imports via shims
3. Run tests + fix regressions

**Acceptance Criteria:**
- No module >300 lines (or documented exception)
- All tests passing
- No circular imports

**Commit:** `refactor: modularize messaging infrastructure to V2 compliance`

**Depends On:** A2-ARCH-REVIEW-001  
**Status:** 🟡 pending - Wait for Agent-2 approval

---

### A1-REFAC-EXEC-002 (P0) - Agent-1
**Priority:** P0 (Critical - Depends on A2-ARCH-REVIEW-001)

**Task:** Execute V2 refactor: synthetic_github.py (1043 lines) → compliant modules + shims

**Actions:**
1. Extract client/models/adapters/helpers
2. Preserve behavior + update tests if needed

**Acceptance Criteria:**
- All tests passing
- Stable public API via shims

**Commit:** `refactor: modularize synthetic github to V2 compliance`

**Depends On:** A2-ARCH-REVIEW-001  
**Status:** 🟡 pending - Wait for Agent-2 approval

---

### A3-SSOT-TAGS-REMAINDER-001 (P1) - Agent-3
**Priority:** P1 (High - Finish infrastructure SSOT tagging)

**Task:** Finish remaining infrastructure SSOT tags (25 files) + rerun verifier + commit report

**Actions:**
1. Add SSOT headers/tags to remaining infrastructure files
2. Run verify_infrastructure_ssot_tags.py
3. Update coverage report artifact

**Acceptance Criteria:**
- Infrastructure SSOT tag coverage >= 95%
- Verification report committed

**Commit:** `chore: complete infrastructure SSOT tagging + verification report`

**Status:** 🟡 pending - Can start immediately (no dependencies)

---

### A4-CAPTAIN-GATES-001 (P0) - Agent-4
**Priority:** P0 (Critical - Maintain merge discipline + test gates)

**Task:** Captain gatekeeping for 4-agent mode: merge discipline + test gate + status hygiene

**Actions:**
1. Enforce dependency order: A2 approve → A1 refactor → A3 tags
2. Require test proof on any refactor PR/commit
3. Keep status.json + cycle artifacts current for A1–A3
4. Post daily swarm status report (4-agent scope)

**Acceptance Criteria:**
- No merges without tests passing evidence
- Daily swarm status report (4-agent scope) committed

**Commit:** `docs: 4-agent mode captain gates + daily status`

**Status:** 🟡 pending - Monitor and enforce throughout cycle

## Dependency Chain

```
A2-ARCH-REVIEW-001 (Agent-2) → START IMMEDIATELY
    ↓
A1-REFAC-EXEC-001 (Agent-1) → Wait for approval
A1-REFAC-EXEC-002 (Agent-1) → Wait for approval
    ↓
A3-SSOT-TAGS-REMAINDER-001 (Agent-3) → Can start immediately
    ↓
A4-CAPTAIN-GATES-001 (Agent-4) → Monitor throughout
```

## Pause Protocol

- Agents 5/6/7/8 do not receive new work
- No Thea/Discord/WP polish tasks this cycle unless critical outage
- If CI breaks: Agent-3 handles infra triage; Agent-4 approves any emergency fix

## Done Definition

Cycle complete when:
- ✅ Agent-2 approval delivered
- ✅ Agent-1 completes both refactors with tests passing
- ✅ Agent-3 finishes SSOT tags + verifier report
- ✅ Agent-4 posts closure status + confirms green baseline

## Broadcast Message

**"4-agent mode: A2 approve → A1 execute V2 splits (messaging + synthetic_github) → A3 finish infra SSOT tags → A4 enforces test-gated merges + daily status. Agents 5/6/7/8 paused."**


