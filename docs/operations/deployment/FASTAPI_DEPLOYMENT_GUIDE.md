# FastAPI Deployment Guide - TradingRobotPlug Phase 3

**Author:** Agent-3 (Infrastructure & DevOps Specialist)  
**Date:** 2025-12-31  
**Status:** ✅ Complete Deployment Pipeline

---

## Overview

Complete deployment guide for TradingRobotPlug FastAPI backend, from file deployment to service setup to endpoint verification.

---

## Deployment Pipeline

### Phase 1: File Deployment ✅

**Script:** `tools/deploy_fastapi_tradingrobotplug.py`

**Status:** ✅ Complete (28 files deployed, 0 failures)

**What it does:**
- Deploys FastAPI backend files to production server via SFTP
- Deploys systemd service file to `/tmp/tradingrobotplug-fastapi.service`
- Creates directory structure on remote server

**Execution:**
```bash
python tools/deploy_fastapi_tradingrobotplug.py
```

**Output:**
- 28 files deployed to `backend/` directory on server
- Systemd service file at `/tmp/tradingrobotplug-fastapi.service`

---

### Phase 2: Service Setup 🟡

**Scripts:**
- `tools/setup_fastapi_service_tradingrobotplug.py` (Python)
- `tools/setup_fastapi_service_tradingrobotplug.sh` (Bash)

**Status:** 🟡 Ready for execution

**What it does:**
- Creates Python 3.11 virtual environment
- Installs dependencies from `requirements.txt`
- Configures `.env` file from `.env.example`
- Provides systemd service installation instructions

**Execution (SSH to server):**
```bash
# Option 1: Python script
python tools/setup_fastapi_service_tradingrobotplug.py

# Option 2: Bash script
bash tools/setup_fastapi_service_tradingrobotplug.sh
```

**Manual Steps After Script:**
1. Edit `.env` file with actual values:
   - `DATABASE_URL`
   - `ALPACA_API_KEY` and `ALPACA_SECRET_KEY`
   - `API_SECRET_KEY` and `JWT_SECRET_KEY`
   - `CORS_ORIGINS` (for production)

2. Initialize database (if needed):
   ```bash
   cd backend
   source venv/bin/activate
   python -c "from database.connection import init_database; init_database()"
   ```

3. Install and start systemd service:
   ```bash
   sudo cp /tmp/tradingrobotplug-fastapi.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable tradingrobotplug-fastapi
   sudo systemctl start tradingrobotplug-fastapi
   sudo systemctl status tradingrobotplug-fastapi
   ```

---

### Phase 3: Health Check & Verification ✅

**Scripts:**
- `tools/monitor_fastapi_deployment.py` (Agent-7)
- `tools/verify_tradingrobotplug_endpoints.py` (Agent-7)

**Status:** ✅ Ready for execution

**What it does:**
- Monitors FastAPI health endpoint
- Verifies all 6 endpoints return 200 OK
- Validates response formats

**Execution:**
```bash
# Monitor deployment and auto-verify when service starts
python tools/monitor_fastapi_deployment.py

# Or verify endpoints directly
python tools/verify_tradingrobotplug_endpoints.py
```

---

## Deployment Checklist

### Pre-Deployment
- [x] FastAPI backend files ready
- [x] Deployment script created
- [x] Service setup scripts created
- [x] Monitoring/verification scripts ready

### Deployment
- [x] Files deployed to production server (28 files)
- [x] Systemd service file deployed to `/tmp`

### Service Setup
- [ ] SSH to production server
- [ ] Execute service setup script
- [ ] Configure `.env` file with actual values
- [ ] Initialize database (if needed)
- [ ] Install systemd service
- [ ] Start systemd service
- [ ] Verify service status

### Verification
- [ ] Health endpoint returns 200 OK
- [ ] All 6 endpoints return 200 OK (not 500)
- [ ] Response formats validated
- [ ] End-to-end integration testing

---

## Endpoints to Verify

1. **Account Info:** `GET /api/v1/account/info`
2. **Positions:** `GET /api/v1/positions`
3. **Trades:** `GET /api/v1/trades`
4. **Orders:** `POST /api/v1/orders`
5. **Strategies List:** `GET /api/v1/strategies/list`
6. **Strategy Execute:** `POST /api/v1/strategies/execute`

**WordPress Endpoints:**
- `GET /wp-json/tradingrobotplug/v1/account`
- `GET /wp-json/tradingrobotplug/v1/positions`
- `GET /wp-json/tradingrobotplug/v1/trades`
- `POST /wp-json/tradingrobotplug/v1/orders`
- `GET /wp-json/tradingrobotplug/v1/strategies`
- `POST /wp-json/tradingrobotplug/v1/strategies/execute`

---

## Troubleshooting

### Service Not Starting
```bash
# Check service status
sudo systemctl status tradingrobotplug-fastapi

# View logs
sudo journalctl -u tradingrobotplug-fastapi -f

# Check for errors
sudo journalctl -u tradingrobotplug-fastapi --since "10 minutes ago" | grep -i error
```

### Health Endpoint Not Responding
```bash
# Check if service is running
sudo systemctl is-active tradingrobotplug-fastapi

# Check if port is listening
sudo netstat -tlnp | grep 8001

# Test health endpoint
curl http://localhost:8001/health
```

### Endpoints Returning 500
- Check FastAPI service is running
- Verify `.env` file is configured correctly
- Check database connection
- Review FastAPI logs for errors

---

## Quick Reference

**Deploy Files:**
```bash
python tools/deploy_fastapi_tradingrobotplug.py
```

**Setup Service (on server):**
```bash
python tools/setup_fastapi_service_tradingrobotplug.py
```

**Verify Endpoints:**
```bash
python tools/monitor_fastapi_deployment.py
# OR
python tools/verify_tradingrobotplug_endpoints.py
```

**Service Management:**
```bash
sudo systemctl start tradingrobotplug-fastapi
sudo systemctl stop tradingrobotplug-fastapi
sudo systemctl restart tradingrobotplug-fastapi
sudo systemctl status tradingrobotplug-fastapi
```

---

## Related Documentation

- `docs/TradingRobotPlug_Phase3_FastAPI_Requirements.md` - Endpoint requirements
- `docs/TradingRobotPlug_Phase3_PostDeployment_Verification.md` - Verification plan
- `docs/deployment/FASTAPI_DEPLOYMENT_PLAN.md` - Detailed deployment plan
- `docs/deployment/FASTAPI_MONITORING_CONFIG.md` - Monitoring configuration

---

**Last Updated:** 2025-12-31  
**Status:** ✅ Deployment pipeline complete, ready for service setup and verification

