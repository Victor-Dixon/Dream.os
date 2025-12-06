#!/usr/bin/env python3
"""
Comprehensive Repository Consolidation Analysis
===============================================

Analyzes ALL 75 repositories to create comprehensive similarity matrix
and identify additional overlaps beyond existing consolidation groups.

Uses GitHub book viewer data and all available repository analyses.

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-01-27
Mission: Complete comprehensive GitHub repo consolidation analysis
"""

import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple
from difflib import SequenceMatcher
from itertools import combinations


def similarity_score(str1: str, str2: str) -> float:
    """Calculate similarity between two strings (0-1)."""
    return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()


def normalize_name(name: str) -> str:
    """Normalize repo name for comparison."""
    # Remove emojis, special chars, normalize case/hyphens/underscores
    normalized = re.sub(r'[^\w\s-]', '', str(name))
    normalized = normalized.lower().replace('-', '_').replace(' ', '_')
    return normalized.strip('_')


def extract_repo_number_from_filename(filename: str) -> int | None:
    """Extract repo number from filename."""
    patterns = [
        r"repo[_\s]*(\d+)",
        r"Repo[_\s]*(\d+)",
        r"repo[_\s]*#(\d+)",
        r"Repo[_\s]*#(\d+)",
        r"analysis[_\s]*(\d+)",
        r"REPO[_\s]*(\d+)",
    ]
    
    for pattern in patterns:
        match = re.search(pattern, filename, re.IGNORECASE)
        if match:
            try:
                return int(match.group(1))
            except ValueError:
                continue
    
    # Try to extract from patterns like "repo_01", "Repo_21", etc.
    match = re.search(r'_(\d{1,2})[_-]', filename)
    if match:
        try:
            return int(match.group(1))
        except ValueError:
            pass
    
    return None


def load_all_repos(devlogs_path: Path) -> Dict[int, Dict[str, Any]]:
    """Load all repository data from devlogs."""
    repos = {}
    
    if not devlogs_path.exists():
        return repos
    
    for devlog_file in sorted(devlogs_path.glob("*.md")):
        try:
            repo_num = extract_repo_number_from_filename(devlog_file.name)
            if not repo_num:
                continue
            
            content = devlog_file.read_text(encoding='utf-8')
            lines = content.split('\n')
            
            # Extract repo name
            repo_name = extract_repo_name(devlog_file.name, content)
            
            # Extract tech stack
            tech_stack = extract_tech_stack(content)
            
            # Extract purpose
            purpose = extract_purpose(content, lines)
            
            # Extract category
            category = extract_category(content, lines)
            
            repos[repo_num] = {
                'repo_num': repo_num,
                'name': repo_name,
                'filename': devlog_file.name,
                'tech_stack': tech_stack,
                'purpose': purpose,
                'category': category,
                'content': content[:1000],  # First 1000 chars
                'full_content': content,
            }
        except Exception as e:
            print(f"Error loading {devlog_file.name}: {e}")
            continue
    
    return repos


def extract_repo_name(filename: str, content: str) -> str:
    """Extract repo name from filename or content."""
    # Try patterns in content first
    patterns = [
        r'Repo[_\s]*#?\s*(\d+)[:\s]+([^\n]+)',
        r'Repository[:\s]+([^\n]+)',
        r'Repo[:\s]+([^\n]+)',
        r'##\s+([^\n]+)',
        r'#\s+([^\n]+)',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, content[:500], re.IGNORECASE)
        if matches:
            name = matches[0][-1] if isinstance(matches[0], tuple) else matches[0]
            name = name.strip(':#-*')
            if name and len(name) < 100:
                return name
    
    # Try filename
    parts = filename.split('_')
    if len(parts) > 1:
        # Find the repo name part
        for part in reversed(parts):
            if part and not part.isdigit() and len(part) > 2:
                return part.replace('-', ' ').title()
    
    return filename.split('.')[0]


def extract_tech_stack(content: str) -> List[str]:
    """Extract technology stack from content."""
    tech_keywords = [
        'Python', 'JavaScript', 'TypeScript', 'React', 'Node.js', 'Node',
        'FastAPI', 'Flask', 'Django', 'Express',
        'Discord', 'discord.py', 'Discord.py',
        'PostgreSQL', 'MySQL', 'SQLite', 'MongoDB', 'Redis',
        'Docker', 'Kubernetes', 'AWS', 'Azure', 'GCP',
        'TensorFlow', 'PyTorch', 'scikit-learn', 'sklearn',
        'Selenium', 'BeautifulSoup', 'requests',
        'PyQt', 'PyQt5', 'Tkinter', 'GUI',
    ]
    
    tech_stack = []
    content_lower = content.lower()
    
    for tech in tech_keywords:
        if tech.lower() in content_lower:
            tech_stack.append(tech)
    
    return list(set(tech_stack))


def extract_purpose(content: str, lines: List[str]) -> str:
    """Extract repository purpose."""
    purpose_keywords = ['Purpose', 'purpose', '🎯 Purpose', 'Primary Function', 'Core Mission']
    
    for i, line in enumerate(lines[:50]):
        for keyword in purpose_keywords:
            if keyword in line:
                # Get next non-empty line
                for j in range(i + 1, min(i + 10, len(lines))):
                    next_line = lines[j].strip()
                    if next_line and not next_line.startswith('#'):
                        return next_line.strip('-* ')[:300]
    
    # Try to extract from content patterns
    patterns = [
        r'Purpose[:\s]+([^\n]+)',
        r'What it is[:\s]+([^\n]+)',
        r'Primary Function[:\s]+([^\n]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, content[:1000], re.IGNORECASE)
        if match:
            return match.group(1).strip()[:300]
    
    return ""


def extract_category(content: str, lines: List[str]) -> str:
    """Extract repository category."""
    content_lower = content.lower()
    
    # Category keywords
    if any(word in content_lower for word in ['trading', 'trade', 'stock', 'options', 'portfolio']):
        return 'trading'
    elif any(word in content_lower for word in ['discord', 'bot', 'chatbot']):
        return 'discord'
    elif any(word in content_lower for word in ['automation', 'automate', 'script']):
        return 'automation'
    elif any(word in content_lower for word in ['ml', 'machine learning', 'neural', 'model', 'ai', 'deep learning']):
        return 'ml'
    elif any(word in content_lower for word in ['web', 'website', 'frontend', 'backend']):
        return 'web'
    elif any(word in content_lower for word in ['game', 'gaming', 'stream', 'youtube']):
        return 'gaming'
    else:
        return 'other'


def create_similarity_matrix(repos: Dict[int, Dict[str, Any]]) -> Dict[Tuple[int, int], float]:
    """Create similarity matrix for all repos."""
    matrix = {}
    repo_list = list(repos.items())
    
    for (num1, repo1), (num2, repo2) in combinations(repo_list, 2):
        if num1 >= num2:
            continue
        
        # Calculate similarity scores
        name_sim = similarity_score(normalize_name(repo1['name']), normalize_name(repo2['name']))
        
        # Tech stack similarity
        tech1 = set(repo1.get('tech_stack', []))
        tech2 = set(repo2.get('tech_stack', []))
        tech_sim = len(tech1 & tech2) / max(len(tech1 | tech2), 1) if (tech1 or tech2) else 0
        
        # Purpose similarity
        purpose1 = repo1.get('purpose', '').lower()
        purpose2 = repo2.get('purpose', '').lower()
        purpose_sim = similarity_score(purpose1, purpose2) if (purpose1 and purpose2) else 0
        
        # Category match
        cat_match = 1.0 if repo1.get('category') == repo2.get('category') and repo1.get('category') != 'other' else 0
        
        # Weighted similarity score
        total_sim = (
            name_sim * 0.4 +  # Name similarity (40%)
            tech_sim * 0.3 +  # Tech stack (30%)
            purpose_sim * 0.2 +  # Purpose (20%)
            cat_match * 0.1  # Category (10%)
        )
        
        if total_sim > 0.3:  # Only store if similarity > 30%
            matrix[(num1, num2)] = total_sim
    
    return matrix


def find_consolidation_groups(repos: Dict[int, Dict[str, Any]], 
                              similarity_matrix: Dict[Tuple[int, int], float],
                              threshold: float = 0.5) -> List[Dict[str, Any]]:
    """Find consolidation groups based on similarity matrix."""
    groups = []
    processed = set()
    
    # Sort by similarity score (highest first)
    sorted_pairs = sorted(similarity_matrix.items(), key=lambda x: x[1], reverse=True)
    
    for (num1, num2), sim_score in sorted_pairs:
        if num1 in processed or num2 in processed:
            continue
        
        if sim_score < threshold:
            continue
        
        # Create group
        repo1 = repos[num1]
        repo2 = repos[num2]
        
        # Determine which should be target (prefer more complete info)
        if len(repo1.get('content', '')) > len(repo2.get('content', '')):
            target = num1
            merge_from = num2
        else:
            target = num2
            merge_from = num1
        
        group = {
            'target_repo': target,
            'target_name': repos[target]['name'],
            'merge_from': [merge_from],
            'merge_from_names': [repos[merge_from]['name']],
            'similarity_score': sim_score,
            'name_similarity': similarity_score(
                normalize_name(repos[target]['name']), 
                normalize_name(repos[merge_from]['name'])
            ),
            'tech_match': bool(set(repos[target].get('tech_stack', [])) & 
                              set(repos[merge_from].get('tech_stack', []))),
            'category_match': repos[target].get('category') == repos[merge_from].get('category'),
        }
        
        groups.append(group)
        processed.add(num1)
        processed.add(num2)
    
    return groups


def analyze_all_repos():
    """Comprehensive analysis of all repos."""
    devlogs_path = Path('swarm_brain/devlogs/repository_analysis')
    
    print("🔍 Loading all repository analyses...")
    repos = load_all_repos(devlogs_path)
    
    print(f"✅ Loaded {len(repos)} repositories")
    print(f"   Repo numbers: {sorted(repos.keys())}")
    
    # Find missing repos (1-75)
    all_repo_nums = set(range(1, 76))
    found_repo_nums = set(repos.keys())
    missing_repos = sorted(all_repo_nums - found_repo_nums)
    
    if missing_repos:
        print(f"⚠️  Missing repo analyses: {missing_repos}")
        print(f"   Total found: {len(found_repo_nums)}/75")
    else:
        print("✅ All 75 repos found!")
    
    # Create similarity matrix
    print("\n📊 Creating similarity matrix...")
    similarity_matrix = create_similarity_matrix(repos)
    print(f"✅ Similarity matrix created: {len(similarity_matrix)} similar pairs found")
    
    # Find consolidation groups at different thresholds
    print("\n🔍 Finding consolidation groups...")
    
    high_threshold_groups = find_consolidation_groups(repos, similarity_matrix, threshold=0.7)
    medium_threshold_groups = find_consolidation_groups(repos, similarity_matrix, threshold=0.5)
    low_threshold_groups = find_consolidation_groups(repos, similarity_matrix, threshold=0.3)
    
    print(f"✅ High similarity (>0.7): {len(high_threshold_groups)} groups")
    print(f"✅ Medium similarity (>0.5): {len(medium_threshold_groups)} groups")
    print(f"✅ Low similarity (>0.3): {len(low_threshold_groups)} groups")
    
    # Categorize by type
    categories = defaultdict(int)
    for repo in repos.values():
        categories[repo.get('category', 'other')] += 1
    
    print("\n📊 Repository Categories:")
    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        print(f"   {cat}: {count}")
    
    # Create comprehensive report
    report = {
        'analysis_date': '2025-01-27',
        'analyzer': 'Agent-5',
        'total_repos_analyzed': len(repos),
        'missing_repos': missing_repos,
        'categories': dict(categories),
        'similarity_matrix_size': len(similarity_matrix),
        'consolidation_groups': {
            'high_similarity': high_threshold_groups,
            'medium_similarity': medium_threshold_groups,
            'low_similarity': low_threshold_groups,
        },
        'all_repos': {num: {
            'name': repo['name'],
            'category': repo.get('category', 'other'),
            'tech_stack': repo.get('tech_stack', []),
            'purpose': repo.get('purpose', '')[:200],
        } for num, repo in repos.items()},
        'top_similar_pairs': sorted(similarity_matrix.items(), key=lambda x: x[1], reverse=True)[:50],
    }
    
    return report


def main():
    """Main analysis function."""
    print("=" * 70)
    print("📦 COMPREHENSIVE REPOSITORY CONSOLIDATION ANALYSIS")
    print("=" * 70)
    print()
    
    report = analyze_all_repos()
    
    # Save report
    output_path = Path('agent_workspaces/Agent-5/comprehensive_repo_analysis_data.json')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2))
    
    print(f"\n✅ Analysis complete!")
    print(f"📄 Data saved to: {output_path}")
    
    # Print summary
    print("\n📊 Summary:")
    print(f"   Total repos analyzed: {report['total_repos_analyzed']}/75")
    print(f"   Missing repos: {len(report['missing_repos'])}")
    print(f"   High similarity groups: {len(report['consolidation_groups']['high_similarity'])}")
    print(f"   Medium similarity groups: {len(report['consolidation_groups']['medium_similarity'])}")
    print(f"   Low similarity groups: {len(report['consolidation_groups']['low_similarity'])}")
    
    return report


if __name__ == '__main__':
    main()


