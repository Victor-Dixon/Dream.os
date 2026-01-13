# Trading Robot API Integration Roadmap

**Author:** Agent-4 (Captain)  
**Date:** 2025-12-27  
**Status:** ACTIVE - Integration Planning  
**Purpose:** Integration roadmap between Trading Robot API and TradingRobotPlug.com WordPress REST API

---

## Executive Summary

This document outlines the integration strategy between two complementary trading systems:

1. **Trading Robot API** (FastAPI, Python) - Trading execution engine
2. **TradingRobotPlug.com WordPress REST API** - Stock data collection and storage

---

## System Overview

### Architecture Clarification

There are **two separate systems** that need to integrate:

1. **Trading Robot Backend API** (Python/FastAPI) - Core trading engine
2. **TradingRobotPlug.com WordPress REST API** - WordPress frontend integration

### Trading Robot Backend API (Agent-2 Documentation)
- **Location:** `websites/TradingRobotPlugWeb/backend/`
- **Base URL:** `http://localhost:8000`
- **Framework:** FastAPI
- **Purpose:** Core trading engine, strategy execution, order management, portfolio management
- **Endpoints:**
  - `/api/status` - System status (market state, portfolio value, positions)
  - `/api/portfolio` - Portfolio information (positions, account details)
  - `/api/market_data/{symbol}` - Market data (OHLCV) for symbol
  - `/api/trade/{symbol}/{side}` - Execute trade (buy/sell)
  - `/api/stop_trading` - Emergency stop trading
  - `ws://localhost:8000/ws/updates` - WebSocket real-time updates (5-second intervals)

### TradingRobotPlug.com WordPress REST API (Agent-4 Implementation)
- **Location:** `websites/tradingrobotplug.com/wp/wp-content/themes/tradingrobotplug-theme/inc/`
- **Base URL:** `https://tradingrobotplug.com/wp-json/tradingrobotplug/v1`
- **Framework:** WordPress REST API
- **Purpose:** WordPress frontend integration, stock data storage, dashboard data, plugin integration
- **Key Endpoints:**
  - `/stock-data` - Latest stock data for all primary symbols
  - `/stock-data/{symbol}` - Historical stock data for specific symbol
  - `/strategies` - Trading strategies for primary symbols
  - `/dashboard/overview` - Dashboard overview
  - `/trades` - List trades
  - `/performance` - Performance data
- **Database:** `wp_trp_stock_data` table (5-minute automated collection)
- **Primary Symbols:** TSLA, QQQ, SPY, NVDA

---

## Integration Architecture

### Data Flow

```
┌─────────────────────────────────┐
│  TradingRobotPlug.com           │
│  WordPress REST API              │
│  (Stock Data Collection)        │
└──────────────┬──────────────────┘
               │
               │ HTTP GET
               │ /stock-data/{symbol}
               │
               ▼
┌─────────────────────────────────┐
│  Trading Robot API               │
│  (Trading Execution Engine)      │
│                                  │
│  - Fetches stock data            │
│  - Executes trades              │
│  - Manages portfolio            │
│  - Real-time WebSocket updates  │
└─────────────────────────────────┘
```

### Integration Points

#### 1. Market Data Integration
**Trading Robot API** → **WordPress REST API**

The Trading Robot API's `/api/market_data/{symbol}` endpoint should fetch data from WordPress REST API:

```python
# Trading Robot API implementation
import requests

def get_market_data(symbol: str, timeframe: str = "5Min", limit: int = 100):
    """Fetch market data from WordPress REST API."""
    base_url = "https://tradingrobotplug.com/wp-json/tradingrobotplug/v1"
    
    # Get historical data
    response = requests.get(
        f"{base_url}/stock-data/{symbol}",
        params={
            "days": limit,  # Convert timeframe to days
            "symbol": symbol
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        # Transform WordPress API format to Trading Robot API format
        return transform_to_ohlcv(data)
    else:
        raise Exception(f"Failed to fetch market data: {response.status_code}")
```

#### 2. Real-Time Price Updates
**WordPress REST API** → **Trading Robot Backend API**

The Trading Robot Backend API can poll WordPress REST API for latest prices:

```python
# Trading Robot API - Real-time price updates
async def update_prices():
    """Poll WordPress REST API for latest stock prices."""
    base_url = "https://tradingrobotplug.com/wp-json/tradingrobotplug/v1"
    
    response = requests.get(f"{base_url}/stock-data")
    if response.status_code == 200:
        data = response.json()
        for stock in data['stock_data']:
            # Update internal price cache
            update_price_cache(stock['symbol'], stock['price'])
```

#### 3. Plugin Integration
**WordPress Plugins** ↔ **Trading Robot Backend API**

WordPress plugins can use Trading Robot Backend API for trading execution, and Trading Robot Backend can send trade/performance data back to WordPress:

```php
// WordPress Plugin - Execute trade via Trading Robot API
function execute_trade($symbol, $side, $quantity) {
    $trading_api_url = 'http://localhost:8000/api/trade';
    
    $response = wp_remote_post(
        "{$trading_api_url}/{$symbol}/{$side}",
        array(
            'body' => json_encode(array('quantity' => $quantity)),
            'headers' => array('Content-Type' => 'application/json')
        )
    );
    
    if (is_wp_error($response)) {
        return array('status' => 'error', 'message' => $response->get_error_message());
    }
    
    return json_decode(wp_remote_retrieve_body($response), true);
}
```

---

## Integration Validation Checklist

### ✅ Documentation Review
- [x] Trading Robot API documentation complete (Agent-2)
- [x] TradingRobotPlug.com REST API documented (Agent-4)
- [x] Integration roadmap created (Agent-4)

### ⏳ Implementation Tasks
- [ ] Trading Robot API: Add WordPress REST API client
- [ ] Trading Robot API: Implement market data fetching from WordPress
- [ ] Trading Robot API: Add real-time price polling
- [ ] WordPress Plugins: Add Trading Robot API client
- [ ] WordPress Plugins: Implement trade execution integration
- [ ] Testing: End-to-end integration testing
- [ ] Security: API authentication implementation
- [ ] Monitoring: Integration health checks

---

## Data Format Mapping

### WordPress API → Trading Robot API

**WordPress Format:**
```json
{
  "symbol": "TSLA",
  "price": 250.50,
  "timestamp": "2025-12-26 15:30:00"
}
```

**Trading Robot Format:**
```json
{
  "timestamp": "2025-12-26T15:30:00Z",
  "open": 250.00,
  "high": 251.00,
  "low": 249.50,
  "close": 250.50,
  "volume": 50000000
}
```

**Transformation Required:**
- Convert timestamp format (MySQL datetime → ISO 8601)
- Add OHLC fields (use price as close, derive others from historical data)
- Add volume field (from WordPress API if available)

---

## Security Considerations

### Current Status
- **Trading Robot API:** No authentication (local development)
- **WordPress REST API:** WordPress authentication (if configured)

### Future Implementation
1. **API Key Authentication:** Shared secret between systems
2. **OAuth 2.0:** For production deployment
3. **Rate Limiting:** Prevent abuse
4. **HTTPS:** Encrypt all API communications
5. **IP Whitelisting:** Restrict Trading Robot API access

---

## Performance Optimization

### Caching Strategy
- **Trading Robot API:** Cache WordPress API responses (5-minute TTL)
- **WordPress REST API:** Use WordPress transients for stock data
- **Database:** Optimize `wp_trp_stock_data` queries with indexes

### Polling Intervals
- **Market Data:** 5 minutes (matches WordPress collection interval)
- **Real-Time Updates:** 1-3 seconds (for active trading)
- **Portfolio Updates:** 10 seconds

---

## Error Handling

### Integration Error Scenarios

1. **WordPress API Unavailable**
   - Trading Robot API should use cached data
   - Log error and retry with exponential backoff
   - Fallback to direct market data source if available

2. **Trading Robot API Unavailable**
   - WordPress plugins should queue trade requests
   - Retry when API becomes available
   - Notify user of delayed execution

3. **Data Format Mismatch**
   - Validate data format before processing
   - Log transformation errors
   - Use default values for missing fields

---

## Testing Strategy

### Unit Tests
- WordPress API client in Trading Robot API
- Trading Robot API client in WordPress plugins
- Data transformation functions

### Integration Tests
- End-to-end data flow (WordPress → Trading Robot)
- Trade execution flow (WordPress Plugin → Trading Robot API)
- Real-time update flow (WebSocket → WordPress data)

### Performance Tests
- API response times
- Concurrent request handling
- Database query performance

---

## Deployment Plan

### Phase 1: Development Integration
1. Set up Trading Robot API development environment
2. Implement WordPress REST API client
3. Test integration locally
4. Validate data flow

### Phase 2: Staging Integration
1. Deploy Trading Robot API to staging
2. Configure WordPress REST API access
3. End-to-end integration testing
4. Performance testing

### Phase 3: Production Deployment
1. Deploy Trading Robot API to production
2. Configure production WordPress REST API access
3. Enable authentication
4. Monitor integration health

---

## Monitoring & Maintenance

### Health Checks
- WordPress REST API availability
- Trading Robot API availability
- Data synchronization status
- Integration error rates

### Metrics to Track
- API response times
- Data freshness (time since last update)
- Trade execution success rate
- Integration error frequency

### Alerting
- WordPress API downtime
- Trading Robot API downtime
- Data synchronization failures
- High error rates

---

## Next Steps

1. **Immediate (Agent-4):**
   - Review API documentation for completeness
   - Validate integration points
   - Create implementation plan

2. **Short-term (Agent-2 + Agent-4):**
   - Implement WordPress REST API client in Trading Robot API
   - Add market data fetching integration
   - Test integration locally

3. **Medium-term:**
   - Implement authentication
   - Add error handling and retry logic
   - Performance optimization

4. **Long-term:**
   - Production deployment
   - Monitoring and alerting
   - Continuous integration testing

---

## References

- **Trading Robot API Documentation:** `docs/trading_robot/API_DOCUMENTATION.md` (Agent-2)
- **TradingRobotPlug.com Stock Data Collection:** `docs/website_audits/tradingrobotplug_stock_data_collection_2025-12-26.md` (Agent-4)
- **TradingRobotPlug.com Plugins Review:** `docs/website_audits/tradingrobotplug_plugins_review_2025-12-26.md` (Agent-4)

---

**Last Updated:** 2025-12-27 by Agent-4  
**Status:** ✅ ACTIVE - Integration Roadmap Complete  
**Next Review:** After Trading Robot API WordPress client implementation

