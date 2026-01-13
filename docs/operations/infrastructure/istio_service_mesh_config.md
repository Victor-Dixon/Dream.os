# Istio Service Mesh Configuration
## Infrastructure Block 4 - Service Mesh & Traffic Management
## Agent-3 (Infrastructure & DevOps) - 2026-01-07

**Status:** ACTIVE IMPLEMENTATION
**Purpose:** Deploy Istio service mesh for Revenue Engine microservices orchestration
**Configuration:** Istio 1.20+ with traffic management, security, and observability

---

## Service Mesh Architecture

### Istio Components
```
Control Plane:
├── istiod (Pilot, Citadel, Galley) - Control plane
├── Ingress Gateway - External traffic ingress
└── Egress Gateway - External traffic egress

Data Plane:
├── Envoy Proxy - Sidecar proxies
├── Service Discovery - Automatic service registration
└── Load Balancing - Intelligent traffic distribution
```

### Traffic Flow
```
Internet → Cloudflare → Istio Ingress Gateway → VirtualService → DestinationRule → Service
                                       ↓
                                 Envoy Sidecar → Revenue Engine Pod
```

---

## Istio Installation & Configuration

### Istio Installation Script
```bash
#!/bin/bash
# Istio installation and configuration

# Download Istio
export ISTIO_VERSION=1.20.0
curl -L https://istio.io/downloadIstio | sh -
cd istio-$ISTIO_VERSION

# Add istioctl to PATH
export PATH=$PWD/bin:$PATH

# Install Istio with demo profile
istioctl install --set profile=demo -y

# Enable sidecar injection for production namespace
kubectl label namespace production istio-injection=enabled

# Verify installation
kubectl get pods -n istio-system
kubectl get svc -n istio-system

echo "Istio service mesh installed successfully"
```

### Istio Ingress Gateway Configuration
```yaml
apiVersion: networking.istio.io/v1beta1
kind: Gateway
metadata:
  name: revenue-engine-gateway
  namespace: production
spec:
  selector:
    istio: ingressgateway
  servers:
  - port:
      number: 443
      name: https
      protocol: HTTPS
    tls:
      mode: SIMPLE
      credentialName: revenue-engine-tls
    hosts:
    - revenue-engine.tradingrobotplug.com
    - api.revenue-engine.tradingrobotplug.com
  - port:
      number: 80
      name: http
      protocol: HTTP
    hosts:
    - revenue-engine.tradingrobotplug.com
    - api.revenue-engine.tradingrobotplug.com
```

### Virtual Service Configuration
```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: revenue-engine-vs
  namespace: production
spec:
  hosts:
  - revenue-engine.tradingrobotplug.com
  gateways:
  - revenue-engine-gateway
  http:
  - name: "api-routes"
    match:
    - uri:
        prefix: "/api/v1/revenue"
    route:
    - destination:
        host: revenue-engine-service
        port:
          number: 8080
    timeout: 30s
    retries:
      attempts: 3
      perTryTimeout: 10s
    corsPolicy:
      allowOrigins:
      - exact: "https://tradingrobotplug.com"
      - exact: "https://www.tradingrobotplug.com"
      allowMethods:
      - GET
      - POST
      - PUT
      - DELETE
      allowHeaders:
      - "Authorization"
      - "Content-Type"
      allowCredentials: true

  - name: "admin-routes"
    match:
    - uri:
        prefix: "/api/v1/admin"
    route:
    - destination:
        host: revenue-engine-admin
        port:
          number: 8080
    timeout: 60s
    retries:
      attempts: 2
      perTryTimeout: 30s

  - name: "health-check"
    match:
    - uri:
        exact: "/health"
    route:
    - destination:
        host: revenue-engine-service
        port:
          number: 8080
```

### Destination Rule Configuration
```yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: revenue-engine-dr
  namespace: production
spec:
  host: revenue-engine-service
  trafficPolicy:
    loadBalancer:
      simple: ROUND_ROBIN
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http1MaxPendingRequests: 50
        http2MaxRequests: 100
        maxRequestsPerConnection: 10
        maxRetries: 3
    outlierDetection:
      consecutiveLocalOriginFailures: 5
      interval: 10s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
  subsets:
  - name: v1
    labels:
      version: v1
    trafficPolicy:
      loadBalancer:
        simple: ROUND_ROBIN
  - name: v2
    labels:
      version: v2
    trafficPolicy:
      loadBalancer:
        simple: ROUND_ROBIN
```

---

## Traffic Management & Routing

### Canary Deployment Configuration
```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: revenue-engine-canary
  namespace: production
spec:
  hosts:
  - revenue-engine.tradingrobotplug.com
  http:
  - name: "canary-rollout"
    match:
    - uri:
        prefix: "/api/v1/revenue"
    route:
    - destination:
        host: revenue-engine-service
        subset: v2
      weight: 20
    - destination:
        host: revenue-engine-service
        subset: v1
      weight: 80
    mirror:
      host: revenue-engine-service
      subset: v2
      percentage:
        value: 100.0
```

### Circuit Breaker Configuration
```yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: revenue-engine-circuit-breaker
  namespace: production
spec:
  host: revenue-engine-service
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
        connectTimeout: 30s
      http:
        http1MaxPendingRequests: 50
        http2MaxRequests: 100
        maxRequestsPerConnection: 10
        maxRetries: 3
    outlierDetection:
      consecutiveLocalOriginFailures: 5
      interval: 10s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
      minHealthPercent: 30
```

### Fault Injection for Testing
```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: revenue-engine-fault-injection
  namespace: production
spec:
  hosts:
  - revenue-engine.tradingrobotplug.com
  http:
  - fault:
      delay:
        percentage:
          value: 10.0
        fixedDelay: 5s
      abort:
        percentage:
          value: 5.0
        httpStatus: 503
    route:
    - destination:
        host: revenue-engine-service
```

---

## Security Configuration

### Mutual TLS (mTLS) Configuration
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

### JWT Authentication
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
    outputPayloadToHeader: "x-jwt-payload"
```

### Authorization Policies
```yaml
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: revenue-engine-api-access
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
        methods: ["GET"]
        paths: ["/api/v1/revenue/market-data"]
  - from:
    - source:
        requestPrincipals: ["user@tradingrobotplug.com"]
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
        paths: ["*"]
```

---

## Observability & Monitoring

### Kiali Installation
```bash
# Install Kiali for service mesh observability
kubectl apply -f https://raw.githubusercontent.com/kiali/kiali/v1.65.0/deploy/kubernetes/kiali.yaml

# Access Kiali dashboard
kubectl port-forward svc/kiali -n istio-system 20001:20001
# Open http://localhost:20001
```

### Prometheus Metrics Collection
```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: istio-monitor
  namespace: production
spec:
  selector:
    matchLabels:
      app: revenue-engine
  endpoints:
  - port: metrics
    path: /stats/prometheus
    interval: 15s
  namespaceSelector:
    matchNames:
    - production
```

### Jaeger Distributed Tracing
```yaml
apiVersion: jaegertracing.io/v1
kind: Jaeger
metadata:
  name: revenue-engine-tracing
  namespace: production
spec:
  strategy: allInOne
  allInOne:
    image: all-in-one
    options:
      log-level: info
      memory:
        max-trunks: 50000
```

### Application Metrics
```yaml
apiVersion: telemetry.istio.io/v1alpha1
kind: Telemetry
metadata:
  name: revenue-engine-telemetry
  namespace: production
spec:
  selector:
    matchLabels:
      app: revenue-engine
  metrics:
  - providers:
    - name: prometheus
    overrides:
    - tagOverrides:
        request_operation:
          value: "istio_request_operation"
      match:
        metric: REQUEST_COUNT
        mode: CLIENT_AND_SERVER
  - providers:
    - name: prometheus
    overrides:
    - tagOverrides:
        response_code:
          value: "istio_response_code"
      match:
        metric: REQUEST_DURATION
        mode: CLIENT_AND_SERVER
  accessLogging:
  - providers:
    - name: envoy
```

---

## Service Mesh Validation

### Health Check Script
```bash
#!/bin/bash
# Istio service mesh health check

# Check Istio control plane
echo "🔍 Checking Istio control plane..."
kubectl get pods -n istio-system

# Check sidecar injection
echo ""
echo "🔍 Checking sidecar injection..."
kubectl get pods -n production -o jsonpath='{.items[*].spec.containers[*].name}' | tr ' ' '\n' | grep istio-proxy | wc -l

# Check gateway status
echo ""
echo "🔍 Checking Istio gateway..."
kubectl get gateway -n production

# Check virtual services
echo ""
echo "🔍 Checking virtual services..."
kubectl get vs -n production

# Check destination rules
echo ""
echo "🔍 Checking destination rules..."
kubectl get dr -n production

# Test service connectivity
echo ""
echo "🔍 Testing service connectivity..."
kubectl exec -n production deployment/revenue-engine -- curl -s http://revenue-engine-service:8080/health

echo ""
echo "Istio service mesh health check complete"
```

### Traffic Testing Script
```bash
#!/bin/bash
# Service mesh traffic testing

ENDPOINT="https://revenue-engine.tradingrobotplug.com/api/v1/revenue/health"
REQUESTS=100
CONCURRENCY=10

echo "🚀 Testing service mesh traffic routing..."

# Install hey for load testing (if not present)
if ! command -v hey &> /dev/null; then
    wget https://hey-release.s3.us-east-2.amazonaws.com/hey_linux_amd64
    chmod +x hey_linux_amd64
    sudo mv hey_linux_amd64 /usr/local/bin/hey
fi

# Run load test
hey -n $REQUESTS -c $CONCURRENCY -m GET "$ENDPOINT"

# Check Istio metrics
echo ""
echo "📊 Checking Istio metrics..."
kubectl exec -n istio-system deployment/istiod -- pilot-agent request GET /metrics | grep istio_requests_total

echo ""
echo "Service mesh traffic testing complete"
```

---

## Troubleshooting Guide

### Common Issues & Solutions

#### Sidecar Injection Not Working
```bash
# Check namespace label
kubectl get namespace production --show-labels

# Label namespace if missing
kubectl label namespace production istio-injection=enabled

# Restart pods to inject sidecar
kubectl rollout restart deployment/revenue-engine -n production
```

#### Gateway Not Routing Traffic
```bash
# Check gateway status
kubectl get gateway -n production
kubectl describe gateway revenue-engine-gateway -n production

# Check virtual service
kubectl get vs -n production
kubectl describe vs revenue-engine-vs -n production

# Check gateway logs
kubectl logs -n istio-system deployment/istio-ingressgateway
```

#### mTLS Issues
```bash
# Check peer authentication
kubectl get peerauthentication -n production

# Test mTLS connectivity
kubectl exec -n production deployment/revenue-engine -- curl -v https://revenue-engine-service:8080/health --cacert /etc/istio/certs/ca-cert.pem
```

#### Certificate Issues
```bash
# Check certificate secrets
kubectl get secrets -n production | grep tls

# Verify certificate validity
kubectl describe secret revenue-engine-tls -n production

# Check gateway certificate configuration
kubectl get gateway -n production -o yaml
```

---

## Performance Optimization

### Resource Limits
```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: istio-resource-quota
  namespace: production
spec:
  hard:
    requests.cpu: "2000m"
    requests.memory: "4Gi"
    limits.cpu: "4000m"
    limits.memory: "8Gi"
---
apiVersion: v1
kind: LimitRange
metadata:
  name: istio-limits
  namespace: production
spec:
  limits:
  - default:
      cpu: "500m"
      memory: "1Gi"
    defaultRequest:
      cpu: "100m"
      memory: "256Mi"
    type: Container
```

### Circuit Breaker Tuning
```yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: revenue-engine-performance
  namespace: production
spec:
  host: revenue-engine-service
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 200
        connectTimeout: 10s
      http:
        http1MaxPendingRequests: 100
        http2MaxRequests: 200
        maxRequestsPerConnection: 20
        maxRetries: 5
        useClientProtocol: true
```

---

**Istio Service Mesh Configuration Complete ✅**
**Agent-3 (Infrastructure & DevOps) - 2026-01-07**
**Status:** Ready for deployment and validation testing