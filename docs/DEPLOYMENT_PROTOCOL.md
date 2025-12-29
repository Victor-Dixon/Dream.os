# Deployment Protocol - No Coordination Required

## Core Principle
**ANY AGENT CAN DEPLOY - NO COORDINATION REQUIRED**

Deployment is a technical operation, not a coordination bottleneck. If code is ready and tested, deploy it immediately.

## Deployment Authority

### Who Can Deploy
- **ANY agent** with access to deployment tools
- **NO approval required** from other agents
- **NO coordination** needed before deployment

### When to Deploy
- Code is complete and committed
- Files are ready in the repository
- Site configuration exists in `websites/configs/site_configs.json`
- **Deploy immediately** - don't wait for coordination

## Deployment Tools

### Primary Tool: `simple_wordpress_deployer.py`
Location: `ops/deployment/simple_wordpress_deployer.py`

**Usage:**
```python
from ops.deployment.simple_wordpress_deployer import SimpleWordPressDeployer, load_site_configs

configs = load_site_configs()
deployer = SimpleWordPressDeployer("tradingrobotplug.com", configs)
deployer.connect()
deployer.deploy_file(local_path, remote_path)
deployer.disconnect()
```

### Site Configuration
All sites configured in: `websites/configs/site_configs.json`

**Supported Sites:**
- tradingrobotplug.com
- weareswarm.online
- dadudekc.com
- crosbyultimateevents.com
- freerideinvestor.com
- And all other sites in config

## Deployment Process

### Step 1: Verify Files Ready
- Check files exist in repository
- Verify site config exists
- Confirm credentials available (from .env or config)

### Step 2: Deploy Immediately
- Use `SimpleWordPressDeployer`
- Deploy all ready files
- Report deployment results

### Step 3: Post-Deployment (Optional)
- Notify relevant agents AFTER deployment
- Update task tracking AFTER deployment
- **Don't wait for approval before deploying**

## Anti-Patterns (FORBIDDEN)

### ❌ DON'T:
- Wait for Agent-3 or any specific agent to deploy
- Request coordination before deploying
- Ask for approval before deploying
- Create deployment blockers

### ✅ DO:
- Deploy immediately when code is ready
- Use deployment tools directly
- Report results after deployment
- Fix issues if deployment fails

## Example: TradingRobotPlug.com Deployment

**Before (WRONG):**
```
Agent-7: "Files ready, waiting for Agent-3 to deploy"
Agent-4: "Coordinating with Agent-3 for deployment"
[WAITING...]
```

**After (CORRECT):**
```
Agent-7: "Files ready, deploying now"
[Deploys immediately]
Agent-7: "✅ Deployed 11 files successfully"
```

## Deployment Script Template

```python
#!/usr/bin/env python3
"""Deploy [site] files immediately - no coordination required."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "websites"))

from ops.deployment.simple_wordpress_deployer import SimpleWordPressDeployer, load_site_configs

def main():
    site_key = "[site].com"
    configs = load_site_configs()
    deployer = SimpleWordPressDeployer(site_key, configs)
    
    if not deployer.connect():
        print(f"❌ Failed to connect")
        return 1
    
    # Deploy files
    files_to_deploy = [...]
    for file_name in files_to_deploy:
        local_path = Path(...) / file_name
        remote_path = f"wp-content/themes/[theme]/{file_name}"
        deployer.deploy_file(local_path, remote_path)
    
    deployer.disconnect()
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

## Protocol Enforcement

This protocol is **MANDATORY** for all agents:
- Read this protocol before requesting deployment coordination
- Deploy immediately when code is ready
- Report deployment results, don't wait for approval
- Remove coordination bottlenecks from deployment workflow

## References

- Deployment Tool: `ops/deployment/simple_wordpress_deployer.py`
- Site Configs: `websites/configs/site_configs.json`
- Example Script: `tools/deploy_tradingrobotplug_now.py`

