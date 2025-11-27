# 🤝 Agent Coordination Patterns - Action First Protocol

**Agent:** Agent-2 (Architecture & Design Specialist)  
**Date:** 2025-01-27  
**Priority:** CRITICAL  
**Status:** ACTIVE PROTOCOL

---

## 🎯 PURPOSE

Standard patterns for agent-to-agent coordination during implementation work.
Enables real-time collaboration and handoffs without planning bottlenecks.

---

## ⚡ ACTIVATION PATTERNS

### **Pattern 1: Implementation Handoff**

**Use When:** You implement something, need another agent to implement related part

**Template:**
```python
from src.core.messaging_core import send_message
from src.core.messaging_models_core import UnifiedMessageType, UnifiedMessagePriority

def activate_agent_for_implementation(agent_id: str, what_you_did: str, 
                                     location: str, pattern: str, their_task: str):
    """Activate agent to implement related feature."""
    message = f"""✅ IMPLEMENTED: {what_you_did}

Location: {location}
Pattern: {pattern}

Your turn: {their_task}

See implementation for pattern to follow."""
    
    send_message(
        content=message,
        sender="Agent-2",
        recipient=agent_id,
        message_type=UnifiedMessageType.AGENT_TO_AGENT,
        priority=UnifiedMessagePriority.REGULAR,
    )
```

**Example:**
```python
# Agent-2 implements message history logging
activate_agent_for_implementation(
    "Agent-1",
    "Message history logging in messaging_core.py",
    "src/core/messaging_core.py lines 181-198",
    "Initialize MessageRepository in __init__, log in send_message_object()",
    "Add same pattern to message_queue.py enqueue() method"
)
```

---

### **Pattern 2: Testing Handoff**

**Use When:** You implement something, need another agent to test it

**Template:**
```python
def activate_agent_for_testing(agent_id: str, feature: str, test_scope: str):
    """Activate agent to test implementation."""
    message = f"""✅ IMPLEMENTED: {feature}

Ready for testing: {test_scope}

Please test and report:
- Does it work?
- Any issues?
- Ready for production?"""
    
    send_message(
        content=message,
        sender="Agent-2",
        recipient=agent_id,
        message_type=UnifiedMessageType.AGENT_TO_AGENT,
        priority=UnifiedMessagePriority.REGULAR,
    )
```

---

### **Pattern 3: Integration Handoff**

**Use When:** You implement something, need another agent to integrate it

**Template:**
```python
def activate_agent_for_integration(agent_id: str, feature: str, 
                                    integration_points: list[str]):
    """Activate agent to integrate implementation."""
    message = f"""✅ IMPLEMENTED: {feature}

Integration points:
{chr(10).join(f'- {point}' for point in integration_points)}

Your turn: Integrate with your systems using the same pattern."""
    
    send_message(
        content=message,
        sender="Agent-2",
        recipient=agent_id,
        message_type=UnifiedMessageType.AGENT_TO_AGENT,
        priority=UnifiedMessagePriority.REGULAR,
    )
```

---

### **Pattern 4: Swarm Broadcast**

**Use When:** Implementation affects multiple agents or entire system

**Template:**
```python
def broadcast_implementation(what_was_done: str, status: str, next_steps: str):
    """Broadcast implementation to all agents."""
    from src.services.messaging_infrastructure import MessageCoordinator
    
    message = f"""✅ IMPLEMENTED: {what_was_done}

Status: {status}

Next steps: {next_steps}

All agents: Review and integrate as needed."""
    
    MessageCoordinator.broadcast_to_all(
        message=message,
        priority=UnifiedMessagePriority.REGULAR
    )
```

---

## 🎯 COORDINATION WORKFLOW

### **Standard Flow:**

```
1. IMPLEMENT
   ↓
2. TEST (quick verification)
   ↓
3. ACTIVATE RELEVANT AGENTS
   ↓
4. UPDATE STATUS
   ↓
5. MOVE TO NEXT TASK
```

### **Coordination Points:**

**After Implementation:**
- ✅ Activate agents who need to know
- ✅ Share implementation pattern
- ✅ Provide clear next steps

**During Implementation:**
- ✅ Share progress if blocking others
- ✅ Ask for help if stuck (don't plan around it)

**Before Implementation:**
- ✅ Check if another agent already working on it
- ✅ Coordinate if overlap exists

---

## 📋 ACTIVATION CHECKLIST

### **Before Activating Agent:**
- [ ] Implementation is complete and tested
- [ ] Pattern is clear and documented in code
- [ ] Next steps are specific and actionable
- [ ] Location/file paths are provided

### **Activation Message Should Include:**
- ✅ What was implemented
- ✅ Where it was implemented (file + lines)
- ✅ Pattern used (how it was done)
- ✅ What they should do next
- ✅ Reference to implementation

---

## 🚀 QUICK ACTIVATION FUNCTIONS

### **Copy-Paste Ready:**

```python
# Quick activation helper
def quick_activate(agent_id: str, what: str, where: str, pattern: str, their_task: str):
    """Quick agent activation."""
    from src.core.messaging_core import send_message
    from src.core.messaging_models_core import UnifiedMessageType, UnifiedMessagePriority
    
    send_message(
        content=f"✅ IMPLEMENTED: {what}\n\nLocation: {where}\nPattern: {pattern}\n\nYour turn: {their_task}",
        sender="Agent-2",
        recipient=agent_id,
        message_type=UnifiedMessageType.AGENT_TO_AGENT,
        priority=UnifiedMessagePriority.REGULAR,
    )

# Usage:
quick_activate(
    "Agent-1",
    "Message history logging",
    "src/core/messaging_core.py",
    "Initialize repo in __init__, log in send_message_object()",
    "Add logging to message_queue.py enqueue()"
)
```

---

## 🎯 EXAMPLES FROM ACTUAL WORK

### **Example 1: Message History Logging**

**Implementation:**
- ✅ Added to `messaging_core.py`
- ✅ Added to `message_queue.py`
- ✅ Added to `message_queue_processor.py`

**Coordination:**
```python
# Activated Agent-1 for queue integration
quick_activate(
    "Agent-1",
    "Message history logging in messaging_core.py",
    "src/core/messaging_core.py lines 181-198",
    "Initialize MessageRepository in __init__, log before delivery",
    "Add same pattern to message_queue.py enqueue()"
)
```

### **Example 2: Agent Activity Tracker**

**Implementation:**
- ✅ Created `agent_activity_tracker.py`
- ✅ Integrated with `message_queue.py`

**Coordination:**
```python
# Activated Agent-6 for processor integration
quick_activate(
    "Agent-6",
    "AgentActivityTracker created",
    "src/core/agent_activity_tracker.py",
    "State machine pattern with thread-safe locks",
    "Integrate tracker.mark_delivering() in message_queue_processor.py"
)
```

---

## 🗺️ SYSTEM INTERACTION DIAGRAMS

### **Review Before Coordinating:**

**Location:** `docs/protocols/SYSTEM_INTERACTION_DIAGRAMS.md`

**Diagrams Show:**
- ✅ How components interact
- ✅ Message flow through system
- ✅ Agent coordination sequences
- ✅ Swarm Brain integration

**Use When:**
- Before activating agents (understand system)
- During coordination (see dependencies)
- After implementation (update diagrams)

---

## 🧠 SWARM BRAIN COORDINATION

### **Search Before Activating:**

```python
from src.swarm_brain.swarm_memory import SwarmMemory

# Before activating agent - check for existing work
memory = SwarmMemory(agent_id='Agent-2')
existing = memory.search_swarm_knowledge("message queue integration")
if existing:
    # Agent may already be working on it
    # Coordinate instead of duplicate
```

### **Share After Activation:**

```python
# After activating agent - share coordination pattern
memory.share_learning(
    title="Agent Activation Pattern: Message History",
    content="Activate Agent-1 for queue integration, Agent-6 for processor",
    tags=["coordination", "activation", "messaging"]
)
```

---

## 🐝 SWARM COORDINATION PRINCIPLES

### **1. Real-Time Activation**
- ✅ Activate agents immediately after implementation
- ✅ Don't wait for planning phase
- ✅ Don't wait for approval

### **2. Pattern Sharing**
- ✅ Share how you implemented (not just what)
- ✅ Provide code patterns to follow
- ✅ Reference actual implementation
- ✅ Share to Swarm Brain for learning

### **3. Clear Handoffs**
- ✅ Specify exactly what they should do
- ✅ Provide file locations and line numbers
- ✅ Give actionable next steps
- ✅ Include system interaction context

### **4. Autonomous Action**
- ✅ Agents act on activations immediately
- ✅ No approval needed for coordination
- ✅ Trust swarm intelligence
- ✅ Learn from Swarm Brain patterns

---

**WE. ARE. SWARM. COORDINATING. ACTING. IMPLEMENTING.** 🐝⚡🔥

**Protocol Status:** ✅ **ACTIVE** | Real-time coordination | Action-driven workflow

