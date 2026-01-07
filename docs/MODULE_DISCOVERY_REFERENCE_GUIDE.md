# Module Discovery Reference Guide
## Complex Module Hierarchies: Analytics, Services, Core

**Author:** Agent-5 (Business Intelligence Specialist)
**Created:** 2026-01-07
**Purpose:** Comprehensive import path reference for complex module hierarchies

---

## Table of Contents
1. [Core Module Hierarchy](#core-module-hierarchy)
2. [Services Module Hierarchy](#services-module-hierarchy)
3. [Infrastructure Module Hierarchy](#infrastructure-module-hierarchy)
4. [Analytics Module Hierarchy](#analytics-module-hierarchy)
5. [Cross-Module Import Patterns](#cross-module-import-patterns)
6. [Common Import Anti-Patterns](#common-import-anti-patterns)
7. [Quick Reference Map](#quick-reference-map)

---

## Core Module Hierarchy

The `src/core/` directory contains foundational system components organized by functionality:

### Base Infrastructure (`src/core/base/`)
```python
# Base service classes and interfaces
from src.core.base.base_service import BaseService
from src.core.base.service_registry import ServiceRegistry
from src.core.base.unified_service_base import UnifiedServiceBase
```

### Configuration Management (`src/core/config/`)
```python
# System configuration and settings
from src.core.config.architectural_assignments import ARCHITECTURAL_ASSIGNMENTS
from src.core.config.unified_config import UnifiedConfig
from src.core.pydantic_config import PydanticConfig
```

### Constants and Models (`src/core/constants/`)
```python
# System-wide constants and data models
from src.core.constants.agent_constants import AGENT_LIST, AGENT_ROLES
from src.core.constants.system_constants import SYSTEM_PATHS, DEFAULT_TIMEOUTS
from src.core.messaging_models_core import MessageCategory, MessagePriority
```

### Analytics Components (`src/core/analytics/`)
```python
# Core analytics processing and metrics
from src.core.analytics.analytics_processor import AnalyticsProcessor
from src.core.analytics.metrics_collector import MetricsCollector
from src.core.analytics.performance_tracker import PerformanceTracker
```

### Coordination Systems (`src/core/coordination/`)
```python
# Agent coordination and orchestration
from src.core.coordination.coordinator import Coordinator
from src.core.coordination.task_distributor import TaskDistributor
from src.core.coordinator_interfaces import ICoordinator
```

### Messaging Infrastructure (`src/core/messaging/`)
```python
# Unified messaging system components
from src.core.messaging.messagerouter import MessageRouter
from src.core.messaging.messagevalidator import MessageValidator
from src.core.messaging.delivery_orchestrator import DeliveryOrchestrator
```

### Error Handling (`src/core/error_handling/`)
```python
# Centralized error management
from src.core.error_handling.error_handler import ErrorHandler
from src.core.error_handling.recovery_manager import RecoveryManager
```

### File and I/O Operations (`src/core/file_locking/`, `src/core/utilities/`)
```python
# File system operations and utilities
from src.core.file_locking.file_lock_manager import FileLockManager
from src.core.utilities.file_utils import FileUtils
from src.core.utilities.path_helpers import PathHelpers
```

---

## Services Module Hierarchy

The `src/services/` directory contains business logic and domain services:

### Core Services
```python
# Primary business services
from src.services.unified_messaging_service import UnifiedMessagingService
from src.services.coordinator import CoordinatorService
from src.services.contract_service import ContractService
from src.services.ai_service import AIService
from src.services.verification_service import VerificationService
from src.services.recovery_service import RecoveryService
from src.services.work_indexer import WorkIndexer
from src.services.performance_analyzer import PerformanceAnalyzer
from src.services.recommendation_engine import RecommendationEngine
from src.services.swarm_intelligence_manager import SwarmIntelligenceManager
```

### Specialized Services
```python
# Domain-specific services
from src.services.portfolio_service import PortfolioService
from src.services.risk_analytics.risk_calculator import RiskCalculator
from src.services.thea_client import TheaClient
from src.services.vector_database_service_unified import VectorDatabaseService
```

### Onboarding and Management
```python
# User and agent onboarding
from src.services.soft_onboarding_service import SoftOnboardingService
from src.services.hard_onboarding_service import HardOnboardingService
from src.services.agent_management import AgentManagementService
```

### Messaging Services (`src/services/messaging/`)
```python
# Messaging protocol implementations
from src.services.messaging.sender_validation import SenderValidation
from src.services.messaging.infrastructure import MessagingInfrastructure
from src.services.messaging.handlers import MessageHandlers
```

### Contract System (`src/services/contract_system/`)
```python
# Contract management and validation
from src.services.contract_system.contract_manager import ContractManager
from src.services.contract_system.contract_validator import ContractValidator
```

---

## Infrastructure Module Hierarchy

The `src/infrastructure/` directory contains technical infrastructure components:

### Analytics Infrastructure
```python
# Analytics deployment and monitoring
from src.infrastructure.analytics_service import get_analytics_service
from src.infrastructure.analytics_deployment_monitor import AnalyticsDeploymentMonitor
```

### Persistence Layer (`src/infrastructure/persistence/`)
```python
# Data persistence and repositories
from src.infrastructure.persistence.agent_repository import AgentRepository
from src.infrastructure.persistence.task_repository import TaskRepository
from src.infrastructure.persistence.database_connection import DatabaseConnection
```

### Browser Infrastructure (`src/infrastructure/browser/`)
```python
# Browser automation and management
from src.infrastructure.browser.unified_browser_service import UnifiedBrowserService
from src.infrastructure.browser.thea_browser_core import TheaBrowserCore
from src.infrastructure.browser.unified.driver_manager import DriverManager
```

### Logging Infrastructure (`src/infrastructure/logging/`)
```python
# Centralized logging system
from src.infrastructure.logging.unified_logger import UnifiedLogger
from src.infrastructure.logging.log_handlers import LogHandlers
from src.infrastructure.logging.std_logger import StdLogger
```

### Time and System Infrastructure (`src/infrastructure/time/`)
```python
# Time management and system clock
from src.infrastructure.time.system_clock import SystemClock
```

---

## Analytics Module Hierarchy

Analytics modules are distributed across multiple locations:

### Core Analytics (`src/core/analytics/`)
```python
from src.core.analytics.analytics_processor import AnalyticsProcessor
from src.core.analytics.metrics_collector import MetricsCollector
from src.core.vector_integration_analytics import VectorIntegrationAnalytics
```

### Infrastructure Analytics (`src/infrastructure/`)
```python
from src.infrastructure.analytics_service import get_analytics_service
from src.infrastructure.analytics_deployment_monitor import AnalyticsDeploymentMonitor
```

### Services Analytics (`src/services/risk_analytics/`)
```python
from src.services.risk_analytics.risk_calculator import RiskCalculator
from src.services.risk_analytics.portfolio_analytics import PortfolioAnalytics
```

### Tools Analytics (`tools/`)
```python
from tools.analytics_validation_scheduler import AnalyticsValidationScheduler
from tools.analytics_deployment_automation import AnalyticsDeploymentAutomation
from tools.analytics_operations_center import AnalyticsOperationsCenter
```

---

## Cross-Module Import Patterns

### Service → Core Dependencies
```python
# Services importing core functionality
from src.core.messaging_models_core import MessageCategory
from src.core.constants.agent_constants import AGENT_LIST
from src.core.base.base_service import BaseService
from src.core.utilities.file_utils import FileUtils
```

### Infrastructure → Core Dependencies
```python
# Infrastructure components importing core systems
from src.core.config.unified_config import UnifiedConfig
from src.core.error_handling.error_handler import ErrorHandler
from src.core.persistence.base_repository import BaseRepository
```

### Services → Infrastructure Dependencies
```python
# Services using infrastructure components
from src.infrastructure.analytics_service import get_analytics_service
from src.infrastructure.persistence.agent_repository import AgentRepository
from src.infrastructure.logging.unified_logger import UnifiedLogger
```

### Analytics Cross-Dependencies
```python
# Analytics components across modules
from src.core.analytics.analytics_processor import AnalyticsProcessor
from src.infrastructure.analytics_deployment_monitor import AnalyticsDeploymentMonitor
from src.services.risk_analytics.risk_calculator import RiskCalculator
```

---

## Common Import Anti-Patterns

### ❌ Circular Imports
```python
# AVOID: These create circular dependencies
# core/analytics.py imports services.risk_analytics
# services/risk_analytics.py imports core.analytics
```

### ❌ Deep Nested Imports
```python
# AVOID: Too specific, brittle imports
from src.core.messaging.templates.data.formats.json_formatter import JSONFormatter

# ✅ PREFER: Import from public interface
from src.core.messaging.formatting import JSONFormatter
```

### ❌ Direct Internal Imports
```python
# AVOID: Importing internal implementation details
from src.services.risk_analytics._internal.calculations import _calculate_var

# ✅ PREFER: Import from public API
from src.services.risk_analytics import calculate_value_at_risk
```

---

## Quick Reference Map

### Import Path Quick Reference

| Component | Primary Location | Import Pattern |
|-----------|------------------|----------------|
| **Base Services** | `src/core/base/` | `from src.core.base.* import *` |
| **Configuration** | `src/core/config/` | `from src.core.config.* import *` |
| **Constants** | `src/core/constants/` | `from src.core.constants.* import *` |
| **Analytics Core** | `src/core/analytics/` | `from src.core.analytics.* import *` |
| **Messaging** | `src/core/messaging/` | `from src.core.messaging.* import *` |
| **Coordination** | `src/core/coordination/` | `from src.core.coordinator import *` |
| **Unified Messaging** | `src/services/` | `from src.services.unified_messaging_service import *` |
| **AI Service** | `src/services/` | `from src.services.ai_service import *` |
| **Risk Analytics** | `src/services/risk_analytics/` | `from src.services.risk_analytics.* import *` |
| **Analytics Infrastructure** | `src/infrastructure/` | `from src.infrastructure.analytics_* import *` |
| **Persistence** | `src/infrastructure/persistence/` | `from src.infrastructure.persistence.* import *` |
| **Logging** | `src/infrastructure/logging/` | `from src.infrastructure.logging.* import *` |

### Service Locator Pattern Usage

For dynamic service resolution, use the service registry:

```python
from src.core.base.service_registry import ServiceRegistry

# Get service instance dynamically
analytics_service = ServiceRegistry.get_service('analytics')
messaging_service = ServiceRegistry.get_service('messaging')
```

### Factory Pattern Usage

For complex object creation:

```python
from src.core.analytics.analytics_processor import AnalyticsProcessorFactory
from src.services.risk_analytics.risk_calculator import RiskCalculatorFactory

# Create configured instances
processor = AnalyticsProcessorFactory.create('portfolio_analytics')
calculator = RiskCalculatorFactory.create('advanced_risk')
```

---

## Navigation Tips

1. **Always import from the public interface** of modules, not internal implementations
2. **Use absolute imports** (`from src.module import Component`) over relative imports
3. **Check for circular dependencies** by reviewing import graphs
4. **Use service registries** for dynamic service resolution
5. **Follow the dependency direction**: Core ← Infrastructure ← Services ← Application

## Related Documentation

- [SSOT Compliance Guide](../SSOT/SSOT_COMPLIANCE_GUIDE.md)
- [Architecture Overview](../architecture/SYSTEM_ARCHITECTURE.md)
- [Service Integration Patterns](../architecture/SERVICE_INTEGRATION_PATTERNS.md)
- [Code Navigation Guide](./CODE_NAVIGATION_GUIDE.md)

---

**Note:** This guide should be updated whenever new modules are added or import patterns change. Use the `tools/module_dependency_analyzer.py` to validate import relationships.