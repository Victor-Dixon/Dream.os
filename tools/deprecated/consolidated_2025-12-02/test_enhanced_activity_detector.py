#!/usr/bin/env python3
"""Test enhanced activity detector."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.orchestrators.overnight.enhanced_agent_activity_detector import EnhancedAgentActivityDetector

detector = EnhancedAgentActivityDetector()
activity = detector.detect_agent_activity("Agent-2")

print("✅ Enhanced Activity Detector Test:")
print(f"Latest Activity: {activity['latest_activity']}")
print(f"Latest Source: {activity['latest_activity_source']}")
print(f"Activity Sources: {activity['activity_sources']}")
print(f"Activity Count: {activity['activity_count']}")
print(f"\nActivity Details:")
for source, details in activity['activity_details'].items():
    print(f"  {source}: {details.get('age_seconds', 0):.0f}s ago")


