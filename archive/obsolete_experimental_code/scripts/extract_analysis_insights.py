#!/usr/bin/env python3
import json

with open('tools_dependency_analysis.json', 'r') as f:
    report = json.load(f)

print('🎯 DEPENDENCY ANALYSIS INSIGHTS')
print('=' * 50)

# Show consolidation opportunities
print('\n🔗 TOP CONSOLIDATION OPPORTUNITIES:')
opportunities = report.get('consolidation_opportunities', [])
for opp in opportunities[:10]:
    shared_deps = ', '.join(opp.get('shared_deps', [])[:3])
    print(f'  • {opp["tool1"]} ↔ {opp["tool2"]} ({opp["consolidation_potential"]})')
    print(f'    Shared: {shared_deps} | Similarity: {opp["similarity_score"]}')

# Show migration priorities
print('\n📊 MIGRATION PRIORITIES:')
priorities = report.get('migration_priorities', [])
for priority in priorities[:10]:
    print(f'  • {priority["tool"]} - {priority["migration_order"]} (Score: {priority["priority_score"]})')

print('\n✅ DEPENDENCY MAPPING COMPLETE')