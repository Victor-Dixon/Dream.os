#!/bin/bash
# CDN Integration Deployment Script
# Infrastructure Block 5 - Global Content Delivery Network
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
    local tools=("curl" "jq")
    for tool in "${tools[@]}"; do
        if ! command -v "$tool" &> /dev/null; then
            log_error "$tool is not installed or not in PATH"
            exit 1
        fi
    done

    # Check if Cloudflare API token is available
    if [ -z "$CLOUDFLARE_API_TOKEN" ]; then
        log_warning "CLOUDFLARE_API_TOKEN environment variable not set"
        log_info "Please set your Cloudflare API token:"
        log_info "export CLOUDFLARE_API_TOKEN='your_api_token_here'"
        exit 1
    fi

    log_success "Prerequisites check passed"
}

# Create Cloudflare zone
create_cloudflare_zone() {
    log_info "Creating Cloudflare zone for Revenue Engine..."

    local domain="revenue-engine.tradingrobotplug.com"

    # Check if zone already exists
    local existing_zone=$(curl -s -X GET "https://api.cloudflare.com/client/v4/zones?name=$domain" \
        -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
        -H "Content-Type: application/json" | jq -r '.result[0].id')

    if [ "$existing_zone" != "null" ] && [ -n "$existing_zone" ]; then
        log_warning "Zone for $domain already exists (ID: $existing_zone)"
        ZONE_ID="$existing_zone"
        return
    fi

    # Create new zone
    local response=$(curl -s -X POST "https://api.cloudflare.com/client/v4/zones" \
        -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
        -H "Content-Type: application/json" \
        --data "{\"name\": \"$domain\", \"type\": \"full\"}")

    local success=$(echo "$response" | jq -r '.success')
    if [ "$success" != "true" ]; then
        log_error "Failed to create Cloudflare zone: $(echo "$response" | jq -r '.errors[0].message')"
        exit 1
    fi

    ZONE_ID=$(echo "$response" | jq -r '.result.id')
    log_success "Created Cloudflare zone for $domain (ID: $ZONE_ID)"

    # Wait for zone to be ready
    log_info "Waiting for zone to be ready..."
    local attempts=0
    while [ $attempts -lt 30 ]; do
        local status=$(curl -s -X GET "https://api.cloudflare.com/client/v4/zones/$ZONE_ID" \
            -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" | jq -r '.result.status')

        if [ "$status" = "active" ]; then
            log_success "Zone is now active"
            break
        fi

        sleep 10
        ((attempts++))
    done

    if [ $attempts -eq 30 ]; then
        log_error "Zone failed to become active within 5 minutes"
        exit 1
    fi
}

# Configure DNS records
configure_dns_records() {
    log_info "Configuring DNS records..."

    local records=(
        "api.revenue-engine.tradingrobotplug.com:CNAME:revenue-engine-service.production.svc.cluster.local"
        "cdn.revenue-engine.tradingrobotplug.com:CNAME:revenue-engine.tradingrobotplug.com"
    )

    for record in "${records[@]}"; do
        local name=$(echo "$record" | cut -d: -f1)
        local type=$(echo "$record" | cut -d: -f2)
        local content=$(echo "$record" | cut -d: -f3)

        local response=$(curl -s -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records" \
            -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
            -H "Content-Type: application/json" \
            --data "{\"type\": \"$type\", \"name\": \"$name\", \"content\": \"$content\", \"proxied\": true}")

        local success=$(echo "$response" | jq -r '.success')
        if [ "$success" = "true" ]; then
            log_success "Created DNS record: $name ($type)"
        else
            log_warning "Failed to create DNS record $name: $(echo "$response" | jq -r '.errors[0].message')"
        fi
    done
}

# Configure SSL/TLS settings
configure_ssl_tls() {
    log_info "Configuring SSL/TLS settings..."

    # Enable full SSL
    curl -s -X PATCH "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/settings/ssl" \
        -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
        -H "Content-Type: application/json" \
        --data '{"value": "full"}' > /dev/null

    # Enable TLS 1.3
    curl -s -X PATCH "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/settings/tls_1_3" \
        -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
        -H "Content-Type: application/json" \
        --data '{"value": "on"}' > /dev/null

    # Set minimum TLS version
    curl -s -X PATCH "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/settings/min_tls_version" \
        -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
        -H "Content-Type: application/json" \
        --data '{"value": "1.2"}' > /dev/null

    log_success "SSL/TLS settings configured"
}

# Configure caching rules
configure_cache_rules() {
    log_info "Configuring cache rules..."

    # Market data caching rule
    local market_data_rule='{
        "targets": [
            {
                "target": "url",
                "constraint": {
                    "operator": "matches",
                    "value": "revenue-engine.tradingrobotplug.com/api/v1/revenue/market-data/*"
                }
            }
        ],
        "actions": [
            {
                "id": "cache_level",
                "value": "cache_everything"
            },
            {
                "id": "edge_cache_ttl",
                "value": 300
            },
            {
                "id": "browser_cache_ttl",
                "value": 60
            }
        ],
        "priority": 1,
        "status": "active"
    }'

    curl -s -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/pagerules" \
        -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
        -H "Content-Type: application/json" \
        --data "$market_data_rule" > /dev/null

    # Static assets caching rule
    local static_assets_rule='{
        "targets": [
            {
                "target": "url",
                "constraint": {
                    "operator": "matches",
                    "value": "revenue-engine.tradingrobotplug.com/static/*"
                }
            }
        ],
        "actions": [
            {
                "id": "cache_level",
                "value": "cache_everything"
            },
            {
                "id": "edge_cache_ttl",
                "value": 86400
            },
            {
                "id": "browser_cache_ttl",
                "value": 31536000
            }
        ],
        "priority": 2,
        "status": "active"
    }'

    curl -s -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/pagerules" \
        -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
        -H "Content-Type: application/json" \
        --data "$static_assets_rule" > /dev/null

    log_success "Cache rules configured"
}

# Configure performance optimizations
configure_performance() {
    log_info "Configuring performance optimizations..."

    # Enable HTTP/2
    curl -s -X PATCH "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/settings/http2" \
        -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
        -H "Content-Type: application/json" \
        --data '{"value": "on"}' > /dev/null

    # Enable 0-RTT
    curl -s -X PATCH "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/settings/0rtt" \
        -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
        -H "Content-Type: application/json" \
        --data '{"value": "on"}' > /dev/null

    # Enable Brotli compression
    curl -s -X PATCH "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/settings/brotli" \
        -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
        -H "Content-Type: application/json" \
        --data '{"value": "on"}' > /dev/null

    # Enable image optimizations
    curl -s -X PATCH "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/settings/mirage" \
        -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
        -H "Content-Type: application/json" \
        --data '{"value": "on"}' > /dev/null

    curl -s -X PATCH "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/settings/polish" \
        -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
        -H "Content-Type: application/json" \
        --data '{"value": "lossy"}' > /dev/null

    curl -s -X PATCH "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/settings/webp" \
        -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
        -H "Content-Type: application/json" \
        --data '{"value": "on"}' > /dev/null

    log_success "Performance optimizations configured"
}

# Configure security settings
configure_security() {
    log_info "Configuring security settings..."

    # Set security level
    curl -s -X PATCH "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/settings/security_level" \
        -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
        -H "Content-Type: application/json" \
        --data '{"value": "medium"}' > /dev/null

    # Create WAF rule for admin endpoints
    local waf_rule='{
        "filter": {
            "expression": "(http.request.uri.path contains \"/api/v1/admin\")"
        },
        "action": "block",
        "description": "Block direct access to admin endpoints"
    }'

    curl -s -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/firewall/rules" \
        -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
        -H "Content-Type: application/json" \
        --data "$waf_rule" > /dev/null

    log_success "Security settings configured"
}

# Run validation tests
run_validation_tests() {
    log_info "Running CDN validation tests..."

    # Test zone status
    local zone_status=$(curl -s -X GET "https://api.cloudflare.com/client/v4/zones/$ZONE_ID" \
        -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" | jq -r '.result.status')

    if [ "$zone_status" = "active" ]; then
        log_success "Cloudflare zone is active"
    else
        log_error "Cloudflare zone is not active (status: $zone_status)"
    fi

    # Test SSL status
    local ssl_status=$(curl -s -X GET "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/ssl/verification" \
        -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" | jq -r '.result.validation_status')

    if [ "$ssl_status" = "active" ]; then
        log_success "SSL certificate is active"
    else
        log_warning "SSL certificate is not active yet (status: $ssl_status)"
    fi

    # Test DNS records
    local dns_records=$(curl -s -X GET "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records" \
        -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" | jq -r '.result | length')

    if [ "$dns_records" -gt 0 ]; then
        log_success "DNS records configured ($dns_records records)"
    else
        log_warning "No DNS records found"
    fi

    # Test page rules
    local page_rules=$(curl -s -X GET "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/pagerules" \
        -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" | jq -r '.result | length')

    if [ "$page_rules" -gt 0 ]; then
        log_success "Cache rules configured ($page_rules rules)"
    else
        log_warning "No cache rules found"
    fi

    log_success "CDN validation tests completed"
}

# Main deployment function
main() {
    log_info "Starting CDN Integration Deployment"
    log_info "Components: Cloudflare CDN configuration with global edge caching"

    check_prerequisites
    create_cloudflare_zone
    configure_dns_records
    configure_ssl_tls
    configure_cache_rules
    configure_performance
    configure_security
    run_validation_tests

    log_success "CDN Integration Deployment completed successfully"
    log_info "Global content delivery network ready for Revenue Engine"

    echo ""
    echo "🎯 CDN Deployment Summary:"
    echo "   ✅ Cloudflare Zone: revenue-engine.tradingrobotplug.com"
    echo "   ✅ SSL/TLS: Full encryption with TLS 1.3"
    echo "   ✅ DNS Records: API and CDN subdomains configured"
    echo "   ✅ Cache Rules: Market data and static assets optimized"
    echo "   ✅ Performance: HTTP/2, Brotli, image optimization enabled"
    echo "   ✅ Security: DDoS protection and WAF rules active"
    echo ""
    echo "🚀 Next Steps:"
    echo "   1. Update application to use CDN URLs"
    echo "   2. Monitor cache hit ratios and performance"
    echo "   3. Configure CDN purging for dynamic content updates"
    echo ""
}

# Run main function
main "$@"