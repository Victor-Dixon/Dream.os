#!/usr/bin/env python3
"""
Run Email Campaigns
===================

Scheduled script to check and send email campaigns.

Usage: python trading_robot/email_campaigns/run_campaigns.py

V2 Compliance: <300 lines
Author: Agent-8 (SSOT & System Integration Specialist)
Date: 2025-12-20
"""

import sys
import logging
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from trading_robot.email_campaigns import EmailCampaignManager, EmailService

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    """Run email campaign check and send."""
    try:
        # Initialize email service (configure from environment)
        import os
        email_service = EmailService(
            smtp_host=os.getenv("SMTP_HOST", "smtp.gmail.com"),
            smtp_port=int(os.getenv("SMTP_PORT", "587")),
            smtp_user=os.getenv("SMTP_USER"),
            smtp_password=os.getenv("SMTP_PASSWORD"),
            from_email=os.getenv("FROM_EMAIL", "noreply@tradingrobotplug.com"),
            from_name="Trading Robot Team",
        )
        
        # Initialize database (if available)
        database = None
        try:
            # Import database connection
            from trading_robot.database import get_database_connection
            database = get_database_connection()
        except ImportError:
            logger.warning("Database not available - campaigns will not check history")
        
        # Initialize campaign manager
        campaign_manager = EmailCampaignManager(
            email_service=email_service,
            database=database,
        )
        
        # Check and send campaigns
        logger.info("Starting email campaign check...")
        sent_count = campaign_manager.check_and_send_campaigns()
        
        logger.info(f"Campaign check complete: {sent_count} emails sent")
        return 0 if sent_count >= 0 else 1
        
    except Exception as e:
        logger.error(f"Error running campaigns: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())

