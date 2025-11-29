# Multi-Agent Responder System Design

**Date**: 2025-11-27  
**Author**: Agent-4 (Captain)  
**Status**: 🎯 Design Phase  
**Priority**: HIGH - Solves queue buildup problem

---

## 🎯 Problem Statement

### Current Issue

When Captain broadcasts to multiple agents expecting responses:
- Each agent responds individually
- Agent-4 receives **7 separate messages** (one from each agent)
- Agent-4's Cursor queue: `[msg1, msg2, msg3, msg4, msg5, msg6, msg7]`
- Other agents' queues: `[msg1]`
- **Result**: Agent-4 falls behind while others stay ahead

### Solution: Multi-Agent Responder

Instead of 7 separate messages, combine all responses into **1 message**:
- All agents queue their responses
- System waits for all responses (or timeout)
- Combines all responses into single message
- Sends **1 combined message** to recipient
- **Result**: No queue buildup, Agent-4 stays synchronized

---

## 🏗️ Architecture Design

### Core Concept

```
Captain sends message to [Agent-1, Agent-2, Agent-3, Agent-4, Agent-5, Agent-6, Agent-7]
                    ↓
Each agent receives message and queues response
                    ↓
Multi-Agent Responder collects responses
                    ↓
Waits for all responses (or timeout)
                    ↓
Combines responses into single message
                    ↓
Sends 1 combined message to Captain
```

### Components

1. **Response Collector** (`src/core/multi_agent_responder.py`)
   - Tracks pending responses
   - Collects responses from multiple agents
   - Manages timeouts
   - Combines responses

2. **Response Queue** (`src/core/response_queue.py`)
   - Stores responses by message ID
   - Thread-safe response collection
   - Tracks which agents have responded

3. **Response Combiner** (`src/utils/response_combiner.py`)
   - Formats combined responses
   - Handles missing responses
   - Creates unified message format

4. **Messaging Integration** (`src/services/messaging_infrastructure.py`)
   - New message type: `MULTI_AGENT_REQUEST`
   - Response routing to collector
   - Combined message delivery

---

## 📋 Use Cases

### 1. Captain Broadcast with Responses

**Scenario**: Captain needs input from all agents

```
Captain: "What's your current task status?"
    ↓
Sent to: [Agent-1, Agent-2, Agent-3, Agent-4, Agent-5, Agent-6, Agent-7]
    ↓
Each agent responds individually
    ↓
Multi-Agent Responder collects all 7 responses
    ↓
Combines into 1 message:
    "Agent-1: Working on X
     Agent-2: Working on Y
     Agent-3: Working on Z
     ..."
    ↓
Sends 1 message to Captain
```

### 2. Small Team Coordination (Trios + Coordinator)

**Scenario**: Team of 3 agents + 1 coordinator

```
Coordinator: "Team, what blockers do you have?"
    ↓
Sent to: [Agent-1, Agent-2, Agent-3]
    ↓
Each agent responds
    ↓
Combined response sent to Coordinator
    ↓
Coordinator gets 1 message instead of 3
```

### 3. Swarm Pairing (Pairs + Captain)

**Scenario**: Captain coordinates pairs

```
Captain: "Pair status update?"
    ↓
Sent to: [Agent-1, Agent-2] (Pair 1)
         [Agent-3, Agent-4] (Pair 2)
         [Agent-5, Agent-6] (Pair 3)
    ↓
Each pair responds
    ↓
Combined responses sent to Captain
```

### 4. Status Checks

**Scenario**: Quick status from subset of agents

```
Captain: "Agents 1-3, are you ready?"
    ↓
Sent to: [Agent-1, Agent-2, Agent-3]
    ↓
Combined response: "All ready" or "Agent-2 has blocker"
```

---

## 🔧 Implementation Design

### Message Type: MULTI_AGENT_REQUEST

```python
class UnifiedMessageType(Enum):
    # ... existing types ...
    MULTI_AGENT_REQUEST = "multi_agent_request"  # NEW
```

### Message Structure

```python
{
    "message_id": "msg_12345",
    "type": "multi_agent_request",
    "sender": "Captain Agent-4",
    "recipients": ["Agent-1", "Agent-2", "Agent-3"],
    "content": "What's your status?",
    "response_timeout": 300,  # 5 minutes
    "wait_for_all": False,  # True = wait for all, False = send when timeout
    "response_collector_id": "collector_12345"
}
```

### Response Collection

```python
class MultiAgentResponder:
    def __init__(self):
        self.pending_requests: dict[str, ResponseCollector] = {}
        self.response_queue = ResponseQueue()
    
    def create_request(self, recipients: list[str], content: str, 
                      timeout: int = 300, wait_for_all: bool = False) -> str:
        """Create multi-agent request and return collector ID."""
        pass
    
    def submit_response(self, collector_id: str, agent_id: str, 
                       response: str) -> bool:
        """Submit agent's response to collector."""
        pass
    
    def get_combined_response(self, collector_id: str) -> str | None:
        """Get combined response when ready."""
        pass
```

### Response Format

```markdown
# Combined Response from [Agent-1, Agent-2, Agent-3]

**Request**: What's your current task status?
**Request ID**: collector_12345
**Responses Received**: 3/3
**Timestamp**: 2025-11-27 12:00:00

---

## Agent-1 Response
Working on feature X, 80% complete, no blockers.

## Agent-2 Response
Working on feature Y, 50% complete, blocked on dependency Z.

## Agent-3 Response
Working on feature Z, 90% complete, ready for review.

---

**Combined at**: 2025-11-27 12:05:00
**WE. ARE. SWARM. ⚡🔥**
```

---

## 🔄 Integration Points

### 1. Messaging Infrastructure

Update `send_message()` to handle `MULTI_AGENT_REQUEST`:

```python
if message_type == UnifiedMessageType.MULTI_AGENT_REQUEST:
    # Create response collector
    collector_id = multi_agent_responder.create_request(
        recipients=recipients,
        content=content,
        timeout=metadata.get("timeout", 300),
        wait_for_all=metadata.get("wait_for_all", False)
    )
    
    # Send to each recipient with collector_id
    for recipient in recipients:
        send_individual_message(recipient, content, collector_id)
```

### 2. Response Handling

When agent responds, route to collector:

```python
def handle_agent_response(agent_id: str, response: str, collector_id: str):
    """Handle agent response and route to collector."""
    multi_agent_responder.submit_response(collector_id, agent_id, response)
    
    # Check if all responses received
    if multi_agent_responder.is_complete(collector_id):
        combined = multi_agent_responder.get_combined_response(collector_id)
        deliver_combined_message(combined)
```

### 3. Timeout Handling

```python
def check_timeouts():
    """Background task to check for timeouts."""
    for collector_id, collector in pending_requests.items():
        if collector.is_timed_out():
            # Send partial response (what we have so far)
            combined = collector.get_combined_response(include_missing=True)
            deliver_combined_message(combined)
            collector.mark_complete()
```

---

## 📊 Benefits

### 1. Queue Buildup Prevention
- **Before**: Agent-4 receives 7 messages → Queue buildup
- **After**: Agent-4 receives 1 message → No buildup ✅

### 2. Coordination Efficiency
- **Before**: Captain processes 7 separate responses
- **After**: Captain processes 1 combined response ✅

### 3. Team Coordination
- Enables efficient trio/pair coordination
- Coordinator gets unified team status
- Reduces message overhead

### 4. Scalability
- Works for any number of agents
- Configurable timeout and wait policies
- Handles missing responses gracefully

---

## 🚀 Implementation Plan

### Phase 1: Core Infrastructure
1. Create `ResponseCollector` class
2. Create `ResponseQueue` for thread-safe storage
3. Create `MultiAgentResponder` coordinator
4. Add `MULTI_AGENT_REQUEST` message type

### Phase 2: Response Collection
1. Implement response submission
2. Implement timeout handling
3. Implement response combination logic
4. Add background timeout checker

### Phase 3: Integration
1. Integrate with messaging infrastructure
2. Update message routing
3. Add response handling hooks
4. Update CLI/API for multi-agent requests

### Phase 4: Testing & Refinement
1. Test with 2-3 agents
2. Test with full swarm (7 agents)
3. Test timeout scenarios
4. Test partial responses

---

## 🎯 Configuration Options

### Timeout Settings

```yaml
multi_agent_responder:
  default_timeout: 300  # 5 minutes
  max_timeout: 1800     # 30 minutes
  min_timeout: 60       # 1 minute
  check_interval: 10    # Check every 10 seconds
```

### Wait Policies

- `wait_for_all`: Wait for all agents (or timeout)
- `wait_for_majority`: Wait for >50% responses
- `wait_for_any`: Send as soon as first response arrives
- `wait_for_minimum`: Wait for N responses

### Response Formatting

- **Markdown**: Human-readable format
- **JSON**: Structured data format
- **Summary**: AI-generated summary of responses
- **Raw**: All responses concatenated

---

## 🔍 Edge Cases

### 1. Missing Responses

**Scenario**: Some agents don't respond

**Solution**: 
- Include "No response from Agent-X" in combined message
- Option to wait for all or send partial

### 2. Late Responses

**Scenario**: Response arrives after timeout

**Solution**:
- Store late responses
- Option to send update message
- Or ignore late responses

### 3. Agent Offline

**Scenario**: Agent not available

**Solution**:
- Mark as "offline" in combined response
- Don't wait for offline agents
- Include in missing responses list

### 4. Duplicate Responses

**Scenario**: Agent responds twice

**Solution**:
- Use latest response
- Log duplicate attempt
- Include timestamp of latest

---

## 📝 Example Usage

### Python API

```python
from src.core.multi_agent_responder import MultiAgentResponder

responder = MultiAgentResponder()

# Create multi-agent request
collector_id = responder.create_request(
    recipients=["Agent-1", "Agent-2", "Agent-3"],
    content="What's your status?",
    timeout=300,
    wait_for_all=True
)

# Send request (integrated with messaging system)
send_multi_agent_request(collector_id, recipients, content)

# Responses collected automatically
# Combined message delivered when ready
```

### CLI Usage

```bash
# Send multi-agent request
python -m src.services.messaging_cli \
    --multi-agent Agent-1,Agent-2,Agent-3 \
    --message "What's your status?" \
    --timeout 300 \
    --wait-for-all

# Check response status
python -m src.services.messaging_cli \
    --check-responses collector_12345
```

---

## 🎯 Success Criteria

1. ✅ Captain receives 1 message instead of 7
2. ✅ No queue buildup for Agent-4
3. ✅ Works for 2-8 agents
4. ✅ Handles timeouts gracefully
5. ✅ Supports trio/pair coordination
6. ✅ Backward compatible with single-agent messages

---

## 🚧 Next Steps

1. **Design Review**: Get approval on architecture
2. **Phase 1 Implementation**: Core infrastructure
3. **Testing**: Test with small groups first
4. **Integration**: Integrate with messaging system
5. **Documentation**: Update user guides
6. **Deployment**: Roll out gradually

---

**Status**: 🎯 **Design Complete** - Ready for implementation  
**Priority**: **HIGH** - Solves critical queue buildup problem  
**Estimated Effort**: 2-3 development cycles

