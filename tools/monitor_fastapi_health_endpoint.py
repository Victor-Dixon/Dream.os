#!/usr/bin/env python3
"""
FastAPI Health Endpoint Monitor
Proactively monitors health endpoint and executes tests immediately when available.

Usage:
    python tools/monitor_fastapi_health_endpoint.py [--endpoint URL] [--interval SECONDS] [--max-wait MINUTES]
    
Monitors health endpoint and executes complete validation pipeline when endpoint responds.
"""

import time
import sys
import argparse
import subprocess
from pathlib import Path
from datetime import datetime, timedelta

PROJECT_ROOT = Path(__file__).parent.parent


def check_health_endpoint(endpoint: str) -> tuple[bool, str]:
    """Check if FastAPI health endpoint is responding."""
    try:
        import requests
        health_url = f"{endpoint}/health"
        response = requests.get(health_url, timeout=5)
        
        if response.status_code == 200:
            return True, f"Health endpoint responding (200)"
        else:
            return False, f"Health endpoint returned {response.status_code}"
    except requests.exceptions.ConnectionError:
        return False, "Connection refused - service may be starting"
    except requests.exceptions.Timeout:
        return False, "Connection timeout"
    except Exception as e:
        return False, f"Error: {str(e)}"


def monitor_and_execute(endpoint: str = "http://localhost:8001", 
                        interval: int = 10, 
                        max_wait_minutes: int = 30):
    """Monitor health endpoint and execute pipeline when available."""
    max_wait_seconds = max_wait_minutes * 60
    start_time = datetime.now()
    end_time = start_time + timedelta(seconds=max_wait_seconds)
    
    print("="*70)
    print("FASTAPI HEALTH ENDPOINT MONITOR")
    print("="*70)
    print(f"Endpoint: {endpoint}")
    print(f"Health Check: {endpoint}/health")
    print(f"Check interval: {interval} seconds")
    print(f"Max wait time: {max_wait_minutes} minutes")
    print()
    print("⚠️  Service is RUNNING but health endpoint not responding yet")
    print("   Monitoring for health endpoint availability...")
    print()
    
    check_count = 0
    
    while datetime.now() < end_time:
        check_count += 1
        is_ready, message = check_health_endpoint(endpoint)
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        elapsed = (datetime.now() - start_time).total_seconds()
        
        if is_ready:
            print(f"✅ [{timestamp}] Health endpoint is RESPONDING! ({elapsed:.1f}s elapsed)")
            print(f"   {message}")
            print()
            print("🚀 Executing complete validation pipeline immediately...")
            print()
            
            # Execute complete pipeline
            pipeline_script = PROJECT_ROOT / "tools" / "run_fastapi_validation_complete.bat"
            if sys.platform == "win32":
                cmd = [str(pipeline_script)]
            else:
                # Use shell script for Linux/Mac
                pipeline_script = PROJECT_ROOT / "tools" / "run_fastapi_validation_complete.sh"
                cmd = ["bash", str(pipeline_script)]
            
            try:
                result = subprocess.run(
                    cmd,
                    cwd=PROJECT_ROOT,
                    timeout=600  # 10 minute timeout
                )
                
                if result.returncode == 0:
                    print("\n✅ Complete validation pipeline executed successfully")
                    print("   Handoff message ready for Agent-4")
                    return True
                else:
                    print(f"\n⚠️  Pipeline completed with exit code: {result.returncode}")
                    return False
            except subprocess.TimeoutExpired:
                print("\n❌ Pipeline execution timed out")
                return False
            except Exception as e:
                print(f"\n❌ Error executing pipeline: {e}")
                return False
        else:
            print(f"⏳ [{timestamp}] Health endpoint not ready yet ({elapsed:.1f}s elapsed, check #{check_count})")
            print(f"   {message}")
            
            if check_count % 6 == 0:  # Every minute
                remaining = (end_time - datetime.now()).total_seconds() / 60
                print(f"   ⏱️  {remaining:.1f} minutes remaining")
            print()
        
        time.sleep(interval)
    
    print(f"❌ Timeout: Health endpoint not responding after {max_wait_minutes} minutes")
    print("   Service may need configuration fixes or restart")
    return False


def main():
    parser = argparse.ArgumentParser(
        description="Monitor FastAPI health endpoint and execute validation when ready"
    )
    parser.add_argument("--endpoint", default="http://localhost:8001", help="FastAPI endpoint URL")
    parser.add_argument("--interval", type=int, default=10, help="Check interval in seconds")
    parser.add_argument("--max-wait", type=int, default=30, help="Maximum wait time in minutes")
    args = parser.parse_args()
    
    success = monitor_and_execute(
        endpoint=args.endpoint,
        interval=args.interval,
        max_wait_minutes=args.max_wait
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

