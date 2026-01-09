#!/usr/bin/env python3
"""
Repository Monitoring Startup Script - Phase 4
==============================================

Starts the continuous repository monitoring system.

<!-- SSOT Domain: monitoring -->

Usage:
    python scripts/start_repository_monitoring.py

This script will:
- Initialize the repository monitor
- Start continuous scanning
- Set up alert callbacks
- Provide status information

Navigation References:
├── Related Files:
│   ├── Monitor Service → src/services/repository_monitor.py
│   ├── FastAPI Integration → src/web/fastapi_app.py
│   └── Configuration → src/config/repository_monitor_config.json
├── Documentation:
│   ├── Phase 4 Roadmap → PHASE4_STRATEGIC_ROADMAP.md
│   ├── Setup Guide → docs/setup/repository_monitoring_setup.md
│   └── API Reference → docs/api/repository_monitor_api.md

Author: Agent-5 (Business Intelligence Specialist)
Date: 2026-01-08
Phase: Phase 4 Sprint 4 - Operational Transformation Engine
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from services.repository_monitor import (
    repository_monitor,
    start_repository_monitoring,
    stop_repository_monitoring,
    handle_repository_alert
)

logger = logging.getLogger(__name__)


async def setup_monitoring():
    """Set up and start repository monitoring."""
    try:
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        logger.info("🚀 Starting Repository Monitoring System...")

        # Add alert callback
        repository_monitor.add_alert_callback(handle_repository_alert)

        # Start monitoring
        await start_repository_monitoring()

        logger.info("✅ Repository monitoring system started successfully")
        logger.info(f"📊 Monitoring repository: {repository_monitor.repository_path}")
        logger.info(f"⏰ Scan interval: {repository_monitor.config['scan_interval_seconds']} seconds")
        logger.info(f"📈 Alert thresholds: Files/hour: {repository_monitor.alert_thresholds['max_files_growth_rate']}, "
                   f"MB/hour: {repository_monitor.alert_thresholds['max_size_growth_rate_mb']}")

        # Get initial stats
        stats = repository_monitor.get_current_stats()
        if not stats.get("error"):
            logger.info(f"📁 Initial repository stats: {stats['total_files']} files, "
                       f"{stats['total_size_mb']:.1f} MB")

        return True

    except Exception as e:
        logger.error(f"❌ Failed to start repository monitoring: {e}")
        return False


async def main():
    """Main function."""
    success = await setup_monitoring()

    if not success:
        sys.exit(1)

    # Keep running
    try:
        logger.info("🔄 Repository monitoring is running... Press Ctrl+C to stop")

        while True:
            await asyncio.sleep(60)  # Check every minute

            # Log status periodically
            stats = repository_monitor.get_current_stats()
            if not stats.get("error"):
                logger.info(f"📊 Status: {stats['total_files']} files, "
                          f"{stats['monitoring_active'] and '🟢' or '🔴'} monitoring")

    except KeyboardInterrupt:
        logger.info("🛑 Shutting down repository monitoring...")
        await stop_repository_monitoring()
        logger.info("✅ Repository monitoring stopped")

    except Exception as e:
        logger.error(f"❌ Error during monitoring: {e}")
        await stop_repository_monitoring()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())