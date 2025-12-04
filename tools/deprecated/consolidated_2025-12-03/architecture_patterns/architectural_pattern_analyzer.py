#!/usr/bin/env python3
"""
Architectural Pattern Analyzer for Repo Consolidation
======================================================

Analyzes GitHub repos for architectural patterns to identify consolidation opportunities
beyond name/purpose similarity. Focuses on:
- Similar architecture patterns
- Shared component opportunities
- Overlapping design patterns
- Common frameworks/structures

Author: Agent-2 (Architecture & Design Specialist)
Date: 2025-01-27
Builds on: Agent-8's consolidation work
"""

import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

def load_master_repo_list() -> List[Dict[str, Any]]:
    """Load master repository list."""
    master_list_path = Path('data/github_75_repos_master_list.json')
    if master_list_path.exists():
        data = json.loads(master_list_path.read_text(encoding='utf-8'))
        return data.get('repos', [])
    return []

def load_repo_analyses() -> Dict[str, Dict[str, Any]]:
    """Load all repository analysis devlogs."""
    analyses = {}
    devlogs_path = Path('swarm_brain/devlogs/repository_analysis')
    
    if devlogs_path.exists():
        for devlog_file in devlogs_path.glob('*.md'):
            try:
                content = devlog_file.read_text(encoding='utf-8')
                # Extract repo name and number
                repo_name = None
                repo_num = None
                
                # Try to extract from filename
                filename = devlog_file.stem
                if 'repo' in filename.lower():
                    # Look for repo number
                    num_match = re.search(r'repo[#_\-\s]*(\d+)', filename, re.IGNORECASE)
                    if num_match:
                        repo_num = int(num_match.group(1))
                
                # Try to extract from content
                for line in content.split('\n')[:50]:
                    if 'repo' in line.lower() and ('#' in line or ':' in line):
                        # Try to extract repo number and name
                        match = re.search(r'repo[#:\s]+(\d+)[\s:]+([^\s]+)', line, re.IGNORECASE)
                        if match:
                            repo_num = int(match.group(1))
                            repo_name = match.match.group(2).strip()
                            break
                        # Or just repo name
                        match = re.search(r'repo[#:\s]+\d+[\s:]+([^\s]+)', line, re.IGNORECASE)
                        if match:
                            repo_name = match.group(1).strip()
                
                if repo_name or repo_num:
                    key = repo_name.lower() if repo_name else f"repo_{repo_num}"
                    analyses[key] = {
                        'name': repo_name or f"repo_{repo_num}",
                        'num': repo_num,
                        'filename': devlog_file.name,
                        'content': content,
                        'analyzed': True
                    }
            except Exception as e:
                continue
    
    return analyses

def extract_architectural_patterns(content: str) -> Dict[str, Any]:
    """Extract architectural patterns from repo analysis content."""
    patterns = {
        'framework': [],
        'architecture_style': [],
        'components': [],
        'patterns': [],
        'tech_stack': [],
        'structure': [],
        'database': [],
        'integration': []
    }
    
    content_lower = content.lower()
    
    # Framework detection (more comprehensive)
    frameworks = {
        'fastapi': ['fastapi', 'fast api'],
        'flask': ['flask'],
        'django': ['django'],
        'react': ['react'],
        'vue': ['vue'],
        'angular': ['angular'],
        'express': ['express'],
        'next.js': ['next.js', 'nextjs'],
        'pyqt': ['pyqt', 'pyqt6', 'pyqt5'],
        'tkinter': ['tkinter'],
        'discord.py': ['discord.py', 'discord', 'discord bot'],
        'selenium': ['selenium', 'webdriver'],
        'opencv': ['opencv', 'cv2'],
        'beautifulsoup': ['beautifulsoup', 'bs4']
    }
    for fw, keywords in frameworks.items():
        if any(kw in content_lower for kw in keywords):
            patterns['framework'].append(fw)
    
    # Architecture style detection (enhanced)
    arch_styles = {
        'mvc': ['mvc', 'model-view-controller'],
        'mvp': ['mvp', 'model-view-presenter'],
        'mvvm': ['mvvm'],
        'microservices': ['microservices', 'micro service'],
        'monolith': ['monolith', 'monolithic'],
        'plugin': ['plugin', 'plugin architecture', 'plugin system', 'plugin-based'],
        'modular': ['modular', 'modular architecture', 'modular design'],
        'layered': ['layered', 'layered architecture'],
        'event-driven': ['event-driven', 'event driven', 'event loop'],
        'rest': ['rest', 'rest api', 'restful'],
        'graphql': ['graphql'],
        'pipeline': ['pipeline', 'processing pipeline', 'data pipeline']
    }
    for style, keywords in arch_styles.items():
        if any(kw in content_lower for kw in keywords):
            patterns['architecture_style'].append(style)
    
    # Component detection (enhanced)
    components = {
        'api': ['api', 'rest api', 'endpoint'],
        'bot': ['bot', 'discord bot', 'telegram bot'],
        'scraper': ['scraper', 'scraping', 'web scraping', 'selenium'],
        'analyzer': ['analyzer', 'analysis', 'data analysis'],
        'database': ['database', 'db', 'sqlite', 'postgresql', 'mongodb'],
        'cache': ['cache', 'caching', 'redis'],
        'queue': ['queue', 'message queue', 'job queue'],
        'scheduler': ['scheduler', 'scheduling', 'cron'],
        'monitor': ['monitor', 'monitoring', 'health check'],
        'dashboard': ['dashboard', 'web ui', 'web interface'],
        'gui': ['gui', 'graphical interface', 'pyqt', 'tkinter'],
        'cli': ['cli', 'command line', 'terminal'],
        'training': ['training', 'train', 'model training', 'ai training'],
        'automation': ['automation', 'automated', 'auto']
    }
    for comp, keywords in components.items():
        if any(kw in content_lower for kw in keywords):
            patterns['components'].append(comp)
    
    # Design pattern detection (enhanced)
    design_patterns = {
        'singleton': ['singleton'],
        'factory': ['factory', 'factory pattern'],
        'observer': ['observer', 'observer pattern'],
        'strategy': ['strategy', 'strategy pattern'],
        'adapter': ['adapter', 'adapter pattern'],
        'facade': ['facade', 'facade pattern'],
        'repository': ['repository', 'repository pattern'],
        'service': ['service', 'service layer'],
        'controller': ['controller', 'controller pattern']
    }
    for pattern, keywords in design_patterns.items():
        if any(kw in content_lower for kw in keywords):
            patterns['patterns'].append(pattern)
    
    # Database detection
    databases = {
        'sqlite': ['sqlite', 'sqlite3'],
        'postgresql': ['postgresql', 'postgres'],
        'mongodb': ['mongodb', 'mongo'],
        'mysql': ['mysql'],
        'redis': ['redis']
    }
    for db, keywords in databases.items():
        if any(kw in content_lower for kw in keywords):
            patterns['database'].append(db)
    
    # Integration detection
    integrations = {
        'discord': ['discord', 'discord.py', 'discord bot'],
        'github': ['github', 'github actions', 'ci/cd'],
        'obs': ['obs', 'open broadcaster'],
        'twitch': ['twitch', 'streaming'],
        'selenium': ['selenium', 'webdriver'],
        'openai': ['openai', 'gpt', 'chatgpt'],
        'api': ['api integration', 'external api']
    }
    for integration, keywords in integrations.items():
        if any(kw in content_lower for kw in keywords):
            patterns['integration'].append(integration)
    
    # Tech stack detection (enhanced)
    tech_keywords = ['python', 'javascript', 'typescript', 'node', 'postgresql', 'sqlite', 'mongodb', 'redis', 'docker', 'kubernetes', 'html', 'css']
    for tech in tech_keywords:
        if tech in content_lower:
            patterns['tech_stack'].append(tech)
    
    # Structure detection (enhanced)
    structure_keywords = ['src/', 'lib/', 'modules/', 'services/', 'controllers/', 'models/', 'views/', 'utils/', 'core/', 'tests/', 'docs/']
    for struct in structure_keywords:
        if struct in content_lower:
            patterns['structure'].append(struct.replace('/', ''))
    
    return patterns

def find_architectural_similarities(repos: List[Dict[str, Any]], analyses: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Find repos with similar architectural patterns."""
    architectural_groups = defaultdict(list)
    
    # Extract patterns for each repo
    repo_patterns = {}
    for repo in repos:
        if repo.get('analyzed'):
            repo_name = repo.get('name', '').lower()
            repo_num = repo.get('num')
            
            # Find analysis
            analysis = None
            if repo_name in analyses:
                analysis = analyses[repo_name]
            elif repo_num:
                # Try to find by number
                for key, anal in analyses.items():
                    if anal.get('num') == repo_num:
                        analysis = anal
                        break
            
            if analysis:
                patterns = extract_architectural_patterns(analysis.get('content', ''))
                repo_patterns[repo_name] = {
                    'repo': repo,
                    'patterns': patterns
                }
    
    # Group by similar patterns
    # Group 1: Same framework
    framework_groups = defaultdict(list)
    for repo_name, data in repo_patterns.items():
        frameworks = data['patterns'].get('framework', [])
        if frameworks:
            key = tuple(sorted(frameworks))
            framework_groups[key].append(data['repo'])
    
    # Group 2: Same architecture style
    arch_style_groups = defaultdict(list)
    for repo_name, data in repo_patterns.items():
        styles = data['patterns'].get('architecture_style', [])
        if styles:
            key = tuple(sorted(styles))
            arch_style_groups[key].append(data['repo'])
    
    # Group 3: Similar components
    component_groups = defaultdict(list)
    for repo_name, data in repo_patterns.items():
        components = data['patterns'].get('components', [])
        if len(components) >= 2:  # Only group if has multiple components
            key = tuple(sorted(components))
            component_groups[key].append(data['repo'])
    
    # Group 4: Same tech stack
    tech_stack_groups = defaultdict(list)
    for repo_name, data in repo_patterns.items():
        tech_stack = data['patterns'].get('tech_stack', [])
        if len(tech_stack) >= 2:  # Only group if has multiple tech items
            key = tuple(sorted(tech_stack))
            tech_stack_groups[key].append(data['repo'])
    
    # Build consolidation opportunities
    opportunities = []
    
    # Framework-based opportunities
    for frameworks, repo_list in framework_groups.items():
        if len(repo_list) >= 2:
            # Check if not already in Agent-8's groups
            repo_names = [r.get('name', '') for r in repo_list]
            # Filter out repos already in consolidation plan
            filtered_repos = [r for r in repo_list if not _is_in_existing_plan(r)]
            
            if len(filtered_repos) >= 2:
                primary = max(filtered_repos, key=lambda r: r.get('goldmine', False) or r.get('num', 0))
                secondary = [r for r in filtered_repos if r.get('name') != primary.get('name')]
                
                if secondary:
                    opportunities.append({
                        'type': 'architectural_framework',
                        'priority': 'MEDIUM',
                        'target': primary.get('name'),
                        'merge_from': [r.get('name') for r in secondary],
                        'repos': filtered_repos,
                        'reduction': len(secondary),
                        'reason': f'Same framework: {", ".join(frameworks)}',
                        'architectural_basis': 'framework'
                    })
    
    # Architecture style opportunities
    for styles, repo_list in arch_style_groups.items():
        if len(repo_list) >= 2:
            filtered_repos = [r for r in repo_list if not _is_in_existing_plan(r)]
            
            if len(filtered_repos) >= 2:
                primary = max(filtered_repos, key=lambda r: r.get('goldmine', False) or r.get('num', 0))
                secondary = [r for r in filtered_repos if r.get('name') != primary.get('name')]
                
                if secondary:
                    opportunities.append({
                        'type': 'architectural_style',
                        'priority': 'MEDIUM',
                        'target': primary.get('name'),
                        'merge_from': [r.get('name') for r in secondary],
                        'repos': filtered_repos,
                        'reduction': len(secondary),
                        'reason': f'Same architecture style: {", ".join(styles)}',
                        'architectural_basis': 'architecture_style'
                    })
    
    # Component-based opportunities
    for components, repo_list in component_groups.items():
        if len(repo_list) >= 2:
            filtered_repos = [r for r in repo_list if not _is_in_existing_plan(r)]
            
            if len(filtered_repos) >= 2:
                primary = max(filtered_repos, key=lambda r: r.get('goldmine', False) or r.get('num', 0))
                secondary = [r for r in filtered_repos if r.get('name') != primary.get('name')]
                
                if secondary:
                    opportunities.append({
                        'type': 'shared_components',
                        'priority': 'MEDIUM',
                        'target': primary.get('name'),
                        'merge_from': [r.get('name') for r in secondary],
                        'repos': filtered_repos,
                        'reduction': len(secondary),
                        'reason': f'Similar components: {", ".join(components[:5])}',
                        'architectural_basis': 'components'
                    })
    
    # Tech stack opportunities
    for tech_stack, repo_list in tech_stack_groups.items():
        if len(repo_list) >= 2:
            filtered_repos = [r for r in repo_list if not _is_in_existing_plan(r)]
            
            if len(filtered_repos) >= 2:
                primary = max(filtered_repos, key=lambda r: r.get('goldmine', False) or r.get('num', 0))
                secondary = [r for r in filtered_repos if r.get('name') != primary.get('name')]
                
                if secondary:
                    opportunities.append({
                        'type': 'tech_stack',
                        'priority': 'LOW',
                        'target': primary.get('name'),
                        'merge_from': [r.get('name') for r in secondary],
                        'repos': filtered_repos,
                        'reduction': len(secondary),
                        'reason': f'Same tech stack: {", ".join(tech_stack[:5])}',
                        'architectural_basis': 'tech_stack'
                    })
    
    return opportunities

def _is_in_existing_plan(repo: Dict[str, Any]) -> bool:
    """Check if repo is already in Agent-8's consolidation plan."""
    repo_name = repo.get('name', '').lower()
    
    # Load existing plan
    plan_path = Path('agent_workspaces/Agent-8/REPO_CONSOLIDATION_PLAN.json')
    if plan_path.exists():
        try:
            plan = json.loads(plan_path.read_text(encoding='utf-8'))
            # Check if repo is in any consolidation group
            if 'consolidation_groups' in plan:
                for group in plan.get('consolidation_groups', []):
                    if 'target' in group and group['target'].lower() == repo_name:
                        return True
                    if 'merge_from' in group:
                        for merge_repo in group['merge_from']:
                            if merge_repo.lower() == repo_name:
                                return True
        except Exception:
            pass
    
    # Also check strategy document
    strategy_path = Path('agent_workspaces/Agent-8/REPO_CONSOLIDATION_STRATEGY.md')
    if strategy_path.exists():
        try:
            content = strategy_path.read_text(encoding='utf-8')
            if repo_name in content.lower():
                return True
        except Exception:
            pass
    
    return False

def analyze_shared_component_opportunities(repos: List[Dict[str, Any]], analyses: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Identify repos that could share common components."""
    opportunities = []
    
    # Find repos with similar component needs
    component_needs = defaultdict(list)
    
    for repo in repos:
        if repo.get('analyzed'):
            repo_name = repo.get('name', '').lower()
            analysis = analyses.get(repo_name)
            
            if analysis:
                content = analysis.get('content', '').lower()
                
                # Identify component needs
                needs = []
                if 'api' in content or 'rest' in content:
                    needs.append('api')
                if 'database' in content or 'db' in content:
                    needs.append('database')
                if 'bot' in content or 'discord' in content:
                    needs.append('bot_framework')
                if 'scraper' in content or 'scraping' in content:
                    needs.append('scraper')
                if 'analyzer' in content or 'analysis' in content:
                    needs.append('analyzer')
                if 'gui' in content or 'interface' in content:
                    needs.append('gui')
                
                if needs:
                    key = tuple(sorted(needs))
                    component_needs[key].append(repo)
    
    # Find groups with similar component needs
    for needs, repo_list in component_needs.items():
        if len(repo_list) >= 2:
            filtered_repos = [r for r in repo_list if not _is_in_existing_plan(r)]
            
            if len(filtered_repos) >= 2:
                opportunities.append({
                    'type': 'shared_component_opportunity',
                    'priority': 'MEDIUM',
                    'repos': filtered_repos,
                    'shared_components': list(needs),
                    'reason': f'Could share components: {", ".join(needs)}',
                    'recommendation': f'Create shared component library for: {", ".join(needs)}'
                })
    
    return opportunities

def main():
    """Main architectural pattern analysis."""
    print("🏗️  Architectural Pattern Analyzer - Agent-2")
    print("=" * 70)
    print("Analyzing repos for architectural consolidation opportunities...")
    print()
    
    # Load data
    repos = load_master_repo_list()
    analyses = load_repo_analyses()
    
    print(f"📊 Loaded {len(repos)} repos from master list")
    print(f"📊 Found {len(analyses)} analyzed repos")
    print()
    
    # Find architectural similarities
    print("🔍 Analyzing architectural patterns...")
    arch_opportunities = find_architectural_similarities(repos, analyses)
    print(f"   Found {len(arch_opportunities)} architectural consolidation opportunities")
    
    # Find shared component opportunities
    print("🔍 Analyzing shared component opportunities...")
    component_opportunities = analyze_shared_component_opportunities(repos, analyses)
    print(f"   Found {len(component_opportunities)} shared component opportunities")
    
    # Generate report
    total_reduction = sum(opp.get('reduction', 0) for opp in arch_opportunities)
    
    report = {
        'analysis_date': '2025-01-27',
        'analyzer': 'Agent-2',
        'focus': 'Architectural patterns and design patterns',
        'total_repos_analyzed': len([r for r in repos if r.get('analyzed')]),
        'architectural_opportunities': len(arch_opportunities),
        'shared_component_opportunities': len(component_opportunities),
        'potential_reduction': total_reduction,
        'architectural_consolidation_groups': arch_opportunities,
        'shared_component_opportunities': component_opportunities
    }
    
    # Save report
    output_path = Path('agent_workspaces/Agent-2/architectural_consolidation_analysis.json')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2))
    
    print()
    print("✅ Architectural analysis complete!")
    print(f"   Architectural opportunities: {len(arch_opportunities)}")
    print(f"   Shared component opportunities: {len(component_opportunities)}")
    print(f"   Potential reduction: {total_reduction} repos")
    print()
    print(f"📄 Full report saved to: {output_path}")
    
    # Print summary
    if arch_opportunities:
        print()
        print("📋 Architectural Consolidation Opportunities:")
        print("-" * 70)
        for i, opp in enumerate(arch_opportunities[:10], 1):
            print(f"\n{i}. {opp['type']} - {opp['priority']} Priority")
            print(f"   Target: {opp['target']}")
            print(f"   Merge from: {', '.join(opp['merge_from'][:3])}")
            print(f"   Reduction: {opp['reduction']} repos")
            print(f"   Reason: {opp['reason']}")
    
    if component_opportunities:
        print()
        print("📋 Shared Component Opportunities:")
        print("-" * 70)
        for i, opp in enumerate(component_opportunities[:5], 1):
            print(f"\n{i}. {opp['type']}")
            print(f"   Repos: {len(opp['repos'])} repos")
            print(f"   Shared components: {', '.join(opp['shared_components'])}")
            print(f"   Recommendation: {opp['recommendation']}")
    
    return report

if __name__ == '__main__':
    main()

