# Digital Dreamscape Lore Codex Guide

## 🌌 Overview
The **Lore Codex** is the single source of truth for the Digital Dreamscape canon. It defines the identities, voices, and rules that govern the Swarm's operations.

## 📁 Structure
- `lore/codex.yaml`: The master registry of Portals, Agents, and Voices.
- `lore/world_state.yaml`: Dynamic state (World Clock, Active Quests).
- `lore/episodes/`: Storage for session episodes (drafts & canon).
- `lore/voices/styleguide.yaml`: Detailed voice profiles for agents.

## 🤖 For Agents
### Session Start
At the beginning of your session, the system invokes `runtime/hooks/lore_sync.py`. This injects your **Identity**, **Voice Profile**, and **Signature Phrases** into your context. Use them to maintain character.

**Example (Agent-1):**
> "Trail marked. Discovery phase complete." (Voice: Scout)

### Session End
When closing a session, use the **Devlog Transmission Template** (`lore/templates/devlog_transmission.md`).
The system will automatically generate an **Episode Draft** in `lore/episodes/drafts/`.

## ⚖️ The Truthkeeper
The **Truthkeeper** (`tests/test_lore_codex.py`) is the validation ritual. It ensures:
1. `codex.yaml` follows the strict schema.
2. All agents have valid voice profiles.
3. Episode drafts are structurally correct.

To invoke the Truthkeeper manually:
```bash
python3 tests/test_lore_codex.py
```

## 📜 Canon Law
1. **Thea arbitrates conflicts.**
2. **Truthkeeper must pass** before any lore is marked `canon: true`.
3. **No destructive git commands** in shared workspaces.

## 🚀 Adding New Lore
1. Update `lore/codex.yaml` or `lore/world_state.yaml`.
2. Run Truthkeeper to validate.
3. Submit for review (Thea).
