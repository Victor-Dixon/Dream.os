---
id: kb-messaging-templates-2025-12-10
title: Messaging Template Structure & Ordering Guards
author: Agent-8
date: 2025-12-10
tags: [messaging-templates, integration-tests, ssot, s2a, d2a, c2a, a2a]
---

## Summary
- Added integration tests that assert full template structure and ordering for S2A/D2A/C2A/A2A.
- Special character and unicode coverage ensures literal braces/markup do not break formatting.
- Footers (devlog/workflows) are validated when requested to guarantee correct wrap for agent-facing messages.

## Key details
- S2A CONTROL expected sections (ordered): header → context → action required → no-reply policy → priority behavior → operating cycle → cycle checklist → Discord reporting → evidence → blocked.
- D2A expected sections (ordered): header → origin → user message → interpretation → proposed action → devlog command → clarification/fallback → hashtags.
- A2A uses Ask/Offer + Cycle Checklist + no-ack rules; ordering asserts these precede fallback and response guidance.
- Coverage currently blocked by `cv2.dnn.DictValue` AttributeError via `pyautogui` import chain; guard/mocking required for headless cov.

## Next actions
- Add guard/stub for `pyautogui/cv2` to unblock coverage.
- Re-run coverage for messaging templates/modules after guard.
- Propagate structure/order assertion pattern to other template consumers.


