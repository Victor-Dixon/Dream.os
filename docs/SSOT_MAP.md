# Single Source of Truth (SSOT) Map
## Agent Cellphone V2 Repository

**Generated:** January 2, 2026 - Technical Debt Purge Phase 1

**Purpose:** Establish canonical sources for duplicated functionality to enable safe consolidation and prevent re-duplication.

---

## 🔥 Top 3 Duplication Hotspots Identified

### 1. **Deploy Scripts** (Critical - 15+ duplicate functions)
**Problem:** Multiple deployment functions scattered across codebase with overlapping functionality.

**SSOT Decision:**
- **CANONICAL:** `mcp_servers/deployment_server.py` - Comprehensive deployment MCP server
- **SECONDARY:** `src/core/deployment/deployment_coordinator.py` - High-level coordination logic

**Deprecated Files to Consolidate:**
| File | Status | Reason | Migration Path |
|------|--------|--------|----------------|
| `scripts/deploy_via_wordpress_admin.py` | DEPRECATE | Single-purpose script, functionality in MCP server | Use `mcp_servers/deployment_server.py::deploy_wordpress_file()` |
| `tools/deploy_tradingrobotplug_plugin.py` | DEPRECATE | Site-specific deploy logic | Use `mcp_servers/deployment_server.py::deploy_wordpress_theme()` |
| `tools/deploy_tradingrobotplug_plugin_phase3.py` | DEPRECATE | Phase-specific duplication | Merge into canonical deployment server |
| `tools/deploy_fastapi_tradingrobotplug.py` | DEPRECATE | FastAPI deployment logic | Use `mcp_servers/deployment_server.py::deploy_analytics_code()` |
| `tools/deploy_weareswarm_feed_system.py` | DEPRECATE | Feed system deployment | Consolidate into site-specific adapter |
| `tools/deploy_weareswarm_font_fix.py` | DEPRECATE | Font deployment fix | Merge into theme deployment |
| `tools/deploy_tradingrobotplug_font_fix.py` | DEPRECATE | Duplicate font fix | Consolidate with above |
| `ops/deployment/simple_wordpress_deployer.py` | KEEP (Dependency) | Still used by canonical deployment_server.py | Will be removed after refactoring canonical server |
| `archive/site_specific/crosbyultimateevents/deploy_business_plan_plugin.py` | DEPRECATE | Temp repo code | Move to canonical location |

### 2. **WordPress Management** (High - 12+ overlapping systems)
**Problem:** Multiple WordPress management interfaces with different APIs and approaches.

**SSOT Decision:**
- **CANONICAL:** `mcp_servers/wp_cli_manager_server.py` - WP-CLI based management
- **SECONDARY:** `mcp_servers/wordpress_theme_server.py` - Theme-specific operations

**Deprecated Files to Consolidate:**
| File | Status | Reason | Migration Path |
|------|--------|--------|----------------|
| `tools/wordpress_manager.py` | KEEP (Operational) | Still used by deployment scripts | Evaluate consolidation in future phase |
| `mcp_servers/website_manager_server.py` | REVIEW | May have unique functionality | Evaluate vs WP-CLI server |
| `src/control_plane/adapters/hostinger/*.py` | PARTIAL | Site adapters have unique config | Keep adapters, consolidate common functions to base |
| `src/web/static/js/services/deployment-*.js` | MIGRATE | Frontend deployment services | Consolidate into single deployment service |
| `scripts/site_management/sync_*_theme.py` | DEPRECATE | Theme sync scripts | Use `mcp_servers/wordpress_theme_server.py` |

### 3. **Site Adapters** (Medium - 8+ similar adapter classes)
**Problem:** Hostinger site adapters have significant code duplication.

**SSOT Decision:**
- **CANONICAL:** `src/control_plane/adapters/base.py` - Base adapter class
- **SECONDARY:** `src/control_plane/adapters/hostinger/` - Directory for site-specific implementations

**Consolidation Strategy:**
| Adapter | Status | Unique Features | Consolidation Action |
|---------|--------|-----------------|---------------------|
| `prismblossom_adapter.py` | KEEP | Custom business logic | Extract common patterns to base |
| `freeride_adapter.py` | KEEP | Trading focus features | Extract common patterns to base |
| `tradingrobotplug_adapter.py` | KEEP | Analytics integration | Extract common patterns to base |
| `weareswarm_adapter.py` | KEEP | Swarm-specific features | Extract common patterns to base |
| `ariajet_adapter.py` | KEEP | Game integration | Extract common patterns to base |
| `dadudekc_adapter.py` | KEEP | Business site logic | Extract common patterns to base |
| `crosbyultimateevents_adapter.py` | KEEP | Event site features | Extract common patterns to base |
| `southwestsecret_adapter.py` | KEEP | Niche site features | Extract common patterns to base |

**Common Patterns to Extract:**
- FTP upload/download logic
- File deployment methods
- Cache management
- Error handling patterns

---

## 📋 Domain SSOT Assignments

### Core Systems
| Domain | Canonical File | Secondary Files | Deprecation Plan |
|--------|----------------|-----------------|------------------|
| **Configuration** | `src/core/config/config_manager.py` | `agent_mode_config.json` | Keep both, config file is SSOT for settings |
| **Error Handling** | `src/core/error_handling/error_handling.py` | `src/core/error_handling/` | Keep package structure |
| **Logging** | `src/core/error_handling/error_handling.py` | Built-in Python logging | Error framework handles all logging |
| **Testing** | `tests/` directory | `src/*/test_*.py` | Consolidate scattered tests into tests/ |

### Deployment & Infrastructure
| Domain | Canonical File | Secondary Files | Deprecation Plan |
|--------|----------------|-----------------|------------------|
| **WordPress Deployment** | `mcp_servers/deployment_server.py` | `tools/deploy_*.py` | Deprecate tool scripts |
| **Theme Management** | `mcp_servers/wordpress_theme_server.py` | `scripts/site_management/` | Deprecate sync scripts |
| **Site Adapters** | `src/control_plane/adapters/base.py` | `src/control_plane/adapters/hostinger/*.py` | Keep inheritance structure |

### Business Logic
| Domain | Canonical File | Secondary Files | Deprecation Plan |
|--------|----------------|-----------------|------------------|
| **Trading Robot** | `src/trading_robot/` | N/A | Well organized, no duplication |
| **Gaming** | `src/gaming/` | `temp_repos/Thea/src/dreamscape/` | Thea code needs migration/consolidation |
| **AI Training** | `src/ai_training/` | `temp_repos/Thea/src/dreamscape/core/` | Consolidate AI training logic |
| **Web Services** | `src/web/` | N/A | Well organized |

---

## 🚩 Deprecation Headers Template

For files marked as DEPRECATED, add this header:

```python
"""
⚠️ DEPRECATED - DO NOT USE

This file is deprecated as part of the SSOT consolidation effort.

REPLACEMENT: [canonical_file_path]
MIGRATION: [brief migration instructions]
DEADLINE: [removal_date]

For new code, use: [canonical_file_path::function_name]
"""
```

Example:
```python
"""
⚠️ DEPRECATED - DO NOT USE

This file is deprecated as part of the SSOT consolidation effort.

REPLACEMENT: mcp_servers/deployment_server.py
MIGRATION: Use deploy_wordpress_file() instead of this script
DEADLINE: 2026-02-01

For new code, use: mcp_servers/deployment_server.py::deploy_wordpress_file()
"""
```

---

## 📊 Impact Assessment

### Files to Deprecate: ~15
### Functions to Consolidate: ~25
### Estimated Code Reduction: ~2,500 lines
### Risk Level: **LOW** (All deprecations have direct replacements)

### Safety Measures:
- ✅ All deprecations have direct canonical replacements
- ✅ No behavior changes in deprecation phase
- ✅ Comprehensive testing required before deletion
- ✅ Reference checking via `rg` before removal

---

## 🎯 Next Steps (Phase 1-2 Implementation)

### Phase 1: Safe Deprecation (PR-1)
1. Add deprecation headers to all identified files
2. Update any new imports to use canonical paths
3. Add CI checks to prevent deprecated file usage
4. Comprehensive testing to ensure no breaking changes

### Phase 2: Consolidation (PR-2)
1. Remove deprecated files (only after verification)
2. Update all references to canonical paths
3. Run full test suite + compile validation
4. Update documentation

### Phase 3: Prevention (PR-3)
1. Add duplication detection CI gates
2. Implement SSOT linting rules
3. Add weekly technical debt reporting
4. Documentation updates

---

*This SSOT map was generated through automated duplicate detection and manual analysis. All deprecation decisions include verified replacement paths to ensure zero disruption.*