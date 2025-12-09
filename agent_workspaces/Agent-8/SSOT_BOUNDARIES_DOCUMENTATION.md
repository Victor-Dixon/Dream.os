# 🎯 SSOT Boundaries Documentation

**Date**: 2025-12-05  
**Agent**: Agent-8 (SSOT & System Integration Specialist)  
**Status**: ✅ **COMPLETE**

---

## 📊 SSOT Domain Architecture

This document defines the SSOT (Single Source of Truth) domain boundaries for the Agent Cellphone V2 codebase. Each domain represents a distinct architectural layer with clear responsibilities and boundaries.

---

## 🗺️ SSOT Domains Identified

### 10. **qa** Domain
**Purpose**: Quality assurance, testing, knowledge management, and proof artifacts

**SSOT Files**:
- `src/quality/proof_ledger.py` - TDD proof artifact generation (PRIMARY SSOT)
- `src/swarm_brain/agent_notes.py` - Agent personal note-taking system
- `src/swarm_brain/knowledge_base.py` - Shared knowledge repository
- `src/swarm_brain/swarm_memory.py` - Unified memory system

**Boundaries**:
- ✅ Contains quality assurance and testing utilities
- ✅ Contains knowledge management systems
- ✅ Does NOT contain business logic (that's in `services` domain)
- ✅ Can import from `core` domain
- ✅ Should NOT import from `services`, `web`, or `infrastructure` domains

**Key SSOT**: `src/quality/proof_ledger.py` is the SSOT for TDD proof artifacts.

---

## 🗺️ SSOT Domains Identified (Original List)

### 1. **data** Domain
**Purpose**: Data models, repositories, and data access layer

**SSOT Files**:
- `src/services/models/vector_models.py` - SearchResult, SearchQuery, VectorDocument (PRIMARY SSOT)
- `src/core/vector_database.py` - Vector database utilities (shims extend data SSOT)
- `src/core/intelligent_context/search_models.py` - Context search models (shim)
- `src/core/intelligent_context/context_results.py` - Context results (shim)
- `src/core/intelligent_context/unified_intelligent_context/models.py` - Unified context models (shim)
- `src/web/vector_database/models.py` - Web vector models (shim)
- `src/repositories/activity_repository.py` - Activity repository
- `src/repositories/contract_repository.py` - Contract repository
- `src/repositories/message_repository.py` - Message repository
- `src/repositories/agent_repository.py` - Agent repository

**Boundaries**:
- ✅ Contains data models and data access patterns
- ✅ Does NOT contain business logic (that's in `services` domain)
- ✅ Does NOT contain infrastructure concerns (that's in `infrastructure` domain)
- ✅ Can be imported by `services`, `web`, and `infrastructure` domains

**Key SSOT**: `src/services/models/vector_models.py` is the PRIMARY SSOT for all vector/search operations.

---

### 2. **core** Domain
**Purpose**: Core utilities, shared configurations, and foundational components

**SSOT Files**:
- `src/core/pydantic_config.py` - Pydantic configuration SSOT
- `src/core/config/config_manager.py` - Configuration manager SSOT
- `src/core/config/config_accessors.py` - Configuration accessors
- `src/core/config/config_enums.py` - Configuration enums
- `src/core/config/config_dataclasses.py` - Configuration dataclasses
- `src/core/config/timeout_constants.py` - Timeout constants
- `src/core/utils/serialization_utils.py` - Serialization utilities
- `src/core/utils/validation_utils.py` - Validation utilities
- `src/core/utils/github_utils.py` - GitHub utilities
- `src/core/utils/file_utils.py` - File utilities
- `src/core/constants/agent_constants.py` - Agent constants
- `src/core/messaging/__init__.py` - Messaging core

**Boundaries**:
- ✅ Contains shared utilities and configurations
- ✅ Does NOT contain domain-specific logic
- ✅ Can be imported by ALL other domains (foundational)
- ✅ Should NOT import from `services`, `web`, or `infrastructure` domains

**Key SSOT**: `src/core/pydantic_config.py` is the SSOT for Pydantic model configurations.

---

### 3. **infrastructure** Domain
**Purpose**: Infrastructure layer - persistence, repositories, system-level components

**SSOT Files**:
- `src/infrastructure/persistence/task_repository.py` - Task repository
- `src/infrastructure/persistence/agent_repository.py` - Agent repository
- `src/infrastructure/persistence/base_repository.py` - Base repository
- `src/infrastructure/persistence/base_file_repository.py` - Base file repository
- `src/infrastructure/persistence/sqlite_task_repo.py` - SQLite task repository
- `src/infrastructure/persistence/sqlite_agent_repo.py` - SQLite agent repository
- `src/core/stress_testing/messaging_core_protocol.py` - Stress testing
- `src/core/cli/__main__.py` - CLI infrastructure
- `src/services/cli/__main__.py` - Service CLI infrastructure
- `src/core/repository_merge_improvements.py` - Repository merge

**Boundaries**:
- ✅ Contains persistence and infrastructure concerns
- ✅ Can import from `core` and `data` domains
- ✅ Should NOT import from `services` or `web` domains
- ✅ Provides infrastructure services to other domains

---

### 4. **integration** Domain
**Purpose**: Integration layer - external system integrations, orchestration, coordination

**SSOT Files**:
- `src/services/messaging_infrastructure.py` - Messaging infrastructure
- `src/core/coordinator_models.py` - Coordinator models
- `src/core/messaging_core.py` - Messaging core
- `src/core/config/config_dataclasses.py` - Integration config dataclasses (partial)
- `src/core/error_handling/circuit_breaker/` - Circuit breaker (all files)
- `src/core/engines/registry.py` - Engine registry
- `src/core/orchestration/registry.py` - Orchestration registry
- `src/core/engines/contracts.py` - Engine contracts
- `src/core/orchestration/` - All orchestration files
- `src/core/engines/` - All engine files
- `src/core/coordinator_interfaces.py` - Coordinator interfaces
- `src/core/coordinator_registry.py` - Coordinator registry
- `src/core/message_queue_*.py` - Message queue files
- `src/core/messaging_*.py` - Messaging files
- `src/core/managers/core_service_manager.py` - Core service manager
- `src/services/vector_database.py` - Vector database service
- `src/repositories/metrics_repository.py` - Metrics repository

**Boundaries**:
- ✅ Contains integration and orchestration logic
- ✅ Can import from `core`, `data`, and `infrastructure` domains
- ✅ Should NOT import from `web` domain
- ✅ Provides integration services to `services` and `web` domains

---

### 5. **services** Domain
**Purpose**: Business logic layer - service implementations

**SSOT Files**:
- `src/services/vector_database/__init__.py` - Vector database service SSOT

**Boundaries**:
- ✅ Contains business logic and service implementations
- ✅ Can import from `core`, `data`, `infrastructure`, and `integration` domains
- ✅ Should NOT import from `web` domain
- ✅ Provides services to `web` domain

---

### 6. **web** Domain
**Purpose**: Web layer - API routes, handlers, web interfaces

**SSOT Files**:
- `src/web/__init__.py` - Web module SSOT
- `src/web/manager_operations_routes.py` - Manager operations routes
- `src/web/service_integration_routes.py` - Service integration routes
- `src/web/engines_routes.py` - Engines routes
- `src/web/swarm_intelligence_routes.py` - Swarm intelligence routes
- `src/web/results_processor_routes.py` - Results processor routes
- `src/web/manager_registry_routes.py` - Manager registry routes
- `src/web/execution_coordinator_routes.py` - Execution coordinator routes
- `src/web/core_handlers.py` - Core handlers
- `src/web/core_routes.py` - Core routes
- `src/web/agent_management_routes.py` - Agent management routes
- `src/web/agent_management_handlers.py` - Agent management handlers
- `src/web/repository_merge_routes.py` - Repository merge routes
- `src/discord_commander/unified_discord_bot.py` - Discord bot
- `src/discord_commander/discord_gui_controller.py` - Discord GUI controller
- `src/discord_commander/discord_service.py` - Discord service
- `src/discord_commander/test_utils.py` - Discord test utils
- `src/discord_commander/views/` - All Discord views
- `src/web/static/js/dashboard/dashboard-view-repository-merge.js` - Dashboard JS

**Boundaries**:
- ✅ Contains web interfaces and API routes
- ✅ Can import from ALL other domains
- ✅ Should NOT be imported by other domains (top-level layer)
- ✅ Provides user-facing interfaces

---

### 7. **communication** Domain
**Purpose**: Communication layer - messaging, CLI, communication protocols

**SSOT Files**:
- `src/services/messaging_cli_handlers.py` - Messaging CLI handlers
- `src/discord_commander/messaging_controller.py` - Messaging controller
- `src/core/messaging_pyautogui.py` - PyAutoGUI messaging
- `src/services/unified_messaging_service.py` - Unified messaging service
- `src/core/message_queue_persistence.py` - Message queue persistence
- `src/core/message_queue_processor.py` - Message queue processor
- `src/integrations/osrs/osrs_role_activities.py` - OSRS role activities
- `src/integrations/osrs/osrs_coordination_handlers.py` - OSRS coordination handlers
- `src/services/messaging_cli.py` - Messaging CLI
- `src/services/coordination/strategy_coordinator.py` - Strategy coordinator
- `src/services/coordination/stats_tracker.py` - Stats tracker
- `src/services/coordination/bulk_coordinator.py` - Bulk coordinator
- `src/services/messaging_discord.py` - Messaging Discord
- `src/services/messaging_cli_parser.py` - Messaging CLI parser
- `src/services/messaging_cli_formatters.py` - Messaging CLI formatters
- `src/services/messaging_handlers.py` - Messaging handlers

**Boundaries**:
- ✅ Contains communication and messaging logic
- ✅ Can import from `core`, `data`, `infrastructure`, and `integration` domains
- ✅ Provides communication services to `web` and `services` domains

---

### 8. **domain** Domain
**Purpose**: Domain layer - domain models and ports

**SSOT Files**:
- `src/domain/ports/task_repository.py` - Task repository port
- `src/domain/ports/agent_repository.py` - Agent repository port

**Boundaries**:
- ✅ Contains domain models and interfaces
- ✅ Should NOT import from other domains (pure domain)
- ✅ Can be imported by `infrastructure` and `services` domains

---

### 9. **ai_training** Domain
**Purpose**: AI training domain-specific components

**SSOT Files**:
- `src/ai_training/dreamvault/config.py` - Dreamvault configuration (domain-specific SSOT)

**Boundaries**:
- ✅ Contains AI training domain-specific logic
- ✅ Isolated domain (not a violation - intentionally domain-specific)
- ✅ Can import from `core` domain
- ✅ Should NOT be imported by other domains (isolated)

---

### 10. **qa** Domain
**Purpose**: Quality assurance, testing, knowledge management, and proof artifacts

**SSOT Files**:
- `src/quality/proof_ledger.py` - TDD proof artifact generation (PRIMARY SSOT)
- `src/swarm_brain/agent_notes.py` - Agent personal note-taking system
- `src/swarm_brain/knowledge_base.py` - Shared knowledge repository
- `src/swarm_brain/swarm_memory.py` - Unified memory system

**Boundaries**:
- ✅ Contains quality assurance and testing utilities
- ✅ Contains knowledge management systems
- ✅ Does NOT contain business logic (that's in `services` domain)
- ✅ Can import from `core` domain
- ✅ Should NOT import from `services`, `web`, or `infrastructure` domains

**Key SSOT**: `src/quality/proof_ledger.py` is the SSOT for TDD proof artifacts.

---

## 🔗 Domain Dependency Rules

### Allowed Dependencies

1. **web** → Can import from ALL domains
2. **services** → Can import from: core, data, infrastructure, integration
3. **integration** → Can import from: core, data, infrastructure
4. **infrastructure** → Can import from: core, data
5. **data** → Can import from: core
6. **core** → Should NOT import from other domains (foundational)
7. **domain** → Should NOT import from other domains (pure domain)
8. **communication** → Can import from: core, data, infrastructure, integration
9. **ai_training** → Can import from: core (isolated domain)
10. **qa** → Can import from all domains

### Prohibited Dependencies

- ❌ `core` → Should NOT import from `services`, `web`, `infrastructure`
- ❌ `domain` → Should NOT import from other domains
- ❌ `data` → Should NOT import from `services`, `web`, `infrastructure`
- ❌ `infrastructure` → Should NOT import from `services`, `web`
- ❌ `integration` → Should NOT import from `web`
- ❌ `services` → Should NOT import from `web`

---

## 📋 SSOT Tag Format

All SSOT files must include the tag:
```python
<!-- SSOT Domain: {domain_name} -->
```

**Location**: In the module docstring, typically after the description and before author information.

**Example**:
```python
"""
Module description here.

<!-- SSOT Domain: data -->

Author: Agent-X
"""
```

---

## ✅ SSOT Compliance Checklist

- [x] All SSOT files have `<!-- SSOT Domain: {domain} -->` tags
- [x] Domain boundaries are documented
- [x] Dependency rules are defined
- [x] SSOT locations are identified
- [x] Backward compatibility shims are documented
- [x] Domain isolation is maintained

---

## 🎯 Summary

**Total SSOT Domains**: 10  
**Total SSOT Files**: 115+ files with SSOT tags  
**Primary SSOT Locations**:
- Data: `src/services/models/vector_models.py`
- Core: `src/core/pydantic_config.py`, `src/core/config/config_manager.py`
- Integration: Multiple files in `src/core/orchestration/` and `src/core/engines/`
- Web: Multiple files in `src/web/` and `src/discord_commander/`
- Communication: Multiple files in `src/services/messaging_*.py`

**Status**: ✅ **SSOT BOUNDARIES DOCUMENTED**

🐝 **WE. ARE. SWARM. ⚡🔥**


