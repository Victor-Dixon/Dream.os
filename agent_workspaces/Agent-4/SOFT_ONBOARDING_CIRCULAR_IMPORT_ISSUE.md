# 🚨 Soft Onboarding Service - Circular Import Issue

**Date:** 2025-11-25  
**Status:** ⚠️ IDENTIFIED - Needs Resolution  
**Workaround:** Direct messaging via `messaging_cli` (completed)

## Issue Description

The `soft_onboarding_service.py` has a circular import dependency:

1. `src/services/soft_onboarding_service.py` imports:
   ```python
   from .handlers.soft_onboarding_handler import SoftOnboardingHandler
   ```

2. `src/services/handlers/soft_onboarding_handler.py` imports:
   ```python
   from ..soft_onboarding_service import SoftOnboardingService
   ```

This creates a circular dependency that prevents the service from being used directly.

## Current Workaround

**Completed:** All agents (1-8) were soft-onboarded via direct `messaging_cli` calls, bypassing the service:

```bash
python -m src.services.messaging_cli --agent Agent-X --message "..." --priority regular
```

Each message included:
- Orientation command (`python tools/agent_orient.py`)
- Cycle passdown reference
- Mission focus
- Devlog reminder

## Resolution Needed

**Assigned to:** Agent-1 (Integration & Core Systems)

**Options:**
1. **Lazy Import Pattern** - Move the import inside the method that uses it
2. **Dependency Injection** - Pass the service as a parameter instead of importing
3. **Refactor Handler** - Remove the handler's dependency on the service
4. **Extract Common Module** - Create a shared module both can import from

## Verification

Test after fix:
```bash
python -c "from src.services.soft_onboarding_service import SoftOnboardingService; s = SoftOnboardingService(); print('✅ Import successful')"
```

## Impact

- **Current:** Service cannot be used for automated onboarding
- **Workaround:** Manual messaging works (completed for this cycle)
- **Future:** Needs resolution for automated onboarding workflows

---

**Next Steps:**
1. Agent-1 to investigate and resolve circular import
2. Test service after fix
3. Update onboarding workflows to use service once fixed

