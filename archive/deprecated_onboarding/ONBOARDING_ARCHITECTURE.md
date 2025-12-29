# Onboarding Architecture Overview

## Current Implementation Status

### ✅ Active Implementations

#### 1. Lite Onboarding (NEW - Message-Only)
**Purpose**: Headless/message-only onboarding without PyAutoGUI dependency

**Entry Points**:
- CLI flags: `--soft-onboard-lite`, `--hard-onboard-lite`
- Location: `src/services/messaging_cli.py`

**Implementation**:
- `MessagingCLI._handle_soft_onboard_lite()` - Renders template and sends via messaging bus
- `MessagingCLI._handle_hard_onboard_lite()` - Renders template and sends via messaging bus
- `MessagingCLI._send_simple_s2a()` - Helper to send S2A messages

**Templates**:
- `src/services/onboarding/soft/templates/soft_onboard_template.md`
- `src/services/onboarding/hard/templates/hard_onboard_template.md`

**Fallback**:
- If templates missing, uses `default_message.py` functions:
  - `src/services/onboarding/soft/default_message.py::get_default_soft_onboarding_message()`
  - `src/services/onboarding/hard/default_message.py::get_default_hard_onboarding_message()`

**Status**: ✅ ACTIVE - Recommended for headless environments

---

#### 2. Full Onboarding (PyAutoGUI-Based)
**Purpose**: Full GUI automation onboarding with coordinate-based delivery

**Entry Points**:
- CLI flags: `--soft-onboarding`, `--hard-onboarding`
- Discord bot: `!soft`, `!hard` commands
- Tools: `tools/soft_onboard_cli.py`

**Handlers**:
- `src/services/handlers/soft_onboarding_handler.py` - CLI handler
- `src/services/handlers/hard_onboarding_handler.py` - CLI handler

**Services**:
- `src/services/soft_onboarding_service.py` - PyAutoGUI service (used by Discord bot)
- `src/services/hard_onboarding_service.py` - PyAutoGUI service (used by Discord bot)

**Tools**:
- `tools/soft_onboard_cli.py` - Standalone CLI wrapper (used by Discord bot)

**Status**: ✅ ACTIVE - Required for Discord bot compatibility

---

#### 3. Legacy Onboarding Handler
**Purpose**: Status checks and utility functions

**Location**: `src/services/handlers/onboarding_handler.py`

**Used By**:
- `src/services/handlers/utility_handler.py` - For `check_status()` and `list_agents()`

**Status**: ✅ ACTIVE - Required for utility functions

---

#### 4. Template Core Definitions
**Purpose**: Centralized S2A template definitions

**Location**: `src/core/messaging_templates_data/s2a_templates_core.py`

**Contains**:
- `SOFT_ONBOARDING` template string
- `HARD_ONBOARDING` template string

**Status**: ✅ ACTIVE - May be used by other systems

---

## Redundancy Analysis

### Not Redundant (All Active)
1. **Lite onboarding** - New streamlined path for headless environments
2. **Full onboarding handlers** - Required for Discord bot
3. **Onboarding services** - Required for Discord bot
4. **Legacy handler** - Required for utility functions
5. **Template core** - May be used by other systems
6. **Default message modules** - Used as fallback for lite onboarding

### Potential Future Consolidation

If Discord bot migrates to lite onboarding:
- Archive `tools/soft_onboard_cli.py`
- Archive `src/services/handlers/soft_onboarding_handler.py`
- Archive `src/services/handlers/hard_onboarding_handler.py`
- Archive `src/services/soft_onboarding_service.py`
- Archive `src/services/hard_onboarding_service.py`

**Current Recommendation**: Keep all implementations active until Discord bot migration is complete.

---

## Usage Guide

### For Headless/CI Environments
```bash
# Use lite flags (message-only, no PyAutoGUI)
python -m src.services.messaging_cli --soft-onboard-lite Agent-7
python -m src.services.messaging_cli --hard-onboard-lite Agent-7
```

### For Discord Bot / GUI Environments
```bash
# Use full onboarding (PyAutoGUI-based)
python -m src.services.messaging_cli --soft-onboarding --agent Agent-7
python -m src.services.messaging_cli --hard-onboarding --agent Agent-7

# Or use standalone tool (Discord bot uses this)
python tools/soft_onboard_cli.py --agent Agent-7
```

---

## File Organization

```
src/services/
├── messaging_cli.py                    # Lite onboarding flags
├── messaging_cli_parser.py              # Flag definitions
├── handlers/
│   ├── soft_onboarding_handler.py      # Full onboarding (Discord bot)
│   ├── hard_onboarding_handler.py       # Full onboarding (Discord bot)
│   └── onboarding_handler.py           # Legacy (utility functions)
├── soft_onboarding_service.py           # PyAutoGUI service (Discord bot)
├── hard_onboarding_service.py           # PyAutoGUI service (Discord bot)
└── onboarding/
    ├── soft/
    │   ├── default_message.py           # Template content source
    │   └── templates/
    │       └── soft_onboard_template.md # Lite template
    └── hard/
        ├── default_message.py           # Template content source
        └── templates/
            └── hard_onboard_template.md # Lite template

tools/
└── soft_onboard_cli.py                  # Standalone CLI (Discord bot)

src/core/messaging_templates_data/
└── s2a_templates_core.py                # Template core definitions
```

---

## Migration Path (Future)

1. Update Discord bot to use `--soft-onboard-lite` / `--hard-onboard-lite`
2. Archive PyAutoGUI-based implementations
3. Consolidate to single lite implementation
4. Remove archived code after verification period

