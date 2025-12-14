#!/usr/bin/env python3
"""Send report truthfulness completion to Discord."""

from src.core.messaging_core import (
    UnifiedMessagePriority, UnifiedMessageTag, UnifiedMessageType, send_message,
)
import sys
from pathlib import Path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))


msg = """**✅ Report Truthfulness Enhancement - COMPLETE**

**Task:** Tighten report truthfulness (scope tags + evidence links)

**Actions:**
1. ✅ Created `tools/report_truthfulness_enhancer.py`
2. ✅ Enhanced WordPress audit report
3. ✅ Created standard template & documentation

**Deliverables:**
• Enhancement tool with automated scope tags & evidence links
• Enhanced example report
• Standard template (`docs/AGENT2_REPORT_TEMPLATE.md`)
• Standards doc (`docs/AGENT2_REPORTING_STANDARDS.md`)

**Status:** ✅ Complete - All reports now verifiable with evidence links"""

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
