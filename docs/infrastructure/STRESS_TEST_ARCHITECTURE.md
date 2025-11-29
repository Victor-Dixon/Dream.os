# 🧪 Stress Test Architecture Design

**Date**: 2025-11-28  
**Agent**: Agent-2 (Architecture & Design Specialist)  
**Status**: ✅ **ARCHITECTURE DESIGN COMPLETE**  
**Priority**: HIGH

---

## 🎯 **MISSION OVERVIEW**

Design architecture for stress testing MessageQueueProcessor with **zero real agent interaction**. Pure simulation using mock messaging core injection.

**Goal**: Test message queue processing at scale (9 concurrent agents, 4 message types) without touching real agents.

---

## 📋 **REQUIREMENTS**

1. ✅ Dependency injection point for MessageQueueProcessor
2. ✅ MockMessagingCore interface matching send_message signature
3. ✅ Stress tester module structure (mock core, stress runner, metrics collector)
4. ✅ Zero real agent interaction (pure simulation)
5. ✅ Support 9 concurrent agents, 4 message types (direct, broadcast, hard_onboard, soft_onboard)

---

## 🏗️ **ARCHITECTURE DESIGN**

### **1. Dependency Injection Point**

#### **Location**: `src/core/message_queue_processor.py`

**Current Implementation**:
```python
def _deliver_via_core(self, recipient: str, content: str, metadata: dict = None) -> bool:
    from .messaging_core import send_message
    # ... uses send_message directly
```

**Proposed Injection Point**:
```python
class MessageQueueProcessor:
    def __init__(
        self,
        queue: Optional[MessageQueue] = None,
        message_repository: Optional[Any] = None,
        config: Optional[QueueConfig] = None,
        messaging_core: Optional[MessagingCoreProtocol] = None,  # NEW: Injection point
    ) -> None:
        self.messaging_core = messaging_core or self._get_default_messaging_core()
    
    def _get_default_messaging_core(self) -> MessagingCoreProtocol:
        """Get default real messaging core (production)."""
        from .messaging_core import send_message
        return RealMessagingCoreAdapter(send_message)
    
    def _deliver_via_core(self, recipient: str, content: str, metadata: dict = None) -> bool:
        """Use injected messaging core (real or mock)."""
        return self.messaging_core.send_message(
            content=content,
            sender="SYSTEM",
            recipient=recipient,
            message_type=UnifiedMessageType.SYSTEM_TO_AGENT,
            priority=UnifiedMessagePriority.REGULAR,
            tags=[UnifiedMessageTag.SYSTEM],
            metadata=metadata or {},
        )
```

**Benefits**:
- ✅ Backward compatible (defaults to real core)
- ✅ Clean separation of concerns
- ✅ Easy to inject mock for testing
- ✅ No changes to existing callers

---

### **2. MockMessagingCore Interface**

#### **Location**: `src/core/stress_testing/messaging_core_protocol.py`

**Protocol Definition**:
```python
from typing import Protocol, Any
from ..messaging_models_core import (
    UnifiedMessageType,
    UnifiedMessagePriority,
    UnifiedMessageTag,
)

class MessagingCoreProtocol(Protocol):
    """Protocol for messaging core (real or mock)."""
    
    def send_message(
        self,
        content: str,
        sender: str,
        recipient: str,
        message_type: UnifiedMessageType,
        priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR,
        tags: list[UnifiedMessageTag] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> bool:
        """Send message - matches real messaging_core.send_message signature."""
        ...
```

**Mock Implementation**:
```python
class MockMessagingCore:
    """Mock messaging core for stress testing - zero real agent interaction."""
    
    def __init__(self, metrics_collector: Optional[MetricsCollector] = None):
        self.metrics_collector = metrics_collector
        self.sent_messages: list[dict] = []
        self.delivery_success_rate: float = 1.0  # Configurable for failure testing
    
    def send_message(
        self,
        content: str,
        sender: str,
        recipient: str,
        message_type: UnifiedMessageType,
        priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR,
        tags: list[UnifiedMessageTag] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> bool:
        """Simulate message delivery - no real agent interaction."""
        import random
        
        # Record message for metrics
        message_record = {
            "content": content,
            "sender": sender,
            "recipient": recipient,
            "message_type": message_type,
            "priority": priority,
            "tags": tags or [],
            "metadata": metadata or {},
            "timestamp": datetime.now(),
            "delivered": random.random() < self.delivery_success_rate,
        }
        
        self.sent_messages.append(message_record)
        
        # Collect metrics
        if self.metrics_collector:
            self.metrics_collector.record_message(message_record)
        
        # Simulate delivery delay (configurable)
        time.sleep(0.001)  # 1ms simulation delay
        
        return message_record["delivered"]
    
    def get_sent_messages(self) -> list[dict]:
        """Get all sent messages for analysis."""
        return self.sent_messages.copy()
    
    def reset(self):
        """Reset mock state for new test run."""
        self.sent_messages.clear()
```

**Real Core Adapter**:
```python
class RealMessagingCoreAdapter:
    """Adapter wrapping real messaging_core.send_message for protocol compliance."""
    
    def __init__(self, send_message_func):
        self._send_message = send_message_func
    
    def send_message(
        self,
        content: str,
        sender: str,
        recipient: str,
        message_type: UnifiedMessageType,
        priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR,
        tags: list[UnifiedMessageTag] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> bool:
        """Delegate to real messaging core."""
        return self._send_message(
            content, sender, recipient, message_type, priority, tags, metadata
        )
```

---

### **3. Stress Tester Module Structure**

#### **Directory**: `src/core/stress_testing/`

```
src/core/stress_testing/
├── __init__.py
├── messaging_core_protocol.py      # Protocol definition
├── mock_messaging_core.py          # Mock implementation
├── real_messaging_core_adapter.py # Real core adapter
├── stress_runner.py                # Main stress test orchestrator
├── metrics_collector.py            # Metrics collection and analysis
└── message_generator.py            # Test message generation
```

#### **File Responsibilities**:

**1. `messaging_core_protocol.py`**
- Protocol definition (`MessagingCoreProtocol`)
- Type hints and interfaces
- Documentation

**2. `mock_messaging_core.py`**
- `MockMessagingCore` class
- Zero real agent interaction
- Configurable success rates
- Message recording

**3. `real_messaging_core_adapter.py`**
- `RealMessagingCoreAdapter` class
- Wraps real `send_message` function
- Protocol compliance

**4. `stress_runner.py`**
- `StressTestRunner` class
- Orchestrates stress tests
- Manages concurrent agents
- Coordinates message generation and processing

**5. `metrics_collector.py`**
- `MetricsCollector` class
- Records message delivery metrics
- Calculates statistics (throughput, latency, success rate)
- Generates reports

**6. `message_generator.py`**
- `MessageGenerator` class
- Generates test messages (4 types: direct, broadcast, hard_onboard, soft_onboard)
- Supports 9 concurrent agents
- Configurable message patterns

---

### **4. Stress Test Runner Design**

#### **Class**: `StressTestRunner`

```python
class StressTestRunner:
    """Orchestrates stress tests for MessageQueueProcessor."""
    
    def __init__(
        self,
        num_agents: int = 9,
        messages_per_agent: int = 100,
        message_types: list[str] = None,
    ):
        self.num_agents = num_agents
        self.messages_per_agent = messages_per_agent
        self.message_types = message_types or ["direct", "broadcast", "hard_onboard", "soft_onboard"]
        
        # Initialize components
        self.metrics_collector = MetricsCollector()
        self.mock_core = MockMessagingCore(self.metrics_collector)
        self.message_generator = MessageGenerator(self.num_agents, self.message_types)
    
    def run_stress_test(self) -> dict:
        """Run complete stress test."""
        # Create processor with mock core
        processor = MessageQueueProcessor(
            messaging_core=self.mock_core  # Inject mock
        )
        
        # Generate test messages
        messages = self.message_generator.generate_batch(
            self.messages_per_agent * self.num_agents
        )
        
        # Enqueue all messages
        for msg in messages:
            processor.queue.enqueue(msg)
        
        # Process queue
        start_time = time.time()
        processed = processor.process_queue(
            max_messages=len(messages),
            batch_size=10,
            interval=0.1,
        )
        end_time = time.time()
        
        # Collect metrics
        metrics = self.metrics_collector.get_metrics()
        metrics["total_processed"] = processed
        metrics["duration"] = end_time - start_time
        metrics["throughput"] = processed / (end_time - start_time)
        
        return metrics
```

---

### **5. Metrics Collector Design**

#### **Class**: `MetricsCollector`

```python
class MetricsCollector:
    """Collects and analyzes stress test metrics."""
    
    def __init__(self):
        self.messages: list[dict] = []
        self.delivery_times: list[float] = []
        self.success_count = 0
        self.failure_count = 0
    
    def record_message(self, message_record: dict):
        """Record a message delivery attempt."""
        self.messages.append(message_record)
        
        if message_record["delivered"]:
            self.success_count += 1
        else:
            self.failure_count += 1
    
    def get_metrics(self) -> dict:
        """Calculate and return metrics."""
        total = self.success_count + self.failure_count
        success_rate = self.success_count / total if total > 0 else 0.0
        
        # Group by message type
        by_type = {}
        for msg in self.messages:
            msg_type = msg["message_type"].value
            by_type[msg_type] = by_type.get(msg_type, 0) + 1
        
        # Group by agent
        by_agent = {}
        for msg in self.messages:
            agent = msg["recipient"]
            by_agent[agent] = by_agent.get(agent, 0) + 1
        
        return {
            "total_messages": total,
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "success_rate": success_rate,
            "by_message_type": by_type,
            "by_agent": by_agent,
        }
```

---

### **6. Message Generator Design**

#### **Class**: `MessageGenerator`

```python
class MessageGenerator:
    """Generates test messages for stress testing."""
    
    def __init__(self, num_agents: int = 9, message_types: list[str] = None):
        self.num_agents = num_agents
        self.message_types = message_types or ["direct", "broadcast", "hard_onboard", "soft_onboard"]
        self.agents = [f"Agent-{i}" for i in range(1, num_agents + 1)]
    
    def generate_batch(self, count: int) -> list[dict]:
        """Generate batch of test messages."""
        messages = []
        
        for i in range(count):
            msg_type = random.choice(self.message_types)
            recipient = random.choice(self.agents) if msg_type != "broadcast" else "ALL"
            
            message = {
                "type": "agent_message",
                "sender": "SYSTEM",
                "recipient": recipient,
                "content": f"Test message {i+1}",
                "priority": "regular",
                "message_type": self._map_message_type(msg_type),
                "tags": ["SYSTEM"],
                "metadata": {"test": True, "message_id": i+1},
            }
            
            messages.append(message)
        
        return messages
    
    def _map_message_type(self, msg_type: str) -> str:
        """Map message type string to UnifiedMessageType."""
        mapping = {
            "direct": "SYSTEM_TO_AGENT",
            "broadcast": "BROADCAST",
            "hard_onboard": "ONBOARDING",
            "soft_onboard": "ONBOARDING",
        }
        return mapping.get(msg_type, "SYSTEM_TO_AGENT")
```

---

## 🔒 **ZERO REAL AGENT INTERACTION**

### **Guarantees**:

1. **Mock Core Only**: `MockMessagingCore` never calls real messaging functions
2. **No PyAutoGUI**: Mock core doesn't import or use PyAutoGUI
3. **No File I/O**: Mock core doesn't write to inbox directories
4. **Pure Simulation**: All delivery is simulated with configurable delays
5. **Isolated Testing**: Stress tests run in isolated environment

### **Validation**:
```python
# In mock_messaging_core.py
def send_message(...) -> bool:
    """Simulate message delivery - NO REAL AGENT INTERACTION."""
    # ✅ No imports of real messaging_core
    # ✅ No PyAutoGUI calls
    # ✅ No file system writes
    # ✅ Only in-memory simulation
    return simulated_delivery_result
```

---

## 📊 **SUPPORTED CONFIGURATIONS**

### **9 Concurrent Agents**:
- Agent-1 through Agent-9
- Configurable via `num_agents` parameter
- Each agent receives messages independently

### **4 Message Types**:
1. **direct**: Direct agent-to-agent messages
2. **broadcast**: Broadcast to all agents
3. **hard_onboard**: Hard onboarding messages
4. **soft_onboard**: Soft onboarding messages

### **Message Type Mapping**:
```python
MESSAGE_TYPE_MAPPING = {
    "direct": UnifiedMessageType.SYSTEM_TO_AGENT,
    "broadcast": UnifiedMessageType.BROADCAST,
    "hard_onboard": UnifiedMessageType.ONBOARDING,
    "soft_onboard": UnifiedMessageType.ONBOARDING,
}
```

---

## 🚀 **USAGE EXAMPLE**

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

# Analyze results
print(f"Total processed: {metrics['total_processed']}")
print(f"Success rate: {metrics['success_rate']:.2%}")
print(f"Throughput: {metrics['throughput']:.2f} msg/s")
print(f"By type: {metrics['by_message_type']}")
print(f"By agent: {metrics['by_agent']}")
```

---

## ✅ **ARCHITECTURE BENEFITS**

1. **Zero Real Interaction**: Pure simulation, no agent impact
2. **Dependency Injection**: Clean, testable design
3. **Protocol-Based**: Type-safe interface matching
4. **Scalable**: Supports any number of agents/messages
5. **Metrics-Driven**: Comprehensive performance analysis
6. **Backward Compatible**: No breaking changes to existing code

---

## 📝 **IMPLEMENTATION CHECKLIST**

- [ ] Create `src/core/stress_testing/` directory
- [ ] Implement `MessagingCoreProtocol`
- [ ] Implement `MockMessagingCore`
- [ ] Implement `RealMessagingCoreAdapter`
- [ ] Add injection point to `MessageQueueProcessor`
- [ ] Implement `StressTestRunner`
- [ ] Implement `MetricsCollector`
- [ ] Implement `MessageGenerator`
- [ ] Create unit tests for stress testing components
- [ ] Document usage examples

---

**Status**: ✅ **ARCHITECTURE DESIGN COMPLETE**  
**Ready For**: Implementation  
**Next Step**: Create implementation files

---

*Agent-2 (Architecture & Design Specialist)*

