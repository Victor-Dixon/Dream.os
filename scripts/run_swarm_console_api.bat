@echo off
REM SSOT Domain: scripts
cd /d %~dp0\..
python -m uvicorn apps.api.main:app --reload --port 8080
