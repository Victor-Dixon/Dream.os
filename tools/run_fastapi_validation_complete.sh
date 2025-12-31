#!/bin/bash
# Complete FastAPI Validation Execution
# Executes pipeline and generates handoff message in one command

cd "$(dirname "$0")/.." || exit 1

echo "============================================================"
echo "FASTAPI VALIDATION - COMPLETE EXECUTION"
echo "============================================================"
echo

# Step 1: Execute pipeline
echo "Step 1: Executing validation pipeline..."
python tools/execute_fastapi_validation_pipeline.py --endpoint http://localhost:8001

if [ $? -ne 0 ]; then
    echo
    echo "❌ Pipeline execution failed. Stopping."
    exit 1
fi

echo
echo "Step 2: Generating coordination handoff message..."
python tools/generate_coordination_handoff_message.py

echo
echo "============================================================"
echo "✅ COMPLETE - Results ready for Agent-4 coordination"
echo "============================================================"
echo
echo "Next: Copy generated message and send to Agent-4"

