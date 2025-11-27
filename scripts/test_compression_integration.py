#!/usr/bin/env python3
"""
Test Compression Integration
============================

Tests MessageRepository compression integration with Agent-3's tools.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.repositories.message_repository import MessageRepository

def test_compression_integration():
    """Test compression integration."""
    print("=" * 60)
    print("Compression Integration Test")
    print("=" * 60)
    
    repo = MessageRepository()
    
    # Test compression stats
    print("\n1. Testing get_compression_stats()...")
    stats = repo.get_compression_stats()
    if stats.get("success"):
        print(f"   ✅ Compression stats retrieved")
        print(f"   Stats: {stats.get('stats', 'N/A')[:100]}...")
    else:
        print(f"   ⚠️  Stats retrieval failed: {stats.get('error', 'Unknown')}")
    
    # Test compression (dry run would be safer, but tool doesn't support it via subprocess easily)
    print("\n2. Testing compress_old_messages()...")
    result = repo.compress_old_messages(days=7)
    if result.get("success"):
        print(f"   ✅ Compression tool executed")
        print(f"   Output: {result.get('output', 'N/A')[:100]}...")
    else:
        print(f"   ⚠️  Compression failed: {result.get('error', 'Unknown')}")
    
    print("\n" + "=" * 60)
    print("Integration Test Complete")
    print("=" * 60)
    
    return stats.get("success", False) or result.get("success", False)

if __name__ == "__main__":
    success = test_compression_integration()
    exit(0 if success else 1)




