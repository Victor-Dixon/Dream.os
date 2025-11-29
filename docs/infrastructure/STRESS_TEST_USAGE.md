# 🧪 Stress Test Usage Guide

**Date**: 2025-01-28  
**Author**: Agent-6 (Coordination & Communication Specialist)  
**Status**: ✅ **READY FOR USE**

---

## 🎯 **OVERVIEW**

The stress testing system allows you to test message queue processing at scale **without touching real agents**. It uses pure simulation with mock messaging core injection.

**Key Features**:
- ✅ Zero real agent interaction
- ✅ 9 concurrent agents support
- ✅ 4 message types (direct, broadcast, hard_onboard, soft_onboard)
- ✅ Comprehensive metrics collection
- ✅ Chaos mode for failure testing
- ✅ Comparison mode (real vs mock)

---

## 🚀 **QUICK START**

### **Basic Usage**

```python
from src.core.stress_testing.stress_runner import StressTestRunner

# Create stress test runner
runner = StressTestRunner(
    num_agents=9,
    messages_per_agent=100,
    message_types=["direct", "broadcast", "hard_onboard", "soft_onboard"],
)

# Run stress test
metrics = runner.run_stress_test()

# View results
print(f"Total processed: {metrics['total_processed']}")
print(f"Success rate: {metrics['success_rate']:.2%}")
print(f"Throughput: {metrics['throughput']:.2f} msg/s")
```

### **CLI Usage**

```bash
# Run standard stress test (9 agents, 100 messages each)
python -m src.core.stress_testing.stress_test_9_agents

# Run with custom parameters
python -m src.core.stress_testing.stress_test_9_agents \
    --agents 9 \
    --messages-per-agent 200 \
    --message-types direct,broadcast,hard_onboard,soft_onboard

# Run with chaos mode
python -m src.core.stress_testing.stress_test_9_agents --chaos

# Run comparison mode (real vs mock)
python -m src.core.stress_testing.stress_test_9_agents --compare
```

---

## 📋 **CONFIGURATION OPTIONS**

### **StressTestRunner Parameters**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `num_agents` | int | 9 | Number of concurrent agents to simulate |
| `messages_per_agent` | int | 100 | Messages to send per agent |
| `message_types` | list[str] | All 4 types | Message types to test |
| `chaos_mode` | bool | False | Enable chaos mode (random failures) |
| `delivery_success_rate` | float | 1.0 | Mock delivery success rate (0.0-1.0) |

### **Message Types**

- **`direct`**: Direct agent-to-agent messages (`SYSTEM_TO_AGENT`)
- **`broadcast`**: Broadcast to all agents (`BROADCAST`)
- **`hard_onboard`**: Hard onboarding messages (`ONBOARDING`)
- **`soft_onboard`**: Soft onboarding messages (`ONBOARDING`)

---

## 📊 **METRICS OUTPUT**

### **Metrics Dictionary Structure**

```json
{
  "total_processed": 900,
  "success_count": 900,
  "failure_count": 0,
  "success_rate": 1.0,
  "duration": 12.5,
  "throughput": 72.0,
  "by_message_type": {
    "SYSTEM_TO_AGENT": 450,
    "BROADCAST": 225,
    "ONBOARDING": 225
  },
  "by_agent": {
    "Agent-1": 100,
    "Agent-2": 100,
    "Agent-3": 100,
    "Agent-4": 100,
    "Agent-5": 100,
    "Agent-6": 100,
    "Agent-7": 100,
    "Agent-8": 100,
    "Agent-9": 100
  },
  "latency_stats": {
    "min_ms": 1.0,
    "max_ms": 5.0,
    "avg_ms": 2.5,
    "p95_ms": 4.0
  }
}
```

### **Metrics Dashboard JSON**

The metrics are automatically saved to:
```
logs/stress_test_metrics_<timestamp>.json
```

---

## 🔍 **VALIDATION**

### **Integration Validation**

Before running stress tests, validate that mock delivery never touches real agents:

```bash
python tools/validate_stress_test_integration.py
```

**Checks Performed**:
- ✅ No real messaging_core imports
- ✅ No PyAutoGUI usage
- ✅ No inbox file writes
- ✅ Protocol compliance
- ✅ Injection point exists
- ✅ Mock isolation

### **Queue Behavior Validation**

Validate queue behavior under load:

```bash
python tools/validate_queue_behavior_under_load.py
```

**Tests Performed**:
- ✅ Queue size limits
- ✅ Message ordering
- ✅ Priority handling
- ✅ Concurrent access safety
- ✅ Memory usage bounds
- ✅ Processing throughput

---

## 🎮 **ADVANCED USAGE**

### **Chaos Mode**

Enable chaos mode to test failure scenarios:

```python
runner = StressTestRunner(
    num_agents=9,
    messages_per_agent=100,
    chaos_mode=True,
    delivery_success_rate=0.9,  # 10% failure rate
)

metrics = runner.run_stress_test()
```

**Chaos Mode Features**:
- Random delivery failures
- Latency spikes
- Queue saturation
- Memory pressure simulation

### **Comparison Mode**

Compare real vs mock delivery performance:

```python
runner = StressTestRunner(
    num_agents=9,
    messages_per_agent=50,
    compare_mode=True,  # Runs both real and mock
)

comparison = runner.run_comparison()
```

**Comparison Output**:
```json
{
  "real": {
    "throughput": 50.0,
    "success_rate": 0.98,
    "avg_latency_ms": 20.0
  },
  "mock": {
    "throughput": 72.0,
    "success_rate": 1.0,
    "avg_latency_ms": 2.5
  },
  "difference": {
    "throughput_ratio": 1.44,
    "latency_ratio": 0.125
  }
}
```

### **Custom Message Generator**

Generate custom test messages:

```python
from src.core.stress_testing.message_generator import MessageGenerator

generator = MessageGenerator(
    num_agents=9,
    message_types=["direct", "broadcast"]
)

messages = generator.generate_batch(count=500)
```

---

## 📝 **EXAMPLE TEST RUNS**

### **Example 1: Standard Stress Test**

```bash
$ python -m src.core.stress_testing.stress_test_9_agents

🧪 Starting Stress Test...
📊 Configuration:
   Agents: 9
   Messages per agent: 100
   Total messages: 900
   Message types: direct, broadcast, hard_onboard, soft_onboard

🔄 Processing queue...
✅ Processing complete!

📊 Results:
   Total processed: 900
   Success rate: 100.00%
   Throughput: 72.0 msg/s
   Duration: 12.5s

📈 By Message Type:
   SYSTEM_TO_AGENT: 450
   BROADCAST: 225
   ONBOARDING: 225

📈 By Agent:
   Agent-1: 100
   Agent-2: 100
   ...
   Agent-9: 100

💾 Metrics saved to: logs/stress_test_metrics_20250128_143000.json
```

### **Example 2: Chaos Mode Test**

```bash
$ python -m src.core.stress_testing.stress_test_9_agents --chaos

🧪 Starting Stress Test (Chaos Mode)...
⚠️  Chaos mode enabled - random failures will occur

📊 Results:
   Total processed: 900
   Success rate: 89.67%
   Failures: 93
   Throughput: 65.2 msg/s
   
⚠️  Chaos events:
   - 45 delivery failures
   - 12 latency spikes
   - 8 queue saturation events
```

### **Example 3: High Load Test**

```bash
$ python -m src.core.stress_testing.stress_test_9_agents \
    --agents 9 \
    --messages-per-agent 1000

🧪 Starting High Load Stress Test...
📊 Configuration:
   Agents: 9
   Messages per agent: 1000
   Total messages: 9000

🔄 Processing queue...
✅ Processing complete!

📊 Results:
   Total processed: 9000
   Success rate: 100.00%
   Throughput: 68.5 msg/s
   Duration: 131.4s
   Memory peak: 45.2 MB
```

---

## 🔒 **SAFETY GUARANTEES**

### **Zero Real Agent Interaction**

The stress test system guarantees:

1. **Mock Core Only**: `MockMessagingCore` never calls real messaging functions
2. **No PyAutoGUI**: Mock core doesn't import or use PyAutoGUI
3. **No File I/O**: Mock core doesn't write to inbox directories
4. **Pure Simulation**: All delivery is simulated with configurable delays
5. **Isolated Testing**: Stress tests run in isolated environment

### **Validation Before Use**

Always run validation before stress testing:

```bash
# Validate integration safety
python tools/validate_stress_test_integration.py

# Validate queue behavior
python tools/validate_queue_behavior_under_load.py
```

---

## 🐛 **TROUBLESHOOTING**

### **Common Issues**

**Issue**: Import errors when running stress test
```bash
# Solution: Make sure you're in repository root
cd /path/to/Agent_Cellphone_V2_Repository
python -m src.core.stress_testing.stress_test_9_agents
```

**Issue**: Queue size limit exceeded
```bash
# Solution: Reduce messages per agent or increase max_queue_size
runner = StressTestRunner(
    messages_per_agent=50,  # Reduced from 100
)
```

**Issue**: Low throughput
```bash
# Solution: Check system resources, reduce batch size
config = QueueConfig(processing_batch_size=5)  # Smaller batches
```

---

## 📚 **ADDITIONAL RESOURCES**

- **Architecture Design**: `docs/infrastructure/STRESS_TEST_ARCHITECTURE.md`
- **Integration Validation**: `tools/validate_stress_test_integration.py`
- **Queue Validation**: `tools/validate_queue_behavior_under_load.py`
- **Metrics Dashboard**: `logs/stress_test_metrics_*.json`

---

## ✅ **BEST PRACTICES**

1. **Always Validate First**: Run validation scripts before stress testing
2. **Start Small**: Begin with small message counts, then scale up
3. **Monitor Resources**: Watch memory and CPU usage during tests
4. **Save Metrics**: Metrics are automatically saved, review them after tests
5. **Use Chaos Mode**: Test failure scenarios regularly
6. **Compare Performance**: Use comparison mode to benchmark improvements

---

**🐝 WE. ARE. SWARM. ⚡🔥**

*Agent-6 - Coordination & Communication Specialist*

