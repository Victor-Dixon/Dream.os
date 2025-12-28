/**
 * Dashboard Agent Activity View Module - V2 Compliant
 * Handles agent activity tracking and visualization
 * 
 * <!-- SSOT Domain: web -->
 * 
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0
 * @license MIT
 * @see docs/WEB_DOMAIN_INDEX.md for navigation reference
 * @see src/web/vector_database/message_routes.py for API endpoint
 */

/**
 * Render agent activity view
 * @param {Object} data - Dashboard data with agent activity
 * @returns {string} HTML content
 */
function renderAgentActivityView(data) {
    const activity = data.agent_activity || [];
    const stats = calculateActivityStats(activity);

    return `
        <div class="row mb-4">
            <!-- Activity Statistics Cards -->
            <div class="col-md-3">
                <div class="metric-card">
                    <div class="metric-value">${stats.active_agents}</div>
                    <div class="metric-label">Active Agents</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="metric-card">
                    <div class="metric-value">${stats.total_actions}</div>
                    <div class="metric-label">Total Actions</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="metric-card">
                    <div class="metric-value">${stats.avg_response_time}ms</div>
                    <div class="metric-label">Avg Response Time</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="metric-card">
                    <div class="metric-value status-${getActivityStatus(stats.health_score)}">${stats.health_score}%</div>
                    <div class="metric-label">Health Score</div>
                </div>
            </div>
        </div>

        <div class="row">
            <!-- Agent Activity Timeline -->
            <div class="col-md-8">
                <div class="card">
                    <div class="card-header">
                        <h5><i class="fas fa-users me-2"></i>Agent Activity Timeline</h5>
                        <div class="card-header-actions">
                            <select id="activityFilter" class="form-select form-select-sm" style="width: 150px;">
                                <option value="all">All Agents</option>
                                <option value="active">Active Only</option>
                                <option value="idle">Idle Only</option>
                            </select>
                            <button class="btn btn-sm btn-primary" onclick="refreshActivityData()">
                                <i class="fas fa-sync-alt"></i> Refresh
                            </button>
                        </div>
                    </div>
                    <div class="card-body" style="max-height: 600px; overflow-y: auto;">
                        <div id="activityTimeline">
                            ${renderActivityTimeline(activity)}
                        </div>
                    </div>
                </div>
            </div>

            <!-- Agent Status List -->
            <div class="col-md-4">
                <div class="card mb-3">
                    <div class="card-header">
                        <h5><i class="fas fa-list me-2"></i>Agent Status</h5>
                    </div>
                    <div class="card-body">
                        <div id="agentStatusList">
                            ${renderAgentStatusList(activity)}
                        </div>
                    </div>
                </div>
                <div class="card">
                    <div class="card-header">
                        <h5><i class="fas fa-chart-line me-2"></i>Activity Trends</h5>
                    </div>
                    <div class="card-body">
                        <canvas id="activityTrendChart" width="300" height="200"></canvas>
                    </div>
                </div>
            </div>
        </div>
    `;
}

/**
 * Calculate activity statistics
 * @param {Array} activity - Activity data array
 * @returns {Object} Statistics object
 */
function calculateActivityStats(activity) {
    const activeAgents = new Set(activity.filter(a => a.status === 'active').map(a => a.agent_id));
    const totalActions = activity.reduce((sum, a) => sum + (a.action_count || 0), 0);
    const responseTimes = activity.filter(a => a.response_time).map(a => a.response_time);
    const avgResponseTime = responseTimes.length > 0
        ? Math.round(responseTimes.reduce((a, b) => a + b, 0) / responseTimes.length)
        : 0;

    const healthScore = activity.length > 0
        ? Math.round((activeAgents.size / 8) * 100)
        : 0;

    return {
        active_agents: activeAgents.size,
        total_actions: totalActions,
        avg_response_time: avgResponseTime,
        health_score: healthScore
    };
}

/**
 * Render activity timeline
 * @param {Array} activity - Activity data array
 * @returns {string} HTML content
 */
function renderActivityTimeline(activity) {
    if (activity.length === 0) {
        return '<div class="text-center text-muted py-5">No activity data available</div>';
    }

    const sortedActivity = [...activity].sort((a, b) =>
        new Date(b.timestamp || b.last_activity) - new Date(a.timestamp || a.last_activity)
    );

    return sortedActivity.map(item => `
        <div class="activity-item mb-3 p-3 border rounded">
            <div class="d-flex justify-content-between align-items-start">
                <div>
                    <strong>${item.agent_id || 'Unknown'}</strong>
                    <span class="badge bg-${getStatusColor(item.status)} ms-2">${item.status || 'unknown'}</span>
                </div>
                <small class="text-muted">${formatTimestamp(item.timestamp || item.last_activity)}</small>
            </div>
            ${item.action ? `<div class="mt-2"><i class="fas fa-tasks me-1"></i>${item.action}</div>` : ''}
            ${item.message_count ? `<div class="mt-1"><small>Messages: ${item.message_count}</small></div>` : ''}
        </div>
    `).join('');
}

/**
 * Render agent status list
 * @param {Array} activity - Activity data array
 * @returns {string} HTML content
 */
function renderAgentStatusList(activity) {
    const agents = ['Agent-1', 'Agent-2', 'Agent-3', 'Agent-4', 'Agent-5', 'Agent-6', 'Agent-7', 'Agent-8'];
    const activityMap = new Map(activity.map(a => [a.agent_id, a]));

    return agents.map(agentId => {
        const agentActivity = activityMap.get(agentId);
        const status = agentActivity?.status || 'idle';
        const lastActivity = agentActivity?.timestamp || agentActivity?.last_activity;

        return `
            <div class="agent-status-item d-flex justify-content-between align-items-center mb-2 p-2 border rounded">
                <div>
                    <strong>${agentId}</strong>
                    <span class="badge bg-${getStatusColor(status)} ms-2">${status}</span>
                </div>
                ${lastActivity ? `<small class="text-muted">${formatTimestamp(lastActivity)}</small>` : ''}
            </div>
        `;
    }).join('');
}

/**
 * Get status color class
 * @param {string} status - Status string
 * @returns {string} Bootstrap color class
 */
function getStatusColor(status) {
    const colors = {
        'active': 'success',
        'idle': 'secondary',
        'working': 'primary',
        'error': 'danger',
        'warning': 'warning'
    };
    return colors[status] || 'secondary';
}

/**
 * Get activity status class
 * @param {number} score - Health score
 * @returns {string} Status class
 */
function getActivityStatus(score) {
    if (score >= 80) return 'healthy';
    if (score >= 60) return 'warning';
    return 'error';
}

/**
 * Format timestamp
 * @param {string|Date} timestamp - Timestamp to format
 * @returns {string} Formatted timestamp
 */
function formatTimestamp(timestamp) {
    if (!timestamp) return 'Never';
    const date = new Date(timestamp);
    const now = new Date();
    const diff = now - date;
    const minutes = Math.floor(diff / 60000);

    if (minutes < 1) return 'Just now';
    if (minutes < 60) return `${minutes}m ago`;
    const hours = Math.floor(minutes / 60);
    if (hours < 24) return `${hours}h ago`;
    return date.toLocaleDateString();
}

/**
 * Refresh activity data
 */
async function refreshActivityData() {
    const refreshBtn = document.querySelector('button[onclick="refreshActivityData()"]');
    const originalText = refreshBtn?.innerHTML;

    try {
        // Show loading state
        if (refreshBtn) {
            refreshBtn.disabled = true;
            refreshBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Refreshing...';
        }

        const response = await fetch('/api/messages/activity');
        const data = await response.json();

        if (data.success) {
            const timeline = document.getElementById('activityTimeline');
            const statusList = document.getElementById('agentStatusList');

            if (timeline) {
                timeline.innerHTML = renderActivityTimeline(data.activity || []);
            }
            if (statusList) {
                statusList.innerHTML = renderAgentStatusList(data.activity || []);
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
        console.error('Failed to refresh activity data:', error);
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

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { renderAgentActivityView };
}

