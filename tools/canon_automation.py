#!/usr/bin/env python3
"""
Canon Automation System
========================

<!-- SSOT Domain: coordination -->

Automatically extracts canon-worthy events from agent work cycles
and structures them for Thea's narrative processing.

V2 Compliance: < 300 lines, single responsibility
Author: Agent-8 (SSOT & System Integration Specialist)
"""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class CanonExtractor:
    """Extracts canon-worthy events from agent status files."""

    def __init__(self, workspaces_dir: Path):
        """Initialize extractor with workspaces directory."""
        self.workspaces_dir = Path(workspaces_dir)
        self.canon_events: List[Dict] = []

    def load_agent_status(self, agent_id: str) -> Optional[Dict]:
        """Load agent status.json file."""
        status_file = self.workspaces_dir / agent_id / "status.json"
        if not status_file.exists():
            return None
        try:
            with open(status_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load {status_file}: {e}")
            return None

    def extract_completed_contracts(self, agent_id: str, status: Dict) -> List[Dict]:
        """Extract canon events from completed contracts."""
        events = []
        contract_status = status.get("contract_status", {})
        
        # Check current contract completion
        if contract_status.get("status") == "✅ COMPLETE":
            contract = contract_status.get("current_contract", "")
            deliverables = contract_status.get("deliverables", [])
            results = contract_status.get("fix_results") or contract_status.get("audit_results") or {}
            
            events.append({
                "type": "contract_completion",
                "agent": agent_id,
                "contract": contract,
                "deliverables": deliverables,
                "results": results,
                "timestamp": status.get("last_updated", datetime.now().isoformat()),
            })
        
        # Check contract history
        contract_history = contract_status.get("contract_history", [])
        for contract in contract_history:
            if contract.get("status") == "✅ COMPLETE":
                events.append({
                    "type": "contract_completion",
                    "agent": agent_id,
                    "contract": contract.get("contract", ""),
                    "deliverables": contract.get("deliverables", []),
                    "results": contract.get("audit_results") or contract.get("validation_results") or {},
                    "timestamp": "historical",
                })
        
        return events

    def extract_achievements(self, agent_id: str, status: Dict) -> List[Dict]:
        """Extract canon events from achievements."""
        events = []
        achievements = status.get("achievements", [])
        
        for achievement in achievements:
            # Only extract significant achievements
            if any(
                keyword in achievement.lower()
                for keyword in ["complete", "milestone", "breakthrough", "established"]
            ):
                events.append({
                    "type": "achievement",
                    "agent": agent_id,
                    "achievement": achievement,
                    "timestamp": status.get("last_updated", datetime.now().isoformat()),
                })
        
        return events

    def extract_task_completions(self, agent_id: str, status: Dict) -> List[Dict]:
        """Extract canon events from completed tasks."""
        events = []
        completed_tasks = status.get("completed_tasks", [])
        
        # Extract recent significant completions
        for task in completed_tasks[-5:]:  # Last 5 tasks
            if "✅ COMPLETE" in task or "COMPLETE" in task:
                # Extract key information
                if ":" in task:
                    parts = task.split(":", 1)
                    task_name = parts[0].strip()
                    details = parts[1].strip() if len(parts) > 1 else ""
                    
                    events.append({
                        "type": "task_completion",
                        "agent": agent_id,
                        "task": task_name,
                        "details": details,
                        "timestamp": status.get("last_updated", datetime.now().isoformat()),
                    })
        
        return events

    def extract_coordination_events(self, agent_id: str, status: Dict) -> List[Dict]:
        """Extract canon events from coordination activities."""
        events = []
        current_tasks = status.get("current_tasks", [])
        next_actions = status.get("next_actions", [])
        
        # Convert to strings if needed
        task_strings = [str(t) if not isinstance(t, str) else t for t in current_tasks]
        action_strings = [str(a) if not isinstance(a, str) else a for a in next_actions]
        
        # Check for coordination mentions
        all_text = " ".join(task_strings + action_strings)
        if any(
            keyword in all_text.lower()
            for keyword in ["coordination", "bilateral", "a2a", "swarm", "collaboration"]
        ):
            events.append({
                "type": "coordination",
                "agent": agent_id,
                "activity": "coordination_active",
                "timestamp": status.get("last_updated", datetime.now().isoformat()),
            })
        
        return events

    def extract_canon_events(self) -> List[Dict]:
        """Extract all canon events from all agents."""
        all_events = []
        
        # Get all agent directories
        agent_dirs = [
            d for d in self.workspaces_dir.iterdir()
            if d.is_dir() and d.name.startswith("Agent-")
        ]
        
        for agent_dir in agent_dirs:
            agent_id = agent_dir.name
            status = self.load_agent_status(agent_id)
            
            if not status:
                continue
            
            # Extract different event types
            all_events.extend(self.extract_completed_contracts(agent_id, status))
            all_events.extend(self.extract_achievements(agent_id, status))
            all_events.extend(self.extract_task_completions(agent_id, status))
            all_events.extend(self.extract_coordination_events(agent_id, status))
        
        return all_events

    def structure_for_thea(self, events: List[Dict]) -> Dict:
        """Structure events for Thea's narrative processing."""
        structured = {
            "timestamp": datetime.now().isoformat(),
            "source": "agent_work_cycles",
            "events": events,
            "summary": {
                "total_events": len(events),
                "by_type": {},
                "by_agent": {},
            },
        }
        
        # Count by type
        for event in events:
            event_type = event.get("type", "unknown")
            structured["summary"]["by_type"][event_type] = (
                structured["summary"]["by_type"].get(event_type, 0) + 1
            )
            
            agent = event.get("agent", "unknown")
            structured["summary"]["by_agent"][agent] = (
                structured["summary"]["by_agent"].get(agent, 0) + 1
            )
        
        return structured

    def generate_canon_candidates(self, structured_events: Dict) -> List[Dict]:
        """Generate canon event candidates for Victor to acknowledge."""
        candidates = []
        
        for event in structured_events["events"]:
            # Only create candidates for significant events
            if event["type"] in ["contract_completion", "achievement"]:
                candidates.append({
                    "canon_candidate": True,
                    "event": event,
                    "suggested_narrative": self._suggest_narrative(event),
                    "requires_victor_acknowledgment": True,
                })
        
        return candidates

    def _suggest_narrative(self, event: Dict) -> str:
        """Suggest narrative framing for an event."""
        event_type = event.get("type", "")
        agent = event.get("agent", "")
        
        if event_type == "contract_completion":
            contract = event.get("contract", "")
            return f"{agent} completed contract: {contract}. This represents progress in the {contract} questline."
        
        elif event_type == "achievement":
            achievement = event.get("achievement", "")
            return f"{agent} achieved: {achievement}. This milestone shapes the Digital Dreamscape world-state."
        
        return f"{agent} completed work that may be canon-worthy."

    def run_extraction(self, output_file: Path) -> int:
        """Run complete extraction process."""
        logger.info("Extracting canon events from agent work cycles...")
        
        events = self.extract_canon_events()
        logger.info(f"Found {len(events)} potential canon events")
        
        structured = self.structure_for_thea(events)
        candidates = self.generate_canon_candidates(structured)
        
        output = {
            "extraction_timestamp": datetime.now().isoformat(),
            "structured_events": structured,
            "canon_candidates": candidates,
            "metadata": {
                "total_events": len(events),
                "candidates_count": len(candidates),
                "agents_scanned": len(set(e.get("agent") for e in events)),
            },
        }
        
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2)
        
        logger.info(f"✅ Canon extraction complete: {output_file}")
        logger.info(f"   Events: {len(events)}")
        logger.info(f"   Candidates: {len(candidates)}")
        
        return 0


def main() -> int:
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Extract canon events from agent work")
    parser.add_argument(
        "--workspaces",
        type=str,
        default="agent_workspaces",
        help="Path to agent workspaces directory"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="reports/canon_extraction.json",
        help="Output file path"
    )
    
    args = parser.parse_args()
    
    root_dir = Path(__file__).parent.parent
    workspaces_dir = root_dir / args.workspaces
    output_file = root_dir / args.output
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    extractor = CanonExtractor(workspaces_dir)
    return extractor.run_extraction(output_file)


if __name__ == "__main__":
    sys.exit(main())

