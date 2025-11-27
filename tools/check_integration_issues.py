#!/usr/bin/env python3
"""
Integration Issues Checker
Checks consolidated repos for:
- Virtual environment files (should NOT be in repo)
- Duplicate files
- Code duplication issues
"""

import os
import hashlib
from pathlib import Path
from collections import defaultdict
import json

def get_file_hash(filepath):
    """Calculate MD5 hash of file content."""
    try:
        with open(filepath, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except Exception:
        return None

def find_venv_directories(root_dir):
    """Find virtual environment directories."""
    venv_patterns = [
        'lib/python*/site-packages/',
        'venv/',
        'env/',
        '.venv/',
        'node_modules/',
        '__pycache__/',
        '.pytest_cache/',
    ]
    
    venv_dirs = []
    for root, dirs, files in os.walk(root_dir):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            rel_path = os.path.relpath(dir_path, root_dir)
            
            # Check for venv patterns
            for pattern in venv_patterns:
                if pattern.replace('*', '') in rel_path or 'site-packages' in rel_path:
                    venv_dirs.append(rel_path)
                    break
    
    return venv_dirs

def find_duplicate_files(root_dir, exclude_patterns=None):
    """Find duplicate files by content hash."""
    if exclude_patterns is None:
        exclude_patterns = [
            'lib/python*/site-packages/',
            'venv/',
            'env/',
            '.venv/',
            'node_modules/',
            '__pycache__/',
            '.pytest_cache/',
            '.git/',
        ]
    
    file_hashes = defaultdict(list)
    total_files = 0
    
    for root, dirs, files in os.walk(root_dir):
        # Skip excluded directories
        rel_root = os.path.relpath(root, root_dir)
        skip = False
        for pattern in exclude_patterns:
            if pattern.replace('*', '') in rel_root or 'site-packages' in rel_root:
                skip = True
                break
        if skip:
            continue
        
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file_name in files:
            if file_name.startswith('.'):
                continue
                
            file_path = os.path.join(root, file_name)
            rel_path = os.path.relpath(file_path, root_dir)
            
            file_hash = get_file_hash(file_path)
            if file_hash:
                file_hashes[file_hash].append(rel_path)
                total_files += 1
    
    # Find duplicates (files with same hash)
    duplicates = {hash_val: paths for hash_val, paths in file_hashes.items() if len(paths) > 1}
    
    return {
        'total_files': total_files,
        'unique_files': len(file_hashes),
        'duplicate_groups': len(duplicates),
        'duplicate_files': sum(len(paths) - 1 for paths in duplicates.values()),
        'duplicates': duplicates
    }

def analyze_repo(repo_path, repo_name):
    """Analyze a repository for integration issues."""
    if not os.path.exists(repo_path):
        return {
            'repo': repo_name,
            'path': repo_path,
            'status': 'not_found',
            'error': f'Repository path not found: {repo_path}'
        }
    
    print(f"Analyzing {repo_name}...")
    
    # Check for venv directories
    venv_dirs = find_venv_directories(repo_path)
    
    # Find duplicate files
    duplicate_analysis = find_duplicate_files(repo_path)
    
    return {
        'repo': repo_name,
        'path': repo_path,
        'status': 'analyzed',
        'venv_directories': venv_dirs,
        'venv_count': len(venv_dirs),
        'duplicate_analysis': duplicate_analysis,
        'issues_found': len(venv_dirs) > 0 or duplicate_analysis['duplicate_groups'] > 0
    }

def main():
    """Main analysis function."""
    import sys
    
    print("=" * 60)
    print("Integration Issues Checker")
    print("=" * 60)
    
    # Check for command-line arguments
    if len(sys.argv) > 1:
        # Analyze specific repo path provided
        repo_path = sys.argv[1]
        repo_name = sys.argv[2] if len(sys.argv) > 2 else os.path.basename(repo_path)
        result = analyze_repo(repo_path, repo_name)
        results = [result]
    else:
        # Default repos to check (consolidated repos)
        repos_to_check = [
            {
                'name': 'Auto_Blogger',
                'path': None  # Would need actual path or clone
            },
            {
                'name': 'trading-leads-bot',
                'path': 'temp_trading_leads_bot' if os.path.exists('temp_trading_leads_bot') else None
            }
        ]
        
        results = []
        
        for repo in repos_to_check:
            if repo['path'] and os.path.exists(repo['path']):
                result = analyze_repo(repo['path'], repo['name'])
                results.append(result)
            else:
                results.append({
                    'repo': repo['name'],
                    'status': 'path_not_provided',
                    'note': 'Repository path needed for analysis'
                })
    
    # Print results
    print("\n" + "=" * 60)
    print("Analysis Results")
    print("=" * 60)
    
    for result in results:
        print(f"\n{result['repo']}:")
        print(f"  Status: {result['status']}")
        
        if result['status'] == 'analyzed':
            print(f"  Venv Directories: {result['venv_count']}")
            if result['venv_directories']:
                print("    Directories found:")
                for venv_dir in result['venv_directories'][:10]:  # Show first 10
                    print(f"      - {venv_dir}")
                if len(result['venv_directories']) > 10:
                    print(f"      ... and {len(result['venv_directories']) - 10} more")
            
            dup_analysis = result['duplicate_analysis']
            print(f"  Total Files: {dup_analysis['total_files']}")
            print(f"  Unique Files: {dup_analysis['unique_files']}")
            print(f"  Duplicate Groups: {dup_analysis['duplicate_groups']}")
            print(f"  Duplicate Files: {dup_analysis['duplicate_files']}")
            
            if result['issues_found']:
                print("  ⚠️  ISSUES FOUND - Needs resolution")
            else:
                print("  ✅ No issues found")
    
    # Save results
    output_file = 'integration_issues_report.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: {output_file}")
    
    return results

if __name__ == '__main__':
    main()

