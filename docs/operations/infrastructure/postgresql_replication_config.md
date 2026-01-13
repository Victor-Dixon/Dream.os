# PostgreSQL Replication Configuration
## Infrastructure Block 5 - Database Read/Write Splitting
## Agent-3 (Infrastructure & DevOps) - 2026-01-07

**Status:** ACTIVE IMPLEMENTATION
**Purpose:** Enable database read/write splitting for Revenue Engine production deployment
**Configuration:** PostgreSQL 15+ with streaming replication

---

## Primary Database Configuration

### postgresql.conf (Primary)
```ini
# Replication Settings
wal_level = replica
max_wal_senders = 10
max_replication_slots = 10
wal_keep_size = 1GB
hot_standby = on

# Connection Settings
listen_addresses = '*'
max_connections = 200
shared_preload_libraries = 'pg_stat_statements'

# Performance Settings
shared_buffers = 256MB
effective_cache_size = 1GB
maintenance_work_mem = 64MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100

# Logging
log_line_prefix = '%t [%p]: [%l-1] user=%u,db=%d,app=%a,client=%h '
log_statement = 'ddl'
log_min_duration_statement = 1000
```

### pg_hba.conf (Primary)
```ini
# TYPE  DATABASE        USER            ADDRESS                 METHOD
local   all             postgres                                trust
local   all             all                                     md5
host    all             all             127.0.0.1/32            md5
host    all             all             ::1/128                 md5

# Replication connections
host    replication     replicator      192.168.1.0/24         md5
host    revenue_engine   revenue_user    192.168.1.0/24         md5
```

### Replication User Setup
```sql
-- Create replication user
CREATE USER replicator WITH REPLICATION ENCRYPTED PASSWORD 'secure_password_here';
GRANT CONNECT ON DATABASE revenue_engine TO replicator;

-- Create revenue engine user with appropriate permissions
CREATE USER revenue_user WITH ENCRYPTED PASSWORD 'secure_password_here';
GRANT CONNECT ON DATABASE revenue_engine TO revenue_user;
GRANT USAGE ON SCHEMA public TO revenue_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO revenue_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO revenue_user;
```

---

## Replica Database Configuration

### postgresql.conf (Replica)
```ini
# Replication Settings
hot_standby = on
max_standby_archive_delay = 30s
max_standby_streaming_delay = 30s
wal_receiver_status_interval = 10s
hot_standby_feedback = on

# Connection Settings
listen_addresses = '*'
max_connections = 200

# Performance Settings (optimized for reads)
shared_buffers = 256MB
effective_cache_size = 1GB
maintenance_work_mem = 64MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100

# Read-only settings
default_transaction_read_only = off  # Allow read/write on primary, read-only on replicas
```

### recovery.conf (Replica)
```ini
# Recovery settings
standby_mode = 'on'
primary_conninfo = 'host=postgres-primary port=5432 user=replicator password=secure_password_here application_name=replica1'
recovery_target_timeline = 'latest'
trigger_file = '/var/lib/postgresql/data/failover_trigger'
```

---

## Application Connection Configuration

### Database URL Configuration
```python
# Revenue Engine database configuration
DATABASE_CONFIG = {
    'primary': {
        'host': 'postgres-primary',
        'port': 5432,
        'database': 'revenue_engine',
        'ssl_mode': 'require',
        'application_name': 'revenue-engine-primary'
    },
    'replicas': [
        {
            'host': 'postgres-replica-1',
            'port': 5432,
            'database': 'revenue_engine',
            'ssl_mode': 'require',
            'application_name': 'revenue-engine-replica-1'
        },
        {
            'host': 'postgres-replica-2',
            'port': 5432,
            'database': 'revenue_engine',
            'ssl_mode': 'require',
            'application_name': 'revenue-engine-replica-2'
        }
    ]
}
```

### Connection Routing Logic
```python
import psycopg2
import random

class DatabaseConnectionManager:
    def __init__(self, config):
        self.primary_config = config['primary']
        self.replica_configs = config['replicas']

    def get_write_connection(self):
        """Always use primary for writes"""
        return psycopg2.connect(**self.primary_config)

    def get_read_connection(self):
        """Use replicas for reads with load balancing"""
        if not self.replica_configs:
            return psycopg2.connect(**self.primary_config)

        # Simple round-robin load balancing
        replica_config = random.choice(self.replica_configs)
        try:
            return psycopg2.connect(**replica_config)
        except Exception as e:
            # Fallback to primary if replica fails
            print(f"Replica connection failed: {e}, using primary")
            return psycopg2.connect(**self.primary_config)

    def execute_read_query(self, query, params=None):
        """Execute read-only queries on replicas"""
        conn = self.get_read_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        finally:
            conn.close()

    def execute_write_query(self, query, params=None):
        """Execute write queries on primary"""
        conn = self.get_write_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                conn.commit()
                return cursor.rowcount
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
```

---

## Monitoring and Health Checks

### Replication Status Query
```sql
-- Check replication status on primary
SELECT
    client_addr,
    state,
    sent_lsn,
    write_lsn,
    flush_lsn,
    replay_lsn,
    sync_state
FROM pg_stat_replication;

-- Check replication lag on replica
SELECT
    now() - pg_last_xact_replay_timestamp() as replication_lag,
    pg_is_in_recovery() as is_replica,
    pg_current_wal_lsn() as current_lsn,
    pg_last_wal_receive_lsn() as received_lsn,
    pg_last_wal_replay_lsn() as replayed_lsn;
```

### Health Check Script
```bash
#!/bin/bash
# PostgreSQL replication health check

PRIMARY_HOST="postgres-primary"
REPLICA_HOST="postgres-replica-1"
DB_NAME="revenue_engine"
DB_USER="monitor_user"

# Check if primary is accepting connections
if psql -h $PRIMARY_HOST -U $DB_USER -d $DB_NAME -c "SELECT 1;" > /dev/null 2>&1; then
    echo "✅ Primary database is healthy"
else
    echo "❌ Primary database is unreachable"
    exit 1
fi

# Check replication lag
LAG=$(psql -h $REPLICA_HOST -U $DB_USER -d $DB_NAME -c "SELECT EXTRACT(EPOCH FROM (now() - pg_last_xact_replay_timestamp())) as lag_seconds;" -t -A)
if (( $(echo "$LAG < 60" | bc -l) )); then
    echo "✅ Replication lag is acceptable: ${LAG}s"
else
    echo "⚠️ Replication lag is high: ${LAG}s"
fi

echo "Database replication health check complete"
```

---

## Failover Procedures

### Manual Failover to Replica
```bash
# On the replica server
# Create trigger file to promote replica to primary
touch /var/lib/postgresql/data/failover_trigger

# Wait for promotion to complete
sleep 10

# Verify promotion
psql -c "SELECT pg_is_in_recovery();"

# Update application configuration to point to new primary
# (This would be handled by your configuration management system)
```

### Automated Failover (Using repmgr)
```bash
# Install repmgr
sudo apt-get install postgresql-15-repmgr

# Configure repmgr
cat > /etc/repmgr.conf << EOF
node_id=1
node_name=node1
conninfo='host=postgres-primary port=5432 user=repmgr dbname=repmgr'
failover=automatic
promote_command='/usr/bin/repmgr standby promote -f /etc/repmgr.conf'
follow_command='/usr/bin/repmgr standby follow -f /etc/repmgr.conf'
EOF

# Register primary
repmgr primary register -f /etc/repmgr.conf

# Register standby
repmgr standby register -f /etc/repmgr.conf
```

---

## Performance Tuning

### Connection Pool Size Calculation
```
Max connections = (RAM in GB * 100) / max_connections_per_process
For 4GB RAM with 10MB per connection: (4000 * 100) / 10 = 40,000 connections
Practical limit with monitoring: ~200 connections per database
```

### WAL Tuning
```sql
-- Adjust WAL settings based on workload
ALTER SYSTEM SET wal_level = 'replica';
ALTER SYSTEM SET max_wal_senders = 10;
ALTER SYSTEM SET wal_keep_size = '1GB';

-- Monitor WAL generation
SELECT
    pg_current_wal_lsn(),
    pg_walfile_name(pg_current_wal_lsn()),
    pg_size_pretty(pg_wal_lsn_diff(pg_current_wal_lsn(), '0/0'));
```

---

## Backup Strategy

### Base Backup
```bash
# Create base backup from replica (non-blocking)
pg_basebackup -h postgres-replica-1 -U replicator -D /backup/base_backup_$(date +%Y%m%d_%H%M%S) -Ft -z -P

# Restore base backup
tar -xzf base_backup_20240107_120000.tar.gz -C /var/lib/postgresql/data
```

### Continuous WAL Archiving
```bash
# archive_command in postgresql.conf
archive_command = 'cp %p /archive/%f'

# Restore from WAL archives
pg_ctl start -D /var/lib/postgresql/data
psql -c "SELECT pg_wal_replay_resume();"
```

---

## Security Considerations

### SSL/TLS Configuration
```ini
# Require SSL for all connections
ssl = on
ssl_cert_file = '/etc/ssl/certs/postgresql.crt'
ssl_key_file = '/etc/ssl/private/postgresql.key'
ssl_ca_file = '/etc/ssl/certs/ca.crt'

# SSL mode settings
ssl_ciphers = 'HIGH:MEDIUM:+3DES:!aNULL:!SSLv3:!TLSv1'
ssl_prefer_server_ciphers = on
```

### Access Control
```sql
-- Create read-only user for analytics
CREATE USER analytics_user WITH PASSWORD 'secure_password';
GRANT CONNECT ON DATABASE revenue_engine TO analytics_user;
GRANT USAGE ON SCHEMA public TO analytics_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO analytics_user;

-- Row-level security for multi-tenant data
ALTER TABLE user_data ENABLE ROW LEVEL SECURITY;
CREATE POLICY user_data_policy ON user_data
    FOR ALL USING (user_id = current_user_id());
```

---

**PostgreSQL Replication Configuration Complete ✅**
**Agent-3 (Infrastructure & DevOps) - 2026-01-07**
**Status:** Ready for deployment and testing