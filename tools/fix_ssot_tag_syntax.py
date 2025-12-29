#!/usr/bin/env python3
"""Fix SSOT tags that are outside docstrings causing syntax errors."""

import re
from pathlib import Path

def fix_ssot_tag_in_file(filepath: Path) -> bool:
    """Fix SSOT tag placement in a file."""
    try:
        content = filepath.read_text(encoding='utf-8')
        original = content
        
        # Pattern: SSOT tag at start of file (before any docstring)
        pattern = r'^(<!-- SSOT Domain: [^>]+ -->)\s*\n'
        
        if re.match(pattern, content):
            # Find first docstring or create one
            lines = content.split('\n')
            ssot_tag = None
            new_lines = []
            in_docstring = False
            docstring_start = -1
            
            for i, line in enumerate(lines):
                if line.strip().startswith('<!-- SSOT Domain:'):
                    ssot_tag = line.strip()
                    continue
                
                if '"""' in line or "'''" in line:
                    if not in_docstring:
                        in_docstring = True
                        docstring_start = i
                        new_lines.append(line)
                        # Add SSOT tag after opening docstring
                        if ssot_tag and i == docstring_start:
                            # Check if next line is empty or has content
                            if i + 1 < len(lines) and lines[i + 1].strip():
                                new_lines.append('')
                                new_lines.append(ssot_tag)
                            else:
                                new_lines.append(ssot_tag)
                        continue
                    else:
                        in_docstring = False
                
                new_lines.append(line)
            
            # If no docstring found, create one at the top
            if ssot_tag and docstring_start == -1:
                # Check if file starts with shebang
                if lines and lines[0].startswith('#!'):
                    new_lines = [lines[0], '', '"""', ssot_tag, '"""', ''] + lines[1:]
                else:
                    new_lines = ['"""', ssot_tag, '"""', ''] + lines
            
            content = '\n'.join(new_lines)
        
        if content != original:
            filepath.write_text(content, encoding='utf-8')
            return True
        return False
    except Exception as e:
        print(f"Error fixing {filepath}: {e}")
        return False

def main():
    """Fix all Python files in src/."""
    src_dir = Path('src')
    fixed_count = 0
    
    for py_file in src_dir.rglob('*.py'):
        if fix_ssot_tag_in_file(py_file):
            print(f"Fixed: {py_file}")
            fixed_count += 1
    
    print(f"\nFixed {fixed_count} files")

if __name__ == '__main__':
    main()

