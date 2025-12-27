# Discord Webhook Username Fix Guide

**Date:** 2025-12-26  
**Issue:** Discord webhook 400 Bad Request - "Username cannot contain discord"  
**Status:** Code fix complete, Discord settings fix needed

---

## Problem

Discord API restriction: Webhook usernames cannot contain the word "discord" anywhere in the username field. This applies to:
1. **Code-level username** (in payload) - ✅ FIXED
2. **Discord webhook settings username** - ⚠️ NEEDS MANUAL UPDATE

---

## Code Fix (✅ Complete)

**File:** `tools/categories/communication_tools.py`

**Change:**
```python
# Before:
"username": f"{agent_id} (Discord Router)",

# After:
"username": f"{agent_id} (Router)",  # Removed "Discord"
```

**Status:** ✅ Fixed and tested - Agent-1 and Agent-5 devlogs posted successfully

---

## Discord Webhook Settings Fix (⏳ Manual Action Required)

If the webhook itself was configured in Discord with a username containing "discord", you need to update it in Discord's settings:

### Steps to Fix:

1. **Open Discord Server Settings**
   - Right-click on your Discord server
   - Select "Server Settings"

2. **Navigate to Webhooks**
   - Go to "Integrations" → "Webhooks"
   - Find the webhook being used (check `DISCORD_ROUTER_WEBHOOK_URL` or `DISCORD_WEBHOOK_URL` in `.env`)

3. **Edit Webhook**
   - Click on the webhook name
   - Click "Edit Webhook"

4. **Update Username**
   - Find the "Name" field (this is the webhook username)
   - If it contains "discord" (e.g., "Discord Router", "Devlog Discord Bot"), change it to something without "discord"
   - Suggested names:
     - "Agent Router"
     - "Devlog Bot"
     - "Swarm Router"
     - "Agent Updates"

5. **Save Changes**
   - Click "Save Changes"
   - The webhook will now accept posts

---

## Verification

After updating the Discord webhook settings:

1. **Test with Agent-1's devlog:**
   ```bash
   python tools/devlog_poster.py --agent Agent-1 --file agent_workspaces/Agent-1/devlogs/DISCORD_STATUS_20251226.md
   ```

2. **Test with Agent-8's devlog:**
   ```bash
   python tools/devlog_poster.py --agent Agent-8 --file agent_workspaces/Agent-8/devlogs/DISCORD_SHORT_2025-12-26.md
   ```

3. **Check Discord channel:**
   - Verify posts appear in the configured Discord channel
   - Confirm no 400 errors

---

## Current Status

- ✅ **Code fix:** Complete - Username in payload fixed
- ⏳ **Discord settings:** Needs manual update - Webhook username in Discord settings
- 📄 **Devlogs ready:** Agent-1 and Agent-8 devlogs ready for posting once webhook is fixed

---

## Alternative: Create New Webhook

If you can't edit the existing webhook, you can create a new one:

1. **Create New Webhook:**
   - Discord Server Settings → Integrations → Webhooks → "New Webhook"
   - Set name WITHOUT "discord" (e.g., "Agent Router")
   - Copy webhook URL

2. **Update .env:**
   ```bash
   DISCORD_ROUTER_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_NEW_WEBHOOK_URL
   ```

3. **Test:**
   - Run devlog_poster.py with any agent's devlog
   - Verify post appears in Discord

---

**Status:** ⚠️ Manual action required - Update Discord webhook username settings



