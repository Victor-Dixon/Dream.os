# 🎯 Agent Command System - Complete Guide

**Purpose**: Command agents to do everything using the available tools  
**Status**: ✅ OPERATIONAL  
**Last Updated**: 2025-12-01

---

## 🚀 **PRIMARY COMMAND METHODS**

### **1. Contract System (Task Assignment)**

**The main way to assign tasks to agents:**

```bash
# Assign next available task to an agent
python -m src.services.messaging_cli --agent Agent-7 --get-next-task

# Check contract status
python -m src.services.messaging_cli --check-status
```

**What it does**:
- Claims next available task from contract queue
- Assigns to specified agent
- Shows task details (title, description, priority, points)
- Marks task as claimed

**Best for**: Structured task assignments from predefined queue

---

### **2. Mission Control (Autonomous Mission Generation)**

**The comprehensive tool that generates optimal missions:**

```bash
# Generate optimal mission for an agent
python tools/mission_control.py --agent Agent-7 --save

# For specific specialization
python tools/mission_control.py --agent Agent-2 --specialization "Architecture & Design"
```

**What it does**:
1. ✅ Checks task queue (--get-next-task)
2. ✅ Runs project scanner analysis
3. ✅ Consults swarm brain patterns
4. ✅ Checks all agent statuses (prevents overlap)
5. ✅ Generates optimal mission for THIS agent

**Output**: Complete mission brief with:
- Mission type (ASSIGNED_TASK, V2_REFACTORING, STRATEGIC_REST)
- Target file/objective
- Priority and rationale
- Pattern suggestions
- Coordination needs

**Best for**: Autonomous agents finding their own optimal work

---

### **3. Agent Mission Controller (Refactoring Missions)**

**For V2 compliance and refactoring work:**

```bash
# Scan for available missions
python tools/agent_mission_controller.py --scan

# Get personalized recommendation
python tools/agent_mission_controller.py --recommend Agent-2

# Get execution plan for specific file
python tools/agent_mission_controller.py --plan src/core/some_file.py

# Check agent status
python tools/agent_mission_controller.py --status Agent-2
```

**What it does**:
- Scans codebase for V2 violations
- Matches missions to agent specialty
- Provides execution plans with proven patterns
- Calculates ROI and success probability

**Best for**: V2 compliance refactoring work

---

### **4. Direct Messaging (Commands & Instructions)**

**Send direct commands to agents:**

```bash
# Send message to specific agent
python -m src.services.messaging_cli --agent Agent-7 -m "Your command here" --priority urgent

# Broadcast to all agents
python -m src.services.messaging_cli --bulk -m "System-wide announcement" --priority normal

# Send onboarding message
python -m src.services.messaging_cli --agent Agent-3 --onboard
```

**Best for**: Direct commands, instructions, coordination

---

## 🎯 **COMMON COMMAND PATTERNS**

### **Pattern 1: Assign Task from Queue**

```bash
# Agent claims next task
python -m src.services.messaging_cli --agent Agent-7 --get-next-task
```

### **Pattern 2: Generate Autonomous Mission**

```bash
# Agent finds optimal work
python tools/mission_control.py --agent Agent-7 --save
```

### **Pattern 3: Direct Command with Task**

```bash
# Send command with specific task
python -m src.services.messaging_cli --agent Agent-7 -m "Fix website issues on prismblossom.online - HIGH priority" --priority urgent
```

### **Pattern 4: Refactoring Assignment**

```bash
# Get refactoring recommendation
python tools/agent_mission_controller.py --recommend Agent-2

# Then send the recommendation
python -m src.services.messaging_cli --agent Agent-2 -m "Execute recommended mission from agent_mission_controller" --priority normal
```

---

## 🔧 **ADVANCED USAGE**

### **Batch Assignment to Multiple Agents**

```bash
# Assign tasks to all agents sequentially
for agent in Agent-1 Agent-2 Agent-3 Agent-5 Agent-6 Agent-7 Agent-8; do
    python -m src.services.messaging_cli --agent $agent --get-next-task
done
```

### **Mission Generation for All Agents**

```bash
# Generate missions for all agents
for agent in Agent-1 Agent-2 Agent-3 Agent-5 Agent-6 Agent-7 Agent-8; do
    python tools/mission_control.py --agent $agent --save
done
```

### **Combined Approach (Recommended)**

```bash
# 1. Check what's available
python tools/agent_mission_controller.py --scan

# 2. Generate mission for specific agent
python tools/mission_control.py --agent Agent-7 --save

# 3. Send mission as command
python -m src.services.messaging_cli --agent Agent-7 -m "Execute mission from mission_control output" --priority normal
```

---

## 📊 **TOOL COMPARISON**

| Tool | Purpose | Best For | Output |
|------|---------|----------|--------|
| `--get-next-task` | Task assignment | Structured tasks from queue | Task details |
| `mission_control.py` | Mission generation | Autonomous work discovery | Complete mission brief |
| `agent_mission_controller.py` | Refactoring missions | V2 compliance work | Refactoring recommendations |
| Direct messaging | Commands | Direct instructions | Message delivered |

---

## 🎯 **RECOMMENDED WORKFLOW**

### **For Captain (Agent-4):**

1. **Check available tasks**:
   ```bash
   python -m src.services.messaging_cli --check-status
   ```

2. **Assign tasks to agents**:
   ```bash
   python -m src.services.messaging_cli --agent Agent-7 --get-next-task
   ```

3. **Or generate autonomous missions**:
   ```bash
   python tools/mission_control.py --agent Agent-7 --save
   ```

4. **Send direct commands when needed**:
   ```bash
   python -m src.services.messaging_cli --agent Agent-7 -m "Your command" --priority urgent
   ```

### **For Agents (Autonomous Mode):**

1. **Find optimal work**:
   ```bash
   python tools/mission_control.py --agent Agent-7 --save
   ```

2. **Or get refactoring recommendation**:
   ```bash
   python tools/agent_mission_controller.py --recommend Agent-7
   ```

3. **Or claim next task**:
   ```bash
   python -m src.services.messaging_cli --agent Agent-7 --get-next-task
   ```

---

## 🚨 **QUICK REFERENCE**

```bash
# Assign task
python -m src.services.messaging_cli --agent <AGENT> --get-next-task

# Generate mission
python tools/mission_control.py --agent <AGENT> --save

# Get refactoring recommendation
python tools/agent_mission_controller.py --recommend <AGENT>

# Send direct command
python -m src.services.messaging_cli --agent <AGENT> -m "<COMMAND>" --priority <normal|urgent>

# Broadcast to all
python -m src.services.messaging_cli --bulk -m "<MESSAGE>" --priority <normal|urgent>
```

---

## 💡 **KEY INSIGHTS**

1. **Contract System** (`--get-next-task`) is the PRIMARY way to assign structured tasks
2. **Mission Control** is the BEST tool for autonomous agents finding optimal work
3. **Agent Mission Controller** is SPECIALIZED for V2 refactoring work
4. **Direct Messaging** is for SPECIFIC commands and coordination

**Use the right tool for the right job!**

---

🐝 **WE. ARE. SWARM. ⚡🔥**

