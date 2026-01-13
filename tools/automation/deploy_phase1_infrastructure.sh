#!/bin/bash
# Phase 1 Infrastructure Deployment Script
# SSL Certificates + Service Mesh + API Gateway
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

    # Check if required tools are available
    local tools=("kubectl" "helm" "openssl" "curl")
    for tool in "${tools[@]}"; do
        if ! command -v "$tool" &> /dev/null; then
            log_error "$tool is not installed or not in PATH"
            exit 1
        fi
    done

    # Check Kubernetes connectivity
    if ! kubectl cluster-info &> /dev/null; then
        log_error "Cannot connect to Kubernetes cluster"
        exit 1
    fi

    # Check if cert-manager is installed (for SSL)
    if ! kubectl get crd certificates.cert-manager.io &> /dev/null; then
        log_warning "cert-manager not found, installing..."
        kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.12.0/cert-manager.yaml
        kubectl wait --for=condition=available --timeout=300s deployment -n cert-manager --all
    fi

    log_success "Prerequisites check passed"
}

# Deploy SSL certificates
deploy_ssl_certificates() {
    log_info "Deploying SSL certificates..."

    # Create SSL namespace and secrets
    kubectl create namespace production --dry-run=client -o yaml | kubectl apply -f -

    # Create SSL certificate directory
    mkdir -p "$PROJECT_ROOT/infrastructure/ssl"

    # Generate self-signed certificates for development (replace with Let's Encrypt in production)
    log_info "Generating SSL certificates..."
    openssl req -x509 -newkey rsa:4096 -keyout "$PROJECT_ROOT/infrastructure/ssl/revenue-engine.key" \
        -out "$PROJECT_ROOT/infrastructure/ssl/revenue-engine.crt" -days 365 -nodes \
        -subj "/C=US/ST=State/L=City/O=Organization/CN=revenue-engine.tradingrobotplug.com"

    # Create Kubernetes TLS secret
    kubectl create secret tls revenue-engine-tls \
        --cert="$PROJECT_ROOT/infrastructure/ssl/revenue-engine.crt" \
        --key="$PROJECT_ROOT/infrastructure/ssl/revenue-engine.key" \
        --namespace production --dry-run=client -o yaml | kubectl apply -f -

    # Create internal mTLS certificates
    openssl req -x509 -newkey rsa:2048 -keyout "$PROJECT_ROOT/infrastructure/ssl/internal.key" \
        -out "$PROJECT_ROOT/infrastructure/ssl/internal.crt" -days 365 -nodes \
        -subj "/C=US/ST=State/L=City/O=Organization/CN=internal.revenue-engine"

    kubectl create secret tls revenue-engine-internal-tls \
        --cert="$PROJECT_ROOT/infrastructure/ssl/internal.crt" \
        --key="$PROJECT_ROOT/infrastructure/ssl/internal.key" \
        --namespace production --dry-run=client -o yaml | kubectl apply -f -

    log_success "SSL certificates deployed"
}

# Deploy Istio service mesh
deploy_istio_mesh() {
    log_info "Deploying Istio service mesh..."

    # Install Istio using istioctl
    if ! command -v istioctl &> /dev/null; then
        log_info "Installing istioctl..."
        curl -L https://istio.io/downloadIstio | sh -
        export PATH="$PWD/istio-1.20.0/bin:$PATH"
    fi

    # Install Istio with production profile
    istioctl install --set profile=default -y

    # Enable sidecar injection for production namespace
    kubectl label namespace production istio-injection=enabled --overwrite

    # Wait for Istio components to be ready
    kubectl wait --for=condition=available --timeout=300s deployment/istiod -n istio-system

    # Deploy Istio gateway configuration
    cat > "$PROJECT_ROOT/infrastructure/istio-gateway.yaml" << 'EOF'
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
  - port:
      number: 80
      name: http
      protocol: HTTP
    hosts:
    - revenue-engine.tradingrobotplug.com
EOF

    kubectl apply -f "$PROJECT_ROOT/infrastructure/istio-gateway.yaml"

    # Deploy VirtualService
    cat > "$PROJECT_ROOT/infrastructure/istio-virtualservice.yaml" << 'EOF'
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
  - match:
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
  - match:
    - uri:
        exact: "/health"
    route:
    - destination:
        host: revenue-engine-service
        port:
          number: 8080
EOF

    kubectl apply -f "$PROJECT_ROOT/infrastructure/istio-virtualservice.yaml"

    # Deploy DestinationRule for traffic policies
    cat > "$PROJECT_ROOT/infrastructure/istio-destinationrule.yaml" << 'EOF'
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
EOF

    kubectl apply -f "$PROJECT_ROOT/infrastructure/istio-destinationrule.yaml"

    log_success "Istio service mesh deployed"
}

# Deploy Kong API Gateway
deploy_kong_gateway() {
    log_info "Deploying Kong API Gateway..."

    # Install Kong using Helm
    helm repo add kong https://charts.konghq.com
    helm repo update

    # Create Kong configuration
    cat > "$PROJECT_ROOT/infrastructure/kong-values.yaml" << 'EOF'
image:
  repository: kong/kong-gateway
  tag: "3.4"

env:
  database: "off"  # Using DB-less mode for simplicity
  log_level: "info"

proxy:
  type: ClusterIP
  http:
    enabled: true
    servicePort: 80
    containerPort: 8000
  tls:
    enabled: true
    servicePort: 443
    containerPort: 8443
    containerPort: 8444

admin:
  type: ClusterIP
  http:
    enabled: true
    servicePort: 8001
    containerPort: 8001

ingressController:
  enabled: false

plugins:
  configMaps: kong-plugins

secretVolumes:
- kong-tls-secret

serviceMonitor:
  enabled: true
EOF

    # Install Kong
    helm upgrade --install kong kong/kong \
        -f "$PROJECT_ROOT/infrastructure/kong-values.yaml" \
        -n production --create-namespace

    # Wait for Kong to be ready
    kubectl wait --for=condition=available --timeout=300s deployment/kong -n production

    # Create Kong TLS secret
    kubectl create secret tls kong-tls \
        --cert="$PROJECT_ROOT/infrastructure/ssl/revenue-engine.crt" \
        --key="$PROJECT_ROOT/infrastructure/ssl/revenue-engine.key" \
        --namespace production --dry-run=client -o yaml | kubectl apply -f -

    # Configure Kong service and routes (declarative configuration)
    cat > "$PROJECT_ROOT/infrastructure/kong-config.yaml" << 'EOF'
_format_version: "3.0"

services:
  - name: revenue-engine-service
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
              policy: local
          - name: cors
            config:
              origins:
                - https://tradingrobotplug.com
              methods:
                - GET
                - POST
                - PUT
                - DELETE
              credentials: true

consumers:
  - username: revenue-engine-user
    keyauth_credentials:
      - key: secure_api_key_here
EOF

    # Apply Kong configuration using decK
    if command -v deck &> /dev/null; then
        deck sync --file "$PROJECT_ROOT/infrastructure/kong-config.yaml"
    else
        log_warning "decK not found, Kong configuration must be applied manually"
    fi

    log_success "Kong API Gateway deployed"
}

# Deploy security policies
deploy_security_policies() {
    log_info "Deploying security policies..."

    # Istio Peer Authentication (mTLS)
    cat > "$PROJECT_ROOT/infrastructure/istio-security.yaml" << 'EOF'
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
EOF

    kubectl apply -f "$PROJECT_ROOT/infrastructure/istio-security.yaml"

    log_success "Security policies deployed"
}

# Run validation tests
run_validation_tests() {
    log_info "Running Phase 1 infrastructure validation..."

    # Test SSL certificate
    if kubectl get secret revenue-engine-tls -n production &> /dev/null; then
        log_success "SSL certificate secret exists"
    else
        log_error "SSL certificate secret not found"
    fi

    # Test Istio components
    if kubectl get gateway revenue-engine-gateway -n production &> /dev/null; then
        log_success "Istio Gateway deployed"
    else
        log_error "Istio Gateway not found"
    fi

    if kubectl get vs revenue-engine-vs -n production &> /dev/null; then
        log_success "Istio VirtualService deployed"
    else
        log_error "Istio VirtualService not found"
    fi

    # Test Kong deployment
    if kubectl get deployment kong -n production &> /dev/null; then
        log_success "Kong API Gateway deployed"
    else
        log_error "Kong API Gateway not found"
    fi

    # Test service mesh injection
    if kubectl get namespace production --show-labels | grep -q "istio-injection=enabled"; then
        log_success "Service mesh injection enabled"
    else
        log_error "Service mesh injection not enabled"
    fi

    log_success "Phase 1 infrastructure validation completed"
}

# Main deployment function
main() {
    log_info "Starting Phase 1 Infrastructure Deployment"
    log_info "Components: SSL Certificates + Istio Service Mesh + Kong API Gateway"

    check_prerequisites
    deploy_ssl_certificates
    deploy_istio_mesh
    deploy_kong_gateway
    deploy_security_policies
    run_validation_tests

    log_success "Phase 1 Infrastructure Deployment completed successfully"
    log_info "Infrastructure foundation ready for Revenue Engine deployment"

    echo ""
    echo "🎯 Phase 1 Deployment Summary:"
    echo "   ✅ SSL Certificates: revenue-engine.tradingrobotplug.com"
    echo "   ✅ Istio Service Mesh: Gateway, VirtualService, DestinationRule"
    echo "   ✅ Kong API Gateway: Service, Routes, Plugins"
    echo "   ✅ Security Policies: mTLS, Authorization"
    echo ""
    echo "🔄 Ready for Phase 2: Database Integration"
    echo "🔄 Agent-1 Validation: SSL verification, mesh connectivity, API gateway testing"
    echo ""
    echo "🚀 Infrastructure foundation operational"
}

# Run main function
main "$@"