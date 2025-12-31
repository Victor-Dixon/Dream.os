@echo off
REM Complete FastAPI Validation Execution
REM Executes pipeline and generates handoff message in one command

cd /d "%~dp0\.."

echo ============================================================
echo FASTAPI VALIDATION - COMPLETE EXECUTION
echo ============================================================
echo.

REM Step 1: Execute pipeline
echo Step 1: Executing validation pipeline...
python tools\execute_fastapi_validation_pipeline.py --endpoint http://localhost:8001

if errorlevel 1 (
    echo.
    echo ❌ Pipeline execution failed. Stopping.
    exit /b 1
)

echo.
echo Step 2: Generating coordination handoff message...
python tools\generate_coordination_handoff_message.py

echo.
echo ============================================================
echo ✅ COMPLETE - Results ready for Agent-4 coordination
echo ============================================================
echo.
echo Next: Copy generated message and send to Agent-4

