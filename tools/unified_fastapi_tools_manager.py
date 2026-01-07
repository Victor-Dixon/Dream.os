#!/usr/bin/env python3
"""
Unified FastAPI Tools Manager
=============================

Consolidates all FastAPI-related tools into a single unified management system.

PHASE 4 SERVICE CONSOLIDATION - FastAPI Tools Block 2
Reduces 15+ fragmented FastAPI tools → 1 unified manager

Author: Agent-1 (Integration & Core Systems)
Date: 2026-01-06

Consolidated Tools:
- Health monitoring (monitor_fastapi_*, check_fastapi_*)
- Deployment (deploy_fastapi_*, setup_fastapi_*)
- Validation (verify_fastapi_*, execute_fastapi_*)
- Testing (report_fastapi_*, run_fastapi_*)
- Configuration management
- Service lifecycle management

Usage:
    python tools/unified_fastapi_tools_manager.py <command> [options]

Commands:
    health      - Monitor health endpoints and service status
    deploy      - Deploy FastAPI applications to production
    validate    - Run validation pipelines and tests
    monitor     - Continuous monitoring and alerting
    setup       - Initial setup and configuration
    status      - Get comprehensive service status
    logs        - View and analyze service logs

Examples:
    # Check health and readiness
    python tools/unified_fastapi_tools_manager.py health check

    # Deploy to production
    python tools/unified_fastapi_tools_manager.py deploy production

    # Run validation pipeline
    python tools/unified_fastapi_tools_manager.py validate pipeline

    # Monitor service continuously
    python tools/unified_fastapi_tools_manager.py monitor service
"""

import sys
import time
import json
import argparse
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any

# Project configuration
PROJECT_ROOT = Path(__file__).parent.parent
DEFAULT_ENDPOINT = "http://localhost:8001"
SERVICE_NAME = "tradingrobotplug-fastapi"

# Import paths for deployment
sys.path.insert(0, str(PROJECT_ROOT / "ops" / "deployment"))


class UnifiedFastAPIToolsManager:
    """Unified manager for all FastAPI-related operations."""

    def __init__(self, endpoint: str = DEFAULT_ENDPOINT, service_name: str = SERVICE_NAME):
        self.endpoint = endpoint.rstrip('/')
        self.service_name = service_name
        self.health_url = f"{self.endpoint}/health"

    def check_health_endpoint(self) -> Tuple[bool, str]:
        """Check if FastAPI health endpoint is responding."""
        try:
            import requests
            response = requests.get(self.health_url, timeout=5)

            if response.status_code == 200:
                return True, f"Health endpoint responding (200)"
            else:
                return False, f"Health endpoint returned {response.status_code}"
        except requests.exceptions.ConnectionError:
            return False, "Connection refused - service may be starting"
        except requests.exceptions.Timeout:
            return False, "Connection timeout"
        except Exception as e:
            return False, f"Error: {str(e)}"

    def get_service_status(self) -> Dict[str, Any]:
        """Get comprehensive service status."""
        status = {
            "service_name": self.service_name,
            "endpoint": self.endpoint,
            "timestamp": datetime.now().isoformat(),
            "health": {},
            "processes": {},
            "deployment": {},
            "validation": {}
        }

        # Health check
        is_healthy, health_message = self.check_health_endpoint()
        status["health"] = {
            "status": "healthy" if is_healthy else "unhealthy",
            "message": health_message,
            "endpoint": self.health_url
        }

        # Process check (if on same system)
        try:
            import psutil
            fastapi_processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    cmdline = proc.info['cmdline']
                    if cmdline and any('fastapi' in str(arg).lower() for arg in cmdline):
                        fastapi_processes.append({
                            "pid": proc.info['pid'],
                            "name": proc.info['name'],
                            "cmdline": " ".join(cmdline)
                        })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            status["processes"] = {
                "count": len(fastapi_processes),
                "processes": fastapi_processes
            }
        except ImportError:
            status["processes"] = {"error": "psutil not available"}

        return status

    def monitor_health(self, interval: int = 10, max_wait_minutes: int = 30) -> bool:
        """Monitor health endpoint until available or timeout."""
        max_wait_seconds = max_wait_minutes * 60
        start_time = datetime.now()
        end_time = start_time + timedelta(seconds=max_wait_seconds)

        print("="*70)
        print("FASTAPI HEALTH MONITOR")
        print("="*70)
        print(f"Endpoint: {self.endpoint}")
        print(f"Health Check: {self.health_url}")
        print(f"Check interval: {interval} seconds")
        print(f"Max wait time: {max_wait_minutes} minutes")
        print()

        check_count = 0

        while datetime.now() < end_time:
            check_count += 1
            is_ready, message = self.check_health_endpoint()

            timestamp = datetime.now().strftime("%H:%M:%S")
            elapsed = (datetime.now() - start_time).total_seconds()

            if is_ready:
                print(f"✅ [{timestamp}] Health endpoint is RESPONDING! ({elapsed:.1f}s elapsed)")
                print(f"   {message}")
                return True
            else:
                print(f"⏳ [{timestamp}] Health endpoint not ready yet ({elapsed:.1f}s elapsed, check #{check_count})")
                print(f"   {message}")

                if check_count % 6 == 0:  # Every minute
                    remaining = (end_time - datetime.now()).total_seconds() / 60
                    print(f"   ⏱️  {remaining:.1f} minutes remaining")

            time.sleep(interval)

        print(f"❌ Timeout: Health endpoint not responding after {max_wait_minutes} minutes")
        return False

    def deploy_application(self, target: str = "production", dry_run: bool = False) -> bool:
        """Deploy FastAPI application to target environment."""
        print("🚀 FastAPI Application Deployment")
        print("="*50)
        print(f"Target: {target}")
        print(f"Dry Run: {dry_run}")
        print()

        # Import deployment dependencies
        try:
            from simple_wordpress_deployer import SimpleWordPressDeployer, load_site_configs
        except ImportError as e:
            print(f"❌ Missing deployment dependencies: {e}")
            return False

        # FastAPI backend path
        fastapi_backend_path = Path("D:/websites/TradingRobotPlugWeb/backend")
        if not fastapi_backend_path.exists():
            print(f"❌ FastAPI backend not found: {fastapi_backend_path}")
            return False

        print(f"✅ FastAPI backend found: {fastapi_backend_path}")

        # Deployment configuration
        site_key = "tradingrobotplug.com"
        remote_base = "backend"

        # Load site configs
        try:
            site_configs = load_site_configs()
            deployer = SimpleWordPressDeployer(site_key, site_configs)
        except Exception as e:
            print(f"❌ Failed to initialize deployer: {e}")
            return False

        # Connect to server
        if not deployer.connect():
            print("❌ Failed to connect to server")
            return False
        print(f"✅ Connected to {site_key}")

        # Files to deploy
        files_to_deploy = [
            # Main application
            ("api/fastapi_app.py", "api/fastapi_app.py"),
            ("api/__init__.py", "api/__init__.py"),
            ("api/dependencies.py", "api/dependencies.py"),
            ("api/auth.py", "api/auth.py"),

            # Routes
            ("api/routes/__init__.py", "api/routes/__init__.py"),
            ("api/routes/account.py", "api/routes/account.py"),
            ("api/routes/trades.py", "api/routes/trades.py"),
            ("api/routes/strategies.py", "api/routes/strategies.py"),
            ("api/routes/analytics.py", "api/routes/analytics.py"),

            # Models
            ("api/models/__init__.py", "api/models/__init__.py"),
            ("api/models/account.py", "api/models/account.py"),
            ("api/models/trade.py", "api/models/trade.py"),
            ("api/models/strategy.py", "api/models/strategy.py"),

            # Middleware
            ("api/middleware/__init__.py", "api/middleware/__init__.py"),
            ("api/middleware/rate_limit.py", "api/middleware/rate_limit.py"),

            # Core modules
            ("core/__init__.py", "core/__init__.py"),
            ("core/trading_engine_v2.py", "core/trading_engine_v2.py"),
            ("core/strategy_manager_v2.py", "core/strategy_manager_v2.py"),

            # Database
            ("database/__init__.py", "database/__init__.py"),
            ("database/connection.py", "database/connection.py"),
            ("database/models.py", "database/models.py"),

            # Configuration
            ("config/__init__.py", "config/__init__.py"),
            ("config/settings.py", "config/settings.py"),

            # Requirements
            ("requirements.txt", "requirements.txt"),
        ]

        deployed_count = 0
        failed_count = 0

        print(f"\n📦 Deploying {len(files_to_deploy)} files...")

        for local_rel_path, remote_rel_path in files_to_deploy:
            local_file = fastapi_backend_path / local_rel_path
            remote_path = f"{remote_base}/{remote_rel_path}"

            if not local_file.exists():
                print(f"⚠️  Local file not found: {local_file} (skipping)")
                continue

            if dry_run:
                print(f"📋 Would deploy: {local_rel_path} -> {remote_path}")
                deployed_count += 1
                continue

            print(f"📤 Deploying: {local_rel_path} -> {remote_path}")

            try:
                # Ensure remote directory exists
                remote_dir = '/'.join(remote_path.split('/')[:-1])
                if remote_dir:
                    deployer.execute_command(f"mkdir -p {remote_dir} 2>&1 || true")

                # Deploy file
                local_file_abs = local_file.resolve()
                full_remote = f"{remote_base}/{remote_rel_path}"
                success = deployer.deploy_file(local_file_abs, full_remote)

                if success:
                    deployed_count += 1
                    print("   ✅ Deployed successfully")
                else:
                    failed_count += 1
                    print("   ❌ Deployment failed")
            except Exception as e:
                print(f"   ❌ Error: {e}")
                failed_count += 1

        # Deploy systemd service
        systemd_service = fastapi_backend_path / "deployment" / "systemd" / f"{self.service_name}.service"
        if systemd_service.exists() and not dry_run:
            print("\n📤 Deploying systemd service file")
            try:
                remote_service_path = f"/tmp/{self.service_name}.service"
                if deployer.deploy_file(systemd_service, remote_service_path):
                    print(f"   ✅ Service file deployed to {remote_service_path}")
                    print(f"   📋 Manual step: sudo mv {remote_service_path} /etc/systemd/system/")
                    print("   📋 Manual step: sudo systemctl daemon-reload")
                    print(f"   📋 Manual step: sudo systemctl enable {self.service_name}")
                    print(f"   📋 Manual step: sudo systemctl start {self.service_name}")
            except Exception as e:
                print(f"   ⚠️  Service deployment error: {e}")

        # Summary
        print("\n📊 Deployment Summary:")
        print(f"   ✅ Deployed: {deployed_count} files")
        print(f"   ❌ Failed: {failed_count} files")

        success = deployed_count > 0 and failed_count == 0
        if success:
            print("\n✅ FastAPI deployment complete!")
            if not dry_run:
                print("\n📋 Next Steps:")
                print("   1. Configure virtual environment and dependencies")
                print("   2. Set up .env file from .env.example")
                print("   3. Initialize database if needed")
                print("   4. Start systemd service")
                print(f"   5. Verify health: curl {self.health_url}")

        return success

    def run_validation_pipeline(self) -> bool:
        """Run complete validation pipeline."""
        print("🔬 FastAPI Validation Pipeline")
        print("="*40)

        # Check if health endpoint is ready
        is_ready, message = self.check_health_endpoint()
        if not is_ready:
            print(f"❌ Health endpoint not ready: {message}")
            print("   Start service first or use 'health monitor' to wait")
            return False

        print("✅ Health endpoint responding")

        # Run validation tests
        test_script = PROJECT_ROOT / "tools" / "execute_fastapi_tests_immediate.py"
        if test_script.exists():
            print("\n🧪 Running validation tests...")
            try:
                result = subprocess.run(
                    [sys.executable, str(test_script)],
                    cwd=PROJECT_ROOT,
                    timeout=300  # 5 minute timeout
                )
                if result.returncode != 0:
                    print(f"⚠️  Tests completed with exit code: {result.returncode}")
                    return False
                print("✅ Validation tests passed")
            except subprocess.TimeoutExpired:
                print("❌ Validation tests timed out")
                return False
            except Exception as e:
                print(f"❌ Error running validation tests: {e}")
                return False

        # Generate coordination handoff
        handoff_script = PROJECT_ROOT / "tools" / "generate_coordination_handoff_message.py"
        if handoff_script.exists():
            print("\n📨 Generating coordination handoff...")
            try:
                result = subprocess.run(
                    [sys.executable, str(handoff_script)],
                    cwd=PROJECT_ROOT,
                    timeout=60
                )
                if result.returncode == 0:
                    print("✅ Coordination handoff generated")
                else:
                    print(f"⚠️  Handoff generation exit code: {result.returncode}")
            except Exception as e:
                print(f"⚠️  Error generating handoff: {e}")

        print("\n✅ Validation pipeline complete")
        return True

    def setup_service(self, environment: str = "development") -> bool:
        """Set up FastAPI service for given environment."""
        print(f"⚙️  FastAPI Service Setup - {environment.upper()}")
        print("="*50)

        # Check if backend exists
        backend_path = Path("D:/websites/TradingRobotPlugWeb/backend")
        if not backend_path.exists():
            print(f"❌ Backend path not found: {backend_path}")
            return False

        print(f"✅ Backend found: {backend_path}")

        # Check required files
        required_files = [
            "api/fastapi_app.py",
            "requirements.txt",
            "config/settings.py"
        ]

        missing_files = []
        for file_path in required_files:
            if not (backend_path / file_path).exists():
                missing_files.append(file_path)

        if missing_files:
            print(f"❌ Missing required files: {', '.join(missing_files)}")
            return False

        print("✅ All required files present")

        # Environment-specific setup
        if environment == "development":
            print("\n🛠️  Development environment setup:")
            print("   - Virtual environment: python -m venv venv")
            print("   - Activate: source venv/bin/activate")
            print("   - Install: pip install -r requirements.txt")
            print(f"   - Run: uvicorn api.fastapi_app:app --reload --host 0.0.0.0 --port 8001")
        elif environment == "production":
            print("\n🏭 Production environment setup:")
            print("   - Configure systemd service")
            print("   - Set up reverse proxy (nginx)")
            print("   - Configure environment variables")
            print("   - Enable SSL/TLS")

        print("\n✅ Service setup instructions provided")
        return True

    def get_logs(self, lines: int = 50, follow: bool = False) -> None:
        """Get service logs."""
        print("📋 FastAPI Service Logs")
        print("="*30)
        print(f"Service: {self.service_name}")
        print(f"Lines: {lines}")
        print(f"Follow: {follow}")
        print()

        # Try journalctl first (systemd)
        try:
            cmd = ["journalctl", "-u", self.service_name, "-n", str(lines)]
            if follow:
                cmd.append("-f")

            print(f"📋 Command: {' '.join(cmd)}")
            result = subprocess.run(cmd, timeout=30 if not follow else None)

        except FileNotFoundError:
            print("❌ journalctl not available (not a systemd system)")
        except subprocess.TimeoutExpired:
            pass  # Normal for follow mode
        except Exception as e:
            print(f"❌ Error getting systemd logs: {e}")

        # Try alternative log locations
        log_paths = [
            f"/var/log/{self.service_name}.log",
            "/var/log/fastapi.log",
            "/tmp/fastapi.log"
        ]

        for log_path in log_paths:
            if Path(log_path).exists():
                print(f"📋 Found log file: {log_path}")
                try:
                    cmd = ["tail", f"-{lines}", log_path]
                    if follow:
                        cmd.append("-f")
                    subprocess.run(cmd, timeout=30 if not follow else None)
                    return
                except Exception as e:
                    print(f"❌ Error reading {log_path}: {e}")

        print("❌ No log files found")
        print("   Service may not be running or logging to stdout")


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(
        description="Unified FastAPI Tools Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Check service health
  %(prog)s health check

  # Monitor health until available
  %(prog)s health monitor --max-wait 60

  # Deploy to production
  %(prog)s deploy production

  # Run validation pipeline
  %(prog)s validate pipeline

  # Get service status
  %(prog)s status

  # Setup development environment
  %(prog)s setup development

  # View recent logs
  %(prog)s logs --lines 100

  # Follow logs in real-time
  %(prog)s logs --follow
        """
    )

    parser.add_argument(
        "command",
        choices=["health", "deploy", "validate", "monitor", "setup", "status", "logs"],
        help="Command to execute"
    )

    parser.add_argument(
        "subcommand",
        nargs="?",
        help="Subcommand (depends on main command)"
    )

    # Global options
    parser.add_argument(
        "--endpoint",
        default=DEFAULT_ENDPOINT,
        help=f"FastAPI endpoint URL (default: {DEFAULT_ENDPOINT})"
    )

    parser.add_argument(
        "--service-name",
        default=SERVICE_NAME,
        help=f"Service name (default: {SERVICE_NAME})"
    )

    # Health command options
    health_group = parser.add_argument_group("health command options")
    health_group.add_argument(
        "--interval",
        type=int,
        default=10,
        help="Health check interval in seconds (default: 10)"
    )
    health_group.add_argument(
        "--max-wait",
        type=int,
        default=30,
        help="Maximum wait time in minutes (default: 30)"
    )

    # Deploy command options
    deploy_group = parser.add_argument_group("deploy command options")
    deploy_group.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be deployed without actually deploying"
    )

    # Logs command options
    logs_group = parser.add_argument_group("logs command options")
    logs_group.add_argument(
        "--lines",
        type=int,
        default=50,
        help="Number of log lines to show (default: 50)"
    )
    logs_group.add_argument(
        "--follow",
        action="store_true",
        help="Follow log output in real-time"
    )

    args = parser.parse_args()

    # Initialize manager
    manager = UnifiedFastAPIToolsManager(
        endpoint=args.endpoint,
        service_name=args.service_name
    )

    # Execute command
    try:
        if args.command == "health":
            if args.subcommand == "check":
                is_healthy, message = manager.check_health_endpoint()
                print(f"Health Status: {'✅ HEALTHY' if is_healthy else '❌ UNHEALTHY'}")
                print(f"Message: {message}")
                sys.exit(0 if is_healthy else 1)
            elif args.subcommand == "monitor":
                success = manager.monitor_health(
                    interval=args.interval,
                    max_wait_minutes=args.max_wait
                )
                sys.exit(0 if success else 1)
            else:
                print("❌ Invalid health subcommand. Use 'check' or 'monitor'")
                sys.exit(1)

        elif args.command == "deploy":
            target = args.subcommand or "production"
            success = manager.deploy_application(
                target=target,
                dry_run=args.dry_run
            )
            sys.exit(0 if success else 1)

        elif args.command == "validate":
            if args.subcommand == "pipeline":
                success = manager.run_validation_pipeline()
                sys.exit(0 if success else 1)
            else:
                print("❌ Invalid validate subcommand. Use 'pipeline'")
                sys.exit(1)

        elif args.command == "status":
            status = manager.get_service_status()
            print(json.dumps(status, indent=2, default=str))
            sys.exit(0)

        elif args.command == "setup":
            environment = args.subcommand or "development"
            success = manager.setup_service(environment=environment)
            sys.exit(0 if success else 1)

        elif args.command == "logs":
            manager.get_logs(lines=args.lines, follow=args.follow)
            sys.exit(0)

        else:
            print(f"❌ Unknown command: {args.command}")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled by user")
        sys.exit(130)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()