#!/usr/bin/env python3
"""
Agent Progress Tracker
======================

Tracks agent productivity by monitoring Discord channel activity.
Identifies most productive agents and documents successful patterns.

Author: Agent-4 (Captain)
Date: 2025-11-27
License: MIT
V2 Compliance: <400 lines
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from collections import defaultdict

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class AgentProgressTracker:
    """Tracks agent progress via Discord channel activity."""
    
    def __init__(self):
        """Initialize tracker."""
        self.progress_file = Path("logs/agent_progress.json")
        self.progress_file.parent.mkdir(parents=True, exist_ok=True)
        self.devlog_posts_file = Path("logs/devlog_posts.json")
        
        # Agent Discord channels
        self.agent_channels = {
            "Agent-1": "#agent-1-devlogs",
            "Agent-2": "#agent-2-devlogs",
            "Agent-3": "#agent-3-devlogs",
            "Agent-4": "#agent-4-devlogs",
            "Agent-5": "#agent-5-devlogs",
            "Agent-6": "#agent-6-devlogs",
            "Agent-7": "#agent-7-devlogs",
            "Agent-8": "#agent-8-devlogs",
        }
    
    def load_progress(self) -> Dict:
        """Load current progress data."""
        if self.progress_file.exists():
            with open(self.progress_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "last_updated": datetime.now().isoformat(),
            "agents": {},
            "patterns": [],
            "most_productive": []
        }
    
    def load_devlog_posts(self) -> List[Dict]:
        """Load devlog posts data."""
        if self.devlog_posts_file.exists():
            with open(self.devlog_posts_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def analyze_agent_activity(self, days: int = 7) -> Dict:
        """Analyze agent activity from devlog posts."""
        posts = self.load_devlog_posts()
        cutoff_date = datetime.now() - timedelta(days=days)
        
        agent_stats = defaultdict(lambda: {
            "posts": 0,
            "tasks_completed": 0,
            "blockers_resolved": 0,
            "accomplishments": 0,
            "last_activity": None
        })
        
        for post in posts:
            try:
                post_date = datetime.fromisoformat(post.get("timestamp", ""))
                if post_date < cutoff_date:
                    continue
                
                agent = post.get("agent", "").upper()
                if not agent or agent not in self.agent_channels:
                    continue
                
                agent_stats[agent]["posts"] += 1
                
                # Analyze content for patterns
                content = post.get("content", "").lower()
                if "complete" in content or "✅" in content:
                    agent_stats[agent]["tasks_completed"] += 1
                if "blocker" in content or "🚨" in content:
                    agent_stats[agent]["blockers_resolved"] += 1
                if "accomplishment" in content or "achievement" in content:
                    agent_stats[agent]["accomplishments"] += 1
                
                # Track last activity
                if not agent_stats[agent]["last_activity"] or post_date > datetime.fromisoformat(agent_stats[agent]["last_activity"]):
                    agent_stats[agent]["last_activity"] = post_date.isoformat()
            
            except Exception as e:
                continue
        
        return dict(agent_stats)
    
    def identify_most_productive(self, agent_stats: Dict) -> List[Dict]:
        """Identify most productive agents."""
        productivity_scores = []
        
        for agent, stats in agent_stats.items():
            # Calculate productivity score
            score = (
                stats["posts"] * 1.0 +
                stats["tasks_completed"] * 3.0 +
                stats["blockers_resolved"] * 2.0 +
                stats["accomplishments"] * 2.0
            )
            
            productivity_scores.append({
                "agent": agent,
                "score": score,
                "stats": stats
            })
        
        # Sort by score (descending)
        productivity_scores.sort(key=lambda x: x["score"], reverse=True)
        
        return productivity_scores
    
    def generate_report(self, agent_stats: Dict, most_productive: List[Dict]) -> str:
        """Generate progress report."""
        report = f"""# Agent Progress Report

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Period**: Last 7 days  
**Agent**: Agent-4 (Captain)

---

## 📊 **AGENT PRODUCTIVITY RANKINGS**

"""
        for i, entry in enumerate(most_productive[:5], 1):
            agent = entry["agent"]
            stats = entry["stats"]
            report += f"""### **#{i} {agent}** (Score: {entry['score']:.1f})
- **Posts**: {stats['posts']}
- **Tasks Completed**: {stats['tasks_completed']}
- **Blockers Resolved**: {stats['blockers_resolved']}
- **Accomplishments**: {stats['accomplishments']}
- **Last Activity**: {stats['last_activity'] or 'N/A'}

"""
        
        report += """---

## 🎯 **SUCCESSFUL PATTERNS IDENTIFIED**

[Patterns will be documented here as they are identified]

---

## 📈 **RECOMMENDATIONS**

1. **Replicate Top Patterns**: Study most productive agents and replicate their patterns
2. **Share Best Practices**: Document successful approaches in Swarm Brain
3. **Improve Lower Performers**: Apply successful patterns to improve all agents

---

**Status**: Progress tracking active - Monitor Discord channels for updates
"""
        
        return report
    
    def track(self) -> Dict:
        """Track and update agent progress."""
        progress = self.load_progress()
        
        # Analyze activity
        agent_stats = self.analyze_agent_activity()
        most_productive = self.identify_most_productive(agent_stats)
        
        # Update progress
        progress["last_updated"] = datetime.now().isoformat()
        progress["agents"] = agent_stats
        progress["most_productive"] = most_productive[:5]
        
        # Save
        with open(self.progress_file, 'w', encoding='utf-8') as f:
            json.dump(progress, f, indent=2)
        
        # Generate report
        report = self.generate_report(agent_stats, most_productive)
        report_file = Path("logs/agent_progress_report.md")
        report_file.parent.mkdir(parents=True, exist_ok=True)
        report_file.write_text(report, encoding='utf-8')
        
        return progress


def main():
    """Main execution."""
    print("=" * 60)
    print("📊 AGENT PROGRESS TRACKER")
    print("=" * 60)
    print()
    
    tracker = AgentProgressTracker()
    
    print("🔍 Tracking agent progress...")
    progress = tracker.track()
    
    print(f"✅ Progress tracked: {len(progress['agents'])} agents")
    print(f"📊 Most productive: {', '.join([a['agent'] for a in progress['most_productive'][:3]])}")
    print(f"📝 Report saved: logs/agent_progress_report.md")
    print()
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())



