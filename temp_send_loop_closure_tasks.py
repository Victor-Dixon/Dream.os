#!/usr/bin/env python3
"""Send loop closure task assignments to agents."""

import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

from src.services.messaging_infrastructure import ConsolidatedMessagingService

loop_closure_assignments = {
    "Agent-1": """Loop Closure Tasks (3): Complete Batch 1 + Validation Coordination
LOOP 1: Complete messaging_infrastructure.py Batch 1 modules 6-7 (71%→100%)
LOOP 2: Request Agent-8 QA validation for all Batch 1 modules
LOOP 3: Coordinate integration testing handoff with Agent-3

Expected: Batch 1 complete, QA validation requested, integration testing coordinated""",

    "Agent-2": """Loop Closure Tasks (3): Report Application + V2 Continuation
LOOP 1: Apply enhanced report template to 3 recent reports (template ready, needs application)
LOOP 2: Continue V2 compliance review - next 5-10 violations, create refactoring plans
LOOP 3: Provide architecture guidance - support Agent-1/Agent-7/Agent-3 as requested

Expected: 3 reports enhanced, next violation plan, architecture support active""",

    "Agent-3": """Loop Closure Tasks (3): Infrastructure Refactoring Completion
LOOP 1: Complete Batch 1 Module 3 - thea_browser_operations.py extraction (~280 lines)
LOOP 2: Continue Batch 2 Module 2 - activity_source_checkers.py extraction (~280 lines)
LOOP 3: Begin SSOT tagging Batch 2 - tag 10-15 core infrastructure files, notify Agent-8

Expected: Module 3 complete, Batch 2 Module 2 started, SSOT tagging batch 2 began""",

    "Agent-5": """Loop Closure Tasks (3): Audit Finalization + Analysis
LOOP 1: Generate Phase 3 report - Web ↔ Analytics (Phase 2 complete, report pending)
LOOP 2: Generate Phase 3 report - Core ↔ Analytics (Phase 2 complete, report pending)
LOOP 3: Delegation overhead analysis - measure + reduce (Gap Closure #5)

Expected: 2 Phase 3 reports complete, delegation overhead analysis started""",

    "Agent-6": """Loop Closure Tasks (3): Metrics + Monitoring Infrastructure
LOOP 1: Add performance metrics baseline - timers/counters, structured logging (Gap Closure #3)
LOOP 2: Create monitoring requirements doc - metrics, thresholds, dashboard needs
LOOP 3: Update force multiplier progress monitor - integrate metrics collection

Expected: Metrics counters implemented, requirements doc, monitor enhanced""",

    "Agent-7": """Loop Closure Tasks (3): Phase 2D Completion + Testing
LOOP 1: Continue Phase 2D - extract remaining command modules (target ~900 lines total)
LOOP 2: Add integration tests - end-to-end coverage for refactored handlers (Gap Closure #2)
LOOP 3: Prepare QA validation handoff - create handoff doc, coordinate with Agent-8

Expected: Phase 2D complete, integration test suite, QA handoff ready""",

    "Agent-8": """Loop Closure Tasks (3): SSOT Verification + QA Validation
LOOP 1: Complete SSOT Verification Phase 2 - verify 25 files, coordinate with Agent-5
LOOP 2: Validate Agent-7 Phase 2D modules - execute QA validation workflow
LOOP 3: Continue core domain scanning - scan next 10 files (code quality + structure)

Expected: Phase 2 verification report, Phase 2D validation report, 10+ files scanned"""
}

print("Sending loop closure task assignments...")
print("=" * 70)

service = ConsolidatedMessagingService()
results = {}

for agent_id, message in loop_closure_assignments.items():
    try:
        result = service.send_message(
            agent=agent_id,
            message=message,
            priority="urgent",
            use_pyautogui=True,
            wait_for_delivery=False,
        )
        
        if result.get("success"):
            results[agent_id] = True
            queue_id = result.get("queue_id", "N/A")
            print(f"✅ {agent_id}: Loop closure tasks queued (Queue ID: {queue_id})")
        else:
            results[agent_id] = False
            error = result.get("message", "Unknown error")
            print(f"❌ {agent_id}: Failed - {error[:80]}")
    except Exception as e:
        results[agent_id] = False
        print(f"❌ {agent_id}: Error - {str(e)[:80]}")

print("\n" + "=" * 70)
success = sum(1 for r in results.values() if r)
print(f"✅ Loop closure assignments queued: {success}/7")
print("💡 Messages queued for PyAutoGUI delivery via queue processor")


