#!/usr/bin/env python3
"""
Comprehensive Grade Card Audit Tool
====================================

<!-- SSOT Domain: web -->

Audits websites against grade card criteria for sales funnel validation.
Validates all 8 categories: Brand Core, Visual Identity, Social Presence,
Funnel Infrastructure, Website Conversion, Content System, Blog & SEO,
Tracking & Ops.

V2 Compliance: < 300 lines, single responsibility
Author: Agent-7 (Web Development Specialist)
Date: 2025-12-25
"""

import json
import logging
import sys
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 4 Revenue Engine Websites (2026 Foundation)
REVENUE_ENGINE_SITES = [
    "freerideinvestor.com",
    "tradingrobotplug.com", 
    "dadudekc.com",
    "crosbyultimateevents.com"
]


class GradeCardAuditor:
    """Comprehensive grade card auditor for revenue engine websites."""
    
    def __init__(self, websites_dir: Path):
        """Initialize auditor with websites directory."""
        self.websites_dir = Path(websites_dir)
        self.results: Dict[str, Any] = {}
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def find_grade_card(self, site_name: str) -> Optional[Path]:
        """Find grade card YAML file for a site."""
        # Check multiple possible locations
        search_paths = [
            self.websites_dir / site_name / "GRADE_CARD_SALES_FUNNEL.yaml",
            self.websites_dir / site_name.replace(".com", "") / "GRADE_CARD_SALES_FUNNEL.yaml",
            project_root / "temp_repos" / site_name / "GRADE_CARD_SALES_FUNNEL.yaml",
        ]
        
        # Also check parent directories
        for parent_dir in [self.websites_dir.parent, self.websites_dir]:
            search_paths.extend([
                parent_dir / site_name / "GRADE_CARD_SALES_FUNNEL.yaml",
                parent_dir / site_name.replace(".com", "") / "GRADE_CARD_SALES_FUNNEL.yaml",
            ])
        
        # Special case: TradingRobotPlugWeb directory
        if "tradingrobotplug" in site_name.lower():
            search_paths.extend([
                self.websites_dir.parent / "TradingRobotPlugWeb" / "GRADE_CARD_SALES_FUNNEL.yaml",
                Path("D:/websites/TradingRobotPlugWeb/GRADE_CARD_SALES_FUNNEL.yaml"),
            ])
        
        # Special case: FreeRideInvestor directory
        if "freerideinvestor" in site_name.lower():
            search_paths.extend([
                self.websites_dir.parent / "FreeRideInvestor" / "GRADE_CARD_SALES_FUNNEL.yaml",
                Path("D:/websites/FreeRideInvestor/GRADE_CARD_SALES_FUNNEL.yaml"),
            ])
        
        for path in search_paths:
            if path.exists():
                logger.info(f"✅ Found grade card: {path}")
                return path
        
        logger.warning(f"⚠️  No grade card found for {site_name}")
        return None
    
    def load_grade_card(self, file_path: Path) -> Dict[str, Any]:
        """Load and parse grade card YAML file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                return data
        except Exception as e:
            logger.error(f"❌ Error loading grade card {file_path}: {e}")
            return {}
    
    def calculate_category_score(self, category: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate score for a single category."""
        weight = category.get('weight_points', 0)
        criteria = category.get('criteria', [])
        
        total_score = 0
        max_score = 0
        scored_criteria = []
        
        for criterion in criteria:
            score = criterion.get('score_0_to_5', 0)
            max_score += 5  # Each criterion is 0-5
            total_score += score
            
            scored_criteria.append({
                'id': criterion.get('id'),
                'name': criterion.get('name'),
                'score': score,
                'max_score': 5,
                'priority': criterion.get('priority', 'P2'),
                'gap': criterion.get('gap', ''),
                'fix': criterion.get('fix', '')
            })
        
        # Weighted score calculation
        category_score = (total_score / max_score) * weight if max_score > 0 else 0
        
        return {
            'name': category.get('name'),
            'weight_points': weight,
            'category_score': round(category_score, 2),
            'max_category_score': weight,
            'total_criterion_score': total_score,
            'max_criterion_score': max_score,
            'criteria': scored_criteria
        }
    
    def calculate_total_score(self, grade_card: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate total score from grade card."""
        categories_data = grade_card.get('gradecard', {}).get('categories', [])
        
        total_score = 0
        max_total_score = 100
        category_scores = []
        
        for category in categories_data:
            category_result = self.calculate_category_score(category)
            total_score += category_result['category_score']
            category_scores.append(category_result)
        
        grade = self._score_to_grade(total_score)
        
        return {
            'total_score': round(total_score, 2),
            'max_score': max_total_score,
            'grade': grade,
            'categories': category_scores
        }
    
    def _score_to_grade(self, score: float) -> str:
        """Convert numeric score to letter grade."""
        if score >= 90:
            return 'A'
        elif score >= 80:
            return 'B+'
        elif score >= 70:
            return 'B'
        elif score >= 60:
            return 'C+'
        elif score >= 50:
            return 'C'
        elif score >= 40:
            return 'D'
        else:
            return 'F'
    
    def audit_site(self, site_name: str) -> Dict[str, Any]:
        """Audit a single site against its grade card."""
        logger.info(f"🔍 Auditing {site_name}...")
        
        result = {
            'site': site_name,
            'timestamp': datetime.now().isoformat(),
            'grade_card_found': False,
            'audit_complete': False
        }
        
        # Find and load grade card
        grade_card_path = self.find_grade_card(site_name)
        if not grade_card_path:
            result['error'] = 'Grade card not found'
            return result
        
        grade_card_data = self.load_grade_card(grade_card_path)
        if not grade_card_data:
            result['error'] = 'Failed to load grade card'
            return result
        
        result['grade_card_found'] = True
        result['grade_card_path'] = str(grade_card_path)
        result['grade_card_data'] = grade_card_data
        
        # Calculate scores
        scoring = self.calculate_total_score(grade_card_data)
        result['scoring'] = scoring
        
        # Extract prioritized fixes
        fixes = self._extract_prioritized_fixes(grade_card_data)
        result['prioritized_fixes'] = fixes
        
        result['audit_complete'] = True
        logger.info(f"✅ Audit complete for {site_name}: {scoring['total_score']}/100 (Grade {scoring['grade']})")
        
        return result
    
    def _extract_prioritized_fixes(self, grade_card: Dict[str, Any]) -> Dict[str, List[Dict]]:
        """Extract fixes grouped by priority."""
        categories_data = grade_card.get('gradecard', {}).get('categories', [])
        
        fixes = {
            'P0': [],  # Blocking revenue
            'P1': [],  # High impact
            'P2': []   # Nice to have
        }
        
        for category in categories_data:
            category_name = category.get('name', '')
            for criterion in category.get('criteria', []):
                priority = criterion.get('priority', 'P2')
                if priority in fixes:
                    fixes[priority].append({
                        'category': category_name,
                        'id': criterion.get('id'),
                        'name': criterion.get('name'),
                        'current_score': criterion.get('score_0_to_5', 0),
                        'gap': criterion.get('gap', ''),
                        'fix': criterion.get('fix', ''),
                        'eta': criterion.get('eta', '')
                    })
        
        return fixes
    
    def audit_all_sites(self) -> Dict[str, Any]:
        """Audit all revenue engine websites."""
        logger.info("🚀 Starting comprehensive grade card audit...")
        logger.info(f"📊 Auditing {len(REVENUE_ENGINE_SITES)} revenue engine websites")
        
        results = {}
        summary = {
            'total_sites': len(REVENUE_ENGINE_SITES),
            'sites_audited': 0,
            'sites_with_grade_cards': 0,
            'average_score': 0,
            'sites_below_target': []
        }
        
        total_scores = []
        
        for site in REVENUE_ENGINE_SITES:
            site_result = self.audit_site(site)
            results[site] = site_result
            
            if site_result.get('audit_complete'):
                summary['sites_audited'] += 1
                summary['sites_with_grade_cards'] += 1
                
                score = site_result.get('scoring', {}).get('total_score', 0)
                total_scores.append(score)
                
                # Check if below target (B+ = 80+)
                if score < 80:
                    summary['sites_below_target'].append({
                        'site': site,
                        'score': score,
                        'grade': site_result.get('scoring', {}).get('grade', 'F')
                    })
            elif site_result.get('grade_card_found'):
                summary['sites_with_grade_cards'] += 1
        
        if total_scores:
            summary['average_score'] = round(sum(total_scores) / len(total_scores), 2)
        
        return {
            'timestamp': datetime.now().isoformat(),
            'summary': summary,
            'results': results
        }
    
    def generate_report(self, audit_results: Dict[str, Any]) -> Path:
        """Generate markdown audit report."""
        reports_dir = project_root / "docs" / "website_audits" / "2026"
        reports_dir.mkdir(parents=True, exist_ok=True)
        
        report_path = reports_dir / f"comprehensive_grade_card_audit_{self.timestamp}.md"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# Comprehensive Grade Card Audit Report\n\n")
            f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Auditor:** Agent-7 (Web Development Specialist)\n")
            f.write(f"**Sites Audited:** {audit_results['summary']['total_sites']}\n\n")
            f.write("---\n\n")
            
            # Summary
            f.write("## Executive Summary\n\n")
            summary = audit_results['summary']
            f.write(f"- **Sites Audited:** {summary['sites_audited']}/{summary['total_sites']}\n")
            f.write(f"- **Sites with Grade Cards:** {summary['sites_with_grade_cards']}\n")
            f.write(f"- **Average Score:** {summary['average_score']}/100\n")
            f.write(f"- **Sites Below Target (B+):** {len(summary['sites_below_target'])}\n\n")
            
            # Site-by-site results
            f.write("## Site-by-Site Results\n\n")
            for site, result in audit_results['results'].items():
                if result.get('audit_complete'):
                    scoring = result.get('scoring', {})
                    f.write(f"### {site}\n\n")
                    f.write(f"**Score:** {scoring['total_score']}/100 (Grade {scoring['grade']})\n")
                    f.write(f"**Target:** 80+/100 (Grade B+)\n")
                    f.write(f"**Gap:** {80 - scoring['total_score']:.1f} points needed\n\n")
                    
                    # Category breakdown
                    f.write("**Category Scores:**\n")
                    for category in scoring.get('categories', []):
                        f.write(f"- {category['name']}: {category['category_score']}/{category['max_category_score']} "
                               f"({category['total_criterion_score']}/{category['max_criterion_score']} criterion points)\n")
                    f.write("\n")
                    
                    # Top priority fixes
                    fixes = result.get('prioritized_fixes', {})
                    if fixes.get('P0'):
                        f.write("**P0 Fixes (Blocking Revenue):**\n")
                        for fix in fixes['P0'][:5]:  # Top 5
                            f.write(f"- [{fix['id']}] {fix['name']}: {fix['fix'][:100]}...\n")
                        f.write("\n")
            
            # Prioritized fix list
            f.write("## Consolidated Prioritized Fix List\n\n")
            all_p0_fixes = []
            for site, result in audit_results['results'].items():
                if result.get('audit_complete'):
                    fixes = result.get('prioritized_fixes', {}).get('P0', [])
                    for fix in fixes:
                        fix['site'] = site
                        all_p0_fixes.append(fix)
            
            if all_p0_fixes:
                f.write("### P0 Fixes (Blocking Revenue) - Immediate Action Required\n\n")
                for i, fix in enumerate(all_p0_fixes[:20], 1):  # Top 20
                    f.write(f"{i}. **{fix['site']}** - [{fix['id']}] {fix['name']}\n")
                    f.write(f"   - Gap: {fix['gap']}\n")
                    f.write(f"   - Fix: {fix['fix']}\n")
                    f.write(f"   - ETA: {fix.get('eta', 'TBD')}\n\n")
        
        logger.info(f"✅ Report generated: {report_path}")
        return report_path


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Comprehensive grade card audit')
    parser.add_argument(
        '--websites-dir',
        type=str,
        default='D:/websites/websites',
        help='Path to websites directory'
    )
    parser.add_argument(
        '--site',
        type=str,
        help='Audit single site (optional)'
    )
    
    args = parser.parse_args()
    
    auditor = GradeCardAuditor(Path(args.websites_dir))
    
    if args.site:
        result = auditor.audit_site(args.site)
        print(json.dumps(result, indent=2))
    else:
        results = auditor.audit_all_sites()
        report_path = auditor.generate_report(results)
        
        # Also save JSON
        json_path = project_root / "reports" / f"comprehensive_grade_card_audit_{auditor.timestamp}.json"
        json_path.parent.mkdir(parents=True, exist_ok=True)
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n✅ Comprehensive audit complete!")
        print(f"📊 Sites audited: {results['summary']['sites_audited']}")
        print(f"📄 Report: {report_path}")
        print(f"📄 JSON: {json_path}")


if __name__ == '__main__':
    main()

