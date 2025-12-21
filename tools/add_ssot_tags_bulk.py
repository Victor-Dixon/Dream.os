#!/usr/bin/env python3
"""
Bulk SSOT Tag Addition Script - Phase 1 V2 Compliance
=====================================================

<!-- SSOT Domain: tools -->

Adds SSOT domain tags to SIGNAL tools that are missing them.
Only processes SIGNAL tools (filters using TOOL_CLASSIFICATION.json).

Author: Agent-6 (Coordination & Communication Specialist)
Created: 2025-12-21
License: MIT
"""

from __future__ import annotations

import ast
import json
import re
import shutil
from pathlib import Path
from typing import Dict, List, Tuple

# SSOT Domain Mapping Rules
DOMAIN_MAPPING: Dict[str, str] = {
    "tools/communication/": "communication",
    "tools/integration/": "integration",
    "tools/infrastructure/": "infrastructure",
    "tools/web/": "web",
    "tools/coordination/": "communication",
    "tools/analysis/": "tools",
    "tools/consolidation/": "tools",
    "tools/": "tools",  # Default for root-level tools
}

# SSOT Tag Pattern
SSOT_TAG_PATTERN = re.compile(r"<!--\s*SSOT\s+Domain:\s*(\w+)\s*-->", re.IGNORECASE)


def load_classification() -> Dict:
    """Load tool classification JSON."""
    classification_path = Path("tools/TOOL_CLASSIFICATION.json")
    if not classification_path.exists():
        raise FileNotFoundError(
            f"Classification file not found: {classification_path}"
        )
    
    with open(classification_path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_signal_tools(classification: Dict) -> List[str]:
    """Extract SIGNAL tool file paths from classification."""
    signal_tools = []
    
    for tool in classification.get("signal", []):
        file_path = tool.get("file", "")
        if file_path:
            # Normalize path separators
            file_path = file_path.replace("\\", "/")
            signal_tools.append(file_path)
    
    return signal_tools


def determine_ssot_domain(file_path: str) -> str:
    """Determine SSOT domain based on file path."""
    # Normalize path
    normalized = file_path.replace("\\", "/")
    
    # Check directory mapping (longest match first)
    for dir_pattern, domain in sorted(
        DOMAIN_MAPPING.items(), key=lambda x: len(x[0]), reverse=True
    ):
        if normalized.startswith(dir_pattern):
            return domain
    
    # Default domain
    return "tools"


def has_ssot_tag(file_path: Path) -> Tuple[bool, str | None]:
    """Check if file already has SSOT tag. Returns (has_tag, domain)."""
    try:
        content = file_path.read_text(encoding="utf-8")
        match = SSOT_TAG_PATTERN.search(content)
        if match:
            return True, match.group(1)
        return False, None
    except Exception as e:
        print(f"  ⚠️  Error reading {file_path}: {e}")
        return False, None


def validate_python_syntax(file_path: Path, content: str) -> Tuple[bool, str | None]:
    """Validate Python syntax. Returns (is_valid, error_message)."""
    if not file_path.suffix == ".py":
        return True, None  # Not a Python file, skip validation
    
    try:
        ast.parse(content)
        return True, None
    except SyntaxError as e:
        return False, f"Syntax error: {e.msg} at line {e.lineno}"
    except Exception as e:
        return False, f"Parse error: {e}"


def find_docstring_insertion_point(lines: List[str]) -> int | None:
    """Find where to insert SSOT tag in docstring. Returns line index or None."""
    # Look for docstring opening (triple quotes)
    docstring_pattern = re.compile(r'^(\s*)("""|\'\'\')')
    
    for i, line in enumerate(lines):
        # Skip shebang
        if i == 0 and line.startswith("#!"):
            continue
        
        # Check if this line starts a docstring
        match = docstring_pattern.match(line)
        if match:
            # Insert after the opening docstring line
            return i + 1
    
    return None


def add_ssot_tag(
    file_path: Path, 
    domain: str, 
    dry_run: bool = False,
    validate_syntax: bool = True,
    backup: bool = True
) -> Tuple[bool, str | None]:
    """Add SSOT tag to file. Returns (success, error_message)."""
    try:
        content = file_path.read_text(encoding="utf-8")
        
        # Check if tag already exists
        if SSOT_TAG_PATTERN.search(content):
            return False, "Already has tag"
        
        # Validate original syntax first
        if validate_syntax:
            is_valid, error = validate_python_syntax(file_path, content)
            if not is_valid:
                return False, f"Original file has syntax error: {error}"
        
        # Determine insertion point
        lines = content.splitlines(keepends=True)
        tag_line = f"<!-- SSOT Domain: {domain} -->\n"
        
        # Try to find docstring insertion point
        docstring_index = find_docstring_insertion_point(lines)
        
        if docstring_index is not None:
            # Insert inside docstring (after opening """)
            insert_index = docstring_index
        else:
            # No docstring found - insert as Python comment after shebang
            insert_index = 0
            if lines and lines[0].startswith("#!"):
                insert_index = 1
            # Use Python comment format instead of HTML comment
            tag_line = f"# SSOT Domain: {domain}\n"
        
        # Insert SSOT tag
        lines.insert(insert_index, tag_line)
        new_content = "".join(lines)
        
        # Validate new syntax
        if validate_syntax:
            is_valid, error = validate_python_syntax(file_path, new_content)
            if not is_valid:
                return False, f"Modified file would have syntax error: {error}"
        
        if not dry_run:
            # Create backup if requested
            if backup:
                backup_path = file_path.with_suffix(file_path.suffix + ".ssot_backup")
                shutil.copy2(file_path, backup_path)
            
            file_path.write_text(new_content, encoding="utf-8")
        
        return True, None
    except Exception as e:
        return False, f"Error: {e}"


def main(
    dry_run: bool = True,
    test_mode: bool = False,
    batch_size: int = 10,
    validate_syntax: bool = True,
    backup: bool = True
):
    """Main execution function."""
    print("🚀 Phase 1: SSOT Tag Automation (Safe Mode)")
    print("=" * 60)
    print(f"Mode: {'DRY RUN' if dry_run else 'EXECUTE'}")
    if test_mode:
        print(f"🧪 TEST MODE: Processing first {batch_size} files only")
    if validate_syntax:
        print("✅ Syntax validation: ENABLED")
    if backup and not dry_run:
        print("💾 Backup: ENABLED (.ssot_backup files)")
    print()
    
    # Load classification
    print("📊 Loading tool classification...")
    try:
        classification = load_classification()
        signal_tools = get_signal_tools(classification)
        print(f"✅ Found {len(signal_tools)} SIGNAL tools")
    except Exception as e:
        print(f"❌ Error loading classification: {e}")
        return
    
    # Limit to test batch if in test mode
    if test_mode:
        signal_tools = signal_tools[:batch_size]
        print(f"🧪 TEST MODE: Processing {len(signal_tools)} files")
    
    # Process each SIGNAL tool
    print("\n📝 Processing SIGNAL tools...")
    stats = {
        "total": len(signal_tools),
        "already_tagged": 0,
        "tagged": 0,
        "errors": 0,
        "skipped": 0,
        "syntax_errors": 0,
    }
    
    errors_list = []
    
    for i, tool_path_str in enumerate(signal_tools, 1):
        tool_path = Path(tool_path_str)
        
        if not tool_path.exists():
            print(f"⚠️  [{i}/{len(signal_tools)}] File not found: {tool_path}")
            stats["skipped"] += 1
            continue
        
        # Check if already has tag
        has_tag, existing_domain = has_ssot_tag(tool_path)
        if has_tag:
            stats["already_tagged"] += 1
            continue
        
        # Determine domain
        domain = determine_ssot_domain(tool_path_str)
        
        # Add tag
        action = "Would add" if dry_run else "Adding"
        print(f"  [{i}/{len(signal_tools)}] {action} SSOT tag to {tool_path} (domain: {domain})")
        
        success, error_msg = add_ssot_tag(
            tool_path, domain, 
            dry_run=dry_run,
            validate_syntax=validate_syntax,
            backup=backup
        )
        
        if success:
            stats["tagged"] += 1
        else:
            stats["errors"] += 1
            if "syntax error" in error_msg.lower():
                stats["syntax_errors"] += 1
            errors_list.append((tool_path_str, error_msg))
            print(f"    ❌ Failed: {error_msg}")
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 Summary:")
    print(f"  Total SIGNAL tools: {stats['total']}")
    print(f"  Already tagged: {stats['already_tagged']}")
    print(f"  {'Would tag' if dry_run else 'Tagged'}: {stats['tagged']}")
    print(f"  Errors: {stats['errors']}")
    if stats['syntax_errors'] > 0:
        print(f"  ⚠️  Syntax errors: {stats['syntax_errors']}")
    print(f"  Skipped: {stats['skipped']}")
    
    if errors_list:
        print("\n⚠️  Errors encountered:")
        for file_path, error in errors_list[:10]:  # Show first 10 errors
            print(f"  - {file_path}: {error}")
        if len(errors_list) > 10:
            print(f"  ... and {len(errors_list) - 10} more errors")
    
    if dry_run:
        print("\n💡 This was a DRY RUN. Run with --execute to apply changes.")
        if test_mode:
            print("💡 Run without --test to process all files.")
    else:
        if stats['errors'] == 0:
            print("\n✅ SSOT tags added successfully!")
        else:
            print(f"\n⚠️  Completed with {stats['errors']} errors. Review errors above.")
            if backup:
                print("💾 Backups created (.ssot_backup files) - can restore if needed")


if __name__ == "__main__":
    import sys
    
    dry_run = "--execute" not in sys.argv
    test_mode = "--test" in sys.argv
    batch_size = 10
    no_validate = "--no-validate" in sys.argv
    no_backup = "--no-backup" in sys.argv
    
    # Parse batch size if provided
    for arg in sys.argv:
        if arg.startswith("--batch="):
            try:
                batch_size = int(arg.split("=")[1])
            except ValueError:
                print(f"⚠️  Invalid batch size: {arg.split('=')[1]}, using default 10")
    
    if "--help" in sys.argv or "-h" in sys.argv:
        print("Usage: python add_ssot_tags_bulk.py [OPTIONS]")
        print()
        print("Options:")
        print("  --execute       Actually add tags (default is dry-run)")
        print("  --test          Test mode: process first N files only (default: 10)")
        print("  --batch=N       Set test batch size (default: 10)")
        print("  --no-validate   Disable Python syntax validation")
        print("  --no-backup     Disable backup creation (not recommended)")
        print("  --help          Show this help message")
        print()
        print("Examples:")
        print("  python add_ssot_tags_bulk.py                    # Dry-run all files")
        print("  python add_ssot_tags_bulk.py --test            # Test first 10 files")
        print("  python add_ssot_tags_bulk.py --test --batch=5  # Test first 5 files")
        print("  python add_ssot_tags_bulk.py --execute --test  # Execute on first 10")
        sys.exit(0)
    
    main(
        dry_run=dry_run,
        test_mode=test_mode,
        batch_size=batch_size,
        validate_syntax=not no_validate,
        backup=not no_backup
    )

