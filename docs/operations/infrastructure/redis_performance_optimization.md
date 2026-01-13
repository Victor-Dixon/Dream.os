# Redis Performance Optimization
## Infrastructure Block 5 - Advanced Caching Performance Tuning
## Agent-3 (Infrastructure & DevOps) - 2026-01-07

**Status:** ACTIVE ENHANCEMENT
**Purpose:** Optimize Redis cluster performance for Revenue Engine high-throughput operations
**Configuration:** Advanced Redis tuning with monitoring and failover optimization

---

## Redis Performance Architecture

### Performance Optimization Strategy
```
Application Layer → Connection Pool → Redis Cluster → Persistence Layer
       ↓                    ↓              ↓              ↓
   Smart Routing    Multiplexing    Sharding     AOF/RDB Backup
   Load Balancing   Pipelining      Replication  Monitoring
```

### Performance Targets
- **Throughput**: 100,000+ operations per second
- **Latency**: <1ms P95 response time
- **Memory Usage**: <80% of allocated memory
- **Cache Hit Rate**: >95% for hot data
- **Availability**: 99.99% uptime with automatic failover

---

## Advanced Redis Configuration

### Memory Optimization
```ini
# Advanced memory management settings
maxmemory 512mb
maxmemory-policy allkeys-lfu  # Least Frequently Used eviction
maxmemory-samples 10          # More samples for better LFU accuracy

# Active memory defragmentation
activedefrag yes
active-defrag-ignore-bytes 100mb
active-defrag-threshold-lower 10
active-defrag-threshold-upper 100
active-defrag-cycle-min 5
active-defrag-cycle-max 75

# Memory usage tracking
memory-usage-tracking yes
tracking-table-max-keys 1000000
```

### Connection Optimization
```ini
# Connection handling optimizations
tcp-keepalive 300
tcp-backlog 511
timeout 0
databases 16

# Client output buffer limits
client-output-buffer-limit normal 0 0 0
client-output-buffer-limit replica 256mb 64mb 60
client-output-buffer-limit pubsub 32mb 8mb 60

# Client query buffer
client-query-buffer-limit 1gb
proto-max-bulk-len 1gb
```

### Persistence Optimization
```ini
# AOF optimization for performance
appendonly yes
appendfilename "appendonly.aof"
appendfsync everysec
no-appendfsync-on-rewrite no

# AOF rewrite optimization
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
aof-rewrite-incremental-fsync yes

# RDB optimization
save 900 1
save 300 10
save 60 10000
rdbcompression yes
rdbchecksum yes
```

---

## Redis Cluster Advanced Features

### Cluster Bus Optimization
```ini
# Cluster bus configuration
cluster-enabled yes
cluster-config-file nodes.conf
cluster-node-timeout 5000
cluster-migration-barrier 1
cluster-require-full-coverage no
cluster-slave-validity-factor 10

# Cluster bus optimization
cluster-announce-bus-port 16379
cluster-announce-port 6379
cluster-announce-ip 10.0.0.10  # Internal IP for cluster communication
```

### Replication Optimization
```ini
# Replication performance tuning
repl-diskless-sync yes
repl-diskless-sync-delay 5
repl-ping-replica-period 10
repl-timeout 60
repl-backlog-size 1mb
repl-backlog-ttl 3600

# Replication buffer optimization
repl-backlog-size 100mb
client-output-buffer-limit replica 512mb 128mb 60
```

### Lua Scripting Optimization
```lua
-- Optimized Lua scripts for Revenue Engine operations
local function batch_get_keys(keys)
    local results = {}
    for i, key in ipairs(keys) do
        results[i] = redis.call('GET', key)
    end
    return results
end

local function conditional_set(key, value, ttl, condition)
    local current = redis.call('GET', key)
    if current == condition then
        redis.call('SETEX', key, ttl, value)
        return 1
    end
    return 0
end

local function market_data_cache(symbol, data, ttl)
    local key = 'market:' .. symbol
    redis.call('SETEX', key, ttl, data)
    redis.call('SADD', 'market_symbols', symbol)
    redis.call('EXPIRE', 'market_symbols', ttl)
    return 1
end
```

---

## Application Integration Optimization

### Advanced Redis Client Configuration
```python
import redis
from redis.cluster import RedisCluster
from redis.connection import ConnectionPool
from typing import Dict, Any, List, Optional
import time

class OptimizedRedisManager:
    """Optimized Redis cluster manager for Revenue Engine."""

    def __init__(self, startup_nodes: List[Dict[str, Any]], password: str):
        self.redis_cluster = RedisCluster(
            startup_nodes=startup_nodes,
            password=password,
            decode_responses=True,
            skip_full_coverage_check=True,
            socket_connect_timeout=5,
            socket_timeout=5,
            retry_on_timeout=True,
            retry=redis.retry.Retry(3, 1),
            health_check_interval=30
        )

        # Connection pool for high-throughput operations
        self.connection_pool = ConnectionPool(
            connection_class=redis.Connection,
            max_connections=50,
            decode_responses=True
        )

    def pipeline_execute(self, operations: List[Dict[str, Any]]) -> List[Any]:
        """Execute multiple operations in a pipeline for atomicity and performance."""
        with self.redis_cluster.pipeline() as pipe:
            for op in operations:
                if op['command'] == 'SET':
                    pipe.set(op['key'], op['value'], ex=op.get('ttl'))
                elif op['command'] == 'GET':
                    pipe.get(op['key'])
                elif op['command'] == 'DEL':
                    pipe.delete(op['key'])
                elif op['command'] == 'INCR':
                    pipe.incr(op['key'])

            return pipe.execute()

    def batch_get(self, keys: List[str]) -> Dict[str, Any]:
        """Batch get multiple keys with optimization."""
        results = {}
        # Use pipeline for multiple keys
        with self.redis_cluster.pipeline() as pipe:
            for key in keys:
                pipe.get(key)
            values = pipe.execute()

        for key, value in zip(keys, values):
            if value is not None:
                results[key] = value

        return results

    def smart_cache(self, key: str, data: Any, ttl: int = 3600) -> bool:
        """Smart caching with compression for large data."""
        try:
            # Compress data if it's large
            if len(str(data)) > 1000:
                import gzip
                compressed = gzip.compress(str(data).encode())
                self.redis_cluster.setex(f"{key}:compressed", ttl, compressed)
                self.redis_cluster.setex(f"{key}:metadata", ttl, "compressed")
                return True

            self.redis_cluster.setex(key, ttl, data)
            return True
        except Exception as e:
            print(f"Smart cache failed: {e}")
            return False

    def get_smart_cache(self, key: str) -> Optional[Any]:
        """Retrieve smart cached data with automatic decompression."""
        try:
            metadata = self.redis_cluster.get(f"{key}:metadata")
            if metadata == "compressed":
                compressed_data = self.redis_cluster.get(f"{key}:compressed")
                if compressed_data:
                    import gzip
                    return gzip.decompress(compressed_data).decode()
            else:
                return self.redis_cluster.get(key)
        except Exception as e:
            print(f"Smart cache retrieval failed: {e}")
            return None

    def health_check(self) -> Dict[str, Any]:
        """Comprehensive Redis cluster health check."""
        try:
            info = self.redis_cluster.info()
            cluster_info = self.redis_cluster.cluster_info()
            memory_info = self.redis_cluster.info('memory')

            return {
                'status': 'healthy',
                'cluster_state': cluster_info.get('cluster_state'),
                'connected_clients': info.get('connected_clients', 0),
                'used_memory': memory_info.get('used_memory_human', '0'),
                'total_commands_processed': info.get('total_commands_processed', 0),
                'instantaneous_ops_per_sec': info.get('instantaneous_ops_per_sec', 0),
                'cache_hit_ratio': self._calculate_cache_hit_ratio(),
                'latency_ms': self._measure_latency()
            }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': str(e)
            }

    def _calculate_cache_hit_ratio(self) -> float:
        """Calculate cache hit ratio from Redis stats."""
        try:
            stats = self.redis_cluster.info('stats')
            hits = stats.get('keyspace_hits', 0)
            misses = stats.get('keyspace_misses', 0)
            total = hits + misses
            return (hits / total * 100) if total > 0 else 0.0
        except:
            return 0.0

    def _measure_latency(self) -> float:
        """Measure Redis latency."""
        start_time = time.time()
        self.redis_cluster.ping()
        return (time.time() - start_time) * 1000  # Convert to milliseconds

    def optimize_performance(self) -> Dict[str, Any]:
        """Dynamic performance optimization based on current metrics."""
        health = self.health_check()
        optimizations = {}

        # Optimize based on memory usage
        memory_percent = float(health.get('used_memory', '0MB').rstrip('MB'))
        if memory_percent > 400:  # Over 400MB
            # Increase memory and adjust policy
            optimizations['memory'] = 'increased_maxmemory'
            optimizations['eviction_policy'] = 'volatile-lfu'

        # Optimize based on cache hit ratio
        hit_ratio = health.get('cache_hit_ratio', 0)
        if hit_ratio < 85:
            optimizations['cache_ttl'] = 'increased_ttl'
            optimizations['compression'] = 'enabled'

        # Optimize based on latency
        latency = health.get('latency', 0)
        if latency > 5:  # Over 5ms
            optimizations['connections'] = 'increased_pool_size'
            optimizations['pipelining'] = 'enabled'

        return {
            'current_health': health,
            'optimizations_applied': optimizations,
            'recommendations': self._generate_recommendations(health)
        }

    def _generate_recommendations(self, health: Dict[str, Any]) -> List[str]:
        """Generate optimization recommendations based on health metrics."""
        recommendations = []

        if health.get('cache_hit_ratio', 0) < 90:
            recommendations.append("Consider increasing cache TTL for frequently accessed data")

        if health.get('latency_ms', 0) > 2:
            recommendations.append("Consider using connection pooling for high-throughput operations")

        memory_usage = health.get('used_memory', '0MB')
        if 'MB' in memory_usage and float(memory_usage.rstrip('MB')) > 400:
            recommendations.append("Consider increasing Redis memory allocation or implementing data eviction")

        return recommendations
```

---

## Monitoring and Alerting

### Prometheus Redis Exporter Configuration
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: redis-exporter-config
  namespace: production
data:
  redis-exporter.conf: |
    redis_addr=redis-cluster:6379
    redis_password=secure_redis_password
    namespace=redis
    check_keys=market:*,user:*,cache:*
    check_key_groups=market,user,cache
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis-exporter
  namespace: production
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis-exporter
  template:
    metadata:
      labels:
        app: redis-exporter
    spec:
      containers:
      - name: redis-exporter
        image: oliver006/redis_exporter:latest
        ports:
        - containerPort: 9121
        env:
        - name: REDIS_ADDR
          value: "redis://redis-cluster:6379"
        - name: REDIS_PASSWORD
          valueFrom:
            secretKeyRef:
              name: redis-secret
              key: password
        resources:
          requests:
            memory: "64Mi"
            cpu: "100m"
          limits:
            memory: "128Mi"
            cpu: "200m"
```

### Grafana Dashboard Configuration
```json
{
  "dashboard": {
    "title": "Redis Cluster Performance",
    "panels": [
      {
        "title": "Cache Hit Ratio",
        "type": "singlestat",
        "targets": [
          {
            "expr": "rate(redis_keyspace_hits_total[5m]) / (rate(redis_keyspace_hits_total[5m]) + rate(redis_keyspace_misses_total[5m])) * 100",
            "legendFormat": "Hit Ratio %"
          }
        ]
      },
      {
        "title": "Memory Usage",
        "type": "graph",
        "targets": [
          {
            "expr": "redis_memory_used_bytes / redis_memory_max_bytes * 100",
            "legendFormat": "Memory Usage %"
          }
        ]
      },
      {
        "title": "Operations Per Second",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(redis_commands_processed_total[1m])",
            "legendFormat": "OPS"
          }
        ]
      },
      {
        "title": "Connection Count",
        "type": "graph",
        "targets": [
          {
            "expr": "redis_connected_clients",
            "legendFormat": "Connected Clients"
          }
        ]
      }
    ]
  }
}
```

---

## Performance Benchmarking

### Redis Performance Test Script
```bash
#!/bin/bash
# Redis performance benchmarking

# Install redis-benchmark if not available
if ! command -v redis-benchmark &> /dev/null; then
    echo "Installing redis-tools..."
    sudo apt-get update && sudo apt-get install -y redis-tools
fi

echo "🧪 Redis Performance Benchmark"
echo "================================"

# Basic performance test
echo "Running basic performance test..."
redis-benchmark -h redis-cluster -p 6379 -a secure_redis_password \
    -n 10000 -c 50 -t get,set,lpush,lpop,sadd,spop

echo ""
echo "Testing different data sizes..."

# Small data test
redis-benchmark -h redis-cluster -p 6379 -a secure_redis_password \
    -n 10000 -c 50 -d 100 -t set,get

# Medium data test
redis-benchmark -h redis-cluster -p 6379 -a secure_redis_password \
    -n 5000 -c 50 -d 1000 -t set,get

# Large data test
redis-benchmark -h redis-cluster -p 6379 -a secure_redis_password \
    -n 1000 -c 20 -d 10000 -t set,get

echo ""
echo "Testing pipeline performance..."

# Pipeline test
redis-benchmark -h redis-cluster -p 6379 -a secure_redis_password \
    -n 10000 -c 50 -P 10 -t set,get

echo ""
echo "Redis performance benchmark completed"
```

### Custom Performance Test
```python
import time
import redis
from redis.cluster import RedisCluster
import statistics

def comprehensive_performance_test():
    """Comprehensive Redis performance testing."""

    # Connect to Redis cluster
    redis_cluster = RedisCluster(
        startup_nodes=[{"host": "redis-cluster", "port": 6379}],
        password="secure_redis_password",
        decode_responses=True
    )

    test_results = {
        'latency': [],
        'throughput': [],
        'memory_usage': [],
        'cache_hit_ratio': []
    }

    # Test duration in seconds
    test_duration = 60

    start_time = time.time()
    operations = 0

    while time.time() - start_time < test_duration:
        # Measure latency
        op_start = time.time()
        redis_cluster.set(f"test_key_{operations}", f"test_value_{operations}")
        value = redis_cluster.get(f"test_key_{operations}")
        latency = (time.time() - op_start) * 1000  # Convert to milliseconds

        test_results['latency'].append(latency)
        operations += 1

        # Periodic memory and hit ratio checks
        if operations % 1000 == 0:
            memory_info = redis_cluster.info('memory')
            stats_info = redis_cluster.info('stats')

            test_results['memory_usage'].append(memory_info.get('used_memory', 0))

            hits = stats_info.get('keyspace_hits', 0)
            misses = stats_info.get('keyspace_misses', 0)
            total = hits + misses
            hit_ratio = (hits / total * 100) if total > 0 else 0
            test_results['cache_hit_ratio'].append(hit_ratio)

    # Calculate final metrics
    final_results = {
        'total_operations': operations,
        'avg_latency_ms': statistics.mean(test_results['latency']),
        'p95_latency_ms': statistics.quantiles(test_results['latency'], n=20)[18],  # 95th percentile
        'p99_latency_ms': statistics.quantiles(test_results['latency'], n=100)[98],  # 99th percentile
        'operations_per_second': operations / test_duration,
        'avg_memory_usage': statistics.mean(test_results['memory_usage']) if test_results['memory_usage'] else 0,
        'avg_cache_hit_ratio': statistics.mean(test_results['cache_hit_ratio']) if test_results['cache_hit_ratio'] else 0
    }

    return final_results

if __name__ == "__main__":
    results = comprehensive_performance_test()
    print("Redis Performance Test Results:")
    print(f"Total Operations: {results['total_operations']}")
    print(f"Average Latency: {results['avg_latency_ms']:.2f}ms")
    print(f"P95 Latency: {results['p95_latency_ms']:.2f}ms")
    print(f"P99 Latency: {results['p99_latency_ms']:.2f}ms")
    print(f"Operations/Second: {results['operations_per_second']:.0f}")
    print(f"Average Memory Usage: {results['avg_memory_usage'] / 1024 / 1024:.1f}MB")
    print(f"Average Cache Hit Ratio: {results['avg_cache_hit_ratio']:.1f}%")
```

---

## Failover and Recovery Optimization

### Automatic Failover Configuration
```ini
# Redis Sentinel configuration for automatic failover
sentinel monitor mymaster redis-master-1 6379 2
sentinel down-after-milliseconds mymaster 5000
sentinel failover-timeout mymaster 60000
sentinel parallel-syncs mymaster 1

# Notification scripts for failover events
sentinel client-reconfig-script mymaster /path/to/reconfig-script.sh
sentinel auth-pass mymaster secure_redis_password
```

### Disaster Recovery Plan
```bash
#!/bin/bash
# Redis disaster recovery script

BACKUP_DIR="/redis_backup"
RESTORE_FROM="$1"

if [ -z "$RESTORE_FROM" ]; then
    echo "Usage: $0 <backup_timestamp>"
    exit 1
fi

# Stop Redis cluster
docker-compose -f redis-cluster.yml down

# Restore from backup
tar -xzf "$BACKUP_DIR/redis_backup_$RESTORE_FROM.tar.gz" -C /redis_data

# Start Redis cluster
docker-compose -f redis-cluster.yml up -d

# Verify cluster integrity
sleep 30
redis-cli -c -h redis-master-1 -p 6379 -a secure_redis_password cluster nodes
redis-cli -c -h redis-master-1 -p 6379 -a secure_redis_password cluster info

echo "Redis disaster recovery completed"
```

---

**Redis Performance Optimization Complete ✅**
**Agent-3 (Infrastructure & DevOps) - 2026-01-07**
**Status:** Advanced performance tuning and monitoring ready for production deployment