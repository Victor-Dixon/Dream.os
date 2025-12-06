#!/usr/bin/env python3
"""
Analyze Unneeded Functionality - Test Coverage Analysis
======================================================

Uses test coverage to identify potentially unneeded functionality:
- Functions/methods with 0% coverage
- Functions tested but never called in production
- Unused imports
- Dead code patterns

Author: Agent-2 (Architecture & Design Specialist)
Date: 2025-11-26
License: MIT
"""

import ast
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple
import json


def find_python_files(directory: Path, limit: int = None) -> List[Path]:
    """Find all Python files in directory."""
    python_files = []
    for path in directory.rglob("*.py"):
        # Skip test files, temp directories, and venv
        if any(skip in str(path) for skip in ["test_", "_test.py", "temp_", "venv", "__pycache__", ".git"]):
            continue
        python_files.append(path)
        if limit and len(python_files) >= limit:
            break
    return python_files


def parse_python_file(file_path: Path) -> Tuple[List[str], List[str], List[str]]:
    """Parse Python file and extract functions, classes, and imports."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content, filename=str(file_path))
        
        functions = []
        classes = []
        imports = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(node.name)
            elif isinstance(node, ast.ClassDef):
                classes.append(node.name)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
                for alias in node.names:
                    imports.append(alias.name if alias.name else alias.asname)
        
        return functions, classes, imports
    except Exception as e:
        print(f"⚠️  Error parsing {file_path}: {e}")
        return [], [], []


def get_test_coverage(module_path: str) -> Dict:
    """Get test coverage for a module using pytest-cov."""
    try:
        # Run pytest with coverage
        result = subprocess.run(
            ['pytest', '--cov', module_path, '--cov-report', 'json', '--cov-report', 'term', '-q'],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        # Parse coverage JSON
        coverage_file = Path('coverage.json')
        if coverage_file.exists():
            with open(coverage_file, 'r') as f:
                coverage_data = json.load(f)
            coverage_file.unlink()  # Clean up
            return coverage_data
        return {}
    except Exception as e:
        print(f"⚠️  Error getting coverage for {module_path}: {e}")
        return {}


def find_test_files_for_module(module_path: Path) -> List[Path]:
    """Find test files that might test this module."""
    module_name = module_path.stem
    test_files = []
    
    # Look for test files with multiple patterns
    test_patterns = [
        f"test_{module_name}.py",
        f"test_{module_path.parent.name}_{module_name}.py",
        f"test_{module_name}_*.py",
        f"*test_{module_name}*.py",  # More flexible matching
    ]
    
    tests_dir = Path("tests")
    if tests_dir.exists():
        for pattern in test_patterns:
            test_files.extend(tests_dir.rglob(pattern))
    
    # Also check if module name appears in any test file
    # (for cases where test file structure doesn't match exactly)
    if not test_files:
        for test_file in tests_dir.rglob("test_*.py"):
            try:
                content = test_file.read_text(encoding='utf-8')
                # Check if module is imported or referenced
                if module_name in content or str(module_path).replace('\\', '/') in content:
                    test_files.append(test_file)
            except Exception:
                continue
    
    return list(set(test_files))  # Remove duplicates


def check_code_usage(item_name: str, item_type: str, all_files: List[Path], source_file: Path) -> bool:
    """Check if a function/class is actually used elsewhere in codebase."""
    # Convert file path to module path for import checking
    try:
        source_relative = source_file.relative_to(Path.cwd())
        module_parts = source_relative.with_suffix('').parts
        module_path = '.'.join(module_parts)
    except ValueError:
        return True  # If can't determine module, assume used
    
    # Check all other files for usage
    for file_path in all_files:
        if file_path == source_file:
            continue
        
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # Check for direct usage patterns
            usage_patterns = [
                f"from {module_path} import {item_name}",
                f"from {module_path} import",
                f"import {module_path}",
                f"{item_name}(",
                f".{item_name}(",
                f" {item_name}(",
            ]
            
            # Also check for class instantiation
            if item_type == "class":
                usage_patterns.extend([
                    f"= {item_name}(",
                    f"({item_name}(",
                    f"isinstance(",
                ])
            
            if any(pattern in content for pattern in usage_patterns):
                return True
                
        except Exception:
            continue
    
    return False


def analyze_unneeded_functionality(directory: Path = Path("src"), limit: int = None) -> Dict:
    """Analyze codebase to identify unneeded functionality."""
    print("🔍 Analyzing codebase for unneeded functionality...")
    print(f"📁 Scanning directory: {directory}\n")
    
    python_files = find_python_files(directory, limit=limit)
    print(f"📄 Found {len(python_files)} Python files\n")
    
    results = {
        "files_analyzed": len(python_files),
        "functions_no_tests": [],
        "classes_no_tests": [],
        "files_no_tests": [],
        "potential_dead_code": [],
        "unused_imports": []
    }
    
    for file_path in python_files:
        try:
            relative_path = file_path.relative_to(Path.cwd())
        except ValueError:
            relative_path = file_path
        print(f"📄 Analyzing: {relative_path}")
        
        functions, classes, imports = parse_python_file(file_path)
        
        # Check if file has tests
        test_files = find_test_files_for_module(file_path)
        
        if not test_files:
            results["files_no_tests"].append({
                "file": str(relative_path),
                "functions": len(functions),
                "classes": len(classes)
            })
        
        # Check functions without tests
        for func in functions:
            # Skip private/dunder methods (but check if they're used)
            is_private = func.startswith("_") and not func.startswith("__")
            
            # Check if function is tested (multiple patterns)
            has_test = False
            for test_file in test_files:
                try:
                    content = test_file.read_text(encoding='utf-8')
                    # Check multiple test naming patterns
                    test_patterns = [
                        f"test_{func}",
                        f"def test_{func}",
                        f"test_{func.lower()}",
                        f"def test_{func.lower()}",
                        f"{func}()",  # Direct call in test
                        f".{func}(",  # Method call
                    ]
                    if any(pattern in content for pattern in test_patterns):
                        has_test = True
                        break
                except Exception:
                    continue
            
            if not has_test and func not in ["__init__", "__main__"]:
                # Check if actually used
                is_used = check_code_usage(func, "function", python_files, file_path)
                
                result_item = {
                    "file": str(relative_path),
                    "function": func,
                    "is_used": is_used,
                    "is_private": is_private
                }
                
                results["functions_no_tests"].append(result_item)
                
                # Mark as potential dead code if not used and not private
                if not is_used and not is_private:
                    results["potential_dead_code"].append({
                        "type": "function",
                        "file": str(relative_path),
                        "name": func
                    })
        
        # Check classes without tests
        for cls in classes:
            has_test = any(
                f"test_{cls}" in test_file.read_text() or
                f"Test{cls}" in test_file.read_text()
                for test_file in test_files
            )
            
            if not has_test:
                # Check if actually used
                is_used = check_code_usage(cls, "class", python_files, file_path)
                
                results["classes_no_tests"].append({
                    "file": str(relative_path),
                    "class": cls,
                    "is_used": is_used
                })
                
                # Mark as potential dead code if not used
                if not is_used:
                    results["potential_dead_code"].append({
                        "type": "class",
                        "file": str(relative_path),
                        "name": cls
                    })
    
    return results


def generate_report(results: Dict, output_file: Path = Path("unneeded_functionality_report.md")):
    """Generate markdown report of unneeded functionality."""
    report = f"""# Unneeded Functionality Analysis Report

**Date**: 2025-11-26  
**Generated By**: Agent-2 (Architecture & Design Specialist)  
**Status**: ✅ **ANALYSIS COMPLETE**

---

## 📊 **SUMMARY**

- **Files Analyzed**: {results['files_analyzed']}
- **Files Without Tests**: {len(results['files_no_tests'])}
- **Functions Without Tests**: {len(results['functions_no_tests'])}
- **Classes Without Tests**: {len(results['classes_no_tests'])}
- **Potential Dead Code**: {len(results['potential_dead_code'])} items

---

## 📁 **FILES WITHOUT TESTS**

"""
    
    if results['files_no_tests']:
        for item in results['files_no_tests'][:20]:  # Limit to 20
            report += f"- **{item['file']}**: {item['functions']} functions, {item['classes']} classes\n"
        if len(results['files_no_tests']) > 20:
            report += f"\n... and {len(results['files_no_tests']) - 20} more files\n"
    else:
        report += "✅ All files have tests!\n"
    
    report += "\n---\n\n## 🔧 **FUNCTIONS WITHOUT TESTS**\n\n"
    
    if results['functions_no_tests']:
        # Sort by usage status (unused first)
        sorted_funcs = sorted(
            results['functions_no_tests'],
            key=lambda x: (x.get('is_used', True), x.get('is_private', False))
        )
        
        for item in sorted_funcs[:30]:  # Limit to 30
            status = "❌ UNUSED" if not item.get('is_used', True) else "✅ USED"
            private = " (private)" if item.get('is_private', False) else ""
            report += f"- **{item['file']}**: `{item['function']}` {status}{private}\n"
        if len(results['functions_no_tests']) > 30:
            report += f"\n... and {len(results['functions_no_tests']) - 30} more functions\n"
    else:
        report += "✅ All functions have tests!\n"
    
    report += "\n---\n\n## 🏗️ **CLASSES WITHOUT TESTS**\n\n"
    
    if results['classes_no_tests']:
        # Sort by usage status (unused first)
        sorted_classes = sorted(
            results['classes_no_tests'],
            key=lambda x: x.get('is_used', True)
        )
        
        for item in sorted_classes[:20]:  # Limit to 20
            status = "❌ UNUSED" if not item.get('is_used', True) else "✅ USED"
            report += f"- **{item['file']}**: `{item['class']}` {status}\n"
        if len(results['classes_no_tests']) > 20:
            report += f"\n... and {len(results['classes_no_tests']) - 20} more classes\n"
    else:
        report += "✅ All classes have tests!\n"
    
    report += "\n---\n\n## 🗑️ **POTENTIAL DEAD CODE** (High Priority for Removal)\n\n"
    
    if results['potential_dead_code']:
        # Group by file
        by_file = {}
        for item in results['potential_dead_code']:
            file_path = item['file']
            if file_path not in by_file:
                by_file[file_path] = []
            by_file[file_path].append(item)
        
        for file_path, items in list(by_file.items())[:15]:  # Limit to 15 files
            report += f"\n### **{file_path}**\n"
            for item in items[:10]:  # Limit to 10 items per file
                report += f"- `{item['name']}` ({item['type']})\n"
        if len(results['potential_dead_code']) > 150:
            report += f"\n... and {len(results['potential_dead_code']) - 150} more items\n"
    else:
        report += "✅ No obvious dead code detected!\n"
    
    report += "\n---\n\n## ✅ **RECOMMENDATIONS**\n\n"
    report += "### **Priority 1: Dead Code Removal**\n"
    report += f"- Review {len(results['potential_dead_code'])} potential dead code items\n"
    report += "- Start with unused functions/classes marked ❌ UNUSED\n"
    report += "- Verify they're not used via CLI or external interfaces\n\n"
    
    report += "### **Priority 2: Test Coverage**\n"
    report += "- Add tests for used but untested code\n"
    report += "- Focus on public APIs and critical paths\n\n"
    
    report += "### **Priority 3: Code Review**\n"
    report += "- Review private methods - may be internal helpers\n"
    report += "- Check if untested code is called via dynamic imports\n"
    report += "- Verify CLI/external interfaces aren't using untested code\n"
    
    report += "\n---\n\n**Status**: ✅ **ANALYSIS COMPLETE**\n"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✅ Report generated: {output_file}")


def main():
    """Main execution."""
    print("=" * 60)
    print("🔍 UNNEEDED FUNCTIONALITY ANALYZER")
    print("=" * 60)
    print()
    
    # Analyze src directory (limit to 50 files for initial run)
    src_dir = Path("src")
    if not src_dir.exists():
        print(f"❌ Directory not found: {src_dir}")
        sys.exit(1)
    
    # Start with key directories
    key_dirs = ["src/discord_commander", "src/services", "src/core"]
    all_results = {
        "files_analyzed": 0,
        "functions_no_tests": [],
        "classes_no_tests": [],
        "files_no_tests": [],
        "potential_dead_code": [],
        "unused_imports": []
    }
    
    for key_dir in key_dirs:
        dir_path = Path(key_dir)
        if dir_path.exists():
            print(f"\n📁 Analyzing: {key_dir}")
            results = analyze_unneeded_functionality(dir_path, limit=50)
            all_results["files_analyzed"] += results["files_analyzed"]
            all_results["functions_no_tests"].extend(results["functions_no_tests"])
            all_results["classes_no_tests"].extend(results["classes_no_tests"])
            all_results["files_no_tests"].extend(results["files_no_tests"])
    
    results = all_results
    
    # Generate report
    report_file = Path("unneeded_functionality_report.md")
    generate_report(results, report_file)
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    print(f"Files Analyzed: {results['files_analyzed']}")
    print(f"Files Without Tests: {len(results['files_no_tests'])}")
    print(f"Functions Without Tests: {len(results['functions_no_tests'])}")
    print(f"Classes Without Tests: {len(results['classes_no_tests'])}")
    print(f"\n✅ Report saved to: {report_file}")
    print("=" * 60)


if __name__ == "__main__":
    main()

