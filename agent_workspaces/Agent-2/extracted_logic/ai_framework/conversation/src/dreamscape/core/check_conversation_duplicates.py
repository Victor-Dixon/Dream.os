#!/usr/bin/env python3
"""
Conversation Duplicate Checker 🔍
================================

Check for and handle duplicate conversations in the database.
This script identifies duplicates based on conversation ID, URL, or content hash.

Usage:
    python scripts/check_conversation_duplicates.py --check     # Just check for duplicates
    python scripts/check_conversation_duplicates.py --remove    # Remove duplicates
    python scripts/check_conversation_duplicates.py --report    # Generate detailed report
"""

import sys
import hashlib
import json
from pathlib import Path
from typing import Dict, List, Tuple, Set
from collections import defaultdict

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.dreamscape.core.database_schema_manager import DatabaseSchemaManager
from src.dreamscape.core.conversation_storage import ConversationStorage

def hash_content(content: str) -> str:
    """Generate SHA-256 hash of conversation content."""
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

def check_duplicates() -> Dict[str, List[Dict]]:
    """Check for duplicate conversations in the database."""
    print("🔍 Checking for duplicate conversations...")
    
    # Initialize database connection
    db_manager = DatabaseSchemaManager()
    connection = db_manager.init_database("dreamos_memory.db")
    conversation_storage = ConversationStorage(connection)
    
    # Get all conversations
    conversations = conversation_storage.get_all_conversations()
    print(f"📊 Found {len(conversations)} total conversations")
    
    # Track duplicates by different criteria
    duplicates = {
        'by_id': defaultdict(list),
        'by_url': defaultdict(list),
        'by_content_hash': defaultdict(list),
        'by_title': defaultdict(list)
    }
    
    # Check for duplicates
    for conv in conversations:
        conv_id = conv.get('id')
        url = conv.get('url', '')
        content = conv.get('content', '')
        title = conv.get('title', '')
        
        # By ID
        if conv_id:
            duplicates['by_id'][conv_id].append(conv)
        
        # By URL
        if url:
            duplicates['by_url'][url].append(conv)
        
        # By content hash
        if content:
            content_hash = hash_content(content)
            duplicates['by_content_hash'][content_hash].append(conv)
        
        # By title (case insensitive)
        if title:
            title_lower = title.lower().strip()
            duplicates['by_title'][title_lower].append(conv)
    
    # Filter to only actual duplicates
    actual_duplicates = {}
    for duplicate_type, groups in duplicates.items():
        actual_duplicates[duplicate_type] = {
            key: convs for key, convs in groups.items() 
            if len(convs) > 1
        }
    
    return actual_duplicates

def print_duplicate_report(duplicates: Dict[str, Dict]):
    """Print a detailed report of duplicates found."""
    print("\n" + "="*60)
    print("📋 DUPLICATE CONVERSATION REPORT")
    print("="*60)
    
    total_duplicates = 0
    
    for duplicate_type, groups in duplicates.items():
        if not groups:
            continue
            
        print(f"\n🔍 Duplicates by {duplicate_type.upper()}:")
        print("-" * 40)
        
        for key, convs in groups.items():
            print(f"\n  Key: {key[:50]}{'...' if len(key) > 50 else ''}")
            print(f"  Count: {len(convs)} conversations")
            
            for i, conv in enumerate(convs, 1):
                conv_id = conv.get('id', 'Unknown')
                title = conv.get('title', 'No Title')[:40]
                url = conv.get('url', 'No URL')[:50]
                message_count = conv.get('message_count', 0)
                word_count = conv.get('word_count', 0)
                
                print(f"    {i}. ID: {conv_id} | Title: {title} | Messages: {message_count} | Words: {word_count}")
                print(f"       URL: {url}")
            
            total_duplicates += len(convs) - 1  # Count extra duplicates
    
    print(f"\n📊 SUMMARY:")
    print(f"   Total duplicate conversations: {total_duplicates}")
    
    duplicate_types = [k for k, v in duplicates.items() if v]
    if duplicate_types:
        print(f"   Duplicate types found: {', '.join(duplicate_types)}")
    else:
        print("   ✅ No duplicates found!")

def remove_duplicates(duplicates: Dict[str, Dict], keep_strategy: str = 'newest') -> int:
    """Remove duplicate conversations from the database."""
    print(f"\n🗑️ Removing duplicates (keeping {keep_strategy})...")
    
    # Initialize database connection
    db_manager = DatabaseSchemaManager()
    connection = db_manager.init_database("dreamos_memory.db")
    conversation_storage = ConversationStorage(connection)
    
    removed_count = 0
    
    for duplicate_type, groups in duplicates.items():
        if not groups:
            continue
            
        print(f"\n  Processing {duplicate_type} duplicates...")
        
        for key, convs in groups.items():
            if len(convs) <= 1:
                continue
                
            # Sort by creation time to determine which to keep
            sorted_convs = sorted(convs, key=lambda x: x.get('created_at', ''), reverse=True)
            
            # Keep the newest (first after reverse sort)
            keep_conv = sorted_convs[0]
            remove_convs = sorted_convs[1:]
            
            print(f"    Keeping: {keep_conv.get('title', 'Unknown')[:40]} (ID: {keep_conv.get('id')})")
            
            # Remove duplicates
            for conv in remove_convs:
                conv_id = conv.get('id')
                if conv_id:
                    try:
                        conversation_storage.delete_conversation(conv_id)
                        removed_count += 1
                        print(f"    Removed: {conv.get('title', 'Unknown')[:40]} (ID: {conv_id})")
                    except Exception as e:
                        print(f"    ❌ Failed to remove {conv_id}: {e}")
    
    print(f"\n✅ Removed {removed_count} duplicate conversations")
    return removed_count

def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Check and handle duplicate conversations")
    parser.add_argument('--check', action='store_true', help='Check for duplicates')
    parser.add_argument('--remove', action='store_true', help='Remove duplicates')
    parser.add_argument('--report', action='store_true', help='Generate detailed report')
    parser.add_argument('--keep', choices=['newest', 'oldest', 'longest'], 
                       default='newest', help='Strategy for keeping duplicates')
    
    args = parser.parse_args()
    
    # Default to check if no action specified
    if not any([args.check, args.remove, args.report]):
        args.check = True
    
    try:
        # Check for duplicates
        duplicates = check_duplicates()
        
        # Print report if requested
        if args.report or args.check:
            print_duplicate_report(duplicates)
        
        # Remove duplicates if requested
        if args.remove:
            # Ask for confirmation
            total_duplicates = sum(len(convs) - 1 for groups in duplicates.values() for convs in groups.values())
            if total_duplicates > 0:
                confirm = input(f"\n⚠️  This will remove {total_duplicates} duplicate conversations. Continue? (y/N): ")
                if confirm.lower() == 'y':
                    removed = remove_duplicates(duplicates, args.keep)
                    print(f"✅ Successfully removed {removed} duplicate conversations")
                else:
                    print("❌ Operation cancelled")
            else:
                print("✅ No duplicates to remove")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 