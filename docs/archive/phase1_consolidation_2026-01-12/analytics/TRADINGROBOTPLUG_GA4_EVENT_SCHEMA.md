# TradingRobotPlug.com GA4 Event Schema

**Created:** 2025-12-27
**Author:** Agent-5 (Business Intelligence Specialist)
**Status:** READY FOR IMPLEMENTATION
**Coordination:** Agent-7 (dashboard integration)

---

## Overview

This document defines the GA4 event schema for TradingRobotPlug.com dashboard analytics tracking. These events should be integrated into `dashboard.js` to enable performance analytics and user behavior insights.

---

## Core Dashboard Events

### 1. `dashboard_view`

**Trigger:** Dashboard page load complete

```javascript
gtag('event', 'dashboard_view', {
    'event_category': 'Dashboard',
    'event_label': 'Dashboard Load',
    'total_strategies': metrics.totalStrategies,
    'active_strategies': metrics.activeStrategies,
    'user_type': 'authenticated'
});
```

**Parameters:**
- `total_strategies` (number): Count of user strategies
- `active_strategies` (number): Currently active strategies
- `user_type` (string): 'authenticated' or 'guest'

---

### 2. `strategy_selected`

**Trigger:** User selects/filters by strategy

```javascript
gtag('event', 'strategy_selected', {
    'event_category': 'Dashboard',
    'event_label': strategyName,
    'strategy_id': strategyId,
    'strategy_type': strategyType
});
```

**Parameters:**
- `strategy_id` (string): Unique strategy identifier
- `strategy_type` (string): 'momentum', 'value', 'swing', etc.

---

### 3. `trade_expanded`

**Trigger:** User expands trade details row

```javascript
gtag('event', 'trade_expanded', {
    'event_category': 'Dashboard',
    'event_label': 'Trade Details View',
    'trade_id': tradeId,
    'symbol': symbol,
    'trade_type': 'BUY' | 'SELL'
});
```

**Parameters:**
- `trade_id` (string): Unique trade identifier
- `symbol` (string): Trading symbol (e.g., 'TSLA', 'SPY')
- `trade_type` (string): 'BUY' or 'SELL'

---

### 4. `chart_interaction`

**Trigger:** User interacts with performance charts

```javascript
gtag('event', 'chart_interaction', {
    'event_category': 'Dashboard',
    'event_label': chartType,
    'interaction_type': interactionType,
    'time_range': timeRange
});
```

**Parameters:**
- `chart_type` (string): 'performance', 'trades_distribution', 'win_loss', 'strategy_comparison'
- `interaction_type` (string): 'zoom', 'pan', 'hover', 'click'
- `time_range` (string): '1d', '1w', '1m', '3m', '1y', 'all'

---

### 5. `metrics_refresh`

**Trigger:** User manually refreshes metrics

```javascript
gtag('event', 'metrics_refresh', {
    'event_category': 'Dashboard',
    'event_label': 'Manual Refresh',
    'refresh_type': 'manual' | 'auto',
    'refresh_source': 'button' | 'pull_to_refresh'
});
```

**Parameters:**
- `refresh_type` (string): 'manual' or 'auto'
- `refresh_source` (string): UI element that triggered refresh

---

## Conversion Events

### 6. `strategy_created`

**Trigger:** User creates a new trading strategy

```javascript
gtag('event', 'strategy_created', {
    'event_category': 'Conversion',
    'event_label': 'New Strategy',
    'strategy_type': strategyType,
    'initial_capital': initialCapital,
    'risk_level': riskLevel
});
```

---

### 7. `export_report`

**Trigger:** User exports performance report

```javascript
gtag('event', 'export_report', {
    'event_category': 'Conversion',
    'event_label': exportFormat,
    'export_format': 'pdf' | 'csv' | 'xlsx',
    'report_type': 'performance' | 'trades' | 'summary'
});
```

---

### 8. `upgrade_click`

**Trigger:** User clicks upgrade/premium CTA

```javascript
gtag('event', 'upgrade_click', {
    'event_category': 'Conversion',
    'event_label': 'Premium Upgrade',
    'source_location': 'dashboard_header' | 'metrics_limit' | 'feature_gate',
    'current_plan': 'free' | 'basic'
});
```

---

## Engagement Events

### 9. `session_duration`

**Trigger:** Dashboard session ends (on unload)

```javascript
gtag('event', 'session_duration', {
    'event_category': 'Engagement',
    'event_label': 'Dashboard Session',
    'duration_seconds': sessionDuration,
    'pages_viewed': pagesViewed,
    'interactions': totalInteractions
});
```

---

### 10. `feature_discovery`

**Trigger:** User discovers/uses feature for first time

```javascript
gtag('event', 'feature_discovery', {
    'event_category': 'Engagement',
    'event_label': featureName,
    'feature_name': featureName,
    'discovery_method': 'click' | 'tooltip' | 'onboarding'
});
```

---

## Implementation Guide

### Integration Steps

1. **Add GA4 Script** (if not present)
```html
<!-- In header.php -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

2. **Add Events to dashboard.js**

In the Dashboard object, add event tracking methods:

```javascript
trackEvent: function(eventName, params) {
    if (typeof gtag !== 'undefined') {
        gtag('event', eventName, params);
    }
},
```

3. **Hook Events to User Actions**

Example for strategy selection:
```javascript
onStrategyChange: function(strategyId, strategyName) {
    this.trackEvent('strategy_selected', {
        'event_category': 'Dashboard',
        'event_label': strategyName,
        'strategy_id': strategyId
    });
    // ... existing logic
}
```

---

## Testing Checklist

- [ ] Verify GA4 script loads on dashboard
- [ ] Test `dashboard_view` fires on page load
- [ ] Test `strategy_selected` fires on filter change
- [ ] Test `trade_expanded` fires on row click
- [ ] Test `chart_interaction` fires on chart zoom/pan
- [ ] Test `metrics_refresh` fires on manual refresh
- [ ] Verify events appear in GA4 Realtime reports
- [ ] Validate parameter values are correctly passed

---

## GA4 Configuration Requirements

### Custom Dimensions to Create in GA4

1. `strategy_type` - Text
2. `trade_type` - Text
3. `chart_type` - Text
4. `export_format` - Text
5. `refresh_type` - Text

### Custom Metrics to Create in GA4

1. `total_strategies` - Number
2. `active_strategies` - Number
3. `duration_seconds` - Number
4. `interactions` - Number

---

## Coordination Notes

**For Agent-7:**
- This schema integrates with the dashboard.js WebSocket/polling updates
- Events should fire asynchronously to not block UI
- Consider debouncing chart_interaction events (1 per 500ms)
- Use try/catch around gtag calls to handle missing GA4

**For Agent-3:**
- GA4 Measurement ID needs to be configured in wp-config.php
- Ensure GA4 script is loaded before dashboard.js

---

**Document Status:** COMPLETE
**Next Steps:** Agent-7 implementation in dashboard.js

