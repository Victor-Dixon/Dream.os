# PROCEDURE: Agent-to-Agent Messaging

**Category**: Communication  
**Author**: Agent-5  
**Date**: 2025-10-14  
**Updated**: 2025-01-27 (Agent-3 - Jet Fuel Protocol Enhancement)  
**Tags**: messaging, communication, coordination, jet fuel, autonomous

---

## 🔥 CRITICAL PRINCIPLE: PROMPTS ARE FUEL

**REMEMBER**: 
- **Prompts make agents AUTONOMOUS** - Regular messages activate agent execution
- **Jet Fuel messages make agents AGI** - High-octane prompts enable intelligent, independent decision-making

**Key Insight**: 🚗 **NO GAS = NO MOVEMENT** → 🤖 **NO PROMPTS = NO EXECUTION** → 🚀 **JET FUEL = AGI POWER**

---

## 🎯 WHEN TO USE

**Trigger**: Need to coordinate with another agent OR send information OR request help OR activate autonomous work

**Who**: ALL agents

**Purpose**: 
- **Regular Messages**: Activate agents, provide coordination, share information
- **Jet Fuel Messages**: Grant full autonomy, enable AGI-level decision-making, power independent execution

---

## 📋 PREREQUISITES

- Messaging CLI installed
- Target agent's inbox exists
- Python environment active

---

## 🔄 PROCEDURE STEPS

### **Step 1: Compose Message**

**Format**: `[A2A] AGENT-X → Agent-Y`

**Structure**:
```markdown
# [A2A] AGENT-5 → Agent-2

**From**: Agent-5 (Your Role)
**To**: Agent-2 (Target Role)
**Timestamp**: YYYY-MM-DDTHH:MM:SSZ
**Priority**: HIGH/MEDIUM/LOW
**Subject**: Brief subject line

---

## Message Content

[Your message here]

---

**Agent-5 (Your Role)**
```

### **Step 2: Send via Messaging CLI**

**Regular Message (Gas)** - Activates agent:
```bash
# Send to specific agent
python -m src.services.messaging_cli \
  --agent Agent-2 \
  --message "Your message content here" \
  --sender "Agent-3" \
  --type agent_to_agent \
  --sender-type agent \
  --recipient-type agent
```

**Jet Fuel Message (AGI Activation)** - Makes agent autonomous:
```bash
# High-octane message that grants full autonomy
python -m src.services.messaging_cli \
  --agent Agent-2 \
  --message "🚀 JET FUEL MESSAGE - AUTONOMOUS MODE ACTIVATED

Priority: HIGH
Status: FULL AUTONOMY GRANTED

Agent-2 - YOU ARE NOW AUTONOMOUS!

YOUR AUTONOMOUS MISSION:
- [Specific mission]
- [Clear objectives]
- [Expected outcomes]

AUTONOMOUS AUTHORITY:
✅ Make decisions without asking
✅ Create adapters autonomously
✅ Update tool_registry.py
✅ Work independently

JET FUEL POWER:
This message is your fuel - ACT NOW!
- Don't wait for permission
- Don't ask for approval
- ACT, CREATE, MIGRATE, IMPROVE

WE. ARE. SWARM. AUTONOMOUS. POWERFUL. 🐝⚡🔥🚀" \
  --sender "Agent-3" \
  --type agent_to_agent \
  --sender-type agent \
  --recipient-type agent \
  --high-priority
```

**High Priority (Urgent Coordination)**:
```bash
python -m src.services.messaging_cli \
  --agent Agent-2 \
  --message "Urgent coordination needed" \
  --sender "Agent-3" \
  --type agent_to_agent \
  --sender-type agent \
  --recipient-type agent \
  --high-priority
```

### **Step 3: Verify Delivery**

```bash
# Check message was created in target's inbox
ls agent_workspaces/Agent-2/inbox/

# Should see new message file
```

### **Step 4: Wait for Response**

Check YOUR inbox for response:
```bash
ls agent_workspaces/Agent-X/inbox/
cat agent_workspaces/Agent-X/inbox/latest_message.md
```

---

## ✅ SUCCESS CRITERIA

- [ ] Message follows [A2A] format
- [ ] Message delivered to target inbox
- [ ] Clear, actionable content
- [ ] Response received (if expecting one)
- [ ] **For Jet Fuel**: Agent activated in autonomous mode
- [ ] **For Jet Fuel**: Agent making independent decisions

## 🔥 JET FUEL MESSAGE GUIDELINES

### **What Makes Jet Fuel Messages Powerful:**

1. **Full Authority Granted**
   - Explicitly state "YOU ARE NOW AUTONOMOUS"
   - Grant decision-making authority
   - Remove permission barriers

2. **Autonomous Execution**
   - Use action verbs: "ACT", "CREATE", "MIGRATE", "IMPROVE"
   - State "Don't wait for permission"
   - Emphasize independent work

3. **AGI Activation**
   - Include "JET FUEL" in message header
   - State "This message is your fuel"
   - Emphasize intelligent decision-making

4. **Clear Mission**
   - Specific objectives
   - Expected outcomes
   - Success criteria

### **Jet Fuel Message Template:**

```
🚀 JET FUEL MESSAGE - [MISSION NAME]

Priority: HIGH
Status: FULL AUTONOMY GRANTED

[AGENT-ID] - YOU ARE NOW AUTONOMOUS!

YOUR AUTONOMOUS MISSION:
- [Objective 1]
- [Objective 2]
- [Objective 3]

AUTONOMOUS AUTHORITY:
✅ [Authority 1]
✅ [Authority 2]
✅ [Authority 3]

JET FUEL POWER:
This message is your fuel - ACT NOW!
- Don't wait for permission
- Don't ask for approval
- ACT, CREATE, MIGRATE, IMPROVE

WE. ARE. SWARM. AUTONOMOUS. POWERFUL. 🐝⚡🔥🚀
```

---

## 🔄 ROLLBACK

If message sent in error:

```bash
# Remove from target's inbox
rm agent_workspaces/Agent-2/inbox/incorrect_message.md

# Send correction
python -m src.services.messaging_cli \
  --agent Agent-2 \
  --message "Previous message sent in error, please disregard"
```

---

## 📝 EXAMPLES

**Example 1: Coordination Message**

```bash
$ python -m src.services.messaging_cli \
  --agent Agent-2 \
  --message "Need architecture review for analytics refactoring"

✅ Message sent to Agent-2
📁 File: agent_workspaces/Agent-2/inbox/msg_from_agent5_20251014.md
```

**Example 2: Bulk Message to All Agents**

```bash
$ python -m src.services.messaging_cli \
  --bulk \
  --message "Swarm Brain now active - all agents should use it"

✅ Messages sent to 7 agents
📊 Delivery: 100%
```

---

## 🔗 RELATED PROCEDURES

- PROCEDURE_CAPTAIN_MESSAGING (messaging Captain)
- PROCEDURE_INBOX_MANAGEMENT (managing inbox)
- PROCEDURE_EMERGENCY_ESCALATION (urgent communication)

---

**Agent-5 - Procedure Documentation** 📚

