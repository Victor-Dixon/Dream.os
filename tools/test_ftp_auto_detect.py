#!/usr/bin/env python3
"""Test FTP auto-detection."""

from pathlib import Path
from tools.ftp_deployer import detect_site_from_path, load_site_configs

print("🧪 Testing FTP Auto-Detection")
print("=" * 60)

test_cases = [
    ("D:/websites/FreeRideInvestor/functions.php", "freerideinvestor"),
    ("D:/websites/prismblossom.online/style.css", "prismblossom"),
    ("D:/websites/southwestsecret.com/functions.php", "southwestsecret"),
    ("D:/websites/ariajet.site/index.html", "ariajet"),
]

for file_path, expected in test_cases:
    detected = detect_site_from_path(Path(file_path))
    status = "✅" if detected == expected or (detected and expected in detected.lower()) else "❌"
    print(f"{status} {file_path}")
    print(f"   Expected: {expected}, Detected: {detected}")

print("\n📋 All Available Sites:")
site_configs = load_site_configs()
for site in sorted(site_configs.keys()):
    print(f"  • {site}")

