#!/usr/bin/env python3
"""Verify Chain 4 sub-chain directories exist."""

from pathlib import Path

dirs = [
    'src/core/integration_coordinators',
    'src/core/emergency_intervention',
    'src/services/coordination',
    'src/services/protocol',
    'src/services/utils',
]

print("Chain 4 Directory Verification:")
print("=" * 50)

for dir_path in dirs:
    path = Path(dir_path)
    exists = path.exists()
    status = "✅ EXISTS" if exists else "❌ MISSING"
    print(f"{dir_path}: {status}")
    
    if exists:
        files = list(path.glob("*.py"))
        print(f"  Files: {len(files)} Python files")
        if files:
            print(f"  Examples: {', '.join([f.name for f in files[:3]])}")

print("\n" + "=" * 50)

