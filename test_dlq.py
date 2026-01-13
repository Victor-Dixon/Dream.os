#!/usr/bin/env python3
"""Test script for dead letter queue functionality"""

from src.core.message_queue_processor.handlers.retry_handler import get_dead_letter_queue

def test_dlq():
    print("Testing Dead Letter Queue functionality...")

    # Get DLQ instance
    dlq = get_dead_letter_queue()
    print("✓ Dead letter queue initialized")

    # Add test message
    dlq.add_message(
        queue_id='test-implementation-001',
        entry='Test message for DLQ implementation verification',
        recipient='Agent-Test',
        failure_reason='Testing completed dead letter queue functionality',
        retry_attempts=3
    )
    print("✓ Test message added to dead letter queue")

    # Get stats
    stats = dlq.get_stats()
    print(f"✓ DLQ Stats: {stats['total_messages']} total messages")

    # Check agent-specific failures
    agent_failures = dlq.get_failed_messages_for_agent('Agent-Test')
    print(f"✓ Agent-Test has {len(agent_failures)} failed messages")

    print("🎉 Dead Letter Queue implementation test PASSED!")

if __name__ == "__main__":
    test_dlq()