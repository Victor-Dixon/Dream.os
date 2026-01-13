---
title: "Messaging Templates Integration Hardening"
author: Agent-8 (SSOT & System Integration Specialist)
date: 2025-12-10
tags: [messaging-templates, integration-tests, pytest, ssot, a2a, c2a, d2a, s2a]
---

## What changed
- Expanded messaging template integration suite to 64 tests (52 original + 12 structure/order validation) covering S2A/D2A/C2A/A2A routing, defaults, special characters, end-to-end flows, and complete template structure validation.
- Added structure/order validation tests to ensure agents receive the full wrapped templates per style (headers, metadata, policies, checklists) with correct section ordering.
- Isolated the integration suite with a scoped `conftest.py` that disables heavy plugins (dash/jupyter) for faster, deterministic runs.
- Created `tools/template_structure_linter.py` for CLI validation of template structure and section ordering.

## Results
- Tests: 64/64 passing (integration suite).
- Coverage: blocked by `cv2.dnn.DictValue` AttributeError imported via `pyautogui` → `pyscreeze` → `cv2` during coverage run; needs guarding/mocking before cov can run headless.

## Next steps
- Add guard/stub for `pyautogui/cv2` in coverage path (or pin cv2 that exposes `DictValue`) and re-run coverage for `src.core.messaging_templates`, `messaging_models`, `messaging_template_texts`.
- Keep structure/order assertions green; propagate patterns to other agents consuming templates.

## How to run
```bash
python -m pytest tests/integration/test_messaging_templates_integration.py -v -p no:dash -p no:jupyter
```

## Notes
- Template structure tests assert both presence and ordering of critical sections (headers, metadata, policies, cycle checklist, footers) to prevent regressions in rendered agent-facing messages.


