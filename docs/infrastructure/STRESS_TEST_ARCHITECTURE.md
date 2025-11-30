# 🧪 Stress Test Architecture Design - Mock Messaging Core

**Date**: 2025-11-29  
**Agent**: Agent-2 (Architecture & Design Specialist)  
**Status**: ✅ **ARCHITECTURE DESIGN COMPLETE**  
**Priority**: HIGH  
**Version**: 2.0 (Enhanced Dependency Injection)

---

## 🎯 **MISSION OVERVIEW**

Design clean architecture for stress testing MessageQueueProcessor with **zero real agent interaction**. Pure simulation using dependency injection pattern that allows mock replacement without code changes.

**Goal**: Test message queue processing at scale (9 concurrent agents, 4 message types) without touching real agents. Architecture must support easy swapping between real and mock implementations.

---

## 📋 **REQUIREMENTS**

1. ✅ **Dependency Injection Point**: Clean injection in MessageQueueProcessor
2. ✅ **Interface Definitions**: Protocol-based interfaces for mock injection
3. ✅ **Module Structure Plan**: Clear file/class responsibilities
4. ✅ **Zero Real Agent Interaction**: Pure simulation guarantee
5. ✅ **Easy Swapping**: No code changes required to swap implementations
6. ✅ **Support 9 Concurrent Agents**: Agent-1 through Agent-9
7. ✅ **Support 4 Message Types**: direct, broadcast, hard_onboard, soft_onboard

---

## 🏗️ **ARCHITECTURE DESIGN**

### **1. Dependency Injection Pattern**

#### **Core Principle**: Constructor Injection with Protocol-Based Interface

**Location**: `src/core/message_queue_processor.py`

**Current Implementation** (Already Implemented):
```python
class MessageQueueProcessor:
    def __init__(
        self,
        queue: Optional[MessageQueue] = None,
        message_repository: Optional[Any] = None,
        config: Optional[QueueConfig] = None,
        messaging_core: Optional[Any] = None,  # ✅ Injection point exists
    ) -> None:
        self.messaging_core = messaging_core  # Injected core
        # ... rest of initialization
```

**Usage Pattern**:
```python
# Production: Use real messaging core (default)
processor = MessageQueueProcessor()  # Uses real core automatically

# Testing: Inject mock core
mock_core = MockMessagingCore(metrics_collector)
processor = MessageQueueProcessor(messaging_core=mock_core)  # Uses mock
```

**Benefits**:
- ✅ **Backward Compatible**: Default behavior unchanged
- ✅ **Zero Code Changes**: Swap implementations via constructor
- ✅ **Type Safe**: Protocol ensures interface compliance
- ✅ **Testable**: Easy to inject mocks for testing

---

### **2. Interface Definitions**

#### **Protocol Definition**: `MessagingCoreProtocol`

**Location**: `src/core/stress_testing/messaging_core_protocol.py`

**Interface Contract**:
```python
from typing import Protocol, Any
from ..messaging_models_core import (
    UnifiedMessageType,
    UnifiedMessagePriority,
    UnifiedMessageTag,
)

class MessagingCoreProtocol(Protocol):
    """
    Protocol for messaging core (real or mock).
    
    This protocol defines the contract that both real and mock
    messaging cores must implement. Any implementation that matches
    this signature can be injected into MessageQueueProcessor.
    """
    
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
        """
        Send message - matches real messaging_core.send_message signature.
        
        Args:
            content: Message content
            sender: Message sender
            recipient: Message recipient
            message_type: Type of message
            priority: Message priority
            tags: Message tags
            metadata: Additional metadata
            
        Returns:
            True if delivery successful, False otherwise
        """
        ...
```

**Interface Compliance**:
- ✅ **Real Core**: `RealMessagingCoreAdapter` implements protocol
- ✅ **Mock Core**: `MockMessagingCore` implements protocol
- ✅ **Type Safety**: Protocol ensures signature matching
- ✅ **Runtime Check**: Python's structural typing validates compliance

---

### **3. Module Structure Plan**

#### **Directory**: `src/core/stress_testing/`

```
src/core/stress_testing/
├── __init__.py                          # Module exports
├── messaging_core_protocol.py           # Protocol definition (interface)
├── mock_messaging_core.py               # Mock implementation
├── real_messaging_core_adapter.py       # Real core adapter
├── stress_runner.py                     # Main stress test orchestrator
├── metrics_collector.py                 # Metrics collection and analysis
└── message_generator.py                # Test message generation
```

#### **File Responsibilities**:

**1. `messaging_core_protocol.py`** (Interface Definition)
- **Purpose**: Define protocol contract for messaging cores
- **Exports**: `MessagingCoreProtocol`
- **Responsibilities**:
  - Protocol definition with type hints
  - Interface documentation
  - Contract validation

**2. `mock_messaging_core.py`** (Mock Implementation)
- **Purpose**: Simulate message delivery without real agent interaction
- **Exports**: `MockMessagingCore`
- **Responsibilities**:
  - Implement `MessagingCoreProtocol`
  - Simulate delivery with configurable success rates
  - Record messages for metrics
  - Zero real agent interaction guarantee

**3. `real_messaging_core_adapter.py`** (Real Core Adapter)
- **Purpose**: Wrap real messaging core for protocol compliance
- **Exports**: `RealMessagingCoreAdapter`
- **Responsibilities**:
  - Wrap real `send_message` function
  - Implement `MessagingCoreProtocol`
  - Provide adapter pattern for real core

**4. `stress_runner.py`** (Orchestrator)
- **Purpose**: Coordinate stress test execution
- **Exports**: `StressTestRunner`
- **Responsibilities**:
  - Initialize components (mock core, metrics, generator)
  - Create MessageQueueProcessor with injected mock
  - Generate and enqueue test messages
  - Process queue and collect metrics
  - Return comprehensive test results

**5. `metrics_collector.py`** (Metrics Collection)
- **Purpose**: Collect and analyze stress test metrics
- **Exports**: `MetricsCollector`
- **Responsibilities**:
  - Record message delivery attempts
  - Calculate statistics (throughput, latency, success rate)
  - Group metrics by message type and agent
  - Generate comprehensive reports

**6. `message_generator.py`** (Test Data Generation)
- **Purpose**: Generate test messages for stress testing
- **Exports**: `MessageGenerator`
- **Responsibilities**:
  - Generate test messages (4 types: direct, broadcast, hard_onboard, soft_onboard)
  - Support 9 concurrent agents
  - Configurable message patterns
  - Realistic message content generation

---

### **4. Dependency Injection Implementation**

#### **MessageQueueProcessor Integration**

**Current Implementation** (Already Complete):
```python
class MessageQueueProcessor:
    def __init__(
        self,
        queue: Optional[MessageQueue] = None,
        message_repository: Optional[Any] = None,
        config: Optional[QueueConfig] = None,
        messaging_core: Optional[Any] = None,  # ✅ Injection point
    ) -> None:
        self.config = config or QueueConfig()
        self.queue = queue or MessageQueue(config=self.config)
        self.message_repository = message_repository
        self.messaging_core = messaging_core  # Injected core (None = use default)
        self.running = False
    
    def _deliver_via_core(self, recipient: str, content: str, metadata: dict = None) -> bool:
        """Use injected messaging core (real or mock)."""
        if self.messaging_core:
            # Use injected core (mock for testing, real for production)
            return self.messaging_core.send_message(
                content=content,
                sender="SYSTEM",
                recipient=recipient,
                message_type=UnifiedMessageType.TEXT,
                priority=UnifiedMessagePriority.REGULAR,
                tags=[UnifiedMessageTag.SYSTEM],
                metadata=metadata or {},
            )
        else:
            # Default: Use real messaging core (backward compatible)
            from .messaging_core import send_message
            return send_message(
                content=content,
                sender="SYSTEM",
                recipient=recipient,
                message_type=UnifiedMessageType.TEXT,
                priority=UnifiedMessagePriority.REGULAR,
                tags=[UnifiedMessageTag.SYSTEM],
                metadata=metadata or {},
            )
```

**Injection Pattern**:
```python
# Production: No injection (uses real core)
processor = MessageQueueProcessor()

# Testing: Inject mock core
mock_core = MockMessagingCore(metrics_collector)
processor = MessageQueueProcessor(messaging_core=mock_core)

# Alternative: Inject real core adapter (explicit)
from src.core.messaging_core import send_message
real_adapter = RealMessagingCoreAdapter(send_message)
processor = MessageQueueProcessor(messaging_core=real_adapter)
```

---

### **5. Mock Implementation Details**

#### **MockMessagingCore Class**

**Location**: `src/core/stress_testing/mock_messaging_core.py`

**Key Features**:
- ✅ **Zero Real Interaction**: No PyAutoGUI, no file I/O, no real agents
- ✅ **Configurable Success Rate**: Test failure scenarios
- ✅ **Simulated Delays**: Realistic delivery timing
- ✅ **Message Recording**: Track all messages for analysis
- ✅ **Metrics Integration**: Automatic metrics collection

**Implementation**:
```python
class MockMessagingCore:
    """Mock messaging core for stress testing - zero real agent interaction."""
    
    def __init__(
        self,
        metrics_collector: Optional[MetricsCollector] = None,
        delivery_success_rate: float = 1.0,
        simulated_delay: float = 0.001,
    ):
        self.metrics_collector = metrics_collector
        self.delivery_success_rate = delivery_success_rate
        self.simulated_delay = simulated_delay
        self.sent_messages: list[dict] = []
    
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
        """Simulate message delivery - NO REAL AGENT INTERACTION."""
        # Record message
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
        
        # Simulate delivery delay
        time.sleep(self.simulated_delay)
        
        return message_record["delivered"]
```

---

### **6. Real Core Adapter**

#### **RealMessagingCoreAdapter Class**

**Location**: `src/core/stress_testing/real_messaging_core_adapter.py`

**Purpose**: Wrap real messaging core to match protocol interface

**Implementation**:
```python
class RealMessagingCoreAdapter:
    """Adapter wrapping real messaging_core.send_message for protocol compliance."""
    
    def __init__(self, send_message_func: Callable):
        """Initialize adapter with real send_message function."""
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

### **7. Stress Test Runner**

#### **StressTestRunner Class**

**Location**: `src/core/stress_testing/stress_runner.py`

**Orchestration Pattern**:
```python
class StressTestRunner:
    """Orchestrates stress tests for MessageQueueProcessor."""
    
    def __init__(
        self,
        num_agents: int = 9,
        messages_per_agent: int = 100,
        message_types: Optional[list] = None,
    ):
        # Initialize components
        self.metrics_collector = MetricsCollector()
        self.mock_core = MockMessagingCore(self.metrics_collector)
        self.message_generator = MessageGenerator(self.num_agents, self.message_types)
    
    def run_stress_test(
        self, batch_size: int = 10, interval: float = 0.1
    ) -> dict[str, Any]:
        """Run complete stress test."""
        # Create processor with injected mock core
        processor = MessageQueueProcessor(messaging_core=self.mock_core)
        
        # Generate and enqueue messages
        messages = self.message_generator.generate_batch(
            self.messages_per_agent * self.num_agents
        )
        for msg in messages:
            processor.queue.enqueue(msg)
        
        # Process queue
        start_time = time.time()
        processed = processor.process_queue(
            max_messages=len(messages),
            batch_size=batch_size,
            interval=interval,
        )
        end_time = time.time()
        
        # Collect metrics
        metrics = self.metrics_collector.get_metrics()
        metrics["total_processed"] = processed
        metrics["duration"] = end_time - start_time
        metrics["throughput"] = processed / (end_time - start_time) if (end_time - start_time) > 0 else 0.0
        
        return metrics
```

---

## 🔒 **ZERO REAL AGENT INTERACTION GUARANTEES**

### **Safety Mechanisms**:

1. **No PyAutoGUI Imports**: Mock core doesn't import PyAutoGUI
2. **No File I/O**: Mock core doesn't write to inbox directories
3. **No Real Messaging Calls**: Mock core doesn't call real messaging functions
4. **Pure Simulation**: All delivery is in-memory simulation
5. **Isolated Testing**: Stress tests run in isolated environment

### **Validation**:
```python
# In mock_messaging_core.py
def send_message(...) -> bool:
    """
    Simulate message delivery - NO REAL AGENT INTERACTION.
    
    Guarantees:
    - ✅ No imports of real messaging_core
    - ✅ No PyAutoGUI calls
    - ✅ No file system writes
    - ✅ Only in-memory simulation
    """
    # Pure simulation code only
    return simulated_delivery_result
```

---

## 📊 **SUPPORTED CONFIGURATIONS**

### **9 Concurrent Agents**:
- Agent-1 through Agent-9
- Configurable via `num_agents` parameter
- Each agent receives messages independently

### **4 Message Types**:
1. **direct**: Direct agent-to-agent messages (`UnifiedMessageType.TEXT`)
2. **broadcast**: Broadcast to all agents (`UnifiedMessageType.BROADCAST`)
3. **hard_onboard**: Hard onboarding messages (`UnifiedMessageType.ONBOARDING`)
4. **soft_onboard**: Soft onboarding messages (`UnifiedMessageType.ONBOARDING`)

### **Message Type Mapping**:
```python
MESSAGE_TYPE_MAPPING = {
    "direct": UnifiedMessageType.TEXT,
    "broadcast": UnifiedMessageType.BROADCAST,
    "hard_onboard": UnifiedMessageType.ONBOARDING,
    "soft_onboard": UnifiedMessageType.ONBOARDING,
}
```

---

## 🚀 **USAGE EXAMPLES**

### **Basic Stress Test**:
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

### **Custom Mock Configuration**:
```python
from src.core.stress_testing.mock_messaging_core import MockMessagingCore
from src.core.stress_testing.metrics_collector import MetricsCollector
from src.core.message_queue_processor import MessageQueueProcessor

# Create custom mock with failure testing
metrics_collector = MetricsCollector()
mock_core = MockMessagingCore(
    metrics_collector=metrics_collector,
    delivery_success_rate=0.95,  # 5% failure rate
    simulated_delay=0.005,  # 5ms delay
)

# Inject into processor
processor = MessageQueueProcessor(messaging_core=mock_core)
```

### **Production Usage** (Real Core):
```python
from src.core.message_queue_processor import MessageQueueProcessor

# Production: Uses real messaging core (default)
processor = MessageQueueProcessor()
# No injection = uses real core automatically
```

---

## ✅ **ARCHITECTURE BENEFITS**

1. **Zero Real Interaction**: Pure simulation, no agent impact
2. **Dependency Injection**: Clean, testable design
3. **Protocol-Based**: Type-safe interface matching
4. **Easy Swapping**: No code changes required to swap implementations
5. **Backward Compatible**: No breaking changes to existing code
6. **Scalable**: Supports any number of agents/messages
7. **Metrics-Driven**: Comprehensive performance analysis
8. **Isolated Testing**: Complete separation from production code

---

## 📝 **IMPLEMENTATION STATUS**

- [x] Create `src/core/stress_testing/` directory
- [x] Implement `MessagingCoreProtocol` (interface definition)
- [x] Implement `MockMessagingCore` (mock implementation)
- [x] Implement `RealMessagingCoreAdapter` (real core adapter)
- [x] Add injection point to `MessageQueueProcessor` (already exists)
- [x] Implement `StressTestRunner` (orchestrator)
- [x] Implement `MetricsCollector` (metrics collection)
- [x] Implement `MessageGenerator` (test data generation)
- [x] Create unit tests for stress testing components
- [x] Document usage examples

**Status**: ✅ **ARCHITECTURE DESIGN COMPLETE**  
**Implementation**: ✅ **COMPLETE**  
**Ready For**: Production stress testing

---

## 🔄 **DEPENDENCY INJECTION PATTERN SUMMARY**

### **Key Principles**:

1. **Constructor Injection**: Dependencies injected via constructor
2. **Protocol-Based**: Interface defined by protocol, not concrete class
3. **Default Behavior**: Production code works without injection
4. **Easy Testing**: Mock injection requires no code changes
5. **Type Safety**: Protocol ensures interface compliance

### **Swapping Pattern**:
```python
# Production (real core)
processor = MessageQueueProcessor()

# Testing (mock core)
mock_core = MockMessagingCore(metrics_collector)
processor = MessageQueueProcessor(messaging_core=mock_core)

# Explicit real core (adapter)
real_adapter = RealMessagingCoreAdapter(send_message)
processor = MessageQueueProcessor(messaging_core=real_adapter)
```

---

*Agent-2 (Architecture & Design Specialist)*  
*Design Date: 2025-11-29*  
*Version: 2.0 (Enhanced Dependency Injection)*
