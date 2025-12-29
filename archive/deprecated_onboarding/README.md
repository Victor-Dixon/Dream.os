# Deprecated Onboarding Code Archive

This directory contains deprecated or redundant onboarding-related code that has been replaced by streamlined implementations.

## Current Active Implementations

### Lite Onboarding (Message-Only)
- **Flags**: `--soft-onboard-lite`, `--hard-onboard-lite`
- **Location**: `src/services/messaging_cli.py` (`_handle_soft_onboard_lite`, `_handle_hard_onboard_lite`)
- **Purpose**: Headless/message-only onboarding without PyAutoGUI
- **Templates**: 
  - `src/services/onboarding/soft/templates/soft_onboard_template.md`
  - `src/services/onboarding/hard/templates/hard_onboard_template.md`

### Full Onboarding (PyAutoGUI-Based)
- **Flags**: `--soft-onboarding`, `--hard-onboarding`
- **Handlers**: 
  - `src/services/handlers/soft_onboarding_handler.py`
  - `src/services/handlers/hard_onboarding_handler.py`
- **Services**:
  - `src/services/soft_onboarding_service.py`
  - `src/services/hard_onboarding_service.py`
- **Purpose**: Full GUI automation onboarding (used by Discord bot)
- **Status**: ✅ ACTIVE - Required for Discord bot commands

## What's Kept vs Archived

### ✅ KEPT (Active)
- `src/services/handlers/soft_onboarding_handler.py` - Used by Discord bot
- `src/services/handlers/hard_onboarding_handler.py` - Used by Discord bot
- `src/services/handlers/onboarding_handler.py` - Used by `utility_handler.py` for status checks
- `src/services/soft_onboarding_service.py` - PyAutoGUI service
- `src/services/hard_onboarding_service.py` - PyAutoGUI service
- `src/services/onboarding/soft/default_message.py` - Template content source
- `src/services/onboarding/hard/default_message.py` - Template content source

### 📦 ARCHIVED (Deprecated/Redundant)
- None yet - all code is still in use

## Migration Notes

The lite onboarding flags (`--soft-onboard-lite`, `--hard-onboard-lite`) were added to provide a streamlined message-only onboarding path that:
1. Doesn't require PyAutoGUI (works in headless environments)
2. Uses templates for consistent messaging
3. Falls back to `default_message.py` if templates are missing
4. Sends directly via messaging bus (no GUI automation)

The full onboarding handlers remain active for Discord bot compatibility and GUI-based workflows.

## Future Cleanup

If Discord bot is migrated to use lite onboarding:
- Archive `soft_onboarding_handler.py` and `hard_onboarding_handler.py`
- Archive `soft_onboarding_service.py` and `hard_onboarding_service.py`
- Keep only lite implementations and templates

