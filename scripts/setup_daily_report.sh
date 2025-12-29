#!/bin/bash
# Setup script for Daily State of the Project Report
# Installs a cron job to run the report generator at 3:00 AM daily.

SCRIPT_PATH="/workspace/scripts/generate_state_of_project.py"
PYTHON_PATH=$(which python3)
LOG_PATH="/workspace/runtime/logs/daily_report.log"

# Ensure log directory exists
mkdir -p /workspace/runtime/logs

# Create the cron command
CRON_CMD="0 3 * * * cd /workspace && $PYTHON_PATH $SCRIPT_PATH >> $LOG_PATH 2>&1"

# Check if crontab exists
if command -v crontab >/dev/null 2>&1; then
    # Add to crontab if not already present
    (crontab -l 2>/dev/null; echo "$CRON_CMD") | crontab -
    echo "✅ Cron job installed: $CRON_CMD"
else
    echo "⚠️  'crontab' command not found. Please install cron or add this line manually to your scheduler:"
    echo "$CRON_CMD"
    
    # Create a systemd timer alternative suggestion
    echo ""
    echo "Alternative: Systemd Timer"
    echo "1. Create /etc/systemd/system/swarm-report.service"
    echo "2. Create /etc/systemd/system/swarm-report.timer"
fi
