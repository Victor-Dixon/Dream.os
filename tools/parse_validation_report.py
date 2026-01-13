#!/usr/bin/env python3
"""Parse SSOT validation checkpoint report and extract key statistics."""
import json
import sys

def main():
    report_path = 'docs/SSOT/FINAL_VALIDATION_CHECKPOINT_20251230_052232.json'
    
    with open(report_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("=" * 60)
    print("SSOT VALIDATION CHECKPOINT SUMMARY")
    print("=" * 60)
    print(f"Timestamp: {data['timestamp']}")
    print(f"Total Files: {data['total_files']}")
    print(f"Valid Files: {data['valid_files']}")
    print(f"Invalid Files: {data['invalid_files']}")
    print(f"Success Rate: {data['success_rate']:.2f}%")
    print("\n" + "=" * 60)
    print("DOMAIN STATISTICS")
    print("=" * 60)
    
    # Sort domains by total files (descending)
    domain_stats = sorted(
        data['domain_statistics'].items(),
        key=lambda x: x[1]['total'],
        reverse=True
    )
    
    for domain, stats in domain_stats:
        valid_pct = (stats['valid'] / stats['total'] * 100) if stats['total'] > 0 else 0
        print(f"{domain:20s} {stats['valid']:4d}/{stats['total']:4d} valid ({stats['invalid']:4d} invalid) - {valid_pct:5.1f}%")
    
    print("\n" + "=" * 60)
    print("INVALID FILES BY DOMAIN (Top 10)")
    print("=" * 60)
    
    # Get invalid files grouped by domain
    invalid_by_domain = {}
    for result in data['validation_results']:
        if not result.get('valid', True):
            file_path = result.get('file', result.get('file_path', 'unknown'))
            domain = result.get('domain', 'unknown')
            if domain not in invalid_by_domain:
                invalid_by_domain[domain] = []
            invalid_by_domain[domain].append(file_path)
    
    # Sort by count of invalid files
    sorted_domains = sorted(
        invalid_by_domain.items(),
        key=lambda x: len(x[1]),
        reverse=True
    )
    
    for domain, files in sorted_domains[:10]:
        print(f"\n{domain} ({len(files)} invalid files):")
        for file_path in files[:5]:  # Show first 5
            print(f"  - {file_path}")
        if len(files) > 5:
            print(f"  ... and {len(files) - 5} more")

if __name__ == '__main__':
    main()

