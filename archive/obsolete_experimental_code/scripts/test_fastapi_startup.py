#!/usr/bin/env python3
"""
Test FastAPI Startup
====================

Simple test to check if FastAPI can start properly.
"""

import subprocess
import time
import signal
import sys

def test_fastapi_startup():
    """Test FastAPI startup process."""
    print("🚀 Testing FastAPI startup...")

    try:
        # Start FastAPI with uvicorn
        # PHASE 4 CONSOLIDATION: FastAPI components moved to TradingRobotPlug repository
        proc = subprocess.Popen([
            sys.executable, "-c",
            "import uvicorn; from trading_robot.web.fastapi_app import app; uvicorn.run(app, host='0.0.0.0', port=8002)"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd="D:\\Agent_Cellphone_V2_Repository")

        # Wait for startup
        time.sleep(5)

        # Check if process is still running
        if proc.poll() is None:
            print("✅ FastAPI started successfully")
            print("🛑 Terminating test process...")
            proc.terminate()
            proc.wait(timeout=5)
            return True
        else:
            print("❌ FastAPI failed to start")
            stdout, stderr = proc.communicate()
            print("STDOUT:")
            print(stdout.decode() if stdout else "None")
            print("STDERR:")
            print(stderr.decode() if stderr else "None")
            return False

    except Exception as e:
        print(f"❌ Error during test: {e}")
        return False

if __name__ == "__main__":
    success = test_fastapi_startup()
    sys.exit(0 if success else 1)