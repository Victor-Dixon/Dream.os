"""
Soft Onboarding Service - 6-Step Protocol Implementation
=========================================================

Implements full soft onboarding protocol with PyAutoGUI animations:
1. Click chat input (move to coords, click)
2. Save session (Ctrl+Enter)
3. Send cleanup prompt (passdown message)
4. Open new tab (Ctrl+T)
5. Navigate to onboarding coords (move to onboarding location)
6. Paste onboarding message

V2 Compliance: <400 lines, single responsibility
"""

from src.core.config.timeout_constants import TimeoutConstants
from src.core.base.base_service import BaseService
import logging
import sys
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))


logger = logging.getLogger(__name__)

# Import PyAutoGUI for animations
try:
    import pyautogui
    import pyperclip
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False
    logger.warning(
        "⚠️ PyAutoGUI not available - soft onboarding animations disabled")


class SoftOnboardingService(BaseService):
    """Soft onboarding service with 6-step protocol."""

    def __init__(self):
        """Initialize soft onboarding service."""
        super().__init__("SoftOnboardingService")
        if not PYAUTOGUI_AVAILABLE:
            self.logger.warning(
                "⚠️ PyAutoGUI not available - soft onboarding will use messaging only")
        self.pyautogui = pyautogui if PYAUTOGUI_AVAILABLE else None

    def _load_agent_coordinates(self, agent_id: str) -> tuple[tuple[int, int] | None, tuple[int, int] | None]:
        """Load chat and onboarding coordinates for agent."""
        from ..core.coordinate_loader import get_coordinate_loader

        coord_loader = get_coordinate_loader()
        chat_coords = coord_loader.get_chat_coordinates(agent_id)
        onboarding_coords = coord_loader.get_onboarding_coordinates(agent_id)

        return chat_coords, onboarding_coords

    def step_1_click_chat_input(self, agent_id: str) -> bool:
        """Step 1: Click chat input to get agent's attention."""
        if not PYAUTOGUI_AVAILABLE:
            self.logger.warning("⚠️ PyAutoGUI not available - skipping step 1")
            return True  # Non-blocking

        try:
            chat_coords, _ = self._load_agent_coordinates(agent_id)
            if not chat_coords:
                self.logger.error(f"❌ No chat coordinates for {agent_id}")
                return False

            x, y = chat_coords
            self.logger.info(
                f"👆 Step 1: Clicking chat input for {agent_id} at {chat_coords}")

            # Click chat input - wait for app to respond to interaction
            self.pyautogui.moveTo(x, y, duration=0.5)
            self.pyautogui.click()
            time.sleep(1.0)  # Wait for app to respond to click interaction

            self.logger.info(f"✅ Chat input clicked for {agent_id}")
            return True
        except Exception as e:
            self.logger.error(f"❌ Failed to click chat input: {e}")
            return False

    def step_2_save_session(self) -> bool:
        """Step 2: Save session (Ctrl+Enter)."""
        if not PYAUTOGUI_AVAILABLE:
            self.logger.warning("⚠️ PyAutoGUI not available - skipping step 2")
            return True  # Non-blocking

        try:
            self.logger.info("💾 Step 2: Saving session (Ctrl+Enter)")
            self.pyautogui.hotkey("ctrl", "enter")
            time.sleep(0.8)  # Wait for session save operation
            self.logger.info("✅ Session saved")
            return True
        except Exception as e:
            self.logger.error(f"❌ Failed to save session: {e}")
            return False

    def step_3_send_cleanup_prompt(self, agent_id: str, custom_cleanup_message: str | None = None) -> bool:
        """Step 3: Send cleanup prompt (passdown message)."""
        if not PYAUTOGUI_AVAILABLE:
            self.logger.warning(
                "⚠️ PyAutoGUI not available - using messaging system for step 3")
            return self._send_cleanup_via_messaging(agent_id, custom_cleanup_message)

        try:
            cleanup_message = custom_cleanup_message or self._get_default_cleanup_message()
            self.logger.info(f"📝 Step 3: Sending cleanup prompt to {agent_id}")

            # Clear input first
            self.pyautogui.hotkey("ctrl", "a")
            time.sleep(0.2)
            self.pyautogui.press("delete")
            time.sleep(0.3)

            # Paste and send cleanup message
            pyperclip.copy(cleanup_message)
            self.pyautogui.hotkey("ctrl", "v")
            time.sleep(0.3)
            self.pyautogui.press("enter")
            time.sleep(1.0)

            self.logger.info(f"✅ Cleanup prompt sent to {agent_id}")
            return True
        except Exception as e:
            self.logger.error(f"❌ Failed to send cleanup prompt: {e}")
            return False

    def step_4_open_new_tab(self) -> bool:
        """Step 4: Open new tab (Ctrl+T)."""
        if not PYAUTOGUI_AVAILABLE:
            self.logger.warning("⚠️ PyAutoGUI not available - skipping step 4")
            return True  # Non-blocking

        try:
            self.logger.info("🆕 Step 4: Opening new tab (Ctrl+T)")
            self.pyautogui.hotkey("ctrl", "t")
            time.sleep(2.0)  # Wait for tab to initialize and stabilize
            self.logger.info("✅ New tab opened")
            return True
        except Exception as e:
            self.logger.error(f"❌ Failed to open new tab: {e}")
            return False

    def step_5_navigate_to_onboarding(self, agent_id: str) -> bool:
        """Step 5: Navigate to onboarding coordinates."""
        if not PYAUTOGUI_AVAILABLE:
            self.logger.warning("⚠️ PyAutoGUI not available - skipping step 5")
            return True  # Non-blocking

        try:
            _, onboarding_coords = self._load_agent_coordinates(agent_id)
            if not onboarding_coords:
                self.logger.error(f"❌ No onboarding coordinates for {agent_id}")
                return False

            x, y = onboarding_coords
            self.logger.info(
                f"🎯 Step 5: Navigating to onboarding coords for {agent_id} at {onboarding_coords}")

            # Click onboarding input - wait for app to respond to interaction
            self.pyautogui.moveTo(x, y, duration=0.5)
            self.pyautogui.click()
            time.sleep(1.0)  # Wait for app to respond to click interaction

            self.logger.info(f"✅ Navigated to onboarding input for {agent_id}")
            return True
        except Exception as e:
            self.logger.error(f"❌ Failed to navigate to onboarding: {e}")
            return False

    def step_6_paste_onboarding_message(self, agent_id: str, message: str) -> bool:
        """Step 6: Paste and send onboarding message."""
        if not PYAUTOGUI_AVAILABLE:
            self.logger.warning(
                "⚠️ PyAutoGUI not available - using messaging system for step 6")
            return self._send_onboarding_via_messaging(agent_id, message)

        try:
            self.logger.info(f"📝 Step 6: Pasting onboarding message for {agent_id}")

            # Clear input first
            self.pyautogui.hotkey("ctrl", "a")
            time.sleep(0.2)
            self.pyautogui.press("delete")
            time.sleep(0.3)

            # Paste and send
            pyperclip.copy(message)
            self.pyautogui.hotkey("ctrl", "v")
            time.sleep(0.5)  # Wait for paste to complete
            self.pyautogui.press("enter")
            time.sleep(0.8)  # Wait for message send

            self.logger.info(f"✅ Onboarding message sent to {agent_id}")
            return True
        except Exception as e:
            self.logger.error(f"❌ Failed to paste onboarding message: {e}")
            return False

    def _get_default_cleanup_message(self) -> str:
        """Get default cleanup/passdown message."""
        return """🎯 SESSION CLEANUP REQUIRED!

Before starting your next session, please complete these tasks:

1. Create/Update passdown.json
2. Create Final Devlog
3. Post Devlog to Discord
4. Update Swarm Brain Database
5. Create a Tool You Wished You Had

Press Enter when complete to proceed to next session onboarding!

📝 Remember: Quality documentation ensures civilization-building!
🐝 WE. ARE. SWARM. ⚡"""

    def _send_cleanup_via_messaging(self, agent_id: str, custom_message: str | None) -> bool:
        """Fallback: Send cleanup via messaging system (S2A template, no-ack)."""
        try:
            from ..services.messaging_infrastructure import MessageCoordinator
            from ..core.messaging_models_core import MessageCategory, UnifiedMessageTag
            from ..core.messaging_core import UnifiedMessagePriority, UnifiedMessage, UnifiedMessageType
            from ..core.messaging_templates import render_message

            message = custom_message or self._get_default_cleanup_message()
            msg = UnifiedMessage(
                content=message,
                sender="SYSTEM",
                recipient=agent_id,
                message_type=UnifiedMessageType.SYSTEM_TO_AGENT,
                priority=UnifiedMessagePriority.REGULAR,
                tags=[UnifiedMessageTag.WRAPUP],
                category=MessageCategory.S2A,
            )

            rendered = render_message(
                msg,
                template_key="PASSDOWN",
                context="Passdown/Cleanup",
                actions=message,
                fallback="If blocked, escalate to Captain with blockers and partial status.",
            )

            return MessageCoordinator.send_to_agent(
                agent=agent_id,
                message=rendered,
                priority=UnifiedMessagePriority.REGULAR,
                use_pyautogui=True,
                sender="SYSTEM",
                message_category=MessageCategory.S2A,
            )
        except Exception as e:
            self.logger.error(f"❌ Failed to send cleanup via messaging: {e}")
            return False

    def _send_onboarding_via_messaging(self, agent_id: str, message: str) -> bool:
        """Fallback: Send onboarding via messaging system (S2A template, no-ack)."""
        try:
            from ..services.messaging_infrastructure import MessageCoordinator
            from ..core.messaging_models_core import MessageCategory, UnifiedMessageTag
            from ..core.messaging_core import UnifiedMessagePriority, UnifiedMessage, UnifiedMessageType
            from ..core.messaging_templates import render_message

            msg = UnifiedMessage(
                content=message,
                sender="SYSTEM",
                recipient=agent_id,
                message_type=UnifiedMessageType.ONBOARDING,
                priority=UnifiedMessagePriority.REGULAR,
                tags=[UnifiedMessageTag.ONBOARDING],
                category=MessageCategory.S2A,
            )

            rendered = render_message(
                msg,
                template_key="HARD_ONBOARDING",
                context="Onboarding",
                actions=message,
                fallback="If blocked, escalate to Captain.",
            )

            return MessageCoordinator.send_to_agent(
                agent=agent_id,
                message=rendered,
                priority=UnifiedMessagePriority.REGULAR,
                use_pyautogui=True,
                sender="SYSTEM",
                message_category=MessageCategory.S2A,
            )
        except Exception as e:
            self.logger.error(f"❌ Failed to send onboarding via messaging: {e}")
            return False

    def onboard_agent(self, agent_id: str, message: str, **kwargs) -> bool:
        """
        Execute soft onboarding for an agent (delegates to handler for compatibility).
        """
        try:
            from .handlers.soft_onboarding_handler import SoftOnboardingHandler
            handler = SoftOnboardingHandler()

            class Args:
                def __init__(self, agent_id, message, **kwargs):
                    self.agent = agent_id
                    self.message = message
                    self.onboarding_file = None  # Fix missing attribute error
                    self.__dict__.update(kwargs)

            args = Args(agent_id, message, **kwargs)
            return handler.handle(args)
        except Exception as e:
            self.logger.error(f"Soft onboarding failed: {e}")
            return False

    def execute_soft_onboarding(
        self, agent_id: str, onboarding_message: str, role: str = None, custom_cleanup_message: str = None
    ) -> bool:
        """
        Execute full soft onboarding protocol (6 steps with animations).

        NOTE: Lock handling is done by caller (soft_onboard_agent or soft_onboard_multiple_agents).
        This method should NOT acquire the lock itself to avoid double-locking.
        """
        try:
            self.logger.info(
                f"🚀 Starting 6-step soft onboarding for {agent_id}")

            # Step 1: Click chat input
            if not self.step_1_click_chat_input(agent_id):
                self.logger.error("❌ Step 1 failed: Click chat input")
                return False

            # Step 2: Save session
            if not self.step_2_save_session():
                self.logger.error("❌ Step 2 failed: Save session")
                return False

            # Step 3: Send cleanup prompt
            if not self.step_3_send_cleanup_prompt(agent_id, custom_cleanup_message):
                self.logger.error("❌ Step 3 failed: Send cleanup prompt")
                return False

            # Step 4: Open new tab
            if not self.step_4_open_new_tab():
                self.logger.error("❌ Step 4 failed: Open new tab")
                return False

            # Step 5: Navigate to onboarding
            if not self.step_5_navigate_to_onboarding(agent_id):
                self.logger.error("❌ Step 5 failed: Navigate to onboarding")
                return False

            # Step 6: Paste onboarding message
            if not self.step_6_paste_onboarding_message(agent_id, onboarding_message):
                self.logger.error("❌ Step 6 failed: Paste onboarding message")
                return False

            self.logger.info(f"🎉 Soft onboarding complete for {agent_id}!")
            return True
        except Exception as e:
            self.logger.error(f"Soft onboarding execution failed: {e}")
            return False


def soft_onboard_agent(agent_id: str, message: str, **kwargs) -> bool:
    """
    Convenience function for soft onboarding.

    CRITICAL: Wrapped in keyboard_control to block other sends during operation.
    All 6 steps must complete before allowing new sends.

    NESTED LOCK FIX: Checks if lock is already held (e.g., by soft_onboard_multiple_agents)
    to prevent deadlock when called from within another keyboard_control context.

    Args:
        agent_id: Target agent ID
        message: Onboarding message
        **kwargs: Additional options

    Returns:
        True if successful
    """
    from ..core.keyboard_control_lock import keyboard_control, is_locked

    service = SoftOnboardingService()

    # CRITICAL: Check if keyboard lock is already held (e.g., by soft_onboard_multiple_agents)
    # If lock is already held, skip acquiring it again to prevent deadlock
    lock_already_held = is_locked()

    if lock_already_held:
        logger.debug(
            f"🔒 Keyboard lock already held, skipping lock acquisition for {agent_id}")
        # Execute onboarding without acquiring lock (caller already has it)
        return service.execute_soft_onboarding(agent_id, message, **kwargs)
    else:
        # CRITICAL: Wrap ENTIRE operation in keyboard lock
        # This blocks ALL other sends until all 6 steps complete
        with keyboard_control(f"soft_onboard_{agent_id}"):
            return service.execute_soft_onboarding(agent_id, message, **kwargs)


def soft_onboard_multiple_agents(
    agents: list[tuple[str, str]], role: str = None, generate_cycle_report: bool = True
) -> dict[str, bool]:
    """
    Soft onboard multiple agents sequentially.

    CRITICAL: Wrapped in keyboard_control to block other sends during entire operation.
    All 8 agents must complete before allowing new sends.

    Args:
        agents: List of (agent_id, onboarding_message) tuples
        role: Optional role assignment for all agents
        generate_cycle_report: Whether to generate cycle accomplishments report after onboarding

    Returns:
        Dictionary of {agent_id: success_status}
    """
    from ..core.keyboard_control_lock import keyboard_control

    results = {}

    # CRITICAL: Wrap ENTIRE operation in keyboard lock
    # This blocks ALL other sends until all 8 agents are onboarded
    with keyboard_control("soft_onboard_multiple"):
        for agent_id, onboarding_message in agents:
            logger.info(f"🚀 Processing {agent_id}...")
            success = soft_onboard_agent(
                agent_id, onboarding_message, role=role)
            results[agent_id] = success

            if success:
                logger.info(f"✅ {agent_id} soft onboarded successfully")
            else:
                logger.error(f"❌ {agent_id} soft onboarding failed")

            # Small delay between agents for stability
            import time
            time.sleep(2.0)  # Wait between agents

        # Generate cycle accomplishments report after onboarding all agents
        if generate_cycle_report:
            try:
                logger.info("📊 Generating cycle accomplishments report...")
                from pathlib import Path
                import subprocess
                import sys

                report_script = Path(__file__).parent.parent.parent / \
                    "tools" / "generate_cycle_accomplishments_report.py"
                if report_script.exists():
                    result = subprocess.run(
                        [sys.executable, str(report_script)],
                        capture_output=True,
                        text=True,
                        timeout=TimeoutConstants.HTTP_DEFAULT
                    )
                    if result.returncode == 0:
                        logger.info("✅ Cycle accomplishments report generated")
                        # Extract report path from output if available
                        for line in result.stdout.split('\n'):
                            if 'Report generated:' in line:
                                logger.info(f"   {line.strip()}")
                    else:
                        logger.warning(
                            f"⚠️  Cycle report generation failed: {result.stderr[:200]}")
                else:
                    logger.warning(
                        f"⚠️  Cycle report script not found: {report_script}")
            except Exception as e:
                logger.warning(f"⚠️  Failed to generate cycle report: {e}")

    return results


def generate_cycle_accomplishments_report(cycle_id: str | None = None) -> Path | None:
    """
    Generate cycle accomplishments report from all agent status.json files.

    Convenience function that can be called programmatically.

    Args:
        cycle_id: Optional cycle identifier (e.g., "C-XXX")

    Returns:
        Path to generated report file, or None if generation failed
    """
    try:
        from pathlib import Path
        import subprocess
        import sys

        report_script = Path(__file__).parent.parent.parent / \
            "tools" / "generate_cycle_accomplishments_report.py"
        if not report_script.exists():
            logger.warning(
                f"⚠️  Cycle report script not found: {report_script}")
            return None

        logger.info("📊 Generating cycle accomplishments report...")
        result = subprocess.run(
            [sys.executable, str(report_script)] +
            (["--cycle", cycle_id] if cycle_id else []),
            capture_output=True,
            text=True,
            timeout=TimeoutConstants.HTTP_DEFAULT
        )

        if result.returncode == 0:
            logger.info("✅ Cycle accomplishments report generated")
            # Try to extract report path from output
            for line in result.stdout.split('\n'):
                if 'Report generated:' in line:
                    report_path_str = line.split(
                        'Report generated:')[1].strip()
                    return Path(report_path_str)
            # If path not found in output, return default location
            return Path("docs/archive/cycles")
        else:
            logger.warning(
                f"⚠️  Cycle report generation failed: {result.stderr[:200]}")
            return None
    except Exception as e:
        logger.warning(f"⚠️  Failed to generate cycle report: {e}")
        return None
