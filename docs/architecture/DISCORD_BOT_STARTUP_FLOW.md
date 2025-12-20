# Discord Bot Startup Flow
**Date**: 2025-12-20  
**Agent**: Agent-8 (SSOT & System Integration)  
**Status**: Documentation

---

## 🔄 **STARTUP FLOW**

The Discord bot is started through a chain of subprocess calls:

```
main.py
  └─> start_discord_bot()
      └─> tools/run_unified_discord_bot_with_restart.py
          └─> subprocess.Popen([python, src/discord_commander/unified_discord_bot.py])
              └─> unified_discord_bot.py (if __name__ == "__main__")
                  └─> bot_runner.main()
                      └─> UnifiedDiscordBot instance
                          └─> bot.start(token)
```

---

## 📋 **DETAILED FLOW**

### **1. Entry Point: `main.py`**
```python
python main.py --discord
```
- Calls `ServiceManager.start_discord_bot()`
- Spawns subprocess: `tools/run_unified_discord_bot_with_restart.py`

### **2. Restart Wrapper: `tools/run_unified_discord_bot_with_restart.py`**
- Provides auto-restart functionality
- Handles crash recovery (max 3 crashes)
- Spawns subprocess: `src/discord_commander/unified_discord_bot.py`

### **3. Bot Module: `src/discord_commander/unified_discord_bot.py`**
- Contains `UnifiedDiscordBot` class definition
- Has `if __name__ == "__main__"` block that imports `bot_runner.main()`
- **This is "piped into" main.py through the subprocess chain**

### **4. Bot Runner: `src/discord_commander/bot_runner.py`**
- Contains `main()` async function
- Creates `UnifiedDiscordBot` instance
- Handles reconnection logic
- Calls `bot.start(token)`

---

## 🎯 **KEY INSIGHT**

**`unified_discord_bot.py` is piped into `main.py`** through the subprocess chain:
- `main.py` → `run_unified_discord_bot_with_restart.py` → `unified_discord_bot.py` → `bot_runner.main()`

This allows:
- ✅ Environment variable inheritance (`.env` variables passed through)
- ✅ Fresh module imports on restart (no cache issues)
- ✅ Process isolation (bot crashes don't kill main.py)
- ✅ Auto-restart capability

---

## 🔧 **DIRECT STARTUP (Alternative)**

You can also start the bot directly:
```bash
cd D:\Agent_Cellphone_V2_Repository
python src\discord_commander\unified_discord_bot.py
```

This bypasses `main.py` and the restart wrapper, but still goes through:
- `unified_discord_bot.py` → `bot_runner.main()` → `UnifiedDiscordBot`

---

## 📝 **ENVIRONMENT VARIABLES**

Required environment variables (passed through subprocess chain):
- `DISCORD_BOT_TOKEN` - Discord bot token
- `DISCORD_CHANNEL_ID` - Optional channel ID

These are loaded from `.env` file and passed via `env=os.environ.copy()` in subprocess calls.

---

**Status**: ✅ **DOCUMENTATION COMPLETE**

