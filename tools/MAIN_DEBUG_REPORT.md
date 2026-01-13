# Main.py Debug Report

**Date**: 2025-12-22  
**File**: `main.py`  
**Status**: ⚠️ **2 Missing Files Found**

## Summary

The `main.py` file is **functionally correct** but references two missing files:
1. `tools/start_message_queue_processor.py` - NOT FOUND
2. `tools/START_CHAT_BOT_NOW.py` - NOT FOUND

## Debug Results

### ✅ Working Components

1. **Syntax**: Valid Python syntax
2. **Imports**: All imports work correctly
   - ✅ dotenv
   - ✅ argparse
   - ✅ subprocess
   - ✅ psutil
   - ✅ agent_mode_manager (imports successfully)
3. **Agent Mode Manager**: Working correctly
   - Current mode: 8-agent
   - Active agents: All 8 agents configured
4. **Environment Variables**: All set correctly
   - ✅ TWITCH_CHANNEL
   - ✅ TWITCH_ACCESS_TOKEN
   - ✅ DISCORD_BOT_TOKEN
5. **Discord Bot Script**: ✅ Found at `tools/start_discord_system.py`

### ❌ Issues Found

#### 1. Missing Message Queue Processor Script

**Expected**: `tools/start_message_queue_processor.py`  
**Status**: ❌ NOT FOUND

**Impact**: The `--message-queue` flag and automatic message queue startup will fail.

**Possible Solutions**:
- ✅ **FOUND**: `start_discord_system.py` starts message queue using `python -m src.core.message_queue_processor`
- Create the missing script OR update `main.py` to use module import: `python -m src.core.message_queue_processor`

**Related Files Found**:
- `src/core/message_queue_processor/` - Processor module (can be run as `-m src.core.message_queue_processor`)
- `src/core/message_queue.py` - Queue implementation
- `tools/start_discord_system.py` - Shows correct way to start: `python -m src.core.message_queue_processor`

#### 2. Missing Twitch Bot Script

**Expected**: `tools/START_CHAT_BOT_NOW.py`  
**Status**: ❌ NOT FOUND

**Impact**: The `--twitch` flag and automatic Twitch bot startup will fail.

**Possible Solutions**:
- Check if Twitch bot is started via another mechanism
- Create the missing script if needed
- Update `main.py` to use alternative entry point (e.g., `src/services/chat_presence/twitch_bridge.py`)

**Related Files Found**:
- `src/services/chat_presence/twitch_bridge.py` - Twitch bridge implementation
- `src/services/chat_presence/twitch_eventsub_handler.py` - Event handler

## Recommendations

### Option 1: Create Missing Scripts

Create stub scripts that call the actual implementations:

**`tools/start_message_queue_processor.py`**:
```python
#!/usr/bin/env python3
"""Start message queue processor."""
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core.message_queue_processor import MessageQueueProcessor

if __name__ == "__main__":
    processor = MessageQueueProcessor()
    processor.start()
```

**`tools/START_CHAT_BOT_NOW.py`**:
```python
#!/usr/bin/env python3
"""Start Twitch chat bot."""
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import and start Twitch bot
# (Implementation depends on actual Twitch bot structure)
```

### Option 2: Update main.py to Use Direct Imports

Modify `main.py` to directly import and start services instead of calling scripts:

```python
def start_message_queue(self):
    """Start message queue processor."""
    from src.core.message_queue_processor import MessageQueueProcessor
    processor = MessageQueueProcessor()
    processor.start()
```

### Option 3: Make Scripts Optional

Update `main.py` to gracefully handle missing scripts:

```python
def start_message_queue(self):
    """Start message queue processor."""
    script = self.project_root / "tools" / "start_message_queue_processor.py"
    if not script.exists():
        print("   ⚠️  Message queue script not found, trying direct import...")
        try:
            from src.core.message_queue_processor import MessageQueueProcessor
            processor = MessageQueueProcessor()
            processor.start()
            return True
        except Exception as e:
            print(f"   ❌ Failed: {e}")
            return False
    # ... existing code ...
```

## Current Behavior

When running `main.py`:
- ✅ `--help` works
- ✅ `--status` works (shows services status)
- ✅ `--select-mode` works (agent mode selection)
- ✅ `--discord` works (Discord bot starts)
- ❌ `--message-queue` fails (script not found)
- ❌ `--twitch` fails (script not found)
- ⚠️  Starting all services will fail for message queue and Twitch bot

## Next Steps

1. **Verify if services are started elsewhere**: Check if `start_discord_system.py` starts message queue
2. **Create missing scripts** OR **update main.py** to use direct imports
3. **Test all service startup paths** after fixes

---

**Debug Tool**: `tools/debug_main.py`  
**Run**: `python tools/debug_main.py`

