#!/usr/bin/env python3
"""
Dream.OS Conversation Ingestion (Legacy Redirect)
================================================

This script has been merged into unified_conversation_manager.py
Run that script instead for full functionality.
"""

import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def main():
    """Redirect to the unified conversation manager."""
    print("🔄 Script Migration Notice")
    print("=" * 50)
    print("This script has been merged into 'unified_conversation_manager.py'")
    print("The new script provides:")
    print("• Conversation ingestion from files")
    print("• Conversation processing with AI analysis")
    print("• MMORPG skill updates")
    print("• Discord integration")
    print("• Full workflow options")
    
    print("\n🚀 To continue, run:")
    print("python scripts/unified_conversation_manager.py")
    
    # Ask if user wants to run the new script
    choice = input("\nRun the unified script now? (y/N): ").strip().lower()
    if choice == 'y':
        import subprocess
        subprocess.run([sys.executable, "scripts/unified_conversation_manager.py"])
    else:
        print("You can run it manually when ready.")

if __name__ == "__main__":
    main() 