import requests

try:
    response = requests.get('http://localhost:8001/health', timeout=5)
    print('Detailed FastAPI Health Check:')
    print(f'HTTP Status: {response.status_code}')
    data = response.json()
    print(f'Overall Status: {data.get("overall_status")}')
    print(f'Analytics Status: {data.get("analytics_status")}')
    print(f'FastAPI Status: {data.get("fastapi_status")}')
    if 'details' in data:
        print('Details:', data['details'])
    if 'warnings' in data:
        print('Warnings:', data['warnings'])
except Exception as e:
    print(f'Health check error: {e}')