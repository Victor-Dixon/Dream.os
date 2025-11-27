#!/usr/bin/env python3
"""
Verify Conversation Content Script
Checks that the 'content' field in the conversations table is populated for all conversations.
"""
import sqlite3
from pathlib import Path

def main():
    db_path = Path('dreamos_memory.db')
    if not db_path.exists():
        print(f"❌ Database not found: {db_path}")
        return
    
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()
    cur.execute("SELECT id, title, content FROM conversations")
    rows = cur.fetchall()
    total = len(rows)
    empty = [r for r in rows if not r[2] or not r[2].strip()]
    non_empty = total - len(empty)
    print(f"\n📊 Total conversations: {total}")
    print(f"✅ Non-empty content: {non_empty}")
    print(f"❌ Empty content: {len(empty)}")
    if empty:
        print("\nExamples of conversations with empty content:")
        for r in empty[:5]:
            print(f"- ID: {r[0]}, Title: {r[1]}")
    conn.close()

if __name__ == "__main__":
    main() 