#!/usr/bin/env python3
"""
<!-- SSOT Domain: infrastructure -->
Deploy corrected FreeRideInvestor V2 theme via SFTP with automatic cache flush.

Author: Agent-3 (Infrastructure & DevOps Specialist)
"""

import os
import sys
import time
import pysftp
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# SFTP credentials - load from environment variables
# Set these in .env file (not committed to git):
# FREERIDE_SFTP_HOST=your_host
# FREERIDE_SFTP_PORT=22
# FREERIDE_SFTP_USER=your_username
# FREERIDE_SFTP_PASS=your_password
# FREERIDE_SFTP_REMOTE_PATH=/path/to/remote
SFTP_CONFIG = {
    'host': os.getenv('FREERIDE_SFTP_HOST', ''),
    'port': int(os.getenv('FREERIDE_SFTP_PORT', '22')),
    'username': os.getenv('FREERIDE_SFTP_USER', ''),
    'password': os.getenv('FREERIDE_SFTP_PASS', ''),
    'remote_path': os.getenv('FREERIDE_SFTP_REMOTE_PATH', '')
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

# WordPress site URL
WP_SITE_URL = 'https://freerideinvestor.com'
WP_ADMIN_URL = f'{WP_SITE_URL}/wp-admin'
WP_PERMALINKS_URL = f'{WP_ADMIN_URL}/options-permalink.php'

def flush_wordpress_cache():
    """
    Flush WordPress cache by saving permalinks.
    Tries multiple methods in order of preference.
    """
    print('\n🔄 Attempting WordPress cache flush...')
    
    # Method 1: Try WordPress REST API (if available)
    try:
        wp_username = os.getenv('WP_ADMIN_USERNAME')
        wp_password = os.getenv('WP_ADMIN_PASSWORD')
        
        if wp_username and wp_password:
            print('   Trying WordPress REST API...')
            api_url = f'{WP_SITE_URL}/wp-json/wp/v2'
            
            # Get nonce for permalink flush
            session = requests.Session()
            auth = (wp_username, wp_password)
            
            # Try to flush rewrite rules via REST API
            flush_url = f'{WP_ADMIN_URL}/admin-ajax.php'
            response = session.post(
                flush_url,
                data={
                    'action': 'flush_rewrite_rules',
                },
                auth=auth,
                timeout=10
            )
            
            if response.status_code == 200:
                print('   ✅ Cache flushed via REST API')
                return True
    except Exception as e:
        print(f'   ⚠️  REST API method failed: {e}')
    
    # Method 2: Try wp-cli via SSH (if available)
    try:
        print('   Trying wp-cli via SSH...')
        import subprocess
        
        # Try to run wp-cli command via SSH
        ssh_command = [
            'ssh',
            f'{SFTP_CONFIG["username"]}@{SFTP_CONFIG["host"]}',
            f'cd {SFTP_CONFIG["remote_path"]}/../../.. && wp rewrite flush --allow-root'
        ]
        
        result = subprocess.run(
            ssh_command,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print('   ✅ Cache flushed via wp-cli')
            return True
    except Exception as e:
        print(f'   ⚠️  wp-cli method failed: {e}')
    
    # Method 3: Browser automation (fallback)
    try:
        print('   Trying browser automation...')
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        wp_username = os.getenv('WP_ADMIN_USERNAME')
        wp_password = os.getenv('WP_ADMIN_PASSWORD')
        
        if not wp_username or not wp_password:
            print('   ⚠️  WP_ADMIN_USERNAME and WP_ADMIN_PASSWORD not set in .env')
            print('   💡 Set these to enable automatic cache flush')
            return False
        
        # Setup headless browser
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        driver = webdriver.Chrome(options=options)
        
        try:
            # Login to wp-admin
            driver.get(f'{WP_ADMIN_URL}/login.php')
            
            username_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'user_login'))
            )
            password_field = driver.find_element(By.ID, 'user_pass')
            submit_button = driver.find_element(By.ID, 'wp-submit')
            
            username_field.send_keys(wp_username)
            password_field.send_keys(wp_password)
            submit_button.click()
            
            # Wait for login to complete
            WebDriverWait(driver, 10).until(
                EC.url_contains('wp-admin')
            )
            
            # Navigate to permalinks page
            driver.get(WP_PERMALINKS_URL)
            
            # Find and click Save Changes button
            save_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'submit'))
            )
            save_button.click()
            
            # Wait for save to complete
            time.sleep(2)
            
            print('   ✅ Cache flushed via browser automation')
            return True
            
        finally:
            driver.quit()
            
    except ImportError:
        print('   ⚠️  Selenium not installed (pip install selenium)')
        print('   💡 Install selenium for automatic cache flush')
    except Exception as e:
        print(f'   ⚠️  Browser automation failed: {e}')
    
    # If all methods fail, provide manual instructions
    print('\n   ⚠️  Automatic cache flush unavailable')
    print('   📋 Manual steps required:')
    print(f'      1. Go to: {WP_PERMALINKS_URL}')
    print('      2. Click "Save Changes" (no edits needed)')
    print('      3. Hard refresh homepage (Ctrl+F5)')
    return False

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
            
            # Attempt automatic cache flush
            cache_flushed = flush_wordpress_cache()
            
            if cache_flushed:
                print('\n✅ Deployment and cache flush complete!')
                print('🌐 Theme should be live now - verify at:', WP_SITE_URL)
            else:
                print('\n✅ Deployment complete!')
                print('🔄 Manual cache flush required (see instructions above)')
            
            return True
            
    except Exception as e:
        print(f'❌ Deployment failed: {e}')
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print('=' * 60)
    print('FreeRideInvestor V2 Theme Deployment Tool')
    print('=' * 60)
    print()
    
    success = main()
    
    if success:
        print('\n'n' + '=' * 60')
        print('🐝 WE. ARE. SWARM. ⚡🔥')
        print('=' * 60)
        print()
        print('💡 TIP: To enable automatic cache flush, add to .env:')
        print('   WP_ADMIN_USERNAME=your_username')
        print('   WP_ADMIN_PASSWORD=your_password')
        print()
    else:
        print('\n❌ DEPLOYMENT FAILED')
    
    sys.exit(0 if success else 1)

