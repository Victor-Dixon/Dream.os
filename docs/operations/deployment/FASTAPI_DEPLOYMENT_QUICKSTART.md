# FastAPI Deployment Quickstart Guide

**Purpose:** Quick reference for deploying FastAPI REST API layer.  
**Target:** Production deployment of TradingRobotPlug API.

---

## Prerequisites

- Python 3.11+
- System access (SSH or local)
- Process manager (systemd or Supervisor)
- Database connection configured

---

## Quick Deployment Steps

### 1. Environment Setup

```bash
python3.11 -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
pip install fastapi uvicorn[standard] websockets
```

### 2. Configure Environment

Copy `FASTAPI_ENV_TEMPLATE.env` to `.env` and configure:
- `DATABASE_URL`
- `API_KEY`
- `CORS_ORIGINS` (production domains only)

### 3. Deploy

```bash
chmod +x deploy_fastapi.sh
./deploy_fastapi.sh
```

### 4. Verify

```bash
curl http://localhost:8000/health
# Expected: {"status":"healthy","service":"TradingRobotPlug API","version":"1.0.0"}
```

---

## Process Management

**systemd (Linux):**
```bash
sudo cp fastapi.systemd.service /etc/systemd/system/fastapi.service
sudo systemctl enable fastapi
sudo systemctl start fastapi
sudo systemctl status fastapi
```

**Supervisor:**
```bash
sudo cp fastapi.supervisor.conf /etc/supervisor/conf.d/fastapi.conf
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl status fastapi
```

---

## Monitoring

**Health Check Monitor:**
```bash
chmod +x fastapi_health_check.sh
./fastapi_health_check.sh &
```

**Resource Monitor:**
```bash
chmod +x fastapi_resource_monitor.sh
./fastapi_resource_monitor.sh &
```

---

## Ports

- **8000:** HTTP API
- **8765:** WebSocket server

---

## Troubleshooting

- **Health check fails:** Check logs (`journalctl -u fastapi` or Supervisor logs)
- **Port already in use:** Change port in `.env` or kill existing process
- **Database connection fails:** Verify `DATABASE_URL` in `.env`
- **CORS errors:** Update `CORS_ORIGINS` with correct domains

---

**Full Documentation:** See `FASTAPI_DEPLOYMENT_PLAN.md` for detailed information.

