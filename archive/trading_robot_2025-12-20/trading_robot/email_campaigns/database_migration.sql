-- Email Campaign Log Table
-- ========================
-- 
-- Stores email campaign sending history to prevent duplicates
-- and track campaign performance.
--
-- Author: Agent-8 (SSOT & System Integration Specialist)
-- Date: 2025-12-20

CREATE TABLE IF NOT EXISTS email_campaign_log (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    trigger_event VARCHAR(100) NOT NULL,
    template_subject VARCHAR(255) NOT NULL,
    campaign_name VARCHAR(50) NOT NULL,
    tier_from VARCHAR(20) NOT NULL,
    tier_to VARCHAR(20) NOT NULL,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    opened_at TIMESTAMP NULL,
    clicked_at TIMESTAMP NULL,
    converted_at TIMESTAMP NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_campaign_log_user 
    ON email_campaign_log(user_id);
CREATE INDEX IF NOT EXISTS idx_campaign_log_sent 
    ON email_campaign_log(sent_at);
CREATE INDEX IF NOT EXISTS idx_campaign_log_event 
    ON email_campaign_log(trigger_event);
CREATE INDEX IF NOT EXISTS idx_campaign_log_campaign 
    ON email_campaign_log(campaign_name);

-- Campaign performance view
CREATE OR REPLACE VIEW email_campaign_performance AS
SELECT 
    campaign_name,
    tier_from,
    tier_to,
    trigger_event,
    COUNT(*) as emails_sent,
    COUNT(opened_at) as emails_opened,
    COUNT(clicked_at) as emails_clicked,
    COUNT(converted_at) as conversions,
    ROUND(COUNT(opened_at)::numeric / NULLIF(COUNT(*), 0) * 100, 2) as open_rate,
    ROUND(COUNT(clicked_at)::numeric / NULLIF(COUNT(*), 0) * 100, 2) as click_rate,
    ROUND(COUNT(converted_at)::numeric / NULLIF(COUNT(*), 0) * 100, 2) as conversion_rate
FROM email_campaign_log
GROUP BY campaign_name, tier_from, tier_to, trigger_event;

