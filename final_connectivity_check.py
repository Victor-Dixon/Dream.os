import requests

print('🔍 Post-Restoration Connectivity Check')
print('-' * 50)

# Check Flask service
try:
    response = requests.get('http://localhost:8000/health', timeout=5)
    print(f'✅ Flask (8000): HTTP {response.status_code}')
except Exception as e:
    print(f'❌ Flask (8000): {str(e)[:50]}')

# Check FastAPI service
try:
    response = requests.get('http://localhost:8001/health', timeout=5)
    data = response.json()
    status = data.get("overall_status", "unknown")
    print(f'✅ FastAPI (8001): HTTP {response.status_code} - Status: {status}')
except Exception as e:
    print(f'❌ FastAPI (8001): {str(e)[:50]}')

print()
if "✅ Flask (8000): HTTP" in str() and "✅ FastAPI (8001): HTTP" in str():
    print('🎯 REVENUE ENGINE CONNECTIVITY: FULLY RESTORED')
    print('🚀 Agent-1 validation can proceed immediately!')
else:
    print('⚠️ Connectivity restoration in progress...')