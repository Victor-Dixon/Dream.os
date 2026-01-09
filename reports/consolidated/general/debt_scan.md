# Technical Debt Scan Report

**Generated:** 2026-01-02 04:50:34

## Executive Summary

**Technical Debt Score:** 64/100 (MEDIUM)
**Total Files:** 9,964
**Lines of Code:** 1,598,996
**Test Coverage:** 0.0% (0 tests)
**Error Rate (24h):** 11.1%

## Detailed Metrics

| Metric | Value | Status |
|--------|-------|--------|
| Duplicate Groups | 740 | ❌ |
| Syntax Errors | 0 | ✅ |
| SSOT Violations | 179 | ❌ |
| Largest File | 128KB | ✅ |
| Avg File Size | 7.2KB | ✅ |

## Issues Found

### SSOT Violations
- `docs\V2_COMPLIANCE_EXCEPTIONS.md`: references deprecated `tools/wordpress_manager.py`
- `docs\MCP_DEPLOYMENT_STAGING_ROLLBACK.md`: references deprecated `ops/deployment/simple_wordpress_deployer.py`
- `docs\LEGACY_WEBSITES_DIRECTORIES_EXPLANATION.md`: references deprecated `tools/deploy_fastapi_tradingrobotplug.py`
- `docs\LEGACY_WEBSITES_DIRECTORIES_EXPLANATION.md`: references deprecated `tools/deploy_weareswarm_feed_system.py`
- `docs\SSOT_MAP.md`: references deprecated `scripts/deploy_via_wordpress_admin.py`
- ... and 174 more

### Duplicate Groups

#### 93 files (10 bytes)
- `artifacts\2025-12-12_agent-5_analytics-import-validation-results.md`
- `devlogs\2025-12-11_agent-5_ci-cd-failure-diagnosis.md`
- `devlogs\2025-12-11_agent-5_communication-domain-audit.md`
- ... and 90 more

#### 3 files (3,109 bytes)
- `agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\src\dreamscape\core\memory\api\conversation_api.py`
- `phase3b_backup\archive\dreamscape_project\Thea\src\dreamscape\core\memory\api\conversation_api.py`
- `phase3b_backup\systems\memory\memory\api\conversation_api.py`

#### 3 files (9,439 bytes)
- `agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\src\dreamscape\core\memory\storage\conversation_operations.py`
- `phase3b_backup\archive\dreamscape_project\Thea\src\dreamscape\core\memory\storage\conversation_operations.py`
- `phase3b_backup\systems\memory\memory\storage\conversation_operations.py`
