<!-- SSOT Domain: documentation -->

# NEXT_UP

## Exact next repair target
Reduce file-header compliance drift by fixing validator-reported violations on newly added files first:

1. `src/core/managers/core_onboarding_manager.py` (`HDR001`)
2. `src/core/utilities/validation_utilities.py` (`HDR001`, `HDR004`)
3. `tools/recovery_notes/check_compliance.py` (`HDR001`, `HDR004`)

## Done when
- `python tools/file_header_validator.py validate` shows zero `violations_on_new_files`.
- Discord template imports continue to load from `src.discord_commander.templates` without fallback.
- CI-critical checks still pass:
  - `python tools/validation/check_recovery_registry.py`
  - `python tools/recovery_notes/check_compliance.py`
