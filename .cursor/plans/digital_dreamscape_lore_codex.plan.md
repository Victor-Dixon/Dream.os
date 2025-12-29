# Digital Dreamscape Lore Codex Implementation Plan

## Overview
This plan outlines the implementation of the "Digital Dreamscape Lore Codex," a single source of truth for the Dreamscape canon (portals, agents, voices, rules) within the Dream.OS repository. This system ensures consistent storytelling, prevents lore drift, and enables automated session cleanup with "mythic" quality.

## Goals
- **Single Source of Truth (SSOT)**: Centralize all lore in `lore/codex.yaml` and related files.
- **Automated Consistency**: Ensure agents speak and act according to their defined voice profiles.
- **Lore Drift Prevention**: Validate lore changes against a schema ("Truthkeeper" ritual).
- **Session Integration**: Automatically sync lore state at session start and end.

## Phase 1: Foundation (Directory Structure & Schemas)
- [ ] Create directory structure:
    - `lore/`
    - `lore/schema/`
    - `lore/episodes/`
    - `lore/episodes/drafts/`
    - `lore/episodes/canon/`
    - `lore/episodes/evidence/`
    - `lore/voices/`
    - `lore/templates/`
- [ ] Define JSON schemas in `lore/schema/`:
    - `lore_schema.json` (for codex.yaml)
    - `episode_schema.json` (for episode tracking)

## Phase 2: Population (Codex, Voices, Agents)
- [ ] Create `lore/codex.yaml` with initial content (from user query).
- [ ] Create `lore/world_state.yaml` for dynamic state (world clock, active quests).
- [ ] Create `lore/voices/styleguide.yaml` detailing voice profiles.
- [ ] Create `lore/episodes/index.yaml` for episode tracking.

## Phase 3: Integration (Session Hooks)
- [ ] Create `runtime/hooks/lore_sync.py` to handle:
    - Loading codex and world state.
    - Fetching recent episodes.
    - Injecting context into agent sessions.
- [ ] Update session start scripts to call `lore_sync.on_session_start`.
- [ ] Update session cleanup scripts to call `lore_sync.on_session_end` (generating episode drafts).

## Phase 4: Validation (Truthkeeper)
- [ ] Create `tests/test_lore_codex.py` to implement the "Truthkeeper" validation ritual.
    - Validate `codex.yaml` against schema.
    - Validate episode drafts.
    - Verify agent/portal references.
- [ ] Add pre-commit hook or CI step for Truthkeeper validation.

## Phase 5: Operationalization (Templates & Docs)
- [ ] Create `lore/templates/devlog_transmission.md` based on the new standard.
- [ ] Update onboarding documentation to reference the Lore Codex.
- [ ] Verify that a new agent can onboard using only the Codex.

## Success Metrics
- `lore/codex.yaml` exists and validates.
- Agents can fetch their "mythic identity" programmatically.
- "Truthkeeper" tests pass.
- Session cleanup produces valid episode drafts.
