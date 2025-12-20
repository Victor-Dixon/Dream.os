@echo off
REM Trading Robot Virtual Environment Setup Script (Windows)
REM Generated: 2025-12-20
REM Author: Agent-3 (Infrastructure & DevOps Specialist)

echo 🚀 Setting up Trading Robot virtual environment...

REM Determine Python command
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Python not found. Please install Python 3.11+
    exit /b 1
)

echo 📍 Using Python:
python --version

REM Create virtual environment
echo 📦 Creating virtual environment in venv...
python -m venv venv

REM Activate virtual environment
echo 🔌 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️  Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo 📥 Installing dependencies from requirements.txt...
pip install -r requirements.txt

echo ✅ Virtual environment setup complete!
echo.
echo To activate the virtual environment, run:
echo   venv\Scripts\activate.bat
