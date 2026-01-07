# Module Discovery Reference Guide
<!-- SSOT Domain: documentation -->

## Complex Module Hierarchies Import Path Reference

This guide provides comprehensive import path references for the three most complex module hierarchies in Agent Cellphone V2: **Analytics**, **Services**, and **Core**. Each section includes navigation trees, common import patterns, and cross-references to related documentation and API endpoints.

---

## 📊 Analytics Module Hierarchy (`src/core/analytics/`)

### Directory Structure
```
src/core/analytics/
├── coordinators/
│   ├── analytics_coordinator.py
│   └── processing_coordinator.py
├── engines/
│   ├── batch_analytics_engine.py
│   ├── caching_engine_fixed.py
│   ├── coordination_analytics_engine.py
│   ├── metrics_engine.py
│   └── realtime_analytics_engine.py
├── intelligence/
│   ├── anomaly_detection_engine.py
│   ├── business_intelligence_engine*.py
│   ├── pattern_analysis_engine.py
│   └── predictive_modeling_engine.py
│   └── pattern_analysis/
│       ├── anomaly_detector.py
│       ├── pattern_extractor.py
│       └── trend_analyzer.py
├── models/
│   └── coordination_analytics_models.py
├── orchestrators/
│   └── coordination_analytics_orchestrator.py
├── prediction/
│   └── base_analyzer.py
└── processors/
    ├── insight_processor.py
    ├── prediction_processor.py
    └── prediction/
        ├── prediction_analyzer.py
        ├── prediction_calculator.py
        └── prediction_validator.py
```

### Common Import Patterns

#### From Analytics Root
```python
# Engines
from src.core.analytics.engines.metrics_engine import MetricsEngine
from src.core.analytics.engines.realtime_analytics_engine import RealtimeAnalyticsEngine
from src.core.analytics.engines.batch_analytics_engine import BatchAnalyticsEngine

# Intelligence
from src.core.analytics.intelligence.pattern_analysis_engine import PatternAnalysisEngine
from src.core.analytics.intelligence.business_intelligence_engine import BusinessIntelligenceEngine
from src.core.analytics.intelligence.anomaly_detection_engine import AnomalyDetectionEngine

# Coordinators
from src.core.analytics.coordinators.analytics_coordinator import AnalyticsCoordinator
from src.core.analytics.coordinators.processing_coordinator import ProcessingCoordinator
```

#### From Analytics Submodules
```python
# Pattern Analysis Components
from src.core.analytics.intelligence.pattern_analysis.anomaly_detector import AnomalyDetector
from src.core.analytics.intelligence.pattern_analysis.pattern_extractor import PatternExtractor
from src.core.analytics.intelligence.pattern_analysis.trend_analyzer import TrendAnalyzer

# Prediction Processing
from src.core.analytics.processors.prediction.prediction_analyzer import PredictionAnalyzer
from src.core.analytics.processors.prediction.prediction_calculator import PredictionCalculator
from src.core.analytics.processors.prediction.prediction_validator import PredictionValidator
```

#### Cross-Module Analytics Imports
```python
# Analytics ↔ Services
from src.services.performance_analyzer import PerformanceAnalyzer
from src.services.portfolio_service import PortfolioService

# Analytics ↔ Core
from src.core.vector_integration_analytics import VectorIntegrationAnalytics
from src.core.pattern_analysis.pattern_analysis_orchestrator import PatternAnalysisOrchestrator

# Analytics ↔ Trading Robot
from src.trading_robot.services.analytics.risk_analysis_engine import RiskAnalysisEngine
from src.trading_robot.services.analytics.performance_metrics_engine import PerformanceMetricsEngine
```

### Related Files & Dependencies
- **Documentation**: `docs/analytics/architecture_overview.md`
- **Web Integration**: `src/web/static/js/trading-robot/risk-dashboard-integration.js`
- **Trading Robot**: `src/trading_robot/services/trading_bi_analytics.py`
- **Infrastructure**: `src/infrastructure/analytics_service.py`

---

## 🔧 Services Module Hierarchy (`src/services/`)

### Directory Structure
```
src/services/
├── ai_service.py
├── unified_messaging_service.py
├── coordinator.py
├── contract_service.py
├── verification_service.py
├── work_indexer.py
├── performance_analyzer.py
├── recommendation_engine.py
├── recovery_service.py
├── swarm_intelligence_manager.py
├── soft_onboarding_service.py
├── messaging/
│   ├── messaging_rest_api.py
│   ├── messaging_service.py
│   └── messaging_websocket.py
├── risk_analytics/
│   ├── risk_calculator_service.py
│   ├── risk_websocket_server.py
│   └── risk_api_endpoints.py
├── chatgpt/
├── thea/
├── vector/
├── vector_database/
├── onboarding/
├── coordination/
└── [40+ additional service files]
```

### Common Import Patterns

#### Core Services
```python
# Primary Services
from src.services.ai_service import AIService
from src.services.unified_messaging_service import UnifiedMessagingService
from src.services.coordinator import Coordinator
from src.services.contract_service import ContractService
from src.services.verification_service import VerificationService

# Analytics Services
from src.services.performance_analyzer import PerformanceAnalyzer
from src.services.portfolio_service import PortfolioService
from src.services.recommendation_engine import RecommendationEngine
```

#### Specialized Services
```python
# Risk Analytics
from src.services.risk_analytics.risk_calculator_service import RiskCalculatorService
from src.services.risk_analytics.risk_websocket_server import RiskWebSocketServer
from src.services.risk_analytics.risk_api_endpoints import RiskApiEndpoints

# Messaging Services
from src.services.messaging_infrastructure import ConsolidatedMessagingService
from src.services.messaging_cli import MessagingCLI
from src.services.messaging_discord import DiscordMessagingService

# Vector Services
from src.services.vector.vector_database_service import VectorDatabaseService
from src.services.vector_database_service_unified import UnifiedVectorDatabaseService
```

#### Service Integration Patterns
```python
# Service ↔ Service Dependencies
from src.services.thea_client import TheaClient
from src.services.chatgpt.chatgpt_service import ChatGPTService
from src.services.vector_database import VectorDatabase

# Service ↔ Core Integration
from src.core.base.base_service import BaseService
from src.core.messaging_core import UnifiedMessagingCore
from src.core.coordination.coordinator_interfaces import ICoordinator
```

### CLI Integration
```python
# CLI Handlers
from src.services.messaging_cli_handlers import MessagingCLIHandlers
from src.services.unified_cli_handlers import UnifiedCLIHandlers
from src.services.messaging_cli_parser import MessagingCLIParser
```

### Related Files & Dependencies
- **Documentation**: `docs/messaging-contracts.mdc`, `docs/architecture/AI_SYSTEM_ARCHITECTURE.md`
- **CLI Interface**: `src/services/messaging_cli.py`
- **Web Integration**: `src/web/fastapi_app.py`
- **Core Dependencies**: `src/core/base/base_service.py`

---

## 🏗️ Core Module Hierarchy (`src/core/`)

### Directory Structure
```
src/core/
├── base/
│   └── base_service.py
├── analytics/ [see above]
├── messaging/
│   ├── messaging_core.py
│   ├── messaging_models.py
│   ├── messaging_protocol_models.py
│   ├── messaging_validation.py
│   └── messaging_*.py [20+ files]
├── coordination/
│   ├── coordinator_interfaces.py
│   ├── coordinator_models.py
│   └── coordinator_registry.py
├── config/
├── deployment/
├── engines/
├── error_handling/
├── health_check.py
├── managers/
├── message_queue/
├── orchestration/
├── pattern_analysis/
├── performance/
├── safety/
├── shared_utilities/
├── ssot/
├── utilities/
├── validation/
└── [40+ additional core modules]
```

### Common Import Patterns

#### Base Infrastructure
```python
# Base Classes
from src.core.base.base_service import BaseService
from src.core.unified_service_base import UnifiedServiceBase

# Configuration
from src.core.unified_config import UnifiedConfig
from src.core.config.config_ssot import SSOTConfig
```

#### Messaging Core
```python
# Primary Messaging
from src.core.messaging_core import UnifiedMessagingCore
from src.core.messaging_models import UnifiedMessage, UnifiedMessagePriority
from src.core.messaging_protocol_models import IMessageDelivery

# Messaging Components
from src.core.messaging_validation import MessageValidator
from src.core.messaging_template_resolution import TemplateResolver
from src.core.messaging_delivery_orchestration import DeliveryOrchestrator
```

#### Coordination System
```python
# Coordinator Interfaces
from src.core.coordination.coordinator_interfaces import ICoordinator
from src.core.coordination.coordinator_models import CoordinationModel
from src.core.coordination.coordinator_registry import CoordinatorRegistry

# Coordination Services
from src.core.messaging_coordinate_routing import CoordinateRoutingService
from src.core.coordinate_loader import CoordinateLoader
```

#### Analytics & Intelligence
```python
# Pattern Analysis
from src.core.pattern_analysis.pattern_analysis_orchestrator import PatternAnalysisOrchestrator
from src.core.vector_integration_analytics import VectorIntegrationAnalytics

# Strategic Oversight
from src.core.vector_strategic_oversight.unified_strategic_oversight.analyzers.prediction_analyzer import PredictionAnalyzer
```

#### Utilities & Shared Components
```python
# Shared Utilities
from src.core.shared_utilities import SharedUtilities
from src.core.utilities.validation_utilities import ValidationUtilities
from src.core.utilities.processing_utilities import ProcessingUtilities

# Error Handling
from src.core.error_handling.error_handler import ErrorHandler
from src.core.self_healing_system import SelfHealingSystem
```

### Message Queue System
```python
# Message Queue Core
from src.core.message_queue.message_queue_impl import MessageQueueImpl
from src.core.message_queue.message_queue_interfaces import IMessageQueue
from src.core.message_queue.message_queue_processor import MessageQueueProcessor

# Queue Components
from src.core.message_queue.message_queue_persistence import MessageQueuePersistence
from src.core.message_queue.message_queue_statistics import MessageQueueStatistics
```

### Related Files & Dependencies
- **Documentation**: `docs/architecture/`, `docs/SSOT/`
- **Web Integration**: `src/web/fastapi_app.py`
- **Service Integration**: `src/services/` (all services depend on core)
- **Configuration**: `src/core/config/`

---

## 🔄 Cross-Module Integration Patterns

### Analytics ↔ Services ↔ Core
```python
# Analytics consuming Services
from src.core.analytics.engines.metrics_engine import MetricsEngine
from src.services.performance_analyzer import PerformanceAnalyzer
from src.core.shared_utilities import SharedUtilities

# Services using Core + Analytics
from src.services.unified_messaging_service import UnifiedMessagingService
from src.core.messaging_core import UnifiedMessagingCore
from src.core.analytics.intelligence.pattern_analysis_engine import PatternAnalysisEngine

# Core orchestrating Services + Analytics
from src.core.orchestration.orchestrator import SystemOrchestrator
from src.services.coordinator import Coordinator
from src.core.analytics.orchestrators.coordination_analytics_orchestrator import CoordinationAnalyticsOrchestrator
```

### Import Path Resolution Hierarchy
1. **Local imports**: `from .submodule import Class`
2. **Parent imports**: `from ..parent_module import Class`
3. **Absolute imports**: `from src.module.submodule import Class`
4. **Service imports**: `from src.services.service_name import ServiceClass`
5. **Core imports**: `from src.core.module_name import CoreClass`

### Dependency Injection Patterns
```python
# Constructor Injection
class AnalyticsService:
    def __init__(self, messaging_service, config_service):
        self.messaging = messaging_service
        self.config = config_service

# Factory Pattern
from src.core.analytics.engines.metrics_engine import MetricsEngine
from src.services.performance_analyzer import PerformanceAnalyzer

def create_analytics_orchestrator():
    metrics_engine = MetricsEngine()
    performance_analyzer = PerformanceAnalyzer()
    return AnalyticsOrchestrator(metrics_engine, performance_analyzer)
```

---

## 📚 Documentation Cross-References

### Architecture Documentation
- `docs/architecture/AI_SYSTEM_ARCHITECTURE.md`
- `docs/architecture/MESSAGING_ARCHITECTURE.md`
- `docs/analytics/architecture_overview.md`
- `docs/SSOT/SSOT_VALIDATION_MILESTONE_COMPLETION.md`

### API Endpoints
- Messaging API: `src/services/messaging/messaging_rest_api.py`
- Risk Analytics: `src/services/risk_analytics/risk_api_endpoints.py`
- Vector Database: `src/services/vector/vector_database_service.py`

### CLI Tools
- Messaging CLI: `src/services/messaging_cli.py`
- Analytics CLI: `tools/analytics_ecosystem_health_scorer.py`
- Core CLI: `src/cli/`

---

## 🔍 Navigation Tips

### Finding Related Components
1. **Start with the domain**: analytics → `src/core/analytics/`
2. **Check service layer**: services → `src/services/`
3. **Look at core infrastructure**: core → `src/core/`
4. **Follow the imports**: Use the patterns above to navigate dependencies

### Common File Patterns
- `*engine.py`: Processing components
- `*service.py`: Service layer implementations
- `*orchestrator.py`: Coordination components
- `*coordinator.py`: Coordination interfaces
- `*models.py`: Data models and interfaces
- `*utilities.py`: Shared utility functions

### V2 Compliance Navigation
- All modules follow `<400 lines` rule
- Service Layer Pattern applied throughout
- SSOT domains clearly marked in file headers
- Navigation references included in docstrings

---

*Author: Agent-8 (Module Discovery Specialist)*
*Last Updated: 2026-01-07*
*V2 Compliance: Comprehensive reference guide*