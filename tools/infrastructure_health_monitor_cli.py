#!/usr/bin/env python3
"""
Infrastructure Health Monitor CLI Tool
=====================================

CLI tool for monitoring infrastructure health metrics.
Provides quick health checks and detailed diagnostics.

Usage:
    python tools/infrastructure_health_monitor_cli.py --check
    python tools/infrastructure_health_monitor_cli.py --disk
    python tools/infrastructure_health_monitor_cli.py --memory

<!-- SSOT Domain: infrastructure -->
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.infrastructure.infrastructure_health_monitor import InfrastructureHealthMonitor


def main():
    """Main CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Infrastructure Health Monitor - Check system health for automation reliability",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tools/infrastructure_health_monitor_cli.py --check
  python tools/infrastructure_health_monitor_cli.py --disk
  python tools/infrastructure_health_monitor_cli.py --memory --cpu
  python tools/infrastructure_health_monitor_cli.py --browser
        """
    )

    parser.add_argument(
        "--check",
        action="store_true",
        help="Perform comprehensive health check (default)"
    )
    parser.add_argument(
        "--disk",
        action="store_true",
        help="Check disk space usage"
    )
    parser.add_argument(
        "--memory",
        action="store_true",
        help="Check memory usage"
    )
    parser.add_argument(
        "--cpu",
        action="store_true",
        help="Check CPU usage"
    )
    parser.add_argument(
        "--browser",
        action="store_true",
        help="Check browser automation readiness"
    )
    parser.add_argument(
        "--warning-threshold",
        type=float,
        default=85.0,
        help="Warning threshold percentage (default: 85%%)"
    )
    parser.add_argument(
        "--critical-threshold",
        type=float,
        default=95.0,
        help="Critical threshold percentage (default: 95%%)"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Quiet mode - only show status"
    )

    args = parser.parse_args()

    # If no specific checks requested, do full check
    if not any([args.disk, args.memory, args.cpu, args.browser]):
        args.check = True

    monitor = InfrastructureHealthMonitor(
        warning_threshold=args.warning_threshold,
        critical_threshold=args.critical_threshold
    )

    try:
        if args.check:
            result = monitor.perform_full_health_check()
            if args.quiet:
                print(f"Status: {result.status.upper()}")
                if result.status != "healthy":
                    print(f"Message: {result.message}")
                    if result.recommendations:
                        print("Recommendations:")
                        for rec in result.recommendations:
                            print(f"  {rec}")
            else:
                monitor.print_health_report(result)

        else:
            # Individual checks
            if args.disk:
                disk_info = monitor.check_disk_space()
                print("💾 DISK SPACE:")
                if "error" in disk_info:
                    print(f"  ❌ Error: {disk_info['error']}")
                else:
                    print(f"  Total: {disk_info['total_gb']} GB")
                    print(f"  Used: {disk_info['used_gb']} GB ({disk_info['usage_percent']}%)")
                    print(f"  Free: {disk_info['free_gb']} GB")
                    print(f"  Status: {disk_info['status'].upper()}")

            if args.memory:
                memory_info = monitor.check_memory_usage()
                print("🧠 MEMORY USAGE:")
                if "error" in memory_info:
                    print(f"  ❌ Error: {memory_info['error']}")
                else:
                    print(f"  Total: {memory_info['total_gb']} GB")
                    print(f"  Used: {memory_info['used_gb']} GB ({memory_info['usage_percent']}%)")
                    print(f"  Free: {memory_info['free_gb']} GB")
                    print(f"  Status: {memory_info['status'].upper()}")

            if args.cpu:
                cpu_info = monitor.check_cpu_usage()
                print("⚡ CPU USAGE:")
                if "error" in cpu_info:
                    print(f"  ❌ Error: {cpu_info['error']}")
                else:
                    print(f"  Usage: {cpu_info['usage_percent']}%")
                    print(f"  Status: {cpu_info['status'].upper()}")

            if args.browser:
                browser_info = monitor.check_browser_automation_readiness()
                print("🌐 BROWSER AUTOMATION:")
                if "error" in browser_info:
                    print(f"  ❌ Error: {browser_info['error']}")
                else:
                    print(f"  Browser Ready: {'✅ Yes' if browser_info['browser_ready'] else '❌ No'}")
                    print(f"  Chrome Available: {'✅ Yes' if browser_info['chrome_available'] else '❌ No'}")
                    print(f"  UC Driver Available: {'✅ Yes' if browser_info['uc_available'] else '❌ No'}")
                    print(f"  Selenium Available: {'✅ Yes' if browser_info['selenium_available'] else '❌ No'}")
                    if browser_info.get('issues'):
                        print("  Issues:")
                        for issue in browser_info['issues']:
                            print(f"    - {issue}")
                    print(f"  Status: {browser_info['status'].upper()}")

    except Exception as e:
        print(f"❌ Error running health check: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
