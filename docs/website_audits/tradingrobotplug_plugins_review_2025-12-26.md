# TradingRobotPlug Plugins Review & Integration Plan - 2025-12-26

## Plugins Reviewed

### 1. Trading Robot Service Plugin
**Location:** `wp-content/plugins/trading-robot-service/`  
**Status:** Basic structure exists, needs integration

**Current State:**
- Has database table: `wp_trading_robot_settings`
- Basic runner class with algorithm initialization
- Sample data display shortcode
- No stock data integration

**Integration Points:**
- ✅ Can now use `/wp-json/tradingrobotplug/v1/stock-data` endpoint
- ✅ Can query `wp_trp_stock_data` table directly
- ✅ Can use historical data for algorithm backtesting

**Recommended Updates:**
1. Update `display_trading_data()` shortcode to use real stock data
2. Integrate with stock data collection system
3. Use stored data for algorithm calculations
4. Add trading signals based on real data

### 2. TRP Paper Trading Stats Plugin
**Location:** `wp-content/plugins/trp-paper-trading-stats/`  
**Status:** Functional, can be enhanced

**Current State:**
- REST API endpoint: `/wp-json/trp/v1/paper-trading-stats`
- Fetches stats from Python service
- Shortcode: `[trp_trading_stats]`
- Frontend JavaScript for stats display

**Integration Points:**
- ✅ Can use stored stock data for performance calculations
- ✅ Can display real-time prices from database
- ✅ Can show historical performance using stored data

**Recommended Updates:**
1. Add stock data integration to stats calculations
2. Display current prices from `wp_trp_stock_data` table
3. Use historical data for performance metrics
4. Add primary symbols (TSLA, QQQ, SPY, NVDA) to stats

### 3. TRP Swarm Status Plugin
**Location:** `wp-content/plugins/trp-swarm-status/`  
**Status:** Status display plugin (not trading-related)

**Note:** This plugin is for swarm status display, not trading functionality.

## Integration Plan

### Phase 1: Immediate Integration (Complete)
✅ Stock data collection system implemented  
✅ Database table created  
✅ REST API endpoints available  
✅ Automated data collection scheduled  

### Phase 2: Plugin Integration (Next Steps)

#### Trading Robot Service Plugin
1. **Update `display_trading_data()` shortcode:**
   ```php
   public function display_trading_data($atts) {
       $symbol = $atts['symbol'] ?? 'TSLA';
       $response = wp_remote_get(rest_url("tradingrobotplug/v1/stock-data/{$symbol}"));
       $data = json_decode(wp_remote_retrieve_body($response), true);
       // Display real stock data
   }
   ```

2. **Add algorithm data source:**
   - Query stored stock data for algorithm inputs
   - Use historical data for backtesting
   - Calculate indicators from stored prices

3. **Add trading signals:**
   - Generate buy/sell signals based on real data
   - Use stored historical data for signal validation

#### Paper Trading Stats Plugin
1. **Enhance stats with real data:**
   - Display current prices from database
   - Calculate performance using stored historical data
   - Show primary symbols (TSLA, QQQ, SPY, NVDA) stats

2. **Add data source option:**
   - Option to use stored data vs. Python service
   - Fallback to Python service if database empty

## API Endpoints Available

### For Trading Plugins

1. **Get Latest Stock Data (All Symbols)**
   ```
   GET /wp-json/tradingrobotplug/v1/stock-data
   ```

2. **Get Historical Data (Single Symbol)**
   ```
   GET /wp-json/tradingrobotplug/v1/stock-data/{symbol}?days=30
   GET /wp-json/tradingrobotplug/v1/stock-data/TSLA?start_date=2025-11-26&end_date=2025-12-26
   ```

3. **Get Strategies (Primary Symbols)**
   ```
   GET /wp-json/tradingrobotplug/v1/strategies
   ```

## Database Access

**Table:** `wp_trp_stock_data`

**Direct Query Example:**
```php
global $wpdb;
$table = $wpdb->prefix . 'trp_stock_data';

// Get latest TSLA price
$latest = $wpdb->get_row(
    $wpdb->prepare(
        "SELECT * FROM $table WHERE symbol = 'TSLA' ORDER BY timestamp DESC LIMIT 1"
    )
);

// Get 30-day history
$history = $wpdb->get_results(
    $wpdb->prepare(
        "SELECT * FROM $table 
        WHERE symbol = 'TSLA' AND timestamp >= %s 
        ORDER BY timestamp ASC",
        date('Y-m-d H:i:s', strtotime('-30 days'))
    )
);
```

## Primary Symbols

**Focus Symbols:**
1. **TSLA** (Tesla) - Most important
2. **QQQ** (Invesco QQQ Trust)
3. **SPY** (SPDR S&P 500 ETF)
4. **NVDA** (NVIDIA)

**Data Collection:**
- Automated collection every 5 minutes
- Stored in `wp_trp_stock_data` table
- Available via REST API and direct database queries

## Next Actions

1. **Update Trading Robot Service Plugin** to use stored data
2. **Enhance Paper Trading Stats Plugin** with real stock prices
3. **Test data collection** on live site
4. **Monitor data quality** and collection reliability
5. **Add error handling** for API failures

## Status
✅ **Data Collection System:** Complete  
⏳ **Plugin Integration:** Ready for implementation  
📋 **Documentation:** Complete  

---

**Reviewed by:** Agent-4 (Captain)  
**Date:** 2025-12-26  
**Next Review:** After plugin integration


