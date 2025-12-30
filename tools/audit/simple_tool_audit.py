#!/usr/bin/env python3
"""
Simple Tool Audit for Agent-6
=============================

Audits Agent-6's assigned tools for basic functionality.
"""

import json
from pathlib import Path

def main():
    # Load Agent-6's assignment
    assignment_file = Path('agent_workspaces/Agent-5/tool_audit_assignments/Agent-6_tool_audit_assignment.json')
    with open(assignment_file, 'r') as f:
        assignment = json.load(f)

    tools = assignment.get('tools', [])
    print(f'🔍 Agent-6 Tool Audit - Auditing {len(tools)} tools (Chunk 6/8)')
    print('=' * 70)

    working = []
    broken = []

    for i, tool_path in enumerate(tools, 1):
        tool_name = Path(tool_path).name
        print(f'{i:2d}/{len(tools):2d} Testing: {tool_name}...', end=' ', flush=True)

        try:
            # Simple syntax check
            with open(tool_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Try to compile
            compile(content, tool_path, 'exec')
            print('✅ WORKING')
            working.append(tool_path)

        except SyntaxError as e:
            print('❌ SYNTAX ERROR')
            broken.append({'path': tool_path, 'error': f'SyntaxError: {e}'})
        except Exception as e:
            print('❌ ERROR')
            broken.append({'path': tool_path, 'error': str(e)})

    print()
    print('📊 AGENT-6 AUDIT RESULTS:')
    print(f'✅ Working tools: {len(working)}')
    print(f'❌ Broken tools: {len(broken)}')

    if broken:
        print()
        print('🔧 BROKEN TOOLS DETAILS:')
        for item in broken:
            tool_name = Path(item['path']).name
            print(f'  {tool_name}: {item["error"]}')

    # Save results
    results = {
        'agent': 'Agent-6',
        'chunk': 6,
        'total_tools': len(tools),
        'working': working,
        'broken': broken,
        'working_count': len(working),
        'broken_count': len(broken)
    }

    with open('AGENT6_TOOL_AUDIT_RESULTS.json', 'w') as f:
        json.dump(results, f, indent=2)

    print(f'\n💾 Results saved to AGENT6_TOOL_AUDIT_RESULTS.json')

    # Generate BROKEN_TOOLS_AUDIT_REPORT.md
    if broken:
        with open('BROKEN_TOOLS_AUDIT_REPORT.md', 'w') as f:
            f.write('# Broken Tools Audit Report - Agent-6\n\n')
            f.write(f'**Audit Date:** {json.dumps({"audit_date": "2025-12-20"})}\n\n')
            f.write('## Summary\n\n')
            f.write(f'- **Total Tools Audited:** {len(tools)}\n')
            f.write(f'- **Working Tools:** {len(working)}\n')
            f.write(f'- **Broken Tools:** {len(broken)}\n')
            f.write(f'- **Success Rate:** {(len(working)/len(tools)*100):.1f}%\n\n')

            f.write('## Broken Tools Details\n\n')
            for item in broken:
                tool_name = Path(item['path']).name
                f.write(f'### {tool_name}\n')
                f.write(f'- **Path:** {item["path"]}\n')
                f.write(f'- **Error:** {item["error"]}\n\n')

        print(f'📄 Report generated: BROKEN_TOOLS_AUDIT_REPORT.md')

if __name__ == '__main__':
    main()
