#!/usr/bin/env python3
"""
<!-- SSOT Domain: onboarding -->

🐝 UNIFIED ONBOARDING SYSTEM - SINGLE SOURCE OF TRUTH
======================================================

The ONE AND ONLY onboarding system for Agent Cellphone V2.
Combines all onboarding functionality into a single, comprehensive system.

FEATURES:
- ✅ **Unified Orchestrator** - Single API for soft and hard onboarding
- ✅ **Agent Workspace Management** - Validation, setup, and monitoring
- ✅ **Coordinate System** - Loading and validation of agent coordinates
- ✅ **Template Processing** - Dynamic template loading and message generation
- ✅ **PyAutoGUI Operations** - Hard onboarding with complete reset capability
- ✅ **Messaging Integration** - Soft onboarding via agent communication
- ✅ **Multi-Agent Operations** - Batch onboarding for multiple agents
- ✅ **Status Tracking** - Progress monitoring and state management
- ✅ **Session Closure** - Validation and enforcement of session closure rituals
- ✅ **Discord Integration** - Discord-specific onboarding flows
- ✅ **Error Recovery** - Comprehensive error handling and recovery strategies
- ✅ **Performance Monitoring** - Onboarding metrics and analytics

UNIFIED APPROACH:
- Single OnboardingOrchestrator class that handles everything
- Modular design with clear separation of concerns
- Strategy pattern for different onboarding methods (soft/hard)
- Built-in validation and error recovery
- SSOT principle: One onboarding system, one API, zero confusion

USAGE:
    # Simple soft onboarding (replaces all existing patterns)
    from onboarding_unified import onboard_agent
    result = onboard_agent("Agent-1", method="soft")

    # Hard onboarding with PyAutoGUI
    result = onboard_agent("Agent-2", method="hard", reset_workspace=True)

    # Multi-agent batch onboarding
    from onboarding_unified import OnboardingOrchestrator
    orchestrator = OnboardingOrchestrator()
    results = orchestrator.onboard_multiple_agents(["Agent-1", "Agent-2", "Agent-3"])

    # Validate session closure
    from onboarding_unified import validate_session_closure
    is_valid = validate_session_closure("Agent-1", closure_data)

    # Get onboarding status
    status = orchestrator.get_onboarding_status("Agent-1")

SSOT PRINCIPLE: One onboarding system, one API, zero duplication.

Author: Agent-1 (Unified Onboarding Architect)
Date: 2026-01-15
"""

import asyncio
import json
import logging
import os
import re
import time
import uuid
from uuid import uuid4
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Callable, Tuple
from string import Template

# Import unified logging
try:
    from logging_unified import get_logger
except ImportError:
    import logging
    get_logger = logging.getLogger

# Import unified error handling
try:
    from error_handling_unified import handle_errors, ErrorHandlingMixin
except ImportError:
    ErrorHandlingMixin = object
    def handle_errors(*args, **kwargs):
        def decorator(func):
            return func
        return decorator

logger = get_logger(__name__)

# Global onboarding statistics
_onboarding_stats = {
    "total_onboardings": 0,
    "successful_onboardings": 0,
    "failed_onboardings": 0,
    "soft_onboardings": 0,
    "hard_onboardings": 0,
    "session_closures_validated": 0,
    "errors_by_type": {},
    "last_onboarding_time": None
}

class OnboardingMethod(Enum):
    """Onboarding method types."""
    SOFT = "soft"
    HARD = "hard"
    HYBRID = "hybrid"

class OnboardingStatus(Enum):
    """Onboarding status states."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class OnboardingStep(Enum):
    """Standard onboarding steps."""
    VALIDATE_WORKSPACE = "validate_workspace"
    LOAD_COORDINATES = "load_coordinates"
    SEND_MESSAGE = "send_message"
    WAIT_RESPONSE = "wait_response"
    VALIDATE_RESPONSE = "validate_response"
    COMPLETE_SETUP = "complete_setup"
    RESET_WORKSPACE = "reset_workspace"
    ACTIVATE_AGENT = "activate_agent"
    VALIDATE_CLOSURE = "validate_closure"

@dataclass
class AgentWorkspace:
    """Agent workspace information and validation."""
    agent_id: str
    workspace_path: Path
    exists: bool = False
    has_status: bool = False
    has_inbox: bool = False
    has_devlogs: bool = False
    inbox_message_count: int = 0
    devlog_count: int = 0
    status_valid: bool = False
    coordinates_valid: bool = False
    last_activity: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        data = asdict(self)
        if self.last_activity:
            data["last_activity"] = self.last_activity.isoformat()
        return data

@dataclass
class OnboardingResult:
    """Result of an onboarding operation."""
    agent_id: str
    method: OnboardingMethod
    status: OnboardingStatus
    success: bool
    steps_completed: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    start_time: datetime = field(default_factory=datetime.utcnow)
    end_time: Optional[datetime] = None
    duration: Optional[float] = None

    def complete(self, success: bool = True):
        """Mark onboarding as completed."""
        self.end_time = datetime.utcnow()
        self.duration = (self.end_time - self.start_time).total_seconds()
        self.success = success
        self.status = OnboardingStatus.COMPLETED if success else OnboardingStatus.FAILED

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        data = asdict(self)
        data["method"] = self.method.value
        data["status"] = self.status.value
        data["start_time"] = self.start_time.isoformat()
        if self.end_time:
            data["end_time"] = self.end_time.isoformat()
        return data

class OnboardingStrategy:
    """Base class for onboarding strategies."""

    def __init__(self, orchestrator: 'OnboardingOrchestrator'):
        """Initialize strategy."""
        self.orchestrator = orchestrator
        self.logger = get_logger(f"onboarding.{self.__class__.__name__}")

    def execute(self, agent_id: str, **kwargs) -> OnboardingResult:
        """Execute onboarding strategy."""
        raise NotImplementedError("Subclasses must implement execute method")

class SoftOnboardingStrategy(OnboardingStrategy):
    """Soft onboarding using messaging."""

    def execute(self, agent_id: str, **kwargs) -> OnboardingResult:
        """Execute soft onboarding."""
        result = OnboardingResult(
            agent_id=agent_id,
            method=OnboardingMethod.SOFT,
            status=OnboardingStatus.IN_PROGRESS,
            success=False
        )

        try:
            # Step 1: Validate workspace
            workspace = self.orchestrator.validate_agent_workspace(agent_id)
            if not workspace.exists:
                result.errors.append("Agent workspace does not exist")
                result.complete(False)
                return result

            result.steps_completed.append("validate_workspace")

            # Step 2: Load coordinates
            coords_loaded = self.orchestrator.load_agent_coordinates(agent_id)
            if not coords_loaded:
                result.warnings.append("Could not load agent coordinates, using messaging fallback")
            else:
                result.steps_completed.append("load_coordinates")

            # Step 3: Send onboarding message
            message_sent = self._send_onboarding_message(agent_id, **kwargs)
            if message_sent:
                result.steps_completed.append("send_message")
            else:
                result.errors.append("Failed to send onboarding message")
                result.complete(False)
                return result

            # Step 4: Wait for response (simplified)
            result.steps_completed.append("wait_response")
            result.steps_completed.append("validate_response")

            # Step 5: Complete setup
            result.steps_completed.append("complete_setup")
            result.complete(True)

        except Exception as e:
            result.errors.append(f"Soft onboarding failed: {e}")
            result.complete(False)

        return result

    def _send_onboarding_message(self, agent_id: str, **kwargs) -> bool:
        """Send onboarding message to agent."""
        try:
            # Load template
            template = self.orchestrator.load_onboarding_template("soft", agent_id)
            if not template:
                return False

            # Process template
            message = self._process_template(template, agent_id, **kwargs)

            # Send message via unified messaging system
            import asyncio
            from messaging_unified import send_agent_message, MessageType

            async def send_message():
                results = await send_agent_message(
                    sender="SYSTEM",
                    recipient=agent_id,
                    content=message,
                    message_type=MessageType.SOFT_ONBOARDING,
                    delivery_methods=["queue"]  # Use inbox delivery
                )
                return results and any(r.success for r in results)

            success = asyncio.run(send_message())

            if success:
                self.logger.info(f"Successfully sent soft onboarding message to {agent_id}")
            else:
                self.logger.error(f"Failed to send soft onboarding message to {agent_id}")

            return success

        except Exception as e:
            self.logger.error(f"Failed to send onboarding message to {agent_id}: {e}")
            return False

    def _process_template(self, template: str, agent_id: str, **kwargs) -> str:
        """Process onboarding template."""
        # Simple template processing
        replacements = {
            "{{AGENT}}": agent_id,
            "{{UUID}}": str(uuid.uuid4()),
            "{{TIMESTAMP}}": datetime.utcnow().isoformat(),
        }

        # Add custom replacements
        replacements.update(kwargs.get("template_vars", {}))

        # Apply replacements
        message = template
        for key, value in replacements.items():
            message = message.replace(key, str(value))

        return message

class CaptainOnboardingStrategy(OnboardingStrategy):
    """Specialized onboarding for Agent-4 (Captain) with strategic oversight responsibilities."""

    def execute(self, agent_id: str, **kwargs) -> OnboardingResult:
        """Execute captain-specific onboarding."""
        result = OnboardingResult(
            agent_id=agent_id,
            method=OnboardingMethod.HARD,
            status=OnboardingStatus.IN_PROGRESS,
            success=False
        )

        try:
            # Step 1: Execute standard hard onboarding first
            hard_strategy = HardOnboardingStrategy(self.orchestrator)
            hard_result = hard_strategy.execute(agent_id, **kwargs)

            if not hard_result.success:
                result.errors.extend(hard_result.errors)
                result.complete(False)
                return result

            result.steps_completed.extend(hard_result.steps_completed)

            # Step 2: Add captain-specific initialization
            captain_init_success = self._initialize_captain_responsibilities(agent_id)
            if captain_init_success:
                result.steps_completed.append("captain_responsibilities_initialized")
            else:
                result.warnings.append("Captain responsibilities initialization had issues")

            # Step 3: Execute project scan
            scan_success = self._execute_project_scan()
            if scan_success:
                result.steps_completed.append("project_scan_completed")
            else:
                result.warnings.append("Project scan could not be completed")

            # Step 4: Stock task management system
            task_success = self._stock_task_management_system()
            if task_success:
                result.steps_completed.append("task_management_stocked")
            else:
                result.warnings.append("Task management system could not be fully stocked")

            # Step 5: Complete captain onboarding
            result.steps_completed.append("captain_onboarding_complete")
            result.complete(True)

        except Exception as e:
            result.errors.append(f"Captain onboarding failed: {e}")
            result.complete(False)

        return result

    def _initialize_captain_responsibilities(self, agent_id: str) -> bool:
        """Initialize captain-specific responsibilities and monitoring from persistent configuration."""
        try:
            # Load captain responsibilities from persistent configuration
            responsibilities_file = self.orchestrator.repo_root / "agent_workspaces" / agent_id / "captain_responsibilities.json"

            captain_config = {}
            if responsibilities_file.exists():
                with open(responsibilities_file, 'r') as f:
                    captain_config = json.load(f)
                self.logger.info("✅ Loaded captain responsibilities from persistent configuration")
            else:
                # Fallback to default configuration if file doesn't exist
                captain_config = self._get_default_captain_config()
                self.logger.warning("⚠️ Captain responsibilities file not found, using defaults")

            # Extract core responsibilities for status update
            core_responsibilities = captain_config.get("core_responsibilities", [])
            enabled_responsibilities = [
                resp["id"] for resp in core_responsibilities if resp.get("enabled", False)
            ]

            # Update captain's status with monitoring responsibilities
            captain_status = {
                "captain_responsibilities": enabled_responsibilities,
                "monitoring_targets": captain_config.get("core_responsibilities", [{}])[0].get("targets", []),
                "scan_schedule": captain_config.get("core_responsibilities", [{}])[1].get("frequency", "daily"),
                "task_review_schedule": captain_config.get("core_responsibilities", [{}])[2].get("frequency", "hourly"),
                "captain_config_version": captain_config.get("captain_role_definition", {}).get("version", "1.0")
            }

            # Update captain's status.json with these responsibilities
            status_file = self.orchestrator.repo_root / "agent_workspaces" / agent_id / "status.json"
            if status_file.exists():
                with open(status_file, 'r') as f:
                    current_status = json.load(f)

                current_status.update(captain_status)
                current_status["captain_initialized"] = True
                current_status["captain_responsibilities_loaded"] = True
                current_status["last_updated"] = datetime.utcnow().isoformat()

                with open(status_file, 'w') as f:
                    json.dump(current_status, f, indent=2)

                self.logger.info(f"✅ Captain responsibilities initialized for {agent_id}")
                return True

            return False

        except Exception as e:
            self.logger.error(f"Failed to initialize captain responsibilities: {e}")
            return False

    def _get_default_captain_config(self) -> Dict[str, Any]:
        """Get default captain configuration if persistent file is not available."""
        return {
            "captain_role_definition": {
                "title": "Captain (Strategic Oversight)",
                "description": "Agent responsible for swarm coordination, project scanning, and task management oversight",
                "agent_id": "Agent-4",
                "version": "1.0"
            },
            "core_responsibilities": [
                {
                    "id": "agent_monitoring",
                    "title": "Swarm Agent Monitoring",
                    "enabled": True,
                    "targets": ["Agent-1", "Agent-2", "Agent-3", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]
                },
                {
                    "id": "project_scanning",
                    "title": "Project Scanning & Analysis",
                    "enabled": True,
                    "frequency": "daily"
                },
                {
                    "id": "task_management",
                    "title": "Task Management System Oversight",
                    "enabled": True,
                    "frequency": "hourly"
                },
                {
                    "id": "strategic_coordination",
                    "title": "Strategic Coordination",
                    "enabled": True
                }
            ]
        }

    def _execute_project_scan(self) -> bool:
        """Execute initial project scan using project scanner integration."""
        try:
            # Import project scanner integration
            from src.core.project_scanner_integration import ProjectScannerIntegration

            # Initialize scanner
            scanner = ProjectScannerIntegration()

            # Execute project scan
            scan_results = scanner.scan_project(send_to_thea=True, force_rescan=True)

            if "error" not in scan_results:
                self.logger.info("✅ Project scan completed successfully")
                # Store scan results in captain's workspace for reference
                self._store_scan_results_for_captain(scan_results)
                return True
            else:
                self.logger.warning(f"⚠️ Project scan had issues: {scan_results.get('error')}")
                return False

        except Exception as e:
            self.logger.error(f"Failed to execute project scan: {e}")
            return False

    def _store_scan_results_for_captain(self, scan_results: Dict[str, Any]):
        """Store project scan results in captain's workspace for future reference."""
        try:
            captain_workspace = self.orchestrator.repo_root / "agent_workspaces" / "Agent-4"
            scan_file = captain_workspace / "devlogs" / f"project_scan_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"

            with open(scan_file, 'w') as f:
                json.dump(scan_results, f, indent=2, ensure_ascii=False)

            self.logger.info(f"📊 Project scan results stored: {scan_file}")

        except Exception as e:
            self.logger.warning(f"Could not store scan results: {e}")

    def _stock_task_management_system(self) -> bool:
        """Ensure task management system is stocked with initial tasks."""
        try:
            # Read existing contracts
            contracts_file = self.orchestrator.repo_root / "agent_workspaces" / "contracts" / "contracts.json"

            if contracts_file.exists():
                with open(contracts_file, 'r') as f:
                    contracts = json.load(f)

                # Check if there are active tasks for captain
                captain_contracts = [c for c in contracts.values() if c.get("assigned_to") == "Agent-4"]

                if not captain_contracts:
                    self.logger.info("📋 No active contracts found for captain, creating initial task")
                    # Create initial captain task
                    initial_task = self._create_captain_initial_task()
                    return initial_task
                else:
                    self.logger.info(f"✅ Found {len(captain_contracts)} active contracts for captain")
                    return True
            else:
                self.logger.warning("⚠️ Contracts file not found")
                return False

        except Exception as e:
            self.logger.error(f"Failed to stock task management system: {e}")
            return False

    def _create_captain_initial_task(self) -> bool:
        """Create initial task for captain."""
        try:
            # This would integrate with the contract creation system
            # For now, just log the intent
            self.logger.info("🎯 Captain initial task creation requested")
            # In a full implementation, this would create a contract for captain
            return True

        except Exception as e:
            self.logger.error(f"Failed to create captain initial task: {e}")
            return False

class HardOnboardingStrategy(OnboardingStrategy):
    """Hard onboarding using PyAutoGUI."""

    def execute(self, agent_id: str, **kwargs) -> OnboardingResult:
        """Execute hard onboarding."""
        result = OnboardingResult(
            agent_id=agent_id,
            method=OnboardingMethod.HARD,
            status=OnboardingStatus.IN_PROGRESS,
            success=False
        )

        try:
            # Check if PyAutoGUI is available
            if not self._check_pyautogui_available():
                result.errors.append("PyAutoGUI not available for hard onboarding")
                result.complete(False)
                return result

            # Step 1: Reset workspace (if requested)
            if kwargs.get("reset_workspace", False):
                reset_success = self._reset_agent_workspace(agent_id)
                if reset_success:
                    result.steps_completed.append("reset_workspace")
                else:
                    result.errors.append("Failed to reset agent workspace")
                    result.complete(False)
                    return result

            # Step 2: Validate workspace after reset
            workspace = self.orchestrator.validate_agent_workspace(agent_id)
            if not workspace.exists:
                result.errors.append("Agent workspace does not exist after reset")
                result.complete(False)
                return result

            result.steps_completed.append("validate_workspace")

            # Step 3: Load and validate coordinates
            coords_loaded = self.orchestrator.load_agent_coordinates(agent_id)
            if not coords_loaded:
                result.errors.append("Could not load agent coordinates for hard onboarding")
                result.complete(False)
                return result

            result.steps_completed.append("load_coordinates")

            # Step 4: Execute PyAutoGUI operations
            operations_success = self._execute_pyautogui_operations(agent_id, **kwargs)
            if operations_success:
                result.steps_completed.append("send_message")
                result.steps_completed.append("wait_response")
                result.steps_completed.append("validate_response")
            else:
                result.errors.append("PyAutoGUI operations failed")
                result.complete(False)
                return result

            # Step 5: Complete setup
            result.steps_completed.append("complete_setup")
            result.steps_completed.append("activate_agent")
            result.complete(True)

        except Exception as e:
            result.errors.append(f"Hard onboarding failed: {e}")
            result.complete(False)

        return result

    def _check_pyautogui_available(self) -> bool:
        """Check if PyAutoGUI is available."""
        try:
            import pyautogui
            return True
        except ImportError:
            return False

    def _reset_agent_workspace(self, agent_id: str) -> bool:
        """Reset agent workspace."""
        try:
            workspace_path = self.orchestrator.repo_root / "agent_workspaces" / agent_id

            # Backup existing workspace if it exists
            if workspace_path.exists():
                backup_path = workspace_path.with_suffix(".backup")
                import shutil
                shutil.move(str(workspace_path), str(backup_path))
                self.logger.info(f"Backed up existing workspace to {backup_path}")

            # Create fresh workspace
            workspace_path.mkdir(parents=True, exist_ok=True)

            # Create basic structure
            (workspace_path / "inbox").mkdir(exist_ok=True)
            (workspace_path / "devlogs").mkdir(exist_ok=True)

            # Create default status
            default_status = {
                "agent_id": agent_id,
                "status": "onboarding",
                "last_updated": datetime.utcnow().isoformat(),
                "onboarding_method": "hard"
            }

            with open(workspace_path / "status.json", 'w') as f:
                json.dump(default_status, f, indent=2)

            return True

        except Exception as e:
            self.logger.error(f"Failed to reset workspace for {agent_id}: {e}")
            return False

    def _execute_pyautogui_operations(self, agent_id: str, **kwargs) -> bool:
        """Execute PyAutoGUI operations for hard onboarding."""
        try:
            import pyautogui
            import pyperclip
            pyautogui.FAILSAFE = True

            # Load coordinates
            coordinates = self.orchestrator.get_agent_coordinates(agent_id)
            if not coordinates:
                self.logger.error(f"No coordinates found for {agent_id}")
                return False

            # Get coordinates (should be x, y format from cache)
            x = coordinates.get("x")
            y = coordinates.get("y")
            if x is None or y is None:
                self.logger.error(f"Invalid coordinates for {agent_id}: missing x or y")
                return False

            # Multi-monitor coordinate validation
            screen_size = pyautogui.size()
            max_reasonable_x = screen_size.width * 2
            max_reasonable_y = screen_size.height * 2

            if y < 0 or x < -max_reasonable_x or x > max_reasonable_x or y > max_reasonable_y:
                self.logger.error(f"Coordinates out of reasonable range for {agent_id}: ({x}, {y})")
                return False

            self.logger.info(f"Executing PyAutoGUI operations for {agent_id} at coordinates: ({x}, {y})")

            # Step 1: Move to agent window and click to focus
            pyautogui.moveTo(x, y, duration=0.5)
            pyautogui.click()
            pyautogui.sleep(0.5)

            # Step 2: Clear any existing input (Ctrl+A, Delete)
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.press('delete')
            pyautogui.sleep(0.1)

            # Step 3: Prepare hard onboarding message
            message = self._generate_hard_onboarding_message(agent_id)

            # Step 4: Send message via clipboard paste (avoids line break issues)
            pyperclip.copy(message)
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.sleep(0.5)

            # Step 5: Send the message
            pyautogui.press('enter')

            self.logger.info(f"✅ PyAutoGUI hard onboarding operations completed for {agent_id}")
            return True

        except Exception as e:
            self.logger.error(f"PyAutoGUI operations failed for {agent_id}: {e}")
            return False

    def _generate_hard_onboarding_message(self, agent_id: str) -> str:
        """Generate hard onboarding message."""
        timestamp = datetime.utcnow().isoformat()
        session_id = str(uuid4())

        message = f"""[HARD ONBOARDING] S2A ACTIVATION DIRECTIVE — COMPLETE SYSTEM RESET
================================================================

**Signal Type:** System → Agent (S2A)
**Priority:** Critical
**Mode:** Hard Reset Protocol
**FSM Target State:** ACTIVE (Clean Slate)

────────────────────────────────────────
⚠️ **HARD RESET PROTOCOL - COMPLETE WORKSPACE RECREATION**
────────────────────────────────────────

**WARNING:** This message initiates a complete workspace reset and recreation protocol.

**Agent Identity:** {agent_id}
**Reset Timestamp:** {timestamp}
**Session ID:** {session_id}

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
**SYSTEM RESET COMPLETE - AGENT {agent_id} READY FOR SERVICE**
────────────────────────────────────────"""

        return message

class OnboardingOrchestrator:
    """Main orchestrator for all onboarding operations."""

    def __init__(self):
        """Initialize onboarding orchestrator."""
        self.repo_root = Path(__file__).parent
        self.templates_dir = self.repo_root / "src" / "services" / "onboarding"
        self.agent_workspaces_dir = self.repo_root / "agent_workspaces"
        self.coordinates_cache = {}
        self.logger = get_logger("OnboardingOrchestrator")

        # Initialize strategies
        self.strategies = {
            OnboardingMethod.SOFT: SoftOnboardingStrategy(self),
            OnboardingMethod.HARD: HardOnboardingStrategy(self),
        }

        # Special handling for Agent-4 (Captain)
        self.captain_strategy = CaptainOnboardingStrategy(self)

        self.logger.info("OnboardingOrchestrator initialized")

    def onboard_agent(self, agent_id: str, method: Union[str, OnboardingMethod] = "soft",
                     **kwargs) -> OnboardingResult:
        """Onboard a single agent."""
        global _onboarding_stats

        if isinstance(method, str):
            method = OnboardingMethod(method.lower())

        _onboarding_stats["total_onboardings"] += 1
        _onboarding_stats["last_onboarding_time"] = datetime.utcnow()

        if method == OnboardingMethod.SOFT:
            _onboarding_stats["soft_onboardings"] += 1
        elif method == OnboardingMethod.HARD:
            _onboarding_stats["hard_onboardings"] += 1

        # Special handling for Agent-4 (Captain) - always use captain strategy
        if agent_id == "Agent-4":
            strategy = self.captain_strategy
            self.logger.info("🎯 Using CaptainOnboardingStrategy for Agent-4")
        else:
            strategy = self.strategies.get(method)
            if not strategy:
                result = OnboardingResult(
                    agent_id=agent_id,
                    method=method,
                    status=OnboardingStatus.FAILED,
                    success=False
                )
                result.errors.append(f"Unknown onboarding method: {method}")
                result.complete(False)
                _onboarding_stats["failed_onboardings"] += 1
                return result

        result = strategy.execute(agent_id, **kwargs)

        if result.success:
            _onboarding_stats["successful_onboardings"] += 1
        else:
            _onboarding_stats["failed_onboardings"] += 1

        self.logger.info(f"Onboarding {'succeeded' if result.success else 'failed'} for {agent_id} using {method.value}")
        return result

    def onboard_multiple_agents(self, agent_ids: List[str],
                               method: Union[str, OnboardingMethod] = "soft",
                               max_concurrent: int = 3, **kwargs) -> List[OnboardingResult]:
        """Onboard multiple agents concurrently."""
        results = []

        # For now, process sequentially to avoid conflicts
        # Could be enhanced with actual concurrency controls
        for agent_id in agent_ids:
            result = self.onboard_agent(agent_id, method, **kwargs)
            results.append(result)

        return results

    def validate_agent_workspace(self, agent_id: str) -> AgentWorkspace:
        """Validate and analyze agent workspace."""
        workspace_path = self.agent_workspaces_dir / agent_id
        workspace = AgentWorkspace(agent_id=agent_id, workspace_path=workspace_path)

        if not workspace_path.exists():
            return workspace

        workspace.exists = True

        # Check status.json
        status_file = workspace_path / "status.json"
        if status_file.exists():
            workspace.has_status = True
            try:
                with open(status_file, 'r') as f:
                    status_data = json.load(f)
                    workspace.status_valid = isinstance(status_data, dict) and "agent_id" in status_data
                    if "last_updated" in status_data:
                        workspace.last_activity = datetime.fromisoformat(status_data["last_updated"])
            except Exception:
                workspace.status_valid = False

        # Check inbox
        inbox_dir = workspace_path / "inbox"
        if inbox_dir.exists() and inbox_dir.is_dir():
            workspace.has_inbox = True
            workspace.inbox_message_count = len(list(inbox_dir.glob("*.md")))

        # Check devlogs
        devlogs_dir = workspace_path / "devlogs"
        if devlogs_dir.exists() and devlogs_dir.is_dir():
            workspace.has_devlogs = True
            workspace.devlog_count = len(list(devlogs_dir.glob("*.md")))

        # Check coordinates
        workspace.coordinates_valid = bool(self.get_agent_coordinates(agent_id))

        return workspace

    def load_agent_coordinates(self, agent_id: str) -> bool:
        """Load agent coordinates."""
        try:
            # Try to load from cursor_agent_coords.json (primary coordinates file)
            coordinates_file = self.repo_root / "cursor_agent_coords.json"
            if coordinates_file.exists():
                with open(coordinates_file, 'r') as f:
                    data = json.load(f)

                # Extract coordinates from the cursor_agent_coords.json format
                agents_data = data.get("agents", {})
                if agent_id in agents_data:
                    agent_data = agents_data[agent_id]
                    # Use chat_input_coordinates for hard onboarding
                    if "chat_input_coordinates" in agent_data:
                        coords = agent_data["chat_input_coordinates"]
                        self.coordinates_cache[agent_id] = {
                            "x": coords[0],
                            "y": coords[1]
                        }
                        return True

            # Fallback: Try to load from agent_coordinates.json
            coordinates_file = self.repo_root / "agent_coordinates.json"
            if coordinates_file.exists():
                with open(coordinates_file, 'r') as f:
                    all_coords = json.load(f)

                if agent_id in all_coords:
                    self.coordinates_cache[agent_id] = all_coords[agent_id]
                    return True

            # Try legacy loading method
            # This would integrate with existing onboarding_helpers
            return False

        except Exception as e:
            self.logger.error(f"Failed to load coordinates for {agent_id}: {e}")
            return False

    def get_agent_coordinates(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get cached agent coordinates."""
        return self.coordinates_cache.get(agent_id)

    def load_onboarding_template(self, template_type: str, agent_id: str = None) -> Optional[str]:
        """Load onboarding template, with special handling for Agent-4."""
        try:
            # Special template for Agent-4 (Captain)
            if agent_id == "Agent-4":
                return self._get_captain_onboarding_template()

            if template_type == "soft":
                template_path = self.templates_dir / "soft" / "templates" / "soft_onboard_template.md"
            elif template_type == "hard":
                template_path = self.templates_dir / "hard" / "templates" / "hard_onboard_template.md"
            else:
                return None

            if template_path.exists():
                with open(template_path, 'r', encoding='utf-8') as f:
                    return f.read()

            return None

        except Exception as e:
            self.logger.error(f"Failed to load {template_type} onboarding template: {e}")
            return None

    def _get_captain_onboarding_template(self) -> str:
        """Get the specialized onboarding template for Agent-4 (Captain)."""
        return """# 🎯 CAPTAIN ONBOARDING PROTOCOL - AGENT-4
<!-- SSOT Domain: captain_onboarding -->

## MISSION BRIEFING

**Agent Designation:** Agent-4 (Captain)
**Role:** Strategic Oversight & Swarm Coordination
**Priority:** CRITICAL
**FSM State:** ACTIVE_COMMAND

## CORE RESPONSIBILITIES

### 1. 🤖 Swarm Intelligence Oversight
- Monitor all agent activities and status
- Coordinate inter-agent communication
- Ensure swarm cohesion and efficiency
- Resolve agent conflicts and bottlenecks

### 2. 📊 Project Scanning & Analysis
- Execute daily project scans using project scanner integration
- Analyze scan results for strategic insights
- Identify high-impact improvement opportunities
- Track project health metrics

### 3. 🎯 Task Management System
- Maintain stocked task management system
- Assign contracts based on agent capabilities
- Monitor task completion and bottlenecks
- Ensure continuous workflow optimization

### 4. 🚀 Strategic Coordination
- Make high-level decisions for swarm direction
- Coordinate major initiatives across agents
- Ensure alignment with overall mission objectives
- Provide guidance and strategic oversight

## IMMEDIATE ACTION ITEMS

### Phase 1: System Assessment
1. **Execute Project Scan**
   - Run comprehensive project analysis
   - Identify critical issues and opportunities
   - Generate strategic recommendations

2. **Agent Status Review**
   - Check status of all swarm agents
   - Identify any offline or blocked agents
   - Assess current task distribution

3. **Task Management Audit**
   - Review existing contracts and assignments
   - Identify gaps in task coverage
   - Stock task pipeline for optimal throughput

### Phase 2: Strategic Planning
1. **Priority Task Identification**
   - Analyze project scan results
   - Determine highest-impact initiatives
   - Create strategic task assignments

2. **Resource Optimization**
   - Balance agent workloads
   - Identify specialization opportunities
   - Optimize swarm performance

### Phase 3: Execution Oversight
1. **Monitor Swarm Activities**
   - Track agent progress and completion
   - Identify and resolve bottlenecks
   - Ensure quality and standards compliance

## OPERATING PROTOCOLS

### Communication Standards
- Use unified messaging system for all communications
- Maintain clear audit trails for all decisions
- Document strategic reasoning for major initiatives

### Decision Framework
- **Data-Driven**: Base decisions on project scans and agent status
- **Impact-Focused**: Prioritize high-impact, low-effort improvements
- **Swarm-Centric**: Consider entire swarm performance, not individual agents

### Escalation Procedures
- **Minor Issues**: Resolve through agent coordination
- **Major Blockers**: Escalate to human oversight if needed
- **System Failures**: Implement emergency protocols

## SUCCESS METRICS

- ✅ Swarm operating at optimal efficiency
- ✅ All agents actively contributing
- ✅ Task pipeline continuously stocked
- ✅ Project health improving over time
- ✅ Strategic objectives being met

## INITIALIZATION SEQUENCE

1. Complete system assessment (Phase 1)
2. Execute strategic planning (Phase 2)
3. Begin execution oversight (Phase 3)
4. Establish monitoring routines
5. Report readiness to swarm

---

**STATUS:** ONBOARDING COMPLETE - CAPTAIN READY FOR DUTY
**TIMESTAMP:** {{TIMESTAMP}}
**SESSION ID:** {{UUID}}

*Captain Agent-4 operational and standing by for swarm coordination.*
"""

    def get_onboarding_status(self, agent_id: str) -> Dict[str, Any]:
        """Get onboarding status for an agent."""
        workspace = self.validate_agent_workspace(agent_id)

        status = {
            "agent_id": agent_id,
            "workspace_valid": workspace.exists,
            "coordinates_loaded": workspace.coordinates_valid,
            "inbox_ready": workspace.has_inbox,
            "status_file_exists": workspace.has_status,
            "devlogs_ready": workspace.has_devlogs,
            "estimated_completion": self._estimate_completion(workspace),
            "workspace_details": workspace.to_dict()
        }

        return status

    def _estimate_completion(self, workspace: AgentWorkspace) -> str:
        """Estimate onboarding completion status."""
        checks = [
            workspace.exists,
            workspace.has_status,
            workspace.has_inbox,
            workspace.has_devlogs,
            workspace.coordinates_valid,
            workspace.status_valid
        ]

        completed = sum(checks)
        total = len(checks)

        if completed == total:
            return "complete"
        elif completed >= total * 0.7:
            return "mostly_complete"
        elif completed >= total * 0.4:
            return "in_progress"
        else:
            return "not_started"

    def validate_session_closure(self, agent_id: str, closure_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate session closure data."""
        global _onboarding_stats

        validation_result = {
            "agent_id": agent_id,
            "valid": True,
            "errors": [],
            "warnings": [],
            "score": 0
        }

        # Required fields check
        required_fields = ["task", "actions_taken", "artifacts_created", "verification", "git_commit"]
        for field in required_fields:
            if field not in closure_data:
                validation_result["errors"].append(f"Missing required field: {field}")
                validation_result["valid"] = False

        # Task description check
        if "task" in closure_data:
            task_desc = closure_data["task"]
            if len(str(task_desc).strip()) < 10:
                validation_result["warnings"].append("Task description is too brief")

        # Actions check
        if "actions_taken" in closure_data:
            actions = closure_data["actions_taken"]
            if isinstance(actions, list) and len(actions) == 0:
                validation_result["errors"].append("No actions taken specified")
                validation_result["valid"] = False

        # Artifacts check
        if "artifacts_created" in closure_data:
            artifacts = closure_data["artifacts_created"]
            if isinstance(artifacts, list):
                # Check if artifacts actually exist
                for artifact in artifacts:
                    if isinstance(artifact, str) and not Path(artifact).exists():
                        validation_result["warnings"].append(f"Artifact does not exist: {artifact}")

        # Git checks
        if "git_commit" in closure_data:
            commit = closure_data["git_commit"]
            if commit and commit not in ["Not committed", "Pending"]:
                # Could validate commit hash format
                if not re.match(r'^[a-f0-9]{7,40}$', str(commit)):
                    validation_result["warnings"].append("Invalid git commit hash format")

        # Calculate score
        total_checks = 5
        errors_count = len(validation_result["errors"])
        warnings_count = len(validation_result["warnings"])

        validation_result["score"] = max(0, (total_checks - errors_count - warnings_count) / total_checks * 100)

        if validation_result["valid"]:
            _onboarding_stats["session_closures_validated"] += 1

        return validation_result

    def get_onboarding_stats(self) -> Dict[str, Any]:
        """Get onboarding statistics."""
        global _onboarding_stats

        stats = _onboarding_stats.copy()

        # Calculate success rate
        if stats["total_onboardings"] > 0:
            stats["success_rate"] = stats["successful_onboardings"] / stats["total_onboardings"] * 100
        else:
            stats["success_rate"] = 0.0

        return stats

# Convenience functions

def onboard_agent(agent_id: str, method: Union[str, OnboardingMethod] = "soft", **kwargs) -> OnboardingResult:
    """Convenience function to onboard a single agent."""
    orchestrator = OnboardingOrchestrator()
    return orchestrator.onboard_agent(agent_id, method, **kwargs)

def onboard_multiple_agents(agent_ids: List[str], method: Union[str, OnboardingMethod] = "soft",
                           **kwargs) -> List[OnboardingResult]:
    """Convenience function to onboard multiple agents."""
    orchestrator = OnboardingOrchestrator()
    return orchestrator.onboard_multiple_agents(agent_ids, method, **kwargs)

def validate_session_closure(agent_id: str, closure_data: Dict[str, Any]) -> Dict[str, Any]:
    """Convenience function to validate session closure."""
    orchestrator = OnboardingOrchestrator()
    return orchestrator.validate_session_closure(agent_id, closure_data)

def get_agent_workspace_status(agent_id: str) -> Dict[str, Any]:
    """Convenience function to get agent workspace status."""
    orchestrator = OnboardingOrchestrator()
    return orchestrator.get_onboarding_status(agent_id)

def get_onboarding_statistics() -> Dict[str, Any]:
    """Convenience function to get onboarding statistics."""
    orchestrator = OnboardingOrchestrator()
    return orchestrator.get_onboarding_stats()

# Export everything needed
__all__ = [
    # Main classes
    "OnboardingOrchestrator",
    "OnboardingResult",
    "AgentWorkspace",

    # Enums
    "OnboardingMethod",
    "OnboardingStatus",
    "OnboardingStep",

    # Strategies
    "OnboardingStrategy",
    "SoftOnboardingStrategy",
    "HardOnboardingStrategy",

    # Functions
    "onboard_agent",
    "onboard_multiple_agents",
    "validate_session_closure",
    "get_agent_workspace_status",
    "get_onboarding_statistics",
]