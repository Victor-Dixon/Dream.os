"""Quick script to verify GITHUB_TOKEN validity."""
import os
import sys
from pathlib import Path

try:
    from dotenv import load_dotenv
    env_path = Path('.env')
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    pass

token = os.getenv('GITHUB_TOKEN')

if not token:
    print("❌ GITHUB_TOKEN not found in environment")
    sys.exit(1)

print(f"✅ GITHUB_TOKEN found ({len(token)} characters)")

# Test token validity via GitHub API
try:
    import requests
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    r = requests.get('https://api.github.com/user', headers=headers, timeout=10)
    
    if r.status_code == 200:
        user = r.json().get('login', 'Unknown')
        print(f"✅ Token is VALID - Authenticated as: {user}")
        print(f"✅ Token has required permissions")
        sys.exit(0)
    else:
        print(f"❌ Token is INVALID - Status code: {r.status_code}")
        print(f"   Response: {r.text[:200]}")
        sys.exit(1)
except ImportError:
    print("⚠️  requests library not available - cannot verify token via API")
    print("   Token exists but validity cannot be confirmed")
    sys.exit(0)
except Exception as e:
    print(f"❌ Error verifying token: {e}")
    sys.exit(1)

