# Messaging Templates (S2A / C2A / A2A / D2A)

## Categories & Usage (cheatsheet)

### S2A (System → Agent)
- Use for: control/ops (resumer, onboarding, passdown, telephone, FSM, debate cycle, task cycle).
- Fields: context, actions, fallback; operating cycle baked into CONTROL.
- Defaults: no devlog reminder; `include_devlog=True` to append footer if needed.
- Policy: no-reply, artifact-only progress; timers reset on artifacts (commit/test/report/doc delta).

### D2A (Discord → Agent)
- Use for: human/Discord intake, short/interactive.
- Fields: content, interpretation, actions, fallback.
- No no-reply posture; devlog off by default.

### C2A (Captain → Agent)
- Use for: captain directives.
- Fields: task, context, deliverable, checkpoint/ETA, fallback.
- Operating Procedures baked in: bilateral coordination, state scan (agent statuses + project/SSOT), learnings → Swarm Brain, scope guard (>2 domains → propose split), no chatter (only blocked or done-with-evidence).
- Devlog off by default; opt-in if you need it.

### A2A (Agent → Agent)
- Use for: handoffs, dependencies, pairing/coordination.
- Fields: ask/offer, context, next step, risks/fallback.
- Devlog off by default; opt-in if you need it.

## Where the templates live
- Code: `src/core/messaging_models_core.py` (`MessageCategory`, `MESSAGE_TEMPLATES`).
- Dispatcher/render helper: `src/core/messaging_templates.py` (`render_message`, `dispatch_template_key`, `format_s2a_message`).

## Devlog reminder (opt-in)
- Core templates do not include devlog lines.
- Pass `include_devlog=True` to `render_message(...)` to append the devlog footer when you explicitly want it.

## Core workflows footer (opt-in)
- Pass `include_workflows=True` to append a short commands footer:
  - Claim task: `python src/services/messaging_cli.py --agent <agent> --get-next-task`
  - Send message: `python src/services/messaging_cli.py --agent <agent> -m "Context + actions"`
  - Post devlog: `python tools/devlog_manager.py --agent <agent> --message "What changed / evidence / links"`
  - Commit with agent flag: `git commit -m "agent-<n>: short description"`

## Core workflows (quick commands)
- Claim task: `python src/services/messaging_cli.py --agent Agent-7 --get-next-task`
- Send a message (CLI): `python src/services/messaging_cli.py --agent Agent-5 -m "Context + actions"`
- Post devlog (tool): `python tools/devlog_manager.py --agent Agent-7 --message "What changed / evidence / links"`
- Commit with agent flag (convention): `git commit -m "agent-7: short description"` to tie activity to status monitors.

## Quick examples

### Send S2A control (Python)
```python
from src.core.messaging_templates import render_message
from src.core.messaging_models_core import UnifiedMessage, MessageCategory

msg = UnifiedMessage(
    content="",
    sender="SYSTEM",
    recipient="Agent-3",
    category=MessageCategory.S2A,
)

rendered = render_message(
    msg,
    template_key="CONTROL",
    context="Inactivity detected 7.2m",
    actions="Produce an artifact (commit/test/report). No replies.",
    fallback="Escalate to Captain if blocked",
)
```

### Send A2A handoff with devlog footer (Python)
```python
from src.core.messaging_templates import render_message
from src.core.messaging_models_core import UnifiedMessage, MessageCategory

msg = UnifiedMessage(
    content="",
    sender="Agent-7",
    recipient="Agent-4",
    category=MessageCategory.A2A,
)

rendered = render_message(
    msg,
    template_key="HANDOFF",
    ask="Code ready for review",
    context="Feature X implemented",
    next_step="Review PR #123",
    fallback="Ping if blocked",
    include_devlog=True,  # appends devlog footer
)
```

## S2A no-reply enforcement
- S2A CONTROL/STALL_RECOVERY carry no-reply + operating-cycle language.
- Ack-like replies after S2A are blocked in `MessageCoordinator`; progress counts only on artifacts.

