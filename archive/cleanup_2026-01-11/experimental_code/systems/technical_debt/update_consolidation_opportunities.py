#!/usr/bin/env python3
"""Update technical debt tracker with consolidation opportunities"""

import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from systems.technical_debt.debt_tracker import TechnicalDebtTracker

def update_consolidation_opportunities():
    """Update technical debt tracker with consolidation opportunities."""
    tracker = TechnicalDebtTracker()
    
    # Add consolidation opportunities to integration category
    integration = tracker.debt_data["categories"]["integration"]
    
    # Add messaging consolidation opportunity
    if "Messaging Consolidation (62+ files)" not in integration["pending"]:
        integration["pending"].append("Messaging Consolidation (62+ files)")
        integration["total"] = len(integration["pending"])
    
    # Add other consolidation opportunities
    consolidation_opportunities = [
        "Tools Consolidation (502 files → Tools V2)",
        "Analytics System Duplication (63 files to review)",
        "Orchestration System Overlap (46 files to review)",
    ]
    
    for opportunity in consolidation_opportunities:
        if opportunity not in integration["pending"]:
            integration["pending"].append(opportunity)
    
    # Update total
    integration["total"] = len(integration["pending"])
    
    # Save updated data
    tracker.save_debt_data()
    
    print("="*60)
    print("✅ CONSOLIDATION OPPORTUNITIES UPDATED")
    print("="*60)
    print(f"Integration category updated: {integration['total']} items")
    print(f"New opportunities added: {len(consolidation_opportunities) + 1}")
    print("="*60)

if __name__ == "__main__":
    update_consolidation_opportunities()


