<<<<<<< HEAD
#!/usr/bin/env python3
"""
Twitch Service Launcher
=======================

Simple launcher script for the Twitch bot.
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from src.services.chat_presence.twitch_eventsub_server import main
    main()
except Exception as e:
    print(f"Failed to start Twitch service: {e}")
=======
#!/usr/bin/env python3
"""
Twitch Service Launcher
=======================

Simple launcher script for the Twitch bot.
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from src.services.chat_presence.twitch_eventsub_server import main
    main()
except Exception as e:
    print(f"Failed to start Twitch service: {e}")
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
    sys.exit(1)