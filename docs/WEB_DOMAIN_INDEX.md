# Web Domain Navigation Index

<!-- SSOT Domain: web -->

**Purpose:** Quick navigation reference for all web domain files and documentation

---

## 📁 Directory Structure

### Core Web Routes (`src/web/`)

| File | Purpose | Lines | Related Files |
|------|---------|-------|---------------|
| `messaging_routes.py` | Message queue and delivery endpoints | - | `messaging_handlers.py` |
| `messaging_handlers.py` | Message processing logic | - | `messaging_template_handlers.py` |
| `messaging_template_handlers.py` | Template-based message generation | - | `templates/` |
| `coordination_routes.py` | Agent coordination endpoints | - | `coordination_handlers.py` |
| `task_routes.py` | Task management endpoints | - | `task_handlers.py` |
| `contract_routes.py` | Contract system endpoints | - | `contract_handlers.py` |
| `monitoring_routes.py` | System monitoring endpoints | - | `monitoring_handlers.py` |
| `vision_routes.py` | Computer vision endpoints | - | `vision_handlers.py` |
| `discord_routes.py` | Discord integration endpoints | - | `discord_handlers.py` |

### Vector Database (`src/web/vector_database/`)

| File | Purpose | Lines | Related Files |
|------|---------|-------|---------------|
| `message_routes.py` | Activity tracking API | - | `handlers.py` |
| `routes.py` | Core vector DB routes | - | `handlers.py`, `middleware.py` |
| `handlers.py` | Request handlers | - | `utils.py` |
| `middleware.py` | Request/response middleware | - | `unified_middleware.py` |
| `search_utils.py` | Search utilities | - | `collection_utils.py` |
| `analytics_utils.py` | Analytics helpers | - | - |

### Frontend JavaScript (`src/web/static/js/`)

| File | Purpose | Related Files |
|------|---------|---------------|
| `dashboard.js` | Main dashboard entry | All `dashboard-*.js` files |
| `dashboard-view-activity.js` | Agent activity view | `dashboard-view-renderer.js` |
| `dashboard-view-messages.js` | Message queue view | `dashboard-data-manager.js` |
| `dashboard-view-overview.js` | System overview | `dashboard-charts.js` |
| `dashboard-navigation.js` | View navigation | `dashboard-state-manager.js` |
| `dashboard-socket-manager.js` | WebSocket connections | `dashboard-data-operations.js` |

### Dashboard Subdirectories

| Directory | Purpose |
|-----------|---------|
| `architecture/` | Dependency injection, pattern coordination |
| `core/` | Core utilities and base classes |
| `services/` | Service layer implementations (31 files) |
| `trading-robot/` | Trading robot integration (31 files) |
| `utilities/` | Helper functions |
| `validation/` | Input validation |
| `vector-database/` | Vector DB frontend |

---

## 🔗 Related Documentation

### Protocols & Standards

| Document | Path | Purpose |
|----------|------|---------|
| Documentation Standards | `.cursor/rules/documentation.mdc` | Doc requirements |
| Messaging Contracts | `.cursor/rules/messaging-contracts.mdc` | Message system contracts |
| V2 Compliance | `.cursor/rules/v2-compliance.mdc` | Code quality standards |
| Git Hygiene | `.cursor/rules/git-hygiene.mdc` | Commit standards |

### Website Documentation

| Document | Path | Purpose |
|----------|------|---------|
| Strategic P0 Framework | `docs/website_audits/2026/STRATEGIC_P0_PRIORITIZATION_FRAMEWORK_2025-12-25.md` | Website fix priorities |
| P0 Fix Tracking | `docs/website_audits/2026/P0_FIX_TRACKING.md` | Progress tracking |
| Website Audits | `docs/website_audits/2026/` | Audit reports directory |

### Tools Reference

| Tool | Path | Purpose |
|------|------|---------|
| Devlog Poster | `tools/devlog_poster.py` | Post devlogs to Discord |
| Grade Card Auditor | `tools/audit_websites_grade_cards.py` | Website quality audits |
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console

---

## 🌐 Website Repositories

### Main Themes (`D:\websites\`)

| Site | Theme Path | Status |
|------|------------|--------|
| freerideinvestor.com | `FreeRideInvestor/` | Active (auto-deploy) |
| tradingrobotplug.com | `sites/tradingrobotplug.com/wp/theme/tradingrobotplug-theme/` | Pending deploy |
| dadudekc.com | `sites/dadudekc.com/wp/theme/dadudekc/` | Pending deploy |
| crosbyultimateevents.com | `sites/crosbyultimateevents.com/wp/theme/crosbyultimateevents/` | Pending deploy |
| weareswarm.online | `sites/weareswarm.online/wp/theme/swarm/` | Pending deploy |

### Site Configuration


---

## 🔧 Common Operations

### Deploy Website Changes
```bash
# Auto-deploy (via pre-commit hook)
git add <files> && git commit -m "message"

# Manual deploy (if needed)
=======
python mcp_servers/deployment_server.py --site <sitename>
>>>>>>> origin/codex/build-tsla-morning-report-system
```

### Post Devlog
```bash
python tools/devlog_poster.py --agent Agent-7 --file <devlog_path>
```

### Run Website Audit
```bash
python tools/audit_websites_grade_cards.py --site <domain>
```

### Check Flask API Health
```bash
curl http://localhost:5000/api/health
```

---

## 📊 Key API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/messages/activity` | GET | Agent activity data |
| `/api/messages/queue` | GET | Message queue status |
| `/api/agents/status` | GET | All agent statuses |
| `/api/contracts` | GET | Contract system data |
| `/api/health` | GET | System health check |

---

## 🏷️ SSOT Domain Tags

All Python files in `src/web/` should include:

```python
"""
Module description

<!-- SSOT Domain: web -->

...
"""
```

**Tagged Files:** 65 (as of 2025-12-27)
**Coverage:** ~95% of Python files

---

## 📌 Quick Links

- **Agent-7 Status:** `agent_workspaces/Agent-7/status.json`
- **Agent-7 Devlogs:** `agent_workspaces/Agent-7/devlogs/`
- **Master Task Log:** `MASTER_TASK_LOG.md`
- **Web Domain Rules:** `.cursor/rules/` (always-applied)

---

*Created by Agent-7 | Web Development Specialist*

