#!/bin/bash
# FastAPI Resource Monitor
# Monitors system resources and triggers alerts on thresholds

THRESHOLD_CPU=90
THRESHOLD_MEM=85
THRESHOLD_DISK=85
CHECK_INTERVAL=300  # 5 minutes
ALERT_SCRIPT="python -m src.infrastructure.alerting_system"

log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

check_cpu() {
    # Get CPU usage percentage (Linux)
    if command -v top >/dev/null 2>&1; then
        top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1 | cut -d'.' -f1
    elif command -v vmstat >/dev/null 2>&1; then
        vmstat 1 2 | tail -1 | awk '{print 100 - $15}'
    else
        echo "0"
    fi
}

check_memory() {
    # Get memory usage percentage
    free | grep Mem | awk '{printf "%.0f", $3/$2 * 100}'
}

check_disk() {
    # Get disk usage percentage for root partition
    df -h / | awk 'NR==2 {print $5}' | cut -d'%' -f1
}

send_alert() {
    local level=$1
    local title=$2
    local message=$3
    $ALERT_SCRIPT \
        --level "$level" \
        --title "$title" \
        --message "$message" \
        --source "fastapi_resource_monitor" || true
}

log_message "Starting FastAPI resource monitor (Interval: ${CHECK_INTERVAL}s)"

while true; do
    cpu_usage=$(check_cpu)
    mem_usage=$(check_memory)
    disk_usage=$(check_disk)
    
    # CPU monitoring
    if [ "$cpu_usage" -gt "$THRESHOLD_CPU" ] 2>/dev/null; then
        log_message "WARNING: CPU usage at ${cpu_usage}% (threshold: ${THRESHOLD_CPU}%)"
        send_alert "warning" \
            "FastAPI High CPU Usage" \
            "CPU usage at ${cpu_usage}% (threshold: ${THRESHOLD_CPU}%)"
    fi
    
    # Memory monitoring
    if [ "$mem_usage" -gt "$THRESHOLD_MEM" ]; then
        log_message "WARNING: Memory usage at ${mem_usage}% (threshold: ${THRESHOLD_MEM}%)"
        send_alert "warning" \
            "FastAPI High Memory Usage" \
            "Memory usage at ${mem_usage}% (threshold: ${THRESHOLD_MEM}%)"
    fi
    
    # Disk monitoring
    if [ "$disk_usage" -gt "$THRESHOLD_DISK" ]; then
        log_message "WARNING: Disk usage at ${disk_usage}% (threshold: ${THRESHOLD_DISK}%)"
        send_alert "warning" \
            "FastAPI High Disk Usage" \
            "Disk usage at ${disk_usage}% (threshold: ${THRESHOLD_DISK}%)"
    fi
    
    sleep $CHECK_INTERVAL
done

