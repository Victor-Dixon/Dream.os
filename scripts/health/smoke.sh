#!/bin/bash
#
# Smoke Test Wrapper - Agent Cellphone V2
# =======================================
#
# Runs the Python smoke test harness for all core systems.
# Exit codes match the Python script (0=success, 1=failure).
#
# Usage: ./scripts/health/smoke.sh
#
# Author: Agent-2 (Architecture & Design Specialist)
# Date: 2026-01-09
#

set -e  # Exit on any error

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Change to project root
cd "$PROJECT_ROOT"

echo "🔥 Dream.OS Smoke Test Suite"
echo "============================"
echo "Project Root: $PROJECT_ROOT"
echo "Timestamp: $(date)"
echo ""

# Set PYTHONPATH to include the project root
export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"

# Run the smoke test
echo "🚀 Executing smoke tests..."
python scripts/health/smoke.py

# Capture exit code
EXIT_CODE=$?

echo ""
echo "============================"

if [ $EXIT_CODE -eq 0 ]; then
    echo "🎉 ALL SYSTEMS OPERATIONAL"
else
    echo "💥 SYSTEMS REQUIRE ATTENTION"
    echo "Check the output above for failed subsystems."
fi

echo "Exit Code: $EXIT_CODE"
echo "============================"

exit $EXIT_CODE