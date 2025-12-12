#!/usr/bin/env python3
"""
Reinitialize Agent Status Monitor
==================================

Quick script to reinitialize and start the agent status monitoring system.
Resets monitor state and starts fresh monitoring cycle.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-12-12

<!-- SSOT Domain: infrastructure -->
"""

import sys
import asyncio
import logging
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def reinitialize_monitor():
    """Reinitialize and start the agent status monitor."""
    try:
        from src.orchestrators.overnight.monitor import ProgressMonitor
        
        logger.info("=" * 70)
        logger.info("🔄 REINITIALIZING AGENT STATUS MONITOR")
        logger.info("=" * 70)
        
        # Create new monitor instance
        monitor = ProgressMonitor()
        
        # Stop if already running
        if monitor.is_monitoring:
            logger.info("⚠️  Monitor already running - stopping first...")
            monitor.stop_monitoring()
        
        # Start fresh
        logger.info("🚀 Starting fresh monitoring cycle...")
        monitor.start_monitoring()
        
        logger.info("✅ Monitor reinitialized and started!")
        logger.info(f"   Status: {'ACTIVE' if monitor.is_monitoring else 'INACTIVE'}")
        logger.info(f"   Tracked agents: {len(monitor.agent_activity)}")
        logger.info(f"   Check interval: {monitor.check_interval}s")
        logger.info(f"   Stall timeout: {monitor.stall_timeout}s")
        logger.info("=" * 70)
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error reinitializing monitor: {e}", exc_info=True)
        return False


async def start_full_monitoring_system():
    """Start the full monitoring system (orchestrator + monitor)."""
    try:
        from src.orchestrators.overnight.orchestrator import OvernightOrchestrator
        
        logger.info("=" * 70)
        logger.info("🚀 STARTING FULL MONITORING SYSTEM")
        logger.info("=" * 70)
        logger.info("This includes:")
        logger.info("  ✅ Agent Status Monitor")
        logger.info("  ✅ Self-Healing System")
        logger.info("  ✅ Recovery System")
        logger.info("  ✅ Continuous autonomous operation")
        logger.info("=" * 70)
        
        orchestrator = OvernightOrchestrator()
        await orchestrator.start()
        
    except KeyboardInterrupt:
        logger.info("\n🛑 Shutting down...")
        if 'orchestrator' in locals():
            await orchestrator.stop()
        logger.info("✅ Shutdown complete")
    except Exception as e:
        logger.error(f"❌ Error: {e}", exc_info=True)
        return False


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Reinitialize agent status monitor",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Reinitialize monitor only (quick reset)
  python tools/reinitialize_status_monitor.py

  # Start full monitoring system (orchestrator + monitor)
  python tools/reinitialize_status_monitor.py --full

  # Just reset monitor state without starting
  python tools/reinitialize_status_monitor.py --reset-only
        """
    )
    
    parser.add_argument(
        "--full", "-f",
        action="store_true",
        help="Start full monitoring system (orchestrator + monitor)"
    )
    
    parser.add_argument(
        "--reset-only", "-r",
        action="store_true",
        help="Reset monitor state only (don't start)"
    )
    
    args = parser.parse_args()
    
    if args.full:
        # Start full system
        try:
            asyncio.run(start_full_monitoring_system())
        except KeyboardInterrupt:
            logger.info("\n⚠️ Interrupted by user")
            sys.exit(0)
    elif args.reset_only:
        # Just reset state
        logger.info("🔄 Resetting monitor state...")
        try:
            from src.orchestrators.overnight.monitor import ProgressMonitor
            monitor = ProgressMonitor()
            if monitor.is_monitoring:
                monitor.stop_monitoring()
            logger.info("✅ Monitor state reset")
        except Exception as e:
            logger.error(f"❌ Error: {e}")
            sys.exit(1)
    else:
        # Reinitialize and start
        success = asyncio.run(reinitialize_monitor())
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

