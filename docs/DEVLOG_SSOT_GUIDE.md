# 📚 Devlog Posting SSOT Guide

**Last Updated**: 2025-01-27  
**SSOT**: `tools/devlog_manager.py`

---

## 🎯 **SINGLE SOURCE OF TRUTH**

**`tools/devlog_manager.py`** is the **ONLY** script you should use for devlog posting.

---

## ✅ **USE THIS**

### **Routine Updates** (Agent Channel):
```bash
python tools/devlog_manager.py post --agent agent-1 --file devlog.md
```

### **Major Updates** (User Channel):
```bash
python tools/devlog_manager.py post --agent agent-4 --file devlog.md --major
```

---

## ⚠️ **DEPRECATED SCRIPTS**

The following scripts are **deprecated** and should **NOT** be used:

1. ❌ `tools/post_devlog_to_discord.py` - Now a wrapper (use devlog_manager.py directly)
2. ❌ `tools/devlog_auto_poster.py` - Deprecated
3. ❌ `scripts/post_devlogs_to_discord.py` - Deprecated
4. ⚠️ `tools/check_and_post_unposted_devlogs.py` - Should be updated to use devlog_manager.py

---

## 🔧 **FEATURES**

`devlog_manager.py` provides:
- ✅ Swarm Brain upload (automatic)
- ✅ Discord posting (agent-specific channels)
- ✅ Smart chunking (long messages split automatically)
- ✅ Mermaid diagram support
- ✅ Agent detection
- ✅ Major update flag
- ✅ Category auto-detection
- ✅ Index updates

---

## 📋 **MIGRATION**

If you're using any deprecated script:
1. Replace with `devlog_manager.py`
2. Use `--agent agent-X` flag
3. Use `--major` flag for major updates

---

## 🐝 **WE. ARE. SWARM.**

**SSOT**: `tools/devlog_manager.py` - Use this for all devlog posting!

---

**Generated**: 2025-01-27  
**Captain Agent-4** - Strategic Oversight

