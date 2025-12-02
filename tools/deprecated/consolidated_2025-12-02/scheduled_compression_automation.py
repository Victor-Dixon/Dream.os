#!/usr/bin/env python3
"""
Scheduled Message Compression Automation
========================================

Automated daily compression of message history.
Can be run as a scheduled task or cron job.

Author: Agent-3 (Infrastructure & DevOps) - JET FUEL AUTONOMOUS MODE
Created: 2025-01-27
Priority: CRITICAL
"""

import logging
import sys
from pathlib import Path

# Add tools directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from message_compression_automation import MessageCompressionAutomation
from message_compression_health_check import MessageCompressionHealthCheck

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def main():
    """Run scheduled compression automation."""
    logger.info("🚀 Starting scheduled message compression automation...")
    
    # Check health first
    health_check = MessageCompressionHealthCheck()
    health = health_check.check_compression_health()
    
    if health.get("status") == "error":
        logger.error(f"❌ Health check failed: {health.get('error')}")
        return 1
    
    # Run compression
    automation = MessageCompressionAutomation()
    stats = automation.run_automated_compression()
    
    if stats.get("error"):
        logger.error(f"❌ Compression failed: {stats.get('error')}")
        return 1
    
    logger.info(f"✅ Compression complete: {stats.get('compressed_count')} messages, {stats.get('compression_ratio')} reduction")
    
    # Verify health after compression
    health_after = health_check.check_compression_health()
    logger.info(f"📊 Post-compression status: {health_after.get('status')}")
    
    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        logger.info("👋 Compression automation interrupted")
        sys.exit(0)
    except Exception as e:
        logger.error(f"💥 Fatal error: {e}", exc_info=True)
        sys.exit(1)




