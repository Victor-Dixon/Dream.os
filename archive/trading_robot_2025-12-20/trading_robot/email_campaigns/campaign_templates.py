#!/usr/bin/env python3
"""
Email Campaign Templates
========================

Email campaign templates for subscription tier conversions.

V2 Compliance: <300 lines
Author: Agent-8 (SSOT & System Integration Specialist)
Date: 2025-12-20
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass


@dataclass
class EmailTemplate:
    """Email template structure."""
    subject: str
    html_body: str
    text_body: str
    trigger_event: str
    delay_days: int


class FreeToLowCampaign:
    """Email campaign for Free → Low Commitment conversion."""
    
    CAMPAIGN_NAME = "free_to_low"
    TIER_FROM = "free"
    TIER_TO = "low"
    PRICE = "$9.99/month"
    
    @staticmethod
    def get_templates() -> List[EmailTemplate]:
        """Get email templates for free → low conversion."""
        return [
            EmailTemplate(
                subject="🚀 Unlock 3 Trading Robots - Upgrade to Low Commitment",
                html_body=FreeToLowCampaign._template_1_html(),
                text_body=FreeToLowCampaign._template_1_text(),
                trigger_event="free_tier_limit_reached",
                delay_days=0
            ),
            EmailTemplate(
                subject="📊 See What You're Missing - Full Performance Tracking Available",
                html_body=FreeToLowCampaign._template_2_html(),
                text_body=FreeToLowCampaign._template_2_text(),
                trigger_event="free_tier_7_days",
                delay_days=7
            ),
            EmailTemplate(
                subject="⚡ Limited Time: Upgrade to Low Commitment - Save on Your First Month",
                html_body=FreeToLowCampaign._template_3_html(),
                text_body=FreeToLowCampaign._template_3_text(),
                trigger_event="free_tier_14_days",
                delay_days=14
            ),
        ]
    
    @staticmethod
    def _template_1_html() -> str:
        """Template 1: Limit reached prompt."""
        return """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
        .content { background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }
        .cta-button { display: inline-block; background: #667eea; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; font-weight: bold; }
        .features { background: white; padding: 20px; margin: 20px 0; border-radius: 5px; border-left: 4px solid #667eea; }
        .feature-item { margin: 10px 0; padding-left: 25px; }
        .footer { text-align: center; color: #666; font-size: 12px; margin-top: 30px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Unlock More Trading Robots</h1>
            <p>You've reached your free tier limit</p>
        </div>
        <div class="content">
            <p>Hi {user_name},</p>
            
            <p>You're currently using the <strong>Free tier</strong> with access to 1 demo robot. We noticed you've hit the 7-day history limit and might want more features.</p>
            
            <div class="features">
                <h3>Upgrade to Low Commitment ($9.99/month) and get:</h3>
                <div class="feature-item">✅ <strong>3 trading robots</strong> (instead of 1)</div>
                <div class="feature-item">✅ <strong>Full performance tracking</strong> (daily/weekly/monthly)</div>
                <div class="feature-item">✅ <strong>30 days historical data</strong> (instead of 7)</div>
                <div class="feature-item">✅ <strong>Email support</strong> and basic strategy customization</div>
            </div>
            
            <p style="text-align: center;">
                <a href="{upgrade_url}" class="cta-button">Upgrade to Low Commitment - $9.99/month</a>
            </p>
            
            <p>See what you're missing with full performance tracking and access to more trading strategies.</p>
            
            <p>Best regards,<br>The Trading Robot Team</p>
        </div>
        <div class="footer">
            <p>You're receiving this because you're on the Free tier. <a href="{unsubscribe_url}">Unsubscribe</a></p>
        </div>
    </div>
</body>
</html>
"""
    
    @staticmethod
    def _template_1_text() -> str:
        """Template 1 text version."""
        return """
🚀 Unlock More Trading Robots

Hi {user_name},

You've reached your free tier limit. Upgrade to Low Commitment ($9.99/month) and get:

✅ 3 trading robots (instead of 1)
✅ Full performance tracking (daily/weekly/monthly)
✅ 30 days historical data (instead of 7)
✅ Email support and basic strategy customization

Upgrade now: {upgrade_url}

See what you're missing with full performance tracking and access to more trading strategies.

Best regards,
The Trading Robot Team

---
Unsubscribe: {unsubscribe_url}
"""
    
    @staticmethod
    def _template_2_html() -> str:
        """Template 2: 7-day follow-up."""
        return """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
        .content { background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }
        .cta-button { display: inline-block; background: #f5576c; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; font-weight: bold; }
        .comparison { background: white; padding: 20px; margin: 20px 0; border-radius: 5px; }
        .comparison-table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        .comparison-table td { padding: 10px; border-bottom: 1px solid #eee; }
        .comparison-table .feature { font-weight: bold; }
        .footer { text-align: center; color: #666; font-size: 12px; margin-top: 30px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 See What You're Missing</h1>
            <p>Full Performance Tracking Available</p>
        </div>
        <div class="content">
            <p>Hi {user_name},</p>
            
            <p>You've been using our Free tier for 7 days. Here's what you're missing with <strong>Low Commitment ($9.99/month)</strong>:</p>
            
            <div class="comparison">
                <table class="comparison-table">
                    <tr>
                        <td class="feature">Trading Robots</td>
                        <td>Free: 1 demo</td>
                        <td>Low: <strong>3 robots</strong></td>
                    </tr>
                    <tr>
                        <td class="feature">Performance Tracking</td>
                        <td>Free: Daily only</td>
                        <td>Low: <strong>Daily/Weekly/Monthly</strong></td>
                    </tr>
                    <tr>
                        <td class="feature">Historical Data</td>
                        <td>Free: 7 days</td>
                        <td>Low: <strong>30 days</strong></td>
                    </tr>
                    <tr>
                        <td class="feature">Support</td>
                        <td>Free: Community</td>
                        <td>Low: <strong>Email support</strong></td>
                    </tr>
                </table>
            </div>
            
            <p style="text-align: center;">
                <a href="{upgrade_url}" class="cta-button">Upgrade Now - $9.99/month</a>
            </p>
            
            <p>Unlock full performance tracking and see your trading results across multiple timeframes.</p>
            
            <p>Best regards,<br>The Trading Robot Team</p>
        </div>
        <div class="footer">
            <p>You're receiving this because you're on the Free tier. <a href="{unsubscribe_url}">Unsubscribe</a></p>
        </div>
    </div>
</body>
</html>
"""
    
    @staticmethod
    def _template_2_text() -> str:
        """Template 2 text version."""
        return """
📊 See What You're Missing

Hi {user_name},

You've been using our Free tier for 7 days. Here's what you're missing:

Trading Robots: Free (1 demo) → Low ($9.99/month): 3 robots
Performance Tracking: Free (Daily only) → Low: Daily/Weekly/Monthly
Historical Data: Free (7 days) → Low: 30 days
Support: Free (Community) → Low: Email support

Upgrade now: {upgrade_url}

Unlock full performance tracking and see your trading results across multiple timeframes.

Best regards,
The Trading Robot Team

---
Unsubscribe: {unsubscribe_url}
"""
    
    @staticmethod
    def _template_3_html() -> str:
        """Template 3: 14-day limited time offer."""
        return """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); color: #333; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
        .content { background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }
        .cta-button { display: inline-block; background: #fa709a; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; font-weight: bold; }
        .offer-badge { background: #fee140; color: #333; padding: 10px 20px; border-radius: 5px; display: inline-block; font-weight: bold; margin: 20px 0; }
        .footer { text-align: center; color: #666; font-size: 12px; margin-top: 30px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⚡ Limited Time Offer</h1>
            <p>Save on Your First Month</p>
        </div>
        <div class="content">
            <p>Hi {user_name},</p>
            
            <p>You've been exploring our Free tier for 2 weeks. As a thank you, we're offering a <strong>special discount</strong> on your first month of Low Commitment.</p>
            
            <div style="text-align: center;">
                <div class="offer-badge">🎁 First Month: $7.99 (Save $2.00)</div>
            </div>
            
            <p>Upgrade to <strong>Low Commitment</strong> and get:</p>
            <ul>
                <li>✅ 3 trading robots (instead of 1)</li>
                <li>✅ Full performance tracking (daily/weekly/monthly)</li>
                <li>✅ 30 days historical data</li>
                <li>✅ Email support</li>
            </ul>
            
            <p style="text-align: center;">
                <a href="{upgrade_url}" class="cta-button">Claim Offer - $7.99 First Month</a>
            </p>
            
            <p><strong>Offer expires in 48 hours.</strong> Don't miss out on unlocking more trading robots and full performance tracking.</p>
            
            <p>Best regards,<br>The Trading Robot Team</p>
        </div>
        <div class="footer">
            <p>You're receiving this because you're on the Free tier. <a href="{unsubscribe_url}">Unsubscribe</a></p>
        </div>
    </div>
</body>
</html>
"""
    
    @staticmethod
    def _template_3_text() -> str:
        """Template 3 text version."""
        return """
⚡ Limited Time Offer - Save on Your First Month

Hi {user_name},

You've been exploring our Free tier for 2 weeks. As a thank you, we're offering a special discount on your first month of Low Commitment.

🎁 First Month: $7.99 (Save $2.00)

Upgrade to Low Commitment and get:
✅ 3 trading robots (instead of 1)
✅ Full performance tracking (daily/weekly/monthly)
✅ 30 days historical data
✅ Email support

Claim offer: {upgrade_url}

Offer expires in 48 hours. Don't miss out on unlocking more trading robots and full performance tracking.

Best regards,
The Trading Robot Team

---
Unsubscribe: {unsubscribe_url}
"""


class LowToMidCampaign:
    """Email campaign for Low → Mid-Tier conversion."""
    
    CAMPAIGN_NAME = "low_to_mid"
    TIER_FROM = "low"
    TIER_TO = "mid"
    PRICE = "$29.99/month"
    
    @staticmethod
    def get_templates() -> List[EmailTemplate]:
        """Get email templates for low → mid conversion."""
        return [
            EmailTemplate(
                subject="🚀 Unlock Live Trading & All Robots - Upgrade to Mid-Tier",
                html_body=LowToMidCampaign._template_1_html(),
                text_body=LowToMidCampaign._template_1_text(),
                trigger_event="low_tier_30_days",
                delay_days=30
            ),
            EmailTemplate(
                subject="📈 Access All Trading Robots - Unlimited History Available",
                html_body=LowToMidCampaign._template_2_html(),
                text_body=LowToMidCampaign._template_2_text(),
                trigger_event="low_tier_robot_limit",
                delay_days=0
            ),
        ]
    
    @staticmethod
    def _template_1_html() -> str:
        """Template 1: 30-day milestone."""
        return """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
        .content { background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }
        .cta-button { display: inline-block; background: #4facfe; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; font-weight: bold; }
        .features { background: white; padding: 20px; margin: 20px 0; border-radius: 5px; border-left: 4px solid #4facfe; }
        .feature-item { margin: 10px 0; padding-left: 25px; }
        .footer { text-align: center; color: #666; font-size: 12px; margin-top: 30px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Unlock Live Trading & All Robots</h1>
            <p>Upgrade to Mid-Tier</p>
        </div>
        <div class="content">
            <p>Hi {user_name},</p>
            
            <p>You've been using <strong>Low Commitment</strong> for 30 days. Ready to unlock the full potential?</p>
            
            <div class="features">
                <h3>Upgrade to Mid-Tier ($29.99/month) and get:</h3>
                <div class="feature-item">✅ <strong>All trading robots</strong> (10+ robots, instead of 3)</div>
                <div class="feature-item">✅ <strong>Live trading</strong> (with safeguards) - Trade with real money</div>
                <div class="feature-item">✅ <strong>Unlimited historical data</strong> (instead of 30 days)</div>
                <div class="feature-item">✅ <strong>Performance analytics dashboard</strong> with advanced metrics</div>
                <div class="feature-item">✅ <strong>API access</strong> for custom integrations</div>
                <div class="feature-item">✅ <strong>Priority email support</strong> and advanced strategy customization</div>
            </div>
            
            <p style="text-align: center;">
                <a href="{upgrade_url}" class="cta-button">Upgrade to Mid-Tier - $29.99/month</a>
            </p>
            
            <p>Take your trading to the next level with live trading and access to all our proven strategies.</p>
            
            <p>Best regards,<br>The Trading Robot Team</p>
        </div>
        <div class="footer">
            <p>You're receiving this because you're on the Low Commitment tier. <a href="{unsubscribe_url}">Unsubscribe</a></p>
        </div>
    </div>
</body>
</html>
"""
    
    @staticmethod
    def _template_1_text() -> str:
        """Template 1 text version."""
        return """
🚀 Unlock Live Trading & All Robots

Hi {user_name},

You've been using Low Commitment for 30 days. Ready to unlock the full potential?

Upgrade to Mid-Tier ($29.99/month) and get:
✅ All trading robots (10+ robots, instead of 3)
✅ Live trading (with safeguards) - Trade with real money
✅ Unlimited historical data (instead of 30 days)
✅ Performance analytics dashboard with advanced metrics
✅ API access for custom integrations
✅ Priority email support and advanced strategy customization

Upgrade now: {upgrade_url}

Take your trading to the next level with live trading and access to all our proven strategies.

Best regards,
The Trading Robot Team

---
Unsubscribe: {unsubscribe_url}
"""
    
    @staticmethod
    def _template_2_html() -> str:
        """Template 2: Robot limit reached."""
        return """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #30cfd0 0%, #330867 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
        .content { background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }
        .cta-button { display: inline-block; background: #30cfd0; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; font-weight: bold; }
        .robot-list { background: white; padding: 20px; margin: 20px 0; border-radius: 5px; }
        .footer { text-align: center; color: #666; font-size: 12px; margin-top: 30px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📈 Access All Trading Robots</h1>
            <p>Unlimited History Available</p>
        </div>
        <div class="content">
            <p>Hi {user_name},</p>
            
            <p>You've reached your 3-robot limit on <strong>Low Commitment</strong>. Upgrade to <strong>Mid-Tier ($29.99/month)</strong> and unlock access to all our trading robots:</p>
            
            <div class="robot-list">
                <h3>Available Robots (10+):</h3>
                <ul>
                    <li>TSLA Improved Strategy</li>
                    <li>Trend Following Robot</li>
                    <li>Mean Reversion Robot</li>
                    <li>Momentum Trading Robot</li>
                    <li>And 6+ more strategies...</li>
                </ul>
            </div>
            
            <p><strong>Plus:</strong></p>
            <ul>
                <li>✅ Live trading capability</li>
                <li>✅ Unlimited historical data</li>
                <li>✅ Performance analytics dashboard</li>
                <li>✅ API access</li>
            </ul>
            
            <p style="text-align: center;">
                <a href="{upgrade_url}" class="cta-button">Upgrade to Mid-Tier - $29.99/month</a>
            </p>
            
            <p>Unlock the full library of proven trading strategies and take your portfolio to the next level.</p>
            
            <p>Best regards,<br>The Trading Robot Team</p>
        </div>
        <div class="footer">
            <p>You're receiving this because you're on the Low Commitment tier. <a href="{unsubscribe_url}">Unsubscribe</a></p>
        </div>
    </div>
</body>
</html>
"""
    
    @staticmethod
    def _template_2_text() -> str:
        """Template 2 text version."""
        return """
📈 Access All Trading Robots

Hi {user_name},

You've reached your 3-robot limit on Low Commitment. Upgrade to Mid-Tier ($29.99/month) and unlock access to all our trading robots:

Available Robots (10+):
- TSLA Improved Strategy
- Trend Following Robot
- Mean Reversion Robot
- Momentum Trading Robot
- And 6+ more strategies...

Plus:
✅ Live trading capability
✅ Unlimited historical data
✅ Performance analytics dashboard
✅ API access

Upgrade now: {upgrade_url}

Unlock the full library of proven trading strategies and take your portfolio to the next level.

Best regards,
The Trading Robot Team

---
Unsubscribe: {unsubscribe_url}
"""


class MidToPremiumCampaign:
    """Email campaign for Mid → Premium conversion."""
    
    CAMPAIGN_NAME = "mid_to_premium"
    TIER_FROM = "mid"
    TIER_TO = "premium"
    PRICE = "$99.99/month"
    
    @staticmethod
    def get_templates() -> List[EmailTemplate]:
        """Get email templates for mid → premium conversion."""
        return [
            EmailTemplate(
                subject="🎯 Custom Trading Robot Development - Upgrade to Premium",
                html_body=MidToPremiumCampaign._template_1_html(),
                text_body=MidToPremiumCampaign._template_1_text(),
                trigger_event="mid_tier_high_usage",
                delay_days=0
            ),
            EmailTemplate(
                subject="💼 Enterprise Features Available - Premium Tier Benefits",
                html_body=MidToPremiumCampaign._template_2_html(),
                text_body=MidToPremiumCampaign._template_2_text(),
                trigger_event="mid_tier_60_days",
                delay_days=60
            ),
        ]
    
    @staticmethod
    def _template_1_html() -> str:
        """Template 1: High usage offer."""
        return """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); color: #333; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
        .content { background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }
        .cta-button { display: inline-block; background: #fa709a; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; font-weight: bold; }
        .premium-features { background: white; padding: 20px; margin: 20px 0; border-radius: 5px; border-left: 4px solid #fa709a; }
        .feature-item { margin: 10px 0; padding-left: 25px; }
        .footer { text-align: center; color: #666; font-size: 12px; margin-top: 30px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 Custom Trading Robot Development</h1>
            <p>Upgrade to Premium</p>
        </div>
        <div class="content">
            <p>Hi {user_name},</p>
            
            <p>We noticed you're a power user on <strong>Mid-Tier</strong>. Ready for something custom?</p>
            
            <div class="premium-features">
                <h3>Upgrade to Premium ($99.99/month) and get:</h3>
                <div class="feature-item">✅ <strong>Custom trading robot development</strong> - Built to your specifications</div>
                <div class="feature-item">✅ <strong>Dedicated support channel</strong> - Priority response time</div>
                <div class="feature-item">✅ <strong>Advanced risk management tools</strong> - Portfolio optimization</div>
                <div class="feature-item">✅ <strong>White-label options</strong> - Brand it your way</div>
                <div class="feature-item">✅ <strong>Early access</strong> to new robots and features</div>
                <div class="feature-item">✅ <strong>1-on-1 strategy consultation</strong> - Monthly sessions</div>
                <div class="feature-item">✅ <strong>Everything in Mid-Tier</strong> - All robots, live trading, API access</div>
            </div>
            
            <p style="text-align: center;">
                <a href="{upgrade_url}" class="cta-button">Contact Sales for Premium - $99.99/month</a>
            </p>
            
            <p>Perfect for traders who need custom solutions, enterprise features, or dedicated support. Let's build a trading robot tailored to your strategy.</p>
            
            <p>Best regards,<br>The Trading Robot Team</p>
        </div>
        <div class="footer">
            <p>You're receiving this because you're on the Mid-Tier. <a href="{unsubscribe_url}">Unsubscribe</a></p>
        </div>
    </div>
</body>
</html>
"""
    
    @staticmethod
    def _template_1_text() -> str:
        """Template 1 text version."""
        return """
🎯 Custom Trading Robot Development

Hi {user_name},

We noticed you're a power user on Mid-Tier. Ready for something custom?

Upgrade to Premium ($99.99/month) and get:
✅ Custom trading robot development - Built to your specifications
✅ Dedicated support channel - Priority response time
✅ Advanced risk management tools - Portfolio optimization
✅ White-label options - Brand it your way
✅ Early access to new robots and features
✅ 1-on-1 strategy consultation - Monthly sessions
✅ Everything in Mid-Tier - All robots, live trading, API access

Contact sales: {upgrade_url}

Perfect for traders who need custom solutions, enterprise features, or dedicated support. Let's build a trading robot tailored to your strategy.

Best regards,
The Trading Robot Team

---
Unsubscribe: {unsubscribe_url}
"""
    
    @staticmethod
    def _template_2_html() -> str:
        """Template 2: 60-day enterprise offer."""
        return """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
        .content { background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }
        .cta-button { display: inline-block; background: #667eea; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; font-weight: bold; }
        .enterprise-box { background: white; padding: 20px; margin: 20px 0; border-radius: 5px; border: 2px solid #667eea; }
        .footer { text-align: center; color: #666; font-size: 12px; margin-top: 30px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>💼 Enterprise Features Available</h1>
            <p>Premium Tier Benefits</p>
        </div>
        <div class="content">
            <p>Hi {user_name},</p>
            
            <p>You've been a valued <strong>Mid-Tier</strong> member for 60 days. Ready to unlock enterprise-level features?</p>
            
            <div class="enterprise-box">
                <h3>Premium Tier ($99.99/month) - Enterprise Features:</h3>
                <ul>
                    <li><strong>Custom Robot Development:</strong> We'll build a trading robot tailored to your specific strategy and risk profile</li>
                    <li><strong>White-Label Options:</strong> Brand the platform with your company name and logo</li>
                    <li><strong>Dedicated Support:</strong> Priority channel with guaranteed response times</li>
                    <li><strong>Portfolio Optimization:</strong> Advanced risk management and portfolio analysis tools</li>
                    <li><strong>Monthly Strategy Consultation:</strong> 1-on-1 sessions with our trading experts</li>
                    <li><strong>Early Access:</strong> Be first to test new robots and features</li>
                </ul>
            </div>
            
            <p style="text-align: center;">
                <a href="{upgrade_url}" class="cta-button">Contact Sales for Premium - $99.99/month</a>
            </p>
            
            <p>Perfect for serious traders, trading firms, or anyone who needs custom solutions and dedicated support.</p>
            
            <p>Best regards,<br>The Trading Robot Team</p>
        </div>
        <div class="footer">
            <p>You're receiving this because you're on the Mid-Tier. <a href="{unsubscribe_url}">Unsubscribe</a></p>
        </div>
    </div>
</body>
</html>
"""
    
    @staticmethod
    def _template_2_text() -> str:
        """Template 2 text version."""
        return """
💼 Enterprise Features Available

Hi {user_name},

You've been a valued Mid-Tier member for 60 days. Ready to unlock enterprise-level features?

Premium Tier ($99.99/month) - Enterprise Features:
- Custom Robot Development: We'll build a trading robot tailored to your specific strategy
- White-Label Options: Brand the platform with your company name and logo
- Dedicated Support: Priority channel with guaranteed response times
- Portfolio Optimization: Advanced risk management and portfolio analysis tools
- Monthly Strategy Consultation: 1-on-1 sessions with our trading experts
- Early Access: Be first to test new robots and features

Contact sales: {upgrade_url}

Perfect for serious traders, trading firms, or anyone who needs custom solutions and dedicated support.

Best regards,
The Trading Robot Team

---
Unsubscribe: {unsubscribe_url}
"""

