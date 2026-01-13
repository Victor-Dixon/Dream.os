#!/usr/bin/env python3
import os
from pathlib import Path
from datetime import datetime, timezone
from dotenv import load_dotenv

# Load environment
load_dotenv()
load_dotenv('.env.discord')

def split_content_into_pages(content, max_length=1900):
    if len(content) <= max_length:
        return [content]

    pages = []
    remaining = content

    while remaining:
        if len(remaining) <= max_length:
            pages.append(remaining)
            break

        break_pos = max_length

        # Look for paragraph break
        paragraph_break = remaining.rfind('\n\n', max_length-200, max_length)
        if paragraph_break > max_length * 0.7:
            break_pos = paragraph_break

        # Look for line break
        elif '\n' in remaining[max_length-100:max_length]:
            line_break = remaining.rfind('\n', max_length-100, max_length)
            if line_break > 0:
                break_pos = line_break

        # Look for sentence break
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

# Test with actual devlog
devlog_path = Path('devlogs/agent3_website_infrastructure_optimization_20260111.md')
if devlog_path.exists():
    with open(devlog_path, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f'✅ Loaded devlog: {len(content)} characters')

    pages = split_content_into_pages(content, 1700)
    print(f'✅ Split into {len(pages)} pages')

    # Test first page posting
    if pages:
        agent_id = 'Agent-3'
        page_content = pages[0]
        page_num = 1
        total_pages = len(pages)

        d2a_template = f'''🤖 **AGENT DEVLOG POST**
**File**: {devlog_path.name}
**Timestamp**: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}

🐝 **SWARM DEVLOG BROADCAST**
**Agent {agent_id}** has posted an updated devlog with progress and achievements.

**Devlog Content**:'''

        if total_pages > 1:
            d2a_template += f'\n**Page {page_num}/{total_pages}**'

        full_content = f'{d2a_template}\n\n{page_content}\n\n🐝 WE. ARE. SWARM. ⚡🔥'

        print(f'📤 Page content length: {len(page_content)} characters')
        print(f'📤 Template length: {len(d2a_template)} characters')
        print(f'📤 Total message length: {len(full_content)} characters')
        print(f'   Status: {"OK" if len(full_content) <= 2000 else "TOO LONG"}')

        # Show where the split happened
        print(f'\\n📄 PAGE CONTENT PREVIEW (first 200 chars):')
        print(repr(page_content[:200]))

        # Test webhook
        webhook_env_var = f'DISCORD_WEBHOOK_{agent_id.replace("-", "_").upper()}'
        webhook_url = os.getenv(webhook_env_var)

        if webhook_url:
            import requests
            payload = {
                'username': f'{agent_id} Devlog (D2A)',
                'content': full_content
            }

            try:
                response = requests.post(webhook_url, json=payload, timeout=10)
                print(f'📤 Webhook response: HTTP {response.status_code}')

                if response.status_code == 204:
                    print('✅ SUCCESS: First page posted!')
                else:
                    print(f'❌ FAILED: HTTP {response.status_code}')
                    if response.text:
                        print(f'   Error: {response.text[:200]}')
            except Exception as e:
                print(f'❌ Exception: {e}')
        else:
            print('❌ No webhook URL found')
else:
    print('❌ Devlog file not found')