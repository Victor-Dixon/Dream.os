#!/usr/bin/env python3
"""
Generate Audit Implementation Roadmap
=====================================

<!-- SSOT Domain: web -->

Consolidates audit findings and creates prioritized implementation roadmap.
Generates timeline with milestones and owner assignments.

V2 Compliance: < 300 lines, single responsibility
Author: Agent-7 (Web Development Specialist)
Date: 2025-12-25
"""

import json
import logging
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class RoadmapGenerator:
    """Generates implementation roadmap from audit results."""
    
    def __init__(self, audit_json_path: Path):
        """Initialize with audit results JSON."""
        self.audit_json_path = Path(audit_json_path)
        self.audit_data = self._load_audit_data()
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def _load_audit_data(self) -> Dict[str, Any]:
        """Load audit results JSON."""
        try:
            with open(self.audit_json_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"❌ Error loading audit data: {e}")
            return {}
    
    def consolidate_fixes(self) -> Dict[str, List[Dict]]:
        """Consolidate all fixes by priority and category."""
        fixes_by_priority = {
            'P0': [],  # Blocking revenue
            'P1': [],  # High impact
            'P2': []   # Nice to have
        }
        
        results = self.audit_data.get('results', {})
        for site, result in results.items():
            if not result.get('audit_complete'):
                continue
                
            prioritized_fixes = result.get('prioritized_fixes', {})
            for priority in ['P0', 'P1', 'P2']:
                site_fixes = prioritized_fixes.get(priority, [])
                for fix in site_fixes:
                    fix['site'] = site
                    fixes_by_priority[priority].append(fix)
        
        return fixes_by_priority
    
    def group_by_category(self, fixes: List[Dict]) -> Dict[str, List[Dict]]:
        """Group fixes by category for better organization."""
        by_category = {}
        for fix in fixes:
            category = fix.get('category', 'Other')
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(fix)
        return by_category
    
    def generate_roadmap(self) -> Path:
        """Generate implementation roadmap markdown."""
        reports_dir = project_root / "docs" / "website_audits" / "2026"
        reports_dir.mkdir(parents=True, exist_ok=True)
        
        roadmap_path = reports_dir / f"implementation_roadmap_{self.timestamp}.md"
        
        consolidated_fixes = self.consolidate_fixes()
        summary = self.audit_data.get('summary', {})
        
        with open(roadmap_path, 'w', encoding='utf-8') as f:
            f.write("# Implementation Roadmap - 2026 Revenue Engine Websites\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Auditor:** Agent-7 (Web Development Specialist)\n")
            f.write(f"**Source:** Comprehensive Grade Card Audit\n\n")
            f.write("---\n\n")
            
            # Executive Summary
            f.write("## Executive Summary\n\n")
            f.write(f"- **Sites Audited:** {summary.get('sites_audited', 0)}\n")
            f.write(f"- **Average Score:** {summary.get('average_score', 0)}/100\n")
            f.write(f"- **Target Score:** 80+/100 (Grade B+)\n")
            f.write(f"- **Gap to Target:** {80 - summary.get('average_score', 0):.1f} points average\n")
            f.write(f"- **P0 Fixes (Blocking Revenue):** {len(consolidated_fixes['P0'])}\n")
            f.write(f"- **P1 Fixes (High Impact):** {len(consolidated_fixes['P1'])}\n")
            f.write(f"- **P2 Fixes (Nice to Have):** {len(consolidated_fixes['P2'])}\n\n")
            
            # Timeline Overview
            f.write("## Implementation Timeline\n\n")
            f.write("### Week 1 (Foundation Phase) - P0 Fixes Only\n")
            f.write("**Goal:** Fix critical revenue-blocking issues\n\n")
            f.write("**Focus Areas:**\n")
            f.write("- Brand Core (positioning, offer ladder, ICP)\n")
            f.write("- Funnel Infrastructure (lead magnets, email sequences, checkout)\n")
            f.write("- Website Conversion (hero, pricing, CTAs)\n\n")
            
            f.write("### Week 2-3 (High Impact Phase) - P1 Fixes\n")
            f.write("**Goal:** Improve conversion and tracking\n\n")
            f.write("**Focus Areas:**\n")
            f.write("- Visual Identity (logo, brand guidelines)\n")
            f.write("- Social Presence (accounts, profiles)\n")
            f.write("- Tracking & Ops (analytics, metrics)\n\n")
            
            f.write("### Week 4 (Polish Phase) - P2 Fixes\n")
            f.write("**Goal:** Optimize for long-term growth\n\n")
            f.write("**Focus Areas:**\n")
            f.write("- Content System (content calendar, repurpose pipeline)\n")
            f.write("- Blog & SEO (SEO optimization, internal linking)\n\n")
            
            # Prioritized Fix List by Week
            f.write("## Prioritized Fix List by Week\n\n")
            
            # Week 1: P0 Fixes
            f.write("### Week 1: P0 Fixes (Blocking Revenue)\n\n")
            p0_grouped = self.group_by_category(consolidated_fixes['P0'])
            
            for category, fixes in sorted(p0_grouped.items()):
                f.write(f"#### {category}\n\n")
                for i, fix in enumerate(fixes[:10], 1):  # Top 10 per category
                    f.write(f"{i}. **{fix['site']}** - [{fix['id']}] {fix['name']}\n")
                    f.write(f"   - **Gap:** {fix['gap'][:150]}...\n")
                    f.write(f"   - **Fix:** {fix['fix'][:150]}...\n")
                    f.write(f"   - **ETA:** {fix.get('eta', 'TBD')}\n\n")
            
            # Common Issues Across Sites
            f.write("## Common Issues Across Sites\n\n")
            common_issues = self._identify_common_issues(consolidated_fixes)
            for issue, sites in common_issues.items():
                f.write(f"- **{issue}:** Affects {len(sites)} site(s) - {', '.join(sites)}\n")
            f.write("\n")
            
            # Success Metrics
            f.write("## Success Metrics\n\n")
            f.write("### Target Goals (Week 4):\n")
            f.write("- ✅ All 4 sites score 80+/100 (Grade B+)\n")
            f.write("- ✅ All P0 fixes completed\n")
            f.write("- ✅ Lead magnets functional on all sites\n")
            f.write("- ✅ Email sequences set up\n")
            f.write("- ✅ Booking/checkout flows work\n")
            f.write("- ✅ Analytics tracking installed\n\n")
            
            # Owner Assignments
            f.write("## Owner Assignments\n\n")
            f.write("- **Agent-7:** Web development, funnel infrastructure, website conversion\n")
            f.write("- **Agent-3:** Performance optimization, infrastructure\n")
            f.write("- **Agent-5:** Analytics, tracking, metrics\n")
            f.write("- **Agent-6:** Coordination, timeline tracking\n\n")
        
        logger.info(f"✅ Roadmap generated: {roadmap_path}")
        return roadmap_path
    
    def _identify_common_issues(self, fixes_by_priority: Dict[str, List[Dict]]) -> Dict[str, List[str]]:
        """Identify common issues across multiple sites."""
        common_issues = {}
        all_fixes = fixes_by_priority['P0'] + fixes_by_priority['P1']
        
        # Group by criterion name
        by_criterion = {}
        for fix in all_fixes:
            criterion_id = fix.get('id', '')
            if criterion_id not in by_criterion:
                by_criterion[criterion_id] = []
            by_criterion[criterion_id].append(fix['site'])
        
        # Find issues affecting 2+ sites
        for criterion_id, sites in by_criterion.items():
            if len(set(sites)) >= 2:
                criterion_name = all_fixes[next(i for i, f in enumerate(all_fixes) if f.get('id') == criterion_id)].get('name', '')
                common_issues[f"{criterion_id}: {criterion_name}"] = list(set(sites))
        
        return common_issues


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate implementation roadmap from audit')
    parser.add_argument(
        '--audit-json',
        type=str,
        required=True,
        help='Path to audit results JSON file'
    )
    
    args = parser.parse_args()
    
    generator = RoadmapGenerator(Path(args.audit_json))
    roadmap_path = generator.generate_roadmap()
    
    print(f"✅ Roadmap generated: {roadmap_path}")


if __name__ == '__main__':
    main()

