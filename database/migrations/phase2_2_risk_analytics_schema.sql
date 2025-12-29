-- TradingRobotPlug Phase 2.2 Risk Analytics Database Schema
-- Author: Agent-5 (Business Intelligence Specialist)
-- Date: 2025-12-29
-- Description: Database schema extensions for advanced risk analytics

-- =====================================================
-- Risk Metrics Storage Table
-- =====================================================

CREATE TABLE IF NOT EXISTS wp_trp_risk_metrics (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    strategy_id VARCHAR(100),
    calculation_date DATE NOT NULL,

    -- Core Risk Metrics
    var_95 DECIMAL(15,2) COMMENT 'Value at Risk (95% confidence, 1-day horizon)',
    cvar_95 DECIMAL(15,2) COMMENT 'Conditional VaR (95% confidence)',

    -- Risk-Adjusted Return Metrics
    sharpe_ratio DECIMAL(10,4) COMMENT 'Sharpe Ratio',
    sortino_ratio DECIMAL(10,4) COMMENT 'Sortino Ratio (downside deviation)',
    information_ratio DECIMAL(10,4) COMMENT 'Information Ratio',

    -- Drawdown Metrics
    max_drawdown DECIMAL(15,2) COMMENT 'Maximum Drawdown (peak-to-trough)',
    calmar_ratio DECIMAL(10,4) COMMENT 'Calmar Ratio (annual return / max drawdown)',

    -- Additional Risk Metrics
    volatility_annual DECIMAL(10,4) COMMENT 'Annualized volatility',
    beta DECIMAL(10,4) COMMENT 'Beta relative to market benchmark',
    alpha DECIMAL(10,4) COMMENT 'Alpha (excess return)',

    -- Metadata
    data_points INT COMMENT 'Number of data points used in calculation',
    confidence_level DECIMAL(3,2) DEFAULT 0.95 COMMENT 'Confidence level for VaR/CVaR',
    calculation_method VARCHAR(50) DEFAULT 'historical_simulation' COMMENT 'Calculation methodology',

    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    -- Indexes for performance
    INDEX idx_user_strategy_date (user_id, strategy_id, calculation_date),
    INDEX idx_calculation_date (calculation_date),
    INDEX idx_user_id (user_id),
    INDEX idx_strategy_id (strategy_id),

    -- Foreign key constraints
    FOREIGN KEY (user_id) REFERENCES wp_users(ID) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- Risk Alerts Table
-- =====================================================

CREATE TABLE IF NOT EXISTS wp_trp_risk_alerts (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    strategy_id VARCHAR(100),

    -- Alert Details
    alert_type VARCHAR(50) NOT NULL COMMENT 'Type of risk alert (var_threshold, drawdown_threshold, sharpe_ratio_low, etc.)',
    alert_code VARCHAR(20) NOT NULL COMMENT 'Unique alert code for grouping',
    severity ENUM('low', 'medium', 'high', 'critical') NOT NULL DEFAULT 'medium',

    -- Threshold and Current Values
    threshold_value DECIMAL(15,2) COMMENT 'Configured threshold value',
    current_value DECIMAL(15,2) NOT NULL COMMENT 'Current calculated value',
    threshold_operator ENUM('gt', 'gte', 'lt', 'lte', 'eq', 'neq') DEFAULT 'gt' COMMENT 'Comparison operator',

    -- Alert Content
    alert_title VARCHAR(255) NOT NULL COMMENT 'Human-readable alert title',
    alert_message TEXT NOT NULL COMMENT 'Detailed alert description',
    alert_recommendation TEXT COMMENT 'Recommended actions',

    -- Alert Status
    acknowledged BOOLEAN DEFAULT FALSE COMMENT 'Whether user has acknowledged the alert',
    acknowledged_at TIMESTAMP NULL COMMENT 'When alert was acknowledged',
    acknowledged_by BIGINT COMMENT 'User ID who acknowledged',
    resolved BOOLEAN DEFAULT FALSE COMMENT 'Whether the underlying risk condition is resolved',
    resolved_at TIMESTAMP NULL COMMENT 'When risk condition was resolved',

    -- Escalation
    escalated BOOLEAN DEFAULT FALSE COMMENT 'Whether alert has been escalated',
    escalation_level INT DEFAULT 0 COMMENT 'Escalation level (0=none, 1=email, 2=sms, 3=phone)',
    last_notification TIMESTAMP NULL COMMENT 'Last time notification was sent',

    -- Metadata
    source_table VARCHAR(100) COMMENT 'Source table that triggered alert',
    source_record_id BIGINT COMMENT 'Record ID in source table',
    calculation_id BIGINT COMMENT 'Risk calculation ID that triggered alert',

    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    -- Indexes for performance
    INDEX idx_user_alert_type (user_id, alert_type),
    INDEX idx_severity (severity),
    INDEX idx_acknowledged (acknowledged),
    INDEX idx_resolved (resolved),
    INDEX idx_created_at (created_at),
    INDEX idx_alert_code (alert_code),
    INDEX idx_user_strategy (user_id, strategy_id),

    -- Foreign key constraints
    FOREIGN KEY (user_id) REFERENCES wp_users(ID) ON DELETE CASCADE,
    FOREIGN KEY (acknowledged_by) REFERENCES wp_users(ID) ON DELETE SET NULL,
    FOREIGN KEY (calculation_id) REFERENCES wp_trp_risk_metrics(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- Risk Thresholds Configuration Table
-- =====================================================

CREATE TABLE IF NOT EXISTS wp_trp_risk_thresholds (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    strategy_id VARCHAR(100),

    -- Threshold Configurations
    threshold_type VARCHAR(50) NOT NULL COMMENT 'Type of threshold (var_95, max_drawdown, sharpe_ratio_min, etc.)',
    threshold_value DECIMAL(15,2) NOT NULL COMMENT 'Threshold value',
    threshold_operator ENUM('gt', 'gte', 'lt', 'lte', 'eq', 'neq') DEFAULT 'gt',
    severity ENUM('low', 'medium', 'high', 'critical') DEFAULT 'medium',

    -- Threshold Settings
    enabled BOOLEAN DEFAULT TRUE COMMENT 'Whether this threshold is active',
    notification_enabled BOOLEAN DEFAULT TRUE COMMENT 'Whether to send notifications',
    notification_channels JSON COMMENT 'Notification channels (email, sms, webhook, etc.)',

    -- Time-based Settings
    time_window VARCHAR(20) DEFAULT '1d' COMMENT 'Time window for threshold evaluation (1d, 1w, 1m, etc.)',
    evaluation_frequency VARCHAR(20) DEFAULT 'realtime' COMMENT 'How often to evaluate (realtime, hourly, daily)',

    -- Metadata
    description TEXT COMMENT 'Human-readable description of threshold',
    created_by BIGINT COMMENT 'User who created this threshold',
    last_triggered TIMESTAMP NULL COMMENT 'Last time this threshold was triggered',

    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    -- Indexes
    INDEX idx_user_threshold_type (user_id, threshold_type),
    INDEX idx_enabled (enabled),
    INDEX idx_user_strategy (user_id, strategy_id),

    -- Foreign key constraints
    FOREIGN KEY (user_id) REFERENCES wp_users(ID) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES wp_users(ID) ON DELETE SET NULL,

    -- Unique constraint to prevent duplicate thresholds
    UNIQUE KEY unique_user_strategy_threshold (user_id, strategy_id, threshold_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- Risk Calculation History Table
-- =====================================================

CREATE TABLE IF NOT EXISTS wp_trp_risk_calculation_history (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    strategy_id VARCHAR(100),

    -- Calculation Details
    calculation_type VARCHAR(50) NOT NULL COMMENT 'Type of calculation (comprehensive, var_only, etc.)',
    calculation_date TIMESTAMP NOT NULL,
    data_start_date DATE COMMENT 'Start date of data used',
    data_end_date DATE COMMENT 'End date of data used',
    data_points_used INT COMMENT 'Number of data points in calculation',

    -- Results Storage (JSON for flexibility)
    calculation_results JSON NOT NULL COMMENT 'Complete calculation results',
    calculation_metadata JSON COMMENT 'Additional calculation metadata',

    -- Performance Metrics
    calculation_duration_ms INT COMMENT 'Time taken for calculation in milliseconds',
    cache_hit BOOLEAN DEFAULT FALSE COMMENT 'Whether result came from cache',

    -- Error Handling
    calculation_status ENUM('success', 'warning', 'error') DEFAULT 'success',
    error_message TEXT COMMENT 'Error message if calculation failed',
    retry_count INT DEFAULT 0 COMMENT 'Number of retries attempted',

    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Indexes
    INDEX idx_user_calculation_date (user_id, calculation_date),
    INDEX idx_calculation_type (calculation_type),
    INDEX idx_calculation_status (calculation_status),
    INDEX idx_user_strategy (user_id, strategy_id),

    -- Foreign key constraints
    FOREIGN KEY (user_id) REFERENCES wp_users(ID) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- Default Risk Thresholds (Seed Data)
-- =====================================================

-- Insert default conservative risk thresholds for new users
INSERT IGNORE INTO wp_trp_risk_thresholds
(user_id, strategy_id, threshold_type, threshold_value, threshold_operator, severity, description)
SELECT
    u.ID as user_id,
    NULL as strategy_id,
    thresholds.threshold_type,
    thresholds.threshold_value,
    thresholds.threshold_operator,
    thresholds.severity,
    thresholds.description
FROM wp_users u
CROSS JOIN (
    SELECT 'var_95' as threshold_type, 0.05 as threshold_value, 'gt' as threshold_operator, 'high' as severity, 'VaR (95%) exceeds 5% threshold' as description
    UNION ALL
    SELECT 'max_drawdown', 0.20, 'gt', 'critical', 'Maximum drawdown exceeds 20% threshold'
    UNION ALL
    SELECT 'sharpe_ratio_min', 1.0, 'lt', 'medium', 'Sharpe ratio below 1.0 minimum'
    UNION ALL
    SELECT 'volatility_max', 0.30, 'gt', 'high', 'Annualized volatility exceeds 30%'
) as thresholds
WHERE u.user_registered > DATE_SUB(NOW(), INTERVAL 30 DAY); -- Only for new users in last 30 days

-- =====================================================
-- Performance Optimizations
-- =====================================================

-- Add partitioning to risk_metrics table for better performance (if MySQL 5.7+)
-- This would be applied as a separate ALTER TABLE statement in production

-- Create composite indexes for common query patterns
CREATE INDEX idx_risk_metrics_user_date_range ON wp_trp_risk_metrics (user_id, calculation_date, strategy_id);
CREATE INDEX idx_risk_alerts_active ON wp_trp_risk_alerts (user_id, acknowledged, resolved, severity);
CREATE INDEX idx_risk_thresholds_active ON wp_trp_risk_thresholds (user_id, enabled, threshold_type);

-- =====================================================
-- Migration Complete
-- =====================================================

-- Add a comment to track migration completion
INSERT INTO wp_trp_risk_calculation_history
(user_id, strategy_id, calculation_type, calculation_date, calculation_results, calculation_metadata, calculation_status)
SELECT
    1, -- Admin user ID
    NULL,
    'migration',
    NOW(),
    '{"migration": "phase2_2_risk_analytics_schema", "status": "completed"}',
    '{"tables_created": ["wp_trp_risk_metrics", "wp_trp_risk_alerts", "wp_trp_risk_thresholds", "wp_trp_risk_calculation_history"], "indexes_created": 6}',
    'success'
FROM dual
WHERE NOT EXISTS (
    SELECT 1 FROM wp_trp_risk_calculation_history
    WHERE calculation_type = 'migration'
    AND JSON_EXTRACT(calculation_results, '$.migration') = 'phase2_2_risk_analytics_schema'
)
LIMIT 1;

