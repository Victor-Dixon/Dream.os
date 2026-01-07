#!/usr/bin/env python3
"""
Web Server Launcher - Infrastructure Block 3
==========================================

Starts the Flask web application with monitoring and infrastructure services.

Features:
- Flask application server
- Health checks
- Monitoring integration
- GA4/Pixel configuration
- Infrastructure monitoring

Usage:
    python scripts/start_web_server.py          # Start server (foreground)
    python scripts/start_web_server.py --background  # Start in background

V2 Compliance: <300 lines
Author: Agent-3 (Infrastructure & DevOps Specialist)
"""

import os
import sys
import time
import signal
import logging
import subprocess
from pathlib import Path
from typing import Optional

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s'
)
logger = logging.getLogger(__name__)

# Import Flask app
try:
    from src.web import create_app
    from src.infrastructure.fastapi_monitoring import FastAPIMonitoring, create_monitoring_middleware
    from src.core.health_check import check_system_health
except ImportError as e:
    logger.error(f"Failed to import required modules: {e}")
    sys.exit(1)


class WebServerLauncher:
    """Web server launcher with infrastructure integration."""

    def __init__(self, background: bool = False):
        self.background = background
        self.project_root = project_root
        self.process: Optional[subprocess.Popen] = None
        self.monitoring = FastAPIMonitoring()
        self.analytics = None  # Will be initialized in create_flask_app

        # Server configuration
        self.host = os.getenv('WEB_HOST', '0.0.0.0')
        self.port = int(os.getenv('WEB_PORT', '8000'))
        self.debug = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'

    def create_flask_app(self):
        """Create and configure Flask application."""
        app = create_app()

        # Add monitoring via Flask before_request/after_request
        @app.before_request
        def start_request_monitoring():
            import time
            from flask import request, g
            g.start_time = time.time()
            g.request_path = request.path

        @app.after_request
        def end_request_monitoring(response):
            import time
            from flask import g
            if hasattr(g, 'start_time'):
                duration = time.time() - g.start_time
                status_code = response.status_code

                # Alert on slow responses
                self.monitoring.alert_slow_response(
                    endpoint=g.request_path,
                    duration=duration
                )

                # Record errors for high error rate detection
                if status_code >= 500:
                    self.monitoring.record_error()

            return response

        # Initialize analytics service
        try:
            from src.infrastructure.analytics_service import get_analytics_service, track_infrastructure_deployment
            self.analytics = get_analytics_service()
            logger.info("✅ Analytics service initialized")
        except ImportError as e:
            logger.warning(f"Analytics service not available: {e}")
            self.analytics = None

        # Add health check endpoint
        @app.route('/health')
        def health_check():
            """Health check endpoint."""
            try:
                health_data = check_system_health()
                status_code = 200 if health_data.get('overall_status') == 'healthy' else 503
                return health_data, status_code
            except Exception as e:
                return {'error': str(e), 'status': 'unhealthy'}, 503

        # Add GA4/Pixel configuration endpoint
        @app.route('/api/config/analytics')
        def get_analytics_config():
            """Get GA4/Pixel configuration."""
            if self.analytics:
                return {'config': self.analytics.get_analytics_config()}
            else:
                # Fallback to environment variables
                config = {
                    'ga4_measurement_id': os.getenv('GA4_MEASUREMENT_ID', ''),
                    'pixel_id': os.getenv('FACEBOOK_PIXEL_ID', ''),
                    'analytics_enabled': bool(os.getenv('GA4_MEASUREMENT_ID', '')),
                    'pixel_enabled': bool(os.getenv('FACEBOOK_PIXEL_ID', ''))
                }
                return {'config': config}

        # Add deployment tracking endpoint
        @app.route('/api/analytics/track/<event_name>', methods=['POST'])
        def track_analytics_event(event_name):
            """Track analytics event."""
            from flask import request

            if not self.analytics:
                return {'error': 'Analytics service not available'}, 503

            data = request.get_json() or {}
            success = self.analytics.track_event(event_name, data)

            if success:
                return {'status': 'tracked', 'event': event_name}
            else:
                return {'error': 'Tracking failed'}, 500

        return app

    def start_server(self):
        """Start the web server."""
        logger.info("🚀 Starting Infrastructure Block 3 - Web Services")
        logger.info(f"📍 Host: {self.host}:{self.port}")
        logger.info(f"🔧 Debug Mode: {self.debug}")
        logger.info(f"📊 Background Mode: {self.background}")

        # Track infrastructure deployment
        if self.analytics:
            self.analytics.track_infrastructure_event("web_server_starting", {
                "host": self.host,
                "port": self.port,
                "background_mode": self.background
            })

        try:
            app = self.create_flask_app()

            if self.background:
                # Start in background
                self.start_background_server(app)
            else:
                # Start in foreground
                logger.info("🌐 Starting Flask development server...")
                app.run(
                    host=self.host,
                    port=self.port,
                    debug=self.debug,
                    threaded=True
                )

        except Exception as e:
            logger.error(f"❌ Failed to start web server: {e}")
            sys.exit(1)

    def start_background_server(self, app):
        """Start server in background process."""
        try:
            # Create log file
            log_dir = self.project_root / "runtime" / "logs"
            log_dir.mkdir(parents=True, exist_ok=True)
            log_file = log_dir / "web_server.log"

            # Prepare environment
            env = os.environ.copy()
            env['PYTHONPATH'] = str(self.project_root)

            # Start process
            cmd = [
                sys.executable, __file__,  # Run this script without --background
            ]

            logger.info(f"📝 Starting background web server (logs: {log_file})")

            with open(log_file, 'a') as logfile:
                self.process = subprocess.Popen(
                    cmd,
                    cwd=str(self.project_root),
                    env=env,
                    stdout=logfile,
                    stderr=subprocess.STDOUT,
                    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
                )

            # Save PID
            pid_file = self.project_root / "pids" / "web_server.pid"
            pid_file.parent.mkdir(exist_ok=True)
            with open(pid_file, 'w') as f:
                f.write(str(self.process.pid))

            logger.info(f"✅ Web server started in background (PID: {self.process.pid})")
            logger.info("🩺 Health check endpoint: http://localhost:8000/health")
            logger.info("📊 Analytics config: http://localhost:8000/api/config/analytics")

            # Wait a moment then check if process is still running
            time.sleep(2)
            if self.process.poll() is None:
                logger.info("✅ Web server process confirmed running")

            # Track successful deployment
            if self.analytics:
                self.analytics.track_infrastructure_event("web_server_deployed", {
                    "status": "running",
                    "pid": self.process.pid,
                    "infrastructure_block": 3
                })

                # Track coordination completion
                self.analytics.track_coordination_event("infrastructure_deployment", ["Agent-3", "Agent-2", "Agent-4"], {
                    "coordination_type": "bilateral_swarm",
                    "block": "Infrastructure Block 3",
                    "services_deployed": ["web_server", "monitoring", "analytics"]
                })
            else:
                logger.error(f"❌ Web server process exited immediately (code: {self.process.returncode})")

        except Exception as e:
            logger.error(f"❌ Failed to start background web server: {e}")
            sys.exit(1)

    def stop_server(self):
        """Stop the background web server."""
        pid_file = self.project_root / "pids" / "web_server.pid"

        if pid_file.exists():
            try:
                with open(pid_file, 'r') as f:
                    pid = int(f.read().strip())

                logger.info(f"🛑 Stopping web server (PID: {pid})")

                if os.name == 'nt':
                    # Windows
                    subprocess.run(['taskkill', '/PID', str(pid), '/F'], check=False)
                else:
                    # Unix/Linux
                    os.kill(pid, signal.SIGTERM)

                # Clean up PID file
                pid_file.unlink()
                logger.info("✅ Web server stopped")

            except Exception as e:
                logger.error(f"❌ Failed to stop web server: {e}")
        else:
            logger.warning("⚠️ No web server PID file found")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Web Server Launcher - Infrastructure Block 3")
    parser.add_argument('--background', action='store_true', help='Start server in background')
    parser.add_argument('--stop', action='store_true', help='Stop background server')
    parser.add_argument('--status', action='store_true', help='Check server status')

    args = parser.parse_args()

    launcher = WebServerLauncher(background=args.background)

    if args.stop:
        launcher.stop_server()
    elif args.status:
        # Check if server is running
        pid_file = project_root / "pids" / "web_server.pid"
        if pid_file.exists():
            try:
                with open(pid_file, 'r') as f:
                    pid = int(f.read().strip())
                print(f"✅ Web server running (PID: {pid})")
                print("🩺 Health check: http://localhost:8000/health")
            except:
                print("❌ Web server PID file corrupted")
        else:
            print("❌ Web server not running")
    else:
        launcher.start_server()


if __name__ == "__main__":
    main()