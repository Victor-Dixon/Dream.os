# Onboarding Architecture Summary

**Generated**: 1766066302.0

## Service Shims

### `HardOnboardingService`
- **File**: `src\services\hard_onboarding_service.py`
- **Lines**: 25
- **V2 Compliant**: ✅

### `SoftOnboardingService`
- **File**: `src\services\soft_onboarding_service.py`
- **Lines**: 27
- **V2 Compliant**: ✅

## Helper Modules

### `agent_instructions`
- **File**: `src\services\onboarding\agent_instructions.py`
- **Lines**: 342
- **V2 Compliant**: ❌
- **Public Functions**: get_agent_specific_instructions

### `onboarding_helpers`
- **File**: `src\services\onboarding\onboarding_helpers.py`
- **Lines**: 89
- **V2 Compliant**: ✅
- **Public Functions**: load_agent_coordinates, validate_coordinates, validate_onboarding_coordinates

## Test Coverage

- **Test File**: `tests\unit\services\test_onboarding_services.py`
- **Locks Public APIs**: ✅

## Pattern Validation

- **Services V2 Compliant**: ✅
- **Helpers V2 Compliant**: ❌
- **Shim Pattern (Delegations)**: ⚠️
