#!/usr/bin/env python3
"""
Coordination Health Check Tool
=============================

Checks health of coordination systems:
- Message queue processor status
- Broadcast system configuration
- Coordination workflow validation

Author: Agent-6 (Coordination & Communication Specialist)
Date: 2025-12-10
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def check_message_queue_processor():
    """Check message queue processor health."""
    print("=" * 80)
    print("MESSAGE QUEUE PROCESSOR HEALTH CHECK")
    print("=" * 80)
    
    processor_file = project_root / "src" / "core" / "message_queue_processor.py"
    
    if not processor_file.exists():
        print("❌ ERROR: Message queue processor file not found")
        return False
    
    with open(processor_file, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')
    
    # Check for throttling
    has_throttle = False
    throttle_lines = []
    
    for i, line in enumerate(lines, 1):
        if 'time.sleep' in line and ('0.5' in line or '1.0' in line):
            has_throttle = True
            throttle_lines.append((i, line.strip()))
    
    print(f"\n📋 Throttling Configuration:")
    print("-" * 80)
    if has_throttle:
        print("✅ Throttling found:")
        for line_num, line_content in throttle_lines:
            print(f"   Line {line_num}: {line_content}")
    else:
        print("❌ No throttling found")
    
    # Check for error handling
    has_error_handling = 'try:' in content and 'except' in content
    
    print(f"\n📋 Error Handling:")
    print("-" * 80)
    if has_error_handling:
        print("✅ Error handling present")
    else:
        print("⚠️  Error handling not verified")
    
    return has_throttle

def check_broadcast_system():
    """Check broadcast system health."""
    print("\n" + "=" * 80)
    print("BROADCAST SYSTEM HEALTH CHECK")
    print("=" * 80)
    
    infra_file = project_root / "src" / "services" / "messaging_infrastructure.py"
    
    if not infra_file.exists():
        print("❌ ERROR: Messaging infrastructure file not found")
        return False
    
    with open(infra_file, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')
    
    # Check for broadcast_to_all method
    has_broadcast = 'def broadcast_to_all' in content
    
    print(f"\n📋 Broadcast Method:")
    print("-" * 80)
    if has_broadcast:
        print("✅ broadcast_to_all method found")
    else:
        print("❌ broadcast_to_all method not found")
        return False
    
    # Check for throttling in fallback path
    has_fallback_throttle = False
    throttle_line = None
    
    for i, line in enumerate(lines, 1):
        if 'falling back to direct broadcast' in line:
            # Check next 30 lines for throttling
            for j in range(i, min(len(lines), i+30)):
                if 'time.sleep(1.0)' in lines[j] or ('time.sleep' in lines[j] and '1.0' in lines[j]):
                    has_fallback_throttle = True
                    throttle_line = j + 1
                    break
            if has_fallback_throttle:
                break
    
    print(f"\n📋 Fallback Path Throttling:")
    print("-" * 80)
    if has_fallback_throttle:
        print(f"✅ Throttling found at line {throttle_line}")
    else:
        print("❌ Throttling not found in fallback path")
    
    # Check for queue path (should use queue processor)
    has_queue_path = 'queue.enqueue' in content or 'queue =' in content
    
    print(f"\n📋 Queue Path:")
    print("-" * 80)
    if has_queue_path:
        print("✅ Queue path present (uses queue processor)")
    else:
        print("⚠️  Queue path not verified")
    
    return has_broadcast and has_fallback_throttle

def check_coordination_workflows():
    """Check coordination workflow health."""
    print("\n" + "=" * 80)
    print("COORDINATION WORKFLOW HEALTH CHECK")
    print("=" * 80)
    
    # Check for coordination tools
    coordination_tools = [
        "tools/validate_broadcast_pacing.py",
        "src/services/messaging_infrastructure.py",
        "src/core/message_queue_processor.py",
    ]
    
    print(f"\n📋 Coordination Tools:")
    print("-" * 80)
    all_present = True
    for tool_path in coordination_tools:
        tool_file = project_root / tool_path
        if tool_file.exists():
            print(f"✅ {tool_path}")
        else:
            print(f"❌ {tool_path} - NOT FOUND")
            all_present = False
    
    return all_present

def main():
    """Run all health checks."""
    print("\n" + "=" * 80)
    print("COORDINATION HEALTH CHECK")
    print("=" * 80)
    print()
    
    results = {
        "message_queue": check_message_queue_processor(),
        "broadcast_system": check_broadcast_system(),
        "coordination_workflows": check_coordination_workflows(),
    }
    
    print("\n" + "=" * 80)
    print("HEALTH CHECK SUMMARY")
    print("=" * 80)
    print()
    
    all_healthy = True
    for check_name, result in results.items():
        status = "✅ HEALTHY" if result else "❌ UNHEALTHY"
        print(f"{check_name.replace('_', ' ').title()}: {status}")
        if not result:
            all_healthy = False
    
    print()
    if all_healthy:
        print("✅ ALL SYSTEMS HEALTHY")
        return 0
    else:
        print("⚠️  SOME ISSUES DETECTED - Review above")
        return 1

if __name__ == "__main__":
    sys.exit(main())

