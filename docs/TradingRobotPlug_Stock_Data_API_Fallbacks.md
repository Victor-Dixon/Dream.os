# TradingRobotPlug Stock Data API Fallback System

## Overview

The stock data API now includes multiple fallback mechanisms to ensure reliable data fetching when the primary API (Yahoo Finance) is unavailable.

## Fallback Chain

The system tries APIs in this order:

1. **Yahoo Finance (Primary)** - `query1.finance.yahoo.com`
   - Free, no API key required
   - Primary data source

2. **Yahoo Finance (Alternative)** - `query2.finance.yahoo.com`
   - Free, no API key required
   - First fallback if primary endpoint fails

3. **Alpha Vantage (Optional)**
   - Requires API key
   - Free tier: 5 API calls per minute, 500 per day
   - Get API key: https://www.alphavantage.co/support/#api-key
   - WordPress option: `trp_alpha_vantage_api_key`

4. **IEX Cloud (Optional)**
   - Requires API key
   - Free tier: 50,000 messages/month
   - Get API key: https://iexcloud.io/console/
   - WordPress option: `trp_iex_cloud_api_key`

5. **Cached Data (Last Resort)**
   - Uses stale data from database if available
   - Ensures site doesn't break completely if all APIs fail

## Configuration

### Alpha Vantage API Key

To enable Alpha Vantage fallback:

```php
// In WordPress admin or via WP-CLI:
update_option('trp_alpha_vantage_api_key', 'YOUR_API_KEY_HERE');
```

Or via WP-CLI:
```bash
wp option update trp_alpha_vantage_api_key 'YOUR_API_KEY_HERE' --site=tradingrobotplug.com
```

### IEX Cloud API Key

To enable IEX Cloud fallback:

```php
// In WordPress admin or via WP-CLI:
update_option('trp_iex_cloud_api_key', 'YOUR_API_KEY_HERE');
```

Or via WP-CLI:
```bash
wp option update trp_iex_cloud_api_key 'YOUR_API_KEY_HERE' --site=tradingrobotplug.com
```

## API Response Format

All APIs return data in a consistent format:

```php
array(
    'symbol' => 'TSLA',
    'price' => 250.50,
    'previous_close' => 248.75,
    'change' => 1.75,
    'change_percent' => 0.70,
    'volume' => 50000000,
    'market_cap' => 800000000000, // May be null for some APIs
    'timestamp' => '2025-12-30 22:30:00',
    'source' => 'yahoo_finance', // or 'yahoo_finance_alt', 'alpha_vantage', 'iex_cloud', 'cached_fallback'
)
```

## Error Handling

- All APIs include proper error handling and logging
- Errors are logged to WordPress error log
- Failed APIs automatically fall through to next in chain
- Cache fallback ensures site remains functional even if all APIs fail

## Rate Limiting

- **Yahoo Finance**: No official limit, but be respectful
- **Alpha Vantage Free**: 5 calls/minute, 500 calls/day
- **IEX Cloud Free**: 50,000 messages/month
- **Cached Data**: No rate limits (reads from database)

## Monitoring

Check WordPress error logs to see which API is being used:

```
TradingRobotPlug: Using Alpha Vantage for TSLA
TradingRobotPlug: Using IEX Cloud for QQQ
TradingRobotPlug: Using cached/stale data for SPY (all APIs failed)
```

## Recommendations

1. **Start with Yahoo Finance** (already active, no setup needed)
2. **Add Alpha Vantage** for free fallback (5 calls/min limit)
3. **Add IEX Cloud** for production reliability (50k messages/month free tier)
4. **Monitor error logs** to see which APIs are being used

## Testing

To test the fallback system:

1. Temporarily disable Yahoo Finance by blocking the endpoint
2. Check error logs to see fallback activation
3. Verify data still loads from fallback APIs
4. Test with API keys configured vs. without

## Future Enhancements

- Add more free APIs (Polygon.io, Finnhub, etc.)
- Implement caching strategy to reduce API calls
- Add admin UI for API key configuration
- Add API usage metrics and monitoring dashboard


