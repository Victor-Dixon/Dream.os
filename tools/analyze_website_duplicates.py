#!/usr/bin/env python3
"""
Analyze Website Directory Duplicates
====================================

Quick analysis tool to identify actual duplicate website directories.
"""

import os
from pathlib import Path

websites_root = Path("D:/websites")

# Check ariajet.site theme locations
ariajet_root_theme = websites_root / "ariajet.site" / "wordpress-theme"
ariajet_websites_theme = websites_root / "websites" / "ariajet.site" / "wp" / "wp-content" / "themes"

print("=" * 60)
print("Website Directory Duplication Analysis")
print("=" * 60)

if ariajet_root_theme.exists():
    root_themes = set(os.listdir(ariajet_root_theme))
    print(f"\n✅ Root theme location exists: {ariajet_root_theme}")
    print(f"   Themes: {sorted(root_themes)}")
else:
    root_themes = set()
    print(f"\n❌ Root theme location missing: {ariajet_root_theme}")

if ariajet_websites_theme.exists():
    websites_themes = set(os.listdir(ariajet_websites_theme))
    print(f"\n✅ Websites theme location exists: {ariajet_websites_theme}")
    print(f"   Themes: {sorted(websites_themes)}")
else:
    websites_themes = set()
    print(f"\n❌ Websites theme location missing: {ariajet_websites_theme}")

if root_themes and websites_themes:
    if root_themes == websites_themes:
        print(f"\n⚠️  DUPLICATE DETECTED: Same themes in both locations!")
        print(f"   Action: Verify if symlinked or consolidate")
    else:
        print(f"\n✅ Different themes: Not duplicates")
        print(f"   Root has: {root_themes - websites_themes}")
        print(f"   Websites has: {websites_themes - root_themes}")

# Check plugin directories
wp_plugins1 = websites_root / "wordpress-plugins"
wp_plugins2 = websites_root / "wp-plugins"

print("\n" + "=" * 60)
print("Plugin Directory Check")
print("=" * 60)

if wp_plugins1.exists():
    plugins1 = set(os.listdir(wp_plugins1))
    print(f"\n✅ wordpress-plugins/ exists: {len(plugins1)} items")
else:
    plugins1 = set()
    print(f"\n❌ wordpress-plugins/ missing")

if wp_plugins2.exists():
    plugins2 = set(os.listdir(wp_plugins2))
    print(f"\n✅ wp-plugins/ exists: {len(plugins2)} items")
else:
    plugins2 = set()
    print(f"\n❌ wp-plugins/ missing")

if plugins1 and plugins2:
    if plugins1 == plugins2:
        print(f"\n⚠️  DUPLICATE DETECTED: Same plugins in both directories!")
    else:
        print(f"\n✅ Different plugins: Not duplicates")
        print(f"   wordpress-plugins has: {plugins1 - plugins2}")
        print(f"   wp-plugins has: {plugins2 - plugins1}")

print("\n" + "=" * 60)


