#!/usr/bin/env python3
"""Display tool classification results."""

import json
from pathlib import Path

report_path = Path("reports/tool_classification_signal_noise.json")
if not report_path.exists():
    print("❌ Classification report not found. Run classify_tools_signal_noise.py first.")
    exit(1)

with open(report_path) as f:
    data = json.load(f)

print("="*60)
print("TOOL CLASSIFICATION SUMMARY")
print("="*60)
print(f"\n✅ SIGNAL: {data['summary']['SIGNAL']} tools")
print(f"❌ NOISE: {data['summary']['NOISE']} tools")
print(f"❓ UNKNOWN: {data['summary']['UNKNOWN']} tools")
print(f"📦 TOTAL: {data['total_tools']} tools")

print("\n" + "="*60)
print("SIGNAL TOOLS (first 20):")
print("="*60)
for tool in data['classifications']['SIGNAL'][:20]:
    print(f"  ✅ {tool['path']}")
    if tool['reasons']:
        print(f"     → {', '.join(tool['reasons'])}")

print("\n" + "="*60)
print("NOISE TOOLS:")
print("="*60)
for tool in data['classifications']['NOISE']:
    print(f"  ❌ {tool['path']}")
    if tool['reasons']:
        print(f"     → {', '.join(tool['reasons'])}")

print("\n" + "="*60)
print("UNKNOWN TOOLS (first 20):")
print("="*60)
for tool in data['classifications']['UNKNOWN'][:20]:
    print(f"  ❓ {tool['path']}")


