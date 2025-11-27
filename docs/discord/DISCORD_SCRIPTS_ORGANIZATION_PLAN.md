# Discord Scripts Organization Plan

**Date**: 2025-01-27  
**Author**: Agent-7 (Web Development Specialist)  
**Status**: 📋 RECOMMENDATIONS

---

## 🎯 Organization Principles

- **`tools/`**: Utility scripts, helpers, automation tools
- **`scripts/`**: Execution scripts, setup scripts, one-off scripts
- **SSOT**: Single Source of Truth should be in `tools/` (utility/helper)

---

## ✅ KEEP IN `tools/` (Already Correct)

1. ✅ **`tools/start_discord_system.py`** - **SSOT** (Main entry point)
2. ✅ **`tools/start_message_queue_processor.py`** - Queue processor (used by SSOT)

---

## 🔄 MOVE TO `tools/` (Dependency of SSOT)

1. **`scripts/run_unified_discord_bot_with_restart.py`** → **`tools/run_unified_discord_bot_with_restart.py`**
   - **Reason**: Dependency of SSOT, should be co-located
   - **Action**: Move file and update SSOT reference

---

## ❌ DELETE (Deprecated - All Redirect to SSOT)

All these scripts are deprecated and redirect to SSOT. They should be deleted:

1. ❌ **`scripts/start_discord_bot.py`** - DELETE
2. ❌ **`scripts/run_unified_discord_bot.py`** - DELETE
3. ❌ **`scripts/run_discord_bot.py`** - DELETE
4. ❌ **`scripts/run_discord_commander.py`** - DELETE
5. ❌ **`scripts/run_discord_messaging.py`** - DELETE
6. ❌ **`scripts/execution/run_discord_bot.py`** - DELETE

---

## 📊 Final Structure

### **`tools/`** (Discord System):
```
tools/
├── start_discord_system.py              # SSOT - Main entry point
├── start_message_queue_processor.py      # Queue processor
└── run_unified_discord_bot_with_restart.py  # Bot runner (moved from scripts/)
```

### **`scripts/`** (Discord):
```
scripts/
└── (all Discord startup scripts deleted)
```

---

## 🔄 Migration Steps

1. **Move dependency**:
   ```bash
   mv scripts/run_unified_discord_bot_with_restart.py tools/
   ```

2. **Update SSOT reference**:
   - Update `tools/start_discord_system.py` to reference new location

3. **Delete deprecated scripts**:
   - Delete all 6 deprecated scripts

4. **Update any documentation**:
   - Update references to moved/deleted scripts

---

## ✅ Benefits

- **Cleaner structure**: All Discord system scripts in one place (`tools/`)
- **No confusion**: Only one way to start the system
- **Easier maintenance**: Related scripts co-located
- **SSOT principle**: Single entry point, clear dependencies

---

**🐝 WE. ARE. SWARM. ⚡🔥**

