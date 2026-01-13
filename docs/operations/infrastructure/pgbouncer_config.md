# PgBouncer Connection Pooling Configuration
## Infrastructure Block 5 - Database Connection Optimization
## Agent-3 (Infrastructure & DevOps) - 2026-01-07

**Status:** ACTIVE IMPLEMENTATION
**Purpose:** Deploy PgBouncer for efficient database connection pooling in Revenue Engine
**Configuration:** Transaction pooling mode with connection multiplexing

---

## PgBouncer Architecture

### Connection Flow
```
Application → PgBouncer → PostgreSQL
     ↓              ↓              ↓
   Pool Mode    Connection      Database
   Management   Multiplexing    Server
```

### Pooling Modes
- **Session Pooling:** One server connection per client connection
- **Transaction Pooling:** One server connection per client transaction ⭐ (RECOMMENDED)
- **Statement Pooling:** One server connection per client statement

---

## Configuration Files

### pgbouncer.ini (Main Configuration)
```ini
[databases]
# Revenue Engine database connections
revenue_engine = host=postgres-primary port=5432 dbname=revenue_engine
revenue_engine_replica1 = host=postgres-replica-1 port=5432 dbname=revenue_engine
revenue_engine_replica2 = host=postgres-replica-2 port=5432 dbname=revenue_engine

# Analytics database (read-only)
analytics_db = host=postgres-replica-1 port=5432 dbname=revenue_engine

[pgbouncer]
# Network settings
listen_addr = 0.0.0.0
listen_port = 6432
unix_socket_dir = /tmp

# Authentication
auth_type = md5
auth_file = /etc/pgbouncer/userlist.txt
auth_user = pgbouncer_admin

# Connection pooling
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 20
min_pool_size = 5
reserve_pool_size = 5
reserve_pool_timeout = 3
max_db_connections = 50
max_user_connections = 100

# Connection settings
server_reset_query = DISCARD ALL
server_check_delay = 30
server_check_query = SELECT 1
server_lifetime = 3600
server_idle_timeout = 600
server_connect_timeout = 15
server_login_retry = 15

# Client settings
client_login_timeout = 60
client_idle_timeout = 0
autodb_idle_timeout = 3600

# Logging
logfile = /var/log/pgbouncer/pgbouncer.log
pidfile = /var/run/pgbouncer/pgbouncer.pid
admin_users = pgbouncer_admin
stats_users = monitor_user

# Performance tuning
pkt_buf = 4096
max_packet_size = 2147483647
listen_backlog = 128

# Security
client_tls_sslmode = require
client_tls_cert_file = /etc/ssl/certs/pgbouncer.crt
client_tls_key_file = /etc/ssl/private/pgbouncer.key
client_tls_ca_file = /etc/ssl/certs/ca.crt
server_tls_sslmode = require
server_tls_ca_file = /etc/ssl/certs/ca.crt
```

### userlist.txt (Authentication)
```
# PgBouncer user authentication
"pgbouncer_admin" "secure_admin_password"
"monitor_user" "secure_monitor_password"
"revenue_user" "secure_revenue_password"
"analytics_user" "secure_analytics_password"
```

---

## Application Connection Configuration

### Python Connection with PgBouncer
```python
import psycopg2
import psycopg2.pool

class PgBouncerConnectionManager:
    def __init__(self, pgbouncer_config):
        self.pgbouncer_host = pgbouncer_config.get('host', 'localhost')
        self.pgbouncer_port = pgbouncer_config.get('port', 6432)
        self.database_configs = pgbouncer_config.get('databases', {})

        # Connection pool settings
        self.pool_min_conn = pgbouncer_config.get('pool_min_conn', 5)
        self.pool_max_conn = pgbouncer_config.get('pool_max_conn', 20)

    def get_connection_pool(self, db_name='revenue_engine'):
        """Create connection pool through PgBouncer"""
        if db_name not in self.database_configs:
            raise ValueError(f"Database {db_name} not configured")

        db_config = self.database_configs[db_name]

        pool = psycopg2.pool.SimpleConnectionPool(
            self.pool_min_conn,
            self.pool_max_conn,
            host=self.pgbouncer_host,
            port=self.pgbouncer_port,
            database=db_config.get('database', db_name),
            user=db_config.get('user', 'revenue_user'),
            password=db_config.get('password', 'secure_password'),
            sslmode='require',
            application_name=f'revenue-engine-{db_name}'
        )

        return pool

    def get_write_connection(self):
        """Get connection for write operations (goes to primary)"""
        pool = self.get_connection_pool('revenue_engine')
        return pool.getconn()

    def get_read_connection(self):
        """Get connection for read operations (load balanced across replicas)"""
        # Round-robin between replica databases
        replica_dbs = ['revenue_engine_replica1', 'revenue_engine_replica2']
        import random
        db_name = random.choice(replica_dbs)

        pool = self.get_connection_pool(db_name)
        return pool.getconn()

    def execute_read_query(self, query, params=None):
        """Execute read-only query with connection pooling"""
        conn = self.get_read_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        finally:
            # Return connection to pool
            pool = self.get_connection_pool('revenue_engine_replica1')
            pool.putconn(conn)

    def execute_write_query(self, query, params=None):
        """Execute write query with connection pooling"""
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
            # Return connection to pool
            pool = self.get_connection_pool('revenue_engine')
            pool.putconn(conn)

# Configuration example
PGBOUNCER_CONFIG = {
    'host': 'pgbouncer-service',
    'port': 6432,
    'pool_min_conn': 5,
    'pool_max_conn': 20,
    'databases': {
        'revenue_engine': {
            'user': 'revenue_user',
            'password': 'secure_revenue_password'
        },
        'revenue_engine_replica1': {
            'user': 'revenue_user',
            'password': 'secure_revenue_password'
        },
        'revenue_engine_replica2': {
            'user': 'revenue_user',
            'password': 'secure_revenue_password'
        },
        'analytics_db': {
            'user': 'analytics_user',
            'password': 'secure_analytics_password'
        }
    }
}
```

---

## Monitoring and Health Checks

### PgBouncer Admin Console
```bash
# Connect to PgBouncer admin console
psql -h localhost -p 6432 -U pgbouncer_admin pgbouncer

# Show connection statistics
SHOW STATS;
SHOW POOLS;
SHOW DATABASES;
SHOW CLIENTS;
SHOW SERVERS;

# Monitor connection usage
SELECT * FROM pg_stat_activity LIMIT 10;
```

### Health Check Script
```bash
#!/bin/bash
# PgBouncer health check

PGBOUNCER_HOST="localhost"
PGBOUNCER_PORT="6432"
ADMIN_USER="pgbouncer_admin"
ADMIN_PASS="secure_admin_password"

# Test basic connectivity
if psql -h $PGBOUNCER_HOST -p $PGBOUNCER_PORT -U $ADMIN_USER -d pgbouncer -c "SHOW VERSION;" > /dev/null 2>&1; then
    echo "✅ PgBouncer is responding"
else
    echo "❌ PgBouncer is unreachable"
    exit 1
fi

# Check pool status
POOL_STATUS=$(psql -h $PGBOUNCER_HOST -p $PGBOUNCER_PORT -U $ADMIN_USER -d pgbouncer -c "SHOW POOLS;" -t -A)

# Parse pool statistics
TOTAL_CLIENTS=$(echo "$POOL_STATUS" | awk '{sum += $3} END {print sum}')
ACTIVE_SERVERS=$(echo "$POOL_STATUS" | awk '{sum += $4} END {print sum}')
IDLE_SERVERS=$(echo "$POOL_STATUS" | awk '{sum += $5} END {print sum}')

echo "📊 Connection Pool Status:"
echo "   Total clients: $TOTAL_CLIENTS"
echo "   Active servers: $ACTIVE_SERVERS"
echo "   Idle servers: $IDLE_SERVERS"

# Check for connection issues
if [ "$TOTAL_CLIENTS" -gt 800 ]; then
    echo "⚠️ High client connections: $TOTAL_CLIENTS"
fi

if [ "$IDLE_SERVERS" -lt 5 ]; then
    echo "⚠️ Low idle servers: $IDLE_SERVERS"
fi

# Test actual database connection through PgBouncer
if psql -h $PGBOUNCER_HOST -p $PGBOUNCER_PORT -U revenue_user -d revenue_engine -c "SELECT 1;" > /dev/null 2>&1; then
    echo "✅ Database connectivity through PgBouncer is working"
else
    echo "❌ Database connectivity failed"
    exit 1
fi

echo "PgBouncer health check complete"
```

### Prometheus Monitoring
```yaml
# PgBouncer exporter configuration
pgbouncer_exporter:
  image: spreaker/pgbouncer-exporter:latest
  environment:
    - PGBOUNCER_HOST=pgbouncer-service
    - PGBOUNCER_PORT=6432
    - PGBOUNCER_USER=monitor_user
    - PGBOUNCER_PASSWORD=secure_monitor_password
  ports:
    - "9127:9127"
```

---

## Performance Tuning

### Pool Size Calculation
```bash
# Calculate optimal pool sizes based on system resources
# Formula: pool_size = (RAM in GB * 50) / avg_connection_size_mb
# For 4GB RAM with 2MB avg connection: (4000 * 50) / 2 = 100,000
# Practical limit with monitoring: 20-50 connections per pool

# Monitor pool efficiency
psql -h localhost -p 6432 -U pgbouncer_admin -d pgbouncer << 'EOF'
SELECT
    database,
    user,
    cl_active,
    cl_waiting,
    sv_active,
    sv_idle,
    sv_used,
    sv_tested,
    sv_login,
    maxwait
FROM pg_stat_pgbouncer_pools;
EOF
```

### Connection Timeout Tuning
```ini
# Optimize timeouts for different workloads
server_idle_timeout = 600    # Close idle server connections after 10 minutes
server_lifetime = 3600       # Recycle connections after 1 hour
client_idle_timeout = 0      # Keep client connections alive
autodb_idle_timeout = 3600   # Close unused database connections after 1 hour
```

### Memory Optimization
```bash
# Monitor PgBouncer memory usage
ps aux | grep pgbouncer
cat /proc/$(pgrep pgbouncer)/status | grep VmRSS

# Adjust packet buffer size for large queries
# pkt_buf = 8192 for queries > 4KB
echo "pkt_buf = 8192" >> /etc/pgbouncer/pgbouncer.ini
```

---

## High Availability Configuration

### Load Balancer Configuration (HAProxy)
```ini
# HAProxy configuration for PgBouncer HA
frontend pgbouncer_frontend
    bind *:6432
    mode tcp
    default_backend pgbouncer_backend

backend pgbouncer_backend
    mode tcp
    balance roundrobin
    server pgbouncer-1 pgbouncer-1:6432 check
    server pgbouncer-2 pgbouncer-2:6432 check backup
```

### Failover Configuration
```bash
# PgBouncer failover script
#!/bin/bash

PRIMARY_PGBOUNCER="pgbouncer-1"
BACKUP_PGBOUNCER="pgbouncer-2"

# Check if primary is healthy
if ! psql -h $PRIMARY_PGBOUNCER -p 6432 -U monitor_user -d pgbouncer -c "SHOW VERSION;" > /dev/null 2>&1; then
    echo "Primary PgBouncer failed, promoting backup..."

    # Update HAProxy configuration
    sed -i 's/server pgbouncer-2.*backup/server pgbouncer-2/' /etc/haproxy/haproxy.cfg
    sed -i 's/server pgbouncer-1/server pgbouncer-1 backup/' /etc/haproxy/haproxy.cfg

    # Reload HAProxy
    systemctl reload haproxy

    echo "✅ Failover completed"
else
    echo "✅ Primary PgBouncer is healthy"
fi
```

---

## Security Configuration

### SSL/TLS Setup
```bash
# Generate SSL certificates for PgBouncer
openssl req -new -x509 -days 365 -nodes -text -out pgbouncer.crt -keyout pgbouncer.key -subj "/CN=pgbouncer-service"

# Set proper permissions
chmod 600 pgbouncer.key
chown pgbouncer:pgbouncer pgbouncer.crt pgbouncer.key

# Configure PgBouncer for SSL
cat >> /etc/pgbouncer/pgbouncer.ini << EOF
client_tls_sslmode = require
client_tls_cert_file = /etc/ssl/certs/pgbouncer.crt
client_tls_key_file = /etc/ssl/private/pgbouncer.key
server_tls_sslmode = require
EOF
```

### Access Control
```ini
# Restrict database access
[databases]
revenue_engine = host=postgres-primary port=5432 dbname=revenue_engine user=revenue_user
analytics_db = host=postgres-replica-1 port=5432 dbname=revenue_engine user=analytics_user

# User-specific connection limits
max_user_connections = 50
```

---

## Integration Testing

### Connection Pool Stress Test
```python
import time
import threading
from pgbouncer_manager import PgBouncerConnectionManager

def stress_test_connections(num_threads=50, duration=60):
    """Stress test connection pooling"""
    manager = PgBouncerConnectionManager(PGBOUNCER_CONFIG)

    def worker_thread(thread_id):
        start_time = time.time()
        connections_used = 0

        while time.time() - start_time < duration:
            try:
                # Test read connection
                conn = manager.get_read_connection()
                with conn.cursor() as cursor:
                    cursor.execute("SELECT 1")
                    result = cursor.fetchone()
                connections_used += 1

                # Test write connection
                conn = manager.get_write_connection()
                with conn.cursor() as cursor:
                    cursor.execute("SELECT pg_backend_pid()")
                    result = cursor.fetchone()
                connections_used += 1

                # Small delay to simulate real usage
                time.sleep(0.1)

            except Exception as e:
                print(f"Thread {thread_id}: Error - {e}")
                break

        print(f"Thread {thread_id}: Completed {connections_used} connection cycles")

    # Start stress test threads
    threads = []
    for i in range(num_threads):
        t = threading.Thread(target=worker_thread, args=(i,))
        threads.append(t)
        t.start()

    # Wait for all threads to complete
    for t in threads:
        t.join()

    print("✅ Connection pool stress test completed")

if __name__ == "__main__":
    stress_test_connections()
```

---

## Troubleshooting

### Common Issues and Solutions

#### Connection Pool Exhaustion
```bash
# Check pool status
psql -h localhost -p 6432 -U pgbouncer_admin -d pgbouncer -c "SHOW POOLS;"

# Increase pool size
echo "default_pool_size = 30" >> /etc/pgbouncer/pgbouncer.ini
systemctl reload pgbouncer
```

#### Authentication Failures
```bash
# Check user authentication
psql -h localhost -p 6432 -U revenue_user -d revenue_engine -c "SELECT current_user;"

# Verify userlist.txt format
cat /etc/pgbouncer/userlist.txt
# Should be: "username" "password"
```

#### Connection Timeouts
```bash
# Increase timeouts
echo "server_connect_timeout = 30" >> /etc/pgbouncer/pgbouncer.ini
echo "client_login_timeout = 120" >> /etc/pgbouncer/pgbouncer.ini
systemctl reload pgbouncer
```

---

**PgBouncer Connection Pooling Configuration Complete ✅**
**Agent-3 (Infrastructure & DevOps) - 2026-01-07**
**Status:** Ready for deployment and parallel validation testing