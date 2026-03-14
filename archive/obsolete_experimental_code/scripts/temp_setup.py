#!/usr/bin/env python3
"""
Temporary script to set Robinhood credentials
"""

import os

# Set your credentials here
os.environ['ROBINHOOD_USERNAME'] = 'DaDudeKC@gmail.com'
os.environ['ROBINHOOD_PASSWORD'] = 'your_password_here'  # Replace with actual password
os.environ['ROBINHOOD_TOTP_SECRET'] = ''  # Leave empty for manual 2FA

print("Environment variables set. Now run:")
print("python tools/robinhood_auth_test.py")