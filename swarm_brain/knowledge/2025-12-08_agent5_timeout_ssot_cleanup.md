# 2025-12-08 - Agent-5 Timeout SSOT Cleanup

**Scope:** Phase 5 timeout constants (Discord UI views)  
**Outcome:** Hardcoded 300/600s replaced with `TimeoutConstants.HTTP_EXTENDED`; imports hoisted to module scope.

## Changed Files
- `src/discord_commander/views/agent_messaging_view.py`
- `src/discord_commander/views/bump_agent_view.py`
- `src/discord_commander/views/aria_profile_view.py`
- `src/discord_commander/views/carmyn_profile_view.py`
- `src/discord_commander/views/help_view.py`

## Rationale
- Prevent timeout drift across Discord interactions by using SSOT defaults.
- Simplify future tuning by centralizing values in `TimeoutConstants`.

## Next Actions
- Run `tools/timeout_sweep_report.py --paths src tools` to catch remaining hardcoded timeouts.
- Replace any remaining matches with the appropriate `TimeoutConstants` value.
- Resume Trading Replay Journal Analytics (performance dashboard, behavioral trends, composite score) with Agent-3 coordination.

## Artifacts
- Devlog: `agent_workspaces/Agent-5/devlog_2025-12-08.md`
- Discord post: `agent_workspaces/Agent-5/DEVLOG_2025-12-08_DISCORD.md`
- Tool: `tools/timeout_sweep_report.py`

