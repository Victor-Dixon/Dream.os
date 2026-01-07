import requests
import json

try:
    response = requests.get('http://localhost:8001/health', timeout=5)
    data = response.json()
    print('FastAPI Health Check:')
    print(f'Status: {response.status_code}')
    print(f'Overall: {data.get("overall_status", "unknown")}')
    print(f'Analytics: {data.get("analytics_status", "unknown")}')
    print(f'FastAPI: {data.get("fastapi_status", "unknown")}')
except Exception as e:
    print(f'FastAPI health check failed: {e}')