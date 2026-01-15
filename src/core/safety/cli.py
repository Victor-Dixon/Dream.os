"""
Safety Foundation CLI
=====================


<!-- SSOT Domain: safety -->


Command-line interface for managing safety components.

Usage:
    python -m src.core.safety.cli <command> [options]

Commands:
    status           - Show status of all safety components
    kill-switch      - Manage kill switch
    sandbox          - Test sandbox execution
    blast-radius     - View blast radius usage
    audit            - Query audit trail
    snapshot         - Manage state snapshots

Author: Agent-4 (Captain) with Cloud Agent
License: MIT
"""

import sys
import argparse
import json
from typing import Optional
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.core.safety import (
    SafetySandbox,
    SandboxConfig,
    get_kill_switch,
    get_blast_radius_limiter,
    get_audit_trail,
    get_snapshot_manager,
    ResourceType,
    EventType
)


def cmd_status(args):
    """Show status of all safety components."""
    print("=" * 60)
    print("SAFETY FOUNDATION STATUS")
    print("=" * 60)
    
    # Kill Switch
    kill_switch = get_kill_switch()
    ks_status = kill_switch.get_status()
    print("\n🛑 Kill Switch:")
    print(f"  State: {ks_status['state']}")
    print(f"  Is Operational: {'✅' if ks_status['is_operational'] else '❌'}")
    print(f"  Active Operations: {ks_status['active_operations']}")
    print(f"  Total Triggers: {ks_status['trigger_count']}")
    
    # Blast Radius
    limiter = get_blast_radius_limiter()
    br_report = limiter.get_usage_report()
    print("\n💥 Blast Radius Limits:")
    for resource, data in br_report.items():
        print(f"  {resource.upper()}:")
        print(f"    Hourly: {data['usage']['hourly']:.1f} / {data['limits']['per_hour']:.1f} "
              f"({data['utilization']['hourly']:.1f}%)")
        print(f"    Daily: {data['usage']['daily']:.1f} / {data['limits']['per_day']:.1f} "
              f"({data['utilization']['daily']:.1f}%)")
    
    # Audit Trail
    audit = get_audit_trail()
    recent_events = audit.query_events(limit=10)
    print(f"\n📋 Audit Trail:")
    print(f"  Recent Events: {len(recent_events)}")
    print(f"  Integrity: {'✅ Valid' if audit.verify_integrity() else '❌ Failed'}")
    
    # Snapshots
    snapshots = get_snapshot_manager()
    all_snapshots = snapshots.list_snapshots()
    latest = snapshots.get_latest_snapshot()
    print(f"\n💾 State Snapshots:")
    print(f"  Total Snapshots: {len(all_snapshots)}")
    if latest:
        print(f"  Latest: {latest.snapshot_id} ({latest.timestamp})")
        print(f"  Size: {latest.size_bytes / (1024*1024):.1f} MB")
    
    print("\n" + "=" * 60)


def cmd_kill_switch(args):
    """Manage kill switch."""
    kill_switch = get_kill_switch()
    
    if args.trigger:
        # Trigger kill switch
        success = kill_switch.trigger(
            triggered_by=args.triggered_by or "CLI",
            trigger_channel="cli",
            reason=args.reason or "Manual trigger via CLI",
            graceful=not args.immediate
        )
        if success:
            print("✅ Kill switch triggered successfully")
        else:
            print("❌ Failed to trigger kill switch")
    
    elif args.arm:
        # Arm kill switch
        success = kill_switch.arm()
        if success:
            print("✅ Kill switch armed")
        else:
            print("❌ Failed to arm kill switch")
    
    elif args.disarm:
        # Disarm kill switch (dangerous!)
        code = args.authorization_code or input("Enter authorization code: ")
        success = kill_switch.disarm(code)
        if success:
            print("⚠️ Kill switch DISARMED")
        else:
            print("❌ Failed to disarm kill switch (invalid code)")
    
    else:
        # Show status
        status = kill_switch.get_status()
        print(json.dumps(status, indent=2))


def cmd_sandbox(args):
    """Test sandbox execution."""
    sandbox = SafetySandbox()
    
    code = args.code or input("Enter code to execute:\n")
    language = args.language or "python"
    
    print(f"\nExecuting in sandbox ({language})...")
    
    try:
        result = sandbox.execute_code(code, language)
        
        print("\n" + "=" * 60)
        print("EXECUTION RESULT")
        print("=" * 60)
        print(f"Success: {result.success}")
        print(f"Exit Code: {result.exit_code}")
        print(f"Execution Time: {result.execution_time_seconds:.2f}s")
        
        if result.stdout:
            print("\nStdout:")
            print(result.stdout)
        
        if result.stderr:
            print("\nStderr:")
            print(result.stderr)
        
        if result.violations:
            print("\nViolations:")
            for violation in result.violations:
                print(f"  - {violation}")
    
    except Exception as e:
        print(f"❌ Execution failed: {e}")


def cmd_blast_radius(args):
    """View blast radius usage."""
    limiter = get_blast_radius_limiter()
    
    if args.report:
        # Show usage report
        report = limiter.get_usage_report()
        print(json.dumps(report, indent=2))
    
    elif args.check:
        # Check if resource request is allowed
        try:
            resource_type = ResourceType[args.resource.upper()]
            limiter.check_limit(
                resource_type=resource_type,
                requested_amount=args.amount,
                action_id="cli_check"
            )
            print(f"✅ Request allowed: {args.amount} {args.resource}")
        except Exception as e:
            print(f"❌ Request denied: {e}")
    
    else:
        # Show remaining capacity
        print("Remaining Capacity:")
        for resource_type in ResourceType:
            hourly = limiter.get_remaining_capacity(resource_type, "hour")
            daily = limiter.get_remaining_capacity(resource_type, "day")
            print(f"  {resource_type.value}:")
            print(f"    Hourly: {hourly:.1f}")
            print(f"    Daily: {daily:.1f}")


def cmd_audit(args):
    """Query audit trail."""
    audit = get_audit_trail()
    
    if args.verify:
        # Verify integrity
        is_valid = audit.verify_integrity()
        if is_valid:
            print("✅ Audit trail integrity verified")
        else:
            print("❌ Audit trail integrity check FAILED")
    
    elif args.query:
        # Query events
        event_type = EventType[args.event_type.upper()] if args.event_type else None
        
        events = audit.query_events(
            agent_id=args.agent,
            event_type=event_type,
            start_time=args.start_time,
            end_time=args.end_time,
            limit=args.limit or 10
        )
        
        print(f"Found {len(events)} events:\n")
        for event in events:
            print(f"[{event['timestamp']}] {event['event_type']} - {event['agent_name']}")
            print(f"  {event['decision_summary']}")
            print(f"  Confidence: {event['confidence_score']:.2f} | Risk: {event['risk_level']}")
            print()
    
    else:
        # Show recent events
        events = audit.query_events(limit=10)
        print(f"Recent {len(events)} events:")
        for event in events:
            print(f"  [{event['timestamp']}] {event['event_type']}: {event['decision_summary']}")


def cmd_snapshot(args):
    """Manage state snapshots."""
    snapshots = get_snapshot_manager()
    
    if args.create:
        # Create snapshot
        snapshot_id = snapshots.create_snapshot(
            description=args.description or "Manual snapshot via CLI",
            tags={"source": "cli"}
        )
        if snapshot_id:
            print(f"✅ Snapshot created: {snapshot_id}")
        else:
            print("❌ Failed to create snapshot")
    
    elif args.restore:
        # Restore snapshot
        success = snapshots.restore_snapshot(args.snapshot_id)
        if success:
            print(f"✅ Restored from snapshot: {args.snapshot_id}")
        else:
            print(f"❌ Failed to restore snapshot: {args.snapshot_id}")
    
    elif args.list:
        # List snapshots
        all_snapshots = snapshots.list_snapshots()
        print(f"Available snapshots ({len(all_snapshots)}):\n")
        for snapshot in all_snapshots:
            print(f"{snapshot['snapshot_id']}")
            print(f"  Timestamp: {snapshot['timestamp']}")
            print(f"  Size: {snapshot['size_bytes'] / (1024*1024):.1f} MB")
            print(f"  Components: {', '.join(snapshot['components'].keys())}")
            print()
    
    else:
        # Show latest snapshot
        latest = snapshots.get_latest_snapshot()
        if latest:
            print(f"Latest snapshot: {latest.snapshot_id}")
            print(f"  Timestamp: {latest.timestamp}")
            print(f"  Size: {latest.size_bytes / (1024*1024):.1f} MB")
            print(f"  Components: {', '.join(latest.components.keys())}")
        else:
            print("No snapshots available")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Safety Foundation CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Show status
  python -m src.core.safety.cli status
  
  # Trigger kill switch
  python -m src.core.safety.cli kill-switch --trigger --reason "Testing"
  
  # Create snapshot
  python -m src.core.safety.cli snapshot --create --description "Before deployment"
  
  # Query audit trail
  python -m src.core.safety.cli audit --query --agent Agent-7 --limit 20
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Status command
    subparsers.add_parser('status', help='Show status of all safety components')
    
    # Kill switch command
    ks_parser = subparsers.add_parser('kill-switch', help='Manage kill switch')
    ks_parser.add_argument('--trigger', action='store_true', help='Trigger kill switch')
    ks_parser.add_argument('--arm', action='store_true', help='Arm kill switch')
    ks_parser.add_argument('--disarm', action='store_true', help='Disarm kill switch')
    ks_parser.add_argument('--reason', help='Reason for triggering')
    ks_parser.add_argument('--triggered-by', help='Who triggered')
    ks_parser.add_argument('--immediate', action='store_true', help='Immediate shutdown')
    ks_parser.add_argument('--authorization-code', help='Authorization code for disarm')
    
    # Sandbox command
    sb_parser = subparsers.add_parser('sandbox', help='Test sandbox execution')
    sb_parser.add_argument('--code', help='Code to execute')
    sb_parser.add_argument('--language', default='python', help='Language (python, bash)')
    
    # Blast radius command
    br_parser = subparsers.add_parser('blast-radius', help='View blast radius usage')
    br_parser.add_argument('--report', action='store_true', help='Show usage report')
    br_parser.add_argument('--check', action='store_true', help='Check if request allowed')
    br_parser.add_argument('--resource', help='Resource type (cost, files, api_calls)')
    br_parser.add_argument('--amount', type=float, help='Amount to check')
    
    # Audit command
    audit_parser = subparsers.add_parser('audit', help='Query audit trail')
    audit_parser.add_argument('--verify', action='store_true', help='Verify integrity')
    audit_parser.add_argument('--query', action='store_true', help='Query events')
    audit_parser.add_argument('--agent', help='Filter by agent ID')
    audit_parser.add_argument('--event-type', help='Filter by event type')
    audit_parser.add_argument('--start-time', help='Start time (ISO format)')
    audit_parser.add_argument('--end-time', help='End time (ISO format)')
    audit_parser.add_argument('--limit', type=int, help='Maximum results')
    
    # Snapshot command
    snap_parser = subparsers.add_parser('snapshot', help='Manage state snapshots')
    snap_parser.add_argument('--create', action='store_true', help='Create snapshot')
    snap_parser.add_argument('--restore', action='store_true', help='Restore snapshot')
    snap_parser.add_argument('--list', action='store_true', help='List snapshots')
    snap_parser.add_argument('--snapshot-id', help='Snapshot ID to restore')
    snap_parser.add_argument('--description', help='Snapshot description')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Execute command
    try:
        if args.command == 'status':
            cmd_status(args)
        elif args.command == 'kill-switch':
            cmd_kill_switch(args)
        elif args.command == 'sandbox':
            cmd_sandbox(args)
        elif args.command == 'blast-radius':
            cmd_blast_radius(args)
        elif args.command == 'audit':
            cmd_audit(args)
        elif args.command == 'snapshot':
            cmd_snapshot(args)
        else:
            print(f"Unknown command: {args.command}")
            sys.exit(1)
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
