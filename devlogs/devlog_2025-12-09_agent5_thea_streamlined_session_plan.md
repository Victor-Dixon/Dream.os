# Thea Streamlined Session Flow — Implementation Plan

## Task
Implement the streamlined Thea auth + keepalive flow using a single public command and a self-throttling session manager.

## Actions Taken
- Locked in the simplified UX:
  - **Single command**: `!thea`
  - **Optional debug**: `!thea-status`
- Defined new core utility:
  - `TheaSessionManager`
  - `ensure_session()` state machine
  - Cookie persistence: `data/thea_cookies.json`
  - Last-refresh tracking: `data/thea_last_refresh.json`
- Selected runtime behavior:
  - Headless refresh when cookies exist + session is likely valid
  - Auto-fallback to interactive login when needed
  - **No cron**, no mode flags
- Designed self-throttling keepalive:
  - Run `ensure_session(min_interval=60m)` on:
    - bot startup
    - first Thea-dependent usage
  - Skip refresh if within interval
- Added guardrails:
  - Missing `undetected-chromedriver` → post exact pip install hint
  - Cookie read/write errors → post path + short error snippet
  - Headless failure x2 → mark cookies invalid and prompt `!thea` re-login
- Confirmed alert strategy:
  - Default: reply in-channel
  - Only notify on actionable failure, no ack spam

## Commit Message (planned)
feat(thea): add TheaSessionManager + single !thea command with self-throttling keepalive

## Status
🟡 In progress — next step:
- Add `core/thea_session.py`
- Wire Discord command handlers:
  - `!thea` → `ensure_session(allow_interactive=True)`
  - `!thea-status` → show cookie presence + last refresh time
- Add startup hook calling:
  - `ensure_session(min_interval_minutes=60, allow_interactive=False)`
- Validate:
  - Happy path headless refresh
  - Expired cookie triggers interactive
  - Missing dependency message
  - Write error messaging







