#!/usr/bin/env python3
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
load_dotenv('.env.discord')

# Load devlog and split
devlog_path = Path('devlogs/agent3_website_infrastructure_optimization_20260111.md')
with open(devlog_path, 'r', encoding='utf-8') as f:
    content = f.read()

def split_content(content, max_length=1700):
    pages = []
    remaining = content

    while remaining:
        if len(remaining) <= max_length:
            pages.append(remaining)
            break

        break_pos = max_length

        paragraph_break = remaining.rfind('\n\n', max_length-200, max_length)
        if paragraph_break > max_length * 0.7:
            break_pos = paragraph_break

        elif '\n' in remaining[max_length-100:max_length]:
            line_break = remaining.rfind('\n', max_length-100, max_length)
            if line_break > 0:
                break_pos = line_break

        elif '.' in remaining[max_length-50:max_length]:
            sentence_break = remaining.rfind('.', max_length-50, max_length)
            if sentence_break > 0:
                break_pos = sentence_break + 1

        page = remaining[:break_pos]
        pages.append(page)
        remaining = remaining[break_pos:].lstrip()

        if len(pages) > 10:
            break

    return pages

pages = split_content(content, 1700)
page_2_content = pages[1]

# Create page 2 message
agent_id = 'Agent-3'
page_num = 2
total_pages = len(pages)

d2a_template = f'''🤖 **AGENT DEVLOG POST**
**File**: {devlog_path.name}
**Timestamp**: 2026-01-13 00:13:00 UTC

🐝 **SWARM DEVLOG BROADCAST**
**Agent {agent_id}** has posted an updated devlog with progress and achievements.

**Devlog Content**:
**Page {page_num}/{total_pages}**

{page_2_content}

🐝 WE. ARE. SWARM. ⚡🔥'''

print(f'Message length: {len(d2a_template)} characters')
print(f'Status: {"OK" if len(d2a_template) <= 2000 else "TOO LONG"}')

# Test webhook
webhook_url = os.getenv('DISCORD_WEBHOOK_AGENT_3')
if webhook_url:
    import requests
    payload = {
        'username': f'{agent_id} Devlog (D2A)',
        'content': d2a_template
    }

    response = requests.post(webhook_url, json=payload, timeout=10)
    print(f'Webhook response: HTTP {response.status_code}')

    if response.status_code != 204:
        print(f'Error: {response.text}')
else:
    print('No webhook URL found')