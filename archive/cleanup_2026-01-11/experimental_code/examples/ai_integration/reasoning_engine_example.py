#!/usr/bin/env python3
"""
AI Reasoning Integration Example
"""

import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from ai_training.dreamvault.advanced_reasoning import AdvancedReasoningEngine

def main():
    engine = AdvancedReasoningEngine()

    # Example reasoning request
    result = engine.reason(
        query="Analyze the benefits of swarm coordination",
        mode="strategic"
    )

    print("Reasoning Result:")
    print(f"Response: {result.get('response', 'No response')}")
    print(f"Confidence: {result.get('confidence', 'N/A')}")
    print(f"Mode: {result.get('mode', 'N/A')}")

if __name__ == "__main__":
    main()
