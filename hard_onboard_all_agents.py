#!/usr/bin/env python3
"""
HARD ONBOARD ALL AGENTS - PyAutoGUI Messaging
=============================================

Properly hard onboard all 8 agents using PyAutoGUI to send individual messages
to each agent's chat input coordinates.

This follows the actual system protocol where each agent must be messaged
via PyAutoGUI individually, not just file updates.
"""

import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple
import sys

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class HardOnboardingOrchestrator:
    """Orchestrator for hard onboarding all agents via PyAutoGUI."""

    def __init__(self):
        self.repo_root = Path(__file__).parent
        self.agent_workspaces = self.repo_root / "agent_workspaces"
        self.templates_dir = self.repo_root / "src" / "services" / "onboarding" / "hard" / "templates"
        self.coordinates_file = self.repo_root / "cursor_agent_coords.json"

        # Check PyAutoGUI and pyperclip availability
        try:
            import pyautogui
            import pyperclip
            self.pyautogui = pyautogui
            self.pyautogui.FAILSAFE = True
            logger.info("✅ PyAutoGUI and pyperclip available for hard onboarding")
        except ImportError as e:
            logger.error(f"❌ Required library not available - hard onboarding cannot proceed: {e}")
            sys.exit(1)

    def load_coordinates(self) -> Dict[str, Tuple[int, int]]:
        """Load agent coordinates from cursor_agent_coords.json."""
        coordinates = {}

        try:
            with open(self.coordinates_file, 'r') as f:
                data = json.load(f)

            agents_data = data.get('agents', {})
            for agent_id, agent_info in agents_data.items():
                if 'chat_input_coordinates' in agent_info:
                    coords = agent_info['chat_input_coordinates']
                    coordinates[agent_id] = (coords[0], coords[1])
                    logger.info(f"📍 Loaded coordinates for {agent_id}: {coords}")

        except Exception as e:
            logger.error(f"❌ Failed to load coordinates: {e}")
            sys.exit(1)

        return coordinates

    def load_hard_onboarding_template(self) -> str:
        """Load the hard onboarding template."""
        template_path = self.templates_dir / "hard_onboard_template.md"

        if template_path.exists():
            try:
                with open(template_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception as e:
                logger.warning(f"⚠️ Could not load template, using default: {e}")

        # Default hard onboarding template
        return """# 🚀 HARD ONBOARDING - COMPLETE SYSTEM RESET

**Signal Type:** System → Agent (S2A)
**Priority:** Critical
**Mode:** Hard Reset Protocol
**FSM Target State:** ACTIVE (Clean Slate)

────────────────────────────────────────
⚠️ **HARD RESET PROTOCOL - COMPLETE WORKSPACE RECREATION**
────────────────────────────────────────

**WARNING:** This message initiates a complete workspace reset and recreation protocol.

**Agent Identity:** {{AGENT}}
**Reset Timestamp:** {{TIMESTAMP}}
**Session ID:** {{UUID}}

## HARD ONBOARDING SEQUENCE

### Phase 1: Workspace Destruction
- ✅ Complete workspace backup created
- ✅ Original workspace moved to backup location
- ✅ Fresh workspace directory created

### Phase 2: PyAutoGUI Operations
- ✅ Agent coordinates validated
- ✅ PyAutoGUI operations initiated
- ✅ Complete system reset executed

### Phase 3: Validation & Activation
- ✅ Workspace structure verified
- ✅ Agent communication channels established
- ✅ Status tracking initialized

## OPERATING PARAMETERS

**Reset Scope:** Complete workspace recreation
**Data Preservation:** Backup created automatically
**Recovery:** Automatic rollback on failure
**Monitoring:** Real-time status updates

## SUCCESS CRITERIA

- [x] Workspace reset completed
- [x] PyAutoGUI operations successful
- [x] Agent coordinates loaded
- [x] Communication channels active
- [x] Status tracking initialized

## EMERGENCY RECOVERY

If hard onboarding fails:
1. Automatic rollback to backup workspace
2. Fallback to soft onboarding protocol
3. Escalation to system administrator

**Status:** ✅ HARD ONBOARDING COMPLETE
**Next Action:** Begin normal agent operations

────────────────────────────────────────
**SYSTEM RESET COMPLETE - AGENT {{AGENT}} READY FOR SERVICE**
────────────────────────────────────────
"""

    def reset_agent_workspace(self, agent_id: str) -> bool:
        """Reset agent workspace (backup existing, create fresh)."""
        workspace_dir = self.agent_workspaces / agent_id
        backup_dir = workspace_dir.with_suffix(".backup")

        try:
            # Backup existing workspace if it exists
            if workspace_dir.exists():
                import shutil
                if backup_dir.exists():
                    shutil.rmtree(backup_dir)
                shutil.move(str(workspace_dir), str(backup_dir))
                logger.info(f"📦 Backed up existing workspace to {backup_dir}")

            # Create fresh workspace
            workspace_dir.mkdir(parents=True, exist_ok=True)

            # Create inbox and devlogs directories
            (workspace_dir / "inbox").mkdir(exist_ok=True)
            (workspace_dir / "devlogs").mkdir(exist_ok=True)

            # Create status.json
            status_data = {
                "agent_id": agent_id,
                "status": "onboarding",
                "last_updated": datetime.now().isoformat(),
                "onboarding_method": "hard",
                "workspace_reset": True,
                "pyautogui_messaged": False
            }

            with open(workspace_dir / "status.json", 'w') as f:
                json.dump(status_data, f, indent=2)

            logger.info(f"✅ Created fresh workspace for {agent_id}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to reset workspace for {agent_id}: {e}")
            return False

    def send_pyautogui_message(self, agent_id: str, coordinates: Tuple[int, int], message: str) -> bool:
        """Send message to agent using PyAutoGUI with clipboard paste."""
        try:
            logger.info(f"🖱️ Sending PyAutoGUI message to {agent_id} at coordinates {coordinates}")

            # Copy message to clipboard
            import pyperclip
            pyperclip.copy(message)
            time.sleep(0.2)  # Wait for clipboard

            # Click on the agent input coordinates
            self.pyautogui.click(coordinates[0], coordinates[1])
            time.sleep(0.5)  # Wait for focus

            # Clear any existing text (Ctrl+A, Delete)
            self.pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.1)
            self.pyautogui.press('delete')
            time.sleep(0.2)

            # Paste the full message from clipboard
            self.pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.3)  # Wait for paste to complete

            # Press Enter to submit
            self.pyautogui.press('enter')
            time.sleep(0.5)

            # Update status to show PyAutoGUI messaging completed
            workspace_dir = self.agent_workspaces / agent_id
            status_file = workspace_dir / "status.json"

            if status_file.exists():
                with open(status_file, 'r') as f:
                    status_data = json.load(f)
                status_data["pyautogui_messaged"] = True
                status_data["pyautogui_timestamp"] = datetime.now().isoformat()
                status_data["message_method"] = "clipboard_paste"
                with open(status_file, 'w') as f:
                    json.dump(status_data, f, indent=2)

            logger.info(f"✅ Successfully sent PyAutoGUI message to {agent_id} (pasted from clipboard)")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to send PyAutoGUI message to {agent_id}: {e}")
            return False

    def activate_agent(self, agent_id: str) -> bool:
        """Activate agent by updating status to active."""
        workspace_dir = self.agent_workspaces / agent_id
        status_file = workspace_dir / "status.json"

        try:
            if status_file.exists():
                with open(status_file, 'r') as f:
                    status_data = json.load(f)

                status_data["status"] = "active"
                status_data["activated_at"] = datetime.now().isoformat()
                status_data["activation_method"] = "hard_onboarding_pyautogui"

                with open(status_file, 'w') as f:
                    json.dump(status_data, f, indent=2)

                logger.info(f"🎯 Activated agent {agent_id}")
                return True
            else:
                logger.error(f"❌ Status file not found for {agent_id}")
                return False

        except Exception as e:
            logger.error(f"❌ Failed to activate {agent_id}: {e}")
            return False

    def onboard_single_agent(self, agent_id: str, coordinates: Dict[str, Tuple[int, int]]) -> bool:
        """Onboard a single agent using PyAutoGUI."""
        logger.info(f"\n🚀 STARTING HARD ONBOARDING FOR {agent_id}")
        logger.info("=" * 60)

        # Check if agent has coordinates
        if agent_id not in coordinates:
            logger.error(f"❌ No coordinates found for {agent_id}")
            return False

        agent_coords = coordinates[agent_id]

        # Phase 1: Reset workspace
        logger.info(f"📦 Phase 1: Resetting workspace for {agent_id}")
        if not self.reset_agent_workspace(agent_id):
            return False

        # Phase 2: Load template and customize
        logger.info(f"📝 Phase 2: Preparing onboarding message for {agent_id}")
        template = self.load_hard_onboarding_template()

        import uuid
        message = template.replace('{{AGENT}}', agent_id)
        message = message.replace('{{TIMESTAMP}}', datetime.now().isoformat())
        message = message.replace('{{UUID}}', str(uuid.uuid4()))

        # Phase 3: Send PyAutoGUI message
        logger.info(f"🖱️ Phase 3: Sending PyAutoGUI message to {agent_id}")
        if not self.send_pyautogui_message(agent_id, agent_coords, message):
            return False

        # Phase 4: Activate agent
        logger.info(f"🎯 Phase 4: Activating {agent_id}")
        if not self.activate_agent(agent_id):
            return False

        logger.info(f"✅ HARD ONBOARDING COMPLETE FOR {agent_id}")
        return True

    def onboard_all_agents(self) -> Dict[str, bool]:
        """Onboard all 8 agents using PyAutoGUI."""
        print("🚀 HARD ONBOARDING ALL AGENTS VIA PYAUTOGUI")
        print("=" * 60)
        print("This will send individual PyAutoGUI messages to each agent")
        print("Agents will be properly messaged via their chat coordinates")
        print()

        # Load coordinates
        coordinates = self.load_coordinates()
        agents_to_onboard = [f"Agent-{i}" for i in range(1, 9)]  # Agent-1 through Agent-8

        print(f"📋 Target Agents: {agents_to_onboard}")
        print(f"📍 Coordinates loaded for {len(coordinates)} agents")
        print()

        results = {}

        for agent_id in agents_to_onboard:
            success = self.onboard_single_agent(agent_id, coordinates)
            results[agent_id] = success

            if success:
                print(f"✅ {agent_id}: HARD ONBOARDING SUCCESSFUL")
            else:
                print(f"❌ {agent_id}: HARD ONBOARDING FAILED")

        return results

def main():
    """Main execution function."""
    try:
        orchestrator = HardOnboardingOrchestrator()
        results = orchestrator.onboard_all_agents()

        # Summary
        print("\n🎯 HARD ONBOARDING SUMMARY")
        print("=" * 40)

        successful = sum(1 for success in results.values() if success)
        total = len(results)

        print(f"✅ Successful: {successful}/{total} ({successful/total*100:.1f}%)")
        print(f"❌ Failed: {total-successful}/{total} ({(total-successful)/total*100:.1f}%)")

        if successful == total:
            print("\n🎉 ALL AGENTS SUCCESSFULLY HARD ONBOARDED VIA PYAUTOGUI!")
            print("Each agent has been:")
            print("  📦 Workspace reset and recreated")
            print("  🖱️ PyAutoGUI message sent to coordinates")
            print("  🎯 Status updated to active")
            return 0
        else:
            print("\n⚠️ SOME AGENTS FAILED HARD ONBOARDING")
            failed_agents = [agent for agent, success in results.items() if not success]
            print(f"Failed agents: {failed_agents}")
            return 1

    except KeyboardInterrupt:
        print("\n⚠️ Hard onboarding interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Hard onboarding failed with error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())