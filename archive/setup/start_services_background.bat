@echo off
REM Start all services in background mode (Windows)
REM This script runs main.py with --background flag

echo Starting services in background...
python main.py --background

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Services started successfully!
    echo To check status: python main.py --status
    echo To stop services: python main.py --stop
) else (
    echo.
    echo Failed to start services. Check the output above.
    pause
)

