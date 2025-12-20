#!/usr/bin/env python3
"""
Email Campaign Manager
======================

Manages automated email campaign sending for subscription tier conversions.

V2 Compliance: <300 lines
Author: Agent-8 (SSOT & System Integration Specialist)
Date: 2025-12-20
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass

from .campaign_templates import (
    FreeToLowCampaign,
    LowToMidCampaign,
    MidToPremiumCampaign,
    EmailTemplate,
)

logger = logging.getLogger(__name__)


@dataclass
class CampaignTrigger:
    """Campaign trigger event."""
    user_id: int
    user_email: str
    user_name: str
    current_tier: str
    trigger_event: str
    trigger_date: datetime
    metadata: Dict


class EmailCampaignManager:
    """Manages email campaign sending and automation."""
    
    def __init__(self, email_service=None, database=None):
        """Initialize campaign manager."""
        self.email_service = email_service
        self.database = database
        self.campaigns = {
            "free_to_low": FreeToLowCampaign,
            "low_to_mid": LowToMidCampaign,
            "mid_to_premium": MidToPremiumCampaign,
        }
    
    def get_campaign_for_tier(self, from_tier: str, to_tier: str) -> Optional:
        """Get campaign class for tier conversion."""
        campaign_key = f"{from_tier}_to_{to_tier}"
        return self.campaigns.get(campaign_key)
    
    def process_trigger(self, trigger: CampaignTrigger) -> bool:
        """Process campaign trigger and send appropriate emails."""
        try:
            # Determine target tier
            target_tier = self._get_target_tier(trigger.current_tier)
            if not target_tier:
                logger.warning(f"No target tier for {trigger.current_tier}")
                return False
            
            # Get campaign
            campaign_class = self.get_campaign_for_tier(
                trigger.current_tier, target_tier
            )
            if not campaign_class:
                logger.warning(
                    f"No campaign found for {trigger.current_tier} → {target_tier}"
                )
                return False
            
            # Get templates for this trigger event
            templates = campaign_class.get_templates()
            matching_templates = [
                t for t in templates
                if t.trigger_event == trigger.trigger_event
            ]
            
            if not matching_templates:
                logger.warning(
                    f"No templates found for event: {trigger.trigger_event}"
                )
                return False
            
            # Send emails
            sent_count = 0
            for template in matching_templates:
                if self._should_send_email(trigger, template):
                    success = self._send_email(trigger, template, target_tier)
                    if success:
                        sent_count += 1
                        self._record_email_sent(trigger, template)
            
            logger.info(
                f"Sent {sent_count} emails for {trigger.trigger_event} "
                f"({trigger.user_id})"
            )
            return sent_count > 0
            
        except Exception as e:
            logger.error(f"Error processing trigger: {e}", exc_info=True)
            return False
    
    def _get_target_tier(self, current_tier: str) -> Optional[str]:
        """Get target tier for conversion."""
        tier_map = {
            "free": "low",
            "low": "mid",
            "mid": "premium",
        }
        return tier_map.get(current_tier.lower())
    
    def _should_send_email(
        self, trigger: CampaignTrigger, template: EmailTemplate
    ) -> bool:
        """Check if email should be sent (avoid duplicates)."""
        if not self.database:
            return True  # No database = always send
        
        try:
            # Check if email already sent for this trigger + template
            query = """
                SELECT COUNT(*) FROM email_campaign_log
                WHERE user_id = %s
                AND trigger_event = %s
                AND template_subject = %s
                AND sent_at > NOW() - INTERVAL '30 days'
            """
            result = self.database.execute_query(
                query,
                (trigger.user_id, trigger.trigger_event, template.subject)
            )
            return result[0][0] == 0 if result else True
        except Exception as e:
            logger.warning(f"Error checking email history: {e}")
            return True  # Default to sending if check fails
    
    def _send_email(
        self, trigger: CampaignTrigger, template: EmailTemplate, target_tier: str
    ) -> bool:
        """Send email using email service."""
        if not self.email_service:
            logger.warning("No email service configured")
            return False
        
        try:
            # Build email content
            upgrade_url = self._build_upgrade_url(trigger.user_id, target_tier)
            unsubscribe_url = self._build_unsubscribe_url(trigger.user_id)
            
            html_body = template.html_body.format(
                user_name=trigger.user_name,
                upgrade_url=upgrade_url,
                unsubscribe_url=unsubscribe_url,
            )
            text_body = template.text_body.format(
                user_name=trigger.user_name,
                upgrade_url=upgrade_url,
                unsubscribe_url=unsubscribe_url,
            )
            
            # Send email
            success = self.email_service.send_email(
                to_email=trigger.user_email,
                subject=template.subject,
                html_body=html_body,
                text_body=text_body,
            )
            
            if success:
                logger.info(
                    f"Email sent: {template.subject} to {trigger.user_email}"
                )
            
            return success
            
        except Exception as e:
            logger.error(f"Error sending email: {e}", exc_info=True)
            return False
    
    def _build_upgrade_url(self, user_id: int, target_tier: str) -> str:
        """Build upgrade URL."""
        base_url = "https://tradingrobotplug.com/upgrade"
        return f"{base_url}?user_id={user_id}&tier={target_tier}"
    
    def _build_unsubscribe_url(self, user_id: int) -> str:
        """Build unsubscribe URL."""
        base_url = "https://tradingrobotplug.com/unsubscribe"
        return f"{base_url}?user_id={user_id}"
    
    def _record_email_sent(
        self, trigger: CampaignTrigger, template: EmailTemplate
    ) -> None:
        """Record email sent in database."""
        if not self.database:
            return
        
        try:
            query = """
                INSERT INTO email_campaign_log
                (user_id, trigger_event, template_subject, sent_at)
                VALUES (%s, %s, %s, NOW())
            """
            self.database.execute_query(
                query,
                (trigger.user_id, trigger.trigger_event, template.subject)
            )
        except Exception as e:
            logger.warning(f"Error recording email sent: {e}")
    
    def check_and_send_campaigns(self) -> int:
        """Check for users who need campaign emails and send them."""
        if not self.database:
            logger.warning("No database configured for campaign checking")
            return 0
        
        try:
            sent_count = 0
            
            # Check free tier users
            free_triggers = self._get_free_tier_triggers()
            for trigger in free_triggers:
                if self.process_trigger(trigger):
                    sent_count += 1
            
            # Check low tier users
            low_triggers = self._get_low_tier_triggers()
            for trigger in low_triggers:
                if self.process_trigger(trigger):
                    sent_count += 1
            
            # Check mid tier users
            mid_triggers = self._get_mid_tier_triggers()
            for trigger in mid_triggers:
                if self.process_trigger(trigger):
                    sent_count += 1
            
            logger.info(f"Campaign check complete: {sent_count} emails sent")
            return sent_count
            
        except Exception as e:
            logger.error(f"Error checking campaigns: {e}", exc_info=True)
            return 0
    
    def _get_free_tier_triggers(self) -> List[CampaignTrigger]:
        """Get triggers for free tier users."""
        if not self.database:
            return []
        
        triggers = []
        try:
            # Users who hit 7-day limit
            query = """
                SELECT u.id, u.email, u.username, u.subscription_start_date
                FROM users u
                WHERE u.subscription_tier = 'free'
                AND u.subscription_status = 'active'
                AND u.subscription_start_date <= NOW() - INTERVAL '7 days'
                AND u.subscription_start_date > NOW() - INTERVAL '8 days'
            """
            results = self.database.execute_query(query)
            
            for row in results:
                triggers.append(CampaignTrigger(
                    user_id=row[0],
                    user_email=row[1],
                    user_name=row[2] or "Trader",
                    current_tier="free",
                    trigger_event="free_tier_7_days",
                    trigger_date=datetime.now(),
                    metadata={"subscription_start": row[3]}
                ))
            
            # Users who hit 14-day milestone
            query = """
                SELECT u.id, u.email, u.username, u.subscription_start_date
                FROM users u
                WHERE u.subscription_tier = 'free'
                AND u.subscription_status = 'active'
                AND u.subscription_start_date <= NOW() - INTERVAL '14 days'
                AND u.subscription_start_date > NOW() - INTERVAL '15 days'
            """
            results = self.database.execute_query(query)
            
            for row in results:
                triggers.append(CampaignTrigger(
                    user_id=row[0],
                    user_email=row[1],
                    user_name=row[2] or "Trader",
                    current_tier="free",
                    trigger_event="free_tier_14_days",
                    trigger_date=datetime.now(),
                    metadata={"subscription_start": row[3]}
                ))
            
        except Exception as e:
            logger.error(f"Error getting free tier triggers: {e}")
        
        return triggers
    
    def _get_low_tier_triggers(self) -> List[CampaignTrigger]:
        """Get triggers for low tier users."""
        if not self.database:
            return []
        
        triggers = []
        try:
            # Users at 30-day milestone
            query = """
                SELECT u.id, u.email, u.username, u.subscription_start_date
                FROM users u
                WHERE u.subscription_tier = 'low'
                AND u.subscription_status = 'active'
                AND u.subscription_start_date <= NOW() - INTERVAL '30 days'
                AND u.subscription_start_date > NOW() - INTERVAL '31 days'
            """
            results = self.database.execute_query(query)
            
            for row in results:
                triggers.append(CampaignTrigger(
                    user_id=row[0],
                    user_email=row[1],
                    user_name=row[2] or "Trader",
                    current_tier="low",
                    trigger_event="low_tier_30_days",
                    trigger_date=datetime.now(),
                    metadata={"subscription_start": row[3]}
                ))
            
        except Exception as e:
            logger.error(f"Error getting low tier triggers: {e}")
        
        return triggers
    
    def _get_mid_tier_triggers(self) -> List[CampaignTrigger]:
        """Get triggers for mid tier users."""
        if not self.database:
            return []
        
        triggers = []
        try:
            # Users at 60-day milestone
            query = """
                SELECT u.id, u.email, u.username, u.subscription_start_date
                FROM users u
                WHERE u.subscription_tier = 'mid'
                AND u.subscription_status = 'active'
                AND u.subscription_start_date <= NOW() - INTERVAL '60 days'
                AND u.subscription_start_date > NOW() - INTERVAL '61 days'
            """
            results = self.database.execute_query(query)
            
            for row in results:
                triggers.append(CampaignTrigger(
                    user_id=row[0],
                    user_email=row[1],
                    user_name=row[2] or "Trader",
                    current_tier="mid",
                    trigger_event="mid_tier_60_days",
                    trigger_date=datetime.now(),
                    metadata={"subscription_start": row[3]}
                ))
            
        except Exception as e:
            logger.error(f"Error getting mid tier triggers: {e}")
        
        return triggers

