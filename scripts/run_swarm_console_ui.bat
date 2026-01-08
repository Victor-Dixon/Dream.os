@echo off
REM SSOT Domain: scripts
cd /d %~dp0\..\apps\ui
python -m http.server 5173
