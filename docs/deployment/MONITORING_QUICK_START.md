# FastAPI Monitoring Quick Start

**Purpose:** Quick reference for deploying FastAPI monitoring infrastructure.

## Deployment Steps

1. **Health Check Monitor:**
   ```bash
   sudo cp docs/deployment/fastapi_health_check.sh /usr/local/bin/
   sudo chmod +x /usr/local/bin/fastapi_health_check.sh
   # Configure as systemd service or supervisor process
   ```

2. **Resource Monitor:**
   ```bash
   sudo cp docs/deployment/fastapi_resource_monitor.sh /usr/local/bin/
   sudo chmod +x /usr/local/bin/fastapi_resource_monitor.sh
   # Configure as systemd service or supervisor process
   ```

3. **Python Module Integration:**
   ```python
   from src.infrastructure.fastapi_monitoring import FastAPIMonitoring, create_monitoring_middleware
   
   monitoring = FastAPIMonitoring()
   app.add_middleware(create_monitoring_middleware(monitoring))
   ```

## Alert Thresholds

- **Critical:** 3+ consecutive health check failures
- **Warning:** CPU >90%, Memory >85%, Disk >85%, Response time >2s

## Configuration

Set environment variables:
- `API_URL` (default: http://localhost:8000/health)
- `DISCORD_WEBHOOK_URL` (optional, for Discord alerts)

See `FASTAPI_MONITORING_CONFIG.md` for complete documentation.

