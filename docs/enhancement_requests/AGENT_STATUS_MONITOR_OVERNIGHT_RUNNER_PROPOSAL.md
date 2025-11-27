# 🛠️ Agent Status Monitor Enhancement Proposal

**Author:** Agent-1 (Integration & Core Systems Specialist)  
**Date:** 2025-11-24  
**Priority:** HIGH  
**Status:** Draft Proposal  

---

## 🎯 Summary

Leverage the **Agent_Cellphone V1 overnight_runner** system to elevate the current **Agent Status Monitor** into a richer, more autonomous operations console. The V1 overnight runner already solved 24/7 autonomous coordination with progressive escalation, real-time dashboards, and multi-channel monitoring. Our current monitor (documented in `docs/captain/AGENT_STATUS_MONITOR_DISCORD_UPDATE.md`) is stable but minimal. This proposal outlines how to merge the best of both worlds.

---

## 📌 Current State (V2 Monitor)

References:
- `docs/captain/AGENT_STATUS_MONITOR_DISCORD_UPDATE.md`
- `docs/captain/RECONFIGURE_MONITOR_FOR_CONTINUOUS_OPERATION.md`
- `src/orchestrators/overnight/monitor.py`

Capabilities:
1. Continuous operation (`max_cycles: 0`, auto-restart)
2. Activity tracking via orchestrator assignments
3. Stall detection (checks every 60s, 5 min timeout)
4. Health + performance tracking toggles
5. Discord notifications (basic status posts)

Limitations:
- No progressive escalation or layered responses
- No GUI/command center for live control
- Limited context in Discord updates
- No democratic decision overlays or playbooks
- No heartbeat visualization or multi-agent summaries

---

## 💡 V1 Overnight Runner Capabilities

Reference: `agent_workspaces/Agent-6/AGENT_CELLPHONE_V1_OVERNIGHT_RUNNER_EXTRACTION.md`

Highlights:
1. **24/7 Autonomous Operation** – Agents 1-5 managed continuously
2. **PyQt Command Center** – Real-time dashboards (`ultimate_agent5_command_center.py`)
3. **FSM-Based Orchestration** – `enhanced_runner.py`, `fsm_bridge.py`
4. **Progressive Escalation** – Escalates from soft nudges → alerts → overrides
5. **Heartbeats & Stall Detection** – File listeners, inbox consumers, heartbeat logging
6. **Playbooks & Onboarding** – 20+ docs covering calibration, troubleshooting, FAQs
7. **Discord Integration** – Smart alerts, mission summaries, recovery prompts

These are exactly the enhancements users are asking for today.

---

## ⚖️ Gap Analysis

| Capability                              | Current Monitor | Overnight Runner | Enhancement Opportunity |
|----------------------------------------|-----------------|------------------|-------------------------|
| Continuous operation                   | ✅ Stable       | ✅ Stable        | Already aligned         |
| Progressive escalation                 | ❌ Missing      | ✅ Mature        | **High impact**         |
| Real-time GUI / command center         | ❌ Missing      | ✅ PyQt5         | Optional, high value    |
| Heartbeat visualization                | Basic (logs)    | ✅ dashboards    | Improve dashboards      |
| Playbooks & operations guide           | Minimal docs    | ✅ Onboarding    | Integrate best docs     |
| Multi-agent summary & democracy        | Basic logging   | ✅ integrated    | Add overlay + insights  |
| Smart Discord updates                  | Static          | ✅ contextual    | Add context + actions   |

---

## 🧭 Proposal Overview

Build a phased enhancement plan that imports the best overnight_runner concepts into V2 while preserving our current stable monitor.

### Phase 1 – **Heartbeat & Escalation Upgrade** (1-2 weeks)
- Import heartbeat logic from `listener.py` + `inbox_consumer.py`
- Add multi-level escalation (warning → alert → intervention)
- Enhance Discord updates with context (who stalled, how long, suggested action)
- Deliverable: `src/orchestrators/overnight/escalation.py` + monitor enhancements

### Phase 2 – **Command Center & Dashboards** (2-3 weeks)
- Adapt PyQt dashboard concepts (`ultimate_agent5_command_center.py`)
- Provide optional GUI for operators (toggle via config)
- Visualize heartbeats, stalls, task assignments, gas levels
- Deliverable: `src/orchestrators/overnight/ui/command_center.py` + docs

### Phase 3 – **Playbooks & Democratic Controls** (1-2 weeks)
- Integrate V1 playbooks (`overnight_runner/onboarding/06_PLAYBOOKS.md`)
- Add “democracy overlay” (e.g., quick actions, gas injection macros)
- Document operations in `docs/captain/OVERNIGHT_MONITOR_PLAYBOOK.md`
- Deliverable: Playbook doc + quick action scripts

---

## 🔧 Implementation Details

### Technical Tasks (Phase 1)
1. **Heartbeat Library** – Extract heartbeat update logic into reusable module
2. **Escalation Engine** – Map V1 escalation levels to V2 actions
3. **Discord Formatter** – Extend monitor to call new escalation summaries
4. **Config Flags** – New `monitoring.escalation: true` toggle in `config/orchestration.yml`

### Technical Tasks (Phase 2)
1. **UI Bridge** – Wrap PyQt command center in optional launcher (`python tools/monitor_command_center.py`)
2. **Data Feed** – Expose monitor metrics via lightweight websocket or shared JSON
3. **Controls** – Provide quick buttons for gas, pause, resume, rescue
4. **Documentation** – How to launch/use the command center

### Technical Tasks (Phase 3)
1. **Playbook Import** – Convert existing overnight_runner onboarding docs into V2 format
2. **Democracy Overlay** – Template for multi-agent consensus actions
3. **Automation Hooks** – Quick access to gas, restarts, queue resets

---

## 📄 Documentation & Deliverables

- `docs/enhancement_requests/AGENT_STATUS_MONITOR_OVERNIGHT_RUNNER_PROPOSAL.md` (this doc)
- Phase-specific design docs (Phase 1/2/3)
- Updated captain docs (`docs/captain/AGENT_STATUS_MONITOR_DISCORD_UPDATE.md`)
- Playbook: `docs/captain/OVERNIGHT_MONITOR_PLAYBOOK.md`
- Operator UI guide (if Phase 2 approved)

---

## ⚠️ Risks & Mitigations

| Risk                                   | Mitigation                                  |
|----------------------------------------|----------------------------------------------|
| GUI adds complexity                    | Make GUI optional via config flag            |
| Escalation spam in Discord             | Rate-limit + combine alerts                  |
| Old PyQt code incompatibility          | Port patterns, not raw code                  |
| Continuous ops stability               | Stage rollout: Phase 1 (headless) first      |

---

## ✅ Next Steps

1. ✅ Proposal submitted for review
2. ⏳ Captain approval for Phase 1 scope
3. ⏳ Assign engineering owner (suggest Agent-6 or Agent-1)
4. ⏳ Schedule sprint work (Phase 1 focus)

With this enhancement, the Agent Status Monitor will move from basic heartbeats to a fully autonomous mission control system inspired by the proven overnight_runner.

*🐝 WE. ARE. SWARM. ⚡🔥*
