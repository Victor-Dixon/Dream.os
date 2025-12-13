# Discord Bot Silent Failure Investigation Report

**Date**: 2025-12-13  
**Agent**: Agent-4 (Captain)  
**Issue**: Discord bot keeps stopping silently/failing

## Problem Summary

The Discord bot is failing silently and stopping instead of automatically reconnecting when disconnected. Investigation reveals multiple failure points.

## Root Causes Identified

### 1. **Early Return on Successful Start (CRITICAL)**
**Location**: `src/discord_commander/unified_discord_bot.py:2581`

```python
await bot.start(token)
# ...
return 0  # Clean exit (shouldn't normally reach here)
```

**Problem**: When `bot.start()` completes (either by disconnect or error), the code immediately returns 0, exiting the reconnection loop. This causes the bot to stop instead of reconnecting.

**Impact**: Any disconnection results in bot stopping completely instead of reconnecting.

### 2. **KeyboardInterrupt Handling**
**Location**: `src/discord_commander/unified_discord_bot.py:2583-2589`

**Problem**: KeyboardInterrupt errors are being logged to error log, suggesting the bot is being killed (possibly by the restart script or system). The bot returns 0 on KeyboardInterrupt, which appears successful to the restart script.

**Impact**: Silent failure - restart script doesn't detect this as a crash.

### 3. **Interaction Already Acknowledged Error**
**Location**: `src/discord_commander/controllers/messaging_controller_view.py:188`

**Problem**: Discord interaction is being acknowledged twice:
- First at line 188: `await interaction.response.send_modal(modal)`
- Then in error handler at line 192: `await interaction.response.send_message(...)`

This causes errors but doesn't crash the bot - it's logged but continues.

### 4. **Missing Exception Types in Reconnection Loop**
**Location**: `src/discord_commander/unified_discord_bot.py:2645`

**Problem**: The generic `Exception` handler may not catch all Discord-specific exceptions that should trigger reconnection.

### 5. **Run Script Doesn't Catch All Exit Codes**
**Location**: `tools/run_unified_discord_bot_with_restart.py:96`

**Problem**: Script checks `exit_code != 0` but the bot returns 0 on KeyboardInterrupt, so the script thinks it's a clean exit.

## Evidence from Logs

### Error Log Patterns:
```
KeyboardInterrupt
Exception ignored in: <module 'threading'...>
lost sys.stderr
```

### Bot Log Patterns:
```
2025-12-12 17:03:16 - WARNING - Discord Bot disconnected - will attempt to reconnect
2025-12-12 17:39:28 - WARNING - Discord Bot disconnected - will attempt to reconnect
2025-12-12 17:42:22 - WARNING - Discord Bot disconnected - will attempt to reconnect
```

**Observation**: Disconnection warnings are logged, but no reconnection attempts are visible after them. Bot stops instead of reconnecting.

## Recommended Fixes

### Fix 1: Remove Early Return in Reconnection Loop (HIGH PRIORITY)
**File**: `src/discord_commander/unified_discord_bot.py`

**Change**: Remove the `return 0` after `await bot.start(token)` and let the loop continue for reconnection.

```python
# BEFORE:
await bot.start(token)
return 0  # Clean exit (shouldn't normally reach here)

# AFTER:
await bot.start(token)
# Bot disconnected - loop will continue for reconnection
# Only reset counters on successful connection
```

### Fix 2: Handle Discord Disconnect Properly
**File**: `src/discord_commander/unified_discord_bot.py`

**Add**: Check for specific disconnect exceptions and handle them in the reconnection loop.

```python
except discord.errors.ConnectionClosed as e:
    logger.warning(f"Discord connection closed: {e.code}")
    # Continue loop for reconnection
    reconnect_count += 1
    continue
```

### Fix 3: Fix Interaction Acknowledgment Error
**File**: `src/discord_commander/controllers/messaging_controller_view.py`

**Change**: Check if interaction is already responded before responding again.

```python
# BEFORE:
except Exception as e:
    logger.error(f"Error opening agent message modal: {e}", exc_info=True)
    if not interaction.response.is_done():
        await interaction.response.send_message(...)

# AFTER:
except Exception as e:
    logger.error(f"Error opening agent message modal: {e}", exc_info=True)
    if not interaction.response.is_done():
        await interaction.response.send_message(...)
    elif isinstance(e, discord.errors.HTTPException) and "already been acknowledged" in str(e):
        # Try to send followup instead
        await interaction.followup.send(f"❌ Error: {e}", ephemeral=True)
```

### Fix 4: Improve KeyboardInterrupt Handling
**File**: `src/discord_commander/unified_discord_bot.py`

**Change**: Log KeyboardInterrupt to main log, not error log, and ensure it's properly propagated.

### Fix 5: Add Heartbeat Monitoring
**File**: `src/discord_commander/unified_discord_bot.py`

**Enhancement**: The bot already has `last_heartbeat` tracking. Add a watchdog that detects missing heartbeats and triggers reconnection.

## Implementation Priority

1. **P1 (Critical)**: Fix 1 - Remove early return (blocks all reconnections)
2. **P1 (Critical)**: Fix 2 - Handle disconnect properly (core functionality)
3. **P2 (Important)**: Fix 3 - Fix interaction error (user experience)
4. **P2 (Important)**: Fix 4 - Improve KeyboardInterrupt handling (diagnostics)
5. **P3 (Enhancement)**: Fix 5 - Add heartbeat monitoring (proactive detection)

## Testing Plan

1. Test normal disconnection (network outage simulation)
2. Test KeyboardInterrupt handling
3. Test interaction error scenarios
4. Monitor logs for 24 hours after fixes
5. Verify reconnection loop works correctly

## Related Files

- `src/discord_commander/unified_discord_bot.py` - Main bot code
- `src/discord_commander/controllers/messaging_controller_view.py` - Interaction handler
- `tools/run_unified_discord_bot_with_restart.py` - Restart script
- `logs/discord_bot.log` - Main bot log
- `logs/discord_bot_errors.log` - Error log

## Status

✅ **Investigation Complete**  
⏳ **Awaiting Implementation**

