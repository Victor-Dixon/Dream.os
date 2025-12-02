#!/usr/bin/env python3
"""
Continuous Daily Report Runner
Runs in background and generates reports at scheduled times.
"""

import time
import subprocess
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORT_SCRIPT = PROJECT_ROOT / "systems" / "technical_debt" / "daily_report_generator.py"
PYTHON_EXE = sys.executable

MORNING_HOUR = 9
AFTERNOON_HOUR = 15

last_morning_report = None
last_afternoon_report = None

print("🔄 Starting continuous daily report runner...")
print(f"   Morning reports: {MORNING_HOUR}:00")
print(f"   Afternoon reports: {AFTERNOON_HOUR}:00")
print("   (Press Ctrl+C to stop)")

while True:
    now = datetime.now()
    current_date = now.date()
    current_hour = now.hour
    
    # Check for morning report (9:00 AM)
    if current_hour == MORNING_HOUR and last_morning_report != current_date:
        print("\n📊 Generating morning report...")
        try:
            subprocess.run(
                [PYTHON_EXE, str(REPORT_SCRIPT), "--time", "morning", "--format", "both"],
                cwd=PROJECT_ROOT,
                check=True
            )
            last_morning_report = current_date
            print("✅ Morning report generated")
        except Exception as e:
            print(f"❌ Error generating morning report: {e}")
    
    # Check for afternoon report (3:00 PM)
    if current_hour == AFTERNOON_HOUR and last_afternoon_report != current_date:
        print("\n📊 Generating afternoon report...")
        try:
            subprocess.run(
                [PYTHON_EXE, str(REPORT_SCRIPT), "--time", "afternoon", "--format", "both"],
                cwd=PROJECT_ROOT,
                check=True
            )
            last_afternoon_report = current_date
            print("✅ Afternoon report generated")
        except Exception as e:
            print(f"❌ Error generating afternoon report: {e}")
    
    # Sleep for 1 minute
    time.sleep(60)
