#!/usr/bin/env python3
"""Send 4-agent mode task assignments based on YAML prompt."""

import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

from src.services.messaging_infrastructure import ConsolidatedMessagingService
import time

print("=" * 70)
print("4-AGENT MODE TASK ASSIGNMENTS")
print("=" * 70)

service = ConsolidatedMessagingService()

# Task assignments for 4-agent mode
task_assignments = {
    "Agent-2": """🚨 4-AGENT MODE - TASK ASSIGNMENT (P0)

TASK ID: A2-ARCH-REVIEW-001
PRIORITY: P0 (Critical - Blocks Agent-1 refactors)

OBJECTIVE:
Architecture review for Agent-1 refactor plans:
- messaging_infrastructure.py (1922 lines) → V2 compliant modules
- synthetic_github.py (1043 lines) → V2 compliant modules

ACTIONS REQUIRED:
1. Review module boundaries + import graph
2. Confirm shims strategy + verify no circular dependencies
3. Return APPROVED or REQUIRED_CHANGES with exact edits

DELIVERABLE:
- Approval notes sent to Agent-1 inbox
- If changes needed: bullet list + file/section targets

COMMIT MESSAGE:
"docs: architecture approval notes for Agent-1 V2 refactor plans"

DEPENDENCY: This blocks A1-REFAC-EXEC-001 and A1-REFAC-EXEC-002
STATUS: 🟡 pending - START IMMEDIATELY

4-AGENT MODE: Agents 5/6/7/8 paused - focus on core V2 refactors only.""",

    "Agent-1": """🚨 4-AGENT MODE - TASK ASSIGNMENTS (P0)

TASK ID: A1-REFAC-EXEC-001
PRIORITY: P0 (Critical - Depends on A2-ARCH-REVIEW-001)

OBJECTIVE:
Execute V2 refactor: messaging_infrastructure.py (1922 lines) → compliant modules + shims

ACTIONS REQUIRED:
1. Split by responsibility (routing/coordinator/templates/utils)
2. Preserve public imports via shims
3. Run tests + fix regressions

ACCEPTANCE CRITERIA:
✅ No module >300 lines (or documented exception)
✅ All tests passing
✅ No circular imports

COMMIT MESSAGE:
"refactor: modularize messaging infrastructure to V2 compliance"

DEPENDENCY: ⏳ WAIT for Agent-2 architecture approval (A2-ARCH-REVIEW-001)
STATUS: 🟡 pending - Wait for Agent-2 approval

---

TASK ID: A1-REFAC-EXEC-002
PRIORITY: P0 (Critical - Depends on A2-ARCH-REVIEW-001)

OBJECTIVE:
Execute V2 refactor: synthetic_github.py (1043 lines) → compliant modules + shims

ACTIONS REQUIRED:
1. Extract client/models/adapters/helpers
2. Preserve behavior + update tests if needed

ACCEPTANCE CRITERIA:
✅ All tests passing
✅ Stable public API via shims

COMMIT MESSAGE:
"refactor: modularize synthetic github to V2 compliance"

DEPENDENCY: ⏳ WAIT for Agent-2 architecture approval (A2-ARCH-REVIEW-001)
STATUS: 🟡 pending - Wait for Agent-2 approval

---

4-AGENT MODE: Agents 5/6/7/8 paused - focus on core V2 refactors only.""",

    "Agent-3": """🚨 4-AGENT MODE - TASK ASSIGNMENT (P1)

TASK ID: A3-SSOT-TAGS-REMAINDER-001
PRIORITY: P1 (High - Finish infrastructure SSOT tagging)

OBJECTIVE:
Finish remaining infrastructure SSOT tags (25 files) + rerun verifier + commit report

ACTIONS REQUIRED:
1. Add SSOT headers/tags to remaining infrastructure files
2. Run verify_infrastructure_ssot_tags.py
3. Update coverage report artifact

ACCEPTANCE CRITERIA:
✅ Infrastructure SSOT tag coverage >= 95%
✅ Verification report committed

COMMIT MESSAGE:
"chore: complete infrastructure SSOT tagging + verification report"

STATUS: 🟡 pending - Can start immediately (no dependencies)

4-AGENT MODE: Agents 5/6/7/8 paused - focus on core V2 refactors only.""",

    "Agent-4": """🚨 4-AGENT MODE - CAPTAIN GATEKEEPING (P0)

TASK ID: A4-CAPTAIN-GATES-001
PRIORITY: P0 (Critical - Maintain merge discipline + test gates)

OBJECTIVE:
Captain gatekeeping for 4-agent mode: merge discipline + test gate + status hygiene

ACTIONS REQUIRED:
1. Enforce dependency order: A2 approve → A1 refactor → A3 tags
2. Require test proof on any refactor PR/commit
3. Keep status.json + cycle artifacts current for A1–A3
4. Post daily swarm status report (4-agent scope)

ACCEPTANCE CRITERIA:
✅ No merges without tests passing evidence
✅ Daily swarm status report (4-agent scope) committed

COMMIT MESSAGE:
"docs: 4-agent mode captain gates + daily status"

STATUS: 🟡 pending - Monitor and enforce throughout cycle

---

PAUSE PROTOCOL:
- Agents 5/6/7/8 do not receive new work
- No Thea/Discord/WP polish tasks this cycle unless critical outage
- If CI breaks: Agent-3 handles infra triage; Agent-4 approves any emergency fix

DONE DEFINITION:
✅ Agent-2 approval delivered
✅ Agent-1 completes both refactors with tests passing
✅ Agent-3 finishes SSOT tags + verifier report
✅ Agent-4 posts closure status + confirms green baseline

4-AGENT MODE: Tight captain oversight - enforce dependency chain strictly."""
}

print("\n📨 Sending task assignments to Agents 1, 2, 3, 4...")
print("-" * 70)

results = {}
for agent_id, message in task_assignments.items():
    try:
        result = service.send_message(
            agent=agent_id,
            message=message,
            priority="urgent",
            use_pyautogui=True,
            wait_for_delivery=False,
        )
        results[agent_id] = result.get("success", False)
        queue_id = result.get("queue_id", "N/A")
        if result.get("success"):
            print(f"✅ {agent_id}: Task assignment queued (Queue ID: {queue_id})")
        else:
            print(f"❌ {agent_id}: Failed - {result.get('message', 'Unknown error')[:60]}")
        time.sleep(0.5)  # Brief pause between queue operations
    except Exception as e:
        results[agent_id] = False
        print(f"❌ {agent_id}: Error - {str(e)[:60]}")

print("\n" + "=" * 70)
success = sum(1 for r in results.values() if r)
print(f"✅ Task assignments queued: {success}/4")
print("\n📋 DEPENDENCY CHAIN:")
print("   1. Agent-2: Architecture review (START IMMEDIATELY)")
print("   2. Agent-1: Wait for approval, then execute refactors")
print("   3. Agent-3: SSOT tags (can start immediately)")
print("   4. Agent-4: Gatekeeping (monitor throughout)")
print("\n💡 Messages queued for PyAutoGUI delivery via queue processor")
print("⏱️ 5-second delays between agents to prevent race conditions")

