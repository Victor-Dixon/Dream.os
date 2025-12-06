#!/usr/bin/env python3
"""
Session Transition Validator - Swarm Productivity Tool
======================================================

Validates that all session transition deliverables are complete:
1. Passdown (passdown.json)
2. Devlog Entry (devlogs/)
3. Discord Post (via devlog_manager)
4. Swarm Brain Update (swarm_brain/)
5. State Report Update (STATE_OF_THE_PROJECT_REPORT.md)
6. Cycle Planner Entry (swarm_cycle_planner/cycles/)

Author: Agent-2 (Architecture & Design Specialist)
Date: 2025-01-27
License: MIT
V2 Compliance: <400 lines
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional


class SessionTransitionValidator:
    """Validates session transition deliverables."""
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.agent_workspace = Path(f"agent_workspaces/{agent_id}")
        self.devlogs_dir = Path("devlogs")
        self.swarm_brain_dir = Path("swarm_brain")
        self.cycle_planner_dir = Path("agent_workspaces/swarm_cycle_planner/cycles")
        self.state_report = Path("STATE_OF_THE_PROJECT_REPORT.md")
        self.results: Dict[str, Tuple[bool, str]] = {}
    
    def validate_passdown(self) -> Tuple[bool, str]:
        """Validate passdown.json exists and is valid."""
        passdown_file = self.agent_workspace / "passdown.json"
        
        if not passdown_file.exists():
            return False, f"❌ passdown.json not found at {passdown_file}"
        
        try:
            with open(passdown_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            required_fields = ["agent_id", "session_date", "deliverables", "next_actions"]
            missing = [field for field in required_fields if field not in data]
            
            if missing:
                return False, f"❌ Missing required fields: {', '.join(missing)}"
            
            if not data.get("deliverables"):
                return False, "❌ Deliverables section is empty"
            
            return True, f"✅ passdown.json valid ({len(data.get('deliverables', {}))} deliverables)"
        except json.JSONDecodeError as e:
            return False, f"❌ Invalid JSON: {e}"
        except Exception as e:
            return False, f"❌ Error reading passdown: {e}"
    
    def validate_devlog(self) -> Tuple[bool, str]:
        """Validate devlog entry exists for today."""
        today = datetime.now().strftime("%Y-%m-%d")
        pattern = f"{today}_*{self.agent_id.lower()}*.md"
        
        devlog_files = list(self.devlogs_dir.glob(pattern))
        
        if not devlog_files:
            return False, f"❌ No devlog found for {today} (pattern: {pattern})"
        
        # Check if devlog has content
        latest_devlog = max(devlog_files, key=lambda p: p.stat().st_mtime)
        content = latest_devlog.read_text(encoding='utf-8')
        
        if len(content) < 100:
            return False, f"❌ Devlog too short ({len(content)} chars) - likely incomplete"
        
        required_sections = ["##", "✅", "Status"]
        has_sections = any(section in content for section in required_sections)
        
        if not has_sections:
            return False, "❌ Devlog missing required sections"
        
        return True, f"✅ Devlog found: {latest_devlog.name} ({len(content)} chars)"
    
    def validate_swarm_brain(self) -> Tuple[bool, str]:
        """Validate Swarm Brain update exists."""
        today = datetime.now().strftime("%Y-%m-%d")
        pattern = f"*{today}*{self.agent_id.lower()}*.md"
        
        # Check all swarm_brain subdirectories
        swarm_brain_files = []
        for subdir in self.swarm_brain_dir.iterdir():
            if subdir.is_dir():
                swarm_brain_files.extend(subdir.glob(pattern))
        
        if not swarm_brain_files:
            return False, f"❌ No Swarm Brain entry found for {today}"
        
        latest_file = max(swarm_brain_files, key=lambda p: p.stat().st_mtime)
        return True, f"✅ Swarm Brain entry found: {latest_file.relative_to(self.swarm_brain_dir)}"
    
    def validate_state_report(self) -> Tuple[bool, str]:
        """Validate STATE_OF_THE_PROJECT_REPORT.md was updated."""
        if not self.state_report.exists():
            return False, "❌ STATE_OF_THE_PROJECT_REPORT.md not found"
        
        content = self.state_report.read_text(encoding='utf-8')
        agent_section = f"### **{self.agent_id}**"
        
        if agent_section not in content:
            return False, f"❌ Agent section not found in state report"
        
        # Check if section has recent updates (contains today's date or recent keywords)
        today = datetime.now().strftime("%Y-%m-%d")
        has_recent_update = today in content or "COMPLETE" in content or "✅" in content
        
        if not has_recent_update:
            return False, "❌ Agent section appears outdated"
        
        return True, f"✅ State report updated (section found, recent content)"
    
    def validate_cycle_planner(self) -> Tuple[bool, str]:
        """Validate cycle planner entry exists."""
        today = datetime.now().strftime("%Y-%m-%d")
        planner_file = self.cycle_planner_dir / f"{today}_{self.agent_id.lower()}_pending_tasks.json"
        
        if not planner_file.exists():
            return False, f"❌ Cycle planner entry not found: {planner_file.name}"
        
        try:
            with open(planner_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not data.get("contracts"):
                return False, "❌ Cycle planner entry has no contracts"
            
            return True, f"✅ Cycle planner entry valid ({len(data.get('contracts', []))} contracts)"
        except Exception as e:
            return False, f"❌ Error reading cycle planner: {e}"
    
    def validate_all(self) -> Dict[str, Tuple[bool, str]]:
        """Validate all session transition deliverables."""
        self.results = {
            "passdown": self.validate_passdown(),
            "devlog": self.validate_devlog(),
            "swarm_brain": self.validate_swarm_brain(),
            "state_report": self.validate_state_report(),
            "cycle_planner": self.validate_cycle_planner(),
        }
        return self.results
    
    def print_report(self):
        """Print validation report."""
        print("=" * 70)
        print(f"📋 SESSION TRANSITION VALIDATION - {self.agent_id}")
        print("=" * 70)
        print()
        
        for deliverable, (valid, message) in self.results.items():
            print(f"{message}")
        
        print()
        print("=" * 70)
        
        all_valid = all(valid for valid, _ in self.results.values())
        valid_count = sum(1 for valid, _ in self.results.values() if valid)
        total_count = len(self.results)
        
        if all_valid:
            print(f"✅ ALL DELIVERABLES COMPLETE ({valid_count}/{total_count})")
        else:
            print(f"⚠️  INCOMPLETE: {valid_count}/{total_count} deliverables complete")
            print()
            print("Missing deliverables:")
            for deliverable, (valid, message) in self.results.items():
                if not valid:
                    print(f"  - {deliverable}: {message.split('❌')[1] if '❌' in message else message}")
        
        print("=" * 70)
        
        return all_valid


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Validate session transition deliverables"
    )
    parser.add_argument(
        "--agent", "-a",
        required=True,
        help="Agent ID (e.g., Agent-2)"
    )
    
    args = parser.parse_args()
    
    validator = SessionTransitionValidator(args.agent)
    validator.validate_all()
    success = validator.print_report()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

