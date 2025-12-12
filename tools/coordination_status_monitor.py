#!/usr/bin/env python3
"""
<!-- SSOT Domain: infrastructure -->
Monitor bilateral coordination status across the swarm.

Author: Agent-6 (Coordination & Communication Specialist)
"""
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional

def parse_timestamp(ts: str) -> Optional[datetime]:
    """Parse timestamp string to datetime."""
    try:
        return datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')
    except:
        return None

def check_coordination_status() -> Dict:
    """Check coordination status across all agents."""
    agents = ['Agent-1', 'Agent-2', 'Agent-3', 'Agent-5', 'Agent-7', 'Agent-8']
    statuses = {}
    now = datetime.now()
    
    for agent in agents:
        status_file = Path(f'agent_workspaces/{agent}/status.json')
        if status_file.exists():
            try:
                data = json.loads(status_file.read_text())
                last_updated = parse_timestamp(data.get('last_updated', ''))
                age_minutes = (now - last_updated).total_seconds() / 60 if last_updated else None
                
                # Check for coordination mentions in tasks
                tasks = data.get('current_tasks', [])
                coordination_mentions = [
                    t for t in tasks 
                    if any(keyword in t.lower() for keyword in ['coordinate', 'coordination', 'bilateral', 'agent-'])
                ]
                
                statuses[agent] = {
                    'status': data.get('status', 'UNKNOWN'),
                    'mission': data.get('current_mission', 'N/A')[:80],
                    'last_updated': data.get('last_updated', 'N/A'),
                    'age_minutes': round(age_minutes, 1) if age_minutes else None,
                    'tasks': len(tasks),
                    'coordination_mentions': len(coordination_mentions),
                    'has_coordination': len(coordination_mentions) > 0
                }
            except Exception as e:
                statuses[agent] = {'error': str(e)}
        else:
            statuses[agent] = {'error': 'No status file'}
    
    return statuses

def generate_coordination_report(statuses: Dict) -> str:
    """Generate coordination status report."""
    report = []
    report.append("=" * 80)
    report.append("BILATERAL COORDINATION STATUS MONITOR")
    report.append("=" * 80)
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    
    # Coordination pairs from Captain broadcast
    pairs = [
        ("Agent-2 ↔ Agent-7", "V2 violations refactoring"),
        ("Agent-2/Agent-7 ↔ Agent-1", "Integration testing"),
        ("Agent-3 ↔ Agent-7", "WordPress web interface"),
        ("All Agents → Agent-8", "QA review")
    ]
    
    report.append("COORDINATION PAIRS (Captain Broadcast):")
    report.append("-" * 80)
    for pair, description in pairs:
        report.append(f"  {pair}: {description}")
    report.append("")
    
    report.append("AGENT STATUS SUMMARY:")
    report.append("-" * 80)
    for agent, info in statuses.items():
        if 'error' in info:
            report.append(f"{agent}: ERROR - {info['error']}")
        else:
            status_icon = "✅" if info['status'] == 'ACTIVE_AGENT_MODE' else "⚠️"
            coord_icon = "🔗" if info['has_coordination'] else "❌"
            age_str = f"{info['age_minutes']}m ago" if info['age_minutes'] else "N/A"
            report.append(f"{status_icon} {agent}: {info['status']}")
            report.append(f"   Mission: {info['mission']}")
            report.append(f"   Last Updated: {info['last_updated']} ({age_str})")
            report.append(f"   Active Tasks: {info['tasks']}")
            report.append(f"   {coord_icon} Coordination Mentions: {info['coordination_mentions']}")
            report.append("")
    
    # Coordination health check
    active_count = sum(1 for s in statuses.values() if s.get('status') == 'ACTIVE_AGENT_MODE')
    coord_count = sum(1 for s in statuses.values() if s.get('has_coordination', False))
    recent_count = sum(1 for s in statuses.values() if s.get('age_minutes') and s.get('age_minutes', 999) < 60)
    
    report.append("COORDINATION HEALTH METRICS:")
    report.append("-" * 80)
    report.append(f"  Active Agents: {active_count}/{len(statuses)}")
    report.append(f"  Agents with Coordination Mentions: {coord_count}/{len(statuses)}")
    report.append(f"  Recently Updated (< 60min): {recent_count}/{len(statuses)}")
    report.append("")
    
    if coord_count == len(statuses):
        report.append("✅ ALL AGENTS HAVE COORDINATION MENTIONS")
    elif coord_count >= len(statuses) * 0.8:
        report.append("⚠️ MOST AGENTS HAVE COORDINATION MENTIONS")
    else:
        report.append("❌ SOME AGENTS LACKING COORDINATION MENTIONS")
    
    report.append("")
    report.append("=" * 80)
    
    return "\n".join(report)

if __name__ == '__main__':
    statuses = check_coordination_status()
    report = generate_coordination_report(statuses)
    print(report)
    
    # Save report
    report_file = Path('tools/COORDINATION_STATUS_REPORT.txt')
    report_file.write_text(report)
    print(f"\n✅ Report saved to: {report_file}")

