#!/usr/bin/env python3
"""
Test Mermaid Discord Renderer
=============================

Tests the Mermaid renderer functionality.
Author: Agent-4 (Captain)
Date: 2025-11-26
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.discord_mermaid_renderer import DiscordMermaidRenderer


def test_mermaid_extraction():
    """Test Mermaid diagram extraction."""
    print("🧪 Testing Mermaid Diagram Extraction\n")
    
    renderer = DiscordMermaidRenderer()
    
    test_content = """
# Test Document

Here's a simple diagram:

```mermaid
graph TD
    A[Start] --> B[Process]
    B --> C[End]
```

More content here.

Another diagram:

```mermaid
sequenceDiagram
    Alice->>Bob: Hello
    Bob-->>Alice: Hi
```
"""
    
    diagrams = renderer.extract_mermaid_diagrams(test_content)
    
    print(f"📊 Found {len(diagrams)} Mermaid diagrams")
    
    for i, (diagram_code, pos) in enumerate(diagrams, 1):
        print(f"\n{i}. Diagram at position {pos}:")
        print(f"   Code preview: {diagram_code[:50]}...")
    
    assert len(diagrams) == 2, f"Expected 2 diagrams, found {len(diagrams)}"
    print("\n✅ Extraction test passed!")
    
    return diagrams


def test_mermaid_rendering():
    """Test Mermaid diagram rendering."""
    print("\n🧪 Testing Mermaid Diagram Rendering\n")
    
    renderer = DiscordMermaidRenderer()
    
    simple_diagram = """graph TD
    A[Start] --> B[Process]
    B --> C[End]"""
    
    print("📸 Rendering diagram to image URL...")
    image_url = renderer.render_mermaid_to_image_url(simple_diagram)
    
    if image_url:
        print(f"✅ Success! Image URL: {image_url[:80]}...")
        return True
    else:
        print("❌ Failed to render diagram")
        return False


def test_mermaid_file_save():
    """Test saving Mermaid diagram to file."""
    print("\n🧪 Testing Mermaid Diagram File Save\n")
    
    renderer = DiscordMermaidRenderer()
    
    simple_diagram = """graph TD
    A[Start] --> B[Process]
    B --> C[End]"""
    
    output_path = Path("temp/test_mermaid.png")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"💾 Saving diagram to: {output_path}")
    success = renderer.render_mermaid_to_file(simple_diagram, output_path)
    
    if success and output_path.exists():
        size = output_path.stat().st_size
        print(f"✅ Success! File saved ({size} bytes)")
        return True
    else:
        print("❌ Failed to save file")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("🔧 MERMAID RENDERER TEST SUITE")
    print("=" * 60)
    
    try:
        # Test 1: Extraction
        diagrams = test_mermaid_extraction()
        
        # Test 2: Rendering
        render_success = test_mermaid_rendering()
        
        # Test 3: File save
        file_success = test_mermaid_file_save()
        
        print("\n" + "=" * 60)
        print("📊 TEST RESULTS")
        print("=" * 60)
        print(f"Extraction: ✅ Passed ({len(diagrams)} diagrams)")
        print(f"Rendering: {'✅ Passed' if render_success else '❌ Failed'}")
        print(f"File Save: {'✅ Passed' if file_success else '❌ Failed'}")
        
        if render_success and file_success:
            print("\n🎉 All tests passed!")
            return 0
        else:
            print("\n⚠️ Some tests failed - check implementation")
            return 1
            
    except Exception as e:
        print(f"\n❌ Test error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())



