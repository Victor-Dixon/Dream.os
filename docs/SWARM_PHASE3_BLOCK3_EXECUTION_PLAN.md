# Swarm Phase 3 - Block 3 Execution Plan

**Agent:** Agent-3 (Infrastructure & DevOps Specialist)  
**Priority:** HIGH  
**Status:** IN PROGRESS  
**Date:** 2025-12-28

---

## 🎯 Block 3 Mission: Critical Deployment & PHP Validation

### Tasks:
1. ✅ **Enhance validation-audit MCP with check_php_syntax** - COMPLETE
2. ⏳ **Resolve TradingRobotPlug.com and Build-In-Public deployment blockers** - IN PROGRESS
3. ⏳ **Configure missing GA4/Pixel IDs in wp-config.php** - PENDING

---

## ✅ Task 1: PHP Syntax Validation MCP Enhancement - COMPLETE

### Implementation:
- **File:** `mcp_servers/validation_audit_server.py`
- **Function:** `check_php_syntax(site_key: str, file_path: str)`
- **Method:** Uses SimpleWordPressDeployer for remote SSH execution of `php -l`
- **Fallback:** Local PHP syntax check if file accessible locally

### Features:
- Remote PHP syntax validation via SSH/WP-CLI
- Line number extraction from error messages
- Error message parsing
- Local fallback for development

### MCP Tool Added:
```json
{
  "name": "check_php_syntax",
  "description": "Check PHP syntax for a remote WordPress file using php -l",
  "inputSchema": {
    "type": "object",
    "properties": {
      "site_key": {"type": "string"},
      "file_path": {"type": "string"}
    },
    "required": ["site_key", "file_path"]
  }
}
```

### Verification:
- ✅ Syntax validation passed
- ✅ Function integrated into MCP server
- ✅ Tool definition added to capabilities

---

## ⏳ Task 2: Resolve Deployment Blockers - IN PROGRESS

### Current Blockers:

#### **TradingRobotPlug.com**
- **Status:** ❌ CODE COMPLETE - DEPLOYMENT PENDING
- **Issue:** Server access credentials needed
- **Files:** 16 theme files + contact page
- **Blocker:** SFTP/SSH credentials not configured

#### **Build-In-Public Phase 0**
- **dadudekc.com:** ❌ CODE COMPLETE - DEPLOYMENT PENDING
  - **Files:** 2 files (front-page.php updates)
  - **Blocker:** Remote WordPress site (no local installation)
  
- **weareswarm.online:** ❌ CODE COMPLETE - DEPLOYMENT PENDING
  - **Files:** 8 files (Manifesto, How the Swarm Works, Build in Public feed)
  - **Blocker:** Remote WordPress site (no local installation)

### Deployment Options:

#### **Option 1: SFTP/File Manager (RECOMMENDED)**
1. Connect to server via SFTP or hosting File Manager
2. Upload files to theme directory
3. Verify deployment

**Requirements:**
- SFTP credentials (host, username, password, port)
- File paths for each site

#### **Option 2: WP-CLI Remote Execution**
1. SSH access to server
2. Execute WP-CLI commands remotely
3. Deploy files via WP-CLI

**Requirements:**
- SSH access
- WP-CLI installed on server

#### **Option 3: WordPress REST API**
1. Use WordPress REST API for file deployment
2. Requires authentication token
3. Limited to content updates (not theme files)

**Requirements:**
- REST API credentials
- Plugin for file management

### Action Plan:

1. **Check for existing credentials:**
   - Check `.deploy_credentials/sites.json`
   - Check `configs/site_configs.json`
   - Check environment variables (HOSTINGER_*)

2. **Coordinate with Captain:**
   - Request SFTP/SSH credentials for:
     - tradingrobotplug.com
     - dadudekc.com
     - weareswarm.online

3. **Deploy files:**
   - Use deployment MCP server or SimpleWordPressDeployer
   - Verify each deployment
   - Check PHP syntax using new validation tool

4. **Verification:**
   - Use `verify_deployment` MCP tool
   - Check for required content markers
   - Validate PHP syntax

---

## ⏳ Task 3: Configure GA4/Pixel IDs - PENDING

### Current Status:

#### **freerideinvestor.com** ✅
- **Code:** Deployed ✅
- **IDs:** ⏳ Needed
- **Location:** `wp/wp-content/themes/freerideinvestor-modern/functions.php`
- **Config:** Requires `GA4_MEASUREMENT_ID` and `FACEBOOK_PIXEL_ID` in wp-config.php

#### **tradingrobotplug.com** ✅
- **Code:** Deployed ✅ (was broken, now fixed)
- **IDs:** ⏳ Needed
- **Location:** `wp/wp-content/themes/tradingrobotplug-theme/functions.php`
- **Config:** Requires `GA4_MEASUREMENT_ID` and `FACEBOOK_PIXEL_ID` in wp-config.php

#### **dadudekc.com** ❌
- **Code:** ⏳ Remote deployment required
- **IDs:** ⏳ Needed (after code deployment)
- **Method:** Manual instructions generated ✅

#### **crosbyultimateevents.com** ❌
- **Code:** ⏳ Remote deployment required
- **IDs:** ⏳ Needed (after code deployment)
- **Method:** Manual instructions generated ✅

### Configuration Template:

```php
// GA4/Pixel Analytics Configuration
define('GA4_MEASUREMENT_ID', 'G-XXXXXXXXXX'); // Replace with actual GA4 ID
define('FACEBOOK_PIXEL_ID', '123456789012345'); // Replace with actual Pixel ID
```

### Action Plan:

1. **Acquire IDs:**
   - Request GA4 Measurement IDs for all 4 sites
   - Request Facebook Pixel IDs for all 4 sites
   - Use template: `docs/website_audits/2026/GA4_PIXEL_ID_REQUEST_TEMPLATE.md`

2. **Configure wp-config.php:**
   - For local sites (freerideinvestor.com, tradingrobotplug.com):
     - Add constants to wp-config.php
     - Use deployment MCP server
   - For remote sites (dadudekc.com, crosbyultimateevents.com):
     - Deploy code first (Task 2)
     - Then configure IDs via SFTP/File Manager

3. **Verification:**
   - Use `check_php_syntax` to validate wp-config.php
   - Use analytics validation tools (Agent-5)
   - Check page source for analytics scripts

---

## 📊 Progress Summary

| Task | Status | Progress |
|------|--------|----------|
| PHP Syntax Validation MCP | ✅ Complete | 100% |
| Deployment Blockers Resolution | ⏳ In Progress | 25% |
| GA4/Pixel ID Configuration | ⏳ Pending | 0% |

---

## 🔗 Dependencies

### Block 2 (Agent-2):
- Staging/snapshot infrastructure (optional - nice to have)

### Block 4 (Agent-5):
- Analytics validation framework (ready)
- WordPress health checks (pending)

### Coordination Needed:
- **Captain (Agent-4):** SFTP/SSH credentials for 3 sites
- **Agent-5:** GA4/Pixel ID acquisition coordination
- **Agent-7:** Deployment coordination (if using WordPress Manager)

---

## 📝 Next Actions

1. **Immediate:**
   - Request SFTP/SSH credentials from Captain
   - Check existing credential files
   - Test PHP syntax validation with known file

2. **Short-term:**
   - Deploy TradingRobotPlug.com theme files
   - Deploy Build-In-Public Phase 0 files
   - Configure GA4/Pixel IDs for deployed sites

3. **Verification:**
   - Run PHP syntax checks on all deployed files
   - Verify deployments using validation-audit MCP
   - Coordinate with Agent-5 for analytics validation

---

**Last Updated:** 2025-12-28  
**Agent:** Agent-3 (Infrastructure & DevOps Specialist)


