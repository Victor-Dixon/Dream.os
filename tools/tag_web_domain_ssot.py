#!/usr/bin/env python3
"""
SSOT Tagging Tool - Web Domain Batch 7
Tags all Python files in src/web/ with SSOT domain tag.
"""

import os
import re
from pathlib import Path

SSOT_TAG = "<!-- SSOT Domain: web -->"
WEB_DIR = Path("src/web")


def has_ssot_tag(content: str) -> bool:
    """Check if file already has SSOT tag."""
    return SSOT_TAG in content


def add_ssot_tag_to_file(file_path: Path) -> bool:
    """Add SSOT tag to a Python file. Returns True if tag was added."""
    try:
        content = file_path.read_text(encoding="utf-8")
        
        # Skip if already tagged
        if has_ssot_tag(content):
            return False
        
        # Pattern 1: File starts with module docstring (triple quotes)
        # Add tag after opening docstring
        pattern1 = r'^(""")(.*?)(\n)'
        match1 = re.match(pattern1, content, re.DOTALL)
        if match1:
            # Has docstring starting at line 1
            docstring_content = match1.group(2)
            # Add tag after first line or at start of docstring
            if "\n" in docstring_content:
                # Multi-line docstring: add tag after first line
                new_content = re.sub(
                    r'^(""")(.*?\n)(.*)',
                    rf'\1\2{SSOT_TAG}\n\3',
                    content,
                    flags=re.DOTALL
                )
            else:
                # Single-line docstring: add tag after description
                new_content = re.sub(
                    r'^(""")(.*?)(""")',
                    rf'\1\2\n\n{SSOT_TAG}\n\3',
                    content,
                    flags=re.DOTALL
                )
            file_path.write_text(new_content, encoding="utf-8")
            return True
        
        # Pattern 2: File starts with single-line docstring
        pattern2 = r'^(""")([^"]+)(""")'
        match2 = re.match(pattern2, content)
        if match2:
            new_content = re.sub(
                r'^(""")([^"]+)(""")',
                rf'\1\2\n\n{SSOT_TAG}\n\3',
                content
            )
            file_path.write_text(new_content, encoding="utf-8")
            return True
        
        # Pattern 3: No docstring - add one at the top
        if not content.strip().startswith('"""'):
            # Check if file starts with imports or other code
            lines = content.split("\n")
            insert_pos = 0
            
            # Skip shebang and encoding declarations
            if lines and lines[0].startswith("#!"):
                insert_pos = 1
            if lines and insert_pos < len(lines) and lines[insert_pos].startswith("# -*-"):
                insert_pos += 1
            
            # Insert docstring with SSOT tag
            docstring = f'"""{SSOT_TAG}\n"""\n'
            lines.insert(insert_pos, docstring)
            new_content = "\n".join(lines)
            file_path.write_text(new_content, encoding="utf-8")
            return True
        
        # Pattern 4: Docstring exists but not at start - add tag after first docstring
        pattern4 = r'(""")(.*?)(""")'
        match4 = re.search(pattern4, content, re.DOTALL)
        if match4:
            docstring_content = match4.group(2)
            if SSOT_TAG not in docstring_content:
                # Add tag to existing docstring
                new_docstring = f'{match4.group(1)}{docstring_content}\n\n{SSOT_TAG}\n{match4.group(3)}'
                new_content = content.replace(match4.group(0), new_docstring)
                file_path.write_text(new_content, encoding="utf-8")
                return True
        
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False


def main():
    """Tag all Python files in src/web/ directory."""
    web_path = Path(WEB_DIR)
    if not web_path.exists():
        print(f"Error: {web_path} does not exist")
        return
    
    python_files = list(web_path.rglob("*.py"))
    print(f"Found {len(python_files)} Python files in {web_path}")
    
    tagged_count = 0
    skipped_count = 0
    error_count = 0
    
    for file_path in sorted(python_files):
        # Skip __pycache__ directories
        if "__pycache__" in str(file_path):
            continue
        
        if has_ssot_tag(file_path.read_text(encoding="utf-8")):
            print(f"⏭️  Skipped (already tagged): {file_path}")
            skipped_count += 1
            continue
        
        if add_ssot_tag_to_file(file_path):
            print(f"✅ Tagged: {file_path}")
            tagged_count += 1
        else:
            print(f"❌ Failed: {file_path}")
            error_count += 1
    
    print(f"\n📊 Summary:")
    print(f"   Tagged: {tagged_count}")
    print(f"   Skipped (already tagged): {skipped_count}")
    print(f"   Errors: {error_count}")
    print(f"   Total: {len(python_files)}")


if __name__ == "__main__":
    main()

