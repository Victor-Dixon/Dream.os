#!/usr/bin/env python3
"""Send downsizing pause notifications to agents 5, 6, 7, 8 and reassignment notices to 1, 2, 3, 4."""

import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

from src.services.messaging_infrastructure import ConsolidatedMessagingService
import time

print("=" * 70)
print("AGENT DOWNSIZING NOTIFICATIONS")
print("=" * 70)

service = ConsolidatedMessagingService()

# Pause messages for agents 5, 6, 7, 8
pause_messages = {
    "Agent-5": """🚨 SYSTEM DOWNSIZING - PAUSE NOTIFICATION

Agent-5, the system is downsizing from 8 agents to 4 agents (Agent-1, Agent-2, Agent-3, Agent-4).

Your current work is being reassigned:
- Pre-Public Audit → Agent-1 (Analytics) + Agent-2 (Reports) + Agent-4 (Coordination)
- Cross-Domain Security → Agent-1 + Agent-4
- Analytics Analysis → Agent-1

Status: PAUSED - Your duties are covered by remaining agents.
No action required. You will be reactivated when the system scales back up.

Thank you for your service!""",

    "Agent-6": """🚨 SYSTEM DOWNSIZING - PAUSE NOTIFICATION

Agent-6, the system is downsizing from 8 agents to 4 agents (Agent-1, Agent-2, Agent-3, Agent-4).

Your current work is being reassigned:
- Progress Monitoring → Agent-4 (Captain)
- Loop Closure Coordination → Agent-4 (Captain)
- Repository Cleanup → Agent-3
- Communication Management → Agent-2

Status: PAUSED - Your duties are covered by remaining agents.
No action required. You will be reactivated when the system scales back up.

Thank you for your service!""",

    "Agent-7": """🚨 SYSTEM DOWNSIZING - PAUSE NOTIFICATION

Agent-7, the system is downsizing from 8 agents to 4 agents (Agent-1, Agent-2, Agent-3, Agent-4).

Your current work is being reassigned:
- Phase 2D Refactoring → Agent-1 (when Batch 1 complete)
- Integration Testing → Agent-1 + Agent-3
- Pre-Public Audit (Web) → Agent-1 + Agent-2
- Architecture Review → Agent-2

Status: PAUSED - Your duties are covered by remaining agents.
No action required. You will be reactivated when the system scales back up.

Thank you for your service!""",

    "Agent-8": """🚨 SYSTEM DOWNSIZING - PAUSE NOTIFICATION

Agent-8, the system is downsizing from 8 agents to 4 agents (Agent-1, Agent-2, Agent-3, Agent-4).

Your current work is being reassigned:
- SSOT Verification → Agent-2
- QA Validation Coordination → Agent-4 (Captain)
- V2 Compliance Validation → Agent-2
- Code Quality Audits → Agent-1 + Agent-2

Status: PAUSED - Your duties are covered by remaining agents.
No action required. You will be reactivated when the system scales back up.

Thank you for your service!"""
}

# Reassignment messages for agents 1, 2, 3, 4
reassignment_messages = {
    "Agent-1": """🚨 DOWNSIZING REASSIGNMENT - NEW DUTIES

Agent-1, due to downsizing (8→4 agents), you're taking on additional duties:

**FROM Agent-5 (Business Intelligence):**
- Analytics integration security validation
- Cross-domain security validation (analytics side)

**FROM Agent-7 (Web Development):**
- Phase 2D refactoring (unified_discord_bot.py) - After Batch 1 complete
- Integration testing for refactored web components

**FROM Agent-8 (SSOT/QA):**
- Self-validation workflow for your own modules (QA for Batch 1)
- Code quality audits for integration work

**Priority Order:**
1. Complete current Batch 1 messaging_infrastructure (modules 6-7)
2. Self-validate Batch 1 modules
3. Begin Agent-7 Phase 2D refactoring
4. Analytics security validation

All reassigned work documented in: docs/captain_reports/downsizing_plan_2025-12-13.md""",

    "Agent-2": """🚨 DOWNSIZING REASSIGNMENT - NEW DUTIES

Agent-2, due to downsizing (8→4 agents), you're taking on additional duties:

**FROM Agent-5 (Business Intelligence):**
- Pre-Public Audit report generation
- Audit coordination documentation

**FROM Agent-7 (Web Development):**
- Architecture review for web refactored components
- Web domain architecture guidance

**FROM Agent-8 (SSOT/QA):**
- SSOT Verification (25 files previously assigned to Agent-8)
- V2 Compliance validation for SSOT tags
- Architecture compliance reviews

**Priority Order:**
1. Continue current architecture/design work
2. Complete SSOT verification for 25 files
3. Support audit report generation
4. Provide architecture guidance for web refactoring

All reassigned work documented in: docs/captain_reports/downsizing_plan_2025-12-13.md""",

    "Agent-3": """🚨 DOWNSIZING REASSIGNMENT - NEW DUTIES

Agent-3, due to downsizing (8→4 agents), you're taking on additional duties:

**FROM Agent-6 (Coordination):**
- Repository cleanup coordination
- Infrastructure coordination management

**FROM Agent-7 (Web Development):**
- Infrastructure integration testing
- Deployment coordination for web components

**FROM Agent-3 (Continue Existing):**
- SSOT tagging coordination (already active)
- Infrastructure refactoring (Batch 1 Module 3)

**Priority Order:**
1. Complete Batch 1 Module 3 (thea_browser_operations.py)
2. Continue SSOT tagging coordination
3. Repository cleanup coordination
4. Infrastructure integration testing

All reassigned work documented in: docs/captain_reports/downsizing_plan_2025-12-13.md""",

    "Agent-4": """🚨 DOWNSIZING REASSIGNMENT - CAPTAIN DUTIES EXPANDED

Agent-4 (Captain), due to downsizing (8→4 agents), you're taking on additional coordination duties:

**FROM Agent-6 (Coordination):**
- Force Multiplier Progress Monitoring
- Loop Closure Campaign Coordination
- Swarm Communication Management

**FROM Agent-8 (SSOT/QA):**
- QA Validation Coordination (for other agents' work)
- Quality oversight across all agents

**FROM Agent-5 (Business Intelligence):**
- Cross-domain coordination oversight
- Audit coordination management

**Priority Order:**
1. Continue Captain oversight
2. Establish progress monitoring for 4-agent system
3. QA validation coordination workflow
4. Loop closure tracking

All reassigned work documented in: docs/captain_reports/downsizing_plan_2025-12-13.md"""
}

print("\n📨 Sending pause notifications to Agents 5, 6, 7, 8...")
print("-" * 70)

pause_results = {}
for agent_id, message in pause_messages.items():
    try:
        result = service.send_message(
            agent=agent_id,
            message=message,
            priority="urgent",
            use_pyautogui=True,
            wait_for_delivery=False,
        )
        pause_results[agent_id] = result.get("success", False)
        queue_id = result.get("queue_id", "N/A")
        if result.get("success"):
            print(f"✅ {agent_id}: Pause notification queued (Queue ID: {queue_id})")
        else:
            print(f"❌ {agent_id}: Failed - {result.get('message', 'Unknown error')[:60]}")
        time.sleep(0.5)  # Brief pause between queue operations
    except Exception as e:
        pause_results[agent_id] = False
        print(f"❌ {agent_id}: Error - {str(e)[:60]}")

print("\n📨 Sending reassignment notices to Agents 1, 2, 3, 4...")
print("-" * 70)

reassignment_results = {}
for agent_id, message in reassignment_messages.items():
    try:
        result = service.send_message(
            agent=agent_id,
            message=message,
            priority="urgent",
            use_pyautogui=True,
            wait_for_delivery=False,
        )
        reassignment_results[agent_id] = result.get("success", False)
        queue_id = result.get("queue_id", "N/A")
        if result.get("success"):
            print(f"✅ {agent_id}: Reassignment notice queued (Queue ID: {queue_id})")
        else:
            print(f"❌ {agent_id}: Failed - {result.get('message', 'Unknown error')[:60]}")
        time.sleep(0.5)  # Brief pause between queue operations
    except Exception as e:
        reassignment_results[agent_id] = False
        print(f"❌ {agent_id}: Error - {str(e)[:60]}")

print("\n" + "=" * 70)
pause_success = sum(1 for r in pause_results.values() if r)
reassignment_success = sum(1 for r in reassignment_results.values() if r)
print(f"✅ Pause notifications: {pause_success}/4")
print(f"✅ Reassignment notices: {reassignment_success}/4")
print("💡 All messages queued for PyAutoGUI delivery via queue processor")
print("⏱️ Messages will be sent with 5-second delays between agents to prevent race conditions")

