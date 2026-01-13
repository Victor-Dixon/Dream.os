<<<<<<< HEAD
"""
Service Manager - Agent Cellphone V2
===================================

Manages the lifecycle of all critical services:
- Message Queue Processor
- Twitch Bot
- Discord Bot
- FastAPI Service

Features:
- Service status monitoring
- Individual service control
- Background process management
- Health checks and error handling

V2 Compliant: Yes (<300 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-07
"""

import os
import sys
import time
import signal
import psutil
import logging
from typing import Dict, List, Optional, Tuple
from pathlib import Path

logger = logging.getLogger(__name__)

class ServiceManager:
    """
    Manages the lifecycle and monitoring of all system services.
    """

    def __init__(self):
        self.services = {
            'messaging_v3': {
                'name': 'Messaging V3 Processor',
                'script': 'messaging_v3/processor.py',
                'pid_file': 'messaging_v3.pid',
                'log_file': 'messaging_v3.log',
                'status': 'stopped',
                'use_launcher': False
            },
            # Legacy messaging (deprecated - use messaging_v3)
            'message_queue': {
                'name': 'Legacy Message Queue (Deprecated)',
                'script': 'scripts/start_message_queue.py',
                'pid_file': 'message_queue.pid',
                'log_file': 'message_queue.log',
                'status': 'stopped',
                'use_launcher': False
            },
            'twitch': {
                'name': 'Twitch Bot',
                'script': 'scripts/start_twitch.py',
                'pid_file': 'twitch_bot.pid',
                'log_file': 'twitch_bot.log',
                'status': 'stopped',
                'use_launcher': False
            },
            'discord': {
                'name': 'Discord Bot',
                'script': 'src/discord_commander/unified_discord_bot.py',
                'pid_file': 'discord.pid',
                'log_file': 'discord_bot.log',
                'status': 'stopped',
                'use_launcher': True  # Launcher manages its own PID file
            },
            'fastapi': {
                'name': 'FastAPI Service',
                'script': 'scripts/start_fastapi.py',
                'pid_file': 'fastapi.pid',
                'log_file': 'fastapi.log',
                'status': 'stopped',
                'use_launcher': False
            }
        }
        self.pid_dir = Path('pids')
        self.log_dir = Path('logs')
        self._ensure_directories()

    def _ensure_directories(self):
        """Ensure PID and log directories exist."""
        self.pid_dir.mkdir(exist_ok=True)
        self.log_dir.mkdir(exist_ok=True)

    def _get_pid_file_path(self, service_name: str) -> Path:
        """Get the full path to a service's PID file."""
        return self.pid_dir / self.services[service_name]['pid_file']

    def _get_log_file_path(self, service_name: str) -> Path:
        """Get the full path to a service's log file."""
        return self.log_dir / self.services[service_name]['log_file']

    def _write_pid(self, service_name: str, pid: int):
        """Write PID to file."""
        pid_file = self._get_pid_file_path(service_name)
        pid_file.write_text(str(pid))

    def _read_pid(self, service_name: str) -> Optional[int]:
        """Read PID from file."""
        pid_file = self._get_pid_file_path(service_name)
        if pid_file.exists():
            try:
                return int(pid_file.read_text().strip())
            except (ValueError, OSError):
                return None
        return None

    def _remove_pid_file(self, service_name: str):
        """Remove PID file."""
        pid_file = self._get_pid_file_path(service_name)
        pid_file.unlink(missing_ok=True)

    def _is_process_running(self, pid: int) -> bool:
        """Check if a process is running."""
        try:
            process = psutil.Process(pid)
            return process.is_running()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return False

    def get_service_status(self, service_name: str) -> str:
        """Get the status of a specific service."""
        if service_name not in self.services:
            return 'unknown'

        pid = self._read_pid(service_name)
        if pid and self._is_process_running(pid):
            self.services[service_name]['status'] = 'running'
            return 'running'
        else:
            self.services[service_name]['status'] = 'stopped'
            return 'stopped'

    def get_all_status(self) -> Dict[str, str]:
        """Get status of all services."""
        return {name: self.get_service_status(name) for name in self.services}

    def start_service(self, service_name: str, background: bool = False) -> bool:
        """Start a specific service."""
        if service_name not in self.services:
            logger.error(f"Unknown service: {service_name}")
            return False

        # Check if already running
        if self.get_service_status(service_name) == 'running':
            logger.info(f"Service {service_name} is already running")
            return True

        service_config = self.services[service_name]
        script_path = service_config['script']
        log_file = self._get_log_file_path(service_name)
        use_launcher = service_config.get('use_launcher', False)

        try:
            if use_launcher:
                # Use launcher script - it manages its own PID file
                import subprocess
                logger.info(f"Starting {service_name} using launcher: {script_path}")
                cmd = [sys.executable, script_path]
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    cwd=os.getcwd()
                )
                if result.returncode == 0:
                    logger.info(f"Launcher started {service_name} successfully")
                    # Don't write PID - launcher does this
                    self.services[service_name]['status'] = 'running'
                    return True
                else:
                    logger.error(f"Launcher failed for {service_name}: {result.stderr}")
                    return False
            elif background:
                # Start in background with PID management
                import subprocess
                cmd = [sys.executable, script_path]
                process = subprocess.Popen(
                    cmd,
                    stdout=open(log_file, 'a'),
                    stderr=subprocess.STDOUT,
                    cwd=os.getcwd()
                )
                self._write_pid(service_name, process.pid)
                logger.info(f"Started {service_name} in background (PID: {process.pid})")
            else:
                # Start in foreground - import and run directly
                logger.info(f"Starting {service_name} in foreground")
                self._run_service_foreground(service_name)

            self.services[service_name]['status'] = 'running'
            return True

        except Exception as e:
            logger.error(f"Failed to start {service_name}: {e}")
            return False

    def _run_service_foreground(self, service_name: str):
        """Run a service in foreground mode."""
        # Import the service module dynamically
        if service_name == 'message_queue':
            from src.core.message_queue_processor.core.processor import main
            main()
        elif service_name == 'twitch':
            from src.services.chat_presence.twitch_eventsub_server import main
            main()
        elif service_name == 'discord':
            from src.discord_commander.unified_discord_bot import main
            main()
        elif service_name == 'fastapi':
            # Import from local FastAPI application
            try:
                from src.web.fastapi_app import app
                import uvicorn
                uvicorn.run(app, host="0.0.0.0", port=8001)
            except ImportError as e:
                logger.error(f"FastAPI service failed to import from local web module: {e}")
                logger.error("Ensure FastAPI components are properly configured")
                raise
        else:
            raise ValueError(f"Unknown service: {service_name}")

    def stop_service(self, service_name: str, force: bool = False) -> bool:
        """Stop a specific service."""
        if service_name not in self.services:
            logger.error(f"Unknown service: {service_name}")
            return False

        pid = self._read_pid(service_name)
        if not pid:
            logger.info(f"No PID file found for {service_name}")
            return True

        try:
            if self._is_process_running(pid):
                if force:
                    # Use taskkill on Windows
                    import subprocess
                    subprocess.run(['taskkill', '/PID', str(pid), '/F'], capture_output=True)
                    logger.info(f"Force killed {service_name} (PID: {pid})")
                else:
                    # Use taskkill for graceful termination
                    import subprocess
                    result = subprocess.run(['taskkill', '/PID', str(pid)], capture_output=True)
                    if result.returncode == 0:
                        logger.info(f"Gracefully stopped {service_name} (PID: {pid})")
                    else:
                        # If graceful termination failed, force kill
                        subprocess.run(['taskkill', '/PID', str(pid), '/F'], capture_output=True)
                        logger.info(f"Force killed {service_name} after graceful termination failed (PID: {pid})")
            else:
                logger.info(f"Service {service_name} was not running")

            self._remove_pid_file(service_name)
            self.services[service_name]['status'] = 'stopped'
            return True

        except (OSError, ProcessLookupError) as e:
            logger.error(f"Failed to stop {service_name}: {e}")
            self._remove_pid_file(service_name)
            return False

    def stop_all_services(self, force: bool = False) -> bool:
        """Stop all running services."""
        success = True
        for service_name in self.services:
            if not self.stop_service(service_name, force):
                success = False
        return success

    def start_all_services(self, background: bool = False) -> bool:
        """Start all services."""
        success = True
        for service_name in self.services:
            if not self.start_service(service_name, background):
                success = False
        return success

    def cleanup_logs(self, days: int = 7):
        """Clean up old log files."""
        import datetime

        cutoff = datetime.datetime.now() - datetime.timedelta(days=days)

        for log_file in self.log_dir.glob("*.log"):
            if log_file.stat().st_mtime < cutoff.timestamp():
                log_file.unlink()
                logger.info(f"Cleaned up old log file: {log_file}")

    def get_service_info(self, service_name: str) -> Optional[Dict]:
        """Get detailed information about a service."""
        if service_name not in self.services:
            return None

        status = self.get_service_status(service_name)
        pid = self._read_pid(service_name)

        info = self.services[service_name].copy()
        info.update({
            'current_status': status,
            'pid': pid,
            'log_file': str(self._get_log_file_path(service_name)),
            'pid_file': str(self._get_pid_file_path(service_name))
        })

=======
"""
Service Manager - Agent Cellphone V2
===================================

Manages the lifecycle of all critical services:
- Message Queue Processor
- Twitch Bot
- Discord Bot
- FastAPI Service

Features:
- Service status monitoring
- Individual service control
- Background process management
- Health checks and error handling

V2 Compliant: Yes (<300 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-07
"""

import os
import sys
import time
import signal
import psutil
import logging
from typing import Dict, List, Optional, Tuple
from pathlib import Path

logger = logging.getLogger(__name__)

class ServiceManager:
    """
    Manages the lifecycle and monitoring of all system services.
    """

    def __init__(self):
        self.services = {
            'message_queue': {
                'name': 'Message Queue Processor',
                'script': 'scripts/start_message_queue.py',
                'pid_file': 'message_queue.pid',
                'log_file': 'message_queue.log',
                'status': 'stopped',
                'use_launcher': False
            },
            'twitch': {
                'name': 'Twitch Bot',
                'script': 'scripts/start_twitch.py',
                'pid_file': 'twitch_bot.pid',
                'log_file': 'twitch_bot.log',
                'status': 'stopped',
                'use_launcher': False
            },
            'discord': {
                'name': 'Discord Bot',
                'script': 'tools/utilities/discord_bot_launcher.py',
                'pid_file': 'discord.pid',
                'log_file': 'discord_bot.log',
                'status': 'stopped',
                'use_launcher': True  # Launcher manages its own PID file
            },
            'fastapi': {
                'name': 'FastAPI Service',
                'script': 'scripts/start_fastapi.py',
                'pid_file': 'fastapi.pid',
                'log_file': 'fastapi.log',
                'status': 'stopped',
                'use_launcher': False
            }
        }
        self.pid_dir = Path('pids')
        self.log_dir = Path('logs')
        self._ensure_directories()

    def _ensure_directories(self):
        """Ensure PID and log directories exist."""
        self.pid_dir.mkdir(exist_ok=True)
        self.log_dir.mkdir(exist_ok=True)

    def _get_pid_file_path(self, service_name: str) -> Path:
        """Get the full path to a service's PID file."""
        return self.pid_dir / self.services[service_name]['pid_file']

    def _get_log_file_path(self, service_name: str) -> Path:
        """Get the full path to a service's log file."""
        return self.log_dir / self.services[service_name]['log_file']

    def _write_pid(self, service_name: str, pid: int):
        """Write PID to file."""
        pid_file = self._get_pid_file_path(service_name)
        pid_file.write_text(str(pid))

    def _read_pid(self, service_name: str) -> Optional[int]:
        """Read PID from file."""
        pid_file = self._get_pid_file_path(service_name)
        if pid_file.exists():
            try:
                return int(pid_file.read_text().strip())
            except (ValueError, OSError):
                return None
        return None

    def _remove_pid_file(self, service_name: str):
        """Remove PID file."""
        pid_file = self._get_pid_file_path(service_name)
        pid_file.unlink(missing_ok=True)

    def _is_process_running(self, pid: int) -> bool:
        """Check if a process is running."""
        try:
            process = psutil.Process(pid)
            return process.is_running()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return False

    def get_service_status(self, service_name: str) -> str:
        """Get the status of a specific service."""
        if service_name not in self.services:
            return 'unknown'

        pid = self._read_pid(service_name)
        if pid and self._is_process_running(pid):
            self.services[service_name]['status'] = 'running'
            return 'running'
        else:
            self.services[service_name]['status'] = 'stopped'
            return 'stopped'

    def get_all_status(self) -> Dict[str, str]:
        """Get status of all services."""
        return {name: self.get_service_status(name) for name in self.services}

    def start_service(self, service_name: str, background: bool = False) -> bool:
        """Start a specific service."""
        if service_name not in self.services:
            logger.error(f"Unknown service: {service_name}")
            return False

        # Check if already running
        if self.get_service_status(service_name) == 'running':
            logger.info(f"Service {service_name} is already running")
            return True

        service_config = self.services[service_name]
        script_path = service_config['script']
        log_file = self._get_log_file_path(service_name)
        use_launcher = service_config.get('use_launcher', False)

        try:
            if use_launcher:
                # Use launcher script - it manages its own PID file
                import subprocess
                logger.info(f"Starting {service_name} using launcher: {script_path}")
                cmd = [sys.executable, script_path]
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    cwd=os.getcwd()
                )
                if result.returncode == 0:
                    logger.info(f"Launcher started {service_name} successfully")
                    # Don't write PID - launcher does this
                    self.services[service_name]['status'] = 'running'
                    return True
                else:
                    logger.error(f"Launcher failed for {service_name}: {result.stderr}")
                    return False
            elif background:
                # Start in background with PID management
                import subprocess
                cmd = [sys.executable, script_path]
                process = subprocess.Popen(
                    cmd,
                    stdout=open(log_file, 'a'),
                    stderr=subprocess.STDOUT,
                    cwd=os.getcwd()
                )
                self._write_pid(service_name, process.pid)
                logger.info(f"Started {service_name} in background (PID: {process.pid})")
            else:
                # Start in foreground - import and run directly
                logger.info(f"Starting {service_name} in foreground")
                self._run_service_foreground(service_name)

            self.services[service_name]['status'] = 'running'
            return True

        except Exception as e:
            logger.error(f"Failed to start {service_name}: {e}")
            return False

    def _run_service_foreground(self, service_name: str):
        """Run a service in foreground mode."""
        # Import the service module dynamically
        if service_name == 'message_queue':
            from src.core.message_queue_processor.core.processor import main
            main()
        elif service_name == 'twitch':
            from src.services.chat_presence.twitch_eventsub_server import main
            main()
        elif service_name == 'discord':
            from src.discord_bot import main
            main()
        elif service_name == 'fastapi':
            # Import from local FastAPI application
            try:
                from src.web.fastapi_app import app
                import uvicorn
                uvicorn.run(app, host="0.0.0.0", port=8001)
            except ImportError as e:
                logger.error(f"FastAPI service failed to import from local web module: {e}")
                logger.error("Ensure FastAPI components are properly configured")
                raise
        else:
            raise ValueError(f"Unknown service: {service_name}")

    def stop_service(self, service_name: str, force: bool = False) -> bool:
        """Stop a specific service."""
        if service_name not in self.services:
            logger.error(f"Unknown service: {service_name}")
            return False

        pid = self._read_pid(service_name)
        if not pid:
            logger.info(f"No PID file found for {service_name}")
            return True

        try:
            if self._is_process_running(pid):
                if force:
                    # Use taskkill on Windows
                    import subprocess
                    subprocess.run(['taskkill', '/PID', str(pid), '/F'], capture_output=True)
                    logger.info(f"Force killed {service_name} (PID: {pid})")
                else:
                    # Use taskkill for graceful termination
                    import subprocess
                    result = subprocess.run(['taskkill', '/PID', str(pid)], capture_output=True)
                    if result.returncode == 0:
                        logger.info(f"Gracefully stopped {service_name} (PID: {pid})")
                    else:
                        # If graceful termination failed, force kill
                        subprocess.run(['taskkill', '/PID', str(pid), '/F'], capture_output=True)
                        logger.info(f"Force killed {service_name} after graceful termination failed (PID: {pid})")
            else:
                logger.info(f"Service {service_name} was not running")

            self._remove_pid_file(service_name)
            self.services[service_name]['status'] = 'stopped'
            return True

        except (OSError, ProcessLookupError) as e:
            logger.error(f"Failed to stop {service_name}: {e}")
            self._remove_pid_file(service_name)
            return False

    def stop_all_services(self, force: bool = False) -> bool:
        """Stop all running services."""
        success = True
        for service_name in self.services:
            if not self.stop_service(service_name, force):
                success = False
        return success

    def start_all_services(self, background: bool = False) -> bool:
        """Start all services."""
        success = True
        for service_name in self.services:
            if not self.start_service(service_name, background):
                success = False
        return success

    def cleanup_logs(self, days: int = 7):
        """Clean up old log files."""
        import datetime

        cutoff = datetime.datetime.now() - datetime.timedelta(days=days)

        for log_file in self.log_dir.glob("*.log"):
            if log_file.stat().st_mtime < cutoff.timestamp():
                log_file.unlink()
                logger.info(f"Cleaned up old log file: {log_file}")

    def get_service_info(self, service_name: str) -> Optional[Dict]:
        """Get detailed information about a service."""
        if service_name not in self.services:
            return None

        status = self.get_service_status(service_name)
        pid = self._read_pid(service_name)

        info = self.services[service_name].copy()
        info.update({
            'current_status': status,
            'pid': pid,
            'log_file': str(self._get_log_file_path(service_name)),
            'pid_file': str(self._get_pid_file_path(service_name))
        })

>>>>>>> rescue/dreamos-down-
        return info