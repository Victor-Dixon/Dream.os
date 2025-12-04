/**
 * Dashboard Engine Discovery View - V2 Compliant
 * 
 * Displays discovered engines from Plugin Discovery Pattern
 * 
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0
 * @license MIT
 */

export class EngineDiscoveryView {
    constructor() {
        this.engines = [];
        this.summary = {
            total: 0,
            active: 0,
            failed: 0,
            pending: 0
        };
        this.discoveryLog = [];
        this.isLoading = false;
    }

    /**
     * Render engine discovery view
     */
    async render() {
        this.isLoading = true;
        try {
            const data = await this.fetchEngineData();
            this.updateSummary(data);
            this.engines = data.engines || [];
            this.discoveryLog = data.discovery_log || [];
            this.isLoading = false;
            return this.renderView();
        } catch (error) {
            this.isLoading = false;
            console.error('Failed to load engine discovery data:', error);
            return this.renderError(error);
        }
    }

    /**
     * Fetch engine discovery data from API
     */
    async fetchEngineData() {
        const response = await fetch('/api/engines/discovery');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    }

    /**
     * Update summary statistics
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
     */
    renderView() {
        return `
            <div class="dashboard-view engine-discovery-view">
                <div class="view-header">
                    <h3>🔌 Engine Discovery Dashboard</h3>
                    <button class="btn btn-sm btn-primary" onclick="window.engineDiscoveryView?.refreshDiscovery()">
                        🔄 Refresh Discovery
                    </button>
                </div>
                
                ${this.renderSummaryCards()}
                ${this.renderEngineList()}
                ${this.renderDiscoveryLog()}
                ${this.renderBulkActions()}
            </div>
        `;
    }

    /**
     * Render summary cards
     */
    renderSummaryCards() {
        return `
            <div class="summary-cards">
                <div class="summary-card">
                    <div class="card-value">${this.summary.total}</div>
                    <div class="card-label">Total Engines</div>
                </div>
                <div class="summary-card active">
                    <div class="card-value">${this.summary.active}</div>
                    <div class="card-label">Active Engines</div>
                </div>
                <div class="summary-card failed">
                    <div class="card-value">${this.summary.failed}</div>
                    <div class="card-label">Failed Engines</div>
                </div>
                <div class="summary-card pending">
                    <div class="card-value">${this.summary.pending}</div>
                    <div class="card-label">Pending Init</div>
                </div>
            </div>
        `;
    }

    /**
     * Render engine list
     */
    renderEngineList() {
        if (this.engines.length === 0) {
            return '<div class="no-engines">No engines discovered yet.</div>';
        }

        const engineRows = this.engines.map(engine => {
            const statusIcon = this.getStatusIcon(engine.status);
            const statusClass = this.getStatusClass(engine.status);
            
            return `
                <tr class="engine-row ${statusClass}">
                    <td>${engine.engine_type}</td>
                    <td>${engine.engine_class}</td>
                    <td>
                        <span class="status-badge ${statusClass}">
                            ${statusIcon} ${engine.status}
                        </span>
                    </td>
                    <td>
                        ${this.renderEngineActions(engine)}
                    </td>
                    <td>
                        <button class="btn btn-sm btn-link" onclick="window.engineDiscoveryView?.showEngineDetails('${engine.engine_type}')">
                            View Details
                        </button>
                    </td>
                </tr>
            `;
        }).join('');

        return `
            <div class="engine-list-section">
                <h4>Discovered Engines</h4>
                <table class="engine-table">
                    <thead>
                        <tr>
                            <th>Engine Type</th>
                            <th>Engine Class</th>
                            <th>Status</th>
                            <th>Actions</th>
                            <th>Details</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${engineRows}
                    </tbody>
                </table>
            </div>
        `;
    }

    /**
     * Render engine actions
     */
    renderEngineActions(engine) {
        const actions = [];
        
        if (engine.status === 'discovered') {
            actions.push(`
                <button class="btn btn-sm btn-success" 
                        onclick="window.engineDiscoveryView?.initializeEngine('${engine.engine_type}')">
                    Initialize
                </button>
            `);
        }
        
        if (engine.status === 'initialized') {
            actions.push(`
                <button class="btn btn-sm btn-warning" 
                        onclick="window.engineDiscoveryView?.cleanupEngine('${engine.engine_type}')">
                    Cleanup
                </button>
            `);
        }
        
        return actions.join(' ');
    }

    /**
     * Render discovery log
     */
    renderDiscoveryLog() {
        if (this.discoveryLog.length === 0) {
            return '';
        }

        const logEntries = this.discoveryLog.map(log => {
            const levelClass = log.level || 'info';
            return `
                <div class="log-entry ${levelClass}">
                    <span class="log-timestamp">[${log.timestamp || 'N/A'}]</span>
                    <span class="log-message">${log.message}</span>
                </div>
            `;
        }).join('');

        return `
            <div class="discovery-log-section">
                <h4>Discovery Log</h4>
                <div class="discovery-log">
                    ${logEntries}
                </div>
            </div>
        `;
    }

    /**
     * Render bulk actions panel
     */
    renderBulkActions() {
        return `
            <div class="bulk-actions-panel">
                <h4>Bulk Actions</h4>
                <div class="bulk-actions-buttons">
                    <button class="btn btn-primary" 
                            onclick="window.engineDiscoveryView?.initializeAllEngines()">
                        Initialize All Engines
                    </button>
                    <button class="btn btn-warning" 
                            onclick="window.engineDiscoveryView?.cleanupAllEngines()">
                        Cleanup All Engines
                    </button>
                </div>
            </div>
        `;
    }

    /**
     * Render error state
     */
    renderError(error) {
        return `
            <div class="dashboard-view engine-discovery-view">
                <div class="error-state">
                    <h3>❌ Error Loading Engine Discovery</h3>
                    <p>${error.message}</p>
                    <button class="btn btn-primary" onclick="window.engineDiscoveryView?.render()">
                        Retry
                    </button>
                </div>
            </div>
        `;
    }

    /**
     * Get status icon
     */
    getStatusIcon(status) {
        const icons = {
            'initialized': '✅',
            'discovered': '⏳',
            'error': '❌'
        };
        return icons[status] || '❓';
    }

    /**
     * Get status class
     */
    getStatusClass(status) {
        const classes = {
            'initialized': 'status-active',
            'discovered': 'status-pending',
            'error': 'status-error'
        };
        return classes[status] || 'status-unknown';
    }

    /**
     * Refresh discovery
     */
    async refreshDiscovery() {
        try {
            const response = await fetch('/api/engines/discovery/refresh', {
                method: 'POST'
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const result = await response.json();
            alert(`Discovery refreshed: ${result.discovered_count} engines found`);
            await this.render();
        } catch (error) {
            console.error('Failed to refresh discovery:', error);
            alert(`Failed to refresh discovery: ${error.message}`);
        }
    }

    /**
     * Initialize engine
     */
    async initializeEngine(engineType) {
        try {
            const response = await fetch(`/api/engines/${engineType}/initialize`, {
                method: 'POST'
            });
            const result = await response.json();
            if (result.success) {
                alert(`Engine ${engineType} initialized successfully`);
                await this.render();
            } else {
                alert(`Failed to initialize engine: ${result.message}`);
            }
        } catch (error) {
            console.error('Failed to initialize engine:', error);
            alert(`Failed to initialize engine: ${error.message}`);
        }
    }

    /**
     * Cleanup engine
     */
    async cleanupEngine(engineType) {
        try {
            const response = await fetch(`/api/engines/${engineType}/cleanup`, {
                method: 'POST'
            });
            const result = await response.json();
            if (result.success) {
                alert(`Engine ${engineType} cleaned up successfully`);
                await this.render();
            } else {
                alert(`Failed to cleanup engine: ${result.message}`);
            }
        } catch (error) {
            console.error('Failed to cleanup engine:', error);
            alert(`Failed to cleanup engine: ${error.message}`);
        }
    }

    /**
     * Initialize all engines
     */
    async initializeAllEngines() {
        if (!confirm('Initialize all engines?')) {
            return;
        }
        
        try {
            const response = await fetch('/api/engines/initialize-all', {
                method: 'POST'
            });
            const result = await response.json();
            const successful = result.summary?.successful || 0;
            const failed = result.summary?.failed || 0;
            alert(`Initialized ${successful} engines, ${failed} failed`);
            await this.render();
        } catch (error) {
            console.error('Failed to initialize all engines:', error);
            alert(`Failed to initialize all engines: ${error.message}`);
        }
    }

    /**
     * Cleanup all engines
     */
    async cleanupAllEngines() {
        if (!confirm('Cleanup all engines? This will remove all engine instances.')) {
            return;
        }
        
        // Note: Cleanup all endpoint not implemented in API yet
        // This would need to be added to engines_routes.py
        alert('Cleanup all functionality not yet implemented');
    }

    /**
     * Show engine details
     */
    async showEngineDetails(engineType) {
        try {
            const response = await fetch(`/api/engines/${engineType}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const engine = await response.json();
            
            const details = `
                <h4>${engine.engine_type} Engine Details</h4>
                <p><strong>Class:</strong> ${engine.engine_class}</p>
                <p><strong>Status:</strong> ${engine.status}</p>
                <p><strong>Module:</strong> ${engine.metadata.module_name}</p>
                <p><strong>Protocol Compliant:</strong> ${engine.metadata.protocol_compliant ? 'Yes' : 'No'}</p>
                <pre>${JSON.stringify(engine.status_info, null, 2)}</pre>
            `;
            
            // Simple alert for now - could be enhanced with modal
            alert(details);
        } catch (error) {
            console.error('Failed to get engine details:', error);
            alert(`Failed to get engine details: ${error.message}`);
        }
    }
}

// Make view accessible globally for onclick handlers
if (typeof window !== 'undefined') {
    window.engineDiscoveryView = new EngineDiscoveryView();
}
