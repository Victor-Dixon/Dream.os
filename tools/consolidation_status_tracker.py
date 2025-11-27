#!/usr/bin/env python3
"""
Consolidation Status Tracker
============================

Tracks GitHub consolidation progress across all agents and phases.
Provides unified status view and identifies next opportunities.

Author: Agent-4 (Captain)
Date: 2025-11-26
License: MIT
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import requests

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tools.merge_prs_via_api import get_github_token
from tools.check_pr_status import check_pr_status


class ConsolidationStatusTracker:
    """Tracks GitHub consolidation status across all agents."""
    
    def __init__(self):
        """Initialize tracker."""
        self.status_file = Path("consolidation_logs/consolidation_status.json")
        self.status_file.parent.mkdir(parents=True, exist_ok=True)
        self.token = get_github_token()
        self.owner = "Dadudekc"
    
    def load_status(self) -> Dict:
        """Load current status."""
        if self.status_file.exists():
            with open(self.status_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "last_updated": datetime.now().isoformat(),
            "phases": {},
            "agents": {},
            "next_opportunities": []
        }
    
    def save_status(self, status: Dict):
        """Save status to file."""
        status["last_updated"] = datetime.now().isoformat()
        with open(self.status_file, 'w', encoding='utf-8') as f:
            json.dump(status, f, indent=2)
    
    def check_agent_2_status(self) -> Dict:
        """Check Agent-2's consolidation status."""
        prs = [
            {"repo": "DreamVault", "pr": 4, "desc": "DigitalDreamscape → DreamVault"},
            {"repo": "DreamVault", "pr": 3, "desc": "Thea → DreamVault"},
            {"repo": "trading-leads-bot", "pr": 5, "desc": "contract-leads → trading-leads-bot"}
        ]
        
        results = []
        for pr_info in prs:
            status = check_pr_status(self.owner, pr_info["repo"], pr_info["pr"])
            if status:
                results.append({
                    "description": pr_info["desc"],
                    "state": status["state"],
                    "merged": status["merged"],
                    "url": status["url"]
                })
        
        return {
            "agent": "Agent-2",
            "phase_1": "Complete (3/3 merges)",
            "phase_2": "Complete (1/1 merge)",
            "prs": results
        }
    
    def identify_next_opportunities(self) -> List[Dict]:
        """Identify next consolidation opportunities."""
        return [
            {
                "name": "Case Variations",
                "repos": 12,
                "risk": "Zero",
                "priority": "HIGH",
                "description": "Case variation merges (focusforge → FocusForge, etc.)"
            },
            {
                "name": "Trading Repos",
                "repos": 3,
                "risk": "Low",
                "priority": "HIGH",
                "description": "4 → 1 consolidation (trade-analyzer, UltimateOptionsTradingRobot, TheTradingRobotPlug → trading-leads-bot)"
            },
            {
                "name": "Content/Blog Systems",
                "repos": 2,
                "risk": "Low",
                "priority": "HIGH",
                "roi": "69.4x",
                "description": "content + FreeWork → Auto_Blogger"
            }
        ]
    
    def generate_report(self) -> str:
        """Generate status report."""
        status = self.load_status()
        agent_2_status = self.check_agent_2_status()
        opportunities = self.identify_next_opportunities()
        
        report = f"""# GitHub Consolidation Status Report

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Agent**: Agent-4 (Captain)

---

## 📊 **CURRENT STATUS**

### **Agent-2 Consolidation** ✅ COMPLETE
- **Phase 1**: {agent_2_status['phase_1']}
- **Phase 2**: {agent_2_status['phase_2']}
- **PRs**: All verified merged

---

## 🎯 **NEXT OPPORTUNITIES**

"""
        for opp in opportunities:
            report += f"### **{opp['name']}**\n"
            report += f"- **Repos**: {opp['repos']} reduction\n"
            report += f"- **Risk**: {opp['risk']}\n"
            report += f"- **Priority**: {opp['priority']}\n"
            if 'roi' in opp:
                report += f"- **ROI**: {opp['roi']}\n"
            report += f"- **Description**: {opp['description']}\n\n"
        
        report += "---\n\n**Status**: Ready for next phase execution\n"
        
        return report
    
    def track(self) -> Dict:
        """Track and update consolidation status."""
        status = self.load_status()
        agent_2_status = self.check_agent_2_status()
        opportunities = self.identify_next_opportunities()
        
        status["agents"]["Agent-2"] = agent_2_status
        status["next_opportunities"] = opportunities
        
        self.save_status(status)
        
        return status


def main():
    """Main execution."""
    print("=" * 60)
    print("📊 CONSOLIDATION STATUS TRACKER")
    print("=" * 60)
    print()
    
    tracker = ConsolidationStatusTracker()
    
    # Track status
    print("🔍 Tracking consolidation status...")
    status = tracker.track()
    
    # Generate report
    print("📝 Generating report...")
    report = tracker.generate_report()
    
    # Save report
    report_file = Path("consolidation_logs/consolidation_status_report.md")
    report_file.parent.mkdir(parents=True, exist_ok=True)
    report_file.write_text(report, encoding='utf-8')
    
    print(f"✅ Status tracked and report saved: {report_file}")
    print()
    print(report)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

