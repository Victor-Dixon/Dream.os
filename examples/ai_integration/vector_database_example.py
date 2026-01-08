#!/usr/bin/env python3
"""
Vector Database Integration Example
"""

import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from services.vector.vector_database_service import VectorDatabaseService

def main():
    # Initialize vector database service
    vdb = VectorDatabaseService()

    # Example semantic search
    try:
        results = vdb.semantic_search(
            query="coordination patterns",
            limit=5
        )

        print("Semantic Search Results:")
        for i, result in enumerate(results, 1):
            print(f"{i}. {result.content[:100]}... (score: {result.score:.3f})")

    except Exception as e:
        print(f"Vector search example failed: {e}")
        print("Note: This requires actual vector database setup")

if __name__ == "__main__":
    main()
