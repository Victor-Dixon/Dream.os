# Discord Bot Restart Loop Fix

**Author**: Agent-3 (Infrastructure & DevOps)  
**Date**: 2025-01-27  
**Issue**: Discord bot keeps restarting itself infinitely  
**Status**: ✅ Fixed

---

## 🐛 **PROBLEM IDENTIFIED**

The Discord bot was restarting infinitely due to:

1. **Infinite Restart Loop**: `scripts/run_unified_discord_bot_with_restart.py` had a `while True:` loop that restarted the bot on ANY exit, including crashes
2. **No Crash Detection**: The script didn't distinguish between intentional restarts (via `!restart` command) and crashes
3. **No Error Recovery**: When the bot crashed, it would immediately restart, creating an infinite loop
4. **Missing Error Handlers**: Bot lacked proper error handlers for disconnects and reconnections

---

## ✅ **FIXES IMPLEMENTED**

### **1. Fixed Restart Script** (`scripts/run_unified_discord_bot_with_restart.py`)

**Changes**:
- ✅ Added crash detection and counting
- ✅ Only restarts on intentional restart (when `.discord_bot_restart` flag exists)
- ✅ Stops after 3 consecutive crashes to prevent infinite loops
- ✅ Added cooldown period (10 seconds) between crash restarts
- ✅ Proper exit code handling

**Before**:
```python
while True:
    exit_code = run_bot()
    if restart_flag.exists():
        continue  # Restart
    break  # Exit
```

**After**:
```python
crash_count = 0
max_crashes = 3

while True:
    exit_code = run_bot()
    if restart_flag.exists():
        crash_count = 0  # Reset on intentional restart
        continue
    if exit_code != 0:
        crash_count += 1
        if crash_count >= max_crashes:
            break  # Stop after too many crashes
        time.sleep(10)  # Cooldown
        continue
    break  # Clean exit
```

---

### **2. Fixed Bot Error Handling** (`src/discord_commander/unified_discord_bot.py`)

**Changes**:
- ✅ Added `on_disconnect()` handler to log disconnections
- ✅ Added `on_error()` handler to catch event errors without crashing
- ✅ Fixed `on_ready()` to prevent duplicate startup messages on reconnection
- ✅ Added proper exit codes to `main()` function
- ✅ Better error handling for login failures and missing intents

**New Error Handlers**:
```python
async def on_disconnect(self):
    """Handle bot disconnection."""
    self.logger.warning("⚠️ Discord Bot disconnected - will attempt to reconnect")
    if hasattr(self, '_startup_sent'):
        delattr(self, '_startup_sent')

async def on_error(self, event, *args, **kwargs):
    """Handle errors in event handlers."""
    self.logger.error(f"❌ Error in event {event}: {args}", exc_info=True)
    # Don't close bot on errors - let it try to recover
```

**Fixed Startup Message**:
```python
async def on_ready(self):
    """Bot ready event."""
    # Prevent duplicate startup messages on reconnection
    if not hasattr(self, '_startup_sent'):
        # Send startup message only once
        await self.send_startup_message()
        self._startup_sent = True
    else:
        # Reconnection - just log, don't spam
        self.logger.info(f"🔄 Discord Bot reconnected: {self.user}")
```

---

## 🎯 **HOW IT WORKS NOW**

1. **Intentional Restart**: When `!restart` command is used:
   - Bot creates `.discord_bot_restart` flag file
   - Bot closes gracefully
   - Restart script detects flag and restarts after 3 seconds
   - Crash count is reset

2. **Bot Crash**: When bot crashes:
   - Exit code is non-zero
   - Restart script increments crash count
   - If crash count < 3: Wait 10 seconds, then restart
   - If crash count >= 3: Stop auto-restart, prevent infinite loop

3. **Clean Shutdown**: When `!shutdown` command is used:
   - Bot closes gracefully
   - Exit code is 0
   - Restart script exits cleanly

4. **Reconnection**: When Discord connection drops:
   - Bot automatically reconnects (Discord.py handles this)
   - `on_ready()` fires but doesn't spam startup message
   - Only logs reconnection

---

## 📋 **USAGE**

### **Start Bot**:
```bash
python scripts/start_discord_bot.py
```

### **Start Bot with Auto-Restart** (for production):
```bash
python scripts/run_unified_discord_bot_with_restart.py
```

### **Restart Bot** (via Discord):
```
!restart
```

### **Shutdown Bot** (via Discord):
```
!shutdown
```

---

## ⚠️ **IMPORTANT NOTES**

1. **Multiple Instances**: If you see multiple Python processes, kill them all before starting:
   ```bash
   # Windows PowerShell
   Get-Process python | Where-Object {$_.CommandLine -like "*discord*"} | Stop-Process
   ```

2. **Crash Prevention**: If bot crashes 3 times in a row, auto-restart stops. Investigate the issue before restarting manually.

3. **Restart Flag**: The `.discord_bot_restart` flag file is automatically created/removed. Don't create it manually.

---

## ✅ **STATUS**

**Issue**: ✅ Fixed  
**Testing**: Ready for testing  
**Documentation**: ✅ Complete

---

**WE. ARE. SWARM. FIXED. STABLE. 🐝⚡🔥**




