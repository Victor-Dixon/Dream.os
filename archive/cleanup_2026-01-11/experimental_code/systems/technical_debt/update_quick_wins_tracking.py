#!/usr/bin/env python3
"""Update quick wins tracking in technical debt data"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from systems.technical_debt.debt_tracker import TechnicalDebtTracker

def update_quick_wins_tracking():
    """Update quick wins tracking."""
    tracker = TechnicalDebtTracker()
    
    # Get current data
    file_deletion = tracker.debt_data["categories"]["file_deletion"]
    integration = tracker.debt_data["categories"]["integration"]
    
    # Calculate quick wins metrics
    quick_wins_total = file_deletion["total"] + integration["total"]
    quick_wins_resolved = file_deletion["resolved"] + integration["resolved"]
    quick_wins_pending = quick_wins_total - quick_wins_resolved
    
    # Calculate percentage of total debt
    total_debt = tracker.calculate_total_debt()["total"]
    quick_wins_percentage = (quick_wins_total / total_debt * 100) if total_debt > 0 else 0
    
    print("="*60)
    print("📊 QUICK WINS TRACKING")
    print("="*60)
    print(f"File Deletion: {file_deletion['resolved']}/{file_deletion['total']} resolved ({file_deletion['total'] - file_deletion['resolved']} pending)")
    print(f"Integration: {integration['resolved']}/{integration['total']} resolved ({integration['total'] - integration['resolved']} pending)")
    print(f"\nCombined Quick Wins: {quick_wins_resolved}/{quick_wins_total} resolved ({quick_wins_pending} pending)")
    print(f"Potential Reduction: {quick_wins_percentage:.1f}% of total debt")
    print("="*60)

if __name__ == "__main__":
    update_quick_wins_tracking()


