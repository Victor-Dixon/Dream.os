"""
SSOT Domain Validation Tool
============================

Validates SSOT tags in tools against the SSOT domain mapping.
Ensures all SSOT tags use valid domains and correct format.

Agent: Agent-8 (SSOT & System Integration Specialist)
Date: 2025-12-21
Contract: Phase 1 - SSOT Domain Mapping & Validation
"""

import re
from pathlib import Path
from typing import List, Dict, Tuple

# Valid SSOT domains (from SSOT_DOMAIN_MAPPING.md)
VALID_DOMAINS = {
    'communication', 'coordination', 'integration', 'toolbelt',
    'autonomous', 'monitoring', 'validation', 'cli', 'codemods',
    'analysis', 'fixes', 'message_queue', 'templates', 'thea',
    'examples', 'captain', 'agent', 'consolidation', 'cleanup',
    'wordpress', 'github', 'deployment', 'audit', 'verification',
    'check', 'creation', 'update', 'debug', 'tools',
    'analytics', 'qa', 'infrastructure'  # Found in existing tags
}

# SSOT tag pattern
SSOT_TAG_PATTERN = re.compile(
    r'<!--\s*SSOT\s+Domain:\s*([a-z_]+)\s*-->',
    re.IGNORECASE
)


def find_ssot_tag(content: str) -> Tuple[bool, str, int]:
    """Find SSOT tag in file content.
    
    Returns: (found, domain, line_number)
    """
    lines = content.split('\n')
    for i, line in enumerate(lines[:50], 1):  # Check first 50 lines
        match = SSOT_TAG_PATTERN.search(line)
        if match:
            domain = match.group(1).lower()
            return True, domain, i
    return False, '', 0


def validate_ssot_tag(domain: str) -> Tuple[bool, str]:
    """Validate SSOT domain name.
    
    Returns: (is_valid, error_message)
    """
    if not domain:
        return False, "Empty domain"
    
    if domain not in VALID_DOMAINS:
        return False, f"Invalid domain: '{domain}' (not in domain registry)"
    
    if ' ' in domain:
        return False, f"Domain contains spaces: '{domain}'"
    
    if domain != domain.lower():
        return False, f"Domain should be lowercase: '{domain}'"
    
    return True, ""


def validate_file(file_path: Path) -> Dict:
    """Validate SSOT tag in a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return {
            "file": str(file_path),
            "error": f"File read error: {str(e)}",
            "valid": False
        }
    
    found, domain, line_num = find_ssot_tag(content)
    
    if not found:
        return {
            "file": str(file_path),
            "has_tag": False,
            "valid": False,
            "error": "No SSOT tag found"
        }
    
    is_valid, error_msg = validate_ssot_tag(domain)
    
    return {
        "file": str(file_path),
        "has_tag": True,
        "domain": domain,
        "line": line_num,
        "valid": is_valid,
        "error": error_msg if not is_valid else ""
    }


def validate_all_tools(tools_dir: Path) -> Dict:
    """Validate SSOT tags in all tools."""
    results = {
        "total_files": 0,
        "files_with_tags": 0,
        "valid_tags": 0,
        "invalid_tags": 0,
        "missing_tags": 0,
        "errors": [],
        "invalid_domains": []
    }
    
    exclude_patterns = [
        '__pycache__', '.pyc', 'test_', '_test.py',
        'archive', 'deprecated', '__init__.py'
    ]
    
    for py_file in tools_dir.rglob('*.py'):
        # Skip excluded files
        if any(pattern in str(py_file) for pattern in exclude_patterns):
            continue
        
        results["total_files"] += 1
        validation = validate_file(py_file)
        
        if validation.get("has_tag"):
            results["files_with_tags"] += 1
            if validation.get("valid"):
                results["valid_tags"] += 1
            else:
                results["invalid_tags"] += 1
                results["errors"].append(validation)
                if validation.get("domain"):
                    domain = validation["domain"]
                    if domain not in VALID_DOMAINS:
                        if domain not in results["invalid_domains"]:
                            results["invalid_domains"].append(domain)
        else:
            results["missing_tags"] += 1
    
    return results


def generate_validation_report(results: Dict, output_path: Path) -> None:
    """Generate validation report."""
    md_content = f"""# SSOT Domain Validation Report

**Date**: 2025-12-21  
**Agent**: Agent-8 (SSOT & System Integration Specialist)  
**Status**: ✅ **VALIDATION COMPLETE**

---

## 📊 Validation Summary

**Total Files Checked**: {results['total_files']}

### SSOT Tag Status:
- **Files with SSOT Tags**: {results['files_with_tags']} ({results['files_with_tags']/results['total_files']*100:.1f}%)
- **Valid Tags**: {results['valid_tags']} ({results['valid_tags']/results['total_files']*100:.1f}%)
- **Invalid Tags**: {results['invalid_tags']}
- **Missing Tags**: {results['missing_tags']} ({results['missing_tags']/results['total_files']*100:.1f}%)

---

## ❌ Invalid SSOT Tags

"""
    
    if results['invalid_tags'] > 0:
        for error in results['errors'][:20]:  # Show first 20
            md_content += f"""
### `{error['file']}`

- **Domain**: `{error.get('domain', 'N/A')}`
- **Line**: {error.get('line', 'N/A')}
- **Error**: {error.get('error', 'Unknown error')}

"""
        
        if len(results['errors']) > 20:
            md_content += f"\n... and {len(results['errors']) - 20} more invalid tags\n"
        
        if results['invalid_domains']:
            md_content += f"""
### Invalid Domains Found:

"""
            for domain in results['invalid_domains']:
                md_content += f"- `{domain}` (not in domain registry)\n"
    else:
        md_content += "✅ **No invalid SSOT tags found!**\n"
    
    md_content += f"""
---

## 📋 Next Steps

1. **Fix Invalid Tags**: Update invalid SSOT tags to use valid domains
2. **Add Missing Tags**: Use bulk SSOT tag addition script for files missing tags
3. **Re-validate**: Run validation again after fixes

---

**Agent-8 (SSOT & System Integration)**  
🐝 **WE. ARE. SWARM.** ⚡🔥
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print(f"📄 Validation report written to: {output_path}")


def main():
    """Main execution function."""
    print("=" * 70)
    print("SSOT Domain Validation")
    print("=" * 70)
    print()
    
    repo_root = Path(__file__).parent.parent
    tools_dir = repo_root / "tools"
    output_dir = repo_root / "tools"
    
    print("🔍 Validating SSOT tags in all tools...")
    results = validate_all_tools(tools_dir)
    
    print(f"\n📊 Validation Results:")
    print(f"   Total files: {results['total_files']}")
    print(f"   Files with tags: {results['files_with_tags']}")
    print(f"   Valid tags: {results['valid_tags']}")
    print(f"   Invalid tags: {results['invalid_tags']}")
    print(f"   Missing tags: {results['missing_tags']}")
    
    if results['invalid_domains']:
        print(f"\n⚠️  Invalid domains found: {', '.join(results['invalid_domains'])}")
    
    # Generate report
    report_path = output_dir / "SSOT_VALIDATION_REPORT.md"
    generate_validation_report(results, report_path)
    
    print()
    print("=" * 70)
    print("✅ SSOT Domain Validation Complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()

