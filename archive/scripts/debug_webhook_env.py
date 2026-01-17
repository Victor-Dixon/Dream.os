#!/usr/bin/env python3
import os
from dotenv import load_dotenv

# Load env files like devlog poster does
load_dotenv()
load_dotenv('.env.discord')

agent_id = 'Agent-3'
webhook_env_var = f'DISCORD_WEBHOOK_{agent_id.replace("-", "_").upper()}'
webhook_url = os.getenv(webhook_env_var)

print(f'🔍 Looking for {webhook_env_var}')
print(f'   Found: {"YES" if webhook_url else "NO"}')

if webhook_url:
    print(f'   URL: {webhook_url[:50]}...')

    # Test with a simple message
    import requests
    payload = {'username': f'{agent_id} Test', 'content': '🧪 Devlog poster webhook test'}
    response = requests.post(webhook_url, json=payload, timeout=10)
    print(f'   Test response: HTTP {response.status_code}')
else:
    print('❌ Webhook URL not found')
    print('   Available DISCORD_WEBHOOK_* variables:')
    for key, value in os.environ.items():
        if key.startswith('DISCORD_WEBHOOK_'):
            print(f'   {key}: {"SET" if value else "EMPTY"}')