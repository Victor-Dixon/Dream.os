#!/bin/bash
# FastAPI Health Check Monitor
# Monitors /health endpoint and triggers alerts on failures

API_URL="${API_URL:-http://localhost:8000/health}"
FAILURE_COUNT=0
MAX_FAILURES=3
CHECK_INTERVAL=30
TIMEOUT=5
ALERT_SCRIPT="python -m src.infrastructure.alerting_system"

log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

check_health() {
    response=$(curl -s -o /dev/null -w "%{http_code}" --max-time $TIMEOUT "$API_URL" 2>/dev/null)
    echo $response
}

send_alert() {
    local level=$1
    local title=$2
    local message=$3
    $ALERT_SCRIPT \
        --level "$level" \
        --title "$title" \
        --message "$message" \
        --source "fastapi_health_monitor" || true
}

log_message "Starting FastAPI health check monitor (URL: $API_URL, Interval: ${CHECK_INTERVAL}s)"

while true; do
    response_code=$(check_health)
    
    if [ "$response_code" != "200" ]; then
        FAILURE_COUNT=$((FAILURE_COUNT + 1))
        log_message "Health check failed (HTTP $response_code) - Failure count: $FAILURE_COUNT"
        
        if [ $FAILURE_COUNT -ge $MAX_FAILURES ]; then
            log_message "CRITICAL: Health check failed $FAILURE_COUNT times consecutively"
            send_alert "critical" \
                "FastAPI Health Check Failed" \
                "Health check failed $FAILURE_COUNT consecutive times (HTTP $response_code)"
            FAILURE_COUNT=0  # Reset after alert
        elif [ $FAILURE_COUNT -eq 1 ]; then
            send_alert "warning" \
                "FastAPI Health Check Warning" \
                "Health check returned HTTP $response_code"
        fi
    else
        if [ $FAILURE_COUNT -gt 0 ]; then
            log_message "Health check recovered (HTTP $response_code)"
            send_alert "info" \
                "FastAPI Health Check Recovered" \
                "Health check recovered after $FAILURE_COUNT failures"
            FAILURE_COUNT=0
        fi
    fi
    
    sleep $CHECK_INTERVAL
done

