# Redis Cluster Configuration
## Infrastructure Block 5 - High-Performance Caching Layer
## Agent-3 (Infrastructure & DevOps) - 2026-01-07

**Status:** ACTIVE IMPLEMENTATION
**Purpose:** Deploy Redis cluster for Revenue Engine caching and session management
**Configuration:** Redis 7+ cluster with 3 masters + 3 replicas (6 nodes total)

---

## Redis Cluster Architecture

### Cluster Topology
```
Master Nodes (Write Operations):
├── redis-master-1:6379 (slots 0-5460)
├── redis-master-2:6380 (slots 5461-10922)
└── redis-master-3:6381 (slots 10923-16383)

Replica Nodes (Read Operations):
├── redis-replica-1:6379 (replicates master-1)
├── redis-replica-2:6380 (replicates master-2)
└── redis-replica-3:6381 (replicates master-3)
```

---

## Redis Configuration Files

### redis.conf (Master Nodes)
```ini
# Cluster settings
cluster-enabled yes
cluster-config-file nodes.conf
cluster-node-timeout 5000
cluster-migration-barrier 1
cluster-require-full-coverage no

# Network settings
bind 0.0.0.0
port 6379
timeout 0
tcp-keepalive 300
tcp-backlog 511

# Memory management
maxmemory 256mb
maxmemory-policy allkeys-lru
maxmemory-samples 5

# Persistence
save 900 1
save 300 10
save 60 10000
appendonly yes
appendfilename "appendonly.aof"
appendfsync everysec

# Security
requirepass secure_redis_password
masterauth secure_redis_password

# Performance
tcp-backlog 511
databases 16
always-show-logo no

# Logging
loglevel notice
logfile /var/log/redis/redis.log

# Disable dangerous commands
rename-command FLUSHDB ""
rename-command FLUSHALL ""
rename-command SHUTDOWN SHUTDOWN_REDIS
```

### redis.conf (Replica Nodes)
```ini
# Cluster settings
cluster-enabled yes
cluster-config-file nodes.conf
cluster-node-timeout 5000
cluster-migration-barrier 1
cluster-require-full-coverage no
cluster-slave-validity-factor 10

# Network settings
bind 0.0.0.0
port 6379
timeout 0
tcp-keepalive 300
tcp-backlog 511

# Memory management
maxmemory 256mb
maxmemory-policy allkeys-lru
maxmemory-samples 5

# Replication settings
replica-read-only yes
repl-diskless-sync no
repl-diskless-sync-delay 5
repl-ping-replica-period 10
repl-timeout 60
repl-backlog-size 1mb
repl-backlog-ttl 3600

# Persistence
save 900 1
save 300 10
save 60 10000
appendonly yes
appendfilename "appendonly.aof"
appendfsync everysec

# Security
requirepass secure_redis_password
masterauth secure_redis_password

# Performance
tcp-backlog 511
databases 16

# Logging
loglevel notice
logfile /var/log/redis/redis.log

# Disable dangerous commands
rename-command FLUSHDB ""
rename-command FLUSHALL ""
rename-command SHUTDOWN SHUTDOWN_REDIS
```

---

## Cluster Setup Script

### Automated Cluster Creation
```bash
#!/bin/bash
# Redis cluster setup script

# Redis nodes configuration
NODES=(
    "redis-master-1:6379"
    "redis-master-2:6380"
    "redis-master-3:6381"
    "redis-replica-1:6379"
    "redis-replica-2:6380"
    "redis-replica-3:6381"
)

# Wait for all nodes to be ready
echo "Waiting for Redis nodes to start..."
for node in "${NODES[@]}"; do
    host=$(echo $node | cut -d: -f1)
    port=$(echo $node | cut -d: -f2)
    while ! redis-cli -h $host -p $port -a secure_redis_password ping > /dev/null 2>&1; do
        echo "Waiting for $host:$port..."
        sleep 2
    done
    echo "✅ $host:$port is ready"
done

# Create cluster
echo "Creating Redis cluster..."
redis-cli --cluster create \
    redis-master-1:6379 \
    redis-master-2:6380 \
    redis-master-3:6381 \
    redis-replica-1:6379 \
    redis-replica-2:6380 \
    redis-replica-3:6381 \
    --cluster-replicas 1 \
    --cluster-yes

echo "✅ Redis cluster created successfully"
```

### Cluster Verification
```bash
# Check cluster status
redis-cli -c -h redis-master-1 -p 6379 -a secure_redis_password cluster info
redis-cli -c -h redis-master-1 -p 6379 -a secure_redis_password cluster nodes

# Test cluster operations
redis-cli -c -h redis-master-1 -p 6379 -a secure_redis_password set test_key "Hello Redis Cluster"
redis-cli -c -h redis-replica-1 -p 6379 -a secure_redis_password get test_key
```

---

## Application Integration

### Python Redis Cluster Client
```python
import redis
from rediscluster import RedisCluster

# Redis cluster configuration
REDIS_CONFIG = {
    'startup_nodes': [
        {'host': 'redis-master-1', 'port': 6379},
        {'host': 'redis-master-2', 'port': 6380},
        {'host': 'redis-master-3', 'port': 6381},
    ],
    'password': 'secure_redis_password',
    'decode_responses': True,
    'skip_full_coverage_check': True
}

class RedisCacheManager:
    def __init__(self, config):
        self.redis_cluster = RedisCluster(**config)
        self.ttl = 3600  # 1 hour default TTL

    def set_cache(self, key, value, ttl=None):
        """Set cache value with TTL"""
        expiry = ttl or self.ttl
        return self.redis_cluster.setex(key, expiry, value)

    def get_cache(self, key):
        """Get cache value"""
        return self.redis_cluster.get(key)

    def delete_cache(self, key):
        """Delete cache key"""
        return self.redis_cluster.delete(key)

    def set_user_session(self, user_id, session_data):
        """Store user session data"""
        key = f"user_session:{user_id}"
        return self.set_cache(key, json.dumps(session_data), 3600)

    def get_user_session(self, user_id):
        """Retrieve user session data"""
        key = f"user_session:{user_id}"
        session_data = self.get_cache(key)
        return json.loads(session_data) if session_data else None

    def cache_revenue_data(self, symbol, data):
        """Cache revenue/market data"""
        key = f"revenue_data:{symbol}"
        return self.set_cache(key, json.dumps(data), 300)  # 5 min TTL

    def get_revenue_data(self, symbol):
        """Get cached revenue data"""
        key = f"revenue_data:{symbol}"
        data = self.get_cache(key)
        return json.loads(data) if data else None

    def increment_counter(self, key, amount=1):
        """Increment counter (for rate limiting, analytics)"""
        return self.redis_cluster.incrby(key, amount)

    def get_cluster_info(self):
        """Get cluster information"""
        return self.redis_cluster.cluster_info()

    def get_memory_stats(self):
        """Get memory usage statistics"""
        return self.redis_cluster.info('memory')
```

### Connection Pool Configuration
```python
# Advanced connection pool settings
REDIS_POOL_CONFIG = {
    'db': 0,
    'password': 'secure_redis_password',
    'socket_timeout': 5,
    'socket_connect_timeout': 5,
    'socket_keepalive': True,
    'socket_keepalive_options': {socket.TCP_KEEPIDLE: 60},
    'health_check_interval': 30,
    'max_connections': 20,
    'decode_responses': True,
    'retry_on_timeout': True,
    'cluster_error_retry_attempts': 3,
}
```

---

## Monitoring and Health Checks

### Redis Exporter Configuration
```yaml
# Prometheus redis_exporter configuration
redis_exporter:
  image: oliver006/redis_exporter:latest
  ports:
    - "9121:9121"
  environment:
    - REDIS_ADDR=redis://redis-master-1:6379
    - REDIS_PASSWORD=secure_redis_password
  command:
    - --redis.addr=redis://redis-master-1:6379
    - --redis.password=secure_redis_password
    - --redis.cluster.enabled=true
```

### Health Check Script
```bash
#!/bin/bash
# Redis cluster health check

MASTER_NODES=("redis-master-1:6379" "redis-master-2:6380" "redis-master-3:6381")
REPLICA_NODES=("redis-replica-1:6379" "redis-replica-2:6380" "redis-replica-3:6381")

REDIS_PASSWORD="secure_redis_password"

# Check cluster status
CLUSTER_INFO=$(redis-cli -c -h redis-master-1 -p 6379 -a $REDIS_PASSWORD cluster info)
if echo "$CLUSTER_INFO" | grep -q "cluster_state:ok"; then
    echo "✅ Redis cluster is healthy"
else
    echo "❌ Redis cluster is degraded"
    exit 1
fi

# Check all master nodes
for node in "${MASTER_NODES[@]}"; do
    host=$(echo $node | cut -d: -f1)
    port=$(echo $node | cut -d: -f2)

    if redis-cli -h $host -p $port -a $REDIS_PASSWORD ping > /dev/null 2>&1; then
        echo "✅ Master $host:$port is responding"
    else
        echo "❌ Master $host:$port is unreachable"
        exit 1
    fi
done

# Check all replica nodes
for node in "${REPLICA_NODES[@]}"; do
    host=$(echo $node | cut -d: -f1)
    port=$(echo $node | cut -d: -f2)

    if redis-cli -h $host -p $port -a $REDIS_PASSWORD ping > /dev/null 2>&1; then
        echo "✅ Replica $host:$port is responding"
    else
        echo "❌ Replica $host:$port is unreachable"
        exit 1
fi
done

# Check memory usage
MEMORY_INFO=$(redis-cli -c -h redis-master-1 -p 6379 -a $REDIS_PASSWORD info memory)
USED_MEMORY=$(echo "$MEMORY_INFO" | grep "used_memory_human" | cut -d: -f2 | tr -d '\r')
echo "📊 Memory usage: $USED_MEMORY"

echo "Redis cluster health check complete"
```

---

## Performance Tuning

### Memory Optimization
```bash
# Configure memory limits and eviction policies
redis-cli -c -h redis-master-1 -p 6379 -a secure_redis_password config set maxmemory 256mb
redis-cli -c -h redis-master-1 -p 6379 -a secure_redis_password config set maxmemory-policy allkeys-lru

# Monitor memory usage
redis-cli -c -h redis-master-1 -p 6379 -a secure_redis_password info memory
```

### Connection Tuning
```bash
# Configure connection timeouts
redis-cli -c -h redis-master-1 -p 6379 -a secure_redis_password config set timeout 300
redis-cli -c -h redis-master-1 -p 6379 -a secure_redis_password config set tcp-keepalive 300

# Monitor connections
redis-cli -c -h redis-master-1 -p 6379 -a secure_redis_password info clients
```

### Cluster Rebalancing
```bash
# Check cluster balance
redis-cli -c -h redis-master-1 -p 6379 -a secure_redis_password cluster slots

# Rebalance cluster (if needed)
redis-cli --cluster rebalance redis-master-1:6379
```

---

## Backup and Recovery

### RDB Snapshot Backup
```bash
# Manual RDB backup
redis-cli -c -h redis-master-1 -p 6379 -a secure_redis_password --rdb /backup/redis_backup_$(date +%Y%m%d_%H%M%S).rdb

# Configure automated backups in redis.conf
save 900 1      # Save after 900 seconds if at least 1 key changed
save 300 10     # Save after 300 seconds if at least 10 keys changed
save 60 10000   # Save after 60 seconds if at least 10000 keys changed
```

### Cluster Recovery
```bash
# Recover cluster from backup
# 1. Stop all Redis nodes
docker-compose stop redis-cluster

# 2. Restore RDB files to each master node
cp /backup/redis_backup_20240107.rdb /data/redis-master-1/dump.rdb
cp /backup/redis_backup_20240107.rdb /data/redis-master-2/dump.rdb
cp /backup/redis_backup_20240107.rdb /data/redis-master-3/dump.rdb

# 3. Start Redis nodes
docker-compose start redis-cluster

# 4. Verify cluster status
redis-cli -c -h redis-master-1 -p 6379 -a secure_redis_password cluster info
```

---

## Security Configuration

### TLS/SSL Configuration
```ini
# Enable TLS for Redis connections
tls-port 6380
tls-cert-file /etc/ssl/certs/redis.crt
tls-key-file /etc/ssl/private/redis.key
tls-ca-cert-file /etc/ssl/certs/ca.crt
tls-auth-clients optional
tls-replication yes
```

### Access Control
```bash
# Use ACLs for fine-grained access control
redis-cli -c -h redis-master-1 -p 6379 -a secure_redis_password acl setuser revenue_user on >secure_password +@all ~revenue:* ~session:* ~cache:*

# Test ACL user
redis-cli -c -h redis-master-1 -p 6379 -a secure_password -u revenue_user set test_key "test_value"
```

---

## Integration with Revenue Engine

### Cache Strategy Implementation
```python
class RevenueEngineCache:
    def __init__(self, redis_manager):
        self.redis = redis_manager

    def cache_market_data(self, symbol, data, ttl=300):
        """Cache market data with short TTL"""
        key = f"market:{symbol}"
        return self.redis.set_cache(key, json.dumps(data), ttl)

    def get_market_data(self, symbol):
        """Get cached market data"""
        key = f"market:{symbol}"
        data = self.redis.get_cache(key)
        return json.loads(data) if data else None

    def cache_revenue_metrics(self, user_id, metrics):
        """Cache user revenue metrics"""
        key = f"revenue:{user_id}"
        return self.redis.set_cache(key, json.dumps(metrics), 600)  # 10 min TTL

    def invalidate_user_cache(self, user_id):
        """Invalidate all user-related cache"""
        keys = [
            f"revenue:{user_id}",
            f"session:{user_id}",
            f"analytics:{user_id}"
        ]
        return sum(self.redis.delete_cache(key) for key in keys)

    def cache_with_tags(self, key, value, tags=[], ttl=3600):
        """Cache with tagging for bulk invalidation"""
        # Store the value
        self.redis.set_cache(key, json.dumps(value), ttl)

        # Add to tag sets for bulk operations
        for tag in tags:
            tag_key = f"tag:{tag}"
            self.redis.redis_cluster.sadd(tag_key, key)
            self.redis.redis_cluster.expire(tag_key, ttl)
```

---

**Redis Cluster Configuration Complete ✅**
**Agent-3 (Infrastructure & DevOps) - 2026-01-07**
**Status:** Ready for deployment and parallel validation testing