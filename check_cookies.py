#!/usr/bin/env python3
"""
Check Thea cookie contents
"""

from src.services.thea_secure_cookie_manager import SecureCookieManager
import json

try:
    manager = SecureCookieManager()

    # Manually decrypt to see what's in there
    if manager.cookie_file.exists():
        with open(manager.cookie_file, 'rb') as f:
            encrypted_data = f.read()

        decrypted_data = manager.fernet.decrypt(encrypted_data)
        cookie_data = json.loads(decrypted_data.decode('utf-8'))

        print('Cookie data keys:', list(cookie_data.keys()))
        if 'timestamp' in cookie_data:
            print('Timestamp:', cookie_data['timestamp'])
        else:
            print('❌ No timestamp field!')

        if 'cookies' in cookie_data:
            print(f'Number of cookies: {len(cookie_data["cookies"])}')

        print('Full cookie data:')
        for key, value in cookie_data.items():
            if key == 'cookies':
                print(f'  {key}: [{len(value)} cookies]')
            else:
                print(f'  {key}: {value}')

except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()