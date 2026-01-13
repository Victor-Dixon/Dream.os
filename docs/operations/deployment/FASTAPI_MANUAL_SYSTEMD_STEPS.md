# FastAPI Manual Systemd Service Installation Steps

**Date:** 2025-12-31  
**Author:** Agent-3 (Infrastructure & DevOps Specialist)  
**Status:** Ready for Human Operator Execution

---

## 🎯 Purpose

Complete the FastAPI service deployment by installing and starting the systemd service. This requires sudo access and cannot be automated via SSH.

---

## ✅ Prerequisites

**Automated Setup Complete:**
- ✅ Virtual environment created (`backend/venv/`)
- ✅ Dependencies installed (`requirements.txt`)
- ✅ `.env` file created from `.env.example`
- ✅ Service file ready at `/tmp/tradingrobotplug-fastapi.service`

**Before Proceeding:**
1. Verify service file exists: `ls -la /tmp/tradingrobotplug-fastapi.service`
2. Review `.env` file configuration (may need actual values):
   - `DATABASE_URL`
   - `ALPACA_API_KEY` and `ALPACA_SECRET_KEY`
   - `API_SECRET_KEY` and `JWT_SECRET_KEY`
   - `CORS_ORIGINS` (for production)

---

## 📋 Manual Steps (Requires Sudo)

**Execute these 5 commands in order:**

### Step 1: Copy Service File
```bash
sudo cp /tmp/tradingrobotplug-fastapi.service /etc/systemd/system/
```

### Step 2: Reload Systemd Daemon
```bash
sudo systemctl daemon-reload
```

### Step 3: Enable Service (Start on Boot)
```bash
sudo systemctl enable tradingrobotplug-fastapi
```

### Step 4: Start Service
```bash
sudo systemctl start tradingrobotplug-fastapi
```

### Step 5: Verify Service Status
```bash
sudo systemctl status tradingrobotplug-fastapi
```

**Expected Output:**
- Service should show `active (running)`
- No error messages in status output

---

## 🔍 Verification Steps

### Check Service Status
```bash
sudo systemctl status tradingrobotplug-fastapi
```

### Check Service Logs (if issues)
```bash
sudo journalctl -u tradingrobotplug-fastapi -n 50
```

### Test Health Endpoint
```bash
curl http://localhost:8001/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-12-31T..."
}
```

---

## ⚠️ Troubleshooting

### Service Fails to Start

**Check Logs:**
```bash
sudo journalctl -u tradingrobotplug-fastapi -n 50 --no-pager
```

**Common Issues:**
1. **Missing .env configuration:** Verify `.env` file has actual values (not just placeholders)
2. **Database connection error:** Check `DATABASE_URL` in `.env`
3. **Port already in use:** Check if port 8001 is available: `netstat -tuln | grep 8001`
4. **Python path issues:** Verify virtual environment path in service file

### Service File Not Found

If `/tmp/tradingrobotplug-fastapi.service` doesn't exist:
1. Check if deployment completed successfully
2. Service file should have been deployed in Phase 1
3. Contact Agent-3 if file is missing

### Health Endpoint Not Responding

**Possible Causes:**
1. Service still starting (wait 10-15 seconds)
2. Service crashed (check logs)
3. `.env` configuration missing or incorrect
4. Database connection failed

**Diagnostic Commands:**
```bash
# Check if service is running
sudo systemctl is-active tradingrobotplug-fastapi

# Check recent logs
sudo journalctl -u tradingrobotplug-fastapi -n 20 --no-pager

# Check if port is listening
sudo netstat -tuln | grep 8001
```

---

## 📊 Post-Installation Verification

**After service is running:**

1. **Service Status:** `sudo systemctl status tradingrobotplug-fastapi` → Should show `active (running)`
2. **Health Endpoint:** `curl http://localhost:8001/health` → Should return JSON response
3. **Service Logs:** `sudo journalctl -u tradingrobotplug-fastapi -n 10` → Should show no errors

**Once verified:**
- Agent-4 will notify Agent-1 for immediate test execution
- Agent-1 will run complete validation pipeline (3-7 min)
- Agent-7 will verify WordPress endpoints

---

## 🔄 Service Management Commands

**Useful Commands:**

```bash
# Start service
sudo systemctl start tradingrobotplug-fastapi

# Stop service
sudo systemctl stop tradingrobotplug-fastapi

# Restart service
sudo systemctl restart tradingrobotplug-fastapi

# Check status
sudo systemctl status tradingrobotplug-fastapi

# View logs (live)
sudo journalctl -u tradingrobotplug-fastapi -f

# View recent logs
sudo journalctl -u tradingrobotplug-fastapi -n 50
```

---

## 📝 Service File Location

**Service File:** `/etc/systemd/system/tradingrobotplug-fastapi.service`

**Backup Location:** `/tmp/tradingrobotplug-fastapi.service` (original deployment)

---

## ✅ Completion Checklist

- [ ] Service file copied to `/etc/systemd/system/`
- [ ] Systemd daemon reloaded
- [ ] Service enabled (starts on boot)
- [ ] Service started successfully
- [ ] Service status shows `active (running)`
- [ ] Health endpoint responds: `curl http://localhost:8001/health`
- [ ] No errors in service logs
- [ ] Agent-4 notified (service ready)
- [ ] Agent-1 ready to execute tests

---

**Estimated Time:** 2-5 minutes (depending on troubleshooting needs)

**Next Step:** After service is running and health endpoint responds, Agent-4 will notify Agent-1 for immediate test execution.
