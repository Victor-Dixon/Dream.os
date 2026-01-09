#!/usr/bin/env python3
"""
Custom Conversation File Ingestion Script
========================================

Handles the specific format of conversation JSON files in data/conversations/
"""

import sys
import json
import logging
from pathlib import Path
from datetime import datetime

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# EDIT START: Consolidate memory imports to use memory_system (core consolidation)
from dreamscape.core.memory import MemoryManager
# EDIT END

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def ingest_conversation_files():
    """Ingest conversation files from data/conversations/ directory."""
    conversations_dir = Path("data/conversations")
    
    if not conversations_dir.exists():
        print("❌ Conversations directory not found")
        return False
    
    # Find all JSON files (excluding extraction summaries)
    json_files = [f for f in conversations_dir.glob("*.json") 
                  if not f.name.startswith("extraction_summary")]
    
    print(f"📁 Found {len(json_files)} conversation files to ingest")
    
    if not json_files:
        print("❌ No conversation files found")
        return False
    
    # Initialize memory manager
    memory_manager = MemoryManager("dreamos_memory.db")
    
    ingested_count = 0
    errors = []
    
    for i, json_file in enumerate(json_files, 1):
        try:
            print(f"📥 Processing: {json_file.name}")
            
            # Read the JSON file
            with open(json_file, 'r', encoding='utf-8') as f:
                conversation_data = json.load(f)
            
            # Extract conversation ID from filename (remove .json extension)
            conversation_id = json_file.stem
            
            # Check if conversation already exists
            existing = memory_manager.get_conversation_by_id(conversation_id)
            if existing:
                print(f"⏭️ Skipping existing: {conversation_data.get('title', 'No title')} (ID: {conversation_id})")
                continue
            
            # Get the actual conversation content
            content = conversation_data.get('full_conversation', conversation_data.get('content', ''))
            
            # Create conversation data structure
            conversation = {
                'id': conversation_id,
                'title': conversation_data.get('title', 'Untitled'),
                'timestamp': datetime.now().isoformat(),
                'captured_at': datetime.now().isoformat(),
                'url': f"https://chat.openai.com/c/{conversation_id}",
                'model': 'gpt-4o',  # Default model
                'content': content,
                'message_count': len(conversation_data.get('messages', [])),
                'word_count': len(content.split()),
                'tags': '',
                'summary': ''
            }
            
            # Store the conversation
            success = memory_manager.store_conversation(conversation)
            if success:
                ingested_count += 1
                print(f"✅ Ingested: {conversation['title']}")
            else:
                errors.append(f"Failed to store {conversation_id}")
                print(f"❌ Failed to store: {conversation['title']}")
            
            # Progress update every 10 files
            if i % 10 == 0:
                print(f"📊 Progress: {i}/{len(json_files)} files processed")
                
        except Exception as e:
            error_msg = f"Failed to ingest {json_file.name}: {str(e)}"
            errors.append(error_msg)
            print(f"❌ {error_msg}")
            continue
    
    # Close memory manager
    memory_manager.close()
    
    # Print summary
    print(f"\n🎉 Ingestion completed!")
    print(f"✅ Successfully ingested: {ingested_count} conversations")
    print(f"❌ Errors: {len(errors)}")
    
    if errors:
        print("\nError details:")
        for error in errors[:10]:  # Show first 10 errors
            print(f"  - {error}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more errors")
    
    return ingested_count > 0

if __name__ == "__main__":
    success = ingest_conversation_files()
    sys.exit(0 if success else 1)
