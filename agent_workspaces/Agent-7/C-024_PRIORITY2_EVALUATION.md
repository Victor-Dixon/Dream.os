# C-024 Web Domain Config Consolidation - Priority 2 Evaluation

**Agent**: Agent-7 (Web Development Specialist)  
**Date**: 2025-12-03  
**Status**: EVALUATION IN PROGRESS

---

## 📋 PRIORITY 2 OBJECTIVE

Evaluate moving `RetryConfig` and `CircuitBreakerConfig` from `error_config.py` (Web domain) to Infrastructure SSOT for cross-cutting infrastructure patterns.

---

## 🔍 CURRENT STATE ANALYSIS

### Current Location
- **File**: `src/core/error_handling/error_config.py`
- **Domain**: Web SSOT (Agent-7)
- **Status**: Priority 1 consolidation complete

### Duplicate Definitions Found

#### 1. `error_config.py` (Current SSOT after Priority 1)
```python
@dataclass
class RetryConfig:
    max_attempts: int = 3
    base_delay: float = 1.0
    backoff_factor: float = 2.0
    max_delay: float = 60.0
    jitter: bool = True
    exceptions: tuple = (Exception,)

@dataclass
class CircuitBreakerConfig:
    name: str
    failure_threshold: int = 5
    recovery_timeout: float = 60.0
```

#### 2. `error_models_core.py` (Enhanced version)
```python
@dataclass
class RetryConfig:
    max_attempts: int = 3
    base_delay: float = 1.0
    max_delay: float = 60.0
    strategy: RetryStrategy = RetryStrategy.EXPONENTIAL  # Additional
    backoff_multiplier: float = 2.0
    jitter: bool = True
    enabled: bool = True  # Additional
    metadata: dict[str, Any] = field(default_factory=dict)  # Additional
    # Has validation in __post_init__

@dataclass
class CircuitBreakerConfig:
    name: str
    failure_threshold: int = 5
    recovery_timeout: int = 60
    expected_exception: type[Exception] = Exception  # Additional
    success_threshold: int = 3  # Additional
    enabled: bool = True  # Additional
    metadata: dict[str, Any] = field(default_factory=dict)  # Additional
    # Has validation in __post_init__
```

#### 3. `circuit_breaker/core.py` (Simple class version)
```python
class CircuitBreakerConfig:
    def __init__(self, name: str, failure_threshold: int = 5, timeout_seconds: int = 60):
        self.name = name
        self.failure_threshold = failure_threshold
        self.timeout_seconds = timeout_seconds
```

#### 4. `error_decision_models.py` (RetryConfiguration - different name)
```python
@dataclass
class RetryConfiguration:
    max_retries: int = 3
    base_delay: float = 1.0
    max_delay: float = 60.0
    exponential_backoff: bool = True
    backoff_factor: float = 2.0
    retry_exceptions: tuple[type[Exception], ...] = ...
```

---

## 📊 USAGE ANALYSIS

### Current Imports
- `error_handling_core.py` - Exports from `error_config.py`
- `component_management.py` - Uses both configs
- `retry_mechanisms.py` - Uses `RetryConfig`
- `circuit_breaker.py` - Uses `CircuitBreakerConfig`
- `error_models_core.py` - Has duplicate definitions
- `circuit_breaker/core.py` - Has duplicate definition

### Domain Distribution
- **Error Handling Domain**: Multiple files using configs
- **Infrastructure Patterns**: Retry and circuit breaker are infrastructure-level
- **Cross-Cutting**: Used across multiple domains (not just web)

---

## 🎯 SSOT DOMAIN ASSESSMENT

### Current Domain: Web SSOT (Agent-7)
- **Rationale**: Configs are in `error_handling` which is part of core
- **Issue**: Retry/circuit breaker are infrastructure patterns, not web-specific

### Proposed Domain: Infrastructure SSOT (Agent-3)
- **Rationale**: 
  - Retry logic and circuit breakers are infrastructure-level patterns
  - Used across multiple domains (not web-specific)
  - Infrastructure SSOT handles DevOps, deployment, infrastructure configs
- **Location**: Should be in `src/core/infrastructure/` or similar

---

## ⚠️ COMPLEXITY ASSESSMENT

### Migration Complexity: **MEDIUM-HIGH**

#### Challenges:
1. **Multiple Duplicate Definitions**: 4 different versions exist
2. **Different APIs**: Some have more fields, validation, different types
3. **Cross-Domain Impact**: Used in error handling, retry mechanisms, circuit breakers
4. **Import Updates**: Need to update 6+ import locations
5. **Backward Compatibility**: Need to maintain compatibility during migration

#### Benefits:
1. **True SSOT**: Single source for infrastructure patterns
2. **Domain Alignment**: Infrastructure patterns in Infrastructure SSOT
3. **Consistency**: Unified config across all domains
4. **Maintainability**: One place to update infrastructure configs

---

## 📝 MIGRATION STRATEGY

### Phase 1: Consolidate Duplicates (HIGH PRIORITY)
1. Analyze differences between all 4 definitions
2. Create unified version with all necessary fields
3. Determine which features to keep (validation, metadata, etc.)
4. Consolidate into single definition

### Phase 2: Coordinate with Agent-3
1. Identify Infrastructure SSOT location
2. Confirm Agent-3 can own these configs
3. Plan migration path with Agent-3

### Phase 3: Migration Execution
1. Move configs to Infrastructure SSOT location
2. Update all imports (6+ files)
3. Remove duplicates
4. Verify no broken imports

### Phase 4: Validation
1. Run tests to verify functionality
2. Check all domains still work
3. Update documentation

---

## 🤝 COORDINATION REQUIRED

### Agent-3 (Infrastructure SSOT)
- **Action**: Confirm Infrastructure SSOT location for cross-cutting configs
- **Question**: Should `RetryConfig` and `CircuitBreakerConfig` be in Infrastructure SSOT?
- **Location**: Need to identify where Infrastructure SSOT configs are stored

### Agent-2 (Architecture SSOT)
- **Action**: Review migration strategy
- **Approval**: Needed before moving cross-cutting configs

---

## ✅ RECOMMENDATION

### Option 1: Move to Infrastructure SSOT (RECOMMENDED)
- **Pros**: True domain alignment, infrastructure patterns in infrastructure domain
- **Cons**: Requires coordination with Agent-3, migration complexity
- **Timeline**: 2-3 cycles (coordination + migration)

### Option 2: Keep in Current Location
- **Pros**: Already consolidated, no migration needed
- **Cons**: Domain misalignment, not true infrastructure SSOT
- **Timeline**: 0 cycles

### Option 3: Create Shared Core Config
- **Pros**: Neutral location, accessible to all domains
- **Cons**: Doesn't follow SSOT domain ownership model
- **Timeline**: 1-2 cycles

---

## 🚀 NEXT STEPS

1. **IMMEDIATE**: Coordinate with Agent-3 on Infrastructure SSOT location
2. **IMMEDIATE**: Analyze duplicate definitions to create unified version
3. **PENDING**: Get Agent-2 approval for migration strategy
4. **PENDING**: Execute migration after coordination complete

---

**Status**: Evaluation complete, awaiting Agent-3 coordination  
**Priority**: MEDIUM (coordination required before execution)



