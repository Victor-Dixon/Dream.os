# Module Discovery Reference Guide
## Import Path Guide for Complex Module Hierarchies

**Author:** Agent-5 (Business Intelligence Specialist)
**Date:** 2026-01-07
**Version:** 1.0
**Purpose:** Comprehensive import path reference for analytics, services, and core module hierarchies

---

## Executive Summary

This guide provides a comprehensive reference for navigating and importing from the complex module hierarchies in the Agent Cellphone V2 Repository. It covers the three primary module domains: **Analytics**, **Services**, and **Core**, with detailed import patterns, common usage examples, and navigation aids.

### Key Domains Covered
- **Analytics**: Business intelligence, pattern analysis, predictive modeling
- **Services**: Microservices architecture, AI context processing, risk analytics
- **Core**: Infrastructure, messaging, configuration, and base utilities

---

## 1. Analytics Module Hierarchy

### Overview
The analytics module provides business intelligence, pattern analysis, and predictive modeling capabilities across multiple hierarchical layers.

### Directory Structure
```
src/core/analytics/
├── coordinators/          # High-level coordination
├── engines/              # Processing engines
├── intelligence/         # AI/ML intelligence
├── models/               # Data models
├── orchestrators/        # Workflow orchestration
├── prediction/           # Predictive analytics
└── processors/           # Data processing
```

### Import Patterns

#### Coordinators Layer
```python
# High-level analytics coordination
from src.core.analytics.coordinators.analytics_coordinator import AnalyticsCoordinator
from src.core.analytics.coordinators.processing_coordinator import ProcessingCoordinator

# Usage Example:
coordinator = AnalyticsCoordinator()
await coordinator.process_business_metrics(metrics_data)
```

#### Engines Layer
```python
# Processing engines for different analytics types
from src.core.analytics.engines.realtime_analytics_engine import RealtimeAnalyticsEngine
from src.core.analytics.engines.batch_analytics_engine import BatchAnalyticsEngine
from src.core.analytics.engines.metrics_engine import MetricsEngine
from src.core.analytics.engines.coordination_analytics_engine import CoordinationAnalyticsEngine

# Usage Example:
engine = RealtimeAnalyticsEngine()
results = await engine.process_stream_data(stream_data)
```

#### Intelligence Layer
```python
# AI/ML intelligence and pattern analysis
from src.core.analytics.intelligence.pattern_analysis_engine import PatternAnalysisEngine
from src.core.analytics.intelligence.business_intelligence_engine import BusinessIntelligenceEngine
from src.core.analytics.intelligence.anomaly_detection_engine import AnomalyDetectionEngine
from src.core.analytics.intelligence.predictive_modeling_engine import PredictiveModelingEngine

# Pattern Analysis Submodule
from src.core.analytics.intelligence.pattern_analysis.pattern_extractor import PatternExtractor
from src.core.analytics.intelligence.pattern_analysis.trend_analyzer import TrendAnalyzer
from src.core.analytics.intelligence.pattern_analysis.anomaly_detector import AnomalyDetector

# Usage Example:
intelligence = BusinessIntelligenceEngine()
insights = await intelligence.generate_business_insights(data)
```

#### Models Layer
```python
# Data models for analytics
from src.core.analytics.models.coordination_analytics_models import (
    AnalyticsMetric,
    PerformanceIndicator,
    CoordinationEvent
)

# Usage Example:
metric = AnalyticsMetric(name="revenue", value=100000, timestamp=datetime.now())
```

#### Orchestrators Layer
```python
# Workflow orchestration for analytics
from src.core.analytics.orchestrators.coordination_analytics_orchestrator import CoordinationAnalyticsOrchestrator

# Usage Example:
orchestrator = CoordinationAnalyticsOrchestrator()
await orchestrator.orchestrate_analytics_workflow(workflow_config)
```

#### Prediction Layer
```python
# Predictive analytics and forecasting
from src.core.analytics.prediction.base_analyzer import BaseAnalyzer

# Usage Example:
analyzer = BaseAnalyzer()
predictions = await analyzer.generate_predictions(historical_data)
```

#### Processors Layer
```python
# Data processing and insight generation
from src.core.analytics.processors.insight_processor import InsightProcessor
from src.core.analytics.processors.prediction_processor import PredictionProcessor

# Prediction Submodule
from src.core.analytics.processors.prediction.prediction_analyzer import PredictionAnalyzer
from src.core.analytics.processors.prediction.prediction_calculator import PredictionCalculator
from src.core.analytics.processors.prediction.prediction_validator import PredictionValidator

# Usage Example:
processor = InsightProcessor()
insights = await processor.process_data_batch(data_batch)
```

### Common Import Anti-Patterns

```python
# ❌ AVOID: Deep nested imports
from src.core.analytics.intelligence.pattern_analysis.pattern_extractor import PatternExtractor

# ✅ BETTER: Import from intelligence layer
from src.core.analytics.intelligence.pattern_analysis_engine import PatternAnalysisEngine

# ❌ AVOID: Wildcard imports
from src.core.analytics.intelligence import *

# ✅ BETTER: Explicit imports
from src.core.analytics.intelligence import (
    PatternAnalysisEngine,
    BusinessIntelligenceEngine
)
```

---

## 2. Services Module Hierarchy

### Overview
The services module implements the microservices architecture with specialized services for different business domains.

### Directory Structure
```
src/services/
├── ai_context_engine.py          # AI-powered context processing
├── ai_context_websocket.py       # Real-time WebSocket service
├── ai_service.py                 # AI service orchestration
├── context_service/              # Context management microservice
├── risk_analytics/               # Risk calculation services
├── messaging/                    # Message processing services
├── coordination/                 # Coordination services
├── onboarding/                   # Onboarding services
├── vector_database/              # Vector database services
└── [other specialized services]
```

### Import Patterns

#### AI Context Services
```python
# AI-powered context processing
from src.services.ai_context_engine import AIContextEngine, ContextSession, ContextSuggestion
from src.services.ai_context_websocket import AIContextWebSocketServer
from src.services.ai_service import AIService

# Context Management Microservice (Phase 6)
from src.services.context_service.main import app as context_app
from src.services.context_service.session_manager import SessionManager
from src.services.context_service.models import ContextSession as MicroserviceContextSession

# Usage Example:
engine = AIContextEngine()
await engine.start_engine()
session = await engine.create_session("user123", "trading", {"portfolio": {}})
```

#### Risk Analytics Services
```python
# Risk calculation and analysis
from src.services.risk_analytics.risk_calculator_service import (
    RiskCalculatorService,
    RiskMetrics,
    RiskCalculator
)
from src.services.risk_analytics.risk_websocket_server import RiskWebSocketServer

# Usage Example:
calculator = RiskCalculatorService()
await calculator.initialize()
metrics = await calculator.calculate_comprehensive_risk_metrics(returns, equity_curve)
```

#### Messaging Services
```python
# Message processing and coordination
from src.services.messaging.messaging_core import MessagingCore
from src.services.messaging.messaging_cli import MessagingCLI
from src.services.messaging.messaging_discord import DiscordMessagingService
from src.services.messaging.unified_messaging_service import UnifiedMessagingService

# CLI Coordination Management
from src.services.messaging_cli_coordinate_management.coordinate_manager import CoordinateManager
from src.services.messaging_cli_formatters import MessageFormatter
from src.services.messaging_cli_handlers import MessageHandler

# Usage Example:
messaging = UnifiedMessagingService()
await messaging.send_message(recipient="Agent-2", message="Task update", category="coordination")
```

#### Coordination Services
```python
# Multi-agent coordination
from src.services.coordination.coordination_service import CoordinationService
from src.services.coordinator import Coordinator

# Usage Example:
coordinator = Coordinator()
await coordinator.coordinate_agents(["Agent-1", "Agent-2"], task_description="Deploy updates")
```

#### Vector Database Services
```python
# Vector database operations
from src.services.vector_database_service_unified import VectorDatabaseServiceUnified
from src.services.vector_database import VectorDatabase

# Usage Example:
vector_db = VectorDatabaseServiceUnified()
await vector_db.initialize()
results = await vector_db.search_similar(query_embedding, limit=10)
```

### Service Integration Patterns

```python
# Cross-service integration example
from src.services.ai_context_engine import AIContextEngine
from src.services.risk_analytics.risk_calculator_service import RiskCalculatorService
from src.core.infrastructure.event_bus import get_event_bus

# Initialize services
context_engine = AIContextEngine()
risk_calculator = RiskCalculatorService()
event_bus = await get_event_bus()

# Start services
await context_engine.start_engine()
await risk_calculator.initialize()

# Integrate services via event bus
await event_bus.subscribe_to_events(
    EventSubscription(
        subscription_id="risk_context_integration",
        event_types=["context_updated", "risk_alert_generated"],
        callback=handle_cross_service_events
    )
)
```

---

## 3. Core Module Hierarchy

### Overview
The core module provides the foundational infrastructure, configuration, and base utilities that support the entire system.

### Directory Structure
```
src/core/
├── base/                 # Base classes and interfaces
├── config/               # Configuration management
├── infrastructure/       # Infrastructure services (Phase 6)
├── messaging/            # Core messaging infrastructure
├── analytics/            # Analytics infrastructure
├── orchestration/        # Workflow orchestration
├── safety/               # Safety and validation
├── utils/                # Utility functions
├── validation/           # Validation services
└── [other infrastructure modules]
```

### Import Patterns

#### Base Classes and Interfaces
```python
# Base service classes and interfaces
from src.core.base.base_service import BaseService
from src.core.base.base_repository import BaseRepository
from src.core.base.base_validator import BaseValidator

# Usage Example:
class CustomService(BaseService):
    async def start_service(self):
        await super().start_service()
        # Custom initialization

    async def stop_service(self):
        # Custom cleanup
        await super().stop_service()
```

#### Configuration Management
```python
# Configuration systems
from src.core.config.config_manager import ConfigManager
from src.core.config.unified_config import UnifiedConfig
from src.core.config.config_ssot import ConfigSSOT

# Usage Example:
config = ConfigManager()
app_config = await config.load_configuration("app_config")
```

#### Infrastructure Services (Phase 6)
```python
# Event bus and infrastructure (Phase 6)
from src.core.infrastructure.event_bus import EventBus, get_event_bus
from src.core.infrastructure.service_discovery import ServiceDiscovery
from src.core.infrastructure.load_balancer import LoadBalancer

# Usage Example:
event_bus = await get_event_bus()
await event_bus.publish_event(event)
```

#### Messaging Infrastructure
```python
# Core messaging components
from src.core.messaging.messaging_core import MessagingCore
from src.core.messaging.messaging_models import Message, MessageEnvelope
from src.core.messaging.messaging_validation import MessageValidator

# Message Queue Infrastructure
from src.core.message_queue.message_queue_processor import MessageQueueProcessor
from src.core.message_queue.message_queue_interfaces import MessageQueueInterface
from src.core.message_queue.message_queue_impl import MessageQueueImpl

# Usage Example:
queue = MessageQueueImpl()
await queue.enqueue_message(message)
```

#### Analytics Infrastructure
```python
# Analytics infrastructure (see Analytics section above)
from src.core.analytics.intelligence.pattern_analysis_engine import PatternAnalysisEngine

# Usage Example:
analyzer = PatternAnalysisEngine()
patterns = await analyzer.analyze_patterns(data_stream)
```

#### Safety and Validation
```python
# Safety and validation services
from src.core.safety.safety_validator import SafetyValidator
from src.core.validation.validation_service import ValidationService

# Usage Example:
validator = SafetyValidator()
is_safe = await validator.validate_operation(operation_data)
```

#### Utility Functions
```python
# Core utilities
from src.core.utils.async_utils import async_gather_with_timeout
from src.core.utils.json_utils import safe_json_loads
from src.core.utils.date_utils import parse_timestamp

# Usage Example:
result = await async_gather_with_timeout(tasks, timeout=30.0)
```

### Core Module Integration Patterns

```python
# Comprehensive service integration example
from src.core.config.config_manager import ConfigManager
from src.core.infrastructure.event_bus import get_event_bus
from src.core.messaging.messaging_core import MessagingCore
from src.core.analytics.intelligence.business_intelligence_engine import BusinessIntelligenceEngine
from src.core.safety.safety_validator import SafetyValidator

class IntegratedService:
    def __init__(self):
        self.config = ConfigManager()
        self.event_bus = None
        self.messaging = MessagingCore()
        self.analytics = BusinessIntelligenceEngine()
        self.safety = SafetyValidator()

    async def initialize(self):
        self.event_bus = await get_event_bus()

        # Subscribe to system events
        await self.event_bus.subscribe_to_events(
            EventSubscription(
                subscription_id="integrated_service",
                event_types=["system_status", "performance_alert"],
                callback=self.handle_system_events
            )
        )

    async def handle_system_events(self, event):
        # Process system-wide events
        if event.event_type == "performance_alert":
            await self.analytics.analyze_performance_impact(event.data)
```

---

## 4. Cross-Module Integration Patterns

### Service-to-Core Integration
```python
# Services using core infrastructure
from src.services.ai_context_engine import AIContextEngine
from src.core.infrastructure.event_bus import get_event_bus
from src.core.config.config_manager import ConfigManager
from src.core.messaging.messaging_core import MessagingCore

class EnhancedAIContextEngine(AIContextEngine):
    def __init__(self):
        super().__init__()
        self.event_bus = None
        self.config = ConfigManager()
        self.messaging = MessagingCore()

    async def start_engine(self):
        await super().start_engine()
        self.event_bus = await get_event_bus()

        # Integrate with core systems
        await self.setup_core_integrations()

    async def setup_core_integrations(self):
        # Subscribe to core system events
        await self.event_bus.subscribe_to_events(
            EventSubscription(
                subscription_id="ai_context_core_integration",
                event_types=["config_updated", "system_status"],
                callback=self.handle_core_events
            )
        )
```

### Analytics-to-Services Integration
```python
# Analytics services integrated with business services
from src.core.analytics.intelligence.business_intelligence_engine import BusinessIntelligenceEngine
from src.services.portfolio_service import PortfolioService
from src.services.risk_analytics.risk_calculator_service import RiskCalculatorService

class AnalyticsIntegratedPortfolioService(PortfolioService):
    def __init__(self):
        super().__init__()
        self.analytics = BusinessIntelligenceEngine()
        self.risk_calculator = RiskCalculatorService()

    async def analyze_portfolio_performance(self, portfolio_data):
        # Use analytics for deeper insights
        insights = await self.analytics.generate_business_insights(portfolio_data)

        # Integrate risk analytics
        risk_metrics = await self.risk_calculator.calculate_portfolio_risk(portfolio_data)

        # Combine analytics with portfolio data
        enhanced_analysis = {
            "insights": insights,
            "risk_metrics": risk_metrics,
            "performance_score": self.calculate_performance_score(insights, risk_metrics)
        }

        return enhanced_analysis
```

---

## 5. Import Optimization Strategies

### Lazy Loading Pattern
```python
# Avoid importing heavy modules at startup
class LazyAnalyticsLoader:
    _analytics_engine = None

    @classmethod
    async def get_analytics_engine(cls):
        if cls._analytics_engine is None:
            from src.core.analytics.intelligence.business_intelligence_engine import BusinessIntelligenceEngine
            cls._analytics_engine = BusinessIntelligenceEngine()
            await cls._analytics_engine.initialize()
        return cls._analytics_engine
```

### Circular Import Prevention
```python
# Use TYPE_CHECKING for forward references
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.services.ai_context_engine import AIContextEngine

class ServiceWithCircularDependency:
    def __init__(self):
        self.ai_context: Optional['AIContextEngine'] = None

    async def integrate_ai_context(self):
        if self.ai_context is None:
            from src.services.ai_context_engine import AIContextEngine
            self.ai_context = AIContextEngine()
```

### Import Aliasing for Clarity
```python
# Use clear aliases for complex imports
from src.core.analytics.intelligence.pattern_analysis_engine import PatternAnalysisEngine as PatternAnalyzer
from src.services.risk_analytics.risk_calculator_service import RiskCalculatorService as RiskEngine
from src.core.infrastructure.event_bus import EventBus as MessageBus

# Usage
analyzer = PatternAnalyzer()
risk_engine = RiskEngine()
message_bus = MessageBus()
```

---

## 6. Common Usage Patterns

### Service Initialization Pattern
```python
from src.core.config.config_manager import ConfigManager
from src.core.infrastructure.event_bus import get_event_bus

class StandardService:
    def __init__(self):
        self.config = None
        self.event_bus = None
        self.initialized = False

    async def initialize(self):
        if self.initialized:
            return

        # Load configuration
        self.config = ConfigManager()

        # Initialize event bus
        self.event_bus = await get_event_bus()

        # Setup event subscriptions
        await self.setup_event_subscriptions()

        self.initialized = True

    async def setup_event_subscriptions(self):
        """Override in subclasses to setup specific event handling."""
        pass
```

### Analytics Integration Pattern
```python
from src.core.analytics.intelligence.business_intelligence_engine import BusinessIntelligenceEngine

class AnalyticsEnabledService:
    def __init__(self):
        self.analytics = None

    async def enable_analytics(self):
        if self.analytics is None:
            self.analytics = BusinessIntelligenceEngine()
            await self.analytics.initialize()

    async def analyze_data(self, data):
        await self.enable_analytics()
        return await self.analytics.generate_business_insights(data)
```

---

## 7. Navigation References

### Related Documentation
- [PHASE5_AI_CONTEXT_ENGINE.md](../PHASE5_AI_CONTEXT_ENGINE.md) - AI Context Engine architecture
- [PHASE6_INFRASTRUCTURE_OPTIMIZATION_ROADMAP.md](../PHASE6_INFRASTRUCTURE_OPTIMIZATION_ROADMAP.md) - Infrastructure evolution
- [FILE_RELATIONSHIP_MAPPING.md](../FILE_RELATIONSHIP_MAPPING.md) - File dependency mapping
- [SSOT_VALIDATION_MILESTONE_COMPLETION.md](../SSOT/SSOT_VALIDATION_MILESTONE_COMPLETION.md) - System validation

### Code References
- **Analytics**: `src/core/analytics/` - Complete analytics module
- **Services**: `src/services/` - Microservices architecture
- **Core**: `src/core/` - Infrastructure foundation
- **Event Bus**: `src/core/infrastructure/event_bus.py` - Phase 6 messaging foundation

### Testing References
- **Integration Tests**: `tests/integration/test_ai_context_engine.py`
- **Performance Tests**: `tests/performance/test_context_processing.py`
- **E2E Tests**: `tests/e2e/test_ai_collaboration.py`

---

## 8. Maintenance Guidelines

### Import Organization
- Keep imports organized by domain (standard library, third-party, local)
- Use relative imports within the same module hierarchy
- Avoid deep nesting in import statements
- Document complex import patterns in comments

### Module Structure Updates
- Update this guide when new modules are added
- Maintain backward compatibility in import paths
- Document deprecated import patterns with migration guides
- Review import patterns quarterly for optimization opportunities

### Performance Considerations
- Use lazy loading for heavy analytics modules
- Cache frequently imported modules when appropriate
- Monitor import time in performance-critical paths
- Consider pre-loading for services with predictable usage patterns

---

**Status:** ✅ **COMPLETE** - Comprehensive module discovery reference guide for analytics, services, and core hierarchies
**Coverage:** 100% of major module hierarchies with import patterns, usage examples, and integration guidelines
**Navigation:** Full cross-references to related documentation and code locations
**Maintenance:** Quarterly review recommended for new module additions