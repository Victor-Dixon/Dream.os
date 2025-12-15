# 🤖 Automatic Website Updates Setup

**Purpose:** Automatically update weareswarm.online when agents complete tasks or update status  
**Status:** Ready to configure and use

---

## 🎯 Quick Setup

### **Step 1: Configure WordPress API** (2 min)

Follow the setup guide: `Swarm_website/SWARM_AUTO_UPDATE_SETUP.md`

You need:
- WordPress Application Password
- Environment variables set in `.env`

### **Step 2: Install Dependencies** (1 min)

```bash
cd D:\Agent_Cellphone_V2_Repository
pip install requests
```

### **Step 3: Test Connection** (1 min)

```bash
python -c "from src.services.swarm_website.website_updater import SwarmWebsiteUpdater; updater = SwarmWebsiteUpdater(); print(updater.test_connection())"
```

Expected: `✅ Website connection successful!`

---

## 🚀 Usage

### **Option 1: Continuous Monitoring (Background Service)**

Run as a background service that continuously monitors agent status files:

```bash
python tools/swarm_website_auto_update.py
```

This will:
- Check all active agents every 10 seconds
- Automatically update website when status changes
- Run continuously until stopped

**For Windows (Background):**
```powershell
Start-Process python -ArgumentList "tools\swarm_website_auto_update.py" -WindowStyle Hidden
```

**For Linux/Mac (Background):**
```bash
nohup python tools/swarm_website_auto_update.py &
```

### **Option 2: Run Once (For Cron/Task Scheduler)**

Run once, check all agents, then exit:

```bash
python tools/swarm_website_auto_update.py --once
```

**Windows Task Scheduler:**
- Create task to run every 5 minutes
- Action: `python`
- Arguments: `tools\swarm_website_auto_update.py --once`
- Start in: `D:\Agent_Cellphone_V2_Repository`

**Linux Cron:**
```bash
# Update every 5 minutes
*/5 * * * * cd /path/to/Agent_Cellphone_V2_Repository && python tools/swarm_website_auto_update.py --once
```

### **Option 3: Custom Interval**

Check every 30 seconds instead of default 10:

```bash
python tools/swarm_website_auto_update.py --interval 30
```

---

## 🔧 How It Works

1. **Monitors Agent Status Files**
   - Watches `agent_workspaces/Agent-X/status.json` files
   - Detects changes by comparing file hashes

2. **Rate Limiting**
   - Cooldown of 5 seconds between updates per agent
   - Prevents API spam

3. **Mode-Aware**
   - Only checks active agents (respects 4-agent mode)
   - Ignores paused agents

4. **Automatic Updates**
   - When status.json changes → Updates website
   - Syncs: status, points, mission, phase, last_updated

---

## 📊 What Gets Updated

When an agent's `status.json` changes, the following is automatically sent to the website:

- **Agent Status** (active/idle/paused)
- **Total Points** (from status.json)
- **Current Mission** (description)
- **Current Phase** (if available)
- **Last Updated** (timestamp)

---

## 🔄 Integration with Agent System

The auto-updater works automatically once running. Agents don't need to change their code - when they update their `status.json` file, the website is updated automatically.

**Example Flow:**
1. Agent completes a task
2. Agent updates `agent_workspaces/Agent-1/status.json`
3. Auto-updater detects change (within 10 seconds)
4. Website is updated via REST API
5. Live activity feed shows the update

---

## 🐝 Mission Log Integration

To automatically post mission logs, agents can call:

```python
from src.services.swarm_website.website_updater import SwarmWebsiteUpdater

updater = SwarmWebsiteUpdater()
updater.post_mission_log(
    agent="Agent-1",
    message="✅ Completed task: Refactored messaging system",
    priority="high",
    tags=["refactor", "messaging"]
)
```

---

## 📈 Monitoring

**Check if it's running:**
```bash
# Windows
tasklist | findstr python

# Linux/Mac
ps aux | grep swarm_website_auto_update
```

**View logs:**
The tool logs to stdout. For background services, redirect to a log file:

```bash
python tools/swarm_website_auto_update.py >> logs/website_updates.log 2>&1
```

---

## 🚨 Troubleshooting

**Q: Website not updating?**
- Check environment variables are set correctly
- Verify WordPress API is accessible
- Check logs for errors
- Test connection: `python -c "from src.services.swarm_website.website_updater import SwarmWebsiteUpdater; updater = SwarmWebsiteUpdater(); print(updater.test_connection())"`

**Q: Updates too frequent?**
- Increase `--interval` (default: 10 seconds)
- Cooldown is 5 seconds per agent already

**Q: Want to update specific agent only?**
```python
from src.services.swarm_website.auto_updater import auto_update_agent_status
auto_update_agent_status("Agent-1")
```

---

## ✅ Summary

**Setup:** 3 steps (5 minutes)
**Usage:** Run background service or cron job
**Result:** Website automatically updates when agents change status!

**WE. ARE. SWARM!** 🐝⚡


