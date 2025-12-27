# Canonical Closure Prompt Integration

## Overview

The **A++ Canonical Swarm Closure Prompt** has been integrated into the soft onboarding system as the default cleanup message. This ensures all agents receive the same high-quality, project-agnostic closure directive during onboarding.

## Architecture

### SSOT Location

The canonical closure prompt is stored as the single source of truth (SSOT) in:

```
src/services/onboarding/soft/canonical_closure_prompt.py
```

### Integration Points

1. **Canonical Prompt File** (`canonical_closure_prompt.py`)
   - Contains the A++ closure prompt text
   - Exports `CANONICAL_CLOSURE_PROMPT` constant and `get_canonical_closure_prompt()` function
   - Documented with use cases and project types

2. **Messaging Fallback** (`messaging_fallback.py`)
   - `_get_default_cleanup_message()` now imports and returns the canonical prompt
   - Used when PyAutoGUI is unavailable (fallback path)
   - Also used in Step 3 when PyAutoGUI is available

3. **Soft Onboarding Steps** (`steps.py`)
   - Step 3 calls `self.messaging._get_default_cleanup_message()` to get the prompt
   - Supports custom cleanup messages via `custom_cleanup_message` parameter
   - Falls back to canonical prompt if no custom message provided

4. **Module Exports** (`__init__.py`)
   - Exports `CANONICAL_CLOSURE_PROMPT` and `get_canonical_closure_prompt()` for external use
   - Allows other parts of the system to access the canonical prompt directly

## Usage Flow

### During Soft Onboarding (Step 3)

```
SoftOnboardingService.execute_soft_onboarding()
  └─> SoftOnboardingSteps.step_3_send_cleanup_prompt()
      └─> OnboardingMessagingFallback._get_default_cleanup_message()
          └─> canonical_closure_prompt.get_canonical_closure_prompt()
              └─> Returns CANONICAL_CLOSURE_PROMPT
```

### Direct Access

```python
from src.services.onboarding.soft import get_canonical_closure_prompt

prompt = get_canonical_closure_prompt()
# Use prompt for custom closure workflows
```

## Features

### Project-Agnostic

Works for:
- Code repos
- Websites
- Research spikes
- Infrastructure work
- Content systems
- Internal tooling
- One-day experiments

### Use Cases

- End of day closure
- End of sprint / cycle
- Before handoff to another agent
- Before public posting
- Before context window reset

### Key Requirements

The prompt enforces:

1. **Cold-start survivability** - Passdown.json must enable cold-start resumption
2. **Public-build readiness** - Devlog serves as public-facing build update
3. **Zero-drift handoff** - Another agent can continue without context loss
4. **Strict output contract** - Verifiable artifacts, no speculation
5. **Progression gate** - Blocks advancement until closure is complete

## Customization

While the canonical prompt is the default, custom cleanup messages can still be provided:

```python
from src.services.onboarding.soft import soft_onboard_agent

# Use canonical prompt (default)
soft_onboard_agent("Agent-7")

# Use custom cleanup message
soft_onboard_agent(
    "Agent-7",
    custom_cleanup_message="Custom closure instructions..."
)
```

## Verification

The integration has been verified:

- ✅ Prompt loads successfully (2580 characters)
- ✅ Messaging fallback can access prompt
- ✅ No linting errors
- ✅ Module exports work correctly
- ✅ Integration path tested end-to-end

## Maintenance

### Updating the Prompt

To update the canonical closure prompt:

1. Edit `src/services/onboarding/soft/canonical_closure_prompt.py`
2. Update `CANONICAL_CLOSURE_PROMPT` constant
3. Test with: `python -c "from src.services.onboarding.soft import get_canonical_closure_prompt; print(get_canonical_closure_prompt())"`
4. Verify soft onboarding still works: `python -m src.services.messaging_cli --soft-onboarding --agent Agent-7 --dry-run`

### Version History

- **2025-01-XX**: Initial integration of A++ canonical closure prompt
- Replaces previous simple cleanup message with comprehensive closure directive

## Related Files

- `src/services/onboarding/soft/canonical_closure_prompt.py` - SSOT for closure prompt
- `src/services/onboarding/soft/messaging_fallback.py` - Uses canonical prompt
- `src/services/onboarding/soft/steps.py` - Step 3 sends cleanup prompt
- `src/services/onboarding/soft/service.py` - Orchestrates 6-step protocol
- `src/services/handlers/soft_onboarding_handler.py` - CLI entry point

## References

- Original prompt specification: User-provided A++ canonical Swarm closure prompt
- Soft onboarding protocol: `docs/onboarding/` (if exists)
- Messaging templates: `src/core/messaging_template_texts.py`

