# Web Domain Security Audit Report
**Date**: 2025-12-13T00:59:04.156548
**Files Checked**: 370

## Summary
- **Total Issues**: 134
- **High Severity**: 16
- **Medium Severity**: 0
- **Low Severity**: 118

## 🔴 High Severity Issues
- **src\discord_commander\README_DISCORD_GUI.md** (line 66): hardcoded_credential
  - Match: `DISCORD_BOT_TOKEN="your_discord_bot_token_here"`
- **src\discord_commander\README_DISCORD_GUI.md** (line 67): hardcoded_credential
  - Match: `DISCORD_BOT_TOKEN="your_discord_bot_token_here"`
- **src\discord_commander\README_DISCORD_GUI.md** (line 128): hardcoded_credential
  - Match: `DISCORD_BOT_TOKEN="your_bot_token"`
- **src\discord_commander\README_DISCORD_GUI.md** (line 66): hardcoded_credential
  - Match: `TOKEN="your_discord_bot_token_here"`
- **src\discord_commander\README_DISCORD_GUI.md** (line 67): hardcoded_credential
  - Match: `TOKEN="your_discord_bot_token_here"`
- **src\discord_commander\README_DISCORD_GUI.md** (line 128): hardcoded_credential
  - Match: `TOKEN="your_bot_token"`
- **src\discord_commander\README_DISCORD_GUI.md** (line 178): hardcoded_credential
  - Match: `token="your_token"`
- **src\web\static\js\architecture\web-service-registry-module.js** (line 37): hardcoded_credential
  - Match: `token: 'dashboardRepository'`
- **src\web\static\js\architecture\web-service-registry-module.js** (line 38): hardcoded_credential
  - Match: `token: 'dashboardService'`
- **src\web\static\js\architecture\web-service-registry-module.js** (line 39): hardcoded_credential
  - Match: `token: 'dashboardStateManager'`
- **src\web\static\js\architecture\web-service-registry-module.js** (line 65): hardcoded_credential
  - Match: `token: 'testingRepository'`
- **src\web\static\js\architecture\web-service-registry-module.js** (line 66): hardcoded_credential
  - Match: `token: 'testingService'`
- **src\web\static\js\architecture\web-service-registry-module.js** (line 92): hardcoded_credential
  - Match: `token: 'deploymentRepository'`
- **src\web\static\js\architecture\web-service-registry-module.js** (line 93): hardcoded_credential
  - Match: `token: 'deploymentService'`
- **src\web\static\js\architecture\web-service-registry-module.js** (line 119): hardcoded_credential
  - Match: `token: 'loggingUtils'`
- **src\web\static\js\architecture\web-service-registry-module.js** (line 120): hardcoded_credential
  - Match: `token: 'validationUtils'`

## 🟢 Low Severity Issues
- **src\web\static\js\agent-coordination-manager.js** (line 31): console.log found in production code
- **src\web\static\js\agent-coordination-manager.js** (line 41): console.log found in production code
- **src\web\static\js\dashboard-alerts.js** (line 17): console.log found in production code
- **src\web\static\js\dashboard-communication.js** (line 41): console.log found in production code
- **src\web\static\js\dashboard-communication.js** (line 64): console.log found in production code
- **src\web\static\js\dashboard-communication.js** (line 142): console.log found in production code
- **src\web\static\js\dashboard-communication.js** (line 155): console.log found in production code
- **src\web\static\js\dashboard-communication.js** (line 237): console.log found in production code
- **src\web\static\js\dashboard-config-manager.js** (line 75): console.log found in production code
- **src\web\static\js\dashboard-config-manager.js** (line 117): console.log found in production code
- ... and 108 more low severity issues
