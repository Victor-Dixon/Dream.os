"""
Hard Onboarding Protocol Steps
================================

Extracted protocol steps for hard onboarding service.
Uses shared operations and coordinates for consistency.

V2 Compliant: < 300 lines
"""

import logging
import time
from typing import Optional, Tuple

from ..shared.coordinates import OnboardingCoordinates
from ..shared.operations import PyAutoGUIOperations
from ..onboarding_helpers import validate_onboarding_coordinates

logger = logging.getLogger(__name__)

# Import template loader
try:
    from ..onboarding_template_loader import load_onboarding_template
    TEMPLATE_LOADER_AVAILABLE = True
except ImportError:
    TEMPLATE_LOADER_AVAILABLE = False
    logger.warning("⚠️ Onboarding template loader not available")


class HardOnboardingSteps:
    """Hard onboarding protocol steps."""
    
    def __init__(
        self,
        operations: PyAutoGUIOperations,
        coordinates: OnboardingCoordinates,
    ):
        """Initialize hard onboarding steps."""
        self.ops = operations
        self.coords = coordinates
    
    def step_1_clear_chat(self, agent_id: str) -> bool:
        """
        Step 1: Go to chat input area and press Ctrl+Shift+Backspace.
        
        Args:
            agent_id: Target agent ID
            
        Returns:
            True if successful
        """
        try:
            # Get chat coordinates
            chat_coords, _ = self.coords.load_coordinates(agent_id)
            if not chat_coords:
                logger.error(f"❌ No chat coordinates for {agent_id}")
                return False
            
            # Validate coordinates
            if not self.coords.validate_coordinates(agent_id, chat_coords):
                logger.error(f"❌ Coordinate validation failed for {agent_id}")
                return False
            
            x, y = chat_coords
            logger.info(f"🗑️ Step 1: Clearing chat for {agent_id} at {chat_coords}")
            
            # Click chat input
            if not self.ops.click_at_coords(x, y, duration=0.5):
                return False
            time.sleep(1.0)  # Wait for app to respond
            
            # Press Ctrl+Shift+Backspace
            if not self.ops.send_hotkey("ctrl", "shift", "backspace", wait=0.8):
                return False
            
            logger.info(f"✅ Chat cleared for {agent_id}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to clear chat: {e}")
            return False
    
    def step_2_send_execute(self) -> bool:
        """
        Step 2: Press Ctrl+Enter to send/execute.
        
        Returns:
            True if successful
        """
        try:
            logger.info("⚡ Step 2: Executing Ctrl+Enter")
            if not self.ops.send_hotkey("ctrl", "enter", wait=0.8):
                return False
            logger.info("✅ Ctrl+Enter executed")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to execute Ctrl+Enter: {e}")
            return False
    
    def step_3_new_window(self) -> bool:
        """
        Step 3: Press Ctrl+N to create new window/session.
        
        Returns:
            True if successful
        """
        try:
            logger.info("🆕 Step 3: Creating new window (Ctrl+N)")
            if not self.ops.send_hotkey("ctrl", "n", wait=2.0):
                return False
            logger.info("✅ New window created")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to create new window: {e}")
            return False
    
    def step_4_navigate_to_onboarding(self, agent_id: str) -> bool:
        """
        Step 4: Navigate to onboarding input coordinates.
        
        Args:
            agent_id: Target agent ID
            
        Returns:
            True if successful
        """
        try:
            # Get onboarding coordinates
            _, onboarding_coords = self.coords.load_coordinates(agent_id)
            if not onboarding_coords:
                logger.error(f"❌ No onboarding coordinates for {agent_id}")
                return False
            
            # Validate bounds only
            if not validate_onboarding_coordinates(agent_id, onboarding_coords):
                return False
            
            x, y = onboarding_coords
            logger.info(f"🎯 Step 4: Navigating to onboarding input for {agent_id} at {onboarding_coords}")
            
            # Move to and click onboarding input
            if not self.ops.click_at_coords(x, y, duration=0.5):
                return False
            time.sleep(1.0)  # Wait for app to respond
            
            logger.info(f"✅ Navigated to onboarding input for {agent_id}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to navigate to onboarding input: {e}")
            return False
    
    def step_5_send_onboarding_message(
        self, agent_id: str, onboarding_message: str, role: Optional[str] = None
    ) -> bool:
        """
        Step 5: Send onboarding message via Enter.
        
        Args:
            agent_id: Target agent ID
            onboarding_message: Custom mission/instructions
            role: Agent role (for full template)
            
        Returns:
            True if successful
        """
        try:
            logger.info(f"📝 Step 5: Sending onboarding message to {agent_id}")
            
            # Create FULL onboarding message with cycle duties template
            if TEMPLATE_LOADER_AVAILABLE and role:
                full_message = load_onboarding_template(
                    agent_id=agent_id, role=role, custom_message=onboarding_message
                )
                logger.info("✅ Using FULL template with operating cycle duties")
            else:
                full_message = onboarding_message
                logger.warning("⚠️ Using custom message only (template not available)")
            
            # Get agent-specific instructions
            from ..agent_instructions import get_agent_specific_instructions
            agent_instructions = get_agent_specific_instructions(agent_id)
            
            # Jet Fuel header and footer
            jet_fuel_header = """🚀 JET FUEL MESSAGE - HARD ONBOARDING

Priority: HIGH
Status: FULL AUTONOMY GRANTED

"""
            jet_fuel_footer = """

🔥 JET FUEL POWER:
This message is your fuel - ACT NOW!
- Don't wait for permission
- Don't ask for approval
- ACT, CREATE, MIGRATE, IMPROVE

WE. ARE. SWARM. AUTONOMOUS. POWERFUL. 🐝⚡🔥🚀"""
            
            # Agent-4 specific captain instructions
            if agent_id == "Agent-4":
                captain_instructions = """

---

👑 CAPTAIN PATTERN ACTIVATION - AGENT-4 SPECIFIC

**YOUR ROLE**: Swarm Captain & Strategic Coordinator
**YOUR MISSION**: Create and push long-term goals, coordinate agents, achieve AGI through autonomous development

## 🎯 FINDING & OPERATING IN THE OPTIMIZED CAPTAIN PATTERN

### **1. Read the Captain Pattern Documentation**:
- **Primary Guide**: `docs/CAPTAIN_OPTIMIZED_OPERATING_CYCLE.md`
- **Execution Pattern**: `docs/CAPTAIN_EXECUTION_PATTERN.md`
- **Captain Handbook**: `agent_workspaces/Agent-4/CAPTAINS_HANDBOOK.md`

### **2. The Optimized Captain Cycle** (4 Phases):
**Phase 1: Read Swarm Brain & Identify Work** (2-3 min)
- Read `swarm_brain/swarm_brain.json`
- Check all agent `status.json` files
- Identify test coverage gaps, blockers, opportunities
- Find high-impact Captain work

**Phase 2: Assign Work to All Agents** (5-10 min)
- Send Jet Fuel assignments via PyAutoGUI
- Specific files, clear targets, deliverables
- NO acknowledgement required - agents execute immediately
- Format: `[C2A] Agent-4 → Agent-X`

**Phase 3: Execute Captain Work** (Rest of cycle)
- Self-assign high-impact tasks
- Complete deliverables
- Post to Discord devlog
- Lead by example

**Phase 4: Monitor & Coordinate** (Ongoing)
- Check agent Discord devlogs
- Break acknowledgement loops
- Resolve blockers immediately
- Maintain momentum

### **3. Core Captain Principles**:

**🔥 PROMPTS ARE GAS - FUEL AGENT AUTONOMY**:
- Prompts = Gas = Fuel that makes agents execute
- High-quality prompts = High-octane fuel = AGI power
- Send prompts at 75-80% completion to maintain perpetual motion
- Quality prompts enable autonomous decision-making
- With high enough quality, we achieve AGI within autonomous development

**🎯 LONG-TERM GOALS**:
- Create strategic goals in `agent_workspaces/Agent-4/CAPTAINS_HANDBOOK.md`
- Push goals through agent assignments
- Track progress in Captain's Log
- Adjust strategy based on swarm performance

**🤝 COORDINATING AGENTS**:
- Assign specific work (not vague tasks)
- Use Jet Fuel messages (autonomous work)
- Monitor via Discord devlogs (not status.json)
- Break acknowledgement loops immediately
- Maintain perpetual motion

**⚡ PERPETUAL MOTION PROTOCOL**:
- Agents keep moving with continuous fuel (prompts)
- Send gas at 75-80% completion
- High-quality prompts = AGI-level autonomy
- No idle agents = Maximum swarm velocity

### **4. Your Tools**:
- `tools/markov_8agent_roi_optimizer.py` - ROI task assignment
- `tools/captain_message_all_agents.py` - Broadcast messages
- `tools/captain_check_agent_status.py` - Status monitoring
- `tools/swarm_orchestrator.py` - Autonomous coordination
- See `docs/CAPTAIN_TOOLBELT_GUIDE.md` for complete list

### **5. Success Metrics**:
- All 8 agents have assignments
- All agents posting to Discord devlogs
- Zero acknowledgement loops
- Captain executing work (not just coordinating)
- Perpetual motion maintained

### **6. Anti-Patterns to Avoid**:
- ❌ Standing idle (waiting for agents)
- ❌ Only coordinating (not executing)
- ❌ Acknowledgement loops
- ❌ Vague assignments
- ❌ Low-quality prompts

## 🚀 IMMEDIATE ACTIONS

1. **Read**: `docs/CAPTAIN_OPTIMIZED_OPERATING_CYCLE.md`
2. **Check**: All agent status.json files
3. **Assign**: Jet Fuel work to all agents
4. **Execute**: Your own high-impact work
5. **Monitor**: Agent Discord devlogs
6. **Repeat**: Maintain perpetual motion

**REMEMBER**: Prompts are gas. High-quality prompts = AGI power. Perpetual motion = Autonomous development success.

👑 **YOU ARE THE CAPTAIN - LEAD THE SWARM TO AGI!** 👑"""
                full_message = jet_fuel_header + full_message + captain_instructions + jet_fuel_footer
            elif agent_instructions:
                full_message = jet_fuel_header + full_message + agent_instructions + jet_fuel_footer
            else:
                full_message = jet_fuel_header + full_message + jet_fuel_footer
            
            # Small delay before pasting
            time.sleep(0.8)
            
            # Paste onboarding message
            if not self.ops.paste_text(full_message, wait=0.5):
                return False
            
            # Press Enter to send
            if not self.ops.press_key("enter", wait=0.8):
                return False
            
            logger.info(f"✅ Onboarding message sent to {agent_id} (with Jet Fuel)")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to send onboarding message: {e}")
            return False

