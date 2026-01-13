#!/usr/bin/env python3
"""
Run Canon Extraction
=====================

Simple wrapper script to run canon extraction and display results.

Usage:
    python scripts/run_canon_extraction.py
"""

import sys
from pathlib import Path

# Add tools to path
sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

from canon_automation import CanonExtractor

def main():
    """Run canon extraction and display summary."""
    root_dir = Path(__file__).parent.parent
    workspaces_dir = root_dir / "agent_workspaces"
    output_file = root_dir / "reports" / "canon_extraction.json"
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    extractor = CanonExtractor(workspaces_dir)
    result = extractor.run_extraction(output_file)
    
    if result == 0:
        print("\n" + "="*60)
        print("📋 CANON EXTRACTION COMPLETE")
        print("="*60)
        print(f"\n✅ Results saved to: {output_file}")
        print("\n💡 Next steps:")
        print("   1. Review canon candidates in the JSON file")
        print("   2. Acknowledge canon-worthy events")
        print("   3. Thea will process and declare canon")
        print("   4. Events will be added to CANON_EVENTS.md")
        print("\n" + "="*60 + "\n")
    
    return result

if __name__ == "__main__":
    sys.exit(main())

