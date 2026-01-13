#!/usr/bin/env python3
"""Generate orphan imports manifest"""

import os
import ast
import json
import sys

def find_orphaned_imports():
    """Find imports that reference non-existent modules"""
    results = []

    for root, dirs, files in os.walk('src'):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        tree = ast.parse(content)
                        for node in ast.walk(tree):
                            if isinstance(node, ast.Import):
                                for alias in node.names:
                                    module_name = alias.name.split('.')[0]
                                    module_path = os.path.join('src', module_name + '.py')
                                    # Check if it's a relative import or absolute
                                    if not os.path.exists(module_path):
                                        # Check subdirectories
                                        subdir_path = os.path.join('src', module_name)
                                        if not os.path.exists(subdir_path):
                                            results.append({
                                                'file': filepath,
                                                'import': module_name,
                                                'line': node.lineno,
                                                'type': 'absolute_import'
                                            })
                            elif isinstance(node, ast.ImportFrom):
                                if node.module:
                                    module_parts = node.module.split('.')
                                    base_module = module_parts[0]

                                    # Check if base module exists
                                    module_path = os.path.join('src', base_module + '.py')
                                    subdir_path = os.path.join('src', base_module)

                                    if not os.path.exists(module_path) and not os.path.exists(subdir_path):
                                        results.append({
                                            'file': filepath,
                                            'import': node.module,
                                            'line': node.lineno,
                                            'type': 'from_import'
                                        })
                except Exception as e:
                    # Skip files with parse errors
                    continue

    return results

if __name__ == "__main__":
    orphans = find_orphaned_imports()
    with open('audit_outputs/orphan_imports.json', 'w') as f:
        json.dump(orphans, f, indent=2)
    print(f"Generated orphan imports manifest: {len(orphans)} orphaned imports found")
    for orphan in orphans[:5]:  # Show first 5
        print(f"  - {orphan['file']}:{orphan['line']} imports {orphan['import']}")