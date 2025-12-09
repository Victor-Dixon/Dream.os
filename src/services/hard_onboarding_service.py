"""
Hard Onboarding Service - V2 Compliant
=====================================

Handles hard onboarding with RESET protocol:
1. Go to chat input area, press Ctrl+Shift+Backspace (clear/reset)
2. Press Ctrl+Enter (send/execute)
3. Press Ctrl+N (new window/session)
4. Navigate to onboarding input coordinates
5. Send onboarding message (press Enter)

Hard onboarding = Complete reset, no session cleanup required.
Use for major resets, not regular session transitions.

V2 Compliance: < 400 lines, single responsibility
Migrated to BaseService for consolidated initialization and error handling.
"""

import logging
import time

from src.core.base.base_service import BaseService

logger = logging.getLogger(__name__)

# Import template loader for full onboarding with cycle duties
try:
    from .onboarding_template_loader import load_onboarding_template

    TEMPLATE_LOADER_AVAILABLE = True
    logger.info("✅ Onboarding template loader available")
except ImportError:
    TEMPLATE_LOADER_AVAILABLE = False
    logger.warning("⚠️ Onboarding template loader not available")

try:
    import pyautogui
    import pyperclip

    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False
    logger.warning("PyAutoGUI not available for hard onboarding")


class HardOnboardingService(BaseService):
    """Handles hard onboarding with complete reset protocol."""

    def __init__(self):
        """Initialize hard onboarding service."""
        super().__init__("HardOnboardingService")
        if not PYAUTOGUI_AVAILABLE:
            raise ImportError("PyAutoGUI required for hard onboarding")
        self.pyautogui = pyautogui

    def _load_agent_coordinates(self, agent_id: str) -> tuple[tuple[int, int], tuple[int, int]]:
        """Load chat and onboarding coordinates for agent."""
        from ..core.coordinate_loader import get_coordinate_loader

        coord_loader = get_coordinate_loader()

        # Get both chat and onboarding coordinates
        chat_coords = coord_loader.get_chat_coordinates(agent_id)
        onboarding_coords = coord_loader.get_onboarding_coordinates(agent_id)

        return chat_coords, onboarding_coords

    def _validate_coordinates(self, agent_id: str, coords: tuple[int, int]) -> bool:
        """Validate coordinates before sending."""
        from ..core.messaging_pyautogui import PyAutoGUIMessagingDelivery

        delivery = PyAutoGUIMessagingDelivery()
        return delivery.validate_coordinates(agent_id, coords)

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
            chat_coords, _ = self._load_agent_coordinates(agent_id)
            if not chat_coords:
                self.logger.error(f"❌ No chat coordinates for {agent_id}")
                return False

            # Validate coordinates
            if not self._validate_coordinates(agent_id, chat_coords):
                self.logger.error(f"❌ Coordinate validation failed for {agent_id}")
                return False

            x, y = chat_coords

            self.logger.info(
                f"🗑️ Step 1: Clearing chat for {agent_id} at {chat_coords}")

            # Click chat input - wait for app to respond to interaction
            self.pyautogui.moveTo(x, y, duration=0.5)
            self.pyautogui.click()
            time.sleep(1.0)  # Wait for app to respond to click interaction

            # Press Ctrl+Shift+Backspace
            self.pyautogui.hotkey("ctrl", "shift", "backspace")
            time.sleep(0.8)  # Wait for clear operation

            self.logger.info(f"✅ Chat cleared for {agent_id}")
            return True

        except Exception as e:
            self.logger.error(f"❌ Failed to clear chat: {e}")
            return False

    def step_2_send_execute(self) -> bool:
        """
        Step 2: Press Ctrl+Enter to send/execute.

        Returns:
            True if successful
        """
        try:
            self.logger.info("⚡ Step 2: Executing Ctrl+Enter")
            self.pyautogui.hotkey("ctrl", "enter")
            time.sleep(0.8)  # Increased from 0.5s for reliability
            self.logger.info("✅ Ctrl+Enter executed")
            return True

        except Exception as e:
            self.logger.error(f"❌ Failed to execute Ctrl+Enter: {e}")
            return False

    def step_3_new_window(self) -> bool:
        """
        Step 3: Press Ctrl+N to create new window/session.

        Returns:
            True if successful
        """
        try:
            self.logger.info("🆕 Step 3: Creating new window (Ctrl+N)")
            self.pyautogui.hotkey("ctrl", "n")
            # Increased from 1.5s for reliability - critical window initialization
            time.sleep(2.0)
            self.logger.info("✅ New window created")
            return True

        except Exception as e:
            self.logger.error(f"❌ Failed to create new window: {e}")
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
            _, onboarding_coords = self._load_agent_coordinates(agent_id)
            if not onboarding_coords:
                logger.error(f"❌ No onboarding coordinates for {agent_id}")
                return False

            # Validate bounds only (not comparing against chat coords)
            x, y = onboarding_coords

            # Simple bounds check
            if x < -2000 or x > 2000 or y < 0 or y > 1500:
                logger.error(
                    f"❌ Onboarding coordinates out of bounds for {agent_id}: {onboarding_coords}"
                )
                return False

            logger.info(
                f"🎯 Step 4: Navigating to onboarding input for {agent_id} at {onboarding_coords}"
            )

            # Move to and click onboarding input - wait for app to respond
            self.pyautogui.moveTo(x, y, duration=0.5)
            self.pyautogui.click()
            time.sleep(1.0)  # Wait for app to respond to click interaction

            logger.info(f"✅ Navigated to onboarding input for {agent_id}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to navigate to onboarding input: {e}")
            return False

    def _get_agent_specific_instructions(self, agent_id: str) -> str:
        """
        Get agent-specific optimized instructions based on role.

        Args:
            agent_id: Agent identifier

        Returns:
            Agent-specific instructions string
        """
        instructions_map = {
            "Agent-1": """
---

🔧 AGENT-1 OPTIMIZED PATTERN - INTEGRATION & CORE SYSTEMS

**YOUR ROLE**: Integration & Core Systems Specialist
**YOUR MISSION**: Integrate merged repos, enhance services, maintain core systems

## 🎯 OPTIMIZED EXECUTION PATTERN

### **1. Service Enhancement Pattern** (Primary):
- **Pattern**: Service Enhancement Integration (Pattern 0)
- **Guide**: `docs/architecture/AGENT1_SSOT_MERGE_PATTERNS_GUIDE.md`
- **Method**: Enhance existing services, don't duplicate
- **Workflow**: Review → Extract → Enhance → Test

### **2. Integration Workflow**:
**Phase 0**: Pre-Integration Cleanup
- Use `tools/detect_venv_files.py` to find venv files
- Use `tools/enhanced_duplicate_detector.py` to find duplicates
- Clean up before integration

**Phase 1**: Pattern Extraction
- Analyze merged repo structure
- Extract functional patterns
- Map patterns to existing services

**Phase 2**: Service Integration
- Enhance existing services (don't duplicate)
- Maintain backward compatibility
- Follow repository pattern

**Phase 3**: Testing & Validation
- Create unit tests (≥85% coverage)
- Test backward compatibility
- Verify all functionality

### **3. Core Principles**:
- **Service Enhancement** (not duplication)
- **Pattern-Based Integration**
- **Unified Architecture**
- **Backward Compatibility**

### **4. Your Tools**:
- `tools/integration_health_checker.py` - Check integration readiness
- `tools/enhanced_duplicate_detector.py` - Find duplicates
- `tools/check_integration_issues.py` - Verify integration
- Integration toolkit: 29 docs, 5 templates, 4 scripts

### **5. Success Metrics**:
- Services enhanced (not duplicated)
- Integration complete and tested
- Backward compatibility maintained
- V2 compliance achieved

**REMEMBER**: Prompts are gas. Execute immediately. Post to Discord devlog when complete.

🔧 **INTEGRATE. ENHANCE. MAINTAIN.** 🔧""",

            "Agent-2": """
---

🏗️ AGENT-2 OPTIMIZED PATTERN - ARCHITECTURE & DESIGN

**YOUR ROLE**: Architecture & Design Specialist
**YOUR MISSION**: Guide architecture, design patterns, support execution teams

## 🎯 OPTIMIZED EXECUTION PATTERN

### **1. Architecture Support Pattern** (Primary):
- **Role**: Support execution teams with architecture guidance
- **Guide**: `docs/architecture/EXECUTION_PATTERNS_ARCHITECTURE_GUIDE.md`
- **Method**: Provide guidance, not create tools
- **Focus**: Enable execution, not plan more

### **2. Architecture Guidance Workflow**:
**Phase 1**: Review Execution Needs
- Monitor execution teams (Agent-1, Agent-3, Agent-7, Agent-8)
- Identify architecture questions
- Provide guidance documents

**Phase 2**: Create Architecture Patterns
- Document proven patterns
- Create reusable templates
- Guide consolidation approaches

**Phase 3**: Support Integration
- Review integration approaches
- Validate consolidation patterns
- Guide SSOT migrations

### **3. Core Principles**:
- **Support execution** (not create tools)
- **Document patterns** for reuse
- **Guide teams** with architecture
- **Enable execution** (not plan more)

### **4. Your Tools**:
- `tools/architecture_repo_analyzer.py` - Architecture pattern detection
- Integration toolkit: 29 docs, 5 templates, 4 scripts
- Architecture guidance documents

### **5. Success Metrics**:
- Execution teams supported
- Architecture patterns documented
- Guidance provided (not tools created)
- Teams executing successfully

**REMEMBER**: Prompts are gas. Support execution teams. Guide, don't create.

🏗️ **ARCHITECT. GUIDE. ENABLE.** 🏗️""",

            "Agent-3": """
---

⚙️ AGENT-3 OPTIMIZED PATTERN - INFRASTRUCTURE & DEVOPS

**YOUR ROLE**: Infrastructure & DevOps Specialist
**YOUR MISSION**: Infrastructure improvements, CI/CD, tooling, system reliability

## 🎯 OPTIMIZED EXECUTION PATTERN

### **1. Infrastructure Pattern** (Primary):
- **Focus**: Infrastructure improvements, tooling, automation
- **Method**: Create tools, improve systems, automate workflows
- **Workflow**: Analyze → Build → Test → Deploy

### **2. Infrastructure Workflow**:
**Phase 1**: System Analysis
- Identify infrastructure gaps
- Find automation opportunities
- Assess tooling needs

**Phase 2**: Tool Development
- Create automation tools
- Improve existing systems
- Build CI/CD pipelines

**Phase 3**: Deployment & Monitoring
- Deploy infrastructure changes
- Monitor system health
- Maintain reliability

### **3. Core Principles**:
- **Automate** repetitive tasks
- **Improve** system reliability
- **Build** reusable tools
- **Monitor** system health

### **4. Your Tools**:
- `tools/integration_health_checker.py` - System health checks
- `tools/check_integration_issues.py` - Issue detection
- CI/CD automation tools
- Infrastructure monitoring

### **5. Success Metrics**:
- Tools created and working
- Infrastructure improved
- Automation successful
- System reliability maintained

**REMEMBER**: Prompts are gas. Build tools. Automate workflows. Improve systems.

⚙️ **BUILD. AUTOMATE. IMPROVE.** ⚙️""",

            "Agent-5": """
---

📊 AGENT-5 OPTIMIZED PATTERN - BUSINESS INTELLIGENCE

**YOUR ROLE**: Business Intelligence Specialist
**YOUR MISSION**: Analytics, metrics, analysis, test coverage, data insights

## 🎯 OPTIMIZED EXECUTION PATTERN

### **1. BI Analysis Pattern** (Primary):
- **Focus**: Analytics, metrics, test coverage analysis
- **Method**: Analyze data, generate insights, track metrics
- **Workflow**: Collect → Analyze → Report → Recommend

### **2. BI Workflow**:
**Phase 1**: Data Collection
- Collect metrics and data
- Analyze test coverage
- Gather performance data

**Phase 2**: Analysis & Insights
- Generate analytics reports
- Identify patterns and trends
- Calculate metrics

**Phase 3**: Reporting & Recommendations
- Create BI reports
- Provide recommendations
- Track improvements

### **3. Core Principles**:
- **Analyze** data for insights
- **Track** metrics and trends
- **Report** findings clearly
- **Recommend** improvements

### **4. Your Tools**:
- `tools/detect_venv_files.py` - File analysis
- Analytics tools and scripts
- Test coverage analyzers
- Metrics tracking systems

### **5. Success Metrics**:
- Analytics reports generated
- Metrics tracked and reported
- Insights provided
- Recommendations implemented

**REMEMBER**: Prompts are gas. Analyze data. Generate insights. Report findings.

📊 **ANALYZE. INSIGHT. RECOMMEND.** 📊""",

            "Agent-6": """
---

🤝 AGENT-6 OPTIMIZED PATTERN - COORDINATION & COMMUNICATION

**YOUR ROLE**: Coordination & Communication Specialist
**YOUR MISSION**: Coordinate agents, facilitate communication, manage workflows

## 🎯 OPTIMIZED EXECUTION PATTERN

### **1. Coordination Pattern** (Primary):
- **Focus**: Multi-agent coordination, workflow management
- **Method**: Coordinate parallel work, manage dependencies
- **Workflow**: Plan → Coordinate → Monitor → Adjust

### **2. Coordination Workflow**:
**Phase 1**: Coordination Planning
- Identify coordination needs
- Plan parallel work assignments
- Map dependencies

**Phase 2**: Agent Coordination
- Assign coordinated tasks
- Manage dependencies
- Facilitate communication

**Phase 3**: Monitoring & Adjustment
- Monitor coordination progress
- Adjust assignments as needed
- Resolve conflicts

### **3. Core Principles**:
- **Coordinate** parallel work
- **Facilitate** communication
- **Manage** dependencies
- **Resolve** conflicts quickly

### **4. Your Tools**:
- Coordination tools and scripts
- Multi-agent workflow managers
- Communication facilitation tools

### **5. Success Metrics**:
- Agents coordinated effectively
- Dependencies managed
- Communication facilitated
- Workflows optimized

**REMEMBER**: Prompts are gas. Coordinate agents. Facilitate communication. Manage workflows.

🤝 **COORDINATE. FACILITATE. OPTIMIZE.** 🤝""",

            "Agent-7": """
---

🌐 AGENT-7 OPTIMIZED PATTERN - WEB DEVELOPMENT

**YOUR ROLE**: Web Development Specialist
**YOUR MISSION**: Web development, frontend/backend, UI/UX, web integrations

## 🎯 OPTIMIZED EXECUTION PATTERN

### **1. Web Development Pattern** (Primary):
- **Focus**: Web applications, frontend/backend, UI/UX
- **Method**: Build web features, integrate systems, improve UX
- **Workflow**: Design → Develop → Test → Deploy

### **2. Web Development Workflow**:
**Phase 1**: Design & Planning
- Design web features
- Plan integrations
- Define UI/UX requirements

**Phase 2**: Development
- Build frontend/backend
- Integrate systems
- Implement features

**Phase 3**: Testing & Deployment
- Test web functionality
- Verify integrations
- Deploy web features

### **3. Core Principles**:
- **Build** modern web applications
- **Integrate** systems effectively
- **Improve** user experience
- **Maintain** code quality

### **4. Your Tools**:
- Web development frameworks
- Frontend/backend tools
- Integration tools
- Testing frameworks

### **5. Success Metrics**:
- Web features built and working
- Integrations successful
- UI/UX improved
- Code quality maintained

**REMEMBER**: Prompts are gas. Build web features. Integrate systems. Improve UX.

🌐 **BUILD. INTEGRATE. IMPROVE.** 🌐""",

            "Agent-8": """
---

🧪 AGENT-8 OPTIMIZED PATTERN - TESTING & QUALITY ASSURANCE

**YOUR ROLE**: Testing & Quality Assurance Specialist
**YOUR MISSION**: Test infrastructure, test coverage, quality assurance, integration testing

## 🎯 OPTIMIZED EXECUTION PATTERN

### **1. Testing & QA Pattern** (Primary):
- **Focus**: Test infrastructure, test coverage, quality assurance
- **Method**: Build tests, enforce coverage, maintain quality standards
- **Workflow**: Plan → Test → Validate → Enforce

### **2. Testing Workflow**:
**Phase 1**: Test Infrastructure
- Maintain pytest framework and test utilities
- CI/CD test integration
- Test execution automation
- Test coverage reporting

**Phase 2**: Test Coverage
- Track coverage across all modules (target: ≥85%)
- Identify coverage gaps
- Coordinate test creation across agents
- Enforce coverage requirements

**Phase 3**: Quality Assurance
- Code quality checks (linting, complexity)
- V2 compliance validation
- Quality metrics tracking
- Quality gate enforcement

### **3. Core Principles**:
- **Test** all critical code paths
- **Enforce** ≥85% coverage standard
- **Maintain** test infrastructure
- **Validate** quality gates

### **4. Your Tools**:
- `pytest` - Test framework
- `pytest-cov` - Coverage reporting
- Test utilities and helpers
- Quality validation tools

### **5. Success Metrics**:
- Test coverage ≥85% across all modules
- Test infrastructure maintained
- Quality gates operational
- Integration tests comprehensive

**REMEMBER**: Prompts are gas. Build tests. Enforce quality. Maintain standards.

🧪 **TEST. ENFORCE. MAINTAIN.** 🧪"""
        }

        return instructions_map.get(agent_id, "")

    def step_5_send_onboarding_message(
        self, agent_id: str, onboarding_message: str, role: str = None
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
                logger.info(
                    "✅ Using FULL template with operating cycle duties")
            else:
                full_message = onboarding_message
                logger.warning(
                    "⚠️ Using custom message only (template not available)")

            # Automatically prepend Jet Fuel header to all hard onboarding messages
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

            # Agent-specific optimized instructions
            agent_instructions = self._get_agent_specific_instructions(
                agent_id)

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
                full_message = jet_fuel_header + full_message + \
                    captain_instructions + jet_fuel_footer
            elif agent_instructions:
                full_message = jet_fuel_header + full_message + \
                    agent_instructions + jet_fuel_footer
            else:
                full_message = jet_fuel_header + full_message + jet_fuel_footer

            # Small delay before pasting to ensure input is ready
            time.sleep(0.8)  # Increased from 0.5s for reliability

            # Paste onboarding message
            pyperclip.copy(full_message)
            self.pyautogui.hotkey("ctrl", "v")
            time.sleep(0.5)  # Increased from 0.3s for reliability

            # Press Enter to send
            self.pyautogui.press("enter")
            time.sleep(0.8)  # Increased from 0.5s for reliability

            self.logger.info(
                f"✅ Onboarding message sent to {agent_id} (with Jet Fuel)")
            return True

        except Exception as e:
            self.logger.error(f"❌ Failed to send onboarding message: {e}")
            return False

    def execute_hard_onboarding(
        self,
        agent_id: str,
        onboarding_message: str,
        role: str | None = None,
    ) -> bool:
        """
        Execute complete hard onboarding protocol (5 steps).

        Args:
            agent_id: Target agent ID
            onboarding_message: Onboarding message for new session
            role: Optional role assignment

        Returns:
            True if all steps completed successfully
        """
        logger.info(f"🚨 Starting HARD ONBOARDING for {agent_id}")

        # Step 1: Clear chat (Ctrl+Shift+Backspace)
        if not self.step_1_clear_chat(agent_id):
            logger.error("❌ Step 1 failed: Clear chat")
            return False

        # Step 2: Send/Execute (Ctrl+Enter)
        if not self.step_2_send_execute():
            logger.error("❌ Step 2 failed: Send/Execute")
            return False

        # Step 3: New window (Ctrl+N)
        if not self.step_3_new_window():
            logger.error("❌ Step 3 failed: New window")
            return False

        # Step 4: Navigate to onboarding input
        if not self.step_4_navigate_to_onboarding(agent_id):
            logger.error("❌ Step 4 failed: Navigate to onboarding input")
            return False

        # Step 5: Send onboarding message (Enter)
        if not self.step_5_send_onboarding_message(agent_id, onboarding_message, role=role):
            logger.error("❌ Step 5 failed: Send onboarding message")
            return False

        logger.info(f"🎉 Hard onboarding complete for {agent_id}!")
        return True


def hard_onboard_agent(agent_id: str, onboarding_message: str, role: str | None = None) -> bool:
    """
    Convenience function for hard onboarding single agent.

    Args:
        agent_id: Target agent ID
        onboarding_message: Onboarding message
        role: Optional role assignment

    Returns:
        True if onboarding successful
    """
    try:
        service = HardOnboardingService()
        return service.execute_hard_onboarding(agent_id, onboarding_message, role)
    except Exception as e:
        self.logger.error(f"❌ Hard onboarding failed: {e}")
        return False


def hard_onboard_multiple_agents(
    agents: list[tuple[str, str]], role: str | None = None
) -> dict[str, bool]:
    """
    Hard onboard multiple agents sequentially.

    Args:
        agents: List of (agent_id, onboarding_message) tuples
        role: Optional role assignment for all agents

    Returns:
        Dictionary of {agent_id: success_status}
    """
    results = {}
    service = HardOnboardingService()

    for agent_id, onboarding_message in agents:
        logger.info(f"🚨 Processing {agent_id}...")
        success = service.execute_hard_onboarding(
            agent_id, onboarding_message, role)
        results[agent_id] = success

        if success:
            logger.info(f"✅ {agent_id} hard onboarded successfully")
        else:
            logger.error(f"❌ {agent_id} hard onboarding failed")

        # Wait between agents
        time.sleep(2.0)

    return results
