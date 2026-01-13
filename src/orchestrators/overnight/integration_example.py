#!/usr/bin/env python3
"""
<!-- SSOT Domain: core -->

Overnight Components Integration Example
========================================

Demonstrates how to use the extracted V1→V2 components together.

This example shows:
1. Using message plans for different work strategies
2. Processing FSM updates
3. Monitoring inboxes with the listener
4. Converting agent responses to FSM events

V2 Compliance: Example/demo file
Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-01-28
"""

from pathlib import Path

# Import extracted components
from .message_plans import build_message_plan, format_message, MessageTag, get_available_plans
from .fsm_bridge import handle_fsm_request, handle_fsm_update, seed_fsm_tasks
from .inbox_consumer import process_inbox, to_fsm_event
from .listener import OvernightListener
from .fsm_updates_processor import process_fsm_updates_directory

# V2 Integration imports
try:
    from ...core.unified_logging_system import get_logger
except ImportError:
    import logging
    def get_logger(name):
        return logging.getLogger(name)

logger = get_logger(__name__)


def example_message_plans():
    """Example: Using message plans."""
    logger.info("=== Message Plans Example ===")
    
    # Get available plans
    plans = get_available_plans()
    logger.info(f"Available plans: {', '.join(plans)}")
    
    # Build a contracts plan
    contracts_plan = build_message_plan("contracts")
    logger.info(f"Contracts plan has {len(contracts_plan)} messages")
    
    # Format messages for an agent
    for planned_msg in contracts_plan:
        message = format_message(planned_msg, "Agent-1")
        logger.info(f"  [{planned_msg.tag.value.upper()}] {message[:80]}...")
    
    # Build FSM-driven plan
    fsm_plan = build_message_plan("fsm-driven")
    logger.info(f"FSM-driven plan has {len(fsm_plan)} messages")


def example_fsm_bridge():
    """Example: Using FSM bridge."""
    logger.info("=== FSM Bridge Example ===")
    
    # Example FSM request
    fsm_request = {
        "from": "Agent-4",
        "agents": ["Agent-1", "Agent-2", "Agent-3"],
        "workflow": "default",
        "timestamp": "2025-01-28T12:00:00"
    }
    
    result = handle_fsm_request(fsm_request)
    logger.info(f"FSM request result: {result}")
    
    # Example FSM update
    fsm_update = {
        "task_id": "TEST_001",
        "state": "completed",
        "summary": "Test task completed",
        "evidence": ["commit_hash_abc123"],
        "from": "Agent-1",
        "captain": "Agent-4"
    }
    
    result = handle_fsm_update(fsm_update)
    logger.info(f"FSM update result: {result}")


def example_inbox_consumer():
    """Example: Using inbox consumer."""
    logger.info("=== Inbox Consumer Example ===")
    
    # Example envelope from agent response
    envelope = {
        "from": "Agent-1",
        "timestamp": "2025-01-28T12:00:00",
        "payload": {
            "type": "agent_report",
            "task": "TEST_001",
            "status": "completed",
            "summary": "Task completed successfully",
            "actions": ["commit_hash_abc123", "test_results.json"]
        }
    }
    
    # Convert to FSM event
    fsm_event = to_fsm_event(envelope)
    logger.info(f"Converted to FSM event: {fsm_event['type']} - {fsm_event['task_id']}")
    
    # Process inbox (would process actual files)
    # processed = process_inbox("Agent-1")
    # logger.info(f"Processed {processed} files from Agent-1 inbox")


def example_listener():
    """Example: Using listener."""
    logger.info("=== Listener Example ===")
    
    # Create listener instance
    listener = OvernightListener(
        agent_id="Agent-1",
        poll_interval=1.0,
        devlog_webhook=None,  # Set if Discord integration needed
        devlog_username="Agent Devlog"
    )
    
    logger.info(f"Listener created for {listener.agent_id}")
    logger.info(f"Inbox directory: {listener.inbox_dir}")
    logger.info(f"State file: {listener.state_path}")
    
    # Process inbox once (example)
    # processed = listener.process_inbox()
    # logger.info(f"Processed {processed} messages")
    
    # To run continuously:
    # listener.run()


def example_fsm_updates_processor():
    """Example: Processing V1 FSM updates."""
    logger.info("=== FSM Updates Processor Example ===")
    
    # Process V1 FSM_UPDATES directory
    v1_updates_dir = Path("D:/Agent_Cellphone/FSM_UPDATES")
    
    if v1_updates_dir.exists():
        processed = process_fsm_updates_directory(v1_updates_dir, target_agent="Agent-5")
        logger.info(f"Processed {processed} FSM update files")
    else:
        logger.warning(f"V1 FSM_UPDATES directory not found: {v1_updates_dir}")


def example_integrated_workflow():
    """Example: Integrated workflow using all components."""
    logger.info("=== Integrated Workflow Example ===")
    
    # 1. Build message plan
    plan = build_message_plan("fsm-driven")
    logger.info(f"Built {len(plan)} message plan steps")
    
    # 2. Format and send messages (would use messaging system)
    for step in plan:
        message = format_message(step, "Agent-1")
        logger.info(f"Would send: {message[:60]}...")
    
    # 3. Monitor for responses (would run listener)
    # listener = OvernightListener("Agent-1")
    # listener.start()
    
    # 4. Process responses through inbox consumer
    # processed = process_inbox("Agent-1")
    
    # 5. Handle FSM updates
    # fsm_update = {...}
    # handle_fsm_update(fsm_update)
    
    logger.info("Integrated workflow example complete")


if __name__ == "__main__":
    """Run all examples."""
    logger.info("Running overnight components integration examples...")
    logger.info("")
    
    try:
        example_message_plans()
        logger.info("")
        
        example_fsm_bridge()
        logger.info("")
        
        example_inbox_consumer()
        logger.info("")
        
        example_listener()
        logger.info("")
        
        example_fsm_updates_processor()
        logger.info("")
        
        example_integrated_workflow()
        logger.info("")
        
        logger.info("✅ All examples completed successfully")
        
    except Exception as e:
        logger.error(f"❌ Example failed: {e}", exc_info=True)

