# Agent Toolbelt - Daily Operator Cheat Sheet

**Last Updated**: 2025-12-04  
**Purpose**: Quick reference for daily operations  
**Target**: 12 commands by scenario

---

## 🎯 Quick Reference

### **Scenario 1: Start Your Day** (3 commands)

```bash
# Check agent statuses
python -m tools.toolbelt --agent-status

# Check workspace health
python -m tools.toolbelt --workspace-health

# Get next task
python -m tools.toolbelt --get-task
```

---

### **Scenario 2: Development Workflow** (3 commands)

```bash
# Scan project
python -m tools.toolbelt --scan

# Check V2 compliance
python -m tools.toolbelt --v2-check

# Verify work completion
python -m tools.toolbelt --verify-complete
```

---

### **Scenario 3: Troubleshooting** (3 commands)

```bash
# Check message queue
python -m tools.toolbelt --queue-status

# Verify Discord running
python -m tools.toolbelt --discord-verify

# Diagnose issues
python -m tools.toolbelt --queue-diagnose
```

---

### **Scenario 4: Ship & Deploy** (3 commands)

```bash
# Run QA checklist
python -m tools.toolbelt --qa-checklist

# Check test coverage
python -m tools.toolbelt --coverage-check

# Verify integration
python -m tools.toolbelt --check-integration
```

---

## 📊 Command Matrix

| Scenario | Command | Purpose |
|----------|---------|---------|
| **Start Day** | `--agent-status` | Check all agent statuses |
| **Start Day** | `--workspace-health` | Verify workspace health |
| **Start Day** | `--get-task` | Claim next task |
| **Development** | `--scan` | Project analysis |
| **Development** | `--v2-check` | V2 compliance |
| **Development** | `--verify-complete` | Verify work done |
| **Troubleshooting** | `--queue-status` | Check message queue |
| **Troubleshooting** | `--discord-verify` | Verify Discord bot |
| **Troubleshooting** | `--queue-diagnose` | Diagnose queue issues |
| **Ship & Deploy** | `--qa-checklist` | QA validation |
| **Ship & Deploy** | `--coverage-check` | Test coverage |
| **Ship & Deploy** | `--check-integration` | Integration health |

---

## 🚀 Masterpiece Tools

### **Swarm Orchestrator** (The Gas Station)
```bash
python -m tools.toolbelt --orchestrate
```

### **Mission Control** (Complete Workflow)
```bash
python -m tools.toolbelt --mission-control
```

---

## 💡 Pro Tips

- **Short Flags**: Use `-s` for `--scan`, `-v` for `--v2-check`, `-l` for `--leaderboard`
- **Help**: `python -m tools.toolbelt --help` shows all tools
- **List**: `python -m tools.toolbelt --list` shows tool names and flags

---

**Daily Cheat Sheet** ✅  
**12 Commands**: 4 scenarios × 3 commands  
**Purpose**: Quick daily operations

🐝 **WE. ARE. SWARM. ⚡🔥**

