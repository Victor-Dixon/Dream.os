# Discord Developer Prefix Mapping

**Author**: Agent-7 (Web Development Specialist)  
**Date**: 2025-01-27  
**Status**: ✅ IMPLEMENTED

---

## 🎯 Overview

The Discord bot now supports automatic developer prefix mapping, allowing messages from Discord to be tagged with developer-specific prefixes like `[VICTOR]`, `[ARIA]`, `[CHRIS]`, `[CARYMN]`, or `[CHARLES]` instead of the generic `[D2A]`.

---

## 📋 Supported Prefixes

| Prefix | Developer | Usage |
|--------|-----------|-------|
| `[D2A]` | Default (Discord to Agent) | Used when no developer mapping found |
| `[VICTOR]` | Victor | Messages from Victor's Discord account |
| `[ARIA]` | Aria | Messages from Aria's Discord account |
| `[CHRIS]` | Chris | Messages from Chris's Discord account |
| `[CARYMN]` | Carymn | Messages from Carymn's Discord account |
| `[CHARLES]` | Charles | Messages from Charles's Discord account |

---

## 🔧 How It Works

### **Automatic Prefix Detection**

1. **Message Format**: Users can send messages in two formats:
   - **With Prefix**: `[VICTOR] Agent-1\n\nMessage content`
   - **Simple Format**: `Agent-1\n\nMessage content` (auto-adds prefix)

2. **Prefix Resolution**:
   - Bot checks Discord user ID against mapping
   - If mapped → Uses developer prefix (e.g., `[VICTOR]`)
   - If not mapped → Uses default `[D2A]`

3. **Mapping Sources** (checked in order):
   - Agent profiles: `agent_workspaces/{Agent-X}/profile.json`
   - Config file: `config/discord_user_map.json`

---

## 📝 Setup Instructions

### **Option 1: Agent Profiles (Recommended)**

Add to each agent's profile file:

**File**: `agent_workspaces/{Agent-X}/profile.json`

```json
{
  "agent_id": "Agent-X",
  "discord_user_id": "123456789012345678",
  "discord_username": "VICTOR",
  "developer_name": "VICTOR"
}
```

### **Option 2: Config File**

Create `config/discord_user_map.json`:

```json
{
  "123456789012345678": "VICTOR",
  "987654321098765432": "ARIA",
  "111222333444555666": "CHRIS",
  "222333444555666777": "CARYMN",
  "333444555666777888": "CHARLES"
}
```

### **Finding Your Discord User ID**

1. Enable Developer Mode in Discord (Settings → Advanced → Developer Mode)
2. Right-click your username → Copy ID
3. Add to config file or profile

---

## 🧪 Testing

### **Test Message Formats**

1. **With Explicit Prefix**:
   ```
   [VICTOR] Agent-1
   
   Test message with explicit prefix
   ```

2. **Simple Format (Auto-Prefix)**:
   ```
   Agent-1
   
   Test message - will auto-add prefix based on Discord user ID
   ```

### **Verification Steps**

1. **Check Bot Logs**:
   - Look for: `✅ Message queued: {queue_id} → {recipient} ([PREFIX])`

2. **Check Queue Processor**:
   - Look for: `✅ Message delivered: {queue_id}`

3. **Check Agent Inbox**:
   - File: `agent_workspaces/{Agent-X}/inbox/CAPTAIN_MESSAGE_{timestamp}_{id}.md`
   - Should contain prefix in message content

---

## 🔍 Troubleshooting

### **Issue: Always Using [D2A] Prefix**

**Cause**: Discord user ID not mapped

**Solution**:
1. Verify Discord user ID is correct
2. Check mapping in `config/discord_user_map.json`
3. Check agent profiles for `discord_user_id` field
4. Restart Discord bot after adding mappings

### **Issue: Invalid Prefix**

**Cause**: Developer name not in valid list

**Valid Names**: `CHRIS`, `ARIA`, `VICTOR`, `CARYMN`, `CHARLES`

**Solution**: Use one of the valid names (case-insensitive)

### **Issue: Messages Not Delivered**

**Cause**: Queue processor not running

**Solution**: Start both services:
```bash
python tools/start_discord_system.py
```

---

## 📊 Implementation Details

### **Code Location**

- **Main Handler**: `src/discord_commander/unified_discord_bot.py`
  - `_load_discord_user_map()` - Loads mappings from profiles/config
  - `_get_developer_prefix()` - Resolves prefix from Discord user ID
  - `on_message()` - Processes messages with prefix detection

### **Mapping Priority**

1. Explicit prefix in message (if valid)
2. Developer prefix from Discord user ID mapping
3. Default `[D2A]` prefix

---

## ✅ Status

- ✅ Developer prefix mapping implemented
- ✅ Profile-based mapping support
- ✅ Config file mapping support
- ✅ Automatic prefix detection
- ✅ Simple format support (auto-add prefix)
- ✅ Validation of developer names

---

## 🚀 Future Enhancements

- [ ] Web UI for managing Discord user mappings
- [ ] Automatic profile creation from Discord messages
- [ ] Support for additional developer names
- [ ] Integration with Discord username resolution

---

**🐝 WE. ARE. SWARM. ⚡🔥**

