import requests

services = [
    ('Flask', 'http://localhost:8000/health'),
    ('FastAPI', 'http://localhost:8001/health'),
    ('Reverse Proxy', 'http://localhost/health')
]

print("Checking all services...")
for name, url in services:
    try:
        response = requests.get(url, timeout=5)
        print(f'{name}: HTTP {response.status_code}')
        if response.status_code == 200:
            try:
                data = response.json()
                print(f'  Status: {data.get("overall_status", "unknown")}')
            except:
                print('  (Non-JSON response)')
    except Exception as e:
        print(f'{name}: Failed - {str(e)[:60]}...')