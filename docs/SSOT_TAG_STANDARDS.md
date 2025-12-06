# SSOT Tag Standards - Infrastructure Domain

**Date**: 2025-12-05  
**Domain**: Infrastructure (Agent-3)  
**Status**: ✅ **ACTIVE STANDARD**

---

## 🎯 **SSOT TAG FORMAT**

All infrastructure monitoring and DevOps tools must include SSOT domain tags:

```markdown
<!-- SSOT Domain: infrastructure -->
```

### **Placement**:
- **Location**: In the file header/docstring, after author/date information
- **Format**: HTML comment style
- **Required**: All infrastructure tools in `tools/` directory

---

## 📋 **INFRASTRUCTURE DOMAIN SCOPE**

### **Tools Requiring SSOT Tags**:

1. **Monitoring Tools**:
   - `unified_monitor.py` ✅
   - `workspace_health_monitor.py` ✅
   - `agent_fuel_monitor.py` ✅
   - `agent_activity_detector.py` ✅
   - `auto_status_updater.py` ✅
   - `mission_control.py` ✅
   - `status_monitor_recovery_trigger.py`
   - `start_monitoring_system.py`
   - `monitor_twitch_bot.py`

2. **Queue & Message Processing**:
   - `start_message_queue_processor.py`
   - Queue status checkers
   - Message queue health monitors

3. **Health Checkers**:
   - Integration health checkers
   - Service health monitors
   - System health validators

4. **DevOps & Deployment**:
   - CI/CD tools
   - Deployment automation
   - Infrastructure automation

---

## 🔍 **TAG VERIFICATION**

### **Check for Missing Tags**:
```bash
python check_ssot_tags.py
```

### **Current Status**:
- **Tools WITH tags**: 24
- **Tools WITHOUT tags**: 368
- **Infrastructure tools tagged**: 6+ (increasing)

---

## 📊 **SSOT DOMAIN BOUNDARIES**

### **Infrastructure Domain (Agent-3)**:
- ✅ Monitoring systems
- ✅ Health checkers
- ✅ Queue processors
- ✅ Status updaters
- ✅ Activity detectors
- ✅ DevOps automation
- ✅ CI/CD tools
- ✅ Deployment automation

### **NOT Infrastructure Domain**:
- ❌ Architecture patterns (Agent-2)
- ❌ Web frameworks (Agent-7)
- ❌ Test infrastructure (Agent-8)
- ❌ Analytics/metrics (Agent-5)
- ❌ Messaging protocols (Agent-6)
- ❌ Integration patterns (Agent-1)

---

## ✅ **COMPLIANCE CHECKLIST**

- [ ] All infrastructure monitoring tools have SSOT tags
- [ ] Tags placed in file header/docstring
- [ ] Format: `<!-- SSOT Domain: infrastructure -->`
- [ ] Tags verified via `check_ssot_tags.py`
- [ ] Documentation updated with boundaries

---

## 🔄 **MAINTENANCE**

- **When creating new infrastructure tools**: Add SSOT tag immediately
- **When consolidating tools**: Preserve or update SSOT tags
- **When archiving tools**: Tag remains for historical reference
- **Regular audits**: Run `check_ssot_tags.py` monthly

---

**Last Updated**: 2025-12-05  
**Maintained By**: Agent-3 (Infrastructure & DevOps Specialist)

