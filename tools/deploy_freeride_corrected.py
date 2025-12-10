#!/usr/bin/env python3
"""Deploy corrected FreeRideInvestor V2 theme via SFTP."""

import os
import sys
import pysftp
from pathlib import Path

# SFTP credentials
SFTP_CONFIG = {
    'host': '185.224.138.49',
    'port': 22,
    'username': 'u996867598',
    'password': 'FreeRideInvestor2024!',
    'remote_path': '/home/u996867598/domains/freerideinvestor.com/public_html/wp-content/themes/freerideinvestor'
}

# Files to deploy
FILES_TO_DEPLOY = [
    'D:/websites/FreeRideInvestor_V2/style.css',
    'D:/websites/FreeRideInvestor_V2/functions.php',
    'D:/websites/FreeRideInvestor_V2/index.php',
    'D:/websites/FreeRideInvestor_V2/home.php',
    'D:/websites/FreeRideInvestor_V2/header.php',
    'D:/websites/FreeRideInvestor_V2/footer.php',
    'D:/websites/FreeRideInvestor_V2/sidebar.php',
    'D:/websites/FreeRideInvestor_V2/js/theme.js',
]

def main():
    print('🚀 Deploying corrected FreeRideInvestor V2 theme...')
    
    try:
        # Connect to SFTP
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        
        with pysftp.Connection(
            host=SFTP_CONFIG['host'],
            port=SFTP_CONFIG['port'],
            username=SFTP_CONFIG['username'],
            password=SFTP_CONFIG['password'],
            cnopts=cnopts
        ) as sftp:
            print('✅ SFTP connection established')
            
            # Deploy each file
            for file_path in FILES_TO_DEPLOY:
                if os.path.exists(file_path):
                    filename = os.path.basename(file_path)
                    remote_file = f"{SFTP_CONFIG['remote_path']}/{filename}"
                    
                    # Handle subdirectory for JS
                    if 'js/' in file_path:
                        remote_file = f"{SFTP_CONFIG['remote_path']}/js/{filename}"
                        try:
                            sftp.makedirs(f"{SFTP_CONFIG['remote_path']}/js")
                        except:
                            pass
                    
                    sftp.put(file_path, remote_file)
                    print(f'✅ Uploaded: {filename}')
                else:
                    print(f'❌ File not found: {file_path}')
            
            print('🎯 Theme deployment complete!')
            print('🔄 WordPress cache flush required for activation')
            return True
            
    except Exception as e:
        print(f'❌ Deployment failed: {e}')
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = main()
    if success:
        print('\n🐝 WE. ARE. SWARM. ⚡🔥')
        print('Status: ✅ **CORRECTED THEME DEPLOYED - CACHE FLUSH REQUIRED**')
    else:
        print('\n❌ DEPLOYMENT FAILED')
    sys.exit(0 if success else 1)

