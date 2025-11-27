"""
Soft Onboarding Service - Wrapper for Unified Onboarding
=========================================================

Provides backward compatibility and simplified interface.
Delegates to handlers and unified onboarding service.

V2 Compliance: Wrapper pattern, <400 lines
"""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class SoftOnboardingService:
    """Soft onboarding service - delegates to handler."""

    def __init__(self):
        """Initialize soft onboarding service."""
        # LAZY IMPORT FIX: Don't import handler in __init__ to avoid circular import
        # Handler will be imported when needed in methods
        self._handler = None
        logger.info("SoftOnboardingService initialized")
    
    @property
    def handler(self):
        """Lazy-load handler to avoid circular import."""
        if self._handler is None:
            from .handlers.soft_onboarding_handler import SoftOnboardingHandler
            self._handler = SoftOnboardingHandler()
        return self._handler

    def onboard_agent(self, agent_id: str, message: str, **kwargs) -> bool:
        """
        Execute soft onboarding for an agent.

        Args:
            agent_id: Target agent ID
            message: Onboarding message
            **kwargs: Additional options

        Returns:
            True if successful
        """
        try:
            # Delegate to handler
            class Args:
                def __init__(self, agent_id, message, **kwargs):
                    self.agent = agent_id
                    self.message = message
                    self.__dict__.update(kwargs)

            args = Args(agent_id, message, **kwargs)
            return self.handler.handle(args)
        except Exception as e:
            logger.error(f"Soft onboarding failed: {e}")
            return False

    def execute_soft_onboarding(
        self, agent_id: str, onboarding_message: str, role: str = None, custom_cleanup_message: str = None
    ) -> bool:
        """
        Execute full soft onboarding protocol (3 steps).
        
        CRITICAL: Wrapped in keyboard_control to block other sends during operation.
        """
        from ..core.keyboard_control_lock import keyboard_control
        
        with keyboard_control(f"soft_onboard_{agent_id}"):
            try:
                from .handlers.soft_onboarding_handler import SoftOnboardingHandler
                handler = SoftOnboardingHandler()
                
                class Args:
                    def __init__(self):
                        self.agent = agent_id
                        self.message = onboarding_message
                        self.role = role
                        self.cleanup_message = custom_cleanup_message
                
                args = Args()
                return handler.handle(args)
            except Exception as e:
                logger.error(f"Soft onboarding execution failed: {e}")
                return False


def soft_onboard_agent(agent_id: str, message: str, **kwargs) -> bool:
    """
    Convenience function for soft onboarding.
    
    CRITICAL: Wrapped in keyboard_control to block other sends during operation.
    All 3 steps (cleanup, new chat, onboarding) must complete before allowing new sends.
    
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
        logger.debug(f"🔒 Keyboard lock already held, skipping lock acquisition for {agent_id}")
        # Execute onboarding without acquiring lock (caller already has it)
        return service.onboard_agent(agent_id, message, **kwargs)
    else:
        # CRITICAL: Wrap ENTIRE operation in keyboard lock
        # This blocks ALL other sends until all 3 steps complete
        with keyboard_control(f"soft_onboard_{agent_id}"):
            return service.onboard_agent(agent_id, message, **kwargs)


def soft_onboard_multiple_agents(
    agents: list[tuple[str, str]], role: str = None, generate_cycle_report: bool = True
) -> dict[str, bool]:
    """
    Soft onboard multiple agents sequentially.
    
    CRITICAL: Wrapped in keyboard_control to block other sends during entire operation.
    All 8 messages must complete before allowing new sends.

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
            success = soft_onboard_agent(agent_id, onboarding_message, role=role)
            results[agent_id] = success

            if success:
                logger.info(f"✅ {agent_id} soft onboarded successfully")
            else:
                logger.error(f"❌ {agent_id} soft onboarding failed")

            # Small delay between agents for stability
            import time
            time.sleep(1.0)
        
        # Generate cycle accomplishments report after onboarding all agents
        if generate_cycle_report:
            try:
                logger.info("📊 Generating cycle accomplishments report...")
                from pathlib import Path
                import subprocess
                import sys
                
                report_script = Path(__file__).parent.parent.parent / "tools" / "generate_cycle_accomplishments_report.py"
                if report_script.exists():
                    result = subprocess.run(
                        [sys.executable, str(report_script)],
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    if result.returncode == 0:
                        logger.info("✅ Cycle accomplishments report generated")
                        # Extract report path from output if available
                        for line in result.stdout.split('\n'):
                            if 'Report generated:' in line:
                                logger.info(f"   {line.strip()}")
                    else:
                        logger.warning(f"⚠️  Cycle report generation failed: {result.stderr[:200]}")
                else:
                    logger.warning(f"⚠️  Cycle report script not found: {report_script}")
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
        
        report_script = Path(__file__).parent.parent.parent / "tools" / "generate_cycle_accomplishments_report.py"
        if not report_script.exists():
            logger.warning(f"⚠️  Cycle report script not found: {report_script}")
            return None
        
        logger.info("📊 Generating cycle accomplishments report...")
        result = subprocess.run(
            [sys.executable, str(report_script)] + (["--cycle", cycle_id] if cycle_id else []),
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            logger.info("✅ Cycle accomplishments report generated")
            # Try to extract report path from output
            for line in result.stdout.split('\n'):
                if 'Report generated:' in line:
                    report_path_str = line.split('Report generated:')[1].strip()
                    return Path(report_path_str)
            # If path not found in output, return default location
            return Path("docs/cycles")
        else:
            logger.warning(f"⚠️  Cycle report generation failed: {result.stderr[:200]}")
            return None
    except Exception as e:
        logger.warning(f"⚠️  Failed to generate cycle report: {e}")
        return None
