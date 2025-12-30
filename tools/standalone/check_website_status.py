#!/usr/bin/env python3
"""Check website branding status."""
from tools.wordpress_manager import WordPressManager
import json

print('🌐 Checking weareswarm.online branding status...')
print('=' * 60)

manager = WordPressManager('weareswarm.online')
if manager.connect():
    # Check site name
    stdout, stderr, code = manager.wp_cli('option get blogname')
    site_name = stdout.strip() if code == 0 else 'Unknown'
    print(f'Site Name: {site_name}')
    
    # Check for any remaining FLAVIO references (dry run)
    stdout, stderr, code = manager.wp_cli('search-replace "FLAVIO" "CHECK" --dry-run --all-tables')
    if code == 0 and ('FLAVIO' in stdout.upper() or 'replacement' in stdout.lower()):
        print('⚠️  Still found FLAVIO references in database')
    else:
        print('✅ No FLAVIO references found in database')
    
    # Check menu status
    stdout, stderr, code = manager.wp_cli('menu list --format=json')
    if code == 0 and stdout.strip():
        menus = json.loads(stdout)
        swarm_menu = [m for m in menus if 'swarm' in m.get('name', '').lower()]
        if swarm_menu:
            print(f'✅ Swarm menu found: {swarm_menu[0].get("name")}')
        else:
            print('⚠️  Swarm menu not found')
    
    manager.disconnect()
    print('\n✅ Website check complete')
else:
    print('❌ Could not connect to website')

