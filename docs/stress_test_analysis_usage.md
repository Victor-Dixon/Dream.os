# Stress Test Metrics Analysis - Usage Guide

**Author**: Agent-5 (Business Intelligence Specialist)  
**Date**: 2025-11-29

---

## Overview

Comprehensive analysis system for stress test metrics that provides:
- Latency pattern analysis (p50, p95, p99)
- Bottleneck identification
- Optimization opportunities
- Performance recommendations
- Dashboard visualization data

---

## Quick Start

```bash
# Analyze latest stress test dashboard
python -m tools.analyze_stress_test_metrics --find-latest

# Analyze specific dashboard file
python -m tools.analyze_stress_test_metrics stress_test_results/stress_test_results_20251129_120000.json

# Generate visualization data only
python -m tools.analyze_stress_test_metrics --find-latest --visualization-only
```

---

## Analysis Components

### 1. Latency Pattern Analysis

Analyzes latency distribution and identifies:
- Tail latency severity (p99/p50 ratio)
- Latency consistency
- Anomalies in latency patterns

### 2. Bottleneck Identification

Identifies performance bottlenecks:
- High latency (p99 > 500ms)
- Low throughput (< 50 msg/sec)
- High failure rate (> 1%)
- Queue depth issues (> 100 items)
- Per-agent bottlenecks

### 3. Optimization Opportunities

Generates actionable optimization opportunities with:
- Priority levels (high/medium)
- Specific recommendations
- Expected impact estimates
- Action items

### 4. Performance Recommendations

Comprehensive recommendations including:
- Critical actions (high priority)
- Recommended actions (medium priority)
- Latency insights and recommendations
- Bottleneck-specific recommendations

### 5. Dashboard Visualization Data

Generates data structures for visualization:
- Latency distribution charts
- Throughput timeline
- Failure rate timeline
- Queue depth timeline
- Per-agent comparison
- Message type analysis

---

## Report Output

### JSON Report

Full analysis report in JSON format:
- Executive summary
- Latency analysis
- Bottleneck analysis with severity breakdown
- Optimization opportunities
- Performance recommendations
- Dashboard visualization data
- Key findings
- Action items

### Markdown Summary

Human-readable summary report:
- Executive summary
- Key findings
- Top bottlenecks
- Recommended action items

---

## Integration with Stress Tests

The analysis system integrates seamlessly with stress test runs:

```python
from src.core.stress_test_metrics_integration import StressTestMetricsIntegration
from src.core.stress_test_analysis_report import StressTestAnalysisReport

# Run stress test with metrics
integration = StressTestMetricsIntegration()
collector = integration.integrate_with_stress_test_runner({
    "test_name": "high_load_test",
    "message_count": 10000,
})

# ... run stress test ...

# Generate dashboard
dashboard = integration.finalize_stress_test("results/")

# Analyze results
report_generator = StressTestAnalysisReport(dashboard)
report = report_generator.generate_full_report("analysis_results/")
```

---

## Example Output

```
📊 SUMMARY:
   Status: NEEDS_ATTENTION
   P99 Latency: 1234.56 ms
   Throughput: 45.23 msg/sec
   Critical Issues: 2

Bottlenecks Identified:
- High latency (p99: 1234.56ms) - Priority: HIGH
- Low throughput (45.23 msg/sec) - Priority: MEDIUM

Optimization Opportunities:
- Latency optimization: Expected 20-40% reduction
- Throughput optimization: Expected 50-100% improvement
```

---

*Agent-5 - Business Intelligence Specialist*

