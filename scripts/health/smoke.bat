@echo off
REM Windows batch wrapper for Dream.OS comprehensive smoke test suite.
REM Provides easy execution for Windows environments and CI/CD pipelines.
REM
REM Usage:
REM   smoke.bat           # Run all tests
REM   smoke.bat --quiet   # Run with minimal output
REM   smoke.bat --help    # Show help
REM
REM Exit codes:
REM   0 = All systems healthy
REM   1 = One or more systems failed
REM   2 = Critical system failure (unable to test)
REM
REM Author: Agent-3 (Infrastructure & DevOps Recovery Specialist)
REM Date: 2026-01-09

setlocal enabledelayedexpansion

REM Get script directory and project root
set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%..\.."

REM Default options
set QUIET=false
set VERBOSE=false

REM Parse command line arguments
:parse_args
if "%~1"=="" goto :end_parse
if "%~1"=="--quiet" (
    set QUIET=true
    shift
    goto :parse_args
)
if "%~1"=="-q" (
    set QUIET=true
    shift
    goto :parse_args
)
if "%~1"=="--verbose" (
    set VERBOSE=true
    shift
    goto :parse_args
)
if "%~1"=="-v" (
    set VERBOSE=true
    shift
    goto :parse_args
)
if "%~1"=="--help" (
    goto :show_help
)
if "%~1"=="-h" (
    goto :show_help
)
echo Unknown option: %~1
echo Use --help for usage information
exit /b 1

:show_help
echo Dream.OS Smoke Test Suite
echo ========================
echo.
echo Usage:
echo   %0                    # Run all tests
echo   %0 --quiet           # Run with minimal output (CI/CD friendly)
echo   %0 --verbose         # Run with detailed output
echo   %0 --help            # Show this help
echo.
echo Exit codes:
echo   0 = All systems healthy
echo   1 = One or more systems failed
echo   2 = Critical system failure
echo.
exit /b 0

:end_parse

REM Pre-flight checks
if "%QUIET%"=="false" (
    echo.
    echo === Pre-flight Checks ===
)

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    if "%QUIET%"=="false" echo [ERROR] Python is not available
    exit /b 2
)
if "%QUIET%"=="false" echo [OK] Python found

REM Check if we're in the right directory
if not exist "scripts\health\smoke.py" (
    if "%QUIET%"=="false" (
        echo [ERROR] smoke.py not found in scripts\health\
        echo [INFO] Please run this script from the project root directory
    )
    exit /b 2
)
if "%QUIET%"=="false" echo [OK] Smoke test script found

REM Check for .env file
if exist ".env" (
    if "%QUIET%"=="false" echo [OK] Environment file (.env) found
) else (
    if "%QUIET%"=="false" echo [WARN] No .env file found - using system environment variables
)

REM Run the smoke tests
if "%QUIET%"=="false" (
    echo.
    echo === Running Smoke Tests ===
)

cd /d "%PROJECT_ROOT%"
python scripts\health\smoke.py
set EXIT_CODE=%errorlevel%

REM Post-run analysis
if "%QUIET%"=="false" (
    echo.
    echo === Test Results ===
)

if %EXIT_CODE% equ 0 (
    if "%QUIET%"=="false" echo [SUCCESS] ALL SYSTEMS HEALTHY - READY FOR PRODUCTION
) else if %EXIT_CODE% equ 1 (
    if "%QUIET%"=="false" echo [ERROR] SYSTEMS WITH FAILURES - RECOVERY NEEDED
) else if %EXIT_CODE% equ 2 (
    if "%QUIET%"=="false" echo [ERROR] CRITICAL SYSTEM FAILURE - UNABLE TO TEST
) else (
    if "%QUIET%"=="false" echo [ERROR] Unexpected exit code: %EXIT_CODE%
)

exit /b %EXIT_CODE%