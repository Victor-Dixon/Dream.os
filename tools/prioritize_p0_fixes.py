#!/usr/bin/env python3
"""
Prioritize P0 Fixes by Impact/Effort Matrix
===========================================
Analyzes audit reports and generates implementation sequence
by impact/effort matrix for revenue engine websites.

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-12-25
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass, asdict

@dataclass
class P0Fix:
    """P0 Fix data structure"""
    site: str
    fix_id: str
    category: str
    description: str
    gap: str
    fix: str
    impact_score: float = 0.0
    effort_score: float = 0.0
    priority_score: float = 0.0

def load_audit_report(report_path: Path) -> Dict:
    """Load audit report JSON or parse markdown"""
    if report_path.suffix == '.json':
        with open(report_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    # Parse markdown audit report
    with open(report_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    fixes = []
    current_site = None
    
    # Extract P0 fixes from markdown
    p0_section = re.search(r'### P0 Fixes.*?(?=##|\Z)', content, re.DOTALL)
    if p0_section:
        lines = p0_section.group(0).split('\n')
        for i, line in enumerate(lines):
            # Extract site name
            site_match = re.search(r'\*\*(\S+\.(com|site|online))\*\*', line)
            if site_match:
                current_site = site_match.group(1)
            
            # Extract fix ID and description
            fix_match = re.search(r'- \[(\w+-\d+)\]\s*(.+)', line)
            if fix_match and current_site:
                fix_id = fix_match.group(1)
                description = fix_match.group(2)
                
                # Extract gap and fix from next lines
                gap = ""
                fix_text = ""
                if i + 1 < len(lines):
                    gap_match = re.search(r'- \*\*Gap:\*\*\s*(.+)', lines[i + 1])
                    if gap_match:
                        gap = gap_match.group(1)
                if i + 2 < len(lines):
                    fix_match = re.search(r'- \*\*Fix:\*\*\s*(.+)', lines[i + 2])
                    if fix_match:
                        fix_text = fix_match.group(1)
                
                category = fix_id.split('-')[0]
                fixes.append({
                    'site': current_site,
                    'fix_id': fix_id,
                    'category': category,
                    'description': description,
                    'gap': gap,
                    'fix': fix_text
                })
    
    return {'p0_fixes': fixes}

def calculate_impact_score(fix: Dict) -> float:
    """Calculate impact score based on category and site score"""
    category_weights = {
        'BRAND': 0.3,  # High impact on conversion
        'FUN': 0.4,    # Highest impact - funnel infrastructure
        'WEB': 0.3,    # High impact on conversion
    }
    
    site_scores = {
        'freerideinvestor.com': 39.0,
        'dadudekc.com': 43.0,
        'crosbyultimateevents.com': 27.0,
        'tradingrobotplug.com': 33.0,
    }
    
    category = fix.get('category', 'WEB')
    site = fix.get('site', '')
    
    base_weight = category_weights.get(category, 0.2)
    site_gap = 100 - site_scores.get(site, 50)  # Larger gap = higher impact
    
    return base_weight * (site_gap / 100)

def calculate_effort_score(fix: Dict) -> float:
    """Calculate effort score (lower = easier, higher = harder)"""
    category_effort = {
        'BRAND': 0.3,  # Content work - medium effort
        'FUN': 0.6,    # Technical implementation - higher effort
        'WEB': 0.4,    # Mixed content/technical - medium-high effort
    }
    
    category = fix.get('category', 'WEB')
    fix_text = fix.get('fix', '').lower()
    
    base_effort = category_effort.get(category, 0.5)
    
    # Adjust based on fix complexity
    if 'stripe' in fix_text or 'payment' in fix_text:
        base_effort += 0.2  # Payment integration is complex
    if 'email' in fix_text and 'sequence' in fix_text:
        base_effort += 0.1  # Email sequences require setup
    if 'chat widget' in fix_text or 'calendar' in fix_text:
        base_effort += 0.1  # Third-party integrations
    
    return min(base_effort, 1.0)

def prioritize_fixes(fixes: List[Dict]) -> List[P0Fix]:
    """Prioritize fixes by impact/effort matrix"""
    prioritized = []
    
    for fix in fixes:
        impact = calculate_impact_score(fix)
        effort = calculate_effort_score(fix)
        priority = impact / effort if effort > 0 else impact  # Higher priority = better ROI
        
        p0_fix = P0Fix(
            site=fix.get('site', ''),
            fix_id=fix.get('fix_id', ''),
            category=fix.get('category', ''),
            description=fix.get('description', ''),
            gap=fix.get('gap', ''),
            fix=fix.get('fix', ''),
            impact_score=impact,
            effort_score=effort,
            priority_score=priority
        )
        prioritized.append(p0_fix)
    
    # Sort by priority score (descending)
    prioritized.sort(key=lambda x: x.priority_score, reverse=True)
    
    return prioritized

def generate_implementation_sequence(prioritized: List[P0Fix]) -> Dict:
    """Generate implementation sequence with phases"""
    sequence = {
        'phase_1_quick_wins': [],
        'phase_2_high_impact': [],
        'phase_3_high_effort': []
    }
    
    for fix in prioritized:
        if fix.effort_score < 0.4 and fix.impact_score > 0.2:
            sequence['phase_1_quick_wins'].append(asdict(fix))
        elif fix.impact_score > 0.3:
            sequence['phase_2_high_impact'].append(asdict(fix))
        else:
            sequence['phase_3_high_effort'].append(asdict(fix))
    
    return sequence

def main():
    """Main execution"""
    print("🎯 P0 Fix Prioritization Tool")
    print("=" * 60)
    
    # Find audit report
    audit_dir = Path("docs/website_audits/2026")
    audit_files = list(audit_dir.glob("comprehensive_grade_card_audit*.md"))
    
    if not audit_files:
        print("❌ No audit reports found in docs/website_audits/2026/")
        return
    
    # Load most recent audit
    latest_audit = sorted(audit_files, key=lambda p: p.stat().st_mtime, reverse=True)[0]
    print(f"📄 Loading audit: {latest_audit.name}")
    
    audit_data = load_audit_report(latest_audit)
    fixes = audit_data.get('p0_fixes', [])
    
    if not fixes:
        print("❌ No P0 fixes found in audit report")
        return
    
    print(f"✅ Found {len(fixes)} P0 fixes")
    
    # Prioritize fixes
    prioritized = prioritize_fixes(fixes)
    
    # Generate implementation sequence
    sequence = generate_implementation_sequence(prioritized)
    
    # Save results
    output_dir = Path("agent_workspaces/Agent-1")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / "p0_fixes_prioritized.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'total_fixes': len(prioritized),
            'prioritized_fixes': [asdict(f) for f in prioritized],
            'implementation_sequence': sequence
        }, f, indent=2)
    
    print(f"\n📊 Prioritization Results:")
    print(f"   Phase 1 (Quick Wins): {len(sequence['phase_1_quick_wins'])} fixes")
    print(f"   Phase 2 (High Impact): {len(sequence['phase_2_high_impact'])} fixes")
    print(f"   Phase 3 (High Effort): {len(sequence['phase_3_high_effort'])} fixes")
    print(f"\n💾 Results saved to: {output_file}")
    
    # Print top 10 priorities
    print(f"\n🏆 Top 10 Priority Fixes:")
    for i, fix in enumerate(prioritized[:10], 1):
        print(f"   {i}. [{fix.fix_id}] {fix.site} - {fix.description[:60]}...")
        print(f"      Priority: {fix.priority_score:.2f} (Impact: {fix.impact_score:.2f}, Effort: {fix.effort_score:.2f})")

if __name__ == "__main__":
    main()



