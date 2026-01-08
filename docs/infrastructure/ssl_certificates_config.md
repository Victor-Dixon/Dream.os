# SSL/TLS Certificate Configuration
## Infrastructure Block 4 - Secure Communications Layer
## Agent-3 (Infrastructure & DevOps) - 2026-01-07

**Status:** ACTIVE IMPLEMENTATION
**Purpose:** Deploy production SSL certificates for Revenue Engine secure communications
**Configuration:** Let's Encrypt + Cloudflare integration with automated renewal

---

## Certificate Architecture

### Certificate Types
- **Domain Certificates**: revenue-engine.tradingrobotplug.com
- **Wildcard Certificates**: *.tradingrobotplug.com (for subdomains)
- **Internal Certificates**: For service mesh mTLS communication

### Certificate Authority
- **Primary CA**: Let's Encrypt (automated, trusted)
- **Backup CA**: Cloudflare Origin CA (for complex deployments)
- **Internal CA**: Self-signed for service mesh (development/staging)

---

## SSL Certificate Configuration

### Let's Encrypt Certificate Generation
```bash
#!/bin/bash
# SSL certificate deployment script

# Install certbot if not present
sudo apt-get update
sudo apt-get install -y certbot

# Generate certificates for Revenue Engine domains
sudo certbot certonly \
  --standalone \
  --agree-tos \
  --email admin@tradingrobotplug.com \
  --domains revenue-engine.tradingrobotplug.com \
  --domains api.revenue-engine.tradingrobotplug.com \
  --domains admin.revenue-engine.tradingrobotplug.com

# Copy certificates to infrastructure directory
sudo cp /etc/letsencrypt/live/revenue-engine.tradingrobotplug.com/fullchain.pem ./ssl/
sudo cp /etc/letsencrypt/live/revenue-engine.tradingrobotplug.com/privkey.pem ./ssl/

# Set proper permissions
sudo chmod 644 ./ssl/fullchain.pem
sudo chmod 600 ./ssl/privkey.pem
sudo chown root:root ./ssl/*.pem

echo "SSL certificates deployed successfully"
```

### Kubernetes TLS Secret Creation
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: revenue-engine-tls
  namespace: production
type: kubernetes.io/tls
data:
  tls.crt: LS0tLS1CRUdJTi... # base64 encoded fullchain.pem
  tls.key: LS0tLS1CRUdJTi... # base64 encoded privkey.pem
---
apiVersion: v1
kind: Secret
metadata:
  name: revenue-engine-internal-tls
  namespace: production
type: kubernetes.io/tls
data:
  tls.crt: LS0tLS1CRUdJTi... # base64 encoded internal cert
  tls.key: LS0tLS1CRUdJTi... # base64 encoded internal key
```

### Certificate Validation Script
```bash
#!/bin/bash
# SSL certificate validation

DOMAIN="revenue-engine.tradingrobotplug.com"
CERT_FILE="./ssl/fullchain.pem"
KEY_FILE="./ssl/privkey.pem"

# Validate certificate files exist
if [ ! -f "$CERT_FILE" ]; then
    echo "❌ Certificate file not found: $CERT_FILE"
    exit 1
fi

if [ ! -f "$KEY_FILE" ]; then
    echo "❌ Key file not found: $KEY_FILE"
    exit 1
fi

# Validate certificate format
if ! openssl x509 -in "$CERT_FILE" -text -noout > /dev/null 2>&1; then
    echo "❌ Invalid certificate format"
    exit 1
fi

# Validate private key format
if ! openssl rsa -in "$KEY_FILE" -check > /dev/null 2>&1; then
    echo "❌ Invalid private key format"
    exit 1
fi

# Check certificate expiration
EXPIRY_DATE=$(openssl x509 -in "$CERT_FILE" -enddate -noout | cut -d= -f2)
EXPIRY_SECONDS=$(date -d "$EXPIRY_DATE" +%s)
CURRENT_SECONDS=$(date +%s)
DAYS_LEFT=$(( ($EXPIRY_SECONDS - $CURRENT_SECONDS) / 86400 ))

if [ $DAYS_LEFT -lt 30 ]; then
    echo "⚠️ Certificate expires in $DAYS_LEFT days - renewal recommended"
elif [ $DAYS_LEFT -lt 7 ]; then
    echo "❌ Certificate expires in $DAYS_LEFT days - urgent renewal required"
    exit 1
else
    echo "✅ Certificate is valid for $DAYS_LEFT days"
fi

# Test SSL connectivity
if openssl s_client -connect "$DOMAIN:443" -servername "$DOMAIN" < /dev/null > /dev/null 2>&1; then
    echo "✅ SSL connectivity test passed"
else
    echo "❌ SSL connectivity test failed"
fi

echo "SSL certificate validation complete"
```

---

## Service Mesh TLS Configuration

### Istio Peer Authentication (mTLS)
```yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: revenue-engine-mtls
  namespace: production
spec:
  selector:
    matchLabels:
      app: revenue-engine
  mtls:
    mode: STRICT
---
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default-mtls
  namespace: production
spec:
  mtls:
    mode: PERMISSIVE
```

### Istio Request Authentication
```yaml
apiVersion: security.istio.io/v1beta1
kind: RequestAuthentication
metadata:
  name: revenue-engine-jwt
  namespace: production
spec:
  selector:
    matchLabels:
      app: revenue-engine
  jwtRules:
  - issuer: "https://accounts.google.com"
    audiences:
    - "revenue-engine.tradingrobotplug.com"
    jwksUri: "https://www.googleapis.com/oauth2/v3/certs"
    forwardOriginalToken: true
```

### Istio Authorization Policy
```yaml
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: revenue-engine-authz
  namespace: production
spec:
  selector:
    matchLabels:
      app: revenue-engine
  action: ALLOW
  rules:
  - from:
    - source:
        requestPrincipals: ["*"]
    to:
    - operation:
        methods: ["GET", "POST", "PUT", "DELETE"]
        paths: ["/api/v1/revenue/*"]
  - from:
    - source:
        requestPrincipals: ["admin@tradingrobotplug.com"]
    to:
    - operation:
        methods: ["*"]
        paths: ["/api/v1/admin/*"]
```

---

## API Gateway SSL Configuration

### Kong SSL Configuration
```yaml
# kong.conf SSL settings
ssl_cert = /etc/kong/ssl/revenue-engine.crt
ssl_cert_key = /etc/kong/ssl/revenue-engine.key
ssl_cipher_suite = intermediate
client_ssl = on
client_ssl_cert = /etc/kong/ssl/client-ca.crt

# Upstream SSL verification
lua_ssl_verify_depth = 3
lua_ssl_trusted_certificate = /etc/kong/ssl/ca-bundle.crt
```

### Kong SSL Certificate Management
```bash
# Install Kong SSL certificate
sudo mkdir -p /etc/kong/ssl
sudo cp ./ssl/fullchain.pem /etc/kong/ssl/revenue-engine.crt
sudo cp ./ssl/privkey.pem /etc/kong/ssl/revenue-engine.key

# Set permissions
sudo chown kong:kong /etc/kong/ssl/*
sudo chmod 644 /etc/kong/ssl/revenue-engine.crt
sudo chmod 600 /etc/kong/ssl/revenue-engine.key

# Reload Kong configuration
sudo kong reload
```

### Kong HTTPS Route Configuration
```yaml
# Kong route with SSL termination
curl -X POST http://localhost:8001/routes \
  -d "protocols[]=https" \
  -d "hosts[]=revenue-engine.tradingrobotplug.com" \
  -d "paths[]=/api/v1/revenue" \
  -d "service.name=revenue-engine-service" \
  -d "preserve_host=true" \
  -d "strip_path=false"
```

---

## Certificate Renewal Automation

### Certbot Renewal Hook
```bash
#!/bin/bash
# Certificate renewal hook script

# Define domains and services
DOMAINS=("revenue-engine.tradingrobotplug.com")
SERVICES=("istio" "kong" "nginx")

# Function to reload service
reload_service() {
    local service=$1

    case $service in
        "istio")
            # Reload Istio gateway
            kubectl rollout restart deployment/istio-ingressgateway -n istio-system
            ;;
        "kong")
            # Reload Kong
            kong reload
            ;;
        "nginx")
            # Reload nginx
            nginx -s reload
            ;;
        *)
            echo "Unknown service: $service"
            return 1
            ;;
    esac
}

# Copy renewed certificates
for domain in "${DOMAINS[@]}"; do
    if [ -d "/etc/letsencrypt/live/$domain" ]; then
        cp "/etc/letsencrypt/live/$domain/fullchain.pem" "./ssl/"
        cp "/etc/letsencrypt/live/$domain/privkey.pem" "./ssl/"

        # Update Kubernetes secrets
        kubectl create secret tls revenue-engine-tls \
          --cert=./ssl/fullchain.pem \
          --key=./ssl/privkey.pem \
          --dry-run=client -o yaml | kubectl apply -f -

        # Reload services
        for service in "${SERVICES[@]}"; do
            reload_service "$service"
        done

        echo "✅ Certificates renewed and services reloaded for $domain"
    fi
done
```

### Cron Job for Certificate Monitoring
```bash
# Add to crontab for daily certificate checks
0 2 * * * /path/to/ssl_monitor.sh

# Certificate monitoring script
#!/bin/bash
CERT_FILE="./ssl/fullchain.pem"
WARNING_DAYS=30
CRITICAL_DAYS=7

if [ ! -f "$CERT_FILE" ]; then
    echo "CRITICAL: Certificate file not found" | mail -s "SSL Certificate Alert" admin@tradingrobotplug.com
    exit 2
fi

EXPIRY_DATE=$(openssl x509 -in "$CERT_FILE" -enddate -noout | sed 's/notAfter=//')
EXPIRY_SECONDS=$(date -d "$EXPIRY_DATE" +%s)
CURRENT_SECONDS=$(date +%s)
DAYS_LEFT=$(( ($EXPIRY_SECONDS - $CURRENT_SECONDS) / 86400 ))

if [ $DAYS_LEFT -le $CRITICAL_DAYS ]; then
    echo "CRITICAL: Certificate expires in $DAYS_LEFT days" | mail -s "SSL Certificate Alert" admin@tradingrobotplug.com
    exit 2
elif [ $DAYS_LEFT -le $WARNING_DAYS ]; then
    echo "WARNING: Certificate expires in $DAYS_LEFT days" | mail -s "SSL Certificate Alert" admin@tradingrobotplug.com
    exit 1
else
    echo "OK: Certificate valid for $DAYS_LEFT days"
fi
```

---

## Security Headers Configuration

### Nginx Security Headers
```nginx
# Security headers for Revenue Engine
server {
    listen 443 ssl http2;
    server_name revenue-engine.tradingrobotplug.com;

    ssl_certificate /etc/ssl/certs/revenue-engine.crt;
    ssl_certificate_key /etc/ssl/private/revenue-engine.key;

    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin";
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'";

    location / {
        proxy_pass http://kong-upstream;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Istio Security Headers
```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: revenue-engine-security-headers
  namespace: production
spec:
  gateways:
  - revenue-engine-gateway
  hosts:
  - revenue-engine.tradingrobotplug.com
  http:
  - route:
    - destination:
        host: revenue-engine-service
    headers:
      request:
        add:
          X-Frame-Options: "DENY"
          X-Content-Type-Options: "nosniff"
          X-XSS-Protection: "1; mode=block"
          Strict-Transport-Security: "max-age=31536000; includeSubDomains"
          Referrer-Policy: "strict-origin-when-cross-origin"
```

---

## Deployment Verification

### SSL Health Check Script
```bash
#!/bin/bash
# Comprehensive SSL health check

DOMAINS=(
    "revenue-engine.tradingrobotplug.com"
    "api.revenue-engine.tradingrobotplug.com"
    "admin.revenue-engine.tradingrobotplug.com"
)

ISSUER_CHECK="Let's Encrypt"
MIN_DAYS=30

echo "🔍 SSL Certificate Health Check"
echo "================================="

for domain in "${DOMAINS[@]}"; do
    echo ""
    echo "Checking $domain..."

    # Test SSL connection
    if ! timeout 10 openssl s_client -connect "$domain:443" -servername "$domain" < /dev/null > /tmp/ssl_check 2>/dev/null; then
        echo "❌ Cannot connect to $domain:443"
        continue
    fi

    # Extract certificate info
    CERT_INFO=$(openssl x509 -in /tmp/ssl_check -text 2>/dev/null)

    # Check issuer
    ISSUER=$(echo "$CERT_INFO" | grep "Issuer:" | head -1)
    if echo "$ISSUER" | grep -q "$ISSUER_CHECK"; then
        echo "✅ Certificate issued by $ISSUER_CHECK"
    else
        echo "⚠️ Certificate not issued by expected CA: $ISSUER"
    fi

    # Check expiration
    END_DATE=$(echo "$CERT_INFO" | grep "Not After" | sed 's/.*Not After : //')
    END_SECONDS=$(date -d "$END_DATE" +%s 2>/dev/null)
    CURRENT_SECONDS=$(date +%s)
    DAYS_LEFT=$(( ($END_SECONDS - $CURRENT_SECONDS) / 86400 ))

    if [ $DAYS_LEFT -gt $MIN_DAYS ]; then
        echo "✅ Certificate valid for $DAYS_LEFT days"
    elif [ $DAYS_LEFT -gt 7 ]; then
        echo "⚠️ Certificate expires in $DAYS_LEFT days"
    else
        echo "❌ Certificate expires in $DAYS_LEFT days - RENEW IMMEDIATELY"
    fi

    # Check cipher
    CIPHER=$(openssl s_client -connect "$domain:443" -servername "$domain" 2>/dev/null | grep "Cipher" | awk '{print $3}')
    if [ -n "$CIPHER" ]; then
        echo "✅ Using cipher: $CIPHER"
    fi

done

rm -f /tmp/ssl_check
echo ""
echo "SSL health check complete"
```

---

**SSL/TLS Certificate Configuration Complete ✅**
**Agent-3 (Infrastructure & DevOps) - 2026-01-07**
**Status:** Ready for deployment and validation testing