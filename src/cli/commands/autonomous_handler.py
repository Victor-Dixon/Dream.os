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

                # Execute real autonomous operations
                self._execute_autonomous_operations(config)

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

    def _execute_autonomous_operations(self, config: Dict[str, Any]) -> None:
        """Execute real autonomous operations based on configuration."""
        import time
        import psutil
        import requests
        from pathlib import Path

        completed_operations = []
        start_time = datetime.now()

        print("\n🚀 Executing autonomous operations...")

        # Get configured services
        services = config.get('services', [])

        operations = []

        # Add service-specific operations
        if 'message_queue' in services:
            operations.extend([
                "Health check - Message Queue",
                "Message Queue cleanup",
                "Queue monitoring"
            ])

        if 'fastapi_service' in services:
            operations.extend([
                "Health check - FastAPI Service",
                "API endpoint validation",
                "Service performance check"
            ])

        # Add common operations
        operations.extend([
            "Log rotation",
            "Cache cleanup",
            "Resource usage analysis",
            "Disk space monitoring"
        ])

        for i, operation in enumerate(operations, 1):
            print(f"   {i}/{len(operations)}: {operation}...", end=' ')
            operation_start = time.time()

            try:
                result = self._execute_single_operation(operation, config)
                operation_duration = time.time() - operation_start

                if result['status'] == 'success':
                    print("✅")
                    completed_operations.append({
                        'operation': operation,
                        'status': 'success',
                        'duration': operation_duration,
                        'timestamp': datetime.now().isoformat(),
                        'details': result.get('details', {})
                    })
                else:
                    print("❌")
                    completed_operations.append({
                        'operation': operation,
                        'status': 'failed',
                        'error': result.get('error', 'Unknown error'),
                        'duration': operation_duration,
                        'timestamp': datetime.now().isoformat()
                    })

            except Exception as e:
                operation_duration = time.time() - operation_start
                print("❌")
                completed_operations.append({
                    'operation': operation,
                    'status': 'failed',
                    'error': str(e),
                    'duration': operation_duration,
                    'timestamp': datetime.now().isoformat()
                })

        # Generate report
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        successful_ops = len([op for op in completed_operations if op['status'] == 'success'])
        success_rate = (successful_ops / len(operations)) * 100 if operations else 0

        report = {
            'timestamp': start_time.isoformat(),
            'duration_seconds': duration,
            'operations': completed_operations,
            'success_rate': success_rate,
            'config': config,
            'system_info': {
                'cpu_percent': psutil.cpu_percent(interval=1),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_usage': psutil.disk_usage('/').percent
            }
        }

        # Save report
        report_filename = f"autonomous_report_{int(start_time.timestamp())}.json"
        report_path = self.reports_dir / report_filename

        try:
            with open(report_path, 'w') as f:
                json.dump(report, f, indent=2)

            print("\n📊 Autonomous operations completed!")
            print(f"   Duration: {duration:.1f} seconds")
            print(f"   Success Rate: {success_rate:.1f}%")
            print(f"   Report saved: {report_path}")

        except Exception as e:
            print(f"❌ Failed to save report: {e}")

    def _execute_single_operation(self, operation: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single autonomous operation."""
        import requests
        import psutil
        from pathlib import Path

        try:
            if operation == "Health check - Message Queue":
                # Check if message queue service is running
                try:
                    # Try to connect to message queue
                    from src.services.message_queue_service import MessageQueueService
                    mq = MessageQueueService()
                    health = mq.health_check()
                    return {
                        'status': 'success' if health else 'failed',
                        'details': {'queue_size': getattr(mq, 'queue_size', 0)}
                    }
                except Exception as e:
                    return {'status': 'failed', 'error': f'Message queue check failed: {e}'}

            elif operation == "Health check - FastAPI Service":
                # Check FastAPI service health
                try:
                    response = requests.get("http://localhost:8000/health", timeout=5)
                    return {
                        'status': 'success' if response.status_code == 200 else 'failed',
                        'details': {'status_code': response.status_code}
                    }
                except requests.exceptions.RequestException as e:
                    return {'status': 'failed', 'error': f'FastAPI health check failed: {e}'}

            elif operation == "Log rotation":
                # Rotate log files older than 7 days
                log_dir = Path("logs")
                if log_dir.exists():
                    rotated_count = 0
                    for log_file in log_dir.glob("*.log"):
                        if log_file.stat().st_mtime < (time.time() - 7*24*3600):
                            # Compress old log file
                            import gzip
                            with open(log_file, 'rb') as f_in:
                                with gzip.open(f"{log_file}.gz", 'wb') as f_out:
                                    f_out.writelines(f_in)
                            log_file.unlink()
                            rotated_count += 1

                    return {
                        'status': 'success',
                        'details': {'files_rotated': rotated_count}
                    }
                return {'status': 'success', 'details': {'files_rotated': 0}}

            elif operation == "Cache cleanup":
                # Clean up cache files
                cache_dirs = ["__pycache__", ".pytest_cache", ".cache"]
                cleaned_files = 0

                for cache_dir in cache_dirs:
                    for cache_path in Path(".").glob(f"**/{cache_dir}"):
                        if cache_path.is_dir():
                            import shutil
                            shutil.rmtree(cache_path)
                            cleaned_files += 1

                return {
                    'status': 'success',
                    'details': {'cache_dirs_removed': cleaned_files}
                }

            elif operation == "Resource usage analysis":
                # Analyze system resources
                cpu = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                disk = psutil.disk_usage('/')

                return {
                    'status': 'success',
                    'details': {
                        'cpu_percent': cpu,
                        'memory_percent': memory.percent,
                        'disk_percent': disk.percent
                    }
                }

            elif operation == "Disk space monitoring":
                # Check disk space
                disk = psutil.disk_usage('/')
                low_space = disk.percent > 90

                return {
                    'status': 'warning' if low_space else 'success',
                    'details': {
                        'disk_percent': disk.percent,
                        'free_gb': disk.free / (1024**3)
                    }
                }

            else:
                # Unknown operation
                return {'status': 'failed', 'error': f'Unknown operation: {operation}'}

        except Exception as e:
            return {'status': 'failed', 'error': str(e)}