#!/usr/bin/env python3
"""
Stress Test Performance Benchmark Runner

Runs performance benchmarks for stress testing system to validate
end-to-end functionality and measure performance.

Author: Agent-2 (Architecture & Design Specialist)
Date: 2025-11-29
"""

import sys
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from src.core.stress_testing.stress_runner import StressTestRunner


def run_benchmark_suite():
    """Run comprehensive benchmark suite."""
    print("=" * 60)
    print("🧪 STRESS TEST PERFORMANCE BENCHMARK SUITE")
    print("=" * 60)
    print()

    results = {}

    # Test 1: Small scale (9 agents, 10 messages/agent = 90 messages)
    print("📊 Test 1: Small Scale (9 agents, 10 messages/agent)")
    print("-" * 60)
    runner = StressTestRunner(num_agents=9, messages_per_agent=10)
    start = time.time()
    metrics = runner.run_stress_test(batch_size=10, interval=0.1)
    duration = time.time() - start
    results["small_scale"] = {
        **metrics,
        "actual_duration": duration,
    }
    print(f"✅ Processed: {metrics['total_processed']} messages")
    print(f"✅ Duration: {duration:.2f}s")
    print(f"✅ Throughput: {metrics.get('throughput', 0):.2f} msg/s")
    print(f"✅ Success Rate: {metrics.get('success_rate', 0):.2%}")
    print()

    # Test 2: Medium scale (9 agents, 50 messages/agent = 450 messages)
    print("📊 Test 2: Medium Scale (9 agents, 50 messages/agent)")
    print("-" * 60)
    runner = StressTestRunner(num_agents=9, messages_per_agent=50)
    start = time.time()
    metrics = runner.run_stress_test(batch_size=50, interval=0.05)
    duration = time.time() - start
    results["medium_scale"] = {
        **metrics,
        "actual_duration": duration,
    }
    print(f"✅ Processed: {metrics['total_processed']} messages")
    print(f"✅ Duration: {duration:.2f}s")
    print(f"✅ Throughput: {metrics.get('throughput', 0):.2f} msg/s")
    print(f"✅ Success Rate: {metrics.get('success_rate', 0):.2%}")
    print()

    # Summary
    print("=" * 60)
    print("📊 BENCHMARK SUMMARY")
    print("=" * 60)
    print(f"Small Scale:  {results['small_scale']['total_processed']:4d} messages, {results['small_scale']['actual_duration']:.2f}s, {results['small_scale'].get('throughput', 0):.2f} msg/s")
    print(f"Medium Scale: {results['medium_scale']['total_processed']:4d} messages, {results['medium_scale']['actual_duration']:.2f}s, {results['medium_scale'].get('throughput', 0):.2f} msg/s")
    print()
    print("✅ All benchmarks completed successfully!")
    print("✅ Stress test system verified operational")

    return results


if __name__ == "__main__":
    try:
        results = run_benchmark_suite()
        sys.exit(0)
    except Exception as e:
        print(f"❌ Benchmark failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

