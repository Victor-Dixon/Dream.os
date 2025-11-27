"""Check GitHub API rate limit status."""
import os
import requests
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
    print("❌ GITHUB_TOKEN not found")
    exit(1)

headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json'
}

try:
    r = requests.get('https://api.github.com/rate_limit', headers=headers, timeout=10)
    data = r.json()
    
    core = data.get('resources', {}).get('core', {})
    search = data.get('resources', {}).get('search', {})
    
    remaining = core.get('remaining', 0)
    limit = core.get('limit', 0)
    reset_time = core.get('reset', 0)
    
    import time
    reset_in_seconds = max(0, reset_time - time.time())
    reset_in_minutes = reset_in_seconds / 60
    
    print(f"📊 GitHub API Rate Limit Status")
    print(f"   Remaining: {remaining}/{limit}")
    print(f"   Reset: {reset_in_minutes:.1f} minutes ({reset_in_seconds:.0f} seconds)")
    
    if remaining == 0:
        print(f"   ⚠️  RATE LIMIT EXCEEDED - Wait {reset_in_minutes:.1f} minutes")
    elif remaining < 100:
        print(f"   ⚠️  Low remaining requests - Use carefully")
    else:
        print(f"   ✅ Rate limit OK")
        
except Exception as e:
    print(f"❌ Error checking rate limit: {e}")

