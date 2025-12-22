@echo off
REM Generate Digital Dreamscape Daily Episode
REM Wrapper script for Windows

cd /d "%~dp0\.."

python tools/generate_daily_episode.py %*

