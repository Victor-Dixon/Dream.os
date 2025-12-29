"""
<!-- SSOT Domain: core -->

Overnight Orchestrator - V2 Compliant
=====================================

Main orchestrator for 24/7 autonomous agent operations.
Extends V2's core orchestration with cycle-based scheduling and agent coordination.

V2 Compliance: ≤400 lines, SOLID principles, comprehensive error handling.

Author: Agent-1 - Autonomous Operations Specialist
License: MIT
"""

import asyncio
import time
from typing import Dict, List, Optional, Any
import logging

# V2 Integration imports
try:
    from ...core.orchestration.core_orchestrator import CoreOrchestrator
    from ...core.messaging_pyautogui import send_message_to_agent
    from ...core.config_ssot import get_unified_config
    from ...core.unified_logging_system import get_logger
    from ...workflows import WorkflowEngine
except ImportError as e:
    logging.warning(f"V2 integration imports failed: {e}")
    # Fallback implementations
    class CoreOrchestrator:
        pass
    
    def send_message_to_agent(*args, **kwargs):
        logging.info(f"Mock message send: {args}, {kwargs}")
        return True
    
    def get_unified_config():
        return type('MockConfig', (), {'get_env': lambda x, y=None: y})()
    
    def get_logger(name):
        return logging.getLogger(name)
    
    class WorkflowEngine:
        pass

from .scheduler import TaskScheduler
from .monitor import ProgressMonitor
from .recovery import RecoverySystem

# Website auto-update integration
try:
    from ...services.swarm_website.auto_updater import SwarmWebsiteAutoUpdater
    WEBSITE_UPDATER_AVAILABLE = True
except ImportError:
    WEBSITE_UPDATER_AVAILABLE = False
    SwarmWebsiteAutoUpdater = None

# Self-healing system integration (Agent-3 - 2025-01-27)
try:
    from ...core.agent_self_healing_system import get_self_healing_system, SelfHealingConfig
    SELF_HEALING_AVAILABLE = True
except ImportError:
    SELF_HEALING_AVAILABLE = False

# V1→V2 Extracted Components Integration
try:
    from .message_plans import build_message_plan, format_message, get_available_plans
    from .fsm_bridge import handle_fsm_request, handle_fsm_update, seed_fsm_tasks
    from .listener import OvernightListener
    from .inbox_consumer import process_inbox
    MESSAGE_PLANS_AVAILABLE = True
    FSM_BRIDGE_AVAILABLE = True
    LISTENER_AVAILABLE = True
except ImportError as e:
    logging.warning(f"V1→V2 extracted components not available: {e}")
    MESSAGE_PLANS_AVAILABLE = False
    FSM_BRIDGE_AVAILABLE = False
    LISTENER_AVAILABLE = False


class OvernightOrchestrator(CoreOrchestrator):
    """
    Main orchestrator for overnight autonomous operations.
    
    Extends V2's core orchestration with:
    - 24/7 autonomous execution
    - Cycle-based scheduling (V2 requirement)
    - Agent task distribution
    - Workflow integration
    - Recovery and monitoring
    """

    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize overnight orchestrator.
        
        Args:
            config: Configuration dictionary (uses config/orchestration.yml if None)
        """
        super().__init__()
        
        self.config = config or {}
        self.logger = get_logger(__name__)
        
        # V2 Integration
        self.unified_config = get_unified_config()
        
        # Overnight settings
        overnight_config = self.config.get('overnight', {})
        self.enabled = overnight_config.get('enabled', True)
        self.cycle_interval = overnight_config.get('cycle_interval', 10)  # minutes (V2 cycle-based)
        self.max_cycles = overnight_config.get('max_cycles', 60)  # 10 hours
        self.auto_restart = overnight_config.get('auto_restart', True)
        
        # Initialize components
        self.scheduler = TaskScheduler(self.config)
        self.monitor = ProgressMonitor(self.config)
        self.recovery = RecoverySystem(self.config)
        
        # Initialize website auto-updater if available
        self.website_updater = None
        website_update_enabled = overnight_config.get('website_updates', {}).get('enabled', True)
        if WEBSITE_UPDATER_AVAILABLE and website_update_enabled:
            try:
                self.website_updater = SwarmWebsiteAutoUpdater()
                if self.website_updater.updater.enabled:
                    self.logger.info("✅ Website auto-updater initialized and enabled")
                else:
                    self.logger.info("⚠️ Website auto-updater initialized but not configured (missing env vars)")
                    self.website_updater = None
            except Exception as e:
                self.logger.warning(f"Failed to initialize website updater: {e}")
                self.website_updater = None
        
        # Initialize self-healing system (Agent-3 - 2025-01-27)
        self.self_healing_enabled = overnight_config.get('self_healing', {}).get('enabled', True)
        self.self_healing_system = None
        if SELF_HEALING_AVAILABLE and self.self_healing_enabled:
            healing_config = SelfHealingConfig(
                check_interval_seconds=overnight_config.get('self_healing', {}).get('check_interval', 30),
                stall_threshold_seconds=overnight_config.get('monitoring', {}).get('stall_timeout', 300),
                recovery_attempts_max=overnight_config.get('self_healing', {}).get('max_attempts', 3),
                auto_reset_enabled=overnight_config.get('self_healing', {}).get('auto_reset', True),
            )
            self.self_healing_system = get_self_healing_system(healing_config)
            self.logger.info("✅ Self-healing system integrated into orchestrator")
        
        # State
        self.is_running = False
        self.current_cycle = 0
        self.start_time = 0
        self.active_agents = []
        self.workflow_engine = None
        
        # Integration flags
        self.workflow_integration = overnight_config.get('integration', {}).get('workflow_engine', True)
        self.vision_integration = overnight_config.get('integration', {}).get('vision_system', False)
        self.messaging_integration = overnight_config.get('integration', {}).get('messaging_system', True)
        self.coordinate_integration = overnight_config.get('integration', {}).get('coordinate_system', True)
        
        # V1→V2 Extracted Components Integration
        self.message_plan_strategy = overnight_config.get('message_plan', 'fsm-driven')
        self.use_message_plans = MESSAGE_PLANS_AVAILABLE and overnight_config.get('use_message_plans', True)
        self.use_fsm_bridge = FSM_BRIDGE_AVAILABLE and overnight_config.get('use_fsm_bridge', True)
        self.use_listener = LISTENER_AVAILABLE and overnight_config.get('use_listener', False)
        
        # Initialize message plan if available
        self.message_plan = None
        if self.use_message_plans:
            try:
                self.message_plan = build_message_plan(self.message_plan_strategy)
                self.logger.info(f"Message plan '{self.message_plan_strategy}' loaded: {len(self.message_plan)} steps")
            except Exception as e:
                self.logger.warning(f"Failed to load message plan: {e}")
                self.use_message_plans = False
        
        # Initialize listeners for active agents (if enabled)
        self.listeners = {}
        if self.use_listener:
            self.logger.info("Listener integration enabled")
        
        self.logger.info("Overnight Orchestrator initialized")

    async def start(self) -> None:
        """Start overnight autonomous operations."""
        if not self.enabled:
            self.logger.warning("Overnight operations disabled")
            return
        
        if self.is_running:
            self.logger.warning("Overnight orchestrator already running")
            return
        
        # Start self-healing system daemon (Agent-3 - 2025-01-27)
        if self.self_healing_system:
            self.self_healing_system.start()
            self.logger.info("🚀 Self-healing daemon started (continuous monitoring)")
        
        self.is_running = True
        self.current_cycle = 0
        self.start_time = time.time()
        
        self.logger.info("Starting overnight autonomous operations")
        
        try:
            # Initialize components
            await self._initialize_components()
            
            # Start monitoring
            self.monitor.start_monitoring()
            
            # Main execution loop
            await self._execute_overnight_loop()
            
        except Exception as e:
            self.logger.error(f"Overnight operations failed: {e}")
            raise
        finally:
            self.is_running = False
            self.monitor.stop_monitoring()
            self.logger.info("Overnight operations stopped")

    async def stop(self) -> None:
        """Stop overnight operations gracefully."""
        self.logger.info("Stopping overnight operations")
        self.is_running = False

    async def _initialize_components(self) -> None:
        """Initialize orchestrator components."""
        try:
            # Initialize scheduler
            await self.scheduler.initialize()
            
            # Initialize recovery system
            await self.recovery.initialize()
            
            # Initialize workflow engine if enabled
            if self.workflow_integration:
                self.workflow_engine = WorkflowEngine("overnight_operations")
                self.logger.info("Workflow engine initialized")
            
            # Get active agents
            self.active_agents = await self._get_active_agents()
            self.logger.info(f"Found {len(self.active_agents)} active agents")
            
            # Initialize FSM bridge if enabled
            if self.use_fsm_bridge:
                try:
                    # Seed FSM tasks from TASK_LIST.md files if configured
                    if overnight_config.get('seed_fsm_tasks', False):
                        seeded = seed_fsm_tasks("Agent-5")
                        self.logger.info(f"Seeded {len(seeded)} FSM tasks")
                except Exception as e:
                    self.logger.warning(f"FSM bridge initialization warning: {e}")
            
            # Initialize listeners for active agents
            if self.use_listener:
                for agent_id in self.active_agents:
                    try:
                        listener = OvernightListener(
                            agent_id=agent_id,
                            poll_interval=0.2,
                            devlog_webhook=self.unified_config.get_env("DISCORD_WEBHOOK_URL"),
                            devlog_username=self.unified_config.get_env("DEVLOG_USERNAME", "Agent Devlog")
                        )
                        self.listeners[agent_id] = listener
                    except Exception as e:
                        self.logger.warning(f"Failed to initialize listener for {agent_id}: {e}")
                self.logger.info(f"Initialized {len(self.listeners)} listeners")
            
        except Exception as e:
            self.logger.error(f"Component initialization failed: {e}")
            raise

    async def _execute_overnight_loop(self) -> None:
        """Main overnight execution loop with cycle-based scheduling."""
        self.logger.info(f"Starting overnight loop: {self.max_cycles} cycles, {self.cycle_interval} min intervals")
        
        while self.is_running and self.current_cycle < self.max_cycles:
            try:
                self.current_cycle += 1
                cycle_start_time = time.time()
                
                self.logger.info(f"Starting cycle {self.current_cycle}/{self.max_cycles}")
                
                # Execute cycle
                await self._execute_cycle()
                
                # Update monitoring
                self.monitor.update_cycle(self.current_cycle, cycle_start_time)
                
                # Check for recovery needs
                await self._check_recovery()
                
                # Calculate sleep time for cycle interval
                cycle_duration = time.time() - cycle_start_time
                sleep_time = max(0, (self.cycle_interval * 60) - cycle_duration)
                
                if sleep_time > 0:
                    self.logger.info(f"Cycle {self.current_cycle} completed, sleeping {sleep_time:.1f}s")
                    await asyncio.sleep(sleep_time)
                else:
                    self.logger.warning(f"Cycle {self.current_cycle} took longer than interval")
                
            except Exception as e:
                self.logger.error(f"Cycle {self.current_cycle} failed: {e}")
                
                # Attempt recovery
                if self.auto_restart:
                    await self.recovery.handle_cycle_failure(self.current_cycle, str(e))
                
                # Continue to next cycle
                continue
        
        self.logger.info(f"Overnight loop completed after {self.current_cycle} cycles")

    async def _execute_cycle(self) -> None:
        """Execute a single cycle of autonomous operations."""
        try:
            # Process FSM requests if FSM bridge is enabled
            if self.use_fsm_bridge:
                await self._process_fsm_requests()
            
            # Get tasks for this cycle
            tasks = await self.scheduler.get_cycle_tasks(self.current_cycle)
            
            if not tasks:
                self.logger.info(f"No tasks scheduled for cycle {self.current_cycle}")
                # Still process inboxes if listeners are enabled
                if self.use_listener:
                    await self._process_agent_responses()
                return
            
            self.logger.info(f"Executing {len(tasks)} tasks in cycle {self.current_cycle}")
            
            # Distribute tasks to agents
            for task in tasks:
                await self._distribute_task(task)
            
            # Execute workflow if available
            if self.workflow_engine:
                await self._execute_workflow_cycle()
            
            # Process agent responses if listeners are enabled
            if self.use_listener:
                await self._process_agent_responses()
            
            # Update progress
            self.monitor.update_tasks(tasks)
            
            # Auto-update website with agent status changes
            if self.website_updater:
                try:
                    updated_count = self.website_updater.check_all_agents()
                    if updated_count > 0:
                        self.logger.info(f"📤 Website updated with {updated_count} agent status change(s)")
                except Exception as e:
                    self.logger.warning(f"Website update check failed: {e}")
            
        except Exception as e:
            self.logger.error(f"Cycle execution failed: {e}")
            raise

    async def _distribute_task(self, task: Dict[str, Any]) -> None:
        """Distribute a task to an agent."""
        try:
            agent_id = task.get('agent_id')
            task_type = task.get('type')
            task_data = task.get('data', {})
            
            if not agent_id:
                self.logger.warning("Task missing agent_id, skipping")
                return
            
            # Create task message
            message = self._create_task_message(task_type, task_data, agent_id)
            
            # Send to agent
            if self.messaging_integration:
                success = await asyncio.get_event_loop().run_in_executor(
                    None,
                    send_message_to_agent,
                    agent_id,
                    message
                )
                
                if success:
                    self.logger.info(f"Task distributed to {agent_id}: {task_type}")
                else:
                    self.logger.error(f"Failed to distribute task to {agent_id}")
            
        except Exception as e:
            self.logger.error(f"Task distribution failed: {e}")

    def _create_task_message(self, task_type: str, task_data: Dict[str, Any], agent_id: Optional[str] = None) -> str:
        """Create task message for agent using message plans if available."""
        # Use message plans if available and configured
        if self.use_message_plans and self.message_plan and agent_id:
            try:
                # Map task_type to message plan step
                plan_step_index = self.current_cycle % len(self.message_plan)
                planned_msg = self.message_plan[plan_step_index]
                
                # Format message with agent and cycle info
                message = format_message(
                    planned_msg,
                    agent_id,
                    cycle=self.current_cycle,
                    **task_data
                )
                
                # Add cycle context
                return f"""[OVERNIGHT CYCLE {self.current_cycle}]

{message}

---
Cycle: {self.current_cycle} | Plan: {self.message_plan_strategy} | Step: {planned_msg.tag.value}
"""
            except Exception as e:
                self.logger.warning(f"Failed to use message plan, falling back to default: {e}")
        
        # Fallback to default message format
        return f"""
[OVERNIGHT TASK] Cycle {self.current_cycle}
Type: {task_type}
Data: {task_data}
Timestamp: {time.time()}

Execute this task autonomously. Report completion or issues.
"""

    async def _execute_workflow_cycle(self) -> None:
        """Execute workflow for current cycle."""
        try:
            if not self.workflow_engine:
                return
            
            # Create cycle-specific workflow
            await self._create_cycle_workflow()
            
            # Execute workflow (simplified)
            self.logger.info("Executing cycle workflow")
            
        except Exception as e:
            self.logger.error(f"Workflow execution failed: {e}")

    async def _create_cycle_workflow(self) -> None:
        """Create workflow for current cycle."""
        # This would integrate with the workflow system
        # For now, just log the intention
        self.logger.info(f"Creating workflow for cycle {self.current_cycle}")

    async def _get_active_agents(self) -> List[str]:
        """Get list of active agents (mode-aware)."""
        # Use agent mode manager to get active agents for current mode
        try:
            from src.core.agent_mode_manager import get_active_agents
            active = get_active_agents()
            self.logger.info(f"Mode-aware: Active agents ({len(active)}): {', '.join(active)}")
            return active
        except Exception as e:
            self.logger.warning(f"Failed to load mode-aware agents, using fallback: {e}")
            # Fallback to 4-agent mode
            return ["Agent-1", "Agent-2", "Agent-3", "Agent-4"]

    async def _check_recovery(self) -> None:
        """Check if recovery actions are needed."""
        try:
            # PROACTIVE SELF-HEALING (Agent-3 - 2025-01-27)
            # Run self-healing FIRST - it's more aggressive and handles file-level recovery
            if self.self_healing_system:
                try:
                    stalled_agents = await self.self_healing_system._detect_stalled_agents()
                    if stalled_agents:
                        self.logger.info(f"🔍 Self-healing detected {len(stalled_agents)} stalled agents")
                        for agent_id, stall_duration in stalled_agents:
                            await self.self_healing_system._heal_stalled_agent(agent_id, stall_duration)
                except Exception as e:
                    self.logger.error(f"Self-healing check failed: {e}", exc_info=True)
            
            # STANDARD RECOVERY SYSTEM (existing infrastructure)
            # Check for stalled agents via monitor
            stalled_agents = await self.monitor.get_stalled_agents()
            
            if stalled_agents:
                self.logger.warning(f"Found {len(stalled_agents)} stalled agents (via monitor)")
                await self.recovery.handle_stalled_agents(stalled_agents)
            
            # Check system health
            health_status = await self.monitor.get_health_status()
            
            if not health_status.get('healthy', True):
                self.logger.warning("System health issues detected")
                await self.recovery.handle_health_issues(health_status)
                
        except Exception as e:
            self.logger.error(f"Recovery check failed: {e}", exc_info=True)

    async def _process_fsm_requests(self) -> None:
        """Process FSM requests and assign tasks to agents."""
        if not self.use_fsm_bridge:
            return
        
        try:
            # Create FSM request for active agents
            fsm_request = {
                "from": "Agent-4",  # Captain
                "agents": self.active_agents,
                "workflow": "default",
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")
            }
            
            result = handle_fsm_request(fsm_request)
            if result.get("ok"):
                assigned = result.get("count", 0)
                if assigned > 0:
                    self.logger.info(f"FSM bridge assigned {assigned} tasks to agents")
        except Exception as e:
            self.logger.warning(f"FSM request processing failed: {e}")

    async def _process_agent_responses(self) -> None:
        """Process agent responses from inboxes."""
        if not self.use_listener:
            return
        
        try:
            total_processed = 0
            for agent_id, listener in self.listeners.items():
                try:
                    # Process inbox once per cycle
                    processed = listener.process_inbox()
                    if processed > 0:
                        total_processed += processed
                        self.logger.info(f"Processed {processed} messages from {agent_id} inbox")
                except Exception as e:
                    self.logger.warning(f"Failed to process inbox for {agent_id}: {e}")
            
            if total_processed > 0:
                self.logger.info(f"Total processed {total_processed} agent responses")
        except Exception as e:
            self.logger.warning(f"Agent response processing failed: {e}")

    def get_orchestrator_status(self) -> Dict[str, Any]:
        """Get current orchestrator status."""
        return {
            "enabled": self.enabled,
            "is_running": self.is_running,
            "current_cycle": self.current_cycle,
            "max_cycles": self.max_cycles,
            "cycle_interval": self.cycle_interval,
            "start_time": self.start_time,
            "active_agents": len(self.active_agents),
            "workflow_integration": self.workflow_integration,
            "vision_integration": self.vision_integration,
            "messaging_integration": self.messaging_integration,
            "coordinate_integration": self.coordinate_integration,
            "auto_restart": self.auto_restart,
            "message_plan_strategy": self.message_plan_strategy if self.use_message_plans else None,
            "message_plans_available": MESSAGE_PLANS_AVAILABLE,
            "fsm_bridge_available": FSM_BRIDGE_AVAILABLE,
            "listener_available": LISTENER_AVAILABLE,
            "active_listeners": len(self.listeners),
        }
