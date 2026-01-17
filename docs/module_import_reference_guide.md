# Module Import Path Reference Guide

## Overview

This guide documents the complex module hierarchies and import patterns for the analytics, services, and core modules in the Agent Cellphone V2 system.

## Table of Contents

1. [Core Modules](#core-modules)
2. [Analytics Modules](#analytics-modules)
3. [Services Modules](#services-modules)
4. [Import Patterns](#import-patterns)
5. [Dependency Chains](#dependency-chains)

## Core Modules

The `src/core/` directory contains the foundational components with extensive sub-modules:

### Main Core Categories

#### Analytics Integration (`src/core/analytics/`)
```python
# Coordinators
from src.core.analytics.coordinators.analytics_coordinator import AnalyticsCoordinator
from src.core.analytics.coordinators.processing_coordinator import ProcessingCoordinator

# Engines
from src.core.analytics.engines.batch_analytics_engine import BatchAnalyticsEngine
from src.core.analytics.engines.realtime_analytics_engine import RealtimeAnalyticsEngine
from src.core.analytics.engines.metrics_engine import MetricsEngine

# Intelligence Layer
from src.core.analytics.intelligence.business_intelligence_engine import BusinessIntelligenceEngine
from src.core.analytics.intelligence.anomaly_detection_engine import AnomalyDetectionEngine
from src.core.analytics.intelligence.pattern_analysis_engine import PatternAnalysisEngine

# Pattern Analysis Sub-modules
from src.core.analytics.intelligence.pattern_analysis.anomaly_detector import AnomalyDetector
from src.core.analytics.intelligence.pattern_analysis.pattern_extractor import PatternExtractor
from src.core.analytics.intelligence.pattern_analysis.trend_analyzer import TrendAnalyzer

# Models
from src.core.analytics.models.coordination_analytics_models import CoordinationAnalyticsModels

# Orchestrators
from src.core.analytics.orchestrators.coordination_analytics_orchestrator import CoordinationAnalyticsOrchestrator

# Prediction Layer
from src.core.analytics.prediction.base_analyzer import BaseAnalyzer

# Processors
from src.core.analytics.processors.insight_processor import InsightProcessor
from src.core.analytics.processors.prediction_processor import PredictionProcessor
from src.core.analytics.processors.prediction.prediction_analyzer import PredictionAnalyzer
from src.core.analytics.processors.prediction.prediction_calculator import PredictionCalculator
```

#### Messaging System (`src/core/messaging/`)
```python
from src.core.messaging.messaging_models import UnifiedMessage, MessagePriority
from src.core.messaging.messaging_models_core import CoreMessageModels
from src.core.messaging.messaging_pyautogui import PyAutoGUIMessaging
from src.core.messaging.messaging_delivery_orchestration import DeliveryOrchestrator
from src.core.messaging.messaging_history import MessageHistory
from src.core.messaging.messaging_templates_data import TemplateData
```

#### Coordination (`src/core/coordination/`)
```python
from src.core.coordination.coordinator_interfaces import CoordinatorInterface
from src.core.coordination.coordinator_models import CoordinationModels
from src.core.coordination.coordinator_registry import CoordinatorRegistry
```

#### Configuration (`src/core/config/`)
```python
from src.core.config.config_browser import ConfigBrowser
from src.core.config.config_thresholds import ConfigThresholds
```

#### Infrastructure (`src/core/infrastructure/`)
```python
from src.core.infrastructure.health_check import HealthChecker
from src.core.infrastructure.load_balancing import LoadBalancer
```

#### Performance (`src/core/performance/`)
```python
from src.core.performance.metrics import PerformanceMetrics
from src.core.performance.monitoring import PerformanceMonitor
```

## Analytics Modules

The analytics modules are primarily located in `src/core/analytics/` with a hierarchical structure:

### Analytics Hierarchy Map

```
src/core/analytics/
├── coordinators/
│   ├── analytics_coordinator.py
│   └── processing_coordinator.py
├── engines/
│   ├── batch_analytics_engine.py
│   ├── realtime_analytics_engine.py
│   ├── metrics_engine.py
│   └── coordination_analytics_engine.py
├── intelligence/
│   ├── business_intelligence_engine*.py
│   ├── anomaly_detection_engine.py
│   ├── pattern_analysis_engine.py
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
        └── prediction_calculator.py
```

### Key Analytics Import Patterns

```python
# Business Intelligence Stack
from src.core.analytics.intelligence import (
    BusinessIntelligenceEngine,
    AnomalyDetectionEngine,
    PatternAnalysisEngine
)

# Analytics Engines
from src.core.analytics.engines import (
    BatchAnalyticsEngine,
    RealtimeAnalyticsEngine,
    MetricsEngine
)

# Pattern Analysis Suite
from src.core.analytics.intelligence.pattern_analysis import (
    AnomalyDetector,
    PatternExtractor,
    TrendAnalyzer
)
```

## Services Modules

The `src/services/` directory contains business logic and external integrations:

### Services Hierarchy Map

```
src/services/
├── messaging/
│   ├── cli/
│   ├── handlers/
│   └── models/
├── coordination/
├── onboarding/
├── vector/
├── ai_context_engine/
├── contract_system/
├── risk_analytics/
├── swarm_intelligence_manager/
└── [250+ additional service modules]
```

### Critical Services Import Patterns

```python
# Messaging Services
from src.services.messaging.messaging_cli import MessagingCLI
from src.services.messaging.handlers.message_handlers import MessageHandlers
from src.services.messaging.models.message_models import MessageModels

# AI Context Engine
from src.services.ai_context_engine.context_processor import ContextProcessor
from src.services.ai_context_engine.websocket_handler import WebSocketHandler

# Vector Database Services
from src.services.vector.vector_database_service import VectorDatabaseService
from src.services.vector_database.vector_database import VectorDatabase

# Contract System
from src.services.contract_system.contract_manager import ContractManager
from src.services.contract_service import ContractService

# Coordination Services
from src.services.coordination.coordinator import Coordinator
from src.services.coordinator import Coordinator

# Onboarding Services
from src.services.onboarding.onboarding_service import OnboardingService
from src.services.onboarding.soft.onboarding_templates import OnboardingTemplates

# Risk Analytics
from src.services.risk_analytics.risk_analyzer import RiskAnalyzer
from src.services.risk_analytics.portfolio_risk import PortfolioRisk

# Swarm Intelligence
from src.services.swarm_intelligence_manager.swarm_manager import SwarmManager
```

## Import Patterns

### Relative vs Absolute Imports

```python
# Absolute imports (recommended)
from src.core.analytics.intelligence.business_intelligence_engine import BusinessIntelligenceEngine
from src.services.messaging.messaging_models import MessagingModels

# Relative imports (within same package)
from .analytics_coordinator import AnalyticsCoordinator
from ..engines.metrics_engine import MetricsEngine
```

### Common Import Anti-patterns to Avoid

```python
# ❌ Avoid wildcard imports in production code
from src.core.analytics import *

# ❌ Avoid deep nested imports in single line
from src.core.analytics.intelligence.pattern_analysis.anomaly_detector import AnomalyDetector

# ✅ Use multi-line imports for clarity
from src.core.analytics.intelligence.pattern_analysis import (
    AnomalyDetector,
    PatternExtractor,
    TrendAnalyzer
)
```

### Factory Pattern Imports

```python
# Service factories
from src.services.unified_service_managers import ServiceManagerFactory
from src.core.unified_service_base import UnifiedServiceBase

# Coordinator factories
from src.core.coordination.coordinator_registry import CoordinatorRegistry
```

## Dependency Chains

### Analytics → Services → Core Chain

```python
# Analytics depends on Services for data
from src.services.vector_database_service_unified import UnifiedVectorService
from src.core.vector_database import VectorDatabase

# Services depend on Core for infrastructure
from src.core.infrastructure.health_check import HealthChecker
from src.core.messaging.messaging_models import MessageModels

# Core provides base functionality
from src.core.service_base import ServiceBase
from src.core.unified_service_base import UnifiedServiceBase
```

### Circular Dependency Prevention

```python
# ✅ Good: Core doesn't depend on Services
# src/core/analytics/engines/metrics_engine.py
from src.core.performance.metrics import CoreMetrics

# ❌ Bad: Would create circular dependency
# src/core/performance/metrics.py
# from src.services.performance_analyzer import PerformanceAnalyzer  # DON'T DO THIS
```

### Layer Boundaries

```
┌─────────────────┐
│   Analytics     │ ← Uses Services & Core
├─────────────────┤
│   Services      │ ← Uses Core only
├─────────────────┤
│     Core        │ ← No dependencies on upper layers
└─────────────────┘
```

## Cross-Module Dependencies

### Analytics ↔ Services Integration

```python
# Analytics using Service data
from src.services.ai_analytics_integration import AIAnalyticsIntegration
from src.services.vector_database import VectorDatabaseService

# Services using Analytics insights
from src.core.analytics.intelligence.business_intelligence_engine import BusinessIntelligenceEngine
```

### Core ↔ External Systems

```python
# Database integrations
from src.core.vector_database import VectorDatabase
from src.services.vector_database_service_unified import UnifiedVectorService

# Messaging integrations
from src.core.messaging.messaging_pyautogui import PyAutoGUIMessaging
from src.services.messaging_cli import MessagingCLI
```

## Best Practices

### 1. Import Organization

```python
# Standard library imports
import os
import sys
from typing import List, Dict, Optional

# Third-party imports
import requests
import pandas as pd

# Local imports - absolute paths preferred
from src.core.config.config_browser import ConfigBrowser
from src.services.contract_service import ContractService
```

### 2. Import Aliases for Complex Paths

```python
# Use aliases for long import paths
from src.core.analytics.intelligence.pattern_analysis import (
    AnomalyDetector as AD,
    PatternExtractor as PE
)

# Or import the module
from src.core.analytics.intelligence import pattern_analysis as pa
detector = pa.AnomalyDetector()
```

### 3. Lazy Imports for Optional Dependencies

```python
# Use lazy imports to avoid circular dependencies
def get_analytics_engine():
    from src.core.analytics.engines.realtime_analytics_engine import RealtimeAnalyticsEngine
    return RealtimeAnalyticsEngine()
```

## Troubleshooting Import Issues

### Common Problems

1. **Circular Imports**: Restructure to use dependency injection
2. **Missing __init__.py**: Ensure all directories have `__init__.py` files
3. **Path Resolution**: Use absolute imports from `src/` root
4. **Module Not Found**: Check PYTHONPATH includes project root

### Debugging Commands

```bash
# Check module structure
python -c "import src.core.analytics; print(dir(src.core.analytics))"

# Validate imports
python -c "from src.core.analytics.intelligence.business_intelligence_engine import BusinessIntelligenceEngine; print('Import successful')"

# Check PYTHONPATH
python -c "import sys; print('\\n'.join(sys.path))"
```

---

*This guide was generated for Agent-5 (Business Intelligence) on 2026-01-16 to document complex module hierarchies and import patterns across the analytics, services, and core modules.*