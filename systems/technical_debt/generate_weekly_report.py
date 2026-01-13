#!/usr/bin/env python3
"""
Generate weekly technical debt report

<!-- SSOT Domain: analytics -->
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from systems.technical_debt.debt_tracker import TechnicalDebtTracker
from systems.technical_debt.weekly_report_generator import WeeklyReportGenerator

def main():
    """Generate weekly report."""
    tracker = TechnicalDebtTracker()
    generator = WeeklyReportGenerator(tracker)
    
    # Generate report
    report = generator.generate_weekly_report()
    
    # Save JSON report
    json_path = generator.save_report(report)
    print(f"✅ Weekly report generated: {json_path}")
    
    # Save Markdown report
    md_path = generator.save_markdown_report(report)
    print(f"✅ Markdown report generated: {md_path}")
    
    # Print summary
    print("\n" + "="*60)
    print("📊 WEEKLY TECHNICAL DEBT REPORT SUMMARY")
    print("="*60)
    print(f"Total Debt Items: {report['summary']['total']}")
    print(f"Resolved: {report['summary']['resolved']}")
    print(f"Pending: {report['summary']['pending']}")
    print(f"Reduction Rate: {report['summary']['reduction_rate']}%")
    print(f"Weekly Resolutions: {report['weekly_metrics']['total_resolved']}")
    print("="*60)

if __name__ == "__main__":
    main()

