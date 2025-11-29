# Stress Test Metrics Dashboard - Usage Guide

**Author**: Agent-5 (Business Intelligence Specialist)  
**Date**: 2025-11-28

---

## Overview

Comprehensive metrics collection and JSON dashboard system for stress testing the messaging infrastructure.

---

## Quick Start

```python
from src.core.stress_test_metrics import StressTestMetricsCollector, StressTestAnalyzer
from pathlib import Path

# Initialize collector
collector = StressTestMetricsCollector()

# Start test
collector.start_test({
    "test_name": "message_delivery_stress_test",
    "duration_seconds": 300,
    "message_rate": 100,  # messages/second
})

# During test: Record metrics
collector.record_message_delivered(
    latency_ms=45.5,
    agent_id="Agent-7",
    message_type="direct",
    delivery_mode="real"
)

collector.record_queue_depth(15)

# Stop test and generate dashboard
collector.stop_test()
dashboard = collector.generate_dashboard_json(Path("results/"))

# Analyze results
analyzer = StressTestAnalyzer()
bottlenecks = analyzer.identify_bottlenecks(dashboard)
failure_patterns = analyzer.analyze_failure_patterns(dashboard)
```

---

## Metrics Collected

### Overall Metrics
- **Latency Percentiles**: p50, p95, p99
- **Throughput**: Messages per second
- **Failure Rate**: Percentage of failed deliveries
- **Queue Depth**: Max, average, current

### Per-Agent Metrics
- Delivery times per agent
- Success rates per agent
- Failure counts per agent

### Per-Message-Type Metrics
- Direct messages
- Broadcast messages
- Hard onboarding messages
- Soft onboarding messages

### Chaos Mode Metrics
- Crash recovery times
- Spike detection and handling
- Chaos event tracking

### Comparison Metrics
- Real delivery vs mock delivery performance
- Performance difference analysis

---

## JSON Dashboard Schema

```json
{
  "test_metadata": {
    "start_time": "2025-11-28T15:30:00",
    "end_time": "2025-11-28T15:35:00",
    "duration_seconds": 300,
    "config": {...}
  },
  "overall_metrics": {
    "latency_percentiles": {
      "p50": 45.2,
      "p95": 123.5,
      "p99": 234.1
    },
    "throughput_msg_per_sec": 98.5,
    "failure_rate_percent": 0.5,
    "queue_depth": {
      "max": 25,
      "avg": 10.2,
      "current": 5
    }
  },
  "per_agent_metrics": {
    "Agent-7": {
      "latency_percentiles": {...},
      "failure_rate_percent": 0.2,
      ...
    }
  },
  "per_message_type_metrics": {
    "direct": {...},
    "broadcast": {...}
  },
  "chaos_mode_metrics": {...},
  "comparison_metrics": {...},
  "failure_analysis": {...}
}
```

---

## Integration Example

```python
from src.core.stress_test_metrics_integration import StressTestMetricsIntegration

# Initialize integration
integration = StressTestMetricsIntegration()

# Start stress test
collector = integration.integrate_with_stress_test_runner({
    "test_name": "high_load_test",
    "message_count": 10000,
})

# Record events during test
integration.record_queue_event(
    "message_queued",
    queue_id="msg_123",
    agent_id="Agent-7",
    message_type="direct",
    queue_depth=10
)

integration.record_queue_event(
    "message_delivered",
    queue_id="msg_123",
    agent_id="Agent-7",
    message_type="direct",
    latency_ms=42.3,
    delivery_mode="real"
)

# Finalize and generate dashboard
dashboard = integration.finalize_stress_test("results/")
```

---

## Analysis Functions

### Identify Bottlenecks

```python
analyzer = StressTestAnalyzer()
bottlenecks = analyzer.identify_bottlenecks(dashboard)

# Returns list of bottleneck issues:
# - High latency bottlenecks
# - Low throughput bottlenecks
# - Queue depth bottlenecks
# - Per-agent bottlenecks
```

### Analyze Failure Patterns

```python
failure_patterns = analyzer.analyze_failure_patterns(dashboard)

# Returns failure analysis:
# - Overall failure rate
# - Per-agent failure patterns
# - Per-message-type failure patterns
# - Failure reasons breakdown
```

---

## File Output

Dashboard JSON files are saved as:
```
stress_test_results_YYYYMMDD_HHMMSS.json
```

Example: `stress_test_results_20251128_153000.json`

---

## Requirements Met

✅ Collect metrics: latency (p50, p95, p99), throughput (msg/sec), failure rate, queue depth  
✅ Track per-agent metrics (delivery times, success rates)  
✅ Track per-message-type metrics (direct, broadcast, hard_onboard, soft_onboard)  
✅ Generate JSON dashboard: stress_test_results_{timestamp}.json  
✅ Include chaos mode metrics (crash recovery, spike handling)  
✅ Include comparison metrics (real vs mock delivery performance)  
✅ Integration with stress test runner  
✅ Analysis functions (identify bottlenecks, failure patterns)

---

*Agent-5 - Business Intelligence Specialist*

