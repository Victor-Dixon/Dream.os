<!-- SSOT Domain: core -->
/**
 * Dashboard Engine Discovery View - V2 Compliant
 * 
 * Displays discovered engines from Plugin Discovery Pattern
 * 
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0
 * @license MIT
 */

class EngineDiscoveryView {
    constructor() {
        this.engines = [];
        this.summary = {
            total: 0,
            active: 0,
            failed: 0,
            pending: 0
        };
        this.discoveryLog = [];
    }

    /**
     * Render engine discovery view
     * @param {Object} data - Optional pre-loaded data
     * @returns {Promise<string>} HTML content
     */
    async render(data = null) {
        try {
            // Fetch engine data from API if not provided
            if (!data) {
                data = await this.fetchEngineData();
            }

            // Update summary
            this.updateSummary(data);
            this.engines = data.engines || [];
            this.discoveryLog = data.discovery_log || [];

            // Render view
            return this.renderView();
        } catch (error) {
            console.error('Error rendering engine discovery view:', error);
            return this.renderError(error);
        }
    }

    /**
     * Fetch engine discovery data from API
     * @returns {Promise<Object>} Engine discovery data
     */
    async fetchEngineData() {
        const response = await fetch('/api/engines/discovery');
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        return await response.json();
    }

    /**
     * Update summary statistics
     * @param {Object} data - Engine discovery data
     */
    updateSummary(data) {
        this.summary = data.summary || {
            total: 0,
            active: 0,
            failed: 0,
            pending: 0
        };
    }

    /**
     * Render the complete view
     * @returns {string} HTML content
     */
    renderView() {
        return `
            <div class="engine-discovery-view">
                <div class="view-header mb-4">
                    <h2>🔌 Engine Discovery Dashboard</h2>
                    <p class="text-muted">Plugin Discovery Pattern - Auto-discovered engines</p>
                </div>
                
                ${this.renderSummaryCards()}
                ${this.renderBulkActions()}
                ${this.renderEngineList()}
                ${this.renderDiscoveryLog()}
            </div>
        `;
    }

    /**
     * Render summary cards
     * @returns {string} HTML for summary cards
     */
    renderSummaryCards() {
        return `
            <div class="row mb-4">
                <div class="col-md-3">
                    <div class="metric-card">
                        <div class="metric-value text-primary">${this.summary.total}</div>
                        <div class="metric-label">Total Engines</div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="metric-card">
                        <div class="metric-value status-healthy">${this.summary.active}</div>
                        <div class="metric-label">Active Engines</div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="metric-card">
                        <div class="metric-value status-warning">${this.summary.pending}</div>
                        <div class="metric-label">Pending Init</div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="metric-card">
                        <div class="metric-value status-critical">${this.summary.failed}</div>
                        <div class="metric-label">Failed Engines</div>
                    </div>
                </div>
            </div>
        `;
    }

    /**
     * Render bulk actions panel
     * @returns {string} HTML for bulk actions
     */
    renderBulkActions() {
        return `
            <div class="bulk-actions-panel mb-4">
                <div class="btn-group" role="group">
                    <button type="button" class="btn btn-primary" onclick="engineDiscoveryView.initializeAll()">
                        Initialize All
                    </button>
                    <button type="button" class="btn btn-secondary" onclick="engineDiscoveryView.refreshDiscovery()">
                        Refresh Discovery
                    </button>
                    <button type="button" class="btn btn-info" onclick="engineDiscoveryView.exportStatus()">
                        Export Status
                    </button>
                </div>
            </div>
        `;
    }

    /**
     * Render engine list
     * @returns {string} HTML for engine list
     */
    renderEngineList() {
        if (this.engines.length === 0) {
            return `
                <div class="alert alert-info">
                    <strong>No engines discovered.</strong> Check discovery logs for details.
                </div>
            `;
        }

        const engineRows = this.engines.map(engine => this.renderEngineRow(engine)).join('');

        return `
            <div class="engine-list-section mb-4">
                <h3>Discovered Engines</h3>
                <div class="table-responsive">
                    <table class="table table-hover">
                        <thead>
                            <tr>
                                <th>Engine Type</th>
                                <th>Class Name</th>
                                <th>Status</th>
                                <th>Initialized</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${engineRows}
                        </tbody>
                    </table>
                </div>
            </div>
        `;
    }

    /**
     * Render single engine row
     * @param {Object} engine - Engine data
     * @returns {string} HTML for engine row
     */
    renderEngineRow(engine) {
        const statusClass = this.getStatusClass(engine.status);
        const statusIcon = this.getStatusIcon(engine.status);
        const initializedBadge = engine.initialized
            ? '<span class="badge bg-success">Yes</span>'
            : '<span class="badge bg-secondary">No</span>';

        return `
            <tr>
                <td><strong>${engine.engine_type}</strong></td>
                <td><code>${engine.engine_class}</code></td>
                <td>
                    <span class="badge ${statusClass}">
                        ${statusIcon} ${engine.status}
                    </span>
                </td>
                <td>${initializedBadge}</td>
                <td>
                    <button class="btn btn-sm btn-primary" onclick="engineDiscoveryView.initializeEngine('${engine.engine_type}')">
                        Initialize
                    </button>
                    <button class="btn btn-sm btn-info" onclick="engineDiscoveryView.viewDetails('${engine.engine_type}')">
                        Details
                    </button>
                    ${engine.initialized ? `
                        <button class="btn btn-sm btn-warning" onclick="engineDiscoveryView.cleanupEngine('${engine.engine_type}')">
                            Cleanup
                        </button>
                    ` : ''}
                </td>
            </tr>
        `;
    }

    /**
     * Render discovery log
     * @returns {string} HTML for discovery log
     */
    renderDiscoveryLog() {
        if (this.discoveryLog.length === 0) {
            return '';
        }

        const logEntries = this.discoveryLog.map(log => `
            <div class="log-entry">
                <span class="log-timestamp">[${log.timestamp}]</span>
                <span class="log-level log-${log.level}">${log.level.toUpperCase()}</span>
                <span class="log-message">${log.message}</span>
            </div>
        `).join('');

        return `
            <div class="discovery-log-section">
                <h3>
                    Discovery Log
                    <button class="btn btn-sm btn-link" onclick="this.parentElement.nextElementSibling.classList.toggle('collapsed')">
                        Toggle
                    </button>
                </h3>
                <div class="discovery-log collapsed">
                    ${logEntries}
                </div>
            </div>
        `;
    }

    /**
     * Get status CSS class
     * @param {string} status - Engine status
     * @returns {string} CSS class
     */
    getStatusClass(status) {
        const classes = {
            'initialized': 'bg-success',
            'discovered': 'bg-info',
            'error': 'bg-danger',
            'pending': 'bg-warning'
        };
        return classes[status] || 'bg-secondary';
    }

    /**
     * Get status icon
     * @param {string} status - Engine status
     * @returns {string} Icon HTML
     */
    getStatusIcon(status) {
        const icons = {
            'initialized': '✅',
            'discovered': '🔍',
            'error': '❌',
            'pending': '⏳'
        };
        return icons[status] || '❓';
    }

    /**
     * Render error state
     * @param {Error} error - Error object
     * @returns {string} HTML for error
     */
    renderError(error) {
        return `
            <div class="alert alert-danger">
                <strong>Error loading engine discovery:</strong> ${error.message}
                <button class="btn btn-sm btn-primary mt-2" onclick="location.reload()">
                    Retry
                </button>
            </div>
        `;
    }

    /**
     * Initialize a specific engine
     * @param {string} engineType - Engine type
     */
    async initializeEngine(engineType) {
        try {
            const response = await fetch(`/api/engines/${engineType}/initialize`, {
                method: 'POST'
            });
            const result = await response.json();

            if (result.success) {
                alert(`Engine ${engineType} initialized successfully!`);
                await this.refreshView();
            } else {
                alert(`Failed to initialize engine: ${result.message}`);
            }
        } catch (error) {
            alert(`Error: ${error.message}`);
        }
    }

    /**
     * Initialize all engines
     */
    async initializeAll() {
        if (!confirm('Initialize all engines?')) {
            return;
        }

        try {
            const response = await fetch('/api/engines/initialize-all', {
                method: 'POST'
            });
            const result = await response.json();

            alert(`Initialized ${result.summary.successful} of ${result.summary.total} engines`);
            await this.refreshView();
        } catch (error) {
            alert(`Error: ${error.message}`);
        }
    }

    /**
     * Refresh discovery
     */
    async refreshDiscovery() {
        try {
            const response = await fetch('/api/engines/discovery/refresh', {
                method: 'POST'
            });
            const result = await response.json();

            alert(`Discovery refreshed: ${result.discovered_count} engines found`);
            await this.refreshView();
        } catch (error) {
            alert(`Error: ${error.message}`);
        }
    }

    /**
     * View engine details
     * @param {string} engineType - Engine type
     */
    async viewDetails(engineType) {
        try {
            const response = await fetch(`/api/engines/${engineType}`);
            const result = await response.json();

            const details = JSON.stringify(result, null, 2);
            alert(`Engine Details:\n\n${details}`);
        } catch (error) {
            alert(`Error: ${error.message}`);
        }
    }

    /**
     * Cleanup engine
     * @param {string} engineType - Engine type
     */
    async cleanupEngine(engineType) {
        if (!confirm(`Cleanup engine ${engineType}?`)) {
            return;
        }

        try {
            const response = await fetch(`/api/engines/${engineType}/cleanup`, {
                method: 'POST'
            });
            const result = await response.json();

            if (result.success) {
                alert(`Engine ${engineType} cleaned up successfully!`);
                await this.refreshView();
            } else {
                alert(`Failed to cleanup engine: ${result.message}`);
            }
        } catch (error) {
            alert(`Error: ${error.message}`);
        }
    }

    /**
     * Export status
     */
    async exportStatus() {
        try {
            const data = await this.fetchEngineData();
            const json = JSON.stringify(data, null, 2);
            const blob = new Blob([json], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `engine-discovery-status-${new Date().toISOString()}.json`;
            a.click();
            URL.revokeObjectURL(url);
        } catch (error) {
            alert(`Error: ${error.message}`);
        }
    }

    /**
     * Refresh view
     */
    async refreshView() {
        const container = document.querySelector('.engine-discovery-view');
        if (container) {
            const newContent = await this.render();
            container.outerHTML = newContent;
        }
    }
}

// Global instance for dashboard integration
const engineDiscoveryView = new EngineDiscoveryView();

// Export for module import
export { engineDiscoveryView };

