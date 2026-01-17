#!/usr/bin/env python3
"""
Debug Discord message formatting
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timezone

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Load environment variables
try:
    from dotenv import load_dotenv
    # Load main .env file first
    load_dotenv()
    # Then load Discord-specific configuration
    load_dotenv('.env.discord')
    print("✅ Environment variables loaded")
except ImportError:
    print("⚠️ python-dotenv not available")

def test_message_formatting():
    # Simulate what devlog poster creates
    agent_id = 'Agent-3'
    page_content = '# 🚀 WEBSITE INFRASTRUCTURE OPTIMIZATION - Agent-3 Deployment Report\n**Date:** 2026-01-11\n**Agent:** Agent-3 (Infrastructure & Deployment Specialist)\n**Mission:** Bilateral coordination with Agent-4 for website performance optimization\n\n## 📊 EXECUTION SUMMARY\n\nSuccessfully transformed coordination message into forward momentum by executing comprehensive website infrastructure optimization across 9 WordPress sites.'
    page_num = 1
    total_pages = 3

    # Template from devlog poster
    d2a_template = f'''🤖 **AGENT DEVLOG POST**
**File**: agent3_website_infrastructure_optimization_20260111.md
**Timestamp**: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")}

🐝 **SWARM DEVLOG BROADCAST**
**Agent {agent_id}** has posted an updated devlog with progress and achievements.

**Devlog Content**:'''

    # Add pagination info
    if total_pages > 1:
        d2a_template += f'\n**Page {page_num}/{total_pages}**'

    # Format the complete D2A message
    full_content = f'{d2a_template}\n\n{page_content}\n\n🐝 WE. ARE. SWARM. ⚡🔥'

    print('📤 DISCORD MESSAGE ANALYSIS')
    print('=' * 50)
    print(f'Total message length: {len(full_content)} characters')
    print(f'Discord limit: 2000 characters')
    print(f'Status: {"✅ OK" if len(full_content) <= 2000 else "❌ TOO LONG"}')

    print(f'\n📄 MESSAGE PREVIEW (first 300 chars):')
    print('=' * 40)
    print(full_content[:300] + '...' if len(full_content) > 300 else full_content)

    # Check for problematic characters
    problematic = []
    for char in full_content:
        if ord(char) < 32 and char not in '\n\r\t':
            problematic.append(repr(char))

    if problematic:
        print(f'\n⚠️ PROBLEMATIC CHARACTERS FOUND: {list(set(problematic))}')
    else:
        print('\n✅ No problematic characters found')

    # Test webhook
    webhook_url = os.getenv('DISCORD_WEBHOOK_AGENT_3')
    if webhook_url:
        print(f'\n🔗 TESTING WEBHOOK: {webhook_url[:50]}...')

        import requests
        payload = {
            'username': f'{agent_id} Devlog (D2A)',
            'content': full_content
        }

        try:
            response = requests.post(webhook_url, json=payload, timeout=10)
            print(f'📤 Webhook response: HTTP {response.status_code}')

            if response.status_code == 204:
                print('✅ Message sent successfully!')
            elif response.status_code == 400:
                print('❌ HTTP 400 - Bad request')
                if response.text:
                    print(f'   Error details: {response.text[:200]}')
            else:
                print(f'❌ Unexpected response: {response.status_code}')

        except Exception as e:
            print(f'❌ Webhook test failed: {e}')
    else:
        print('\n❌ No webhook URL found for Agent-3')

if __name__ == "__main__":
    test_message_formatting()