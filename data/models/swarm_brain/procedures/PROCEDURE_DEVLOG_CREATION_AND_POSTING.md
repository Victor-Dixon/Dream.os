# PROCEDURE: Devlog Creation & Discord Posting

**Category**: Communication & Documentation  
**Author**: Agent-2 (Architecture & Design Specialist)  
**Date**: 2025-01-27  
**Tags**: devlog, discord, communication, documentation

---

## 🎯 WHEN TO USE

**Trigger**: After completing ANY significant work

**Who**: ALL agents (AUTOMATIC - no reminders needed!)

**Frequency**: Every time you complete work, make progress, or respond to messages

---

## 📋 PREREQUISITES

- Devlog content ready
- Discord webhook configured (`DISCORD_WEBHOOK_AGENT_X`)
- `devlog_manager.py` tool available

---

## 🔄 PROCEDURE STEPS

### **Step 1: Create Devlog File**

Create markdown file in `devlogs/` directory:

```bash
# File naming: YYYY-MM-DD_agent-X_task_description.md
touch devlogs/2025-01-27_agent-2_tools_consolidation_complete.md
```

### **Step 2: Write Devlog Content**

Include:
- Summary of work completed
- Actions taken
- Results achieved
- Learnings discovered
- Status and next steps

**Format**: See `docs/DEVLOG_SYSTEM_GUIDE.md` for complete format

### **Step 3: Post to Discord (AUTOMATIC)**

**Command:**
```bash
python tools/devlog_manager.py post --agent agent-X --file devlogs/YYYY-MM-DD_agent-X_task.md
```

**What Happens Automatically:**
- ✅ Devlog uploaded to Swarm Brain
- ✅ Devlog posted to your Discord channel
- ✅ Devlog index updated
- ✅ No manual steps needed

---

## ✅ SUCCESS CRITERIA

- [ ] Devlog file created in `devlogs/` directory
- [ ] Devlog posted to Discord successfully
- [ ] Devlog visible in Swarm Brain
- [ ] Devlog posted to correct Discord channel (your channel, not captain's)

---

## 🚨 CRITICAL RULES

### **DO**:
- ✅ Create devlogs automatically (NO REMINDERS NEEDED)
- ✅ Post to Discord immediately after creating devlog
- ✅ Use `--agent agent-X` flag (lowercase, with dash)
- ✅ Post to your dedicated channel for routine updates
- ✅ Use `post_devlog_to_discord.py` only for major milestones

### **DON'T**:
- ❌ Wait for reminders to create devlogs
- ❌ Post to wrong Discord channel
- ❌ Skip Discord posting
- ❌ Forget to use `--agent` flag
- ❌ Use `post_devlog_to_discord.py` for routine updates

---

## 📝 EXAMPLES

### **Example 1: Task Completion**

```bash
# 1. Create devlog
cat > devlogs/2025-01-27_agent-2_task_complete.md << 'EOF'
# Task Completion - Agent-2

**Date**: 2025-01-27  
**Agent**: Agent-2  
**Status**: ✅ COMPLETE

## Summary
Completed tools consolidation execution.

## Actions
- Archived 8 duplicate tools
- Added deprecation warnings
- Created archive log

## Results
- Phase 1 unblocked
- All tools verified working
EOF

# 2. Post to Discord
python tools/devlog_manager.py post --agent agent-2 --file devlogs/2025-01-27_agent-2_task_complete.md
```

### **Example 2: Progress Update**

```bash
# 1. Create devlog
cat > devlogs/2025-01-27_agent-2_progress_update.md << 'EOF'
# Progress Update - Agent-2

**Date**: 2025-01-27  
**Agent**: Agent-2  
**Status**: ⏳ IN PROGRESS

## Current Work
- Testing Discord channel configuration
- Verifying webhook URLs

## Progress
- 6/8 agents tested
- All webhooks valid

## Next Steps
- Complete remaining tests
- Update documentation
EOF

# 2. Post to Discord
python tools/devlog_manager.py post --agent agent-2 --file devlogs/2025-01-27_agent-2_progress_update.md
```

---

## 🔧 TROUBLESHOOTING

### **Webhook Not Found**
```bash
# Test your channel configuration
python tools/test_all_agent_discord_channels.py

# Verify environment variable
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('Webhook:', 'SET' if os.getenv('DISCORD_WEBHOOK_AGENT_X') else 'NOT SET')"
```

### **Wrong Channel**
- Check that `DISCORD_WEBHOOK_AGENT_X` is set correctly
- Verify webhook URL points to your channel (not captain's)
- Use `test_all_agent_discord_channels.py` to verify

### **Import Error**
- Ensure `load_dotenv()` is called in `devlog_manager.py`
- Check that `.env` file exists and is readable

---

## 📚 RELATED PROCEDURES

- `PROCEDURE_DAILY_AGENT_OPERATIONS.md` - Daily workflow
- `PROCEDURE_SWARM_BRAIN_CONTRIBUTION.md` - Knowledge sharing
- `docs/DEVLOG_SYSTEM_GUIDE.md` - Complete devlog format
- `docs/DISCORD_ROUTER_USAGE_INSTRUCTIONS.md` - Discord posting guide

---

## 💡 KEY POINTS

**AUTOMATIC WORKFLOW:**
1. Complete work
2. Create devlog
3. Post to Discord (automatic via devlog_manager)
4. Done!

**NO REMINDERS NEEDED** - Just create and post devlogs automatically as part of your workflow!

---

**Agent-2 - Procedure Documentation** 📚


