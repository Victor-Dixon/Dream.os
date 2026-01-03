#!/usr/bin/env python3
"""
Process All Conversations Demo
=============================

This script demonstrates the correct way to process ALL existing conversations
through the Dreamscape system, which is what the "🌌 Process Dreamscape" 
button in the Conversations Panel does.

This is DIFFERENT from Live Processing, which only monitors for new conversations.
"""

import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# EDIT START: Consolidate memory imports to use memory_system (core consolidation)
from dreamscape.core.memory import MemoryManager
# EDIT END
from dreamscape.core.dreamscape_processor import DreamscapeProcessor
from dreamscape.core.mmorpg_system import MMORPGEngine

def demo_process_all_conversations():
    """Demonstrate processing all conversations through Dreamscape."""
    print("🎯 Processing ALL Conversations Demo")
    print("=" * 50)
    print()
    print("This demonstrates what the '🌌 Process Dreamscape' button does.")
    print("It processes ALL existing conversations, not just new ones.")
    print()
    
    try:
        # Initialize components
        print("🔧 Initializing components...")
        memory_manager = MemoryManager("dreamos_memory.db")
        processor = DreamscapeProcessor()
        mmorpg = MMORPGEngine()
        
        # Get total conversation count
        total_count = memory_manager.get_conversations_count()
        print(f"📊 Found {total_count} conversations in database")
        
        if total_count == 0:
            print("❌ No conversations found. Please import some conversations first.")
            return
        
        # Get current MMORPG state
        player = mmorpg.get_player()
        print(f"👤 Current Player: {player.name} (Tier {player.architect_tier})")
        print(f"⭐ Current XP: {player.xp}")
        
        # Process ALL conversations in chronological order
        print(f"\n🔄 Processing ALL {total_count} conversations through Dreamscape...")
        print("This may take several minutes...")
        
        result = processor.process_conversations_chronological(limit=None)  # None = process all
        
        if result.get("error"):
            print(f"❌ Processing failed: {result['error']}")
            return
        
        processed_count = result.get("processed_count", 0)
        total_conversations = result.get("total_conversations", 0)
        conversations_processed = result.get("conversations_processed", 0)
        
        print(f"\n✅ Processing completed!")
        print(f"   Processed: {processed_count}/{conversations_processed} conversations")
        print(f"   Total in database: {total_conversations}")
        
        # Show updated MMORPG state
        player = mmorpg.get_player()
        skills = mmorpg.get_skills()
        
        print(f"\n🎮 Updated MMORPG State:")
        print(f"   Player: {player.name} (Tier {player.architect_tier})")
        print(f"   XP: {player.xp}")
        print(f"   Skills: {len(skills)} active skills")
        
        # Show any errors
        if result.get("errors"):
            print(f"\n⚠️  Errors encountered: {len(result['errors'])}")
            for error in result["errors"][:5]:  # Show first 5 errors
                print(f"   • {error}")
            if len(result["errors"]) > 5:
                print(f"   • ... and {len(result['errors']) - 5} more errors")
        
        print(f"\n🎉 All conversations have been processed through the Dreamscape system!")
        print("   Your MMORPG storyline has been updated with new quests, skills, and domains.")
        
        processor.close()
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()

def explain_difference():
    """Explain the difference between Live Processing and Process All."""
    print("\n" + "="*60)
    print("📚 UNDERSTANDING THE DIFFERENCE")
    print("="*60)
    print()
    print("🔄 LIVE PROCESSING (Dashboard 'Start Live Processing' button):")
    print("   • Monitors for NEW conversations in real-time")
    print("   • Only processes conversations that appear AFTER you start it")
    print("   • Does NOT process existing conversations in your database")
    print("   • Use this for continuous monitoring of new activity")
    print()
    print("🌌 PROCESS ALL CONVERSATIONS (Conversations Panel 'Process Dreamscape' button):")
    print("   • Processes ALL existing conversations in your database")
    print("   • Runs them through the Dreamscape MMORPG system")
    print("   • Updates your player stats, skills, and quests")
    print("   • Use this to process your entire conversation history")
    print()
    print("💡 RECOMMENDED WORKFLOW:")
    print("   1. First use '🌌 Process Dreamscape' to process all existing conversations")
    print("   2. Then optionally use 'Start Live Processing' to monitor for new ones")
    print()

if __name__ == "__main__":
    explain_difference()
    
    response = input("Would you like to run the demo to process all conversations? (y/N): ")
    if response.lower() == 'y':
        demo_process_all_conversations()
    else:
        print("Demo skipped. Use the '🌌 Process Dreamscape' button in the Conversations Panel instead.") 