# Message Queue Monitoring Requirements
**Date:** 2025-12-13  
**Author:** Agent-6 (Coordination & Communication Specialist)  
**Status:** Active Requirements Document

## Overview

This document defines monitoring requirements for the message queue system, including metrics, thresholds, and alerting criteria.

## Monitoring Objectives

1. **Performance Monitoring**: Track delivery times, throughput, and success rates
2. **Error Monitoring**: Detect stuck messages, failures, and processing issues
3. **Health Monitoring**: Assess overall queue health and capacity
4. **Baseline Tracking**: Compare current performance to established baselines

## Metrics Categories

### 1. Performance Metrics

#### Delivery Time Metrics
- **Average Delivery Time**: Mean time from queue entry to successful delivery
  - **Threshold**: Warning > 10s, Critical > 30s
  - **Measurement**: Per message, aggregated over time window
  
- **Median Delivery Time**: 50th percentile delivery time
  - **Threshold**: Warning > 8s, Critical > 20s
  
- **P95 Delivery Time**: 95th percentile delivery time
  - **Threshold**: Warning > 20s, Critical > 60s
  
- **P99 Delivery Time**: 99th percentile delivery time
  - **Threshold**: Warning > 30s, Critical > 120s

#### Throughput Metrics
- **Messages Per Second**: Rate of message processing
  - **Threshold**: Warning < 0.1 msg/s, Critical < 0.01 msg/s
  - **Measurement**: Rolling average over 5-minute window

- **Queue Processing Rate**: Messages processed per batch
  - **Threshold**: Warning < 1 msg/batch, Critical = 0 msg/batch

#### Success Rate Metrics
- **Overall Success Rate**: Percentage of successfully delivered messages
  - **Threshold**: Warning < 95%, Critical < 90%
  - **Measurement**: Rolling window of last 100 messages
  
- **PyAutoGUI Success Rate**: Success rate for PyAutoGUI delivery method
  - **Threshold**: Warning < 90%, Critical < 80%
  
- **Inbox Success Rate**: Success rate for inbox fallback delivery
  - **Threshold**: Warning < 95%, Critical < 85%

### 2. Error Metrics

#### Stuck Message Detection
- **Stuck Messages**: Messages in PROCESSING status for extended period
  - **Threshold**: Warning > 60s, Critical > 300s (5 minutes)
  - **Alert**: Immediate notification when detected
  - **Action**: Auto-reset to PENDING for retry

#### Failure Metrics
- **Failure Rate**: Percentage of failed deliveries
  - **Threshold**: Warning > 5%, Critical > 10%
  - **Measurement**: Rolling window of last 100 messages
  
- **Permanent Failures**: Messages that failed after max retries
  - **Threshold**: Warning > 1%, Critical > 5%
  - **Alert**: Daily summary report

#### Retry Metrics
- **Average Retry Count**: Mean number of retry attempts per message
  - **Threshold**: Warning > 1.5, Critical > 2.0
  
- **Max Retry Exceeded**: Messages that exceeded max retry limit
  - **Threshold**: Warning > 0, Critical > 5 per hour

### 3. Capacity Metrics

#### Queue Size Metrics
- **Total Queue Size**: Number of messages in queue
  - **Threshold**: Warning > 500, Critical > 1000
  
- **Pending Messages**: Messages waiting for processing
  - **Threshold**: Warning > 200, Critical > 500
  
- **Processing Messages**: Messages currently being processed
  - **Threshold**: Warning > 50, Critical > 100

#### Age Metrics
- **Oldest Message Age**: Age of oldest pending message
  - **Threshold**: Warning > 1 hour, Critical > 6 hours
  
- **Average Message Age**: Mean age of all pending messages
  - **Threshold**: Warning > 30 minutes, Critical > 2 hours

### 4. Health Metrics

#### Queue Health Score
- **Overall Health**: Composite health score (0-100)
  - **Threshold**: Warning < 70, Critical < 50
  - **Components**: Success rate (40%), Delivery time (30%), Queue size (20%), Error rate (10%)

#### Processing Health
- **Processing Ratio**: Ratio of processing to total messages
  - **Threshold**: Warning > 50%, Critical > 75%
  - **Indicates**: Potential stuck messages or processing bottleneck

## Alerting Thresholds

### Critical Alerts (Immediate Action Required)
1. **Queue Processor Down**: No messages processed in 5 minutes
2. **Stuck Messages**: Messages stuck in PROCESSING > 5 minutes
3. **Critical Failure Rate**: Success rate < 90%
4. **Queue Overflow**: Queue size > 1000 messages
5. **Critical Delivery Time**: P99 delivery time > 120s

### Warning Alerts (Investigation Recommended)
1. **Elevated Failure Rate**: Success rate < 95%
2. **Slow Processing**: Average delivery time > 10s
3. **Queue Growth**: Queue size > 500 messages
4. **Stuck Messages**: Messages stuck in PROCESSING > 60s
5. **High Retry Rate**: Average retry count > 1.5

### Info Alerts (Monitoring)
1. **Baseline Deviation**: Performance metrics deviate > 20% from baseline
2. **Method Performance**: PyAutoGUI or Inbox success rate drops
3. **Capacity Warning**: Queue size > 200 messages

## Monitoring Implementation

### Real-Time Monitoring
- **Metrics Collection**: Automatic via `MessageQueuePerformanceMetrics`
- **Collection Frequency**: Per message delivery
- **Storage**: `message_queue/metrics.json` (last 1000 entries)

### Baseline Tracking
- **Baseline File**: `message_queue/baseline.json`
- **Capture Command**: `python tools/capture_performance_baseline.py`
- **Comparison Command**: `python tools/compare_performance_metrics.py`
- **Update Frequency**: After significant changes or weekly

### Stuck Message Detection
- **Detection Method**: Check PROCESSING status + timestamp
- **Detection Frequency**: Every 60 seconds
- **Auto-Recovery**: Reset to PENDING after timeout
- **Alert**: Immediate notification

### Health Checks
- **Check Frequency**: Every 5 minutes
- **Health Score Calculation**: Weighted composite of key metrics
- **Reporting**: Logged and available via API

## Monitoring Tools

### 1. Performance Metrics
- **Module**: `src/core/message_queue_performance_metrics.py`
- **Tool**: `tools/capture_performance_baseline.py`
- **Tool**: `tools/compare_performance_metrics.py`

### 2. Error Monitoring
- **Module**: `src/core/message_queue_error_monitor.py` (to be implemented)
- **Tool**: `tools/check_stuck_messages.py` (to be implemented)

### 3. Health Monitoring
- **Module**: `src/core/message_queue_statistics.py`
- **Method**: `QueueHealthMonitor.assess_health()`

## Reporting Requirements

### Daily Reports
- Total messages processed
- Success/failure rates
- Average delivery times
- Stuck message count
- Queue size trends

### Weekly Reports
- Performance trends vs baseline
- Error pattern analysis
- Capacity planning recommendations
- Health score trends

### On-Demand Reports
- Current queue status
- Performance comparison to baseline
- Stuck message details
- Error analysis

## Integration Points

### Metrics Collection
- Integrated into `MessageQueueProcessor._deliver_entry()`
- Automatic collection on every delivery attempt
- Non-blocking: failures don't affect message delivery

### Alerting
- Log-based alerts (INFO, WARNING, ERROR levels)
- File-based alerts (`message_queue/alerts.json`)
- Discord integration (future)

### Dashboard
- Real-time metrics display (future)
- Historical trend visualization (future)
- Health score dashboard (future)

## Maintenance

### Baseline Updates
- Update baseline after significant system changes
- Weekly baseline review recommended
- Document baseline changes with reasons

### Threshold Tuning
- Review thresholds monthly
- Adjust based on observed patterns
- Document threshold changes

### Monitoring Review
- Quarterly review of monitoring effectiveness
- Update requirements based on system evolution
- Remove obsolete metrics, add new ones as needed

## Compliance

- **V2 Compliance**: All monitoring code follows V2 standards
- **SSOT Domain**: Communication (message queue system)
- **Documentation**: This document is the SSOT for monitoring requirements





