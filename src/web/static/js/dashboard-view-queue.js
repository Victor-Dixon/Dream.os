<!-- SSOT Domain: core -->
/**
 * Dashboard Queue Status View Module - V2 Compliant
 * Handles message queue status monitoring and visualization
 * 
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0
 * @license MIT
 */

/**
 * Render queue status view
 * @param {Object} data - Dashboard data with queue status
 * @returns {string} HTML content
 */
function renderQueueStatusView(data) {
    const queue = data.queue_status || {};
    const stats = calculateQueueStats(queue);

    return `
        <div class="row mb-4">
            <!-- Queue Statistics Cards -->
            <div class="col-md-3">
                <div class="metric-card">
                    <div class="metric-value status-${getQueueStatusClass(stats.pending)}">${stats.pending}</div>
                    <div class="metric-label">Pending Messages</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="metric-card">
                    <div class="metric-value status-healthy">${stats.delivered}</div>
                    <div class="metric-label">Delivered</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="metric-card">
                    <div class="metric-value status-${stats.failed > 0 ? 'error' : 'healthy'}">${stats.failed}</div>
                    <div class="metric-label">Failed</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="metric-card">
                    <div class="metric-value">${stats.total}</div>
                    <div class="metric-label">Total Processed</div>
                </div>
            </div>
        </div>

        <div class="row mb-4">
            <!-- Queue Health Metrics -->
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h5><i class="fas fa-heartbeat me-2"></i>Queue Health</h5>
                        <button class="btn btn-sm btn-primary" onclick="refreshQueueData()">
                            <i class="fas fa-sync-alt"></i> Refresh
                        </button>
                    </div>
                    <div class="card-body">
                        <div class="mb-3">
                            <div class="d-flex justify-content-between mb-1">
                                <span>Processing Rate</span>
                                <span class="text-muted">${stats.processing_rate}/min</span>
                            </div>
                            <div class="progress" style="height: 20px;">
                                <div class="progress-bar bg-success" role="progressbar" 
                                     style="width: ${Math.min(stats.processing_rate * 10, 100)}%">
                                    ${stats.processing_rate}/min
                                </div>
                            </div>
                        </div>
                        <div class="mb-3">
                            <div class="d-flex justify-content-between mb-1">
                                <span>Success Rate</span>
                                <span class="text-muted">${stats.success_rate}%</span>
                            </div>
                            <div class="progress" style="height: 20px;">
                                <div class="progress-bar bg-${getSuccessRateColor(stats.success_rate)}" 
                                     role="progressbar" style="width: ${stats.success_rate}%">
                                    ${stats.success_rate}%
                                </div>
                            </div>
                        </div>
                        <div>
                            <div class="d-flex justify-content-between mb-1">
                                <span>Queue Depth</span>
                                <span class="text-muted">${stats.pending} messages</span>
                            </div>
                            <div class="progress" style="height: 20px;">
                                <div class="progress-bar bg-${getQueueDepthColor(stats.pending)}" 
                                     role="progressbar" style="width: ${Math.min(stats.pending * 5, 100)}%">
                                    ${stats.pending}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Queue Operations -->
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h5><i class="fas fa-cog me-2"></i>Queue Operations</h5>
                    </div>
                    <div class="card-body">
                        <div class="mb-3">
                            <strong>Blocking Operations:</strong>
                            <div class="mt-2">
                                ${stats.blocking_operations > 0 
                                    ? `<span class="badge bg-warning">${stats.blocking_operations} active</span>`
                                    : '<span class="badge bg-success">None</span>'}
                            </div>
                        </div>
                        <div class="mb-3">
                            <strong>Average Wait Time:</strong>
                            <div class="mt-2">
                                <span class="text-muted">${stats.avg_wait_time}ms</span>
                            </div>
                        </div>
                        <div class="mb-3">
                            <strong>Peak Queue Depth:</strong>
                            <div class="mt-2">
                                <span class="text-muted">${stats.peak_depth} messages</span>
                            </div>
                        </div>
                        <div>
                            <button class="btn btn-sm btn-warning" onclick="clearFailedMessages()">
                                <i class="fas fa-trash"></i> Clear Failed
                            </button>
                            <button class="btn btn-sm btn-info" onclick="retryFailedMessages()">
                                <i class="fas fa-redo"></i> Retry Failed
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="row">
            <!-- Queue Timeline -->
            <div class="col-md-12">
                <div class="card">
                    <div class="card-header">
                        <h5><i class="fas fa-history me-2"></i>Recent Queue Activity</h5>
                        <div class="card-header-actions">
                            <select id="queueFilter" class="form-select form-select-sm" style="width: 150px;">
                                <option value="all">All Events</option>
                                <option value="pending">Pending Only</option>
                                <option value="delivered">Delivered Only</option>
                                <option value="failed">Failed Only</option>
                            </select>
                        </div>
                    </div>
                    <div class="card-body" style="max-height: 400px; overflow-y: auto;">
                        <div id="queueTimeline">
                            ${renderQueueTimeline(queue.recent_events || [])}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

/**
 * Calculate queue statistics
 * @param {Object} queue - Queue data object
 * @returns {Object} Statistics object
 */
function calculateQueueStats(queue) {
    const pending = queue.pending || 0;
    const delivered = queue.delivered || 0;
    const failed = queue.failed || 0;
    const total = queue.total || (pending + delivered + failed);
    
    const success_rate = total > 0 ? Math.round((delivered / total) * 100) : 100;
    const processing_rate = queue.processing_rate || 0;
    const blocking_operations = queue.blocking_operations || 0;
    const avg_wait_time = queue.avg_wait_time || 0;
    const peak_depth = queue.peak_depth || 0;

    return {
        pending,
        delivered,
        failed,
        total,
        success_rate,
        processing_rate,
        blocking_operations,
        avg_wait_time,
        peak_depth
    };
}

/**
 * Render queue timeline
 * @param {Array} events - Queue event array
 * @returns {string} HTML content
 */
function renderQueueTimeline(events) {
    if (events.length === 0) {
        return '<div class="text-center text-muted py-5">No queue events available</div>';
    }

    const sortedEvents = [...events].sort((a, b) => 
        new Date(b.timestamp) - new Date(a.timestamp)
    );

    return sortedEvents.map(event => `
        <div class="queue-event-item mb-2 p-2 border rounded">
            <div class="d-flex justify-content-between align-items-start">
                <div>
                    <strong>${event.type || 'Unknown'}</strong>
                    <span class="badge bg-${getEventStatusColor(event.status)} ms-2">${event.status || 'unknown'}</span>
                    ${event.agent_id ? `<span class="text-muted ms-2">→ ${event.agent_id}</span>` : ''}
                </div>
                <small class="text-muted">${formatTimestamp(event.timestamp)}</small>
            </div>
            ${event.message ? `<div class="mt-1"><small>${event.message}</small></div>` : ''}
        </div>
    `).join('');
}

/**
 * Get event status color
 * @param {string} status - Event status
 * @returns {string} Bootstrap color class
 */
function getEventStatusColor(status) {
    const colors = {
        'delivered': 'success',
        'pending': 'warning',
        'failed': 'danger',
        'processing': 'info'
    };
    return colors[status] || 'secondary';
}

/**
 * Get queue status class
 * @param {number} pending - Pending count
 * @returns {string} Status class
 */
function getQueueStatusClass(pending) {
    if (pending === 0) return 'healthy';
    if (pending < 10) return 'warning';
    return 'error';
}

/**
 * Get success rate color
 * @param {number} rate - Success rate percentage
 * @returns {string} Bootstrap color class
 */
function getSuccessRateColor(rate) {
    if (rate >= 95) return 'success';
    if (rate >= 80) return 'warning';
    return 'danger';
}

/**
 * Get queue depth color
 * @param {number} depth - Queue depth
 * @returns {string} Bootstrap color class
 */
function getQueueDepthColor(depth) {
    if (depth === 0) return 'success';
    if (depth < 10) return 'warning';
    return 'danger';
}

/**
 * Format timestamp
 * @param {string|Date} timestamp - Timestamp to format
 * @returns {string} Formatted timestamp
 */
function formatTimestamp(timestamp) {
    if (!timestamp) return 'Unknown';
    const date = new Date(timestamp);
    return date.toLocaleString();
}

/**
 * Refresh queue data
 */
async function refreshQueueData() {
    const refreshBtn = document.querySelector('button[onclick="refreshQueueData()"]');
    const originalText = refreshBtn?.innerHTML;
    
    try {
        // Show loading state
        if (refreshBtn) {
            refreshBtn.disabled = true;
            refreshBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Refreshing...';
        }
        
        const response = await fetch('/api/messages/queue');
        const data = await response.json();
        
        if (data.success) {
            // Reload the view with new data
            if (window.loadDashboardData) {
                window.loadDashboardData('queue_status');
            }
            
            // Show success feedback
            if (refreshBtn) {
                refreshBtn.innerHTML = '<i class="fas fa-check"></i> Refreshed';
                setTimeout(() => {
                    if (refreshBtn) {
                        refreshBtn.innerHTML = originalText;
                        refreshBtn.disabled = false;
                    }
                }, 2000);
            }
        }
    } catch (error) {
        console.error('Failed to refresh queue data:', error);
        if (refreshBtn) {
            refreshBtn.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Error';
            setTimeout(() => {
                if (refreshBtn) {
                    refreshBtn.innerHTML = originalText;
                    refreshBtn.disabled = false;
                }
            }, 2000);
        }
    }
}

/**
 * Clear failed messages
 */
async function clearFailedMessages() {
    if (!confirm('Are you sure you want to clear all failed messages?')) return;
    
    try {
        const response = await fetch('/api/messages/queue/clear-failed', { method: 'POST' });
        const data = await response.json();
        
        if (data.success) {
            alert('Failed messages cleared');
            refreshQueueData();
        }
    } catch (error) {
        console.error('Failed to clear failed messages:', error);
    }
}

/**
 * Retry failed messages
 */
async function retryFailedMessages() {
    try {
        const response = await fetch('/api/messages/queue/retry-failed', { method: 'POST' });
        const data = await response.json();
        
        if (data.success) {
            alert(`Retrying ${data.count || 0} failed messages`);
            refreshQueueData();
        }
    } catch (error) {
        console.error('Failed to retry failed messages:', error);
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { renderQueueStatusView };
}

