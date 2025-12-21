# Onboarding Services & Helpers

## Overview

The onboarding flow is split into **thin service shims** and a set of **helper modules** to keep V2 constraints (LOC, single responsibility, SSOT) intact.

Public behaviour is locked in by `tests/unit/services/test_onboarding_services.py`, which treats the free functions and service methods as the stable external contract:

- `hard_onboard_agent` / `hard_onboard_multiple_agents`
- `soft_onboard_agent` / `soft_onboard_multiple_agents`

Any future refactor must preserve these function signatures and semantics while keeping heavy logic in the onboarding helper modules.

## Service Shims

### `HardOnboardingService` (`src/services/hard_onboarding_service.py`)

- **Responsibility**: Orchestrate the 5-step **hard onboarding** reset protocol:
  1. Clear chat (Ctrl+Shift+Backspace)
  2. Execute current input (Ctrl+Enter)
  3. Open a new window/session (Ctrl+N)
  4. Navigate to onboarding input coordinates
  5. Send the onboarding message
- **Delegation**:
  - Coordinate loading and validation are delegated to `onboarding_helpers`.
  - Long-form, role-specific instructions are delegated to `agent_instructions.get_agent_specific_instructions`.
  - Optional cycle-duty templates are handled by `onboarding_template_loader` when available.
- **Public API**:
  - `HardOnboardingService.execute_hard_onboarding(agent_id, onboarding_message, role=None) -> bool`
  - `hard_onboard_agent(agent_id, onboarding_message, role=None) -> bool`
  - `hard_onboard_multiple_agents(agents: list[tuple[str, str]], role=None) -> dict[str, bool]`

### `SoftOnboardingService` (`src/services/soft_onboarding_service.py`)

- **Responsibility**: Orchestrate the 6-step **soft onboarding** protocol with PyAutoGUI animations:
  1. Click chat input
  2. Save session (Ctrl+Enter)
  3. Send cleanup prompt (passdown message)
  4. Open new tab (Ctrl+T)
  5. Navigate to onboarding coordinates
  6. Paste onboarding message
- **Delegation**:
  - Coordinate loading is delegated to the shared coordinate loader (`core.coordinate_loader`).
  - When PyAutoGUI is unavailable, both cleanup and onboarding messages fall back to the unified messaging system (`MessageCoordinator`, `UnifiedMessage`, templates).
  - Keyboard lock handling lives in the free functions and `keyboard_control_lock` helpers, not in the core service logic.
- **Public API**:
  - `SoftOnboardingService.execute_soft_onboarding(agent_id, onboarding_message, role=None, custom_cleanup_message=None) -> bool`
  - `soft_onboard_agent(agent_id, message, **kwargs) -> bool`
  - `soft_onboard_multiple_agents(agents: list[tuple[str, str]], role=None, generate_cycle_report=True) -> dict[str, bool]`

## Helper Modules

### `onboarding_helpers` (`src/services/onboarding/onboarding_helpers.py`)

**SSOT Domain**: `integration`

- **Responsibility**: Coordinate loading and validation plus generic onboarding utilities.
- **Public API**:
  - `load_agent_coordinates(agent_id: str) -> tuple[Coords | None, Coords | None]`
  - `validate_coordinates(agent_id: str, coords: Coords) -> bool`
  - `validate_onboarding_coordinates(agent_id: str, coords: Coords) -> bool`

All coordinate and bounds logic should live here so that both hard and soft onboarding services share the same behaviour.

### `agent_instructions` (`src/services/onboarding/agent_instructions.py`)

**SSOT Domain**: `integration`

- **Responsibility**: Long-form, agent-specific "optimized pattern" instructions that are appended to onboarding messages.
- **Public API**:
  - `get_agent_specific_instructions(agent_id: str) -> str`

This module is the **single source of truth** for the per-agent instruction blocks. Service shims must not inline large instruction mappings; they should always call this helper.

## Design Pattern

- Services remain **thin orchestration layers** over helpers:
  - They own sequencing, keyboard/mouse actions, and high-level behaviour.
  - They do **not** own large content blocks or coordinate logic.
- Helpers own:
  - Coordinate loading and validation (`onboarding_helpers`).
  - Role-specific, human-readable instruction content (`agent_instructions`).
  - Optional future responsibilities like onboarding message formatting.

This separation keeps onboarding code V2-compliant while still allowing safe refactors: tests pin the public APIs, and helpers can evolve independently as long as their contracts remain stable.