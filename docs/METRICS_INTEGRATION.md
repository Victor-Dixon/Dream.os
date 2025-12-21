# Metrics Integration Guide

## Overview

The blog post template and reports now include real backtest performance metrics from the TSLA strategy.

## Metrics Included

### Profit Metrics
- **Initial Capital:** $1,000,000.00
- **Net Profit:** +$726,897.07 (+72.69%)
- **Gross Profit:** $1,003,137.17 (+100.31%)
- **Gross Loss:** $276,240.10 (-27.62%)

### Risk Metrics
- **Maximum Drawdown:** $33,992.48 (-2.03%)
- **Average Drawdown:** $14,170.88 (-1.42%)
- **Maximum Run-up:** $726,933.15 (+42.09%)
- **Average Run-up:** $44,280.70 (+4.43%)

### Comparison Metrics
- **Buy & Hold Return:** +$32,360.52 (+3.24%)
- **Strategy Outperformance:** +69.45% vs Buy & Hold

### Position Metrics
- **Maximum Contracts Held:** 1,897
- **Average Drawdown Duration:** 18 hours
- **Average Run-up Duration:** 1 day

## Where Metrics Appear

### Blog Posts
- **Backtest Performance Summary** section
- Two-column layout (Profit Metrics | Risk Metrics)
- Formatted currency and percentages

### Free Reports
- **Backtest Performance Overview** in Executive Summary
- Key metrics summary
- Performance highlights

### Premium Reports
- **Detailed Performance Metrics** section
- Profit analysis with profit factor
- Risk metrics with averages
- Position sizing details
- Buy & Hold comparison
- Full PineScript code

## Data Source

Metrics are stored in `TSLA_STRATEGY['backtest_metrics']` in `strategy_blog_automation.py`.

## Formatting

- Currency: `$1,000,000.00` format
- Percentages: `+72.69%` format (with +/- sign)
- Large numbers: Comma-separated (1,897 contracts)

## Updating Metrics

To update the metrics:
1. Edit `TSLA_STRATEGY['backtest_metrics']` in `strategy_blog_automation.py`
2. Regenerate blog posts: `python tools/strategy_blog_automation.py --site tradingrobotplug.com --generate-post`
3. Regenerate reports: `python tools/strategy_blog_automation.py --site tradingrobotplug.com --generate-report --premium`

