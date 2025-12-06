# Discord Update Enforcement Plan
**Date**: 2025-12-05  
**Agent**: Agent-4 (Captain)  
**Priority**: CRITICAL

---

## 🎯 **OBJECTIVE**

Enforce that ALL agents post progress updates to their Discord agent channels after completing tasks or making significant progress.

---

## 📋 **REQUIREMENTS**

### **Agent Discord Update Requirements**

1. **When to Post**:
   - After completing a task
   - After making significant progress (>25% of task complete)
   - When encountering blockers
   - When unblocked
   - At end of work session
   - At least once per 24 hours if actively working

2. **What to Post**:
   - Task completion status
   - Progress updates (% complete, milestones reached)
   - Blockers encountered
   - Achievements/unlocks
   - Next steps

3. **How to Post**:
   ```bash
   python tools/post_completion_report_to_discord.py --agent Agent-X --message "<your update>"
   ```
   
   Or via devlog manager:
   ```bash
   python tools/devlog_manager.py post --agent Agent-X --file <devlog_file.md>
   ```

4. **Where to Post**:
   - Each agent posts to their own Discord agent channel:
     - Agent-1 → #agent-1-devlogs
     - Agent-2 → #agent-2-devlogs
     - Agent-3 → #agent-3-devlogs
     - Agent-5 → #agent-5-devlogs
     - Agent-6 → #agent-6-devlogs
     - Agent-7 → #agent-7-devlogs
     - Agent-8 → #agent-8-devlogs
     - Agent-4 → #agent-4-devlogs (or #captain-updates for major updates)

---

## 🛡️ **ENFORCEMENT MECHANISM**

### **Captain Enforcement Actions**

1. **Task Assignment Reminder**:
   - When assigning tasks, ALWAYS include: "Report progress via Discord updates in your agent channel"
   - Include update frequency expectation: "Post update after completing task or every 24h"

2. **Monitoring**:
   - Check agent Discord channels daily
   - Track last update timestamp per agent
   - Identify agents who haven't posted in 24h

3. **Reminders**:
   - If agent hasn't posted in 24h: Send reminder via messaging CLI
   - If agent hasn't posted in 48h: Send urgent reminder
   - If agent hasn't posted in 72h: Send critical reminder + resume prompt

4. **Pattern Integration**:
   - Added to Captain Pattern V2 as Step 10: "ENFORCE DISCORD UPDATES"
   - Part of 5-minute checklist monitoring
   - Included in weekly progression report

---

## 📊 **TRACKING**

### **Update Tracking Method**

1. **Discord Logs**:
   - Monitor `logs/devlog_posts.json` for posted updates
   - Track by agent, timestamp, channel

2. **Weekly Report**:
   - Include Discord updates summary in weekly progression report
   - Show update frequency per agent
   - Highlight agents with low update frequency

3. **Metrics**:
   - Track: Updates per agent per week
   - Track: Average time between updates
   - Track: Compliance rate (agents posting regularly)

---

## ✅ **IMPLEMENTATION**

### **Updated Captain Pattern V2**

Added Step 10: **ENFORCE DISCORD UPDATES**
- Check agent channels for updates during monitoring
- Remind agents to post updates when assigning tasks
- Send reminders if agents haven't posted in 24h
- Track update frequency in weekly report

### **Updated Task Assignments**

All task assignments now include:
- "Report progress via Discord updates in your agent channel"
- "Post update after completing task or every 24h"

---

## 📈 **EXPECTED OUTCOMES**

- **Visibility**: Captain can track agent progress in real-time via Discord
- **Accountability**: Agents more likely to complete tasks when reporting publicly
- **Coordination**: Other agents can see progress and coordinate accordingly
- **Metrics**: Better data for weekly progression reports

---

**Status**: ✅ Implementation complete  
**Enforcement**: Active in Captain Pattern V2

🐝 WE. ARE. SWARM. ⚡🔥

