# Trading Robot Email Campaigns

Email campaign system for subscription tier conversions.

## Campaigns

### Free → Low Commitment ($9.99/month)
- **Template 1**: Limit reached prompt (trigger: `free_tier_limit_reached`)
- **Template 2**: 7-day follow-up (trigger: `free_tier_7_days`)
- **Template 3**: 14-day limited time offer (trigger: `free_tier_14_days`)

### Low → Mid-Tier ($29.99/month)
- **Template 1**: 30-day milestone (trigger: `low_tier_30_days`)
- **Template 2**: Robot limit reached (trigger: `low_tier_robot_limit`)

### Mid → Premium ($99.99/month)
- **Template 1**: High usage offer (trigger: `mid_tier_high_usage`)
- **Template 2**: 60-day enterprise offer (trigger: `mid_tier_60_days`)

## Usage

```python
from trading_robot.email_campaigns import EmailCampaignManager, EmailService

# Initialize
email_service = EmailService(
    smtp_host="smtp.gmail.com",
    smtp_port=587,
    smtp_user="your-email@gmail.com",
    smtp_password="your-password",
    from_email="noreply@tradingrobotplug.com",
)

campaign_manager = EmailCampaignManager(
    email_service=email_service,
    database=your_database,
)

# Process triggers
trigger = CampaignTrigger(
    user_id=123,
    user_email="user@example.com",
    user_name="John Doe",
    current_tier="free",
    trigger_event="free_tier_7_days",
    trigger_date=datetime.now(),
    metadata={},
)

campaign_manager.process_trigger(trigger)

# Or check and send automatically
campaign_manager.check_and_send_campaigns()
```

## Database Schema

```sql
CREATE TABLE email_campaign_log (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    trigger_event VARCHAR(100) NOT NULL,
    template_subject VARCHAR(255) NOT NULL,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE INDEX idx_campaign_log_user ON email_campaign_log(user_id);
CREATE INDEX idx_campaign_log_sent ON email_campaign_log(sent_at);
```

## Automation

Set up a scheduled job (cron/scheduler) to run:
```python
campaign_manager.check_and_send_campaigns()
```

Recommended frequency: Daily at 9 AM (after user activity analysis)

