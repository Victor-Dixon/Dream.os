#!/usr/bin/env python3
"""
Repository Overlap Analyzer
============================

Builds on Agent-3 and Agent-8's consolidation work to identify additional overlaps
and organize similar repos into consolidation groups.

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-01-27
"""

import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Set
from difflib import SequenceMatcher


def similarity_score(str1: str, str2: str) -> float:
    """Calculate similarity between two strings (0-1)."""
    return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()


def normalize_repo_name(name: str) -> str:
    """Normalize repo name for comparison."""
    # Remove emojis, special chars, normalize case/hyphens/underscores
    normalized = re.sub(r'[^\w\s-]', '', name)
    normalized = normalized.lower().replace('-', '_').replace(' ', '_')
    return normalized.strip('_')


def extract_repo_info_from_devlog(devlog_path: Path) -> Dict[str, Any]:
    """Extract repo information from devlog file."""
    try:
        content = devlog_path.read_text(encoding='utf-8')
        lines = content.split('\n')
        
        # Extract repo name
        repo_name = None
        for line in lines[:20]:
            if 'Repo' in line and ('#' in line or ':' in line):
                parts = re.split(r'[#:]', line)
                if len(parts) > 1:
                    repo_name = parts[-1].strip().split()[0]
                    break
        
        # Extract tech stack
        tech_stack = []
        for line in lines:
            if 'tech_stack' in line.lower() or 'technology' in line.lower():
                # Look for common tech keywords
                tech_keywords = ['Python', 'JavaScript', 'TypeScript', 'React', 'Node', 
                               'FastAPI', 'Flask', 'Discord', 'PostgreSQL', 'SQLite', 'MongoDB']
                for keyword in tech_keywords:
                    if keyword.lower() in line.lower():
                        tech_stack.append(keyword)
        
        # Extract purpose
        purpose = None
        for i, line in enumerate(lines):
            if 'purpose' in line.lower() and i + 1 < len(lines):
                purpose = lines[i + 1].strip('- ').strip()[:200]
                break
        
        return {
            'name': repo_name or devlog_path.stem,
            'filename': devlog_path.name,
            'tech_stack': list(set(tech_stack)),
            'purpose': purpose or '',
            'content': content[:500]
        }
    except Exception as e:
        return {'name': devlog_path.stem, 'error': str(e)}


def analyze_overlaps():
    """Analyze repository overlaps and create consolidation groups."""
    devlogs_path = Path('swarm_brain/devlogs/repository_analysis')
    
    # Load existing consolidation work
    agent3_analysis = Path('agent_workspaces/Agent-3/repo_consolidation_analysis.json')
    agent8_strategy = Path('agent_workspaces/Agent-8/REPO_CONSOLIDATION_STRATEGY.md')
    
    repos = []
    repo_by_name = {}
    
    # Load repos from devlogs
    if devlogs_path.exists():
        for devlog_file in sorted(devlogs_path.glob('*.md')):
            repo_info = extract_repo_info_from_devlog(devlog_file)
            if 'error' not in repo_info:
                repos.append(repo_info)
                normalized = normalize_repo_name(repo_info['name'])
                if normalized not in repo_by_name:
                    repo_by_name[normalized] = []
                repo_by_name[normalized].append(repo_info)
    
    print(f"📊 Loaded {len(repos)} repositories from devlogs")
    
    # Find duplicates (same normalized name)
    duplicates = {k: v for k, v in repo_by_name.items() if len(v) > 1}
    
    # Find similar names (high similarity score)
    similar_groups = defaultdict(list)
    for i, repo1 in enumerate(repos):
        for repo2 in repos[i+1:]:
            norm1 = normalize_repo_name(repo1['name'])
            norm2 = normalize_repo_name(repo2['name'])
            
            # Skip exact duplicates (handled separately)
            if norm1 == norm2:
                continue
            
            # Check similarity
            similarity = similarity_score(norm1, norm2)
            if similarity > 0.7:  # 70% similarity threshold
                key = tuple(sorted([norm1, norm2]))
                if key not in similar_groups:
                    similar_groups[key] = []
                similar_groups[key].extend([repo1, repo2])
    
    # Group by tech stack
    tech_stack_groups = defaultdict(list)
    for repo in repos:
        if repo.get('tech_stack'):
            stack_key = tuple(sorted(repo['tech_stack']))
            tech_stack_groups[stack_key].append(repo)
    
    # Find repos with same tech stack and similar purpose
    purpose_groups = defaultdict(list)
    for repo in repos:
        if repo.get('purpose'):
            # Extract key words from purpose
            words = set(re.sub(r'[^\w\s]', '', repo['purpose'].lower()).split())
            # Look for common domain keywords
            if any(word in ['trading', 'trade', 'analyzer', 'bot'] for word in words):
                purpose_groups['trading'].append(repo)
            elif any(word in ['discord', 'bot', 'automation'] for word in words):
                purpose_groups['discord_automation'].append(repo)
            elif any(word in ['dream', 'ai', 'assistant'] for word in words):
                purpose_groups['dream_ai'].append(repo)
            elif any(word in ['stream', 'youtube', 'video'] for word in words):
                purpose_groups['streaming'].append(repo)
    
    # Build consolidation recommendations
    consolidation_groups = []
    
    # Group 1: Exact duplicate names (case variations)
    for norm_name, dup_repos in duplicates.items():
        if len(dup_repos) > 1:
            # Keep the one with most complete info
            primary = max(dup_repos, key=lambda r: len(r.get('content', '')))
            secondary = [r for r in dup_repos if r['name'] != primary['name']]
            
            consolidation_groups.append({
                'type': 'duplicate_name',
                'priority': 'HIGH',
                'target': primary['name'],
                'merge_from': [r['name'] for r in secondary],
                'repos': dup_repos,
                'reduction': len(secondary)
            })
    
    # Group 2: Similar names
    processed = set()
    for (norm1, norm2), similar_repos in similar_groups.items():
        if norm1 in processed or norm2 in processed:
            continue
        
        # Choose primary (most complete or most recent)
        primary = max(similar_repos, key=lambda r: len(r.get('content', '')))
        secondary = [r for r in similar_repos if r['name'] != primary['name']]
        
        consolidation_groups.append({
            'type': 'similar_name',
            'priority': 'MEDIUM',
            'target': primary['name'],
            'merge_from': [r['name'] for r in secondary],
            'repos': similar_repos,
            'reduction': len(secondary),
            'similarity_score': similarity_score(norm1, norm2)
        })
        
        processed.add(norm1)
        processed.add(norm2)
    
    # Group 3: Same tech stack + similar purpose
    for purpose_key, purpose_repos in purpose_groups.items():
        if len(purpose_repos) > 2:  # Only group if 3+ repos
            # Further filter by exact tech stack match
            by_stack = defaultdict(list)
            for repo in purpose_repos:
                stack_key = tuple(sorted(repo.get('tech_stack', [])))
                by_stack[stack_key].append(repo)
            
            for stack_key, stack_repos in by_stack.items():
                if len(stack_repos) >= 2:
                    primary = max(stack_repos, key=lambda r: len(r.get('content', '')))
                    secondary = [r for r in stack_repos if r['name'] != primary['name']]
                    
                    consolidation_groups.append({
                        'type': 'same_purpose_tech',
                        'priority': 'MEDIUM',
                        'target': primary['name'],
                        'merge_from': [r['name'] for r in secondary],
                        'repos': stack_repos,
                        'reduction': len(secondary),
                        'tech_stack': list(stack_key),
                        'purpose_category': purpose_key
                    })
    
    # Create summary report
    total_reduction = sum(g['reduction'] for g in consolidation_groups)
    high_priority = [g for g in consolidation_groups if g['priority'] == 'HIGH']
    medium_priority = [g for g in consolidation_groups if g['priority'] == 'MEDIUM']
    
    report = {
        'analysis_date': '2025-01-27',
        'analyzer': 'Agent-5',
        'total_repos_analyzed': len(repos),
        'duplicate_name_groups': len([g for g in consolidation_groups if g['type'] == 'duplicate_name']),
        'similar_name_groups': len([g for g in consolidation_groups if g['type'] == 'similar_name']),
        'purpose_tech_groups': len([g for g in consolidation_groups if g['type'] == 'same_purpose_tech']),
        'total_consolidation_groups': len(consolidation_groups),
        'potential_reduction': total_reduction,
        'high_priority_groups': len(high_priority),
        'medium_priority_groups': len(medium_priority),
        'consolidation_groups': consolidation_groups,
        'duplicates_found': {
            name: [r['name'] for r in repos] 
            for name, repos in duplicates.items()
        }
    }
    
    return report


def main():
    """Main analysis function."""
    print("🔍 Repository Overlap Analyzer - Agent-5")
    print("=" * 60)
    print("Building on Agent-3 and Agent-8's consolidation work...")
    print()
    
    report = analyze_overlaps()
    
    # Save report
    output_path = Path('agent_workspaces/Agent-5/repo_overlap_analysis.json')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2))
    
    print(f"✅ Analysis complete!")
    print(f"   Total repos analyzed: {report['total_repos_analyzed']}")
    print(f"   Consolidation groups found: {report['total_consolidation_groups']}")
    print(f"   Potential reduction: {report['potential_reduction']} repos")
    print(f"   High priority: {report['high_priority_groups']} groups")
    print(f"   Medium priority: {report['medium_priority_groups']} groups")
    print()
    print(f"📄 Full report saved to: {output_path}")
    
    # Print summary of groups
    print("\n📋 Consolidation Groups Summary:")
    print("-" * 60)
    for i, group in enumerate(report['consolidation_groups'][:10], 1):  # Show first 10
        print(f"\n{i}. {group['type']} - {group['priority']} Priority")
        print(f"   Target: {group['target']}")
        print(f"   Merge from: {', '.join(group['merge_from'][:3])}")
        print(f"   Reduction: {group['reduction']} repos")
    
    if len(report['consolidation_groups']) > 10:
        print(f"\n   ... and {len(report['consolidation_groups']) - 10} more groups")
    
    return report


if __name__ == '__main__':
    main()

