# 🔄 Reinitialize Agent Status Monitor - Quick Guide

## 📊 OVERVIEW

The agent status monitor tracks agent activity and detects stalls. This guide shows how to reinitialize it.

---

## 🚀 QUICK START

### **Option 1: Reinitialize Monitor Only** (Recommended)

```bash
python tools/reinitialize_status_monitor.py
```

**What it does:**
- Stops existing monitor if running
- Starts fresh monitoring cycle
- Resets agent activity tracking
- Uses hardened multi-source detection

**Use when:**
- Monitor seems stuck or not detecting activity
- Need to reset after system changes
- Quick restart without full orchestrator

---

### **Option 2: Start Full Monitoring System**

```bash
python tools/reinitialize_status_monitor.py --full
```

**What it does:**
- Starts full overnight orchestrator
- Includes monitor + self-healing + recovery
- Continuous 24/7 operation
- Full autonomous agent management

**Use when:**
- Starting complete monitoring system
- Need full orchestrator functionality
- Running overnight operations

---

### **Option 3: Reset State Only** (No Start)

```bash
python tools/reinitialize_status_monitor.py --reset-only
```

**What it does:**
- Stops monitor if running
- Resets state
- Does NOT start monitoring

**Use when:**
- Need to stop monitor completely
- Preparing for manual restart
- Troubleshooting

---

## 📋 ALTERNATIVE METHODS

### **Method 1: Use Start Monitoring Script**

```bash
python tools/start_monitoring_system.py
```

**What it does:**
- Starts full orchestrator with monitoring
- Background mode available: `--background`

---

### **Method 2: Direct Python API**

```python
from src.orchestrators.overnight.monitor import ProgressMonitor

# Create and start monitor
monitor = ProgressMonitor()
monitor.start_monitoring()

# Check status
print(f"Monitoring: {monitor.is_monitoring}")
print(f"Agents tracked: {len(monitor.agent_activity)}")
```

---

## 🔍 VERIFY MONITOR STATUS

### **Check if Monitor is Running**

```python
from src.orchestrators.overnight.monitor import ProgressMonitor

monitor = ProgressMonitor()
print(f"Is monitoring: {monitor.is_monitoring}")
print(f"Agent status: {monitor.get_agent_status()}")
```

### **Check Agent Activity**

```bash
python -m tools.agent_activity_detector --agent Agent-3 --lookback 10
```

---

## 🛠️ TROUBLESHOOTING

### **Monitor Not Starting**

1. **Check for running processes:**
   ```bash
   # Windows
   tasklist | findstr python
   
   # Linux/Mac
   ps aux | grep python
   ```

2. **Check logs:**
   - Look for errors in console output
   - Check `logs/` directory for error logs

3. **Verify dependencies:**
   ```bash
   pip install paramiko  # For SFTP connections
   ```

### **Monitor Not Detecting Activity**

1. **Verify hardened system is working:**
   - Check `src/orchestrators/overnight/monitor.py` uses multi-source detection
   - Verify `tools/agent_activity_detector.py` has all methods

2. **Test activity detection:**
   ```bash
   python -m tools.agent_activity_detector --agent Agent-3 --report
   ```

3. **Check agent status:**
   ```python
   from src.orchestrators.overnight.monitor import ProgressMonitor
   monitor = ProgressMonitor()
   status = monitor.get_agent_status()
   print(status)
   ```

---

## 📊 MONITOR CONFIGURATION

### **Default Settings**

- **Check interval:** 60 seconds
- **Stall timeout:** 300 seconds (5 minutes)
- **Activity sources:** 17+ sources monitored
- **Confidence scoring:** Enabled
- **Progressive timeouts:** Enabled

### **Customize Settings**

Edit `config/orchestration.yml`:

```yaml
overnight:
  monitoring:
    check_interval: 60  # seconds
    stall_timeout: 300  # seconds
    health_checks: true
    performance_tracking: true
```

---

## ✅ VERIFICATION CHECKLIST

After reinitializing, verify:

- [ ] Monitor reports `is_monitoring: True`
- [ ] All 8 agents tracked in `agent_activity`
- [ ] Activity detection working (test with `agent_activity_detector`)
- [ ] No errors in logs
- [ ] Stall detection functional (test with inactive agent)

---

## 🎯 RECOMMENDED WORKFLOW

1. **Stop existing monitor** (if running):
   ```bash
   python tools/reinitialize_status_monitor.py --reset-only
   ```

2. **Reinitialize and start:**
   ```bash
   python tools/reinitialize_status_monitor.py
   ```

3. **Verify status:**
   ```bash
   python -m tools.agent_activity_detector --agent Agent-3
   ```

4. **Monitor logs:**
   - Watch console output for activity
   - Check for stall detections

---

**🐝 WE. ARE. SWARM. STATUS MONITOR REINITIALIZATION GUIDE. ⚡🔥**

