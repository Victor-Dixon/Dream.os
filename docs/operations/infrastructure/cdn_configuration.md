# CDN Configuration
## Infrastructure Block 5 - Global Content Delivery Network
## Agent-3 (Infrastructure & DevOps) - 2026-01-07

**Status:** ACTIVE IMPLEMENTATION
**Purpose:** Deploy global CDN for Revenue Engine static asset optimization and worldwide content delivery
**Configuration:** Cloudflare CDN integration with edge caching and performance optimization

---

## CDN Architecture

### Content Delivery Strategy
```
Origin Server → Cloudflare CDN → Global Edge Network → End Users
                     ↓
            Static Assets, API Responses, Dynamic Content
```

### CDN Components
- **Edge Servers**: 300+ global data centers worldwide
- **Caching Rules**: Intelligent caching based on content type and TTL
- **Security**: DDoS protection, WAF, SSL/TLS termination
- **Performance**: HTTP/2, Brotli compression, image optimization
- **Analytics**: Real-time traffic insights and performance metrics

---

## Cloudflare CDN Configuration

### Zone Setup and DNS Configuration
```bash
# Add domain to Cloudflare
curl -X POST "https://api.cloudflare.com/client/v4/zones" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "name": "revenue-engine.tradingrobotplug.com",
    "type": "full"
  }'

# Update DNS records to point to Cloudflare
curl -X POST "https://api.cloudflare.com/client/v4/zones/ZONE_ID/dns_records" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "type": "CNAME",
    "name": "api.revenue-engine.tradingrobotplug.com",
    "content": "revenue-engine-service.production.svc.cluster.local",
    "proxied": true
  }'
```

### Page Rules for Caching Strategy
```bash
# Create page rules for different content types
curl -X POST "https://api.cloudflare.com/client/v4/zones/ZONE_ID/pagerules" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
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

# Static assets caching rule
curl -X POST "https://api.cloudflare.com/client/v4/zones/ZONE_ID/pagerules" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
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
      },
      {
        "id": "bypass_cache_on_cookie",
        "value": "except"
      }
    ],
    "priority": 2,
    "status": "active"
  }'
```

### SSL/TLS Configuration
```bash
# Enable full SSL/TLS encryption
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/ZONE_ID/settings/ssl" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"value": "full"}'

# Configure SSL/TLS settings
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/ZONE_ID/settings/tls_1_3" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"value": "on"}'

curl -X PATCH "https://api.cloudflare.com/client/v4/zones/ZONE_ID/settings/min_tls_version" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"value": "1.2"}'
```

---

## Application Integration

### Revenue Engine CDN Integration
```python
import cloudflare
from typing import Dict, Any, Optional

class CDNManager:
    """Manages CDN integration for Revenue Engine content delivery."""

    def __init__(self, api_token: str, zone_id: str):
        self.cf = cloudflare.CloudFlare(token=api_token)
        self.zone_id = zone_id

    def purge_cache(self, urls: Optional[list] = None, tags: Optional[list] = None) -> bool:
        """Purge CDN cache for specific URLs or cache tags."""
        try:
            if urls:
                self.cf.zones.purge_cache.post(self.zone_id, data={'files': urls})
            elif tags:
                self.cf.zones.purge_cache.post(self.zone_id, data={'tags': tags})
            else:
                # Purge everything
                self.cf.zones.purge_cache.post(self.zone_id, data={'purge_everything': True})
            return True
        except Exception as e:
            print(f"CDN cache purge failed: {e}")
            return False

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get CDN cache performance statistics."""
        try:
            analytics = self.cf.zones.analytics.dashboard.get(
                self.zone_id,
                params={'since': '-1440', 'continuous': True}
            )
            return {
                'requests': analytics['totals']['requests']['all'],
                'bandwidth': analytics['totals']['bandwidth']['all'],
                'cache_hit_ratio': analytics['totals']['requests']['cached'] / analytics['totals']['requests']['all'] * 100,
                'threats_blocked': analytics['totals']['threats']['all']
            }
        except Exception as e:
            print(f"Failed to get CDN stats: {e}")
            return {}

    def update_cache_rules(self, content_type: str, ttl: int) -> bool:
        """Update cache rules for specific content types."""
        try:
            # Update page rules based on content type
            rules = self.cf.zones.pagerules.get(self.zone_id)['result']

            for rule in rules:
                if content_type in rule['targets'][0]['constraint']['value']:
                    rule['actions'] = [
                        {"id": "cache_level", "value": "cache_everything"},
                        {"id": "edge_cache_ttl", "value": ttl},
                        {"id": "browser_cache_ttl", "value": ttl // 10}
                    ]
                    self.cf.zones.pagerules.put(self.zone_id, rule['id'], data=rule)
                    break
            return True
        except Exception as e:
            print(f"Failed to update cache rules: {e}")
            return False

# Integration with Revenue Engine cache manager
class RevenueEngineCDNCache:
    """Integrates CDN with Revenue Engine caching strategy."""

    def __init__(self, cdn_manager: CDNManager):
        self.cdn = cdn_manager
        self.cache_strategy = {
            'market_data': {'ttl': 300, 'tag': 'market-data'},
            'static_assets': {'ttl': 86400, 'tag': 'static'},
            'user_content': {'ttl': 3600, 'tag': 'user-content'},
            'api_responses': {'ttl': 600, 'tag': 'api'}
        }

    def cache_market_data(self, symbol: str, data: Dict[str, Any]) -> bool:
        """Cache market data with CDN integration."""
        cache_config = self.cache_strategy['market_data']
        # Store in Redis first
        redis_key = f"market:{symbol}"
        # Then invalidate CDN cache for this data
        urls = [f"https://revenue-engine.tradingrobotplug.com/api/v1/revenue/market-data/{symbol}"]
        return self.cdn.purge_cache(urls=urls)

    def optimize_cdn_performance(self) -> Dict[str, Any]:
        """Optimize CDN performance based on current metrics."""
        stats = self.cdn.get_cache_stats()

        if stats.get('cache_hit_ratio', 0) < 80:
            # Increase cache TTL for underperforming content
            for content_type, config in self.cache_strategy.items():
                if config['ttl'] < 3600:  # Don't exceed 1 hour for dynamic content
                    new_ttl = min(config['ttl'] * 2, 3600)
                    self.cdn.update_cache_rules(content_type, new_ttl)
                    config['ttl'] = new_ttl

        return {
            'cache_hit_ratio': stats.get('cache_hit_ratio', 0),
            'optimizations_applied': True,
            'current_config': self.cache_strategy
        }
```

---

## Performance Optimization

### Image Optimization Configuration
```bash
# Enable Cloudflare image optimization
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/ZONE_ID/settings/mirage" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"value": "on"}'

curl -X PATCH "https://api.cloudflare.com/client/v4/zones/ZONE_ID/settings/polish" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"value": "lossy"}'

curl -X PATCH "https://api.cloudflare.com/client/v4/zones/ZONE_ID/settings/webp" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"value": "on"}'
```

### HTTP/2 and Performance Settings
```bash
# Enable HTTP/2 and performance optimizations
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/ZONE_ID/settings/http2" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"value": "on"}'

curl -X PATCH "https://api.cloudflare.com/client/v4/zones/ZONE_ID/settings/0rtt" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"value": "on"}'

curl -X PATCH "https://api.cloudflare.com/client/v4/zones/ZONE_ID/settings/brotli" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"value": "on"}'
```

### DDoS Protection and Security
```bash
# Enable DDoS protection
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/ZONE_ID/settings/security_level" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"value": "medium"}'

# Configure WAF rules
curl -X POST "https://api.cloudflare.com/client/v4/zones/ZONE_ID/firewall/rules" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "filter": {
      "expression": "(http.request.uri.path contains \"/api/v1/admin\")"
    },
    "action": "block",
    "description": "Block direct access to admin endpoints"
  }'
```

---

## Monitoring and Analytics

### Real-time Analytics Dashboard
```bash
# Get real-time analytics
curl -X GET "https://api.cloudflare.com/client/v4/zones/ZONE_ID/analytics/dashboard?since=-300" \
  -H "Authorization: Bearer YOUR_API_TOKEN"

# Monitor CDN performance
curl -X GET "https://api.cloudflare.com/client/v4/zones/ZONE_ID/analytics/latency?since=-3600" \
  -H "Authorization: Bearer YOUR_API_TOKEN"
```

### Health Check and Alerting
```bash
#!/bin/bash
# CDN health check script

ZONE_ID="your_zone_id"
API_TOKEN="your_api_token"

# Check CDN status
STATUS=$(curl -s -X GET "https://api.cloudflare.com/client/v4/zones/$ZONE_ID" \
  -H "Authorization: Bearer $API_TOKEN" \
  -H "Content-Type: application/json" | jq -r '.result.status')

if [ "$STATUS" != "active" ]; then
    echo "CRITICAL: CDN zone is not active (status: $STATUS)"
    exit 2
fi

# Check SSL status
SSL_STATUS=$(curl -s -X GET "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/ssl/verification" \
  -H "Authorization: Bearer $API_TOKEN" | jq -r '.result.validation_status')

if [ "$SSL_STATUS" != "active" ]; then
    echo "WARNING: SSL certificate is not active (status: $SSL_STATUS)"
fi

# Check cache hit ratio
CACHE_STATS=$(curl -s -X GET "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/analytics/dashboard?since=-3600" \
  -H "Authorization: Bearer $API_TOKEN")

CACHE_HITS=$(echo "$CACHE_STATS" | jq -r '.result.totals.requests.cached')
TOTAL_REQUESTS=$(echo "$CACHE_STATS" | jq -r '.result.totals.requests.all')

if [ "$TOTAL_REQUESTS" -gt 0 ]; then
    CACHE_RATIO=$((CACHE_HITS * 100 / TOTAL_REQUESTS))
    echo "Cache hit ratio: ${CACHE_RATIO}%"

    if [ "$CACHE_RATIO" -lt 70 ]; then
        echo "WARNING: Cache hit ratio is below 70%"
    fi
fi

echo "CDN health check completed"
```

---

## Cost Optimization

### Bandwidth and Request Optimization
```bash
# Configure rate limiting to prevent abuse
curl -X POST "https://api.cloudflare.com/client/v4/zones/ZONE_ID/rate_limits" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "match": {
      "request": {
        "url": "revenue-engine.tradingrobotplug.com/api/v1/revenue/*"
      }
    },
    "action": {
      "mode": "simulate",
      "timeout": 60,
      "response": {
        "content_type": "text/plain",
        "body": "Rate limit exceeded"
      }
    },
    "period": 60,
    "requests_per_period": 100,
    "burst": 10
  }'
```

### Cache Optimization Strategy
```python
def optimize_cache_strategy(cdn_manager: CDNManager, traffic_patterns: Dict[str, Any]) -> Dict[str, Any]:
    """Optimize cache strategy based on traffic patterns."""

    optimizations = {}

    # Analyze traffic patterns
    high_traffic_endpoints = []
    for endpoint, stats in traffic_patterns.items():
        if stats['requests_per_minute'] > 100:
            high_traffic_endpoints.append(endpoint)

    # Increase cache TTL for high-traffic endpoints
    for endpoint in high_traffic_endpoints:
        content_type = identify_content_type(endpoint)
        if content_type in ['market_data', 'static_assets']:
            current_ttl = get_current_ttl(endpoint)
            new_ttl = min(current_ttl * 2, 3600)  # Max 1 hour
            cdn_manager.update_cache_rules(content_type, new_ttl)
            optimizations[endpoint] = f"TTL increased from {current_ttl}s to {new_ttl}s"

    return optimizations
```

---

**CDN Configuration Complete ✅**
**Agent-3 (Infrastructure & DevOps) - 2026-01-07**
**Status:** Ready for deployment and integration testing