#!/usr/bin/env python3
"""
Integration Pattern Analyzer
============================

Analyzes GitHub repos for integration patterns to identify consolidation opportunities.
Focuses on repos that:
1. Have similar integration needs
2. Could share integration code
3. Could merge into core systems
4. Are already integrated into V2

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-01-27
Priority: HIGH
"""

import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Set


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


def check_repo_integrated_into_v2(repo_name: str) -> Dict[str, Any]:
    """Check if a repo is already integrated into V2."""
    integrated_repos = {
        'projectscanner': {
            'integrated': True,
            'location': 'tools/projectscanner*.py',
            'status': 'Fully integrated',
            'note': 'Core project scanning functionality'
        },
        'network-scanner': {
            'integrated': False,
            'potential_location': 'src/core/health/monitoring/',
            'status': 'Could integrate',
            'note': 'Network monitoring could be part of health system'
        },
        'contract-leads': {
            'integrated': False,
            'potential_location': 'src/services/contract_system/',
            'status': 'Could integrate',
            'note': 'Contract system already exists'
        },
        'prompt-library': {
            'integrated': False,
            'potential_location': 'swarm_brain/',
            'status': 'Could integrate',
            'note': 'Could be part of swarm brain knowledge'
        },
        'gpt_automation': {
            'integrated': False,
            'potential_location': 'src/services/',
            'status': 'Could integrate',
            'note': 'Automation service could be consolidated'
        },
        'IT_help_desk': {
            'integrated': False,
            'potential_location': 'src/services/',
            'status': 'Could integrate',
            'note': 'Help desk could be service layer'
        }
    }
    
    normalized = repo_name.lower().replace('-', '_').replace(' ', '_')
    return integrated_repos.get(normalized, {
        'integrated': False,
        'status': 'Not integrated',
        'note': 'No integration found'
    })


def categorize_by_integration_pattern(repos: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Categorize repos by integration patterns."""
    patterns = defaultdict(list)
    
    for repo in repos:
        name = repo.get('name', '').lower()
        
        # Discord integration repos
        if any(word in name for word in ['discord', 'bot', 'commander']):
            patterns['discord_integration'].append(repo)
        
        # GitHub integration repos
        elif any(word in name for word in ['github', 'repo', 'repository']):
            patterns['github_integration'].append(repo)
        
        # Messaging/communication repos
        elif any(word in name for word in ['message', 'messaging', 'communication', 'chat']):
            patterns['messaging_integration'].append(repo)
        
        # Automation repos
        elif any(word in name for word in ['automation', 'automate', 'gpt_automation', 'script']):
            patterns['automation_integration'].append(repo)
        
        # API/integration repos
        elif any(word in name for word in ['api', 'integration', 'webhook', 'service']):
            patterns['api_integration'].append(repo)
        
        # Monitoring/health repos
        elif any(word in name for word in ['monitor', 'health', 'scanner', 'network']):
            patterns['monitoring_integration'].append(repo)
        
        # Database/data repos
        elif any(word in name for word in ['database', 'data', 'storage', 'db']):
            patterns['data_integration'].append(repo)
        
        # Contract/lead repos
        elif any(word in name for word in ['contract', 'lead', 'trading-leads']):
            patterns['contract_integration'].append(repo)
        
        # Tool/utility repos
        elif any(word in name for word in ['tool', 'utility', 'helper', 'scanner']):
            patterns['utility_integration'].append(repo)
    
    return patterns


def find_shared_integration_code(repos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Find repos that could share integration code."""
    shared_integrations = []
    
    # Discord bots that could share code
    discord_repos = [r for r in repos if 'discord' in r.get('name', '').lower() or 'bot' in r.get('name', '').lower()]
    if len(discord_repos) > 1:
        shared_integrations.append({
            'type': 'shared_integration',
            'category': 'discord_bots',
            'repos': discord_repos,
            'shared_code': 'Discord API client, command handling, event system',
            'consolidation_opportunity': 'All Discord bots could use unified_discord_bot.py',
            'target': 'unified_discord_bot.py (already exists)',
            'reduction': len(discord_repos) - 1
        })
    
    # Automation repos that could share code
    automation_repos = [r for r in repos if 'automation' in r.get('name', '').lower() or 'gpt_automation' in r.get('name', '').lower()]
    if len(automation_repos) > 1:
        shared_integrations.append({
            'type': 'shared_integration',
            'category': 'automation',
            'repos': automation_repos,
            'shared_code': 'GPT API client, automation patterns, task execution',
            'consolidation_opportunity': 'Could merge into unified automation service',
            'target': 'src/services/automation/',
            'reduction': len(automation_repos) - 1
        })
    
    # Scanner/monitoring repos
    scanner_repos = [r for r in repos if 'scanner' in r.get('name', '').lower() or 'network' in r.get('name', '').lower()]
    if len(scanner_repos) > 1:
        shared_integrations.append({
            'type': 'shared_integration',
            'category': 'monitoring',
            'repos': scanner_repos,
            'shared_code': 'Network scanning, health checks, monitoring patterns',
            'consolidation_opportunity': 'Could merge into health monitoring system',
            'target': 'src/core/health/monitoring/',
            'reduction': len(scanner_repos) - 1
        })
    
    return shared_integrations


def find_core_system_merges(repos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Find repos that could merge into core systems."""
    core_merges = []
    
    # Repos that could merge into messaging system
    messaging_repos = [r for r in repos if any(word in r.get('name', '').lower() for word in ['message', 'chat', 'communication'])]
    if messaging_repos:
        core_merges.append({
            'type': 'core_system_merge',
            'target_system': 'Messaging Infrastructure',
            'target_location': 'src/services/messaging_infrastructure.py',
            'repos': messaging_repos,
            'rationale': 'All messaging functionality should be in unified messaging system',
            'reduction': len(messaging_repos)
        })
    
    # Repos that could merge into contract system
    contract_repos = [r for r in repos if 'contract' in r.get('name', '').lower() or 'lead' in r.get('name', '').lower()]
    if contract_repos:
        core_merges.append({
            'type': 'core_system_merge',
            'target_system': 'Contract System',
            'target_location': 'src/services/contract_system/',
            'repos': contract_repos,
            'rationale': 'Contract and lead management should be unified',
            'reduction': len(contract_repos) - 1  # trading-leads-bot is target
        })
    
    # Repos that could merge into health monitoring
    health_repos = [r for r in repos if any(word in r.get('name', '').lower() for word in ['network', 'scanner', 'monitor', 'health'])]
    if health_repos:
        core_merges.append({
            'type': 'core_system_merge',
            'target_system': 'Health Monitoring',
            'target_location': 'src/core/health/monitoring/',
            'repos': health_repos,
            'rationale': 'Network and health monitoring should be unified',
            'reduction': len(health_repos) - 1
        })
    
    # Repos that could merge into tool system
    tool_repos = [r for r in repos if any(word in r.get('name', '').lower() for word in ['tool', 'utility', 'helper', 'scanner'])]
    if tool_repos:
        # Exclude projectscanner (already integrated)
        tool_repos = [r for r in tool_repos if r.get('name', '').lower() != 'projectscanner']
        if tool_repos:
            core_merges.append({
                'type': 'core_system_merge',
                'target_system': 'Tools System',
                'target_location': 'tools/',
                'repos': tool_repos,
                'rationale': 'Utility tools should be in unified tools directory',
                'reduction': len(tool_repos) - 1
            })
    
    return core_merges


def analyze_integration_opportunities(repos: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze all integration consolidation opportunities."""
    # Check which repos are already integrated
    integrated = []
    not_integrated = []
    
    for repo in repos:
        name = repo.get('name', '')
        if name and name != 'Unknown':
            integration_status = check_repo_integrated_into_v2(name)
            if integration_status['integrated']:
                integrated.append({
                    'repo': repo,
                    'status': integration_status
                })
            else:
                not_integrated.append({
                    'repo': repo,
                    'status': integration_status
                })
    
    # Categorize by integration patterns
    patterns = categorize_by_integration_pattern(repos)
    
    # Find shared integration code opportunities
    shared_integrations = find_shared_integration_code(repos)
    
    # Find core system merge opportunities
    core_merges = find_core_system_merges(repos)
    
    # Calculate totals
    total_reduction = sum(s.get('reduction', 0) for s in shared_integrations) + sum(c.get('reduction', 0) for c in core_merges)
    
    return {
        'integrated_repos': integrated,
        'not_integrated_repos': not_integrated,
        'integration_patterns': dict(patterns),
        'shared_integration_opportunities': shared_integrations,
        'core_system_merge_opportunities': core_merges,
        'total_integration_reduction': total_reduction,
        'summary': {
            'already_integrated': len(integrated),
            'could_integrate': len(not_integrated),
            'shared_integration_groups': len(shared_integrations),
            'core_system_merges': len(core_merges),
            'potential_reduction': total_reduction
        }
    }


def main():
    """Main analysis function."""
    print("🔗 Integration Pattern Analyzer - Agent-1")
    print("=" * 70)
    print("Analyzing repos for integration consolidation opportunities...")
    print()
    
    # Load data
    repos = load_master_repo_list()
    if not repos:
        print("❌ No repos loaded. Exiting.")
        return
    
    # Analyze
    print("📊 Analyzing integration patterns...")
    analysis = analyze_integration_opportunities(repos)
    
    # Save report
    output_path = Path('agent_workspaces/Agent-1/integration_analysis.json')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(analysis, indent=2))
    
    print(f"\n✅ Analysis complete!")
    print(f"   Already integrated: {analysis['summary']['already_integrated']} repos")
    print(f"   Could integrate: {analysis['summary']['could_integrate']} repos")
    print(f"   Shared integration groups: {analysis['summary']['shared_integration_groups']}")
    print(f"   Core system merges: {analysis['summary']['core_system_merges']}")
    print(f"   Potential reduction: {analysis['summary']['potential_reduction']} repos")
    print()
    print(f"📄 Full report saved to: {output_path}")
    
    # Print summary
    print("\n📋 Integration Opportunities Summary:")
    print("-" * 70)
    
    if analysis['shared_integration_opportunities']:
        print("\n🔗 Shared Integration Code Opportunities:")
        for i, opp in enumerate(analysis['shared_integration_opportunities'], 1):
            print(f"\n{i}. {opp['category']}")
            print(f"   Repos: {', '.join([r['name'] for r in opp['repos']])}")
            print(f"   Shared code: {opp['shared_code']}")
            print(f"   Target: {opp['target']}")
            print(f"   Reduction: {opp['reduction']} repos")
    
    if analysis['core_system_merge_opportunities']:
        print("\n🏗️ Core System Merge Opportunities:")
        for i, merge in enumerate(analysis['core_system_merge_opportunities'], 1):
            print(f"\n{i}. {merge['target_system']}")
            print(f"   Repos: {', '.join([r['name'] for r in merge['repos']])}")
            print(f"   Target location: {merge['target_location']}")
            print(f"   Rationale: {merge['rationale']}")
            print(f"   Reduction: {merge['reduction']} repos")
    
    return analysis


if __name__ == '__main__':
    main()


