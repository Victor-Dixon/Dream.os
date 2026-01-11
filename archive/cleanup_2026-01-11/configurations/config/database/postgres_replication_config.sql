-- PostgreSQL Replication Configuration for Read/Write Splitting
-- Infrastructure Block 5 - Database Optimization Phase
-- Agent-3 (Infrastructure & DevOps) - 2026-01-07

-- Primary Database Configuration (Write Operations)
-- postgresql.conf settings for primary
-- wal_level = replica
-- max_wal_senders = 3
-- wal_keep_size = 64MB
-- synchronous_commit = off
-- hot_standby = on

-- Replica Configuration (Read Operations)
-- recovery.conf for streaming replication
-- standby_mode = on
-- primary_conninfo = 'host=postgres-primary port=5432 user=replication password=replication_password'
-- trigger_file = '/tmp/postgresql.trigger'

-- Database Connection Configuration for Application
-- Read/Write Splitting Logic
CREATE OR REPLACE FUNCTION get_replica_host()
RETURNS TEXT AS $$
DECLARE
    replica_hosts TEXT[] := ARRAY['postgres-replica-1', 'postgres-replica-2'];
    random_index INTEGER;
BEGIN
    -- Random load balancing across replicas
    random_index := floor(random() * array_length(replica_hosts, 1)) + 1;
    RETURN replica_hosts[random_index];
END;
$$ LANGUAGE plpgsql;

-- Connection Pool Configuration for PgBouncer
-- pgbouncer.ini configuration
-- [databases]
-- tradingrobotplug = host=postgres-primary port=5432 dbname=tradingrobotplug
-- tradingrobotplug_read = host=get_replica_host() port=5432 dbname=tradingrobotplug

-- [pgbouncer]
-- listen_port = 6432
-- listen_addr = *
-- auth_type = md5
-- auth_file = /etc/pgbouncer/userlist.txt
-- pool_mode = transaction
-- max_client_conn = 1000
-- default_pool_size = 50
-- reserve_pool_size = 10
-- reserve_pool_timeout = 5
-- max_db_connections = 200
-- max_user_connections = 100
-- server_idle_timeout = 30
-- server_lifetime = 3600
-- server_reset_query = DISCARD ALL
-- server_reset_query_always = 0
-- server_check_delay = 30
-- server_check_query = select 1

-- Database Schema Optimization for Revenue Engine
CREATE TABLE IF NOT EXISTS revenue_metrics (
    id SERIAL PRIMARY KEY,
    metric_name VARCHAR(255) NOT NULL,
    metric_value DECIMAL(15,6),
    metric_type VARCHAR(50),
    collection_timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    source_system VARCHAR(100),
    tags JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Partitioning for performance (by month)
CREATE TABLE revenue_metrics_y2026m01 PARTITION OF revenue_metrics
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');

CREATE TABLE revenue_metrics_y2026m02 PARTITION OF revenue_metrics
    FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');

-- Indexes for Revenue Engine queries
CREATE INDEX CONCURRENTLY idx_revenue_metrics_name_time ON revenue_metrics (metric_name, collection_timestamp DESC);
CREATE INDEX CONCURRENTLY idx_revenue_metrics_type ON revenue_metrics (metric_type);
CREATE INDEX CONCURRENTLY idx_revenue_metrics_source ON revenue_metrics (source_system);
CREATE INDEX CONCURRENTLY idx_revenue_metrics_tags ON revenue_metrics USING GIN (tags);

-- Materialized view for aggregated metrics (refreshed every 5 minutes)
CREATE MATERIALIZED VIEW revenue_metrics_hourly AS
SELECT
    metric_name,
    date_trunc('hour', collection_timestamp) as hour_bucket,
    source_system,
    AVG(metric_value) as avg_value,
    MIN(metric_value) as min_value,
    MAX(metric_value) as max_value,
    COUNT(*) as sample_count,
    STDDEV(metric_value) as std_dev
FROM revenue_metrics
WHERE collection_timestamp >= NOW() - INTERVAL '24 hours'
GROUP BY metric_name, date_trunc('hour', collection_timestamp), source_system
ORDER BY hour_bucket DESC, metric_name;

-- Refresh function for materialized view
CREATE OR REPLACE FUNCTION refresh_revenue_metrics_hourly()
RETURNS VOID AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY revenue_metrics_hourly;
END;
$$ LANGUAGE plpgsql;

-- Automated refresh schedule (every 5 minutes)
-- Would be configured in pg_cron or external scheduler
-- SELECT cron.schedule('refresh-revenue-metrics', '*/5 * * * *', 'SELECT refresh_revenue_metrics_hourly();');

-- Read replica routing function for application
CREATE OR REPLACE FUNCTION get_connection_string(is_write BOOLEAN DEFAULT FALSE)
RETURNS TEXT AS $$
DECLARE
    conn_string TEXT;
BEGIN
    IF is_write THEN
        -- Always route writes to primary
        conn_string := 'host=postgres-primary port=5432 dbname=tradingrobotplug user=app_user sslmode=require';
    ELSE
        -- Route reads to replicas with load balancing
        conn_string := 'host=' || get_replica_host() || ' port=5432 dbname=tradingrobotplug user=app_user sslmode=require';
    END IF;

    RETURN conn_string;
END;
$$ LANGUAGE plpgsql;

-- Connection health check function
CREATE OR REPLACE FUNCTION check_database_health()
RETURNS TABLE (
    database_name TEXT,
    connection_count INTEGER,
    active_connections INTEGER,
    max_connections INTEGER,
    connection_ratio DECIMAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        datname::TEXT,
        (SELECT count(*) FROM pg_stat_activity WHERE datname = d.datname)::INTEGER,
        (SELECT count(*) FROM pg_stat_activity WHERE datname = d.datname AND state = 'active')::INTEGER,
        (SELECT setting::INTEGER FROM pg_settings WHERE name = 'max_connections'),
        ROUND(
            (SELECT count(*) FROM pg_stat_activity WHERE datname = d.datname)::DECIMAL /
            (SELECT setting::INTEGER FROM pg_settings WHERE name = 'max_connections')::DECIMAL * 100,
            2
        )
    FROM pg_database d
    WHERE datname NOT IN ('postgres', 'template0', 'template1');
END;
$$ LANGUAGE plpgsql;

-- Performance monitoring view
CREATE OR REPLACE VIEW database_performance_metrics AS
SELECT
    schemaname,
    tablename,
    attname AS column_name,
    n_distinct,
    correlation,
    most_common_vals,
    most_common_freqs
FROM pg_stats
WHERE schemaname = 'public'
ORDER BY n_distinct DESC, tablename;

-- Query performance monitoring
CREATE TABLE IF NOT EXISTS query_performance_log (
    id SERIAL PRIMARY KEY,
    query_text TEXT,
    execution_time INTERVAL,
    rows_affected INTEGER,
    user_name TEXT,
    database_name TEXT,
    client_addr INET,
    application_name TEXT,
    executed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Auto-explain for slow queries (would be configured in postgresql.conf)
-- auto_explain.log_min_duration = 1000ms
-- auto_explain.log_analyze = true
-- auto_explain.log_verbose = true
-- auto_explain.log_buffers = true

-- Replication monitoring
CREATE OR REPLACE VIEW replication_status AS
SELECT
    client_addr,
    state,
    sent_lsn,
    write_lsn,
    flush_lsn,
    replay_lsn,
    write_lag,
    flush_lag,
    replay_lag,
    sync_priority,
    sync_state
FROM pg_stat_replication;

COMMENT ON VIEW replication_status IS 'Real-time replication status for read replicas';
COMMENT ON MATERIALIZED VIEW revenue_metrics_hourly IS 'Hourly aggregated revenue metrics for performance monitoring';
COMMENT ON FUNCTION get_replica_host() IS 'Load balancing function for read replicas';
COMMENT ON FUNCTION check_database_health() IS 'Health check function for database connections';