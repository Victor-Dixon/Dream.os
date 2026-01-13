"""
Autonomous Operations Handler - V2 Compliant (<400 lines)
Handles autonomous mode operations and reporting.
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List
from pathlib import Path


class AutonomousHandler:
    """Handles autonomous operations and reporting."""

    def __init__(self):
        self.reports_dir = Path('reports/autonomous')
        self.config_file = Path('config/autonomous_config.json')
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def handle_reports_command(self) -> None:
        """Handle autonomous reports command."""
        print("📊 dream.os - Autonomous Reports")
        print("=" * 35)

        if not self.reports_dir.exists():
            print("❌ No autonomous reports directory found.")
            print("💡 Run autonomous operations first to generate reports.")
            return

        reports = list(self.reports_dir.glob('*.json'))
        if not reports:
            print("❌ No autonomous reports found.")
            print("💡 Run autonomous operations first to generate reports.")
            return

        # Sort reports by timestamp (newest first)
        reports.sort(key=lambda x: x.stat().st_mtime, reverse=True)

        print(f"Found {len(reports)} autonomous report(s):")
        print()

        for i, report_file in enumerate(reports[:10], 1):  # Show last 10 reports
            try:
                with open(report_file, 'r') as f:
                    report_data = json.load(f)

                timestamp = report_data.get('timestamp', 'Unknown')
                operations = len(report_data.get('operations', []))
                success_rate = report_data.get('success_rate', 0)

                status_icon = "✅" if success_rate >= 80 else "⚠️" if success_rate >= 50 else "❌"

                print(f"{i}. {status_icon} {report_file.name}")
                print(f"   Timestamp: {timestamp}")
                print(f"   Operations: {operations}")
                print(f"   Success Rate: {success_rate:.1f}%")
            except Exception as e:
                print(f"{i}. ❌ {report_file.name} (Error reading: {e})")

        if len(reports) > 10:
            print(f"\n... and {len(reports) - 10} older reports")

        print("\n💡 View full report: python main.py --autonomous-reports <filename>")

    def handle_run_autonomous_config_command(self) -> None:
        """Handle run autonomous config command."""
        print("🤖 dream.os - Autonomous Configuration")
        print("=" * 40)

        if not self.config_file.exists():
            print("❌ No autonomous configuration file found.")
            print("💡 Create config/autonomous_config.json first.")
            self._create_default_config()
            return

        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)

            print("Loaded autonomous configuration:")
            print(f"   Mode: {config.get('mode', 'Unknown')}")
            print(f"   Services: {', '.join(config.get('services', []))}")
            print(f"   Schedule: {config.get('schedule', 'Not set')}")
            print(f"   Monitoring: {config.get('monitoring', 'Disabled')}")

            # Validate configuration
            is_valid, errors = self._validate_config(config)

            if is_valid:
                print("\n✅ Configuration is valid!")
                print("🚀 Starting autonomous operations...")

                # Here you would start the autonomous operations
                # For now, just simulate
                self._simulate_autonomous_operations(config)

            else:
                print("\n❌ Configuration validation failed:")
                for error in errors:
                    print(f"   • {error}")

        except Exception as e:
            print(f"❌ Error loading configuration: {e}")

    def _create_default_config(self) -> None:
        """Create a default autonomous configuration file."""
        default_config = {
            "mode": "supervised",
            "services": ["message_queue", "fastapi_service"],
            "schedule": "daily",
            "monitoring": True,
            "health_checks": True,
            "auto_recovery": False,
            "notification_channels": ["console"],
            "log_level": "INFO"
        }

        self.config_file.parent.mkdir(parents=True, exist_ok=True)

        try:
            with open(self.config_file, 'w') as f:
                json.dump(default_config, f, indent=2)

            print(f"✅ Created default configuration: {self.config_file}")
            print("💡 Edit this file to customize autonomous behavior.")

        except Exception as e:
            print(f"❌ Failed to create default configuration: {e}")

    def _validate_config(self, config: Dict[str, Any]) -> tuple[bool, List[str]]:
        """Validate autonomous configuration."""
        errors = []

        required_fields = ['mode', 'services']
        for field in required_fields:
            if field not in config:
                errors.append(f"Missing required field: {field}")

        if 'mode' in config:
            valid_modes = ['supervised', 'semi_autonomous', 'full_autonomous']
            if config['mode'] not in valid_modes:
                errors.append(f"Invalid mode: {config['mode']}. Must be one of: {', '.join(valid_modes)}")

        if 'services' in config:
            if not isinstance(config['services'], list):
                errors.append("Services must be a list")
            elif not config['services']:
                errors.append("At least one service must be specified")

        return len(errors) == 0, errors

    def _simulate_autonomous_operations(self, config: Dict[str, Any]) -> None:
        """Simulate autonomous operations (placeholder for actual implementation)."""
        import time
        import random

        operations = [
            "Health check - Message Queue",
            "Health check - FastAPI Service",
            "Log rotation",
            "Cache cleanup",
            "Performance monitoring",
            "Resource usage analysis"
        ]

        completed_operations = []
        start_time = datetime.now()

        print("\n🚀 Executing autonomous operations...")
        for i, operation in enumerate(operations, 1):
            print(f"   {i}/{len(operations)}: {operation}...", end=' ')

            # Simulate operation time
            time.sleep(random.uniform(0.5, 2.0))

            # Simulate success/failure
            success = random.random() > 0.1  # 90% success rate

            if success:
                print("✅")
                completed_operations.append({
                    'operation': operation,
                    'status': 'success',
                    'timestamp': datetime.now().isoformat()
                })
            else:
                print("❌")
                completed_operations.append({
                    'operation': operation,
                    'status': 'failed',
                    'error': 'Simulated failure',
                    'timestamp': datetime.now().isoformat()
                })

        # Generate report
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        successful_ops = len([op for op in completed_operations if op['status'] == 'success'])
        success_rate = (successful_ops / len(operations)) * 100

        report = {
            'timestamp': start_time.isoformat(),
            'duration_seconds': duration,
            'operations': completed_operations,
            'success_rate': success_rate,
            'config': config
        }

        # Save report
        report_filename = f"autonomous_report_{int(start_time.timestamp())}.json"
        report_path = self.reports_dir / report_filename

        try:
            with open(report_path, 'w') as f:
                json.dump(report, f, indent=2)

            print("\n📊 Autonomous operations completed!")
            print(f"   Duration: {duration:.1f} seconds")
            print(f"   Report saved: {report_path}")

        except Exception as e:
            print(f"❌ Failed to save report: {e}")