# Kong API Gateway Configuration
## Infrastructure Block 4 - API Management & Routing
## Agent-3 (Infrastructure & DevOps) - 2026-01-07

**Status:** ACTIVE IMPLEMENTATION
**Purpose:** Deploy Kong API Gateway for Revenue Engine API management and security
**Configuration:** Kong Gateway 3.4+ with plugins for authentication, rate limiting, and monitoring

---

## Kong Architecture

### API Gateway Components
```
Kong Gateway:
├── Admin API (8001) - Configuration management
├── Proxy (8000/8443) - API traffic proxy
├── Manager (8002) - Web UI (optional)
└── Developer Portal (8003) - API documentation (optional)

Database:
├── PostgreSQL - Configuration storage
└── Redis - Rate limiting & caching
```

### Traffic Flow
```
Client → Kong Gateway → Authentication → Rate Limiting → Upstream Service
                     ↓
            Request Transformation → Response Caching → Logging
```

---

## Kong Installation & Configuration

### Kong Installation Script
```bash
#!/bin/bash
# Kong API Gateway installation

# Update system
sudo apt-get update
sudo apt-get install -y postgresql postgresql-contrib redis-server

# Install Kong
wget -qO - 'https://packages.konghq.com/public/kong-repositories-ce/gpg.24E2982F779C9F6A.key' | sudo apt-key add -
echo "deb https://packages.konghq.com/public/kong-repositories-ce/deb/ubuntu focal main" | sudo tee /etc/apt/sources.list.d/kong-community.list
sudo apt-get update
sudo apt-get install -y kong

# Configure PostgreSQL for Kong
sudo -u postgres createdb kong
sudo -u postgres createuser kong
sudo -u postgres psql -c "ALTER USER kong WITH PASSWORD 'kong_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE kong TO kong;"

# Run Kong database migrations
kong migrations bootstrap -c /etc/kong/kong.conf

# Configure Kong
sudo tee /etc/kong/kong.conf > /dev/null <<EOF
database = postgres
pg_host = 127.0.0.1
pg_port = 5432
pg_user = kong
pg_password = kong_password
pg_database = kong

proxy_listen = 0.0.0.0:8000 reuseport backlog=16384, 0.0.0.0:8443 http2 ssl reuseport backlog=16384
admin_listen = 127.0.0.1:8001 reuseport
admin_gui_listen = 127.0.0.1:8002

ssl_cert = /etc/kong/ssl/revenue-engine.crt
ssl_cert_key = /etc/kong/ssl/revenue-engine.key

lua_ssl_verify_depth = 3
client_ssl = on

log_level = notice
plugins = bundled,cors,key-auth,rate-limiting,request-transformer,response-transformer,cache,correlation-id,http-log

nginx_worker_processes = auto
nginx_worker_connections = 16384
EOF

# Start Kong
sudo systemctl enable kong
sudo systemctl start kong

echo "Kong API Gateway installed and configured"
```

### Kong Declarative Configuration
```yaml
# kong.yaml - Declarative configuration
_format_version: "3.0"

services:
  - name: revenue-engine-api
    url: http://revenue-engine-service.production.svc.cluster.local:8080
    routes:
      - name: revenue-api-route
        paths:
          - /api/v1/revenue
        methods:
          - GET
          - POST
          - PUT
          - DELETE
        plugins:
          - name: key-auth
            config:
              key_names:
                - apikey
              hide_credentials: true
          - name: rate-limiting
            config:
              minute: 1000
              policy: redis
              redis_host: redis-cluster
              redis_port: 6379
              redis_password: secure_redis_password
          - name: cors
            config:
              origins:
                - https://tradingrobotplug.com
                - https://www.tradingrobotplug.com
              methods:
                - GET
                - POST
                - PUT
                - DELETE
              headers:
                - Accept
                - Accept-Version
                - Content-Length
                - Content-MD5
                - Content-Type
                - Date
                - X-Auth-Token
              credentials: true
          - name: request-transformer
            config:
              add:
                headers:
                  X-API-Version: v1
                  X-Request-ID: $(uuid)
          - name: correlation-id
            config:
              header_name: X-Correlation-ID
              generator: uuid

  - name: revenue-engine-admin
    url: http://revenue-engine-admin.production.svc.cluster.local:8080
    routes:
      - name: admin-api-route
        paths:
          - /api/v1/admin
        methods:
          - GET
          - POST
          - PUT
          - DELETE
        plugins:
          - name: key-auth
          - name: rate-limiting
            config:
              minute: 100
              policy: redis

consumers:
  - username: revenue-engine-user
    keyauth_credentials:
      - key: secure_api_key_here

  - username: admin-user
    keyauth_credentials:
      - key: admin_api_key_here
```

---

## Authentication & Authorization

### Key Authentication Plugin
```bash
# Create API consumer
curl -X POST http://localhost:8001/consumers \
  -d "username=revenue-engine-user"

# Add API key
curl -X POST http://localhost:8001/consumers/revenue-engine-user/key-auth \
  -d "key=secure_api_key_here"

# Configure key-auth plugin on service
curl -X POST http://localhost:8001/services/revenue-engine-api/plugins \
  -d "name=key-auth" \
  -d "config.key_names=apikey" \
  -d "config.hide_credentials=true"
```

### JWT Authentication Plugin
```bash
# Install JWT plugin
curl -X POST http://localhost:8001/services/revenue-engine-api/plugins \
  -d "name=jwt" \
  -d "config.secret_is_base64=false" \
  -d "config.run_on_preflight=true"
```

### OAuth 2.0 Plugin
```bash
# Configure OAuth 2.0 plugin
curl -X POST http://localhost:8001/services/revenue-engine-api/plugins \
  -d "name=oauth2" \
  -d "config.scopes=email,profile" \
  -d "config.mandatory_scope=true" \
  -d "config.provision_key=provision_key_here" \
  -d "config.token_expiration=7200" \
  -d "config.enable_authorization_code=true" \
  -d "config.enable_client_credentials=true"
```

---

## Rate Limiting & Traffic Control

### Rate Limiting Plugin
```bash
# Configure rate limiting
curl -X POST http://localhost:8001/services/revenue-engine-api/plugins \
  -d "name=rate-limiting" \
  -d "config.minute=1000" \
  -d "config.hour=10000" \
  -d "config.day=50000" \
  -d "config.policy=redis" \
  -d "config.redis_host=redis-cluster" \
  -d "config.redis_port=6379" \
  -d "config.redis_password=secure_redis_password" \
  -d "config.redis_database=1"
```

### Request Size Limiting
```bash
# Configure request size limit
curl -X POST http://localhost:8001/services/revenue-engine-api/plugins \
  -d "name=request-size-limiting" \
  -d "config.allowed_payload_size=10485760" \
  -d "config.size_unit=bytes"
```

### Bot Detection
```bash
# Configure bot detection
curl -X POST http://localhost:8001/services/revenue-engine-api/plugins \
  -d "name=bot-detection" \
  -d "config.whitelist=1.2.3.4,5.6.7.8" \
  -d "config.blacklist=9.10.11.12"
```

---

## Caching & Performance

### Proxy Caching Plugin
```bash
# Configure response caching
curl -X POST http://localhost:8001/services/revenue-engine-api/plugins \
  -d "name=proxy-cache" \
  -d "config.response_code=200" \
  -d "config.request_method=GET" \
  -d "config.content_type=application/json" \
  -d "config.cache_ttl=300" \
  -d "config.strategy=memory"
```

### Upstream Health Checks
```bash
# Configure upstream health checks
curl -X POST http://localhost:8001/upstreams \
  -d "name=revenue-engine-upstream" \
  -d "healthchecks.active.healthy.interval=10" \
  -d "healthchecks.active.healthy.successes=2" \
  -d "healthchecks.active.unhealthy.interval=5" \
  -d "healthchecks.active.unhealthy.tcp_failures=3" \
  -d "healthchecks.active.unhealthy.timeouts=3" \
  -d "healthchecks.active.unhealthy.http_failures=3"

# Add targets
curl -X POST http://localhost:8001/upstreams/revenue-engine-upstream/targets \
  -d "target=revenue-engine-service.production.svc.cluster.local:8080" \
  -d "weight=100"
```

---

## Monitoring & Observability

### HTTP Logging Plugin
```bash
# Configure HTTP logging
curl -X POST http://localhost:8001/services/revenue-engine-api/plugins \
  -d "name=http-log" \
  -d "config.http_endpoint=https://logging-service.tradingrobotplug.com/logs" \
  -d "config.method=POST" \
  -d "config.timeout=10000" \
  -d "config.keepalive=60000" \
  -d "config.retry_count=3" \
  -d "config.queue_size=1000" \
  -d "config.flush_timeout=2"
```

### Prometheus Metrics Plugin
```bash
# Configure Prometheus metrics
curl -X POST http://localhost:8001/services/revenue-engine-api/plugins \
  -d "name=prometheus" \
  -d "config.per_consumer=true" \
  -d "config.status_code_metrics=true" \
  -d "config.latency_metrics=true" \
  -d "config.bandwidth_metrics=true"
```

### StatsD Metrics
```bash
# Configure StatsD metrics
curl -X POST http://localhost:8001/services/revenue-engine-api/plugins \
  -d "name=statsd" \
  -d "config.host=statsd-service" \
  -d "config.port=8125" \
  -d "config.prefix=kong" \
  -d "config.metrics=request_count,latency,status_count,response_size,upstream_latency"
```

---

## Security Configuration

### IP Restriction Plugin
```bash
# Configure IP restrictions
curl -X POST http://localhost:8001/services/revenue-engine-api/plugins \
  -d "name=ip-restriction" \
  -d "config.allow=192.168.0.0/16,10.0.0.0/8" \
  -d "config.deny=172.16.0.0/12"
```

### AWS Lambda Integration
```bash
# Configure AWS Lambda plugin for serverless functions
curl -X POST http://localhost:8001/services/revenue-engine-api/plugins \
  -d "name=aws-lambda" \
  -d "config.aws_key=your_aws_key" \
  -d "config.aws_secret=your_aws_secret" \
  -d "config.aws_region=us-east-1" \
  -d "config.function_name=revenue-processor" \
  -d "config.invocation_type=RequestResponse"
```

---

## Kong Manager & Developer Portal

### Kong Manager Setup
```bash
# Enable Kong Manager
sudo tee -a /etc/kong/kong.conf > /dev/null <<EOF
admin_gui_listen = 0.0.0.0:8002
admin_gui_url = https://kong-manager.tradingrobotplug.com
EOF

# Restart Kong
sudo systemctl restart kong

echo "Kong Manager available at https://kong-manager.tradingrobotplug.com:8002"
```

### Developer Portal Configuration
```bash
# Enable Developer Portal
sudo tee -a /etc/kong/kong.conf > /dev/null <<EOF
portal = on
portal_gui_listen = 0.0.0.0:8003
portal_gui_url = https://developer.tradingrobotplug.com
EOF

# Configure portal authentication
curl -X POST http://localhost:8001/services/portal-api/plugins \
  -d "name=key-auth"

# Add portal routes
curl -X POST http://localhost:8001/services/portal-api/routes \
  -d "paths[]=/portal" \
  -d "preserve_host=true"
```

---

## High Availability & Scaling

### Kong Clustering
```bash
# Configure Kong for clustering (multiple Kong nodes)
sudo tee -a /etc/kong/kong.conf > /dev/null <<EOF
cluster_listen = 0.0.0.0:7946
cluster_advertise = kong-node-1:7946
cluster_encrypt = secure_cluster_key_here
EOF

# Database-backed configuration (already configured)
# All Kong nodes share the same PostgreSQL database
```

### Load Balancing
```bash
# Configure upstream load balancing
curl -X POST http://localhost:8001/upstreams \
  -d "name=revenue-engine-cluster" \
  -d "algorithm=round_robin"

# Add multiple targets
curl -X POST http://localhost:8001/upstreams/revenue-engine-cluster/targets \
  -d "target=revenue-engine-1:8080" \
  -d "weight=100"

curl -X POST http://localhost:8001/upstreams/revenue-engine-cluster/targets \
  -d "target=revenue-engine-2:8080" \
  -d "weight=100"
```

---

## Backup & Recovery

### Configuration Backup
```bash
#!/bin/bash
# Kong configuration backup

BACKUP_DIR="/backup/kong"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p "$BACKUP_DIR"

# Backup Kong configuration
kong config db_export "$BACKUP_DIR/kong_config_$TIMESTAMP.yaml"

# Backup database
pg_dump -h localhost -U kong -d kong > "$BACKUP_DIR/kong_db_$TIMESTAMP.sql"

# Compress backup
tar -czf "$BACKUP_DIR/kong_backup_$TIMESTAMP.tar.gz" -C "$BACKUP_DIR" "kong_config_$TIMESTAMP.yaml" "kong_db_$TIMESTAMP.sql"

# Clean up old files (keep last 7 days)
find "$BACKUP_DIR" -name "kong_*" -type f -mtime +7 -delete

echo "Kong backup completed: $BACKUP_DIR/kong_backup_$TIMESTAMP.tar.gz"
```

### Configuration Restore
```bash
#!/bin/bash
# Kong configuration restore

BACKUP_FILE="$1"

if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: $0 <backup_file>"
    exit 1
fi

# Stop Kong
sudo systemctl stop kong

# Restore database
tar -xzf "$BACKUP_FILE" -C /tmp
psql -h localhost -U kong -d kong < /tmp/kong_db_*.sql

# Restore configuration
kong config db_import /tmp/kong_config_*.yaml

# Start Kong
sudo systemctl start kong

echo "Kong restore completed"
```

---

## Testing & Validation

### API Gateway Test Script
```bash
#!/bin/bash
# Kong API Gateway testing

API_URL="https://revenue-engine.tradingrobotplug.com"
API_KEY="secure_api_key_here"

echo "🧪 Testing Kong API Gateway..."

# Test basic connectivity
echo "Testing basic connectivity..."
curl -H "apikey: $API_KEY" "$API_URL/api/v1/revenue/health" -k

# Test rate limiting
echo ""
echo "Testing rate limiting..."
for i in {1..5}; do
    curl -H "apikey: $API_KEY" "$API_URL/api/v1/revenue/health" -k -s -o /dev/null -w "Request $i: %{http_code}\n"
done

# Test authentication
echo ""
echo "Testing authentication..."
curl "$API_URL/api/v1/revenue/health" -k  # Should fail without API key

# Test CORS
echo ""
echo "Testing CORS..."
curl -H "Origin: https://tradingrobotplug.com" -H "apikey: $API_KEY" "$API_URL/api/v1/revenue/health" -k -I | grep -i "access-control"

echo ""
echo "Kong API Gateway testing complete"
```

### Performance Benchmark
```bash
#!/bin/bash
# Kong performance benchmarking

# Install wrk for benchmarking
sudo apt-get install -y wrk

# Run benchmark
wrk -t12 -c400 -d30s \
    -H "apikey: secure_api_key_here" \
    "https://revenue-engine.tradingrobotplug.com/api/v1/revenue/health"

# Monitor Kong metrics during test
curl http://localhost:8001/metrics | grep kong
```

---

## Troubleshooting

### Common Issues

#### Plugin Not Working
```bash
# Check plugin status
curl http://localhost:8001/services/revenue-engine-api/plugins

# Check Kong logs
sudo tail -f /var/log/kong/error.log

# Validate plugin configuration
curl http://localhost:8001/plugins | jq '.data[] | select(.name=="rate-limiting")'
```

#### Upstream Connection Issues
```bash
# Check upstream health
curl http://localhost:8001/upstreams/revenue-engine-upstream/health

# Test direct connection to upstream
curl http://revenue-engine-service.production.svc.cluster.local:8080/health

# Check Kong to upstream connectivity
curl http://localhost:8001/upstreams/revenue-engine-upstream/targets
```

#### SSL/TLS Issues
```bash
# Check SSL certificate
openssl x509 -in /etc/kong/ssl/revenue-engine.crt -text -noout

# Test SSL connectivity
openssl s_client -connect localhost:8443 -servername revenue-engine.tradingrobotplug.com

# Check Kong SSL configuration
grep ssl /etc/kong/kong.conf
```

---

**Kong API Gateway Configuration Complete ✅**
**Agent-3 (Infrastructure & DevOps) - 2026-01-07**
**Status:** Ready for deployment and validation testing