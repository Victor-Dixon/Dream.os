# Smoke Test Wrapper - Agent Cellphone V2 (PowerShell)
# ===================================================
#
# Runs the Python smoke test harness for all core systems.
# Exit codes match the Python script (0=success, 1=failure).
#
# Usage: .\scripts\health\smoke.ps1
#
# Author: Agent-2 (Architecture & Design Specialist)
# Date: 2026-01-09
#

# Get the directory where this script is located
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent (Split-Path -Parent $ScriptDir)

# Change to project root
Set-Location $ProjectRoot

Write-Host "🔥 Dream.OS Smoke Test Suite" -ForegroundColor Yellow
Write-Host "============================" -ForegroundColor Yellow
Write-Host "Project Root: $ProjectRoot"
Write-Host "Timestamp: $(Get-Date)"
Write-Host ""

# Set PYTHONPATH to include the project root
$env:PYTHONPATH = "$ProjectRoot;$env:PYTHONPATH"

# Run the smoke test
Write-Host "🚀 Executing smoke tests..." -ForegroundColor Green
& python scripts/health/smoke.py

# Capture exit code
$ExitCode = $LASTEXITCODE

Write-Host ""
Write-Host "============================" -ForegroundColor Yellow

if ($ExitCode -eq 0) {
    Write-Host "🎉 ALL SYSTEMS OPERATIONAL" -ForegroundColor Green
} else {
    Write-Host "💥 SYSTEMS REQUIRE ATTENTION" -ForegroundColor Red
    Write-Host "Check the output above for failed subsystems."
}

Write-Host "Exit Code: $ExitCode" -ForegroundColor Yellow
Write-Host "============================" -ForegroundColor Yellow

exit $ExitCode