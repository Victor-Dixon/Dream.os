# Onboarding Template Unification

**Date:** 2025-12-26  
**Agent:** Agent-3  
**Status:** ✅ COMPLETE

---

## Summary

Unified hard and soft onboarding into a single contract-driven template (`ONBOARDING`) to prevent drift and ensure consistent Output Contract behavior across both modes.

---

## Problem Statement

Previously, hard and soft onboarding used separate templates (`HARD_ONBOARDING` and `SOFT_ONBOARDING`) that could diverge over time, leading to:

- **Inconsistent Output Contracts** - Hard onboarding lacked the strict Output Contract requirement
- **Different No-Ack policies** - Hard used "artifact/blocker", soft used "Output Contract only"
- **Template drift risk** - Two templates to maintain increases maintenance burden
- **Behavioral inconsistency** - Agents behaved differently depending on onboarding path

---

## Solution

Created unified `ONBOARDING` template that:
- **Single canonical template** - `ONBOARDING` template with parameterized mode
- **Identical Output Contract** - Both hard and soft now use the same strict Output Contract
- **Parameterized differences** - Mode, priority, and optional footer are parameters
- **Backward compatibility** - Old templates marked as DEPRECATED but still functional

---

## Changes Made

### 1. Unified Template (`src/core/messaging_template_texts.py`)

Created new `ONBOARDING` template with:
- `{mode}` parameter (HARD/SOFT)
- `{footer}` parameter (optional, empty string default)
- **Identical Output Contract** for both modes
- **Unified No-Ack Policy**: "Respond ONLY with the Output Contract"

```python
"ONBOARDING": (
    "[HEADER] S2A ONBOARDING ({mode})\n"
    ...
    "No-Ack Policy:\n"
    "- Do not send empty acknowledgments.\n"
    "- Respond ONLY with the Output Contract.\n\n"
    ...
    "OUTPUT CONTRACT (STRICT):\n"
    "- Task: <name>\n"
    "- Actions Taken: bullet list\n"
    ...
    "{footer}"
)
```

### 2. Updated Template Routing (`src/core/messaging_templates.py`)

- Added `ONBOARDING` to `S2A_KEYS`
- Updated `S2A_TAG_ROUTING` to use `ONBOARDING` instead of `HARD_ONBOARDING`
- Updated `S2A_TYPE_ROUTING` to use `ONBOARDING`
- Added defaults for `mode` and `footer` in `format_s2a_message()`

### 3. Hard Onboarding Steps (`src/services/onboarding/hard/steps.py`)

- Updated `step_5_send_onboarding_message()` to use unified template
- Added `include_jet_fuel: bool = False` parameter (default: False)
- Changed `template_key` from `"HARD_ONBOARDING"` to `"ONBOARDING"`
- Added `mode="HARD"` parameter
- Made Jet Fuel footer optional via `footer` parameter

### 4. Soft Onboarding Steps (`src/services/onboarding/soft/steps.py`)

- Updated `step_6_paste_onboarding_message()` to use unified template
- Changed `template_key` from `"SOFT_ONBOARDING"` to `"ONBOARDING"`
- Added `mode="SOFT"` parameter
- Added `footer=""` parameter (no footer)

### 5. Soft Onboarding Messaging Fallback (`src/services/onboarding/soft/messaging_fallback.py`)

- Updated `send_onboarding_via_messaging()` to use unified template
- Changed `template_key` from `"SOFT_ONBOARDING"` to `"ONBOARDING"`
- Added `mode="SOFT"` and `footer=""` parameters

---

## Key Differences (Now Parameterized)

| Aspect | Hard Onboarding | Soft Onboarding |
|--------|----------------|----------------|
| **Mode** | `mode="HARD"` | `mode="SOFT"` |
| **Priority** | `URGENT` | `REGULAR` |
| **Footer** | Optional Jet Fuel (default: `""`) | `""` (no footer) |
| **Actions Content** | Hard onboarding default message | Soft onboarding default message |
| **Template** | ✅ `ONBOARDING` (unified) | ✅ `ONBOARDING` (unified) |
| **Output Contract** | ✅ **Identical** | ✅ **Identical** |
| **No-Ack Policy** | ✅ **Identical** | ✅ **Identical** |

---

## Benefits

1. **Prevents Template Drift** - Single source of truth for onboarding contract
2. **Consistent Behavior** - All agents follow same Output Contract regardless of onboarding path
3. **Maintainability** - One template to update instead of two
4. **Flexibility** - Easy to add new modes or customize via parameters
5. **Backward Compatible** - Old templates still work (marked DEPRECATED)

---

## Migration Notes

### For Code Using Hard Onboarding

**Old:**
```python
render_message(msg, template_key="HARD_ONBOARDING", ...)
```

**New:**
```python
render_message(msg, template_key="ONBOARDING", mode="HARD", footer=jet_fuel_footer, ...)
```

### For Code Using Soft Onboarding

**Old:**
```python
render_message(msg, template_key="SOFT_ONBOARDING", ...)
```

**New:**
```python
render_message(msg, template_key="ONBOARDING", mode="SOFT", footer="", ...)
```

---

## Deprecation

Old templates (`HARD_ONBOARDING`, `SOFT_ONBOARDING`) are marked as DEPRECATED in code comments but remain functional for backward compatibility. They will be removed in a future version once all code paths are migrated.

---

## Verification

✅ All onboarding code paths updated  
✅ No linting errors  
✅ Backward compatible (old templates still work)  
✅ Output Contract identical across both modes  
✅ No-Ack policy unified  

---

## Files Modified

1. `src/core/messaging_template_texts.py` - Added unified `ONBOARDING` template
2. `src/core/messaging_templates.py` - Updated routing and defaults
3. `src/services/onboarding/hard/steps.py` - Updated to use unified template
4. `src/services/onboarding/soft/steps.py` - Updated to use unified template
5. `src/services/onboarding/soft/messaging_fallback.py` - Updated to use unified template
6. `src/services/onboarding/soft/service.py` - Updated docstrings

---

**Status:** ✅ COMPLETE - Unified onboarding templates prevent drift and ensure consistent Output Contract behavior

