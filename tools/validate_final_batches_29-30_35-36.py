#!/usr/bin/env python3
"""
Validate Final SSOT Batches 29-30, 35-36 (60 files)
Validates SSOT tag format, domain registry compliance, tag placement, and compilation.
Uses actual file lists from batch assignments JSON.
"""

import sys
import re
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple

# Load batch assignments to get actual file lists
def load_batch_files():
    """Load file lists from batch assignments JSON."""
    repo_root = Path(__file__).parent.parent
    batch_file = repo_root / "reports/ssot/ssot_batch_assignments_latest.json"
    
    if not batch_file.exists():
        print(f"❌ Batch assignments file not found: {batch_file}")
        return []
    
    with open(batch_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    all_files = []
    batch_ids = ['core_batch_29', 'core_batch_30', 'core_batch_35', 'core_batch_36']
    
    for batch in data.get('batches', {}).get('priority_1', []):
        if batch.get('batch_id') in batch_ids:
            files = batch.get('files', [])
            # Convert Windows paths to Unix-style
            files = [f.replace('\\', '/') for f in files]
            all_files.extend(files)
    
    return list(set(all_files))  # Remove duplicates

ALL_FILES = load_batch_files()

# SSOT Domain Registry
VALID_DOMAINS = [
    "integration", "core", "messaging", "analytics", "trading_robot",
    "architecture", "infrastructure", "deployment", "coordination",
    "gaming", "vision", "logging", "config", "monitoring", "performance",
    "error_handling", "discord", "swarm_brain", "git", "communication",
    "safety", "domain", "trading_robot", "performance", "error_handling",
    "swarm_brain", "analytics", "ai_training", "qa", "data"
]

def validate_ssot_tag_format(content: str) -> Tuple[bool, str]:
    """Validate SSOT tag format."""
    pattern = r'<!--\s*SSOT\s+Domain:\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*-->'
    match = re.search(pattern, content, re.IGNORECASE)
    if not match:
        return False, "SSOT tag not found or invalid format"
    domain = match.group(1)
    return True, domain

def validate_domain_registry(domain: str) -> bool:
    """Validate domain is in SSOT registry."""
    return domain.lower() in [d.lower() for d in VALID_DOMAINS]

def validate_tag_placement(content: str) -> Tuple[bool, str]:
    """Validate tag is in docstring or header (first 50 lines)."""
    lines = content.split('\n')[:50]
    header_content = '\n'.join(lines)
    pattern = r'<!--\s*SSOT\s+Domain:\s*[a-zA-Z_][a-zA-Z0-9_]*\s*-->'
    if re.search(pattern, header_content, re.IGNORECASE):
        return True, "Tag found in header/docstring"
    return False, "Tag not found in first 50 lines"

def validate_compilation(file_path: Path) -> Tuple[bool, str]:
    """Validate Python file compiles."""
    if not file_path.suffix == '.py':
        return True, "Not a Python file (skipping compilation)"
    
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'py_compile', str(file_path)],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return True, "Compilation successful"
        else:
            error = result.stderr[:200] if result.stderr else "Unknown compilation error"
            return False, f"Compilation failed: {error}"
    except subprocess.TimeoutExpired:
        return False, "Compilation timeout"
    except Exception as e:
        return False, f"Compilation error: {str(e)[:200]}"

def validate_file(file_path: Path) -> Dict:
    """Validate a single file."""
    repo_root = Path(__file__).parent.parent
    full_path = repo_root / file_path
    
    if not full_path.exists():
        return {
            "file": str(file_path),
            "valid": False,
            "errors": [f"File not found: {full_path}"],
            "exists": False
        }
    
    try:
        content = full_path.read_text(encoding='utf-8', errors='ignore')
    except Exception as e:
        return {
            "file": str(file_path),
            "valid": False,
            "errors": [f"Could not read file: {e}"],
            "exists": True
        }
    
    errors = []
    
    # Validate tag format
    tag_valid, tag_result = validate_ssot_tag_format(content)
    if not tag_valid:
        errors.append(f"Tag Format: {tag_result}")
    else:
        domain = tag_result
        # Validate domain registry
        if not validate_domain_registry(domain):
            errors.append(f"Domain Registry: Domain '{domain}' not in SSOT registry")
        # Validate domain matches expected (core for these batches)
        if domain.lower() != "core" and not file_path.suffix == '.md':
            # Allow non-core domains for markdown files
            if file_path.suffix != '.md':
                errors.append(f"Domain Mismatch: Expected 'core', found '{domain}'")
    
    # Validate tag placement
    placement_valid, placement_msg = validate_tag_placement(content)
    if not placement_valid:
        errors.append(f"Tag Placement: {placement_msg}")
    
    # Validate compilation (Python files only)
    if full_path.suffix == '.py':
        compile_valid, compile_msg = validate_compilation(full_path)
        if not compile_valid:
            errors.append(f"Compilation: {compile_msg}")
    
    return {
        "file": str(file_path),
        "valid": len(errors) == 0,
        "errors": errors,
        "exists": True
    }

def main():
    """Main validation function."""
    print("🔍 Validating Final Batches 29-30, 35-36...\n")
    print(f"📋 Loaded {len(ALL_FILES)} files from batch assignments\n")
    
    results = []
    valid_count = 0
    invalid_count = 0
    not_found_count = 0
    
    for file_path_str in ALL_FILES:
        file_path = Path(file_path_str)
        result = validate_file(file_path)
        results.append(result)
        
        if not result.get("exists", True):
            not_found_count += 1
            print(f"⚠️  {file_path} (file not found)")
        elif result["valid"]:
            valid_count += 1
            print(f"✅ {file_path}")
        else:
            invalid_count += 1
            print(f"❌ {file_path}")
            for error in result["errors"]:
                print(f"   - {error}")
    
    existing_count = valid_count + invalid_count
    
    print(f"\n📊 Summary:")
    print(f"   Total files in batches: {len(ALL_FILES)}")
    print(f"   Files found: {existing_count}")
    print(f"   Files not found: {not_found_count}")
    print(f"   Valid: {valid_count}")
    print(f"   Invalid: {invalid_count}")
    if existing_count > 0:
        print(f"   Pass rate (existing files): {(valid_count/existing_count*100):.1f}%")
    
    if invalid_count > 0:
        print(f"\n❌ Validation failed: {invalid_count} files have errors")
        sys.exit(1)
    else:
        print(f"\n✅ All existing files validated successfully!")
        if not_found_count > 0:
            print(f"⚠️  Note: {not_found_count} files from batch assignments were not found (may have been moved/renamed)")
        sys.exit(0)

if __name__ == "__main__":
    main()
