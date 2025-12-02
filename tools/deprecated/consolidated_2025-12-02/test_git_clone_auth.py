"""Test git clone authentication with actual merge repositories."""
import os
import subprocess
import tempfile
from pathlib import Path

try:
    from dotenv import load_dotenv
    env_path = Path('.env')
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    pass

token = os.getenv('GITHUB_TOKEN')
username = os.getenv('GITHUB_USERNAME', 'Dadudekc')

# Merge #1 repositories
target_repo = 'Streamertools'  # Target (capital S)
source_repo = 'streamertools'  # Source (lowercase s)

print(f"🔍 Testing git clone authentication...")
print(f"   Token: {'Found' if token else 'NOT FOUND'} ({len(token) if token else 0} chars)")
print(f"   Username: {username}")
print(f"   Target: {target_repo}")
print(f"   Source: {source_repo}")

temp_dir = Path(tempfile.mkdtemp(prefix="git_clone_test_"))

# Test target repo clone
print(f"\n📥 Testing target repo clone: {target_repo}...")
if token:
    target_url = f"https://{token}@github.com/{username}/{target_repo}.git"
else:
    target_url = f"https://github.com/{username}/{target_repo}.git"

target_dir = temp_dir / "target"
result = subprocess.run(
    ['git', 'clone', target_url, str(target_dir)],
    capture_output=True,
    text=True,
    timeout=60
)

print(f"   Exit code: {result.returncode}")
if result.returncode != 0:
    print(f"   ❌ FAILED")
    print(f"   Error: {result.stderr[:500]}")
else:
    print(f"   ✅ SUCCESS")

# Test source repo clone
print(f"\n📥 Testing source repo clone: {source_repo}...")
if token:
    source_url = f"https://{token}@github.com/{username}/{source_repo}.git"
else:
    source_url = f"https://github.com/{username}/{source_repo}.git"

source_dir = temp_dir / "source"
result = subprocess.run(
    ['git', 'clone', source_url, str(source_dir)],
    capture_output=True,
    text=True,
    timeout=60
)

print(f"   Exit code: {result.returncode}")
if result.returncode != 0:
    print(f"   ❌ FAILED")
    print(f"   Error: {result.stderr[:500]}")
else:
    print(f"   ✅ SUCCESS")

# Cleanup
import shutil
shutil.rmtree(temp_dir, ignore_errors=True)
print(f"\n🧹 Cleaned up test directory")

