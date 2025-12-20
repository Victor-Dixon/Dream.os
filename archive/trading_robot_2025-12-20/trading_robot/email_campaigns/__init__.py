"""
Trading Robot Email Campaigns
=============================

Email campaigns for subscription tier conversions:
- Free → Low Commitment ($9.99/month)
- Low → Mid-Tier ($29.99/month)
- Mid → Premium ($99.99/month)

Author: Agent-8 (SSOT & System Integration Specialist)
Date: 2025-12-20
"""

from .campaign_manager import EmailCampaignManager
from .campaign_templates import (
    FreeToLowCampaign,
    LowToMidCampaign,
    MidToPremiumCampaign,
)

__all__ = [
    "EmailCampaignManager",
    "FreeToLowCampaign",
    "LowToMidCampaign",
    "MidToPremiumCampaign",
]

