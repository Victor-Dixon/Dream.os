<!-- SSOT Domain: core -->
/**
 * Dashboard Message History View Module - V2 Compliant
 * Handles message history visualization and statistics
 * 
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0
 * @license MIT
 */

/**
 * Render message history view
 * @param {Object} data - Dashboard data with message history
 * @returns {string} HTML content
 */
function renderMessageHistoryView(data) {
    const messages = data.message_history || [];
    const stats = calculateMessageStats(messages);

    return `
        <div class="row mb-4">
            <!-- Message Statistics Cards -->
            <div class="col-md-3">
                <div class="metric-card">
                    <div class="metric-value">${stats.total}</div>
                    <div class="metric-label">Total Messages</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="metric-card">
                    <div class="metric-value">${stats.today}</div>
                    <div class="metric-label">Today</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="metric-card">
                    <div class="metric-value">${stats.agents.length}</div>
                    <div class="metric-label">Active Agents</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="metric-card">
                    <div class="metric-value status-${getPriorityStatus(stats.urgent)}">${stats.urgent}</div>
                    <div class="metric-label">Urgent Messages</div>
                </div>
            </div>
        </div>

        <div class="row">
            <!-- Message Timeline -->
            <div class="col-md-8">
                <div class="card">
                    <div class="card-header">
                        <h5><i class="fas fa-history me-2"></i>Message Timeline</h5>
                        <div class="card-header-actions">
                            <input type="text" id="messageSearch" class="form-control form-control-sm" placeholder="Search messages..." style="width: 200px;">
                            <select id="messageFilter" class="form-select form-select-sm" style="width: 150px;">
                                <option value="all">All Messages</option>
                                <option value="urgent">Urgent Only</option>
                                <option value="today">Today</option>
                                <option value="week">This Week</option>
                            </select>
                        </div>
                    </div>
                    <div class="card-body" style="max-height: 600px; overflow-y: auto;">
                        <div id="messageTimeline">
                            ${renderMessageTimeline(messages)}
                        </div>
                    </div>
                </div>
            </div>

            <!-- Message Statistics -->
            <div class="col-md-4">
                <div class="card mb-3">
                    <div class="card-header">
                        <h5><i class="fas fa-chart-pie me-2"></i>By Type</h5>
                    </div>
                    <div class="card-body">
                        <canvas id="messageTypeChart" width="300" height="200"></canvas>
                    </div>
                </div>
                <div class="card">
                    <div class="card-header">
                        <h5><i class="fas fa-users me-2"></i>By Agent</h5>
                    </div>
                    <div class="card-body">
                        <canvas id="messageAgentChart" width="300" height="200"></canvas>
                    </div>
                </div>
            </div>
        </div>
    `;
}

/**
 * Render message timeline
 * @param {Array} messages - Array of message objects
 * @returns {string} HTML content
 */
function renderMessageTimeline(messages) {
    if (!messages || messages.length === 0) {
        return '<div class="text-center text-muted p-4">No messages found</div>';
    }

    return messages.map(msg => `
        <div class="message-item mb-3 p-3 border-start border-3 border-${getPriorityColor(msg.priority)}">
            <div class="d-flex justify-content-between align-items-start">
                <div class="flex-grow-1">
                    <div class="d-flex align-items-center mb-2">
                        <strong class="me-2">${escapeHtml(msg.from || 'Unknown')}</strong>
                        <i class="fas fa-arrow-right me-2 text-muted"></i>
                        <strong>${escapeHtml(msg.to || 'Unknown')}</strong>
                        <span class="badge bg-${getPriorityColor(msg.priority)} ms-2">${msg.priority || 'regular'}</span>
                    </div>
                    <div class="message-content text-muted mb-2">${escapeHtml(msg.content || '')}</div>
                    <div class="message-meta text-muted small">
                        <i class="fas fa-clock me-1"></i>${formatTimestamp(msg.timestamp)}
                        ${msg.message_type ? `<span class="ms-2"><i class="fas fa-tag me-1"></i>${msg.message_type}</span>` : ''}
                    </div>
                </div>
            </div>
        </div>
    `).join('');
}

/**
 * Calculate message statistics
 * @param {Array} messages - Array of message objects
 * @returns {Object} Statistics object
 */
function calculateMessageStats(messages) {
    const now = new Date();
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    const agents = new Set();
    let urgent = 0;
    let todayCount = 0;

    messages.forEach(msg => {
        if (msg.from) agents.add(msg.from);
        if (msg.to) agents.add(msg.to);
        if (msg.priority === 'urgent') urgent++;
        
        if (msg.timestamp) {
            const msgDate = new Date(msg.timestamp);
            if (msgDate >= today) todayCount++;
        }
    });

    return {
        total: messages.length,
        today: todayCount,
        urgent: urgent,
        agents: Array.from(agents)
    };
}

/**
 * Get priority color class
 * @param {string} priority - Message priority
 * @returns {string} Bootstrap color class
 */
function getPriorityColor(priority) {
    const colors = {
        'urgent': 'danger',
        'high': 'warning',
        'regular': 'info',
        'normal': 'secondary'
    };
    return colors[priority] || 'secondary';
}

/**
 * Get priority status class
 * @param {number} count - Count of urgent messages
 * @returns {string} Status class
 */
function getPriorityStatus(count) {
    if (count > 10) return 'critical';
    if (count > 5) return 'warning';
    return 'normal';
}

/**
 * Format timestamp for display
 * @param {string} timestamp - ISO timestamp
 * @returns {string} Formatted timestamp
 */
function formatTimestamp(timestamp) {
    if (!timestamp) return 'Unknown';
    try {
        const date = new Date(timestamp);
        const now = new Date();
        const diff = now - date;
        const minutes = Math.floor(diff / 60000);
        
        if (minutes < 1) return 'Just now';
        if (minutes < 60) return `${minutes}m ago`;
        if (minutes < 1440) return `${Math.floor(minutes / 60)}h ago`;
        return date.toLocaleDateString();
    } catch (e) {
        return timestamp;
    }
}

/**
 * Escape HTML to prevent XSS
 * @param {string} text - Text to escape
 * @returns {string} Escaped text
 */
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Export for use in dashboard system
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        renderMessageHistoryView,
        renderMessageTimeline,
        calculateMessageStats
    };
}


