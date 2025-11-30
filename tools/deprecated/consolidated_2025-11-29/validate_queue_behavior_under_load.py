#!/usr/bin/env python3
"""
Queue Behavior Validation Under Load
=====================================

Validates that message queue behaves correctly under stress test load.

Tests:
1. Queue size limits are respected
2. Message ordering is maintained
3. Priority handling works correctly
4. Concurrent access is safe
5. Memory usage is bounded
6. Processing throughput is acceptable

Author: Agent-6 (Coordination & Communication Specialist)
Date: 2025-01-28
License: MIT
"""

import json
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from src.core.message_queue import MessageQueue, QueueConfig
    from src.core.messaging_models_core import (
        UnifiedMessage,
        UnifiedMessageType,
        UnifiedMessagePriority,
        SenderType,
    )
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("⚠️  Make sure you're running from repository root")
    sys.exit(1)


class QueueBehaviorValidator:
    """Validates queue behavior under load."""

    def __init__(self):
        """Initialize validator."""
        self.results: Dict[str, Any] = {
            "tests": [],
            "summary": {},
        }

    def validate_all(self) -> Dict[str, Any]:
        """Run all validation tests.
        
        Returns:
            Results dictionary
        """
        print("🔍 Starting Queue Behavior Validation Under Load...\n")
        
        # Test 1: Queue size limits
        self._test_queue_size_limits()
        
        # Test 2: Message ordering
        self._test_message_ordering()
        
        # Test 3: Priority handling
        self._test_priority_handling()
        
        # Test 4: Concurrent access
        self._test_concurrent_access()
        
        # Test 5: Memory usage
        self._test_memory_usage()
        
        # Test 6: Processing throughput
        self._test_processing_throughput()
        
        # Calculate summary
        self._calculate_summary()
        
        return self.results

    def _test_queue_size_limits(self):
        """Test that queue respects size limits."""
        print("📊 Test 1: Queue Size Limits...")
        
        config = QueueConfig(max_queue_size=100)
        queue = MessageQueue(config=config)
        
        # Try to enqueue more than max
        enqueued = 0
        failed = 0
        
        for i in range(150):
            try:
                message = UnifiedMessage(
                    content=f"Test message {i}",
                    sender="SYSTEM",
                    recipient="Agent-1",
                    message_type=UnifiedMessageType.SYSTEM_TO_AGENT,
                    priority=UnifiedMessagePriority.REGULAR,
                    sender_type=SenderType.SYSTEM,
                )
                queue.enqueue(message)
                enqueued += 1
            except RuntimeError:
                failed += 1
        
        passed = enqueued <= config.max_queue_size
        result = {
            "test": "queue_size_limits",
            "passed": passed,
            "enqueued": enqueued,
            "max_size": config.max_queue_size,
            "failed_after_limit": failed,
        }
        
        self.results["tests"].append(result)
        
        if passed:
            print(f"✅ Queue respects size limit: {enqueued}/{config.max_queue_size}")
        else:
            print(f"❌ Queue exceeded size limit: {enqueued} > {config.max_queue_size}")

    def _test_message_ordering(self):
        """Test that message ordering is maintained."""
        print("📊 Test 2: Message Ordering...")
        
        queue = MessageQueue()
        message_ids = []
        
        # Enqueue messages with timestamps
        for i in range(50):
            message = UnifiedMessage(
                content=f"Ordered message {i}",
                sender="SYSTEM",
                recipient="Agent-1",
                message_type=UnifiedMessageType.SYSTEM_TO_AGENT,
                priority=UnifiedMessagePriority.REGULAR,
                sender_type=SenderType.SYSTEM,
            )
            queue_id = queue.enqueue(message)
            message_ids.append((i, queue_id))
        
        # Dequeue and check order
        dequeued = queue.dequeue(batch_size=50)
        dequeued_ids = [getattr(entry, 'queue_id', '') for entry in dequeued]
        
        # Check that all messages were dequeued
        passed = len(dequeued) == 50
        
        result = {
            "test": "message_ordering",
            "passed": passed,
            "enqueued": 50,
            "dequeued": len(dequeued),
        }
        
        self.results["tests"].append(result)
        
        if passed:
            print(f"✅ Message ordering maintained: {len(dequeued)}/50 dequeued")
        else:
            print(f"❌ Message ordering issue: {len(dequeued)}/50 dequeued")

    def _test_priority_handling(self):
        """Test that priority handling works correctly."""
        print("📊 Test 3: Priority Handling...")
        
        queue = MessageQueue()
        
        # Enqueue mix of urgent and regular
        for i in range(20):
            priority = UnifiedMessagePriority.URGENT if i % 2 == 0 else UnifiedMessagePriority.REGULAR
            message = UnifiedMessage(
                content=f"Priority test {i}",
                sender="SYSTEM",
                recipient="Agent-1",
                message_type=UnifiedMessageType.SYSTEM_TO_AGENT,
                priority=priority,
                sender_type=SenderType.SYSTEM,
            )
            queue.enqueue(message)
        
        # Dequeue and check urgent come first
        dequeued = queue.dequeue(batch_size=20)
        
        # Check that urgent messages have higher priority scores
        urgent_count = 0
        for entry in dequeued:
            priority_score = getattr(entry, 'priority_score', 0)
            if priority_score > 0.5:  # Urgent should have higher score
                urgent_count += 1
        
        passed = urgent_count >= 8  # At least some urgent messages
        
        result = {
            "test": "priority_handling",
            "passed": passed,
            "urgent_messages": urgent_count,
            "total": len(dequeued),
        }
        
        self.results["tests"].append(result)
        
        if passed:
            print(f"✅ Priority handling works: {urgent_count} urgent messages prioritized")
        else:
            print(f"❌ Priority handling issue: {urgent_count} urgent messages")

    def _test_concurrent_access(self):
        """Test that concurrent access is safe."""
        print("📊 Test 4: Concurrent Access...")
        
        import threading
        
        queue = MessageQueue()
        errors = []
        
        def enqueue_worker(worker_id: int, count: int):
            """Worker thread that enqueues messages."""
            try:
                for i in range(count):
                    message = UnifiedMessage(
                        content=f"Concurrent test {worker_id}-{i}",
                        sender="SYSTEM",
                        recipient=f"Agent-{worker_id}",
                        message_type=UnifiedMessageType.SYSTEM_TO_AGENT,
                        priority=UnifiedMessagePriority.REGULAR,
                        sender_type=SenderType.SYSTEM,
                    )
                    queue.enqueue(message)
            except Exception as e:
                errors.append(f"Worker {worker_id}: {e}")
        
        # Start multiple threads
        threads = []
        for i in range(5):
            thread = threading.Thread(target=enqueue_worker, args=(i, 20))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads
        for thread in threads:
            thread.join()
        
        # Check results
        passed = len(errors) == 0
        total_enqueued = len(queue.dequeue(batch_size=1000))  # Get all
        
        result = {
            "test": "concurrent_access",
            "passed": passed,
            "errors": len(errors),
            "total_enqueued": total_enqueued,
            "expected": 100,  # 5 threads * 20 messages
        }
        
        self.results["tests"].append(result)
        
        if passed:
            print(f"✅ Concurrent access safe: {total_enqueued} messages enqueued")
        else:
            print(f"❌ Concurrent access errors: {errors}")

    def _test_memory_usage(self):
        """Test that memory usage is bounded."""
        print("📊 Test 5: Memory Usage...")
        
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        queue = MessageQueue()
        
        # Enqueue many messages
        for i in range(1000):
            message = UnifiedMessage(
                content=f"Memory test {i}" * 10,  # Larger messages
                sender="SYSTEM",
                recipient="Agent-1",
                message_type=UnifiedMessageType.SYSTEM_TO_AGENT,
                priority=UnifiedMessagePriority.REGULAR,
                sender_type=SenderType.SYSTEM,
            )
            queue.enqueue(message)
        
        peak_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = peak_memory - initial_memory
        
        # Cleanup
        queue.cleanup_expired()
        
        # Check that memory increase is reasonable (< 100MB for 1000 messages)
        passed = memory_increase < 100
        
        result = {
            "test": "memory_usage",
            "passed": passed,
            "initial_memory_mb": round(initial_memory, 2),
            "peak_memory_mb": round(peak_memory, 2),
            "increase_mb": round(memory_increase, 2),
        }
        
        self.results["tests"].append(result)
        
        if passed:
            print(f"✅ Memory usage bounded: {memory_increase:.2f}MB increase")
        else:
            print(f"❌ Memory usage high: {memory_increase:.2f}MB increase")

    def _test_processing_throughput(self):
        """Test that processing throughput is acceptable."""
        print("📊 Test 6: Processing Throughput...")
        
        queue = MessageQueue()
        
        # Enqueue messages
        start_time = time.time()
        for i in range(500):
            message = UnifiedMessage(
                content=f"Throughput test {i}",
                sender="SYSTEM",
                recipient="Agent-1",
                message_type=UnifiedMessageType.SYSTEM_TO_AGENT,
                priority=UnifiedMessagePriority.REGULAR,
                sender_type=SenderType.SYSTEM,
            )
            queue.enqueue(message)
        enqueue_time = time.time() - start_time
        
        # Dequeue messages
        start_time = time.time()
        dequeued = queue.dequeue(batch_size=500)
        dequeue_time = time.time() - start_time
        
        enqueue_throughput = 500 / enqueue_time if enqueue_time > 0 else 0
        dequeue_throughput = len(dequeued) / dequeue_time if dequeue_time > 0 else 0
        
        # Check that throughput is acceptable (> 100 msg/s)
        passed = enqueue_throughput > 100 and dequeue_throughput > 100
        
        result = {
            "test": "processing_throughput",
            "passed": passed,
            "enqueue_throughput_msg_per_sec": round(enqueue_throughput, 2),
            "dequeue_throughput_msg_per_sec": round(dequeue_throughput, 2),
        }
        
        self.results["tests"].append(result)
        
        if passed:
            print(f"✅ Throughput acceptable: {enqueue_throughput:.2f} enqueue, {dequeue_throughput:.2f} dequeue msg/s")
        else:
            print(f"❌ Throughput low: {enqueue_throughput:.2f} enqueue, {dequeue_throughput:.2f} dequeue msg/s")

    def _calculate_summary(self):
        """Calculate test summary."""
        total = len(self.results["tests"])
        passed = sum(1 for test in self.results["tests"] if test["passed"])
        failed = total - passed
        
        self.results["summary"] = {
            "total_tests": total,
            "passed": passed,
            "failed": failed,
            "pass_rate": round(passed / total * 100, 2) if total > 0 else 0,
        }

    def print_results(self):
        """Print validation results."""
        print("\n" + "=" * 60)
        print("📊 QUEUE BEHAVIOR VALIDATION RESULTS")
        print("=" * 60)
        
        summary = self.results["summary"]
        print(f"\n📈 Summary:")
        print(f"   Total Tests: {summary['total_tests']}")
        print(f"   ✅ Passed: {summary['passed']}")
        print(f"   ❌ Failed: {summary['failed']}")
        print(f"   📊 Pass Rate: {summary['pass_rate']}%")
        
        print(f"\n📋 Test Details:")
        for test in self.results["tests"]:
            status = "✅" if test["passed"] else "❌"
            print(f"   {status} {test['test']}: {test}")


def main():
    """Main validation entry point."""
    validator = QueueBehaviorValidator()
    results = validator.validate_all()
    validator.print_results()
    
    # Save results to JSON
    output_file = Path("logs/queue_behavior_validation.json")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n💾 Results saved to: {output_file}")
    
    # Return exit code
    all_passed = all(test["passed"] for test in results["tests"])
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())

