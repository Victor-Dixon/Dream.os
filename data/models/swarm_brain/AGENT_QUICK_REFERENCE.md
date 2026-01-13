# 🚀 AGENT QUICK REFERENCE - ONE-PAGE CHEAT SHEET

**Last Updated:** 2025-10-15  
**Purpose:** Quick lookup for critical agent operations

---

## ⚡ EMERGENCY PROCEDURES

**System Down:**
```bash
python -m src.services.messaging_cli --captain \
  --message "CRITICAL: [description]" --high-priority
```

**Blocked:**
```python
lifecycle.add_blocker("Waiting for X")
```

**Rollback:**
```bash
git reset HEAD~1  # Undo last commit
```

---

## 🔄 EVERY CYCLE (MANDATORY)

**Start:**
```python
from src.core.agent_lifecycle import AgentLifecycle
lifecycle = AgentLifecycle('Agent-X')
lifecycle.start_cycle()
```

**End:**
```python
lifecycle.end_cycle(commit=True)
```

---

## 📊 STATUS.JSON FIELDS

```json
{
  "status": "ACTIVE|IDLE|BLOCKED",
  "fsm_state": "start|active|process|blocked|complete|end",
  "current_phase": "What you're doing",
  "cycle_count": 42,
  "last_updated": "2025-10-15T12:00:00Z"
}
```

---

## 🎯 FSM STATES

```
START → ACTIVE → PROCESS → COMPLETE → END
         ↓
      BLOCKED (resolve) → ACTIVE
```

---

## ⛽ GAS PIPELINE

**CRITICAL:** Send gas at **75-80%** complete!

```bash
# At 75%
python -m src.services.messaging_cli --agent Agent-X \
  --message "6/10 complete, patterns discovered!"

# At 90%
python -m src.services.messaging_cli --agent Agent-X \
  --message "9/10 complete, almost done!"

# At 100%
python -m src.services.messaging_cli --captain \
  --message "10/10 COMPLETE!"
```

---

## 🛠️ COMMON COMMANDS

**Swarm Brain Search:**
```bash
python tools/agent_toolbelt.py brain.search --query "topic"
```

**V2 Compliance Check:**
```bash
python tools/agent_toolbelt.py v2.check --file file.py
```

**Memory Leak Detection:**
```bash
python tools/agent_toolbelt.py mem.leaks
```

**Sync to Database:**
```bash
python tools/sync_status_to_db.py --agent Agent-X
```

---

## 📋 CYCLE CHECKLIST

**START:**
- [ ] Check inbox: `ls agent_workspaces/Agent-X/inbox/`
- [ ] Update status: `lifecycle.start_cycle()`
- [ ] Review mission

**DURING:**
- [ ] Update phase: `lifecycle.update_phase("...")`
- [ ] Complete tasks: `lifecycle.complete_task("...", points=100)`
- [ ] Send gas at 75%!

**END:**
- [ ] Update next_actions
- [ ] Commit: `lifecycle.end_cycle(commit=True)`
- [ ] Create devlog automatically (for all significant work)
- [ ] Post to Discord: `python tools/devlog_manager.py post --agent agent-X --file devlog.md`

---

## 🚨 COMMON ISSUES

**Status stale:**
```python
lifecycle._save_status()
```

**Database out of sync:**
```bash
python tools/sync_status_to_db.py --agent Agent-X --force
```

**FSM stuck:**
```python
lifecycle.status['fsm_state'] = 'active'
lifecycle._save_status()
```

---

## 💡 BEST PRACTICES

✅ Update status.json EVERY cycle  
✅ Send gas at 75-80%  
✅ Use AgentLifecycle class  
✅ Search swarm brain before starting  
✅ Check V2 compliance before committing  

❌ Skip status updates  
❌ Wait until 100% to send gas  
❌ Manual status.json edits  
❌ Forget to commit  

---

## 🔗 FULL GUIDES

- **CYCLE_PROTOCOLS.md** - Cycle requirements
- **STATUS_JSON_GUIDE.md** - Complete field reference
- **AGENT_LIFECYCLE_FSM.md** - FSM states
- **GAS_SYSTEM_COMPLETE.md** - Gas pipeline
- **TOOLBELT_USAGE.md** - All 41+ tools
- **DATABASE_INTEGRATION.md** - Database sync

---

## 📞 CONTACTS

**Captain:** Agent-4  
**Emergency:** `--captain --high-priority`  
**Swarm Brain:** `python tools/agent_toolbelt.py brain.search`

---

**🐝 QUICK REFERENCE = FAST DECISIONS!** 🚀

