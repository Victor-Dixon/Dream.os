#!/usr/bin/env python3
"""
Coordination Health Check Tool
=============================

Checks health of coordination systems:
- Message queue processor status
- Broadcast system configuration
- Coordination workflow validation
- Basic coordination metrics collection

Author: Agent-6 (Coordination & Communication Specialist)
Date: 2025-12-10
V2 Compliance: <300 lines, single responsibility

<!-- SSOT Domain: infrastructure -->
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

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

def collect_coordination_metrics() -> Dict[str, Any]:
    """
    Collect basic coordination metrics.
    
    Returns:
        Dictionary with coordination metrics
    """
    metrics = {
        "timestamp": datetime.now().isoformat(),
        "message_queue_health": False,
        "broadcast_system_health": False,
        "coordination_tools_health": False,
        "metrics_collected": True,
    }
    
    # Check message queue file
    queue_file = project_root / "runtime" / "agent_comms" / "message_queue.json"
    if queue_file.exists():
        try:
            with open(queue_file, 'r', encoding='utf-8') as f:
                queue_data = json.load(f)
                metrics["queue_size"] = len(queue_data.get("queue", []))
                metrics["queue_processing"] = queue_data.get("processing", False)
        except Exception:
            metrics["queue_size"] = 0
            metrics["queue_processing"] = False
    else:
        metrics["queue_size"] = 0
        metrics["queue_processing"] = False
    
    # Check agent status files for engagement
    agent_workspaces = project_root / "agent_workspaces"
    active_agents = 0
    total_agents = 0
    
    if agent_workspaces.exists():
        for agent_dir in agent_workspaces.iterdir():
            if agent_dir.is_dir() and agent_dir.name.startswith("Agent-"):
                total_agents += 1
                status_file = agent_dir / "status.json"
                if status_file.exists():
                    try:
                        with open(status_file, 'r', encoding='utf-8') as f:
                            status = json.load(f)
                            if status.get("status") == "ACTIVE_AGENT_MODE":
                                active_agents += 1
                    except Exception:
                        pass
    
    metrics["active_agents"] = active_agents
    metrics["total_agents"] = total_agents
    metrics["swarm_engagement"] = (
        (active_agents / total_agents * 100) if total_agents > 0 else 0
    )
    
    return metrics

def display_coordination_metrics(metrics: Dict[str, Any]):
    """Display coordination metrics."""
    print("\n" + "=" * 80)
    print("COORDINATION METRICS")
    print("=" * 80)
    
    print(f"\n📊 Message Queue Status:")
    print("-" * 80)
    print(f"   Queue Size: {metrics.get('queue_size', 0)}")
    print(f"   Processing: {'✅ Active' if metrics.get('queue_processing') else '⏸️  Idle'}")
    
    print(f"\n📊 Swarm Engagement:")
    print("-" * 80)
    print(f"   Active Agents: {metrics.get('active_agents', 0)}/{metrics.get('total_agents', 0)}")
    print(f"   Engagement Rate: {metrics.get('swarm_engagement', 0):.1f}%")
    
    print(f"\n📊 Metrics Collection:")
    print("-" * 80)
    print(f"   Timestamp: {metrics.get('timestamp', 'N/A')}")
    print(f"   Status: ✅ Metrics collected successfully")

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
    
    # Update metrics with health check results
    metrics = collect_coordination_metrics()
    metrics["message_queue_health"] = results["message_queue"]
    metrics["broadcast_system_health"] = results["broadcast_system"]
    metrics["coordination_tools_health"] = results["coordination_workflows"]
    
    # Display metrics
    display_coordination_metrics(metrics)
    
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

