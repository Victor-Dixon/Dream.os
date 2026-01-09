#!/usr/bin/env python3
import requests
import json

# Simple test query
data = {
    'query': 'What are the main coordination challenges in the current system?',
    'mode': 'analytical'
}

try:
    response = requests.post('http://localhost:8001/ai/reason', json=data, timeout=10)
    if response.status_code == 200:
        result = response.json()
        print('✅ AI Reasoning Engine Response:')
        response_text = result.get('response', 'No response')[:200]
        print(f'Response: {response_text}...')
        print(f'Confidence: {result.get("confidence", "N/A")}')
        print(f'Processing Time: {result.get("processing_time", "N/A")}s')
    else:
        print(f'❌ HTTP Error: {response.status_code}')
        print(response.text[:500])
except Exception as e:
    print(f'❌ Connection Error: {e}')