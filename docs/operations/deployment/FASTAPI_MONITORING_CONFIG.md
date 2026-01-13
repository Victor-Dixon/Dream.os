# FastAPI Monitoring and Alerting Configuration

**Generated:** 2025-12-30  
**Deployment Coordinator:** Agent-3 (Infrastructure & DevOps Specialist)  
**Status:** ✅ Ready

---

## Overview

Monitoring and alerting configuration for FastAPI deployment. Integrates with existing infrastructure alerting system and provides comprehensive observability for the API layer.

---

## Monitoring Components

### 1. Health Check Monitoring

**Endpoint:** `GET /health`

**Monitoring Frequency:**
- **Interval:** 30 seconds
- **Timeout:** 5 seconds
- **Failure Threshold:** 3 consecutive failures

**Health Check Script:**
```bash
#!/bin/bash
# health_check.sh - FastAPI health check monitor

API_URL="${API_URL:-http://localhost:8000}"
FAILURE_COUNT=0
MAX_FAILURES=3

while true; do
    response=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "${API_URL}/health")
    
    if [ "$response" != "200" ]; then
        FAILURE_COUNT=$((FAILURE_COUNT + 1))
        echo "$(date): Health check failed (HTTP $response) - Failure count: $FAILURE_COUNT"
        
        if [ $FAILURE_COUNT -ge $MAX_FAILURES ]; then
            echo "$(date): CRITICAL: Health check failed $FAILURE_COUNT times consecutively"
            # Trigger alert via alerting system
            python -m src.infrastructure.alerting_system \
                --level critical \
                --title "FastAPI Health Check Failed" \
                --message "Health check failed $FAILURE_COUNT consecutive times (HTTP $response)" \
                --source "fastapi_health_monitor"
            FAILURE_COUNT=0  # Reset after alert
        fi
    else
        if [ $FAILURE_COUNT -gt 0 ]; then
            echo "$(date): Health check recovered"
            FAILURE_COUNT=0
        fi
    fi
    
    sleep 30
done
```

**systemd Service (Optional):**
```ini
[Unit]
Description=FastAPI Health Check Monitor
After=network.target

[Service]
Type=simple
User=www-data
ExecStart=/usr/local/bin/fastapi_health_check.sh
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

---

### 2. Application Metrics Monitoring

**Prometheus Metrics Endpoint (Recommended):**

Add to FastAPI application:
```python
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from fastapi import Response

# Metrics
request_count = Counter(
    'fastapi_requests_total',
    'Total number of requests',
    ['method', 'endpoint', 'status']
)

request_duration = Histogram(
    'fastapi_request_duration_seconds',
    'Request duration in seconds',
    ['method', 'endpoint']
)

active_connections = Gauge(
    'fastapi_active_connections',
    'Number of active connections'
)

# Metrics endpoint
@app.get("/metrics")
async def metrics():
    return Response(content=generate_latest(), media_type="text/plain")
```

**Monitoring Metrics:**
- Request rate (requests/second)
- Response time (p50, p95, p99)
- Error rate (4xx, 5xx responses)
- Active connections
- WebSocket connections (port 8765)

---

### 3. Logging Configuration

**Structured Logging Setup:**

```python
# logging_config.py
import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup_fastapi_logging(
    log_dir: Path = Path("logs"),
    log_level: str = "INFO",
    max_bytes: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5
):
    """Configure FastAPI logging."""
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Root logger
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    
    # File handler (rotating)
    file_handler = RotatingFileHandler(
        log_dir / "fastapi.log",
        maxBytes=max_bytes,
        backupCount=backup_count
    )
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s'
    )
    file_handler.setFormatter(file_formatter)
    
    # Error file handler
    error_handler = RotatingFileHandler(
        log_dir / "fastapi_errors.log",
        maxBytes=max_bytes,
        backupCount=backup_count
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(file_formatter)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.addHandler(error_handler)
    
    # Uvicorn access logs
    access_logger = logging.getLogger("uvicorn.access")
    access_file_handler = RotatingFileHandler(
        log_dir / "fastapi_access.log",
        maxBytes=max_bytes,
        backupCount=backup_count
    )
    access_file_handler.setFormatter(console_formatter)
    access_logger.addHandler(access_file_handler)
    
    return logger
```

**Log Rotation Configuration (logrotate):**

```bash
# /etc/logrotate.d/fastapi
/path/to/logs/fastapi*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 0644 www-data www-data
    sharedscripts
    postrotate
        systemctl reload fastapi > /dev/null 2>&1 || true
    endscript
}
```

---

### 4. Alerting Integration

**FastAPI Alerting Module:**

```python
# fastapi_monitoring.py
from src.infrastructure.alerting_system import AlertingSystem, AlertLevel
from typing import Optional

class FastAPIMonitoring:
    """FastAPI-specific monitoring and alerting."""
    
    def __init__(self, alerting_system: Optional[AlertingSystem] = None):
        self.alerting = alerting_system or AlertingSystem()
        self.error_count = 0
        self.error_threshold = 10  # Alert after 10 errors in 5 minutes
    
    def alert_health_check_failure(self, status_code: int, consecutive_failures: int):
        """Alert on health check failures."""
        level = AlertLevel.CRITICAL if consecutive_failures >= 3 else AlertLevel.WARNING
        self.alerting.send_alert(
            level=level,
            title=f"FastAPI Health Check {'CRITICAL' if consecutive_failures >= 3 else 'WARNING'}",
            message=f"Health check returned HTTP {status_code} ({consecutive_failures} consecutive failures)",
            source="fastapi_health_monitor",
            metadata={
                "status_code": status_code,
                "consecutive_failures": consecutive_failures
            }
        )
    
    def alert_high_error_rate(self, error_count: int, time_window: str = "5 minutes"):
        """Alert on high error rate."""
        self.alerting.send_alert(
            level=AlertLevel.WARNING,
            title="FastAPI High Error Rate",
            message=f"{error_count} errors detected in {time_window}",
            source="fastapi_error_monitor",
            metadata={"error_count": error_count, "time_window": time_window}
        )
    
    def alert_slow_response(self, endpoint: str, duration: float, threshold: float = 2.0):
        """Alert on slow response times."""
        if duration > threshold:
            self.alerting.send_alert(
                level=AlertLevel.WARNING,
                title="FastAPI Slow Response",
                message=f"Endpoint {endpoint} took {duration:.2f}s (threshold: {threshold}s)",
                source="fastapi_performance_monitor",
                metadata={
                    "endpoint": endpoint,
                    "duration": duration,
                    "threshold": threshold
                }
            )
    
    def alert_websocket_connection_issue(self, active_connections: int, max_connections: int = 1000):
        """Alert on WebSocket connection issues."""
        if active_connections >= max_connections * 0.9:
            self.alerting.send_alert(
                level=AlertLevel.WARNING,
                title="FastAPI WebSocket Connection Limit",
                message=f"WebSocket connections at {active_connections}/{max_connections} (90% threshold)",
                source="fastapi_websocket_monitor",
                metadata={
                    "active_connections": active_connections,
                    "max_connections": max_connections
                }
            )
```

---

### 5. Resource Monitoring

**System Resource Alerts:**

Integrate with existing alerting system for:
- **CPU Usage:** Alert if >90% for 5 minutes
- **Memory Usage:** Alert if >85% for 5 minutes
- **Disk Space:** Alert if >85% usage
- **Network:** Alert on connection failures

**Monitoring Script:**
```bash
#!/bin/bash
# resource_monitor.sh - System resource monitoring for FastAPI

THRESHOLD_CPU=90
THRESHOLD_MEM=85
THRESHOLD_DISK=85

while true; do
    # CPU usage
    cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
    if (( $(echo "$cpu_usage > $THRESHOLD_CPU" | bc -l) )); then
        python -m src.infrastructure.alerting_system \
            --level warning \
            --title "FastAPI High CPU Usage" \
            --message "CPU usage at ${cpu_usage}%" \
            --source "fastapi_resource_monitor"
    fi
    
    # Memory usage
    mem_usage=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100}')
    if [ $mem_usage -gt $THRESHOLD_MEM ]; then
        python -m src.infrastructure.alerting_system \
            --level warning \
            --title "FastAPI High Memory Usage" \
            --message "Memory usage at ${mem_usage}%" \
            --source "fastapi_resource_monitor"
    fi
    
    # Disk usage
    disk_usage=$(df -h / | awk 'NR==2 {print $5}' | cut -d'%' -f1)
    if [ $disk_usage -gt $THRESHOLD_DISK ]; then
        python -m src.infrastructure.alerting_system \
            --level warning \
            --title "FastAPI High Disk Usage" \
            --message "Disk usage at ${disk_usage}%" \
            --source "fastapi_resource_monitor"
    fi
    
    sleep 300  # Check every 5 minutes
done
```

---

## Alert Thresholds

### Critical Alerts (Immediate Action Required)
- Health check fails 3+ times consecutively
- API returns 5xx errors >10% of requests
- Service becomes unresponsive
- Database connection failures

### Warning Alerts (Monitor Closely)
- Health check fails 1-2 times
- Response time >2 seconds (p95)
- Error rate >5% (4xx/5xx)
- CPU usage >90% for 5+ minutes
- Memory usage >85% for 5+ minutes
- Disk usage >85%
- WebSocket connections >90% of limit

### Info Alerts (Informational)
- Deployment completed
- Service restarted
- Configuration changes
- Scheduled maintenance

---

## Monitoring Dashboard (Recommended)

**Tools:**
- **Grafana:** Visualize metrics from Prometheus
- **Prometheus:** Metrics collection and alerting
- **ELK Stack:** Log aggregation and analysis
- **Sentry:** Error tracking and performance monitoring

**Key Metrics to Display:**
- Request rate (requests/second)
- Response time percentiles (p50, p95, p99)
- Error rate (4xx, 5xx)
- Active connections
- System resources (CPU, memory, disk)
- WebSocket connections

---

## Integration with Existing Systems

### Alerting System Integration

The FastAPI monitoring integrates with `src.infrastructure.alerting_system`:

```python
from src.infrastructure.alerting_system import AlertingSystem, AlertLevel

alerting = AlertingSystem(
    enable_discord=True,
    discord_webhook=os.getenv("DISCORD_WEBHOOK_URL")
)

# Example: Alert on deployment
alerting.send_alert(
    level=AlertLevel.INFO,
    title="FastAPI Deployment Complete",
    message="FastAPI service deployed successfully",
    source="fastapi_deployment",
    metadata={"version": "1.0.0", "environment": "production"}
)
```

---

## Deployment Checklist

- [ ] Health check monitoring script deployed
- [ ] Prometheus metrics endpoint implemented
- [ ] Logging configuration applied
- [ ] Log rotation configured
- [ ] Alerting system integrated
- [ ] Resource monitoring script deployed
- [ ] Alert thresholds configured
- [ ] Monitoring dashboard configured (if applicable)
- [ ] Discord webhook configured (if applicable)
- [ ] Test alerts sent and verified

---

## Next Steps

1. ✅ Monitoring configuration documented
2. ✅ Alerting integration documented
3. ⏳ Agent-1 to implement Prometheus metrics endpoint
4. ⏳ Deploy monitoring scripts to production
5. ⏳ Configure alerting thresholds based on production metrics
6. ⏳ Set up monitoring dashboard (Grafana/Prometheus)

---

**Last Updated:** 2025-12-30  
**Status:** ✅ Configuration ready, awaiting implementation integration

