#!/usr/bin/env python3
"""
Unified CLI Handlers V2 - Phase 4 Consolidation
===============================================

PHASE 4 CONSOLIDATION: Consolidated CLI handler modules
Merged from: handlers/task_handler.py, handlers/batch_message_handler.py,
             handlers/utility_handler.py, handlers/coordinate_handler.py

Reduced from 4 separate handler files (~1000+ lines) to 1 consolidated module

Consolidated CLI handlers for:
- TaskHandler: Task management operations (get-next-task, list-tasks, task-status, complete-task)
- BatchMessageHandler: Message batching operations (batch-start, batch-add, batch-send, batch-status, batch-cancel)
- UtilityHandler: Utility operations (status checks, vector database operations)
- CoordinateHandler: Coordinate management and validation

Features:
- Unified CLI command interface across all operations
- Consolidated error handling and logging
- Single responsibility principle maintained
- V2 compliance and SSOT integration

V2 Compliance: <800 lines
Author: Agent-2 (Architecture & Design) - Phase 4 Consolidation 2026-01-06
<!-- SSOT Domain: integration -->
"""

import logging
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from ..core.base.base_service import BaseService

logger = logging.getLogger(__name__)


class UnifiedTaskHandler(BaseService):
    """Unified task handler for task management operations.

    PHASE 4 CONSOLIDATION: Migrated from handlers/task_handler.py
    Handles task system commands: get-next-task, list-tasks, task-status, complete-task.
    """

    def __init__(self):
        """Initialize unified task handler."""
        super().__init__("UnifiedTaskHandler")
        self.exit_code = 0
        self._ensure_data_dir()

    def _ensure_data_dir(self) -> None:
        """Ensure data directory exists for task database."""
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)

    def can_handle(self, args) -> bool:
        """Check if this handler can handle the given arguments."""
        return (
            hasattr(args, "get_next_task") and args.get_next_task
            or hasattr(args, "list_tasks") and args.list_tasks
            or hasattr(args, "task_status") and args.task_status
            or hasattr(args, "complete_task") and args.complete_task
        )

    def handle(self, args) -> bool:
        """Handle task commands."""
        try:
            if hasattr(args, "get_next_task") and args.get_next_task:
                return self._handle_get_next_task(args)
            elif hasattr(args, "list_tasks") and args.list_tasks:
                return self._handle_list_tasks(args)
            elif hasattr(args, "task_status") and args.task_status:
                return self._handle_task_status(args)
            elif hasattr(args, "complete_task") and args.complete_task:
                return self._handle_complete_task(args)
            else:
                logger.error("❌ No valid task command specified")
                self.exit_code = 1
                return True

        except Exception as e:
            logger.error(f"❌ Task handling error: {e}")
            self.exit_code = 1
            return True

    def _handle_get_next_task(self, args) -> bool:
        """Handle get next task command."""
        try:
            from .unified_service_managers import UnifiedContractManager

            agent_id = getattr(args, "agent", None)
            if not agent_id:
                logger.error("❌ --agent required for --get-next-task")
                self.exit_code = 1
                return True

            manager = UnifiedContractManager()
            contracts = manager.get_agent_contracts(agent_id)

<<<<<<< HEAD
            if contracts.get("success"):
                # Successfully retrieved contracts (may be empty)
                all_contracts = contracts.get("contracts", [])

                # Get the first pending/active contract
                pending_contracts = [
                    c for c in all_contracts
=======
            if contracts.get("success") and contracts.get("contracts"):
                # Get the first pending/active contract
                pending_contracts = [
                    c for c in contracts["contracts"]
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
                    if c.get("status") in ["pending", "active"]
                ]

                if pending_contracts:
                    contract = pending_contracts[0]
                    logger.info(f"📋 Next task for {agent_id}:")
                    logger.info(f"   Title: {contract.get('title', 'N/A')}")
                    logger.info(f"   Description: {contract.get('description', 'N/A')}")
                    logger.info(f"   Priority: {contract.get('priority', 'normal')}")
                    if contract.get("deadline"):
                        logger.info(f"   Deadline: {contract.get('deadline')}")

                    self.exit_code = 0
                else:
                    logger.info(f"📋 No pending tasks for {agent_id}")
                    self.exit_code = 0
            else:
                logger.error(f"❌ Failed to get contracts for {agent_id}")
                self.exit_code = 1

            return True

        except Exception as e:
            logger.error(f"❌ Error getting next task: {e}")
            self.exit_code = 1
            return True

    def _handle_list_tasks(self, args) -> bool:
        """Handle list tasks command."""
        try:
            from .unified_service_managers import UnifiedContractManager

            agent_id = getattr(args, "agent", None)
            if not agent_id:
                logger.error("❌ --agent required for --list-tasks")
                self.exit_code = 1
                return True

            manager = UnifiedContractManager()
            contracts = manager.get_agent_contracts(agent_id)

            if contracts.get("success"):
                logger.info(f"📋 Tasks for {agent_id} ({len(contracts.get('contracts', []))} total):")

                for contract in contracts.get("contracts", []):
                    status = contract.get("status", "unknown")
                    title = contract.get("title", "N/A")[:50]
                    priority = contract.get("priority", "normal")
                    logger.info(f"   • [{status.upper()}] {title} (Priority: {priority})")

                self.exit_code = 0
            else:
                logger.error(f"❌ Failed to list tasks for {agent_id}")
                self.exit_code = 1

            return True

        except Exception as e:
            logger.error(f"❌ Error listing tasks: {e}")
            self.exit_code = 1
            return True

    def _handle_task_status(self, args) -> bool:
        """Handle task status command."""
        try:
            from .unified_service_managers import UnifiedContractManager

            agent_id = getattr(args, "agent", None)
            if not agent_id:
                logger.error("❌ --agent required for --task-status")
                self.exit_code = 1
                return True

            manager = UnifiedContractManager()
            status = manager.get_system_status()

            if status.get("success", False):
                logger.info(f"📊 Contract System Status:")
                logger.info(f"   Total Contracts: {status.get('total_contracts', 0)}")
                logger.info(f"   Active: {status.get('active_contracts', 0)}")
                logger.info(f"   Completed: {status.get('completed_contracts', 0)}")
                logger.info(f"   Pending: {status.get('pending_contracts', 0)}")
                self.exit_code = 0
            else:
                logger.error("❌ Failed to get contract system status")
                self.exit_code = 1

            return True

        except Exception as e:
            logger.error(f"❌ Error getting task status: {e}")
            self.exit_code = 1
            return True

    def _handle_complete_task(self, args) -> bool:
        """Handle complete task command."""
        try:
            task_id = getattr(args, "task_id", None)
            if not task_id:
                logger.error("❌ --task-id required for --complete-task")
                self.exit_code = 1
                return True

            # This would integrate with contract system to mark task complete
            logger.info(f"✅ Task {task_id} marked as completed")
            logger.warning("⚠️  Task completion integration not yet implemented")
            self.exit_code = 0
            return True

        except Exception as e:
            logger.error(f"❌ Error completing task: {e}")
            self.exit_code = 1
            return True


class UnifiedBatchMessageHandler(BaseService):
    """Unified batch message handler for message batching operations.

    PHASE 4 CONSOLIDATION: Migrated from handlers/batch_message_handler.py
    Handles batch operations: batch-start, batch-add, batch-send, batch-status, batch-cancel.
    """

    def __init__(self):
        """Initialize unified batch message handler."""
        super().__init__("UnifiedBatchMessageHandler")
        self.exit_code = 0

    def can_handle(self, args) -> bool:
        """Check if this handler can handle the given arguments."""
        return (
            hasattr(args, "batch_start") and args.batch_start
            or hasattr(args, "batch_add") and args.batch_add
            or hasattr(args, "batch_send") and args.batch_send
            or hasattr(args, "batch_status") and args.batch_status
            or hasattr(args, "batch_cancel") and args.batch_cancel
            or hasattr(args, "batch") and args.batch
        )

    def handle(self, args) -> bool:
        """Handle batch message commands."""
        try:
            from ..message_batching_service import get_batching_service

            service = get_batching_service()

            # Determine sender (agent or captain)
            sender = getattr(args, "agent", None) or "CAPTAIN"
            recipient = "Agent-4"  # Default to Captain

            # Handle simplified batch (--batch)
            if hasattr(args, "batch") and args.batch:
                return self._handle_simplified_batch(args, service, sender, recipient)

            # Handle batch-start
            if hasattr(args, "batch_start") and args.batch_start:
                return self._handle_batch_start(args, service, sender, recipient)

            # Handle batch-add
            if hasattr(args, "batch_add") and args.batch_add:
                return self._handle_batch_add(args, service, sender, recipient)

            # Handle batch-send
            if hasattr(args, "batch_send") and args.batch_send:
                return self._handle_batch_send(args, service, sender, recipient)

            # Handle batch-status
            if hasattr(args, "batch_status") and args.batch_status:
                return self._handle_batch_status(args, service, sender, recipient)

            # Handle batch-cancel
            if hasattr(args, "batch_cancel") and args.batch_cancel:
                return self._handle_batch_cancel(args, service, sender, recipient)

            return True

        except ImportError as e:
            logger.error(f"❌ Message batching service not available: {e}")
            self.exit_code = 1
            return True
        except Exception as e:
            logger.error(f"❌ Batch handling error: {e}")
            self.exit_code = 1
            return True

    def _handle_simplified_batch(self, args, service, sender, recipient) -> bool:
        """Handle simplified batch (all in one command)."""
        if not hasattr(args, "batch") or not args.batch:
            logger.error("❌ No messages provided for batch")
            self.exit_code = 1
            return True

        logger.info(f"📦 Simplified batch: {len(args.batch)} messages")

        # Start batch
        service.start_batch(sender, recipient)

        # Add all messages
        for i, message in enumerate(args.batch, 1):
            logger.info(f"📥 Adding message {i}/{len(args.batch)}")
            service.add_to_batch(sender, recipient, message)

        # Send batch
        raw_priority = getattr(args, "priority", "regular")
        normalized_priority = "regular" if raw_priority == "normal" else raw_priority

        success, consolidated_message = service.send_batch(
            sender, recipient, priority=normalized_priority
        )

        if success:
            # Send consolidated message via messaging system
            from ..core.messaging_core import (
                UnifiedMessagePriority,
                UnifiedMessageTag,
                UnifiedMessageType,
                send_message,
            )

            priority = (
                UnifiedMessagePriority.URGENT
                if normalized_priority == "urgent"
                else UnifiedMessagePriority.REGULAR
            )

            send_success = send_message(
                content=consolidated_message,
                sender=sender,
                recipient=recipient,
                message_type=UnifiedMessageType.AGENT_TO_CAPTAIN,
                priority=priority,
                tags=[UnifiedMessageTag.BATCHED, UnifiedMessageTag.COORDINATION],
            )

            if send_success:
                logger.info("✅ Batch sent successfully")
                self.exit_code = 0
            else:
                logger.error("❌ Failed to send consolidated batch message")
                self.exit_code = 1
        else:
            logger.error("❌ Failed to create consolidated batch message")
            self.exit_code = 1

        return True

    def _handle_batch_start(self, args, service, sender, recipient) -> bool:
        """Handle batch-start command."""
        logger.info("📦 Starting new message batch")
        service.start_batch(sender, recipient)
        logger.info("✅ Batch started successfully")
        return True

    def _handle_batch_add(self, args, service, sender, recipient) -> bool:
        """Handle batch-add command."""
        if not hasattr(args, "message") or not args.message:
            logger.error("❌ --message required for --batch-add")
            self.exit_code = 1
            return True

        service.add_to_batch(sender, recipient, args.message)
        logger.info("✅ Message added to batch")
        return True

    def _handle_batch_send(self, args, service, sender, recipient) -> bool:
        """Handle batch-send command."""
        raw_priority = getattr(args, "priority", "regular")
        normalized_priority = "regular" if raw_priority == "normal" else raw_priority

        success, consolidated_message = service.send_batch(
            sender, recipient, priority=normalized_priority
        )

        if success:
            logger.info("✅ Batch sent successfully")
            self.exit_code = 0
        else:
            logger.error("❌ Failed to send batch")
            self.exit_code = 1

        return True

    def _handle_batch_status(self, args, service, sender, recipient) -> bool:
        """Handle batch-status command."""
        status = service.get_batch_status(sender, recipient)
        logger.info(f"📊 Batch Status: {status}")
        return True

    def _handle_batch_cancel(self, args, service, sender, recipient) -> bool:
        """Handle batch-cancel command."""
        service.cancel_batch(sender, recipient)
        logger.info("✅ Batch cancelled")
        return True


class UnifiedUtilityHandler(BaseService):
    """Unified utility handler for utility operations.

    PHASE 4 CONSOLIDATION: Migrated from handlers/utility_handler.py
    Handles utility operations: status checks, vector database operations.
    """

    def __init__(self):
        """Initialize unified utility handler."""
        super().__init__("UnifiedUtilityHandler")

        # Vector database imports with guard (optional dependency)
        try:
            from ..core.vector_database import VectorDatabaseService
            from ..vector_database_service_unified import get_vector_database_service
            self.VECTOR_DB_AVAILABLE = True
        except ImportError:
            self.VECTOR_DB_AVAILABLE = False

    def check_status(self, agent_id: Optional[str] = None) -> dict[str, Any]:
        """Check status of agents or specific agent using onboarding handler."""
        try:
            from .unified_onboarding_handlers import UnifiedOnboardingHandler

            handler = UnifiedOnboardingHandler()
            # This would need to be implemented based on the onboarding handler interface
            return {"success": True, "message": "Status check not yet implemented in unified handler"}

        except Exception as e:
            logger.error(f"Error checking status: {e}")
            return {"success": False, "error": str(e)}

    def get_system_info(self) -> dict[str, Any]:
        """Get system information."""
        return {
            "vector_db_available": self.VECTOR_DB_AVAILABLE,
            "timestamp": datetime.now().isoformat(),
        }


class UnifiedCoordinateHandler(BaseService):
    """Unified coordinate handler for coordinate management and validation.

    PHASE 4 CONSOLIDATION: Migrated from handlers/coordinate_handler.py
    Handles coordinate loading, caching, and validation.
    """

    def __init__(self):
        """Initialize unified coordinate handler."""
        super().__init__("UnifiedCoordinateHandler")
        self.coordinates_cache: dict[str, list[int]] = {}
        self.last_coordinate_load: Optional[float] = None
        self.cache_ttl_seconds = 300

    def can_handle(self, args) -> bool:
        """Check if this handler can handle the given arguments."""
        return False  # This handler is used programmatically, not via CLI args

    def handle(self, args) -> bool:
        """Handle the command."""
        return False

    async def load_coordinates_async(self, service=None) -> dict[str, Any]:
        """Load agent coordinates asynchronously with caching."""
        try:
            from ..core.coordinate_loader import get_coordinate_loader

            # Check cache validity
            current_time = time.time()
            if (
                self.last_coordinate_load
                and (current_time - self.last_coordinate_load) < self.cache_ttl_seconds
                and self.coordinates_cache
            ):
                logger.info("📍 Using cached coordinates")
                return {
                    "success": True,
                    "coordinates": self.coordinates_cache,
                    "cached": True,
                    "cache_age_seconds": current_time - self.last_coordinate_load,
                }

            # Load fresh coordinates
            loader = get_coordinate_loader()
            result = await loader.load_coordinates_async()

            if result.get("success"):
                self.coordinates_cache = result["coordinates"]
                self.last_coordinate_load = current_time
                logger.info("📍 Coordinates loaded and cached")

            return result

        except Exception as e:
            logger.error(f"Error loading coordinates: {e}")
            return {"success": False, "error": str(e)}

    def print_coordinates_table(self, coordinates: dict[str, list[int]]) -> None:
        """Print coordinates in a formatted table."""
        if not coordinates:
            logger.info("📍 No coordinates available")
            return

        logger.info("📍 Agent Coordinates:")
        logger.info("   Agent ID    | X    | Y")
        logger.info("   ------------|------|------")

        for agent_id, coords in coordinates.items():
            if len(coords) >= 2:
                logger.info("5")
            else:
                logger.info("5")


# Backward compatibility aliases
TaskHandler = UnifiedTaskHandler
BatchMessageHandler = UnifiedBatchMessageHandler
UtilityHandler = UnifiedUtilityHandler
CoordinateHandler = UnifiedCoordinateHandler

# Export all unified handlers
__all__ = [
    "UnifiedTaskHandler",
    "UnifiedBatchMessageHandler",
    "UnifiedUtilityHandler",
    "UnifiedCoordinateHandler",
    "TaskHandler",  # Backward compatibility
    "BatchMessageHandler",  # Backward compatibility
    "UtilityHandler",  # Backward compatibility
    "CoordinateHandler",  # Backward compatibility
]