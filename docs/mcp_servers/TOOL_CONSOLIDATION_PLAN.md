# Tool Consolidation Plan - Centralized MCP Servers

**Date**: 2025-12-27  
**Agent**: Agent-3 (Infrastructure & DevOps Specialist)  
**Status**: CONSOLIDATION PLAN

---

## 🎯 Objective

Replace scattered tools in `tools/` directory with centralized MCP servers that provide consistent, accessible interfaces for common operations.

---

## 📊 Current State Analysis

### **Scattered Tools Identified:**

**Deployment & Verification (15+ tools):**
- `deploy_tradingrobotplug_theme*.py` (5 variants)
- `deploy_ga4_pixel_*.py` (2 variants)
- `deploy_build_in_public_phase0.py`
- `deploy_dadudekc_tier1_quick_wins.py`
- `deploy_website_optimizations.py`
- `verify_*.py` (10+ verification tools)
- `deployment_verification_tool.py`
- `deployment_status_checker.py`

**Devlog Management (8+ tools):**
- `devlog_poster.py`
- `devlog_poster_agent_channel.py`
- `devlog_manager.py`
- `devlog_auto_poster.py`
- `devlog_compliance_validator.py`
- `post_agent*_devlog_to_discord.py` (multiple)

**Coordination & Status (10+ tools):**
- `a2a_coordination_queue.py`
- `a2a_coordination_validator.py`
- `coordination_status_dashboard.py`
- `coordination_status_tracker.py`
- `identify_coordination_opportunities.py`
- `debug_status_check.py`

**Website Management (20+ tools):**
- `check_*.py` (multiple check tools)
- `fix_*.py` (multiple fix tools)
- `audit_*.py` (multiple audit tools)
- Website-specific tools scattered

**Git & CI (10+ tools):**
- `check_open_prs.py`
- `check_pr_merge_status.py`
- `create_new_pr.py`
- `merge_pr_*.py` (multiple)
- `configure_git_auth.py`

---

## 🏗️ Proposed MCP Server Consolidation

### **1. Deployment & Verification Server** (NEW)

**Consolidates:**
- All `deploy_*.py` tools
- All `verify_*.py` tools
- `deployment_verification_tool.py`
- `deployment_status_checker.py`

**MCP Tools:**
- `deploy_wordpress_theme` - Deploy theme files to WordPress
- `deploy_wordpress_file` - Deploy single file to WordPress
- `verify_deployment` - Verify deployment status
- `check_deployment_status` - Check deployment health
- `deploy_analytics_code` - Deploy GA4/Pixel code
- `verify_page_content` - Verify page content matches requirements
- `check_http_status` - Check HTTP status codes

**Benefits:**
- Single interface for all deployment operations
- Consistent error handling
- Centralized logging
- Reusable across all sites

---

### **2. Devlog Management Server** (NEW)

**Consolidates:**
- All `devlog_*.py` tools
- All `post_*_devlog_*.py` tools
- `devlog_manager.py`
- `devlog_auto_poster.py`

**MCP Tools:**
- `create_devlog_entry` - Create new devlog entry
- `post_devlog_to_discord` - Post devlog to Discord
- `validate_devlog_format` - Validate devlog compliance
- `get_agent_devlogs` - Get devlogs for agent
- `auto_post_new_devlogs` - Auto-post new devlogs (watch mode)
- `generate_devlog_feed` - Generate devlog feed content

**Benefits:**
- Centralized devlog operations
- Consistent formatting
- Automated posting
- Compliance validation

---

### **3. Coordination & Status Server** (NEW)

**Consolidates:**
- All `a2a_coordination_*.py` tools
- All `coordination_*.py` tools
- `identify_coordination_opportunities.py`
- `debug_status_check.py`

**MCP Tools:**
- `send_coordination_message` - Send A2A coordination message
- `get_coordination_status` - Get coordination status dashboard
- `track_coordination` - Track coordination progress
- `identify_coordination_opportunities` - Find coordination needs
- `get_agent_status` - Get agent status.json
- `update_agent_status` - Update agent status.json

**Benefits:**
- Unified coordination interface
- Status tracking
- Opportunity identification
- Agent status management

---

### **4. Website Operations Server** (EXTEND existing website-manager)

**Extends:** `mcp_servers/website_manager_server.py`

**Adds Tools:**
- `check_website_status` - Check website HTTP status
- `audit_website` - Run website audit
- `fix_website_issue` - Fix common website issues
- `verify_page_content` - Verify page content
- `check_wordpress_errors` - Check WordPress errors
- `deploy_website_file` - Deploy file to website

**Consolidates:**
- All `check_*.py` website tools
- All `fix_*.py` website tools
- All `audit_*.py` website tools
- Website-specific verification tools

**Benefits:**
- Extends existing server
- Centralizes website operations
- Consistent error handling

---

### **5. Git Operations Server** (EXTEND existing git-operations)

**Extends:** `mcp_servers/git_operations_server.py`

**Adds Tools:**
- `create_pull_request` - Create new PR
- `check_pr_status` - Check PR merge status
- `merge_pull_request` - Merge PR
- `list_open_prs` - List open PRs
- `configure_git_auth` - Configure git authentication

**Consolidates:**
- `check_open_prs.py`
- `check_pr_merge_status.py`
- `create_new_pr.py`
- `merge_pr_*.py` tools
- `configure_git_auth.py`

**Benefits:**
- Extends existing server
- Complete git workflow
- PR management

---

### **6. Analytics & Configuration Server** (NEW)

**Consolidates:**
- `analytics_validation_scheduler.py`
- `configuration_sync_checker.py`
- `check_ga4_pixel_configuration.py`
- `automated_p0_analytics_validation.py`
- `validate_analytics_ssot.py`

**MCP Tools:**
- `check_analytics_configuration` - Check GA4/Pixel config
- `validate_analytics_setup` - Validate analytics setup
- `schedule_analytics_validation` - Schedule validation checks
- `check_configuration_sync` - Check wp-config.php sync
- `validate_analytics_ssot` - Validate analytics SSOT

**Benefits:**
- Centralized analytics operations
- Configuration management
- Validation scheduling

---

## 📋 Implementation Plan

### **Phase 1: Create New MCP Servers (P0)**

1. **Deployment & Verification Server**
   - Create `mcp_servers/deployment_server.py`
   - Consolidate all deployment tools
   - Consolidate all verification tools
   - Add to `all_mcp_servers.json`

2. **Devlog Management Server**
   - Create `mcp_servers/devlog_server.py`
   - Consolidate all devlog tools
   - Add to `all_mcp_servers.json`

3. **Coordination & Status Server**
   - Create `mcp_servers/coordination_server.py`
   - Consolidate coordination tools
   - Add to `all_mcp_servers.json`

### **Phase 2: Extend Existing Servers (P1)**

4. **Extend Website Manager Server**
   - Add website operations tools
   - Consolidate check/fix/audit tools

5. **Extend Git Operations Server**
   - Add PR management tools
   - Consolidate git tools

6. **Create Analytics Server**
   - Create `mcp_servers/analytics_server.py`
   - Consolidate analytics tools

### **Phase 3: Migration & Cleanup (P2)**

7. **Migrate Tool Usage**
   - Update agent code to use MCP servers
   - Replace direct tool calls with MCP calls

8. **Archive Old Tools**
   - Move consolidated tools to `tools/archived/`
   - Update documentation
   - Remove from active use

---

## 🎯 Server Structure

### **Deployment & Verification Server**

```python
# mcp_servers/deployment_server.py

Tools:
- deploy_wordpress_theme(site_key, theme_files, options)
- deploy_wordpress_file(site_key, file_path, destination)
- verify_deployment(site_key, page_url, requirements)
- check_deployment_status(site_key)
- deploy_analytics_code(site_key, analytics_config)
- verify_page_content(url, required_content)
- check_http_status(url)
```

### **Devlog Management Server**

```python
# mcp_servers/devlog_server.py

Tools:
- create_devlog_entry(agent_id, content, tags)
- post_devlog_to_discord(devlog_path, channel)
- validate_devlog_format(devlog_path)
- get_agent_devlogs(agent_id, date_range)
- auto_post_new_devlogs(agent_id, watch_mode)
- generate_devlog_feed(output_format)
```

### **Coordination & Status Server**

```python
# mcp_servers/coordination_server.py

Tools:
- send_coordination_message(recipient, message, priority)
- get_coordination_status(agent_filter, status_filter)
- track_coordination(coordination_id, updates)
- identify_coordination_opportunities()
- get_agent_status(agent_id)
- update_agent_status(agent_id, updates)
```

---

## 📊 Tool Mapping

### **Deployment Tools → Deployment Server**

| Current Tool | MCP Tool | Status |
|-------------|----------|--------|
| `deploy_tradingrobotplug_theme.py` | `deploy_wordpress_theme` | → Consolidate |
| `deploy_ga4_pixel_analytics.py` | `deploy_analytics_code` | → Consolidate |
| `verify_trp_web04_deployment.py` | `verify_deployment` | → Consolidate |
| `deployment_verification_tool.py` | `verify_deployment` | → Consolidate |
| `deployment_status_checker.py` | `check_deployment_status` | → Consolidate |

### **Devlog Tools → Devlog Server**

| Current Tool | MCP Tool | Status |
|-------------|----------|--------|
| `devlog_poster.py` | `post_devlog_to_discord` | → Consolidate |
| `devlog_manager.py` | `create_devlog_entry` | → Consolidate |
| `devlog_auto_poster.py` | `auto_post_new_devlogs` | → Consolidate |
| `devlog_compliance_validator.py` | `validate_devlog_format` | → Consolidate |

### **Coordination Tools → Coordination Server**

| Current Tool | MCP Tool | Status |
|-------------|----------|--------|
| `a2a_coordination_queue.py` | `send_coordination_message` | → Consolidate |
| `coordination_status_dashboard.py` | `get_coordination_status` | → Consolidate |
| `coordination_status_tracker.py` | `track_coordination` | → Consolidate |

---

## 🚀 Implementation Steps

### **Step 1: Create Deployment Server**

1. Create `mcp_servers/deployment_server.py`
2. Extract common deployment logic from scattered tools
3. Create unified deployment interface
4. Add verification tools
5. Test with existing deployment workflows

### **Step 2: Create Devlog Server**

1. Create `mcp_servers/devlog_server.py`
2. Consolidate devlog posting logic
3. Add validation and formatting
4. Implement auto-posting
5. Test with agent devlogs

### **Step 3: Create Coordination Server**

1. Create `mcp_servers/coordination_server.py`
2. Consolidate coordination message sending
3. Add status tracking
4. Implement opportunity identification
5. Test with A2A coordination

### **Step 4: Extend Existing Servers**

1. Extend `website_manager_server.py` with operations tools
2. Extend `git_operations_server.py` with PR tools
3. Create `analytics_server.py` for analytics operations

### **Step 5: Migration**

1. Update agent code to use MCP servers
2. Replace tool calls with MCP calls
3. Archive old tools
4. Update documentation

---

## 📈 Benefits

1. **Centralization**
   - Single source of truth for operations
   - Consistent interfaces
   - Easier maintenance

2. **Accessibility**
   - Available via MCP protocol
   - Can be called from any agent
   - Standardized error handling

3. **Maintainability**
   - Fewer files to maintain
   - Centralized bug fixes
   - Easier testing

4. **Consistency**
   - Uniform error handling
   - Standardized logging
   - Consistent return formats

---

## 🎯 Priority Order

1. **P0 - Critical:**
   - Deployment & Verification Server
   - Devlog Management Server

2. **P1 - High:**
   - Coordination & Status Server
   - Extend Website Manager Server

3. **P2 - Medium:**
   - Extend Git Operations Server
   - Analytics & Configuration Server

4. **P3 - Low:**
   - Migration and cleanup
   - Archive old tools

---

**Status:** 📋 CONSOLIDATION PLAN READY  
**Next:** Create first consolidated MCP server (Deployment & Verification)


