#!/usr/bin/env python3
"""
Enhanced Repository Consolidation Analyzer
==========================================

Builds on existing consolidation work (Agent-3, Agent-5, Agent-8) to:
1. Use master repo list (75 repos) instead of devlogs
2. Identify new overlaps not previously found
3. Refine consolidation groups with better similarity detection
4. Avoid duplicate work

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-01-27
Priority: HIGH
"""

import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Set
from difflib import SequenceMatcher


def normalize_repo_name(name: str) -> str:
    """Normalize repo name for comparison."""
    # Remove emojis, special chars, normalize case/hyphens/underscores
    normalized = re.sub(r'[^\w\s-]', '', name)
    normalized = normalized.lower().replace('-', '_').replace(' ', '_')
    return normalized.strip('_')


def similarity_score(str1: str, str2: str) -> float:
    """Calculate similarity between two strings (0-1)."""
    return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()


def load_master_repo_list() -> List[Dict[str, Any]]:
    """Load repos from master list JSON file."""
    master_list_path = Path('data/github_75_repos_master_list.json')
    
    if not master_list_path.exists():
        print(f"❌ Master repo list not found: {master_list_path}")
        return []
    
    try:
        with open(master_list_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            repos = data.get('repos', [])
            print(f"✅ Loaded {len(repos)} repos from master list")
            return repos
    except Exception as e:
        print(f"❌ Error loading master repo list: {e}")
        return []


def load_existing_consolidation_plan() -> Dict[str, Any]:
    """Load existing consolidation plan from Agent-8."""
    plan_path = Path('agent_workspaces/Agent-8/REPO_CONSOLIDATION_PLAN.json')
    
    if not plan_path.exists():
        return {}
    
    try:
        with open(plan_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ Could not load existing plan: {e}")
        return {}


def find_duplicate_names(repos: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Find repos with duplicate names (case variations)."""
    by_normalized = defaultdict(list)
    
    for repo in repos:
        name = repo.get('name', '')
        if name and name != 'Unknown':
            normalized = normalize_repo_name(name)
            by_normalized[normalized].append(repo)
    
    # Return only duplicates
    return {k: v for k, v in by_normalized.items() if len(v) > 1}


def find_similar_names(repos: List[Dict[str, Any]], threshold: float = 0.7) -> List[Dict[str, Any]]:
    """Find repos with similar names."""
    similar_pairs = []
    processed = set()
    
    for i, repo1 in enumerate(repos):
        name1 = repo1.get('name', '')
        if not name1 or name1 == 'Unknown':
            continue
        
        norm1 = normalize_repo_name(name1)
        if norm1 in processed:
            continue
        
        for repo2 in repos[i+1:]:
            name2 = repo2.get('name', '')
            if not name2 or name2 == 'Unknown':
                continue
            
            norm2 = normalize_repo_name(name2)
            
            # Skip exact duplicates (handled separately)
            if norm1 == norm2:
                continue
            
            # Check similarity
            similarity = similarity_score(norm1, norm2)
            if similarity >= threshold:
                similar_pairs.append({
                    'repo1': repo1,
                    'repo2': repo2,
                    'similarity': similarity,
                    'norm1': norm1,
                    'norm2': norm2
                })
                processed.add(norm1)
                processed.add(norm2)
    
    return similar_pairs


def categorize_repos(repos: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Categorize repos by purpose/domain."""
    categories = defaultdict(list)
    
    for repo in repos:
        name = repo.get('name', '').lower()
        
        # Trading repos
        if any(word in name for word in ['trade', 'trading', 'options', 'robot']):
            categories['trading'].append(repo)
        
        # Dream/AI repos
        elif any(word in name for word in ['dream', 'autodream', 'digitaldream']):
            categories['dream_projects'].append(repo)
        
        # Agent systems
        elif any(word in name for word in ['agent', 'multi-agent', 'intelligent']):
            categories['agent_systems'].append(repo)
        
        # Streaming
        elif any(word in name for word in ['stream', 'metuber', 'youtube']):
            categories['streaming'].append(repo)
        
        # ML/AI models
        elif any(word in name for word in ['lstm', 'model', 'machinelearning', 'ml']):
            categories['ml_models'].append(repo)
        
        # Personal projects
        elif any(word in name for word in ['dadudekc', 'resume', 'personal']):
            categories['personal'].append(repo)
        
        # External libraries (keep separate)
        elif name in ['fastapi', 'transformers', 'langchain-google']:
            categories['external_libs'].append(repo)
    
    return categories


def build_consolidation_groups(repos: List[Dict[str, Any]], existing_plan: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Build consolidation groups from analysis."""
    groups = []
    
    # 1. Find duplicate names (case variations)
    duplicates = find_duplicate_names(repos)
    for norm_name, dup_repos in duplicates.items():
        if len(dup_repos) > 1:
            # Choose primary (most analyzed, or goldmine, or first)
            primary = max(dup_repos, key=lambda r: (
                r.get('analyzed', False),
                r.get('goldmine', False),
                0
            ))
            secondary = [r for r in dup_repos if r['name'] != primary['name']]
            
            groups.append({
                'type': 'duplicate_name',
                'priority': 'HIGH',
                'category': 'case_variation',
                'target_repo': primary['name'],
                'target_num': primary.get('num'),
                'merge_from': [{'name': r['name'], 'num': r.get('num')} for r in secondary],
                'repos': dup_repos,
                'reduction': len(secondary),
                'notes': f"Case variation: {norm_name}"
            })
    
    # 2. Find similar names
    similar_pairs = find_similar_names(repos, threshold=0.75)
    processed_names = set()
    
    for pair in similar_pairs:
        repo1 = pair['repo1']
        repo2 = pair['repo2']
        name1 = repo1.get('name', '')
        name2 = repo2.get('name', '')
        
        # Skip if already processed as duplicate
        if normalize_repo_name(name1) in processed_names or normalize_repo_name(name2) in processed_names:
            continue
        
        # Choose primary
        primary = repo1 if (repo1.get('analyzed', False) or repo1.get('goldmine', False)) else repo2
        secondary = repo2 if primary == repo1 else repo1
        
        groups.append({
            'type': 'similar_name',
            'priority': 'MEDIUM',
            'category': 'name_similarity',
            'target_repo': primary['name'],
            'target_num': primary.get('num'),
            'merge_from': [{'name': secondary['name'], 'num': secondary.get('num')}],
            'repos': [repo1, repo2],
            'reduction': 1,
            'similarity_score': pair['similarity'],
            'notes': f"Similar names: {name1} ~ {name2} ({pair['similarity']:.2%})"
        })
        
        processed_names.add(normalize_repo_name(name1))
        processed_names.add(normalize_repo_name(name2))
    
    # 3. Categorize and group by domain
    categories = categorize_repos(repos)
    
    # Trading repos consolidation
    if len(categories.get('trading', [])) > 1:
        trading_repos = categories['trading']
        # Find primary (goldmine or most analyzed)
        primary = max(trading_repos, key=lambda r: (
            r.get('goldmine', False),
            r.get('analyzed', False),
            0
        ))
        secondary = [r for r in trading_repos if r['name'] != primary['name']]
        
        if secondary:  # Only add if there are repos to merge
            groups.append({
                'type': 'domain_group',
                'priority': 'HIGH',
                'category': 'trading',
                'target_repo': primary['name'],
                'target_num': primary.get('num'),
                'merge_from': [{'name': r['name'], 'num': r.get('num')} for r in secondary],
                'repos': trading_repos,
                'reduction': len(secondary),
                'notes': f"Trading domain consolidation: {len(trading_repos)} repos"
            })
    
    # Dream projects consolidation
    if len(categories.get('dream_projects', [])) > 1:
        dream_repos = categories['dream_projects']
        # Exclude AutoDream_Os (it's Agent_Cellphone_V2)
        dream_repos = [r for r in dream_repos if r.get('name') != 'AutoDream_Os']
        
        if len(dream_repos) > 1:
            primary = max(dream_repos, key=lambda r: (
                r.get('goldmine', False),
                r.get('analyzed', False),
                0
            ))
            secondary = [r for r in dream_repos if r['name'] != primary['name']]
            
            if secondary:
                groups.append({
                    'type': 'domain_group',
                    'priority': 'HIGH',
                    'category': 'dream_projects',
                    'target_repo': primary['name'],
                    'target_num': primary.get('num'),
                    'merge_from': [{'name': r['name'], 'num': r.get('num')} for r in secondary],
                    'repos': dream_repos,
                    'reduction': len(secondary),
                    'notes': 'Dream projects consolidation (AutoDream_Os excluded - it is Agent_Cellphone_V2)'
                })
    
    # Agent systems consolidation
    if len(categories.get('agent_systems', [])) > 1:
        agent_repos = categories['agent_systems']
        # Exclude Agent_Cellphone (current V2)
        agent_repos = [r for r in agent_repos if 'V2' not in r.get('name', '')]
        
        if len(agent_repos) > 1:
            primary = max(agent_repos, key=lambda r: (
                r.get('goldmine', False),
                r.get('analyzed', False),
                0
            ))
            secondary = [r for r in agent_repos if r['name'] != primary['name']]
            
            if secondary:
                groups.append({
                    'type': 'domain_group',
                    'priority': 'HIGH',
                    'category': 'agent_systems',
                    'target_repo': primary['name'],
                    'target_num': primary.get('num'),
                    'merge_from': [{'name': r['name'], 'num': r.get('num')} for r in secondary],
                    'repos': agent_repos,
                    'reduction': len(secondary),
                    'notes': 'Agent systems consolidation'
                })
    
    # Streaming consolidation
    if len(categories.get('streaming', [])) > 1:
        streaming_repos = categories['streaming']
        primary = max(streaming_repos, key=lambda r: (
            r.get('analyzed', False),
            0
        ))
        secondary = [r for r in streaming_repos if r['name'] != primary['name']]
        
        if secondary:
            groups.append({
                'type': 'domain_group',
                'priority': 'MEDIUM',
                'category': 'streaming',
                'target_repo': primary['name'],
                'target_num': primary.get('num'),
                'merge_from': [{'name': r['name'], 'num': r.get('num')} for r in secondary],
                'repos': streaming_repos,
                'reduction': len(secondary),
                'notes': 'Streaming tools consolidation'
            })
    
    # ML models consolidation
    if len(categories.get('ml_models', [])) > 1:
        ml_repos = categories['ml_models']
        primary = max(ml_repos, key=lambda r: (
            r.get('analyzed', False),
            0
        ))
        secondary = [r for r in ml_repos if r['name'] != primary['name']]
        
        if secondary:
            groups.append({
                'type': 'domain_group',
                'priority': 'MEDIUM',
                'category': 'ml_models',
                'target_repo': primary['name'],
                'target_num': primary.get('num'),
                'merge_from': [{'name': r['name'], 'num': r.get('num')} for r in secondary],
                'repos': ml_repos,
                'reduction': len(secondary),
                'notes': 'ML models consolidation'
            })
    
    return groups


def compare_with_existing(groups: List[Dict[str, Any]], existing_plan: Dict[str, Any]) -> Dict[str, Any]:
    """Compare new findings with existing consolidation plan."""
    existing_groups = existing_plan.get('consolidation_plan', {}).get('high_priority', [])
    existing_targets = {g.get('target_repo') for g in existing_groups if 'target_repo' in g}
    
    new_groups = []
    updated_groups = []
    existing_found = []
    
    for group in groups:
        target = group.get('target_repo', '')
        if target in existing_targets:
            existing_found.append(group)
        else:
            # Check if similar to existing
            is_new = True
            for existing in existing_groups:
                existing_target = existing.get('target_repo', '')
                if similarity_score(target.lower(), existing_target.lower()) > 0.8:
                    updated_groups.append({
                        'new': group,
                        'existing': existing
                    })
                    is_new = False
                    break
            
            if is_new:
                new_groups.append(group)
    
    return {
        'new_groups': new_groups,
        'updated_groups': updated_groups,
        'existing_found': existing_found,
        'total_new': len(new_groups),
        'total_updated': len(updated_groups)
    }


def main():
    """Main analysis function."""
    print("🔍 Enhanced Repository Consolidation Analyzer - Agent-1")
    print("=" * 70)
    print("Building on Agent-3, Agent-5, and Agent-8's consolidation work...")
    print()
    
    # Load data
    repos = load_master_repo_list()
    if not repos:
        print("❌ No repos loaded. Exiting.")
        return
    
    existing_plan = load_existing_consolidation_plan()
    
    # Analyze
    print("📊 Analyzing repos for consolidation opportunities...")
    groups = build_consolidation_groups(repos, existing_plan)
    
    # Compare with existing
    comparison = compare_with_existing(groups, existing_plan)
    
    # Calculate totals
    total_reduction = sum(g['reduction'] for g in groups)
    high_priority = [g for g in groups if g['priority'] == 'HIGH']
    medium_priority = [g for g in groups if g['priority'] == 'MEDIUM']
    
    # Create report
    report = {
        'analysis_date': '2025-01-27',
        'analyzer': 'Agent-1',
        'total_repos_analyzed': len(repos),
        'total_consolidation_groups': len(groups),
        'potential_reduction': total_reduction,
        'high_priority_groups': len(high_priority),
        'medium_priority_groups': len(medium_priority),
        'consolidation_groups': groups,
        'comparison_with_existing': comparison,
        'summary': {
            'duplicate_names': len([g for g in groups if g['type'] == 'duplicate_name']),
            'similar_names': len([g for g in groups if g['type'] == 'similar_name']),
            'domain_groups': len([g for g in groups if g['type'] == 'domain_group']),
        }
    }
    
    # Save report
    output_path = Path('agent_workspaces/Agent-1/repo_consolidation_enhanced.json')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2))
    
    print(f"\n✅ Analysis complete!")
    print(f"   Total repos analyzed: {report['total_repos_analyzed']}")
    print(f"   Consolidation groups found: {report['total_consolidation_groups']}")
    print(f"   Potential reduction: {report['potential_reduction']} repos")
    print(f"   High priority: {report['high_priority_groups']} groups")
    print(f"   Medium priority: {report['medium_priority_groups']} groups")
    print()
    print(f"📊 New findings:")
    print(f"   New groups: {comparison['total_new']}")
    print(f"   Updated groups: {comparison['total_updated']}")
    print()
    print(f"📄 Full report saved to: {output_path}")
    
    # Print summary
    print("\n📋 Consolidation Groups Summary:")
    print("-" * 70)
    for i, group in enumerate(groups[:15], 1):  # Show first 15
        print(f"\n{i}. {group['type']} - {group['priority']} Priority - {group.get('category', 'N/A')}")
        print(f"   Target: {group['target_repo']} (#{group.get('target_num', '?')})")
        merge_from = group.get('merge_from', [])
        if merge_from:
            merge_names = [f"{m['name']} (#{m.get('num', '?')})" for m in merge_from[:3]]
            print(f"   Merge from: {', '.join(merge_names)}")
            if len(merge_from) > 3:
                print(f"   ... and {len(merge_from) - 3} more")
        print(f"   Reduction: {group['reduction']} repos")
        if group.get('notes'):
            print(f"   Note: {group['notes']}")
    
    if len(groups) > 15:
        print(f"\n   ... and {len(groups) - 15} more groups")
    
    return report


if __name__ == '__main__':
    main()


