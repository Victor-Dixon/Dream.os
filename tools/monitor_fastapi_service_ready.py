#!/usr/bin/env python3
"""
FastAPI Service Readiness Monitor
Proactively monitors FastAPI service and executes tests immediately when ready.

Usage:
    python tools/monitor_fastapi_service_ready.py [--endpoint URL] [--interval SECONDS] [--max-wait MINUTES]
    
Default: Monitors http://localhost:8000 every 10 seconds, max 60 minutes
"""

import time
import sys
import argparse
import subprocess
from pathlib import Path
from datetime import datetime, timedelta

PROJECT_ROOT = Path(__file__).parent.parent


def check_service_health(endpoint: str) -> tuple[bool, str]:
    """Check if FastAPI service is responding with health check."""
    try:
        import requests
        health_url = f"{endpoint}/health"
        response = requests.get(health_url, timeout=5)
        
        if response.status_code == 200:
            return True, f"Service healthy at {endpoint}"
        else:
            return False, f"Service responding but health check returned {response.status_code}"
    except requests.exceptions.ConnectionError:
        return False, "Connection refused - service not running"
    except requests.exceptions.Timeout:
        return False, "Connection timeout"
    except Exception as e:
        return False, f"Error: {str(e)}"


def monitor_and_execute(endpoint: str = "http://localhost:8000", 
                        interval: int = 10, 
                        max_wait_minutes: int = 60,
                        auto_execute: bool = True):
    """Monitor service and execute tests when ready."""
    max_wait_seconds = max_wait_minutes * 60
    start_time = datetime.now()
    end_time = start_time + timedelta(seconds=max_wait_seconds)
    
    print(f"🔍 Monitoring FastAPI service readiness...")
    print(f"   Endpoint: {endpoint}")
    print(f"   Check interval: {interval} seconds")
    print(f"   Max wait time: {max_wait_minutes} minutes")
    print(f"   Auto-execute tests: {auto_execute}")
    print()
    
    check_count = 0
    
    while datetime.now() < end_time:
        check_count += 1
        is_ready, message = check_service_health(endpoint)
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        elapsed = (datetime.now() - start_time).total_seconds()
        
        if is_ready:
            print(f"✅ [{timestamp}] Service is READY! ({elapsed:.1f}s elapsed)")
            print(f"   {message}")
            print()
            
            if auto_execute:
                print("🚀 Executing test suite immediately...")
                print()
                test_script = PROJECT_ROOT / "tools" / "execute_fastapi_tests_immediate.py"
                
                try:
                    result = subprocess.run(
                        [sys.executable, str(test_script), "--endpoint", endpoint],
                        cwd=PROJECT_ROOT,
                        timeout=600  # 10 minute timeout for tests
                    )
                    
                    if result.returncode == 0:
                        print("\n✅ Test execution completed successfully")
                    else:
                        print(f"\n❌ Test execution completed with errors (exit code: {result.returncode})")
                    
                    return True
                except subprocess.TimeoutExpired:
                    print("\n❌ Test execution timed out")
                    return False
                except Exception as e:
                    print(f"\n❌ Error executing tests: {e}")
                    return False
            else:
                print("✅ Service ready - tests can be executed manually")
                return True
        else:
            print(f"⏳ [{timestamp}] Service not ready yet ({elapsed:.1f}s elapsed, check #{check_count})")
            print(f"   {message}")
            
            if check_count % 6 == 0:  # Every minute (6 checks at 10s interval)
                remaining = (end_time - datetime.now()).total_seconds() / 60
                print(f"   ⏱️  {remaining:.1f} minutes remaining")
            print()
        
        time.sleep(interval)
    
    print(f"❌ Timeout: Service not ready after {max_wait_minutes} minutes")
    return False


def main():
    parser = argparse.ArgumentParser(description="Monitor FastAPI service and execute tests when ready")
    parser.add_argument("--endpoint", default="http://localhost:8001", help="FastAPI endpoint URL")
    parser.add_argument("--interval", type=int, default=10, help="Check interval in seconds")
    parser.add_argument("--max-wait", type=int, default=60, help="Maximum wait time in minutes")
    parser.add_argument("--no-auto-execute", action="store_true", help="Don't auto-execute tests, just monitor")
    args = parser.parse_args()
    
    success = monitor_and_execute(
        endpoint=args.endpoint,
        interval=args.interval,
        max_wait_minutes=args.max_wait,
        auto_execute=not args.no_auto_execute
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

