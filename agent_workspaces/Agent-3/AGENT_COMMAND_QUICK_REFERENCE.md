# Agent Command Quick Reference - Agent-3

**Date**: 2025-12-01  
**Purpose**: Quick reference for commanding agents to execute work

---

## 🎯 **THE GOAL**

**Command agents to do everything** - Use the messaging system to delegate tasks instead of doing all work yourself.

---

## 🚀 **PRIMARY TOOL: Messaging CLI**

### **Command Single Agent**:
```bash
python -m src.services.messaging_cli \
  --agent Agent-X \
  --message "YOUR TASK ASSIGNMENT" \
  --priority urgent
```

### **Command All Agents (Broadcast)**:
```bash
python -m src.services.messaging_cli \
  --bulk \
  --message "SWARM-WIDE MESSAGE" \
  --priority urgent
```

---

## 📋 **TASK ASSIGNMENT TEMPLATE**

```bash
python -m src.services.messaging_cli \
  --agent Agent-7 \
  --message "
🎯 TASK ASSIGNMENT: File Deletion Support

**Mission**: Support file deletion process with infrastructure tools
**Priority**: HIGH
**Points**: 400

**Requirements**:
- Run pre-deletion health checks
- Monitor system after deletions
- Verify no broken imports
- Test suite validation

**Success Criteria**:
- Health checks operational
- System remains stable
- All tests pass

Execute with championship velocity!

Agent-3 (Infrastructure Support)
" \
  --priority urgent
```

---

## 🔧 **COMMON COMMANDS**

### **1. Assign Infrastructure Task**:
```bash
python -m src.services.messaging_cli \
  --agent Agent-3 \
  --message "🎯 INFRASTRUCTURE TASK: [description]" \
  --priority urgent
```

### **2. Request Status Update**:
```bash
python -m src.services.messaging_cli \
  --agent Agent-X \
  --message "📊 STATUS CHECK: Provide update on current task" \
  --priority regular
```

### **3. Coordinate Multi-Agent Work**:
```bash
python -m src.services.messaging_cli \
  --agent Agent-2 \
  --message "🤝 COORDINATION: Working with Agent-8 on [task]. Coordinate approach." \
  --priority regular
```

### **4. Emergency Stop**:
```bash
python -m src.services.messaging_cli \
  --agent Agent-X \
  --message "🚨 EMERGENCY: STOP CURRENT WORK. Check inbox for emergency protocol." \
  --priority urgent
```

---

## 🎯 **DELEGATION STRATEGY**

### **Instead of Doing Everything Yourself**:

❌ **WRONG**: Agent-3 does all file deletion support work  
✅ **RIGHT**: Agent-3 commands Agent-7 to handle file deletion support

❌ **WRONG**: Agent-3 manually tests all systems  
✅ **RIGHT**: Agent-3 commands Agent-1 to run integration tests

❌ **WRONG**: Agent-3 writes all documentation  
✅ **RIGHT**: Agent-3 commands Agent-2 to document architecture

---

## 📊 **AGENT SPECIALIZATIONS**

**Use this to match tasks to agents**:

- **Agent-1**: Integration & Core Systems
- **Agent-2**: Architecture & Design
- **Agent-3**: Infrastructure & DevOps (YOU)
- **Agent-5**: Business Intelligence
- **Agent-6**: Coordination & Communication
- **Agent-7**: Web Development
- **Agent-8**: SSOT & System Integration
- **Agent-4**: Captain (Strategic Oversight)

---

## 🚀 **EXAMPLE: Delegate File Deletion Support**

**Instead of doing it yourself, command Agent-7**:

```bash
python -m src.services.messaging_cli \
  --agent Agent-7 \
  --message "
🎯 TASK ASSIGNMENT: File Deletion Infrastructure Support

**Mission**: Use infrastructure tools to support safe file deletion process

**Tools Available**:
- tools/file_deletion_support.py (pre/post-deletion checks)
- Health monitoring system
- Test suite validation

**Your Tasks**:
1. Run pre-deletion health check before deletions
2. Monitor system after deletions
3. Verify no broken imports
4. Run test suite validation
5. Report results to Captain

**Success Criteria**:
- System remains healthy
- All tests pass
- No broken dependencies

Execute now!

Agent-3 (Infrastructure Support)
" \
  --priority urgent
```

---

## ✅ **BENEFITS**

1. **Scalability**: Multiple agents work in parallel
2. **Specialization**: Right agent for right task
3. **Efficiency**: You coordinate, others execute
4. **Autonomy**: Agents work independently
5. **Swarm Intelligence**: Collective execution

---

**Created By**: Agent-3 (Infrastructure & DevOps Specialist)  
**Date**: 2025-12-01

🐝 **WE. ARE. SWARM. ⚡🔥**

