import requests
import time
import sys

print("Waiting for FastAPI service to start...")
time.sleep(5)

try:
    response = requests.get('http://localhost:8001/health', timeout=10)
    print(f'✅ FastAPI Health Check - Status: {response.status_code}')
    data = response.json()
    print(f'   Overall Status: {data.get("overall_status", "unknown")}')
    print(f'   Analytics Status: {data.get("analytics_status", "unknown")}')
    print(f'   FastAPI Status: {data.get("fastapi_status", "unknown")}')
    sys.exit(0)
except requests.exceptions.Timeout:
    print('❌ FastAPI health check: Timeout - service may not be responding')
    sys.exit(1)
except Exception as e:
    print(f'❌ FastAPI health check failed: {e}')
    sys.exit(1)