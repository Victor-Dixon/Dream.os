import requests
import time

print("Checking FastAPI service health...")
time.sleep(3)  # Give service time to start

try:
    response = requests.get('http://localhost:8001/health', timeout=10)
    print(f'✅ FastAPI Status: {response.status_code}')
    data = response.json()
    print(f'Overall: {data.get("overall_status", "unknown")}')
    print(f'Analytics: {data.get("analytics_status", "unknown")}')
    print(f'FastAPI: {data.get("fastapi_status", "unknown")}')

    if response.status_code == 200 and data.get("overall_status") == "healthy":
        print("🎉 FastAPI service is fully operational!")
    else:
        print("⚠️ FastAPI service responding but may need configuration")

except requests.exceptions.Timeout:
    print('❌ FastAPI health check: Timeout - service not responding')
except Exception as e:
    print(f'❌ FastAPI health check failed: {e}')