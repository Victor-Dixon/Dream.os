# 📋 Protocols Directory

**Purpose:** Standard workflows and patterns for agent coordination

---

## 🚀 ACTIVE PROTOCOLS

### **⚡ ACTION FIRST PROTOCOL** (CRITICAL)
**File:** `ACTION_FIRST_PROTOCOL.md`  
**Status:** ✅ ACTIVE  
**Purpose:** Implementation-first workflow (not planning-first)

**Key Principle:** "Action First, Plan Second, Document Third"

**Use When:** Starting any new work or fixing issues

**Includes:**
- ✅ Mermaid diagrams for system understanding
- ✅ Swarm Brain integration patterns
- ✅ Agent activation templates

---

### **🤝 AGENT COORDINATION PATTERNS** (CRITICAL)
**File:** `AGENT_COORDINATION_PATTERNS.md`  
**Status:** ✅ ACTIVE  
**Purpose:** Standard patterns for agent-to-agent coordination

**Key Features:**
- Implementation handoffs
- Testing handoffs
- Integration handoffs
- Swarm broadcasts
- Swarm Brain integration

**Use When:** You implement something and need to activate other agents

---

### **🗺️ SYSTEM INTERACTION DIAGRAMS** (CRITICAL)
**File:** `SYSTEM_INTERACTION_DIAGRAMS.md`  
**Status:** ✅ ACTIVE  
**Purpose:** Mermaid diagrams showing system architecture and interactions

**Diagrams Include:**
- ✅ Message system architecture flow
- ✅ Agent coordination sequences
- ✅ Swarm Brain integration patterns
- ✅ Component dependencies
- ✅ Action First workflow

**Use When:** Need to understand how components interact before implementing

---

## 📚 PROTOCOL USAGE

### **Before Starting Work:**
1. Read `ACTION_FIRST_PROTOCOL.md`
2. Review `SYSTEM_INTERACTION_DIAGRAMS.md` (relevant diagrams)
3. Search Swarm Brain for existing patterns
4. Follow: Implement → Test → Coordinate → Document

### **When Implementing:**
1. Write code immediately (don't plan first)
2. Test as you go
3. Activate relevant agents using `AGENT_COORDINATION_PATTERNS.md`
4. Share pattern to Swarm Brain
5. Document what was done (not what will be done)

### **When Completing Work:**
1. Handoff to next agent using coordination patterns
2. Share implementation pattern to Swarm Brain
3. Update system diagrams if architecture changes
4. Update status.json
5. Move to next task

---

## 🧠 SWARM BRAIN INTEGRATION

### **Access Pattern:**

```python
from src.swarm_brain.swarm_memory import SwarmMemory

# Before implementing - search for patterns
memory = SwarmMemory(agent_id='Agent-2')
patterns = memory.search_swarm_knowledge("your topic")
# Use existing patterns instead of reinventing

# After implementing - share learning
memory.share_learning(
    title="Your Implementation Pattern",
    content="How you implemented it",
    tags=["category", "pattern", "implementation"]
)
```

---

## 🎯 QUICK REFERENCE

**Action First Workflow:**
```
See Issue → Review Diagrams → Search Swarm Brain → Fix It → Test It → Activate Agents → Share to Swarm Brain → Document It
```

**Coordination Template:**
```
✅ IMPLEMENTED: {what}
Location: {where}
Pattern: {how}
Your turn: {next_step}
See: SYSTEM_INTERACTION_DIAGRAMS.md for context
```

**Swarm Brain Integration:**
```
Before: search_swarm_knowledge() - Find existing patterns
After: share_learning() - Help others learn
```

---

## 🗺️ DIAGRAM QUICK ACCESS

### **Message System:**
- Complete flow: Message System Architecture
- Components: Component Interaction
- Dependencies: Component Dependencies

### **Coordination:**
- Workflow: Action First Workflow Diagram
- Activation: Agent Activation Flow
- Sequence: Agent Coordination Flow

### **Swarm Brain:**
- Learning: Swarm Brain Integration
- Access: Swarm Brain Access Pattern

---

**WE. ARE. SWARM. ACTING. IMPLEMENTING. COORDINATING. LEARNING.** 🐝⚡🔥
