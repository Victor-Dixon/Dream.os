# FastAPI Deployment Plan - Phase 3

**Generated:** 2025-12-30  
**Deployment Coordinator:** Agent-3 (Infrastructure & DevOps Specialist)  
**API Implementation:** Agent-1 (Integration & Core Systems Specialist)  
**Status:** 🟡 In Progress

---

## Overview

Deployment plan for FastAPI REST API layer with 6 endpoints + WebSocket route. This document outlines deployment environment setup, configuration, monitoring, and production deployment strategy.

---

## Deployment Environment Setup

### 1. Python Environment

**Requirements:**
- Python 3.10+ (recommended: Python 3.11)
- Virtual environment isolation
- Dependency management via `requirements.txt`

**Setup Steps:**
```bash
# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate  # Windows

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install fastapi uvicorn[standard] websockets

# Verify installation
python -c "import fastapi; print(fastapi.__version__)"
```

**Dependencies Required:**
- `fastapi>=0.104.0`
- `uvicorn[standard]>=0.24.0`
- `websockets>=12.0`
- `pydantic>=2.0`
- Additional dependencies per endpoint requirements (to be provided by Agent-1)

---

### 2. Process Management

**Option A: systemd (Linux)**
```ini
# /etc/systemd/system/fastapi.service
[Unit]
Description=FastAPI REST API Service
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/Agent_Cellphone_V2_Repository
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Option B: Supervisor (Cross-platform)**
```ini
# /etc/supervisor/conf.d/fastapi.conf
[program:fastapi]
command=/path/to/venv/bin/uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --workers 4
directory=/path/to/Agent_Cellphone_V2_Repository
user=www-data
autostart=true
autorestart=true
stderr_logfile=/var/log/fastapi/error.log
stdout_logfile=/var/log/fastapi/access.log
environment=PATH="/path/to/venv/bin"
```

**Option C: Docker (Recommended for containerized deployment)**
```dockerfile
# Dockerfile (to be created)
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

---

### 3. Environment Configuration

**Environment Variables Required:**
```bash
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4
API_RELOAD=false  # Set to true for development

# Database Connection
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
# OR
DATABASE_URL=sqlite:///./data/app.db  # Development

# Broker/Cache (if using Redis/RabbitMQ)
REDIS_URL=redis://localhost:6379/0
BROKER_URL=amqp://user:password@localhost:5672/vhost

# API Keys & Secrets
API_KEY=<api_key>
SECRET_KEY=<secret_key>

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/fastapi/app.log

# Security
CORS_ORIGINS=https://example.com,https://www.example.com
ALLOWED_HOSTS=example.com,www.example.com
```

**Configuration File Template:**
Create `.env` file (use `.env.example` as template):
```bash
cp env.example .env
# Edit .env with actual values
```

**Security Notes:**
- Never commit `.env` to version control
- Use secrets management in production (AWS Secrets Manager, HashiCorp Vault, etc.)
- Rotate API keys regularly
- Use strong passwords for database/broker connections

---

## Monitoring Setup

### 1. Health Checks

**Endpoint:** `GET /health`

**Implementation Requirements:**
- Database connectivity check
- Broker connectivity check (if applicable)
- Service dependencies status
- Response format: `{"status": "healthy", "checks": {...}}`

**Example Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-12-30T08:00:00Z",
  "checks": {
    "database": "ok",
    "broker": "ok",
    "memory": "ok"
  }
}
```

### 2. Logging

**Logging Configuration:**
```python
# Logging setup (to be integrated)
import logging
from logging.handlers import RotatingFileHandler

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler('/var/log/fastapi/app.log', maxBytes=10485760, backupCount=5),
        logging.StreamHandler()
    ]
)
```

**Log Levels:**
- `DEBUG`: Development only
- `INFO`: General operational messages
- `WARNING`: Potential issues
- `ERROR`: Error conditions
- `CRITICAL`: Critical failures

**Log Rotation:**
- Max file size: 10MB
- Backup count: 5 files
- Compress old logs

### 3. Error Tracking

**Recommended Tools:**
- Sentry (production error tracking)
- Log aggregation (ELK stack, CloudWatch, etc.)
- Application Performance Monitoring (APM) tools

**Error Handling:**
- Structured error responses
- Error IDs for tracking
- Stack traces in development, sanitized in production

---

## Production Deployment Plan

### Pre-Deployment Checklist

- [ ] FastAPI implementation complete (6 endpoints + WebSocket)
- [ ] All dependencies documented in `requirements.txt`
- [ ] Environment variables documented
- [ ] Health check endpoint implemented
- [ ] Logging configured
- [ ] Error handling implemented
- [ ] Security review completed
- [ ] Load testing completed
- [ ] Database migrations ready (if applicable)
- [ ] Backup strategy in place
- [ ] Rollback plan documented

### Deployment Process

**Step 1: Preparation**
```bash
# Pull latest code
git pull origin main

# Backup current deployment (if applicable)
# Backup database (if applicable)

# Create deployment branch/tag
git tag -a v1.0.0 -m "FastAPI Phase 3 deployment"
```

**Step 2: Environment Setup**
```bash
# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
pip install -r requirements.txt

# Verify environment
python -c "import fastapi; import uvicorn"
```

**Step 3: Configuration**
```bash
# Load environment variables
source .env

# Verify configuration
python -c "import os; print(os.getenv('DATABASE_URL'))"
```

**Step 4: Database Migration (if applicable)**
```bash
# Run migrations
alembic upgrade head
# OR
python -m src.core.database.migrate
```

**Step 5: Pre-Deployment Testing**
```bash
# Run health checks
curl http://localhost:8000/health

# Run unit tests
pytest tests/

# Run integration tests
pytest tests/integration/
```

**Step 6: Deployment Execution**

**Option A: Rolling Deployment (Zero-Downtime)**
```bash
# Start new instance on different port
uvicorn src.api.main:app --host 0.0.0.0 --port 8001 --workers 4

# Health check new instance
curl http://localhost:8001/health

# Switch traffic (using load balancer/proxy)
# Update nginx/HAProxy config to point to port 8001

# Stop old instance
systemctl stop fastapi
# OR
supervisorctl stop fastapi

# Verify new instance
curl http://localhost:8000/health
```

**Option B: Blue-Green Deployment**
```bash
# Deploy to green environment
# Switch DNS/load balancer to green
# Monitor green for issues
# If stable, keep green, decommission blue
# If issues, rollback to blue
```

**Option C: Direct Deployment (Development/Single Instance)**
```bash
# Stop current instance
systemctl stop fastapi

# Deploy new code
git pull origin main
pip install -r requirements.txt

# Start new instance
systemctl start fastapi

# Verify
curl http://localhost:8000/health
```

### Rollback Strategy

**Immediate Rollback (if deployment fails):**

1. **Stop new instance:**
   ```bash
   systemctl stop fastapi
   ```

2. **Revert code:**
   ```bash
   git revert HEAD
   # OR
   git checkout <previous_tag>
   ```

3. **Restore database (if applicable):**
   ```bash
   # Restore from backup
   ```

4. **Start previous version:**
   ```bash
   systemctl start fastapi
   ```

5. **Verify:**
   ```bash
   curl http://localhost:8000/health
   ```

**Rollback Time:** < 5 minutes target

---

## Post-Deployment

### Verification

1. **Health Check:**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Endpoint Testing:**
   ```bash
   # Test each endpoint
   curl http://localhost:8000/api/v1/endpoint1
   curl http://localhost:8000/api/v1/endpoint2
   # ... etc
   ```

3. **WebSocket Testing:**
   ```bash
   # Test WebSocket connection
   wscat -c ws://localhost:8000/ws
   ```

4. **Monitor Logs:**
   ```bash
   tail -f /var/log/fastapi/app.log
   ```

### Monitoring

- Monitor health check endpoint (every 1 minute)
- Monitor error rates
- Monitor response times
- Monitor resource usage (CPU, memory, disk)
- Set up alerts for critical errors

---

## Deployment Checklist (Agent-1 Requirements)

**Need from Agent-1:**

- [ ] FastAPI implementation complete
- [ ] Endpoint specifications (6 endpoints)
- [ ] WebSocket route specification
- [ ] Required dependencies list
- [ ] Database schema/migrations (if applicable)
- [ ] Broker integration requirements (if applicable)
- [ ] API authentication method
- [ ] Rate limiting requirements
- [ ] CORS configuration requirements
- [ ] Security requirements (API keys, secrets)

---

## Next Steps

1. ✅ **Agent-3:** Create deployment documentation (this document)
2. ⏳ **Agent-1:** Complete FastAPI implementation
3. ⏳ **Agent-1:** Provide endpoint specifications and requirements
4. ⏳ **Agent-3:** Create environment configuration template
5. ⏳ **Agent-3:** Set up process management configuration
6. ⏳ **Agent-3:** Set up monitoring and logging
7. ⏳ **Agent-3:** Create deployment scripts
8. ⏳ **Both:** Coordinate deployment execution

---

**Status:** 🟡 Waiting for Agent-1 FastAPI implementation and requirements  
**Last Updated:** 2025-12-30 08:00:00

