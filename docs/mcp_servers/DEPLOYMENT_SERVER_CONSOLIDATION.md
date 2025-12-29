# Deployment Server Consolidation Plan

**Date**: 2025-12-27  
**Agent**: Agent-3  
**Status**: Consolidation needed

---

## 🔍 Current State

**Three Overlapping Deployment Servers:**

1. **`deployment_manager_server.py`**
   - Tools: `check_deployment_status`, `verify_deployment`, `list_deployable_sites`
   - Focus: Status checking and verification

2. **`deployment_verification_server.py`**
   - Tools: `check_deployment_status`, `verify_deployment_integration`, `check_site_status`
   - Focus: Verification and integration checks

3. **`deployment_server.py`** (NEW)
   - Tools: `deploy_wordpress_theme`, `deploy_wordpress_file`, `verify_deployment`, `check_deployment_status`, `check_http_status`, `deploy_analytics_code`
   - Focus: Deployment operations + verification

---

## 🎯 Consolidation Strategy

### **Unified Server: `deployment_server.py`**

**Merge all functionality into single server:**

**Deployment Operations:**
- `deploy_wordpress_theme` - Deploy theme files (from deployment_server.py)
- `deploy_wordpress_file` - Deploy single file (from deployment_server.py)
- `deploy_analytics_code` - Deploy GA4/Pixel (from deployment_server.py)
- `list_deployable_sites` - List configured sites (from deployment_manager_server.py)

**Verification Operations:**
- `verify_deployment` - Verify deployment status (merge from all 3)
- `check_deployment_status` - Check site deployment (merge from all 3)
- `check_http_status` - Check HTTP status (from deployment_server.py)
- `check_site_status` - Check site health (from deployment_verification_server.py)
- `verify_deployment_integration` - Verify integration (from deployment_verification_server.py)

**Result:** Single unified server with all deployment + verification tools

---

## 📋 Implementation Steps

1. **Merge Functions**
   - Combine `verify_deployment` implementations (best features from all 3)
   - Combine `check_deployment_status` implementations
   - Add missing functions to unified server

2. **Update Configuration**
   - Remove `deployment-manager` and `deployment-verification` from config
   - Keep only `deployment` server

3. **Archive Old Servers**
   - Move `deployment_manager_server.py` → `mcp_servers/archived/`
   - Move `deployment_verification_server.py` → `mcp_servers/archived/`

4. **Test Unified Server**
   - Test all tools
   - Verify backward compatibility
   - Update documentation

---

**Status:** 📋 Consolidation plan ready  
**Next:** Merge functions into unified `deployment_server.py`


