#!/usr/bin/env python3
"""Send Discord monitor fix completion to Discord."""

from src.core.messaging_core import (
    UnifiedMessagePriority, UnifiedMessageTag, UnifiedMessageType, send_message,
)
import sys
from pathlib import Path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))


msg = """**✅ Discord Monitor Button Fix - COMPLETE**

**Task:** Fix !monitor discord.view button - add start/stop functionality

**Issue:** Button only showed status, couldn't start/stop monitor

**Fix Applied:**
• Created MonitorControlView class with Start/Stop buttons
• Updated show_monitor_control() to use interactive view
• Buttons now allow starting/stopping monitor directly from UI

**Files Changed:**
• src/discord_commander/views/main_control_panel_view.py

**Status:** ✅ Complete - Monitor button now has functional start/stop controls"""

if __name__ == "__main__":
    try:
        result = send_message(
            content=msg, sender="Agent-2", recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            tags=[UnifiedMessageTag.SYSTEM, UnifiedMessageTag.COORDINATION],
        )
        print("✅ Sent" if result else "❌ Failed")
        sys.exit(0 if result else 1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
