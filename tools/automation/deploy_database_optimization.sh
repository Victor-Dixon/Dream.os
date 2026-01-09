#!/bin/bash
# Database Optimization Deployment Script
# Infrastructure Block 5 - PostgreSQL + Redis + PgBouncer
# Agent-3 (Infrastructure & DevOps) - 2026-01-07

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."

    # Check if Docker is available
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed or not in PATH"
        exit 1
    fi

    # Check if docker-compose is available
    if ! command -v docker-compose &> /dev/null; then
        log_error "docker-compose is not installed or not in PATH"
        exit 1
    fi

    # Check if required ports are available
    local ports=(5432 6432 6379 6380 6381)
    for port in "${ports[@]}"; do
        if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
            log_error "Port $port is already in use"
            exit 1
        fi
    done

    log_success "Prerequisites check passed"
}

# Deploy PostgreSQL replication
deploy_postgresql() {
    log_info "Deploying PostgreSQL replication cluster..."

    # Create PostgreSQL configuration directory
    mkdir -p "$PROJECT_ROOT/infrastructure/postgresql"

    # Generate PostgreSQL configuration files
    cat > "$PROJECT_ROOT/infrastructure/postgresql/postgresql.conf" << 'EOF'
# PostgreSQL configuration for replication
listen_addresses = '*'
max_connections = 200
shared_preload_libraries = 'pg_stat_statements'
wal_level = replica
max_wal_senders = 10
max_replication_slots = 10
wal_keep_size = 1GB
hot_standby = on
EOF

    cat > "$PROJECT_ROOT/infrastructure/postgresql/pg_hba.conf" << 'EOF'
# PostgreSQL client authentication configuration
local   all             postgres                                trust
local   all             all                                     md5
host    all             all             127.0.0.1/32            md5
host    all             all             ::1/128                 md5
host    replication     replicator      172.20.0.0/16         md5
host    revenue_engine   revenue_user    172.20.0.0/16         md5
EOF

    # Create docker-compose for PostgreSQL cluster
    cat > "$PROJECT_ROOT/infrastructure/postgresql/docker-compose.yml" << 'EOF'
version: '3.8'
services:
  postgres-primary:
    image: postgres:15
    environment:
      POSTGRES_DB: revenue_engine
      POSTGRES_USER: revenue_user
      POSTGRES_PASSWORD: secure_revenue_password
      POSTGRES_INITDB_ARGS: "--encoding=UTF-8"
    volumes:
      - ./postgresql.conf:/etc/postgresql/postgresql.conf
      - ./pg_hba.conf:/etc/postgresql/pg_hba.conf
      - postgres_primary_data:/var/lib/postgresql/data
      - ./init-replication.sh:/docker-entrypoint-initdb.d/init-replication.sh
    command: postgres -c config_file=/etc/postgresql/postgresql.conf
    ports:
      - "5432:5432"
    networks:
      - database_network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U revenue_user -d revenue_engine"]
      interval: 30s
      timeout: 10s
      retries: 3

  postgres-replica-1:
    image: postgres:15
    environment:
      POSTGRES_DB: revenue_engine
      POSTGRES_USER: revenue_user
      POSTGRES_PASSWORD: secure_revenue_password
    volumes:
      - ./postgresql.conf:/etc/postgresql/postgresql.conf
      - ./pg_hba.conf:/etc/postgresql/pg_hba.conf
      - postgres_replica1_data:/var/lib/postgresql/data
      - ./init-replica.sh:/docker-entrypoint-initdb.d/init-replica.sh
    command: postgres -c config_file=/etc/postgresql/postgresql.conf
    ports:
      - "5433:5432"
    depends_on:
      postgres-primary:
        condition: service_healthy
    networks:
      - database_network

  postgres-replica-2:
    image: postgres:15
    environment:
      POSTGRES_DB: revenue_engine
      POSTGRES_USER: revenue_user
      POSTGRES_PASSWORD: secure_revenue_password
    volumes:
      - ./postgresql.conf:/etc/postgresql/postgresql.conf
      - ./pg_hba.conf:/etc/postgresql/pg_hba.conf
      - postgres_replica2_data:/var/lib/postgresql/data
      - ./init-replica.sh:/docker-entrypoint-initdb.d/init-replica.sh
    command: postgres -c config_file=/etc/postgresql/postgresql.conf
    ports:
      - "5434:5432"
    depends_on:
      postgres-primary:
        condition: service_healthy
    networks:
      - database_network

volumes:
  postgres_primary_data:
  postgres_replica1_data:
  postgres_replica2_data:

networks:
  database_network:
    driver: bridge
EOF

    # Create replication initialization scripts
    cat > "$PROJECT_ROOT/infrastructure/postgresql/init-replication.sh" << 'EOF'
#!/bin/bash
set -e

# Create replication user
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
CREATE USER replicator WITH REPLICATION ENCRYPTED PASSWORD 'secure_replicator_password';
GRANT CONNECT ON DATABASE revenue_engine TO replicator;
EOSQL

echo "Replication user created"
EOF

    cat > "$PROJECT_ROOT/infrastructure/postgresql/init-replica.sh" << 'EOF'
#!/bin/bash
set -e

# Wait for primary to be ready
until pg_isready -h postgres-primary -p 5432 -U revenue_user; do
  echo "Waiting for primary database..."
  sleep 2
done

# Remove existing data directory if it exists
if [ -d "$PGDATA" ]; then
  rm -rf "$PGDATA"/*
fi

# Perform base backup from primary
pg_basebackup -h postgres-primary -p 5432 -U replicator -D "$PGDATA" -Fp -Xs -P -R

echo "Replica initialized from primary"
EOF

    # Make scripts executable
    chmod +x "$PROJECT_ROOT/infrastructure/postgresql/init-replication.sh"
    chmod +x "$PROJECT_ROOT/infrastructure/postgresql/init-replica.sh"

    # Start PostgreSQL cluster
    cd "$PROJECT_ROOT/infrastructure/postgresql"
    docker-compose up -d

    # Wait for cluster to be ready
    log_info "Waiting for PostgreSQL cluster to initialize..."
    sleep 30

    # Verify replication
    if docker-compose exec postgres-primary pg_isready -U revenue_user -d revenue_engine >/dev/null 2>&1; then
        log_success "PostgreSQL primary is ready"
    else
        log_error "PostgreSQL primary failed to start"
        exit 1
    fi

    log_success "PostgreSQL replication cluster deployed"
}

# Deploy Redis cluster
deploy_redis() {
    log_info "Deploying Redis cluster..."

    # Create Redis configuration directory
    mkdir -p "$PROJECT_ROOT/infrastructure/redis"

    # Create Redis cluster configuration
    cat > "$PROJECT_ROOT/infrastructure/redis/redis.conf" << 'EOF'
# Redis cluster configuration
cluster-enabled yes
cluster-config-file nodes.conf
cluster-node-timeout 5000
cluster-migration-barrier 1
cluster-require-full-coverage no

bind 0.0.0.0
port 6379
timeout 0
tcp-keepalive 300
tcp-backlog 511

maxmemory 256mb
maxmemory-policy allkeys-lru
maxmemory-samples 5

save 900 1
save 300 10
save 60 10000
appendonly yes
appendfilename "appendonly.aof"
appendfsync everysec

requirepass secure_redis_password
masterauth secure_redis_password

loglevel notice
logfile /var/log/redis/redis.log

rename-command FLUSHDB ""
rename-command FLUSHALL ""
rename-command SHUTDOWN SHUTDOWN_REDIS
EOF

    # Create docker-compose for Redis cluster
    cat > "$PROJECT_ROOT/infrastructure/redis/docker-compose.yml" << 'EOF'
version: '3.8'
services:
  redis-master-1:
    image: redis:7-alpine
    command: redis-server /etc/redis/redis.conf
    volumes:
      - ./redis.conf:/etc/redis/redis.conf
      - redis_master1_data:/data
    ports:
      - "6379:6379"
    networks:
      - redis_network
    healthcheck:
      test: ["CMD", "redis-cli", "--raw", "incr", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3

  redis-master-2:
    image: redis:7-alpine
    command: redis-server /etc/redis/redis.conf
    volumes:
      - ./redis.conf:/etc/redis/redis.conf
      - redis_master2_data:/data
    ports:
      - "6380:6379"
    networks:
      - redis_network
    healthcheck:
      test: ["CMD", "redis-cli", "-p", "6379", "--raw", "incr", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3

  redis-master-3:
    image: redis:7-alpine
    command: redis-server /etc/redis/redis.conf
    volumes:
      - ./redis.conf:/etc/redis/redis.conf
      - redis_master3_data:/data
    ports:
      - "6381:6379"
    networks:
      - redis_network
    healthcheck:
      test: ["CMD", "redis-cli", "-p", "6379", "--raw", "incr", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3

  redis-replica-1:
    image: redis:7-alpine
    command: redis-server /etc/redis/redis.conf
    volumes:
      - ./redis.conf:/etc/redis/redis.conf
      - redis_replica1_data:/data
    ports:
      - "6382:6379"
    depends_on:
      redis-master-1:
        condition: service_healthy
    networks:
      - redis_network

  redis-replica-2:
    image: redis:7-alpine
    command: redis-server /etc/redis/redis.conf
    volumes:
      - ./redis.conf:/etc/redis/redis.conf
      - redis_replica2_data:/data
    ports:
      - "6383:6379"
    depends_on:
      redis-master-2:
        condition: service_healthy
    networks:
      - redis_network

  redis-replica-3:
    image: redis:7-alpine
    command: redis-server /etc/redis/redis.conf
    volumes:
      - ./redis.conf:/etc/redis/redis.conf
      - redis_replica3_data:/data
    ports:
      - "6384:6379"
    depends_on:
      redis-master-3:
        condition: service_healthy
    networks:
      - redis_network

volumes:
  redis_master1_data:
  redis_master2_data:
  redis_master3_data:
  redis_replica1_data:
  redis_replica2_data:
  redis_replica3_data:

networks:
  redis_network:
    driver: bridge
EOF

    # Create Redis cluster setup script
    cat > "$PROJECT_ROOT/infrastructure/redis/create-cluster.sh" << 'EOF'
#!/bin/bash
set -e

echo "Waiting for Redis nodes to start..."
sleep 10

# Create Redis cluster
echo "Creating Redis cluster..."
redis-cli --cluster create \
    redis-master-1:6379 \
    redis-master-2:6380 \
    redis-master-3:6381 \
    redis-replica-1:6382 \
    redis-replica-2:6383 \
    redis-replica-3:6384 \
    --cluster-replicas 1 \
    --cluster-yes

echo "Redis cluster created successfully"

# Verify cluster
echo "Verifying cluster status..."
redis-cli -c -h redis-master-1 -p 6379 -a secure_redis_password cluster info
redis-cli -c -h redis-master-1 -p 6379 -a secure_redis_password cluster nodes

echo "Redis cluster verification complete"
EOF

    # Make cluster script executable
    chmod +x "$PROJECT_ROOT/infrastructure/redis/create-cluster.sh"

    # Start Redis nodes
    cd "$PROJECT_ROOT/infrastructure/redis"
    docker-compose up -d

    # Wait for nodes to be ready
    log_info "Waiting for Redis nodes to initialize..."
    sleep 15

    # Create cluster
    ./create-cluster.sh

    log_success "Redis cluster deployed"
}

# Deploy PgBouncer
deploy_pgbouncer() {
    log_info "Deploying PgBouncer connection pooling..."

    # Create PgBouncer configuration directory
    mkdir -p "$PROJECT_ROOT/infrastructure/pgbouncer"

    # Create PgBouncer configuration
    cat > "$PROJECT_ROOT/infrastructure/pgbouncer/pgbouncer.ini" << 'EOF'
[databases]
revenue_engine = host=host.docker.internal port=5432 dbname=revenue_engine
revenue_engine_replica1 = host=host.docker.internal port=5433 dbname=revenue_engine
revenue_engine_replica2 = host=host.docker.internal port=5434 dbname=revenue_engine

[pgbouncer]
listen_addr = 0.0.0.0
listen_port = 6432
auth_type = md5
auth_file = /etc/pgbouncer/userlist.txt
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 20
min_pool_size = 5
reserve_pool_size = 5
server_reset_query = DISCARD ALL
server_check_delay = 30
server_lifetime = 3600
server_idle_timeout = 600
logfile = /var/log/pgbouncer/pgbouncer.log
pidfile = /var/run/pgbouncer/pgbouncer.pid
admin_users = pgbouncer_admin
stats_users = monitor_user
EOF

    # Create user authentication file
    cat > "$PROJECT_ROOT/infrastructure/pgbouncer/userlist.txt" << 'EOF'
"pgbouncer_admin" "secure_admin_password"
"monitor_user" "secure_monitor_password"
"revenue_user" "secure_revenue_password"
EOF

    # Create docker-compose for PgBouncer
    cat > "$PROJECT_ROOT/infrastructure/pgbouncer/docker-compose.yml" << 'EOF'
version: '3.8'
services:
  pgbouncer:
    image: edoburu/pgbouncer:latest
    volumes:
      - ./pgbouncer.ini:/etc/pgbouncer/pgbouncer.ini
      - ./userlist.txt:/etc/pgbouncer/userlist.txt
    ports:
      - "6432:6432"
    networks:
      - database_network
    depends_on:
      - postgres-primary
    healthcheck:
      test: ["CMD-SHELL", "psql -h localhost -p 6432 -U monitor_user -d pgbouncer -c 'SHOW VERSION;'"]
      interval: 30s
      timeout: 10s
      retries: 3

networks:
  database_network:
    external: true
    name: postgresql_database_network
EOF

    # Start PgBouncer
    cd "$PROJECT_ROOT/infrastructure/pgbouncer"
    docker-compose up -d

    # Wait for PgBouncer to be ready
    log_info "Waiting for PgBouncer to initialize..."
    sleep 10

    # Verify PgBouncer
    if docker-compose exec pgbouncer psql -h localhost -p 6432 -U monitor_user -d pgbouncer -c "SHOW VERSION;" >/dev/null 2>&1; then
        log_success "PgBouncer is ready"
    else
        log_error "PgBouncer failed to start"
        exit 1
    fi

    log_success "PgBouncer connection pooling deployed"
}

# Run health checks
run_health_checks() {
    log_info "Running infrastructure health checks..."

    # PostgreSQL health check
    if docker-compose -f "$PROJECT_ROOT/infrastructure/postgresql/docker-compose.yml" exec -T postgres-primary pg_isready -U revenue_user -d revenue_engine >/dev/null 2>&1; then
        log_success "PostgreSQL cluster is healthy"
    else
        log_warning "PostgreSQL cluster health check failed"
    fi

    # Redis health check
    if docker-compose -f "$PROJECT_ROOT/infrastructure/redis/docker-compose.yml" exec -T redis-master-1 redis-cli ping | grep -q "PONG"; then
        log_success "Redis cluster is healthy"
    else
        log_warning "Redis cluster health check failed"
    fi

    # PgBouncer health check
    if docker-compose -f "$PROJECT_ROOT/infrastructure/pgbouncer/docker-compose.yml" exec -T pgbouncer psql -h localhost -p 6432 -U monitor_user -d pgbouncer -c "SHOW POOLS;" >/dev/null 2>&1; then
        log_success "PgBouncer is healthy"
    else
        log_warning "PgBouncer health check failed"
    fi

    log_success "Infrastructure health checks completed"
}

# Main deployment function
main() {
    log_info "Starting Database Optimization Deployment (Infrastructure Block 5)"
    log_info "Components: PostgreSQL Replication + Redis Cluster + PgBouncer"

    check_prerequisites
    deploy_postgresql
    deploy_redis
    deploy_pgbouncer
    run_health_checks

    log_success "Database Optimization Deployment completed successfully"
    log_info "Infrastructure Block 5 ready for validation testing"

    echo ""
    echo "🎯 Deployment Summary:"
    echo "   PostgreSQL Primary: localhost:5432"
    echo "   PostgreSQL Replicas: localhost:5433, localhost:5434"
    echo "   Redis Cluster: localhost:6379,6380,6381 (masters)"
    echo "   PgBouncer: localhost:6432"
    echo ""
    echo "🔧 Next Steps:"
    echo "   1. Run parallel validation testing with Agent-1"
    echo "   2. Monitor performance metrics"
    echo "   3. Execute production deployment procedures"
    echo ""
}

# Run main function
main "$@"