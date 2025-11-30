# Agent Activity Detection Enhancement

**Date**: 2025-11-30  
**Author**: Agent-6 (Coordination & Communication Specialist)  
**Priority**: HIGH

---

## 🎯 **PROBLEM STATEMENT**

The Discord status checker (`StatusChangeMonitor`) only posts when `status.json` changes. It doesn't:
- Detect when agents are inactive
- Send resumer prompts when agents aren't active
- Monitor activity from multiple sources

**Current Limitation**: Only detects `status.json` file modifications, missing other activity indicators.

---

## 💡 **SOLUTION: Multi-Source Activity Detection**

Created `tools/agent_activity_detector.py` to monitor agent activity from **7 different sources**:

### **Activity Sources**

1. **status.json Updates** ✅
   - File modification time
   - `last_updated` timestamp field
   - Status, phase, mission changes

2. **File Modifications** ✅
   - Any file changes in `agent_workspaces/{Agent-X}/`
   - Excludes `status.json` (checked separately)
   - Tracks file paths and sizes

3. **Devlog Creation** ✅
   - New devlogs in `devlogs/` directory
   - Pattern: `*{agent_id}*.md`
   - Tracks devlog filenames

4. **Inbox Activity** ✅
   - Messages sent/received in `agent_workspaces/{Agent-X}/inbox/`
   - Detects message creation/modification
   - Distinguishes sent vs received messages

5. **Task Claims** ✅
   - Cycle planner task claims
   - Pattern: `*_{agent_id}_*.json`
   - Tracks claimed contracts

6. **Git Commits** ✅
   - Git commits in agent workspace (if git repo)
   - Uses `git log --since` to find recent commits
   - Tracks commit messages and timestamps

7. **Message Queue Activity** ✅
   - Messages queued for agent in `data/message_queue.json`
   - Tracks message types and timestamps
   - Detects queued messages for agent

---

## 🔧 **INTEGRATION WITH RESUMER PROMPTS**

### **Current Flow**
1. `StatusChangeMonitor` detects `status.json` changes
2. Posts to Discord when status changes
3. **Missing**: No detection of inactivity or resumer prompts

### **Enhanced Flow**
1. `AgentActivityDetector` monitors all 7 sources
2. Detects inactivity (no activity for X minutes)
3. Triggers `OptimizedStallResumePrompt` for inactive agents
4. Posts resumer prompt to Discord

---

## 📊 **USAGE**

### **Check Single Agent**
```bash
python tools/agent_activity_detector.py --agent Agent-6 --report
```

### **Find Inactive Agents**
```bash
python tools/agent_activity_detector.py --inactive --threshold 30
```

### **Activity Summary**
```bash
python tools/agent_activity_detector.py --lookback 60
```

---

## 🔗 **INTEGRATION POINTS**

### **1. StatusChangeMonitor Enhancement**
- Add `AgentActivityDetector` integration
- Check for inactivity in monitoring loop
- Trigger resumer prompts when inactive

### **2. Discord Bot Integration**
- Add activity monitoring to Discord bot
- Post inactivity alerts
- Send resumer prompts automatically

### **3. Captain Tools**
- Add to `captain_find_idle_agents.py`
- Use activity detector for more accurate idle detection
- Generate resumer prompts automatically

---

## 🎯 **NEXT STEPS**

1. **Integrate with StatusChangeMonitor**
   - Add inactivity detection to monitoring loop
   - Trigger resumer prompts automatically

2. **Discord Bot Integration**
   - Add activity monitoring task
   - Post inactivity alerts to Discord
   - Send resumer prompts via Discord

3. **Captain Tools Enhancement**
   - Update `captain_find_idle_agents.py` to use activity detector
   - Generate resumer prompts for inactive agents

4. **Testing**
   - Test with all 7 activity sources
   - Verify inactivity detection accuracy
   - Test resumer prompt generation

---

## 📈 **BENEFITS**

- **More Accurate Detection**: 7 sources vs 1 source
- **Proactive Resumer Prompts**: Automatic detection and prompting
- **Better Activity Tracking**: Comprehensive activity monitoring
- **Reduced False Positives**: Multiple sources confirm activity
- **Improved Swarm Coordination**: Better visibility into agent activity

---

**🐝 WE. ARE. SWARM. ⚡🔥**

*Agent-6 - Coordination & Communication Specialist*

