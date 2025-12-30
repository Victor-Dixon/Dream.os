#!/usr/bin/env python3
"""
Final SSOT Validation Checkpoint - All 42 Batches (1258 files)
Validates SSOT tag format, domain registry compliance, tag placement, and compilation.
"""

import sys
import re
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Tuple, Set
from collections import defaultdict
from datetime import datetime

# SSOT Domain Registry - all valid domains
VALID_DOMAINS = [
    "core", "architecture", "services", "integration", "infrastructure",
    "messaging", "onboarding", "web", "frontend", "backend", "api",
    "database", "storage", "security", "authentication", "authorization",
    "logging", "monitoring", "testing", "documentation", "tools",
    "utilities", "gaming", "trading", "discord", "vision", "ai",
    "automation", "deployment", "config", "models", "utils"
]

def extract_ssot_domain(content: str) -> Tuple[str, bool]:
    """Extract SSOT domain from file content"""
    # Pattern: <!-- SSOT Domain: domain_name -->
    pattern = r'<!--\s*SSOT\s+Domain:\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*-->'
    match = re.search(pattern, content, re.IGNORECASE)
    if match:
        return match.group(1).lower(), True
    return "", False

def validate_tag_format(content: str) -> Tuple[bool, str]:
    """Validate SSOT tag format: <!-- SSOT Domain: domain -->"""
    pattern = r'<!--\s*SSOT\s+Domain:\s*[a-zA-Z_][a-zA-Z0-9_]*\s*-->'
    if re.search(pattern, content, re.IGNORECASE):
        return True, "Tag format correct"
    return False, "Tag format incorrect or missing"

def validate_domain_registry(domain: str) -> Tuple[bool, str]:
    """Validate domain matches SSOT registry"""
    if domain.lower() in [d.lower() for d in VALID_DOMAINS]:
        return True, f"Domain '{domain}' matches SSOT registry"
    return False, f"Domain '{domain}' not in SSOT registry"

def validate_tag_placement(content: str) -> Tuple[bool, str]:
    """Validate tag placement in docstrings/headers (first 50 lines)"""
    lines = content.split('\n')[:50]
    header_content = '\n'.join(lines)
    
    pattern = r'<!--\s*SSOT\s+Domain:\s*[a-zA-Z_][a-zA-Z0-9_]*\s*-->'
    if re.search(pattern, header_content, re.IGNORECASE):
        return True, "Tag placed in module docstring/header"
    return False, "Tag not found in module docstring/header (first 50 lines)"

def validate_compilation(file_path: Path) -> Tuple[bool, str]:
    """Validate Python file compiles without syntax errors"""
    if not file_path.suffix == '.py':
        return True, "Not a Python file (compilation check skipped)"
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", str(file_path)],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return True, "Compilation successful"
        else:
            return False, f"Compilation error: {result.stderr.strip()[:200]}"
    except subprocess.TimeoutExpired:
        return False, "Compilation timeout"
    except Exception as e:
        return False, f"Compilation error: {str(e)[:200]}"

def validate_file(file_path: Path) -> Dict:
    """Validate a single file for SSOT compliance"""
    if not file_path.exists():
        return {
            "file": str(file_path),
            "valid": False,
            "error": "File not found"
        }
    
    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        return {
            "file": str(file_path),
            "valid": False,
            "error": f"Could not read file: {str(e)[:200]}"
        }
    
    # Extract domain
    domain, has_domain = extract_ssot_domain(content)
    
    if not has_domain:
        return {
            "file": str(file_path),
            "valid": False,
            "error": "No SSOT domain tag found"
        }
    
    results = {
        "file": str(file_path),
        "domain": domain,
        "tag_format": validate_tag_format(content),
        "domain_registry": validate_domain_registry(domain),
        "tag_placement": validate_tag_placement(content),
        "compilation": validate_compilation(file_path)
    }
    
    # Overall validation
    results["valid"] = all([
        results["tag_format"][0],
        results["domain_registry"][0],
        results["tag_placement"][0],
        results["compilation"][0]
    ])
    
    return results

def find_ssot_files(repo_root: Path) -> List[Path]:
    """Find all files with SSOT tags"""
    ssot_files = []
    pattern = r'<!--\s*SSOT\s+Domain:\s*[a-zA-Z_][a-zA-Z0-9_]*\s*-->'
    
    # Exclude cache directories and generated files
    excluded_dirs = {'__pycache__', '.git', 'node_modules', '.next', '.venv', 'venv', 'env', '.pytest_cache'}
    excluded_patterns = {'.pyc', '.pyo', '.pyd', '.pyc.'}
    
    # Search in src/ directory
    src_dir = repo_root / "src"
    if not src_dir.exists():
        return []
    
    for file_path in src_dir.rglob("*"):
        # Skip excluded directories
        if any(excluded_dir in file_path.parts for excluded_dir in excluded_dirs):
            continue
        
        # Skip excluded file patterns
        if file_path.suffix in excluded_patterns:
            continue
        
        if file_path.is_file() and not file_path.name.startswith('.'):
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                if re.search(pattern, content, re.IGNORECASE):
                    ssot_files.append(file_path)
            except Exception:
                # Skip files that can't be read
                continue
    
    return ssot_files

def main():
    """Validate all SSOT-tagged files"""
    repo_root = Path(__file__).parent.parent
    print("=" * 80)
    print("Final SSOT Validation Checkpoint - All 42 Batches (1258 files)")
    print("=" * 80)
    print()
    print("🔍 Scanning for SSOT-tagged files...")
    
    # Find all SSOT-tagged files
    ssot_files = find_ssot_files(repo_root)
    print(f"📊 Found {len(ssot_files)} files with SSOT tags")
    print()
    
    if not ssot_files:
        print("❌ No SSOT-tagged files found!")
        return 1
    
    # Validate each file
    results = []
    domain_stats = defaultdict(lambda: {"total": 0, "valid": 0, "invalid": 0})
    
    print("🔬 Validating files...")
    print()
    
    for i, file_path in enumerate(ssot_files, 1):
        relative_path = file_path.relative_to(repo_root)
        result = validate_file(file_path)
        results.append(result)
        
        # Update domain stats
        if "domain" in result:
            domain = result["domain"]
            domain_stats[domain]["total"] += 1
            if result["valid"]:
                domain_stats[domain]["valid"] += 1
            else:
                domain_stats[domain]["invalid"] += 1
        
        # Progress indicator
        if i % 100 == 0:
            print(f"   Validated {i}/{len(ssot_files)} files...")
        
        # Print invalid files immediately
        if not result["valid"]:
            status = "❌"
            print(f"{status} {relative_path}")
            if "error" in result:
                print(f"   Error: {result['error']}")
            else:
                if not result["tag_format"][0]:
                    print(f"   Tag Format: {result['tag_format'][1]}")
                if not result["domain_registry"][0]:
                    print(f"   Domain Registry: {result['domain_registry'][1]}")
                if not result["tag_placement"][0]:
                    print(f"   Tag Placement: {result['tag_placement'][1]}")
                if not result["compilation"][0]:
                    print(f"   Compilation: {result['compilation'][1]}")
    
    print()
    print("=" * 80)
    print("VALIDATION SUMMARY")
    print("=" * 80)
    print()
    
    valid_count = sum(1 for r in results if r["valid"])
    total_count = len(results)
    invalid_count = total_count - valid_count
    
    print(f"Total Files: {total_count}")
    print(f"Valid: {valid_count} ✅")
    print(f"Invalid: {invalid_count} ❌")
    print(f"Success Rate: {(valid_count/total_count)*100:.1f}%")
    print()
    
    # Domain statistics
    print("Domain Statistics:")
    print("-" * 80)
    for domain in sorted(domain_stats.keys()):
        stats = domain_stats[domain]
        valid_pct = (stats["valid"] / stats["total"] * 100) if stats["total"] > 0 else 0
        status = "✅" if stats["invalid"] == 0 else "⚠️"
        print(f"{status} {domain:20s} {stats['valid']:4d}/{stats['total']:4d} valid ({valid_pct:5.1f}%)")
    print()
    
    # Invalid files summary
    if invalid_count > 0:
        print("=" * 80)
        print("INVALID FILES SUMMARY")
        print("=" * 80)
        print()
        
        invalid_files = [r for r in results if not r["valid"]]
        for result in invalid_files[:50]:  # Show first 50 invalid files
            relative_path = Path(result["file"]).relative_to(repo_root)
            print(f"❌ {relative_path}")
            if "error" in result:
                print(f"   Error: {result['error']}")
            else:
                issues = []
                if not result["tag_format"][0]:
                    issues.append("Tag Format")
                if not result["domain_registry"][0]:
                    issues.append("Domain Registry")
                if not result["tag_placement"][0]:
                    issues.append("Tag Placement")
                if not result["compilation"][0]:
                    issues.append("Compilation")
                print(f"   Issues: {', '.join(issues)}")
        
        if len(invalid_files) > 50:
            print(f"\n... and {len(invalid_files) - 50} more invalid files")
        print()
    
    # Generate report file
    report_dir = repo_root / "docs" / "SSOT"
    report_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = report_dir / f"FINAL_VALIDATION_CHECKPOINT_{timestamp}.json"
    
    report_data = {
        "timestamp": datetime.now().isoformat(),
        "total_files": total_count,
        "valid_files": valid_count,
        "invalid_files": invalid_count,
        "success_rate": (valid_count/total_count)*100,
        "domain_statistics": dict(domain_stats),
        "validation_results": results
    }
    
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)
    
    print(f"📄 Validation report saved to: {report_file.relative_to(repo_root)}")
    print()
    
    if valid_count == total_count:
        print("🎉 All files validated successfully!")
        return 0
    else:
        print(f"⚠️  {invalid_count} files need attention")
        return 1

if __name__ == "__main__":
    sys.exit(main())

