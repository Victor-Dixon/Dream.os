#!/usr/bin/env python3
"""
Phase 5 Infrastructure Automation Tool
Automated operations for enterprise infrastructure management
"""

import os
import json
import subprocess
import shutil
import tarfile
import gzip
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import logging
import argparse
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class AutomationTask:
    name: str
    description: str
    status: str
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    result: Optional[str] = None
    error: Optional[str] = None

class Phase5InfrastructureAutomation:
    def __init__(self):
        self.backup_dir = Path("backups")
        self.backup_dir.mkdir(exist_ok=True)
        self.tasks = []

    def run_docker_compose_command(self, command: str, service: Optional[str] = None) -> Tuple[bool, str]:
        """Execute docker-compose command safely"""
        try:
            cmd = ["docker-compose"]
            if service:
                cmd.extend([command, service])
            else:
                cmd.append(command)

            logger.info(f"Executing: {' '.join(cmd)}")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout
                cwd="."
            )

            success = result.returncode == 0
            output = result.stdout if success else result.stderr

            return success, output

        except subprocess.TimeoutExpired:
            return False, "Command timed out after 5 minutes"
        except Exception as e:
            return False, f"Command execution failed: {e}"

    def scale_service(self, service: str, replicas: int) -> AutomationTask:
        """Scale a Docker service to specified number of replicas"""
        task = AutomationTask(
            name=f"scale_{service}",
            description=f"Scale {service} to {replicas} replicas",
            status="RUNNING",
            start_time=datetime.now().isoformat()
        )

        try:
            success, output = self.run_docker_compose_command("up", f"--scale {service}={replicas} {service}")

            if success:
                task.status = "COMPLETED"
                task.result = f"Successfully scaled {service} to {replicas} replicas"
                logger.info(task.result)
            else:
                task.status = "FAILED"
                task.error = output
                logger.error(f"Failed to scale {service}: {output}")

        except Exception as e:
            task.status = "FAILED"
            task.error = str(e)
            logger.error(f"Scale operation failed: {e}")

        task.end_time = datetime.now().isoformat()
        return task

    def restart_service(self, service: str) -> AutomationTask:
        """Restart a specific service"""
        task = AutomationTask(
            name=f"restart_{service}",
            description=f"Restart {service} service",
            status="RUNNING",
            start_time=datetime.now().isoformat()
        )

        try:
            success, output = self.run_docker_compose_command("restart", service)

            if success:
                task.status = "COMPLETED"
                task.result = f"Successfully restarted {service}"
                logger.info(task.result)
            else:
                task.status = "FAILED"
                task.error = output
                logger.error(f"Failed to restart {service}: {output}")

        except Exception as e:
            task.status = "FAILED"
            task.error = str(e)
            logger.error(f"Restart operation failed: {e}")

        task.end_time = datetime.now().isoformat()
        return task

    def backup_database(self, database_type: str = "all") -> AutomationTask:
        """Create database backup"""
        task = AutomationTask(
            name=f"backup_{database_type}",
            description=f"Create {database_type} database backup",
            status="RUNNING",
            start_time=datetime.now().isoformat()
        )

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_files = []

        try:
            if database_type in ["postgres", "all"]:
                # PostgreSQL backup
                pg_backup_file = self.backup_dir / f"postgres_backup_{timestamp}.sql.gz"
                logger.info(f"Creating PostgreSQL backup: {pg_backup_file}")

                # Use pg_dump through docker
                dump_cmd = [
                    "docker", "exec", "postgres",
                    "pg_dump", "-U", "postgres", "-d", "tradingrobotplug"
                ]

                with gzip.open(pg_backup_file, 'wb') as f:
                    result = subprocess.run(
                        dump_cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        timeout=300
                    )

                    if result.returncode == 0:
                        f.write(result.stdout)
                        backup_files.append(str(pg_backup_file))
                        logger.info(f"PostgreSQL backup created: {pg_backup_file}")
                    else:
                        error_msg = result.stderr.decode()
                        logger.error(f"PostgreSQL backup failed: {error_msg}")
                        if database_type == "postgres":
                            task.status = "FAILED"
                            task.error = error_msg
                            task.end_time = datetime.now().isoformat()
                            return task

            if database_type in ["redis", "all"]:
                # Redis backup (RDB file)
                redis_backup_file = self.backup_dir / f"redis_backup_{timestamp}.rdb"
                logger.info(f"Creating Redis backup: {redis_backup_file}")

                # Copy Redis dump file
                redis_cmd = ["docker", "cp", "redis:/data/dump.rdb", str(redis_backup_file)]

                result = subprocess.run(
                    redis_cmd,
                    capture_output=True,
                    text=True,
                    timeout=60
                )

                if result.returncode == 0:
                    backup_files.append(str(redis_backup_file))
                    logger.info(f"Redis backup created: {redis_backup_file}")
                else:
                    error_msg = result.stderr
                    logger.error(f"Redis backup failed: {error_msg}")
                    if database_type == "redis":
                        task.status = "FAILED"
                        task.error = error_msg
                        task.end_time = datetime.now().isoformat()
                        return task

            # Create compressed archive of all backups
            if backup_files:
                archive_name = f"database_backup_{database_type}_{timestamp}.tar.gz"
                archive_path = self.backup_dir / archive_name

                with tarfile.open(archive_path, "w:gz") as tar:
                    for backup_file in backup_files:
                        tar.add(backup_file, arcname=os.path.basename(backup_file))

                # Clean up individual backup files
                for backup_file in backup_files:
                    os.remove(backup_file)

                task.status = "COMPLETED"
                task.result = f"Database backup completed: {archive_path} ({len(backup_files)} files)"
                logger.info(task.result)
            else:
                task.status = "FAILED"
                task.error = "No backup files were created"
                logger.error(task.error)

        except Exception as e:
            task.status = "FAILED"
            task.error = str(e)
            logger.error(f"Backup operation failed: {e}")

        task.end_time = datetime.now().isoformat()
        return task

    def cleanup_old_backups(self, days_to_keep: int = 7) -> AutomationTask:
        """Clean up old backup files"""
        task = AutomationTask(
            name="cleanup_backups",
            description=f"Remove backups older than {days_to_keep} days",
            status="RUNNING",
            start_time=datetime.now().isoformat()
        )

        try:
            cutoff_date = datetime.now() - timedelta(days=days_to_keep)
            removed_files = []
            total_size_freed = 0

            for backup_file in self.backup_dir.glob("*"):
                if backup_file.is_file() and backup_file.stat().st_mtime < cutoff_date.timestamp():
                    file_size = backup_file.stat().st_size
                    backup_file.unlink()
                    removed_files.append(backup_file.name)
                    total_size_freed += file_size

            task.status = "COMPLETED"
            task.result = f"Cleaned up {len(removed_files)} old backup files, freed {total_size_freed / (1024*1024):.1f} MB"
            logger.info(task.result)

        except Exception as e:
            task.status = "FAILED"
            task.error = str(e)
            logger.error(f"Cleanup operation failed: {e}")

        task.end_time = datetime.now().isoformat()
        return task

    def update_ssl_certificates(self) -> AutomationTask:
        """Update SSL certificates"""
        task = AutomationTask(
            name="update_ssl_certs",
            description="Update SSL certificates using automated script",
            status="RUNNING",
            start_time=datetime.now().isoformat()
        )

        try:
            # Run SSL configuration script
            ssl_script = Path("ssl/ssl-config.sh")
            if not ssl_script.exists():
                task.status = "FAILED"
                task.error = "SSL configuration script not found"
                logger.error(task.error)
            else:
                # Make script executable
                ssl_script.chmod(0o755)

                result = subprocess.run(
                    [str(ssl_script)],
                    capture_output=True,
                    text=True,
                    timeout=120
                )

                if result.returncode == 0:
                    task.status = "COMPLETED"
                    task.result = "SSL certificates updated successfully"
                    logger.info(task.result)

                    # Reload nginx to pick up new certificates
                    reload_success, reload_output = self.run_docker_compose_command("exec", "nginx nginx -s reload")
                    if reload_success:
                        task.result += " and nginx reloaded"
                    else:
                        logger.warning(f"Nginx reload failed: {reload_output}")

                else:
                    task.status = "FAILED"
                    task.error = result.stderr
                    logger.error(f"SSL update failed: {task.error}")

        except Exception as e:
            task.status = "FAILED"
            task.error = str(e)
            logger.error(f"SSL update operation failed: {e}")

        task.end_time = datetime.now().isoformat()
        return task

    def optimize_database_performance(self) -> AutomationTask:
        """Run database optimization tasks"""
        task = AutomationTask(
            name="optimize_databases",
            description="Optimize database performance and maintenance",
            status="RUNNING",
            start_time=datetime.now().isoformat()
        )

        try:
            optimizations = []

            # PostgreSQL optimizations
            pg_commands = [
                "VACUUM ANALYZE;",
                "REINDEX DATABASE tradingrobotplug;",
                "ANALYZE;"
            ]

            for cmd in pg_commands:
                result = subprocess.run([
                    "docker", "exec", "postgres",
                    "psql", "-U", "postgres", "-d", "tradingrobotplug", "-c", cmd
                ], capture_output=True, text=True, timeout=60)

                if result.returncode == 0:
                    optimizations.append(f"PostgreSQL: {cmd.strip()}")
                else:
                    logger.warning(f"PostgreSQL command failed: {cmd}")

            # Redis optimizations
            redis_result = subprocess.run([
                "docker", "exec", "redis", "redis-cli", "MEMORY", "PURGE"
            ], capture_output=True, text=True, timeout=30)

            if redis_result.returncode == 0:
                optimizations.append("Redis memory purge")
            else:
                logger.warning("Redis memory purge failed")

            if optimizations:
                task.status = "COMPLETED"
                task.result = f"Database optimizations completed: {', '.join(optimizations)}"
                logger.info(task.result)
            else:
                task.status = "WARNING"
                task.result = "No database optimizations were performed"
                logger.warning(task.result)

        except Exception as e:
            task.status = "FAILED"
            task.error = str(e)
            logger.error(f"Database optimization failed: {e}")

        task.end_time = datetime.now().isoformat()
        return task

    def health_check_all_services(self) -> AutomationTask:
        """Perform comprehensive health check of all services"""
        task = AutomationTask(
            name="health_check_all",
            description="Comprehensive health check of all infrastructure services",
            status="RUNNING",
            start_time=datetime.now().isoformat()
        )

        try:
            # Run health check tool
            result = subprocess.run([
                "python", "tools/phase5_health_check.py"
            ], capture_output=True, text=True, timeout=60)

            if result.returncode == 0:
                task.status = "COMPLETED"
                task.result = "All services passed health checks"
                logger.info(task.result)
            elif result.returncode == 2:  # Warnings
                task.status = "WARNING"
                task.result = "Health check completed with warnings"
                logger.warning(task.result)
            else:
                task.status = "FAILED"
                task.error = result.stdout or result.stderr
                logger.error(f"Health check failed: {task.error}")

        except Exception as e:
            task.status = "FAILED"
            task.error = str(e)
            logger.error(f"Health check operation failed: {e}")

        task.end_time = datetime.now().isoformat()
        return task

    def execute_automation_task(self, task_type: str, **kwargs) -> AutomationTask:
        """Execute automation task based on type"""
        if task_type == "scale":
            service = kwargs.get("service")
            replicas = kwargs.get("replicas", 1)
            if not service:
                return AutomationTask(
                    name="invalid_task",
                    description="Scale task requires 'service' parameter",
                    status="FAILED",
                    error="Missing service parameter"
                )
            return self.scale_service(service, replicas)

        elif task_type == "restart":
            service = kwargs.get("service")
            if not service:
                return AutomationTask(
                    name="invalid_task",
                    description="Restart task requires 'service' parameter",
                    status="FAILED",
                    error="Missing service parameter"
                )
            return self.restart_service(service)

        elif task_type == "backup":
            database_type = kwargs.get("database", "all")
            return self.backup_database(database_type)

        elif task_type == "cleanup":
            days = kwargs.get("days", 7)
            return self.cleanup_old_backups(days)

        elif task_type == "ssl_update":
            return self.update_ssl_certificates()

        elif task_type == "db_optimize":
            return self.optimize_database_performance()

        elif task_type == "health_check":
            return self.health_check_all_services()

        else:
            return AutomationTask(
                name="unknown_task",
                description=f"Unknown task type: {task_type}",
                status="FAILED",
                error=f"Unsupported task type: {task_type}"
            )

    def run_automation_pipeline(self, tasks_config: List[Dict]) -> List[AutomationTask]:
        """Run a series of automation tasks"""
        logger.info(f"🚀 Starting automation pipeline with {len(tasks_config)} tasks")

        results = []

        for task_config in tasks_config:
            task_type = task_config.get("type")
            task_name = task_config.get("name", f"task_{len(results) + 1}")

            logger.info(f"Executing task: {task_name} ({task_type})")

            task_result = self.execute_automation_task(task_type, **task_config.get("params", {}))
            task_result.name = task_name
            results.append(task_result)

            # Log task completion
            if task_result.status == "COMPLETED":
                logger.info(f"✅ {task_name}: {task_result.result}")
            elif task_result.status == "WARNING":
                logger.warning(f"⚠️  {task_name}: {task_result.result}")
            else:
                logger.error(f"❌ {task_name}: {task_result.error}")

        return results

    def print_automation_report(self, tasks: List[AutomationTask]):
        """Print automation execution report"""
        print("\n" + "="*100)
        print("🤖 PHASE 5 INFRASTRUCTURE AUTOMATION REPORT")
        print("="*100)

        completed_tasks = len([t for t in tasks if t.status == "COMPLETED"])
        warning_tasks = len([t for t in tasks if t.status == "WARNING"])
        failed_tasks = len([t for t in tasks if t.status == "FAILED"])

        print(f"📋 TASKS EXECUTED: {len(tasks)}")
        print(f"✅ COMPLETED: {completed_tasks}")
        print(f"⚠️  WARNINGS: {warning_tasks}")
        print(f"❌ FAILED: {failed_tasks}")

        print("\n" + "-"*100)
        print("📋 TASK DETAILS")
        print("-"*100)

        for task in tasks:
            status_emoji = "✅" if task.status == "COMPLETED" else "⚠️" if task.status == "WARNING" else "❌"
            duration = "N/A"
            if task.start_time and task.end_time:
                start = datetime.fromisoformat(task.start_time)
                end = datetime.fromisoformat(task.end_time)
                duration = f"{(end - start).total_seconds():.1f}s"

            print(f"{status_emoji} {task.name:<20} | {task.status:<9} | {duration:<8} | {task.description}")
            if task.result:
                print(f"   ✓ {task.result}")
            if task.error:
                print(f"   ✗ {task.error}")

        print("\n" + "="*100)

    def save_automation_report(self, tasks: List[AutomationTask], filename: str = None):
        """Save automation report to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"phase5_automation_report_{timestamp}.json"

        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_tasks": len(tasks),
                "completed_tasks": len([t for t in tasks if t.status == "COMPLETED"]),
                "warning_tasks": len([t for t in tasks if t.status == "WARNING"]),
                "failed_tasks": len([t for t in tasks if t.status == "FAILED"])
            },
            "tasks": [asdict(task) for task in tasks]
        }

        with open(filename, 'w') as f:
            json.dump(report, f, indent=2, default=str)

        logger.info(f"📄 Automation report saved to: {filename}")

def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description='Phase 5 Infrastructure Automation Tool')
    parser.add_argument('action', choices=[
        'scale', 'restart', 'backup', 'cleanup', 'ssl-update',
        'db-optimize', 'health-check', 'pipeline'
    ], help='Automation action to perform')
    parser.add_argument('--service', help='Service name for scale/restart actions')
    parser.add_argument('--replicas', type=int, default=1, help='Number of replicas for scaling')
    parser.add_argument('--database', choices=['postgres', 'redis', 'all'], default='all', help='Database type for backup')
    parser.add_argument('--days', type=int, default=7, help='Days to keep backups for cleanup')
    parser.add_argument('--pipeline-file', help='JSON file containing automation pipeline')
    parser.add_argument('--output', type=str, help='Output filename for report')

    args = parser.parse_args()

    automation = Phase5InfrastructureAutomation()

    try:
        if args.action == 'pipeline':
            if not args.pipeline_file:
                logger.error("Pipeline action requires --pipeline-file")
                sys.exit(1)

            with open(args.pipeline_file, 'r') as f:
                pipeline_config = json.load(f)

            tasks = automation.run_automation_pipeline(pipeline_config)
            automation.print_automation_report(tasks)
            automation.save_automation_report(tasks, args.output)

        else:
            # Single action
            params = {}
            if args.action == 'scale':
                if not args.service:
                    logger.error("Scale action requires --service")
                    sys.exit(1)
                params = {'service': args.service, 'replicas': args.replicas}
            elif args.action == 'restart':
                if not args.service:
                    logger.error("Restart action requires --service")
                    sys.exit(1)
                params = {'service': args.service}
            elif args.action == 'backup':
                params = {'database': args.database}
            elif args.action == 'cleanup':
                params = {'days': args.days}

            task = automation.execute_automation_task(args.action.replace('-', '_'), **params)
            automation.print_automation_report([task])
            automation.save_automation_report([task], args.output)

    except Exception as e:
        logger.error(f"Automation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()