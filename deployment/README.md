# 🚀 Deployment Architecture

## Overview

This repository follows a **monorepo + deployment pipeline** pattern to eliminate duplication between development and production environments.

## Architecture

```
Agent_Cellphone_V2_Repository/          # ← Canonical source (development)
├── packages/                          # ← Shared components
│   ├── trading-robot-plugin/          # ← Versioned plugin package
│   ├── trading-robot-theme/           # ← Versioned theme package
│   └── shared-utils/                  # ← Shared utilities
├── sites/                             # ← Site-specific code
│   ├── tradingrobotplug.com/          # ← Site configuration
│   └── freerideinvestor.com/          # ← Site configuration
├── deployment/                        # ← Deployment scripts
│   ├── deploy.ps1                     # ← Main deployment script
│   ├── package-deploy.ps1             # ← Package deployment
│   └── site-sync.ps1                  # ← Site synchronization
└── docs/
    └── deployment-guide.md
```

## Key Principles

### 🎯 Single Source of Truth
- **Repository** = Canonical source for all code
- **Live sites** = Deployed instances only
- **No manual editing** of live site files

### 📦 Package-Based Architecture
- **Reusable components** packaged as deployable artifacts
- **Versioned releases** for stability
- **Dependency management** between packages

### 🚀 Deployment Pipeline
- **Automated deployment** from repository to live sites
- **Environment-specific configs** applied during deployment
- **Rollback capability** for failed deployments

## Workflow

### Development
1. Make changes in repository
2. Test locally
3. Create versioned packages (if needed)
4. Deploy to staging/live

### Deployment
1. Run deployment script
2. Script syncs packages to live sites
3. Applies site-specific configurations
4. Verifies deployment success

## File Synchronization

### What Gets Synced
- ✅ **Packages**: Plugin/theme code from `packages/`
- ✅ **Site configs**: Environment-specific settings
- ✅ **Shared utilities**: Common functionality

### What Stays Local
- ❌ **User data**: wp-content/uploads/
- ❌ **Logs**: Error/debug logs
- ❌ **Cache**: Cached files
- ❌ **Database**: wp-config.php database settings

## Commands

```bash
# Deploy all sites
.\deployment\deploy.ps1 -All

# Deploy specific site
.\deployment\deploy.ps1 -Site tradingrobotplug.com

# Deploy specific package
.\deployment\deploy.ps1 -Package trading-robot-plugin

# Dry run
.\deployment\deploy.ps1 -All -DryRun
```