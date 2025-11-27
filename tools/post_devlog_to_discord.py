#!/usr/bin/env python3
"""
Devlog Posting Wrapper - SSOT: devlog_poster.py

⚠️ DEPRECATED: This script is a wrapper around devlog_poster.py (SSOT).
All devlog posting should use devlog_poster.py directly:
    python tools/devlog_poster.py --agent Agent-7 --file <file>
    python tools/devlog_poster.py --agent Agent-4 --file <file> --major

This wrapper is maintained for backward compatibility only.
"""

import sys
import subprocess
from pathlib import Path

def detect_agent_from_filename(filename: str) -> str:
    """Detect agent from filename for backward compatibility."""
    filename_lower = filename.lower()
    
    if 'agent-4' in filename_lower or 'captain' in filename_lower:
        return "agent-4"
    elif 'agent-1' in filename_lower:
        return "agent-1"
    elif 'agent-2' in filename_lower:
        return "agent-2"
    elif 'agent-3' in filename_lower:
        return "agent-3"
    elif 'agent-5' in filename_lower:
        return "agent-5"
    elif 'agent-6' in filename_lower:
        return "agent-6"
    elif 'agent-7' in filename_lower:
        return "agent-7"
    elif 'agent-8' in filename_lower:
        return "agent-8"
    else:
        # Default to captain for major updates
        return "agent-4"

def post_devlog_to_discord(devlog_file: str) -> bool:
    """
    Post devlog to Discord via devlog_manager.py (SSOT).
    
    This is a wrapper that calls devlog_manager.py for backward compatibility.
    """
    devlog_path = Path(devlog_file)
    if not devlog_path.exists():
        print(f"❌ ERROR: Devlog file not found: {devlog_file}")
        return False
    
    # Detect agent from filename
    agent = detect_agent_from_filename(devlog_path.name)
    
    # Call devlog_poster.py (SSOT)
    print("⚠️  NOTE: This script is a wrapper. Using devlog_poster.py (SSOT)...")
    print(f"📤 Posting via devlog_poster.py (agent: {agent}, major: true)")
    
    # Call devlog_poster.py directly (SSOT)
    devlog_poster_path = Path(__file__).parent / "devlog_poster.py"
    cmd = [
        sys.executable, str(devlog_poster_path),
        "--agent", agent,
        "--file", str(devlog_path),
        "--major"  # Major updates (Captain posts to captain channel)
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ ERROR: devlog_manager.py failed")
        print(f"   Exit code: {e.returncode}")
        print(f"   Output: {e.stdout}")
        print(f"   Error: {e.stderr}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"❌ ERROR: Failed to call devlog_manager.py: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python post_devlog_to_discord.py <devlog_file>")
        print("\n⚠️  NOTE: This script is a wrapper around devlog_poster.py (SSOT).")
        print("   For direct usage, use: python tools/devlog_poster.py --agent Agent-X --file <file>")
        sys.exit(1)
    
    devlog_file = sys.argv[1]
    success = post_devlog_to_discord(devlog_file)
    sys.exit(0 if success else 1)

