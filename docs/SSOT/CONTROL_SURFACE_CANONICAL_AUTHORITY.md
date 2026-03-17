# Control Surface Canonical Authority (SSOT)

**SSOT Domain:** infrastructure  
**Scope:** CLI/runtime invocation authority and startup routing

## Problem Snapshot

The current repository exposes multiple high-level control paths:

- `main.py`
- `src/cli/argument_parser.py`
- `src/cli/commands/handlers/start_handler.py`
- `src/services/service_manager.py`
- `src/core/cli/__main__.py`

This increases risk of startup drift and inconsistent runtime behavior when different entrypoints evolve independently.

## Canonical Authority Decision

`src/cli/__main__.py` is the **one true control-plane entrypoint**.

- Human/operator entry command: `python -m src.cli ...`
- Legacy entrypoints (`main.py`, `src/core/cli/__main__.py`) are compatibility adapters only.
- Service orchestration (`src/services/service_manager.py`) must not define top-level CLI authority.

## Architecture Diagram (Control-Path SSOT)

```mermaid
flowchart TD
    U[Operator / Automation] --> C[python -m src.cli\nCanonical Entry]

    C --> D1[Domain Router]
    D1 --> SVC[services domain]
    D1 --> CORE[core domain]

    SVC --> SH[Start/stop handlers]
    SH --> SM[ServiceManager\n(orchestration only)]

    CORE --> CP[Core feature CLIs]

    L1[main.py\nLegacy Adapter] -. redirects only .-> C
    L2[src/core/cli/__main__.py\nLegacy Adapter] -. redirects only .-> C

    classDef canonical fill:#d1fae5,stroke:#065f46,stroke-width:2px;
    classDef legacy fill:#fee2e2,stroke:#991b1b,stroke-width:1px,stroke-dasharray: 5 3;
    class C canonical;
    class L1,L2 legacy;
```

## Control-Path Rules

1. **No new top-level runtime entrypoints** without explicit SSOT update in this document.
2. `main.py` and `src/core/cli/__main__.py` may only:
   - parse minimal compatibility flags, and/or
   - redirect to `src.cli`.
3. Business/runtime lifecycle logic lives behind domain handlers and services, not in adapters.
4. Any new domain added to unified CLI must be registered in this document.

## Migration Queue (High-Leverage)

1. Reduce `main.py` to an adapter that invokes `src.cli` and emits deprecation warning.
2. Move any command-only logic still embedded in `main.py` into `src/cli/commands/...` handlers.
3. Keep `ServiceManager` orchestration-focused (no CLI branching logic).
4. Add CI guardrail: fail if a new root-level executable Python entrypoint appears without SSOT annotation.

## Success Criteria

- Single documented CLI authority: `src/cli/__main__.py`.
- Legacy entrypoints perform redirection only.
- Startup behavior parity no longer depends on invocation path.
