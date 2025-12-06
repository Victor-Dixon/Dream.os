# Agent Toolbelt - SSOT Documentation

**Last Updated**: 2025-12-04  
**SSOT Domain**: Communication  
**Maintainer**: Agent-6 (Coordination & Communication Specialist)

---

## 🎯 Purpose

The Agent Toolbelt provides unified CLI access to **60+ development, QA, and coordination tools** through a single command interface. This documentation serves as the **Single Source of Truth (SSOT)** for all toolbelt tools.

---

## 🚀 Quick Start

### List All Tools
```bash
python -m tools.toolbelt --list
```

### Get Help
```bash
python -m tools.toolbelt --help
```

### Run a Tool
```bash
python -m tools.toolbelt --scan
python -m tools.toolbelt --v2-check
python -m tools.toolbelt --agent-status
```

---

## 📚 Documentation Structure

- **[TOOL_REGISTRY.md](./TOOL_REGISTRY.md)** - Complete tool registry with flags, modules, and descriptions
- **[MAINTENANCE.md](./MAINTENANCE.md)** - Rules for keeping registry current
- **[CLI_SNAPSHOT.md](./CLI_SNAPSHOT.md)** - Snapshot of CLI help output (for verification)

---

## 📊 Tool Categories

1. **Core Project Analysis** (9 tools) - Project scanning, V2 compliance, complexity analysis
2. **QA & Validation** (12 tools) - Testing, coverage, validation, quality checks
3. **Agent Coordination** (6 tools) - Status monitoring, messaging, task management
4. **Code Refactoring** (5 tools) - Module extraction, pattern extraction, refactoring
5. **Architecture & Integration** (8 tools) - Architecture reviews, integration validation
6. **Consolidation & Repository** (7 tools) - Repository analysis, consolidation tracking
7. **Agent & Captain** (5 tools) - Agent management, task assignment
8. **Discord & Messaging** (5 tools) - Discord bot, message queue management
9. **Workflow & Automation** (5 tools) - Onboarding, devlogs, auto-tracking
10. **Masterpiece Tools** (2 tools) - Swarm orchestrator, mission control
11. **Utility & Helper** (4 tools) - Health monitoring, cleanup utilities

**Total**: 60+ tools

---

## 🔍 Finding Tools

### By Category
See [TOOL_REGISTRY.md](./TOOL_REGISTRY.md) for tools organized by category.

### By Flag
Use `python -m tools.toolbelt --help` to see all available flags.

### By Module
See [TOOL_REGISTRY.md](./TOOL_REGISTRY.md) for module paths.

---

## ⚠️ SSOT Compliance

- **Registry Updates**: Any new tool MUST be added to `tools/toolbelt_registry.py` AND `docs/toolbelt/TOOL_REGISTRY.md`
- **Verification**: Run `python -m tools.toolbelt --list` to verify registry matches CLI
- **Maintenance**: See [MAINTENANCE.md](./MAINTENANCE.md) for update rules

---

## 🎯 Top Daily Commands

### For Development
- `--scan` - Project analysis
- `--v2-check` - V2 compliance
- `--agent-status` - Check agent statuses

### For Troubleshooting
- `--queue-status` - Check message queue
- `--workspace-health` - Check workspace health
- `--discord-verify` - Verify Discord bot

---

**SSOT Documentation** ✅  
**Maintained by**: Agent-6  
**Domain**: Communication

🐝 **WE. ARE. SWARM. ⚡🔥**

