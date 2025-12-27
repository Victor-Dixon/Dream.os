#!/usr/bin/env python3
"""
Scan SSOT Domain Tags
=====================

Scans codebase for all SSOT domain tags and generates a comprehensive domain registry.

<!-- SSOT Domain: tools -->
"""

import re
import json
from pathlib import Path
from collections import defaultdict
from typing import Dict, Set, List


def scan_ssot_domains(root_dir: Path = None) -> Dict:
    """Scan codebase for SSOT domain tags."""
    if root_dir is None:
        root_dir = Path(__file__).parent.parent
    
    # Pattern to match SSOT domain tags
    pattern = re.compile(
        r'<!--\s*SSOT\s+Domain:\s*([\w_]+)\s*-->',
        re.IGNORECASE
    )
    
    domains_found: Set[str] = set()
    domain_files: Dict[str, List[str]] = defaultdict(list)
    domain_file_types: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
    
    # File extensions to scan
    extensions = ['.py', '.md', '.php', '.js', '.ts', '.html', '.css']
    
    for ext in extensions:
        for file_path in root_dir.rglob(f'*{ext}'):
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                if 'SSOT Domain' in content:
                    matches = pattern.findall(content)
                    for domain in matches:
                        domains_found.add(domain.lower())
                        rel_path = str(file_path.relative_to(root_dir))
                        domain_files[domain.lower()].append(rel_path)
                        
                        # Track file types
                        domain_file_types[domain.lower()][ext] += 1
            except Exception as e:
                # Skip files that can't be read
                continue
    
    # Sort domains and file lists
    domains_sorted = sorted(domains_found)
    domain_files_sorted = {
        domain: sorted(files) 
        for domain, files in sorted(domain_files.items())
    }
    
    return {
        'domains': domains_sorted,
        'domain_count': len(domains_sorted),
        'domain_files': domain_files_sorted,
        'domain_file_types': dict(domain_file_types),
        'target_count': 32  # As per Agent-8 Phase 1
    }


def main():
    """Main function."""
    root_dir = Path(__file__).parent.parent
    
    print("🔍 Scanning codebase for SSOT domain tags...")
    print(f"   Root directory: {root_dir}")
    print()
    
    results = scan_ssot_domains(root_dir)
    
    print(f"📊 SSOT Domain Scan Results:")
    print(f"   Domains found: {results['domain_count']}")
    print(f"   Target domains: {results['target_count']}")
    print(f"   Remaining: {results['target_count'] - results['domain_count']}")
    print()
    
    print(f"📋 Domains found ({results['domain_count']}):")
    for domain in results['domains']:
        file_count = len(results['domain_files'][domain])
        file_types = results['domain_file_types'].get(domain, {})
        types_str = ', '.join(f"{ext}:{count}" for ext, count in sorted(file_types.items()))
        print(f"   - {domain} ({file_count} files) [{types_str}]")
    
    print()
    print(f"📁 Domain files summary:")
    for domain in sorted(results['domain_files'].keys()):
        files = results['domain_files'][domain]
        if len(files) <= 5:
            print(f"   {domain}: {', '.join(files)}")
        else:
            print(f"   {domain}: {len(files)} files (first 5: {', '.join(files[:5])}...)")
    
    # Save results to JSON
    output_file = root_dir / 'docs' / 'ssot_domain_scan_results.json'
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print()
    print(f"💾 Results saved to: {output_file.relative_to(root_dir)}")
    
    return results


if __name__ == '__main__':
    main()

