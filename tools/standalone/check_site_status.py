#!/usr/bin/env python3
import json
from pathlib import Path

# Load current site status
audit_file = Path('docs/site_audit/broken_links.json')
if audit_file.exists():
    with open(audit_file, 'r') as f:
        data = json.load(f)

    print('🔍 CURRENT SITE HEALTH STATUS:')
    print('=' * 50)

    total_broken = 0
    for site, info in data['sites'].items():
        broken_count = len(info.get('broken_links', []))
        total_broken += broken_count
        status = '✅ OK' if broken_count == 0 else f'❌ {broken_count} broken links'
        print(f'{site}: {status}')

        if broken_count > 0:
            for link in info['broken_links']:
                print(f'  - {link["text"]} → {link["url"]} ({link["status"]})')

    print(f'\n📊 SUMMARY: {total_broken} total broken links across {len(data["sites"])} sites')

    # Provide recommendations
    print('\n🎯 RECOMMENDED FIXES:')
    print('=' * 30)

    if total_broken > 0:
        print('1. 🔗 Broken Link Fixes (Priority: HIGH)')
        for site, info in data['sites'].items():
            broken_links = info.get('broken_links', [])
            if broken_links:
                print(f'   - {site}: {len(broken_links)} broken links')
                for link in broken_links:
                    if link['url'].startswith('https://github.com/Agent_Cellphone_V2_Repository'):
                        print('     → GitHub link: Update to correct repository URL or remove')
                    elif 'tradingrobotplug.com/products' in link['url']:
                        print('     → Missing page: Create Products page')
                    elif 'tradingrobotplug.com/features' in link['url']:
                        print('     → Missing page: Create Features page')
                    elif 'freerideinvestor.com/about' in link['url']:
                        print('     → Missing page: Create About page')
                    else:
                        print(f'     → {link["url"]}: Check and fix')

        print('\n2. 🔧 SFTP Connectivity (All sites showing issues)')
        print('   - Verify Hostinger SFTP credentials')
        print('   - Check firewall/network connectivity')
        print('   - Update site_configs.json with correct credentials')

        print('\n3. 🚀 Automated Fixes Available:')
        print('   - Hostinger WordPress Manager: API-based fixes')
        print('   - WordPress Manager: SFTP-based deployment')
        print('   - Manual WordPress admin: Direct fixes')
else:
    print('❌ Site audit file not found')
