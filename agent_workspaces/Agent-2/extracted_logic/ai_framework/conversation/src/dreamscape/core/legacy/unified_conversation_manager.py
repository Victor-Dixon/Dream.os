#from src.dreamscape.core.utils.print_utils import print_header, print_section, print_step, print_success, print_warning, print_error, print_info
"""
Unified Conversation Manager
============================

Combines conversation ingestion and processing functionality.
Can ingest new conversations from files and process existing conversations
with AI analysis, MMORPG skill updates, and Discord posting.
"""

import sys
import os
import time
import logging
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dreamscape.core.conversation_system import ConversationStorage  # Consolidated import (was conversation_storage)
from dreamscape.core.database_schema_manager import DatabaseSchemaManager
from dreamscape.core.enhanced_progress_system import EnhancedProgressSystem
from dreamscape.core.mmorpg_engine import MMORPGEngine
from dreamscape.core.memory import MemoryManager
from dreamscape.core.discord_manager import DiscordManager
from dreamscape.core.template_engine import render_template

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def ingest_conversations_from_files():
    """Ingest conversations from data/conversations/ directory."""
    print_step(1, "Ingesting Conversations from Files")
    
    # Check if conversations directory exists
    conversations_dir = Path("data/conversations")
    if not conversations_dir.exists():
        print_error(f"Conversations directory not found: {conversations_dir}")
        print_info("Please ensure you have conversations in data/conversations/")
        return False, 0
    
    # Count existing conversation files
    conversation_files = list(conversations_dir.glob("*.json"))
    print_info(f"Found {len(conversation_files)} conversation files")
    
    if not conversation_files:
        print_warning("No conversation files found to ingest")
        return False, 0
    
    # Initialize memory manager
    try:
        with MemoryManager("dreamos_memory.db") as memory:
            print_success("Memory database initialized")
            
            # Show existing stats
            existing_stats = memory.get_conversation_stats()
            if existing_stats['total_conversations'] > 0:
                print_info(f"Existing conversations in database: {existing_stats['total_conversations']}")
            
            # Ingest conversations
            print_info("Starting conversation ingestion...")
            ingested_count = memory.ingest_conversations(str(conversations_dir))
            
            if ingested_count > 0:
                print_success(f"Successfully ingested {ingested_count} conversations!")
                
                # Show updated stats
                updated_stats = memory.get_conversation_stats()
                print_info(f"Memory Database Statistics:")
                print(f"  Total Conversations: {updated_stats['total_conversations']}")
                print(f"  Total Messages: {updated_stats['total_messages']}")
                print(f"  Total Words: {updated_stats['total_words']:,}")
                print(f"  Models Used: {', '.join(updated_stats['models'].keys())}")
                
                if updated_stats['date_range']['earliest']:
                    print(f"  Date Range: {updated_stats['date_range']['earliest']} to {updated_stats['date_range']['latest']}")
                
                return True, ingested_count
            else:
                print_warning("No conversations were ingested")
                return False, 0
                
    except Exception as e:
        print_error(f"Failed to ingest conversations: {e}")
        return False, 0

def check_conversation_status():
    """Check the current status of conversations."""
    print_step(2, "Checking Conversation Status")
    
    try:
        # Initialize database
        db_manager = DatabaseSchemaManager()
        connection = db_manager.init_database("dreamos_memory.db")
        
        # Get conversation storage
        conversation_storage = ConversationStorage(connection)
        
        # Get all conversations
        conversations = conversation_storage.get_conversations(limit=None)
        
        print_info(f"Total conversations found: {len(conversations)}")
        
        # Check processing status
        processed = [c for c in conversations if c.get('processed', False)]
        unprocessed = [c for c in conversations if not c.get('processed', False)]
        
        print_info(f"Already processed: {len(processed)}")
        print_info(f"Need processing: {len(unprocessed)}")
        
        # Check content status
        with_content = [c for c in conversations if c.get('content') and len(c.get('content', '')) > 100]
        without_content = [c for c in conversations if not c.get('content') or len(c.get('content', '')) <= 100]
        
        print_info(f"With content: {len(with_content)}")
        print_info(f"Without content: {len(without_content)}")
        
        return conversations, unprocessed, with_content
        
    except Exception as e:
        print_error(f"Failed to check conversation status: {e}")
        return None, None, None

def process_conversations(conversations, limit=None, override_daily_limits=False):
    """Process conversations using the enhanced pipeline."""
    print_step(3, "Processing Conversations")
    
    try:
        # Initialize systems
        db_manager = DatabaseSchemaManager()
        connection = db_manager.init_database("dreamos_memory.db")
        
        conversation_storage = ConversationStorage(connection)
        mmorpg_engine = MMORPGEngine()
        memory_manager = MemoryManager("dreamos_memory.db")
        enhanced_progress = EnhancedProgressSystem(mmorpg_engine, memory_manager)
        discord_manager = DiscordManager()
        
        print_success("All systems initialized")
        
        # Filter conversations to process
        to_process = [c for c in conversations if not c.get('processed', False)]
        
        if limit:
            to_process = to_process[:limit]
        
        # Detect if this is a first ingestion (large number of unprocessed conversations)
        is_first_ingestion = len(to_process) > 50 or override_daily_limits
        
        if is_first_ingestion:
            print_info(f"🚀 First ingestion detected! Processing {len(to_process)} conversations with daily XP limit override")
            print_info("This allows you to process all historical conversations without daily XP restrictions")
        else:
            print_info(f"Processing {len(to_process)} conversations (daily XP limits apply)")
        
        # Process each conversation
        processed_count = 0
        failed_count = 0
        
        for i, conversation in enumerate(to_process, 1):
            try:
                print(f"\n📝 Processing conversation {i}/{len(to_process)}: {conversation.get('title', 'Untitled')[:50]}...")
                
                # Skip if no content
                if not conversation.get('content') or len(conversation.get('content', '')) < 100:
                    print_warning("Skipping - insufficient content")
                    continue
                
                # Process with enhanced pipeline
                try:
                    # Analyze conversation for progress
                    progress_event = enhanced_progress.analyze_conversation_for_progress(
                        conversation['id'], 
                        conversation.get('content', '')
                    )
                    
                    # Apply the progress event (with override for first ingestion)
                    result = enhanced_progress.apply_progress_event(progress_event, override_daily_limit=is_first_ingestion)
                    
                    # Update MMORPG state
                    mmorpg_engine.update_from_conversation(conversation['id'])
                    
                except Exception as e:
                    print_error(f"Error in progress analysis: {e}")
                    result = False
                
                if result:
                    processed_count += 1
                    print_success(f"Processed successfully")
                    
                    # Mark as processed
                    conversation['processed'] = True
                    conversation['processed_at'] = time.time()
                    
                    # Update conversation in storage
                    try:
                        conversation_storage.update_conversation(conversation['id'], conversation)
                    except:
                        # Fallback to content update if full update fails
                        content = conversation.get('content', '')
                        message_count = conversation.get('message_count', 0)
                        word_count = conversation.get('word_count', 0)
                        conversation_storage.update_conversation_content(conversation['id'], content, message_count, word_count)
                    
                else:
                    failed_count += 1
                    print_warning("Processing failed")
                
                # Small delay to avoid overwhelming the system
                time.sleep(0.1)
                
            except Exception as e:
                failed_count += 1
                print_error(f"Error processing conversation: {e}")
                continue
        
        print_success(f"Processing complete!")
        print_info(f"Successfully processed: {processed_count}")
        print_info(f"Failed: {failed_count}")
        
        return processed_count, failed_count
        
    except Exception as e:
        print_error(f"Failed to process conversations: {e}")
        return 0, 0

def update_mmorpg_state():
    """Update MMORPG state after processing."""
    print_step(4, "Updating MMORPG State")
    
    try:
        mmorpg_engine = MMORPGEngine()
        
        # Save current state
        mmorpg_engine.save_state()
        
        # Get current stats
        player = mmorpg_engine.get_player_info()
        skills = mmorpg_engine.get_all_skills()
        
        print_success("MMORPG state updated")
        print_info(f"Player: {player.get('name', 'Unknown')}")
        print_info(f"Tier: {player.get('tier', 1)}")
        print_info(f"Total XP: {player.get('total_xp', 0)}")
        print_info(f"Skills: {len(skills)}")
        
        return True
        
    except Exception as e:
        print_error(f"Failed to update MMORPG state: {e}")
        return False

def post_discord_updates():
    """Post updates to Discord if enabled."""
    print_step(5, "Posting Discord Updates")
    
    try:
        discord_manager = DiscordManager()
        
        if not discord_manager.config['enabled']:
            print_warning("Discord is not enabled")
            return True
        
        if not discord_manager.config['bot_token'] or discord_manager.config['bot_token'] == 'YOUR_DISCORD_BOT_TOKEN_HERE':
            print_warning("Discord bot token not configured")
            return True
        
        # Send a summary message
        summary_message = "🎮 **Dream.OS Conversation Processing Complete**\n\n✅ All conversations have been processed through the enhanced pipeline.\n\nThis includes:\n• AI analysis and template processing\n• MMORPG skill updates\n• Devlog generation\n• Progress tracking"
        
        # Try to send via Discord manager
        try:
            import asyncio
            asyncio.run(discord_manager.send_message(summary_message, discord_manager.config['channel_id']))
            print_success("Discord update posted")
        except Exception as e:
            print_warning(f"Failed to post to Discord: {e}")
        
        return True
        
    except Exception as e:
        print_error(f"Failed to post Discord updates: {e}")
        return False

def show_usage_examples():
    """Show usage examples for the Memory Manager."""
    print("\n🧠 Memory Manager Usage Examples:")
    print("=" * 40)
    
    print("""
# Initialize Memory Manager
from dreamscape.core.memory_manager import MemoryManager

with MemoryManager("dreamos_memory.db") as memory:
    # Search for relevant conversations
    context = memory.get_context_window("python web scraping", limit=3)
    
    # Get specific conversation
    conv = memory.get_conversation_by_id("conversation_id")
    
    # Get recent conversations
    recent = memory.get_recent_conversations(limit=10)
    
    # Get statistics
    stats = memory.get_conversation_stats()
    """)

def main():
    """Main function."""
    print_header("Unified Conversation Manager")
    
    print("This script can:")
    print("1. Ingest new conversations from data/conversations/")
    print("2. Process existing conversations with AI analysis and MMORPG updates")
    print("3. Both ingest and process in one workflow")
    
    # Ask user what they want to do
    print("\n📋 What would you like to do?")
    print("1. Ingest new conversations only")
    print("2. Process existing conversations only")
    print("3. Ingest AND process (full workflow)")
    print("4. Check conversation status only")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        # Ingest only
        success, count = ingest_conversations_from_files()
        if success:
            print_success(f"Ingestion complete! {count} conversations added.")
            show_usage_examples()
        else:
            print_error("Ingestion failed")
        return
    
    elif choice == "2":
        # Process only
        conversations, unprocessed, with_content = check_conversation_status()
        
        if not conversations:
            print_error("Failed to load conversations")
            return
        
        if not unprocessed:
            print_warning("No conversations need processing")
            return
        
        # Ask for confirmation
        print(f"\n📊 Summary:")
        print(f"   Total conversations: {len(conversations)}")
        print(f"   To process: {len(unprocessed)}")
        print(f"   With content: {len(with_content)}")
        
        confirm = input(f"\nProcess {len(unprocessed)} conversations? (y/N): ").strip().lower()
        if confirm != 'y':
            print_info("Processing cancelled")
            return
        
        # Ask for limit
        limit_input = input(f"Process all {len(unprocessed)} or limit? (all/limit): ").strip().lower()
        limit = None
        if limit_input == 'limit':
            try:
                limit = int(input("Enter limit: "))
            except ValueError:
                limit = 10
        
        # Ask about first ingestion override
        if len(unprocessed) > 10:
            override_input = input(f"Override daily XP limits for first ingestion? (y/N): ").strip().lower()
            override_daily_limits = override_input == 'y'
            if override_daily_limits:
                print_info("Daily XP limits will be overridden for this processing run")
        else:
            override_daily_limits = False
        
        # Process conversations
        processed_count, failed_count = process_conversations(unprocessed, limit, override_daily_limits)
        
        if processed_count > 0:
            # Update MMORPG state
            update_mmorpg_state()
            
            # Post Discord updates
            post_discord_updates()
            
            print_success(f"Successfully processed {processed_count} conversations!")
            print_info("Run 'python scripts/track_mmorpg_progress.py' to see updated progress")
        else:
            print_warning("No conversations were processed successfully")
    
    elif choice == "3":
        # Full workflow: Ingest AND process
        print_info("Starting full workflow: Ingest + Process")
        
        # Step 1: Ingest
        success, count = ingest_conversations_from_files()
        if not success:
            print_error("Ingestion failed, stopping workflow")
            return
        
        print_success(f"Ingested {count} conversations")
        
        # Step 2: Check status
        conversations, unprocessed, with_content = check_conversation_status()
        
        if not conversations:
            print_error("Failed to load conversations after ingestion")
            return
        
        if not unprocessed:
            print_warning("No conversations need processing after ingestion")
            return
        
        # Step 3: Process
        print(f"\n📊 Processing Summary:")
        print(f"   Total conversations: {len(conversations)}")
        print(f"   To process: {len(unprocessed)}")
        print(f"   With content: {len(with_content)}")
        
        confirm = input(f"\nProcess {len(unprocessed)} conversations? (y/N): ").strip().lower()
        if confirm != 'y':
            print_info("Processing cancelled")
            return
        
        # For full workflow, always override daily limits
        override_daily_limits = True
        print_info("Daily XP limits will be overridden for full workflow")
        
        # Process conversations
        processed_count, failed_count = process_conversations(unprocessed, None, override_daily_limits)
        
        if processed_count > 0:
            # Update MMORPG state
            update_mmorpg_state()
            
            # Post Discord updates
            post_discord_updates()
            
            print_success(f"Full workflow complete! Processed {processed_count} conversations!")
            print_info("Run 'python scripts/track_mmorpg_progress.py' to see updated progress")
        else:
            print_warning("No conversations were processed successfully")
    
    elif choice == "4":
        # Check status only
        conversations, unprocessed, with_content = check_conversation_status()
        
        if conversations:
            print_success("Status check complete")
            print_info("Use option 2 or 3 to process conversations")
        else:
            print_error("Failed to check conversation status")
    
    else:
        print_error("Invalid choice. Please run the script again and select 1-4.")

if __name__ == "__main__":
    main() 