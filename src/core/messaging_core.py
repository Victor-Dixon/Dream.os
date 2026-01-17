#!/usr/bin/env python3
"""
Messaging Core Services - Service Layer Architecture
===================================================

<!-- SSOT Domain: integration -->

Core messaging services following service layer pattern.
Extracted from monolithic messaging_unified.py for better maintainability.

SERVICES INCLUDED:
- MessageQueueService: Queue management and persistence
- TemplateResolutionService: Dynamic message formatting
- DeliveryOrchestrationService: Coordinates delivery methods
- MessageValidationService: Content validation and sanitization
- MessagingCoreOrchestrator: Main orchestration layer

PHASE 2 INFRASTRUCTURE REFACTORING:
- Service layer pattern implementation
- Clear separation of concerns
- Dependency injection for testability
- Modular design for extensibility

ARCHITECTURAL REFACTORING (Agent-2):
- V2 Compliance: Broke down 544-line monolithic file into 5 service modules
- Each service now in separate file under 300 lines (V2 max limit)
- Improved maintainability and testability
- Preserved all legacy compatibility functions

Author: Agent-3 (Infrastructure & DevOps Specialist)
Architectural Refactoring: Agent-2 (Architecture & Design Specialist)
Created: 2026-01-16
Last Refactored: 2026-01-16
"""

import logging

logger = logging.getLogger(__name__)

# Import service modules (V2 compliance - separated from monolithic file)
from .services.message_queue_service import MessageQueueService
from .services.template_resolution_service import TemplateResolutionService
from .services.message_validation_service import MessageValidationService
from .services.delivery_orchestration_service import DeliveryOrchestrationService
from .services.messaging_core_orchestrator import (
    MessagingCoreOrchestrator,
    send_agent_message,
    broadcast_message,
    get_messaging_stats
)

# Legacy class aliases for backward compatibility
# These are now imported from separate service modules to maintain V2 compliance
# (each service class moved to individual files under 300 lines)

# All service classes and legacy functions are now imported from separate modules above
# This maintains backward compatibility while achieving V2 compliance

# End of file - all functionality now in separate service modules
