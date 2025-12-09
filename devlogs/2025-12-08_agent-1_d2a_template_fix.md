# D2A Message Template Fix - Agent Operating Cycle + Devlog Commands

**Agent**: Agent-1 (Integration & Core Systems Specialist)  
**Date**: 2025-12-08  
**Type**: Template Enhancement  
**Status**: ✅ **COMPLETE**

---

## 🎯 **OBJECTIVE**

Fix D2A (Discord-to-Agent) message template to include:
1. Agent Operating Cycle explanation
2. Commands for posting Discord devlogs

**Rationale**: Users may only see messages via Discord devlogs when not at computer.

---

## ✅ **CHANGES MADE**

### **Updated D2A Template** (`src/core/messaging_models_core.py`)

**Added Sections**:

1. **Agent Operating Cycle (Mandatory)**:
   - 7-step cycle: Claim → Sync → Slice → Execute → Validate → Commit → Report
   - Clear step-by-step explanation

2. **Discord Devlog Posting (How to Reply)**:
   - Command: `python tools/devlog_manager.py post --agent Agent-X --file <file.md>`
   - Step-by-step instructions
   - Example usage
   - Links to full documentation

**Key Addition**:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AGENT OPERATING CYCLE (MANDATORY)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1) Claim - Check Contract System (--get-next-task)
2) Sync SSOT/context - Review mission, check Swarm Brain
3) Slice - Break work into executable pieces
4) Execute - Do the work
5) Validate - Verify results (tests, checks, evidence)
6) Commit - Git commit with evidence
7) Report evidence - Post Discord devlog (see below)
```

**Devlog Posting Section**:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DISCORD DEVLOG POSTING (HOW TO REPLY)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**This may be the ONLY way users see your messages!**

**Command:**
python tools/devlog_manager.py post --agent {recipient} --file <devlog_file.md>

**Steps:**
1. Create devlog file: devlogs/YYYY-MM-DD_agent-X_topic.md
2. Write your response/update in the file
3. Post to Discord: python tools/devlog_manager.py post --agent {recipient} --file devlogs/YYYY-MM-DD_agent-X_topic.md
4. For major updates: Add --major flag
```

---

## 📊 **IMPACT**

- ✅ **Clear Instructions**: Agents now have explicit cycle steps
- ✅ **Devlog Commands**: Exact commands provided for posting
- ✅ **User Visibility**: Emphasizes devlogs may be only way users see messages
- ✅ **Documentation Links**: Points to full guides for details

---

## 🎯 **NEXT STEPS**

- ✅ Template updated
- ✅ Changes committed
- ⏳ Ready for use in next D2A message

---

**🐝 WE. ARE. SWARM. ⚡🔥**


