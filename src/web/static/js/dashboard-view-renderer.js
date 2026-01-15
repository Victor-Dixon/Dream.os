<!-- SSOT Domain: core -->
/**
 * Dashboard View Renderer - V2 Compliant
 * View rendering methods extracted from dashboard-refactored-main.js
 *
 * @author Agent-3 - Infrastructure & DevOps Specialist
 * @version 1.0.0 - V2 COMPLIANCE EXTRACTION
 * @license MIT
 */

// ====
// DASHBOARD VIEW RENDERER
// ====

/**
 * Dashboard view rendering utilities
 */
export class DashboardViewRenderer {
    constructor() {
        this.logger = console;
    }

    /**
     * Render view content based on view type
     */
    async renderView(view) {
        const contentDiv = document.getElementById('dashboardContent');
        if (!contentDiv) {
            this.logger.error('Dashboard content div not found');
            return;
        }

        let content;
        switch (view) {
            case 'overview':
                content = this.renderOverviewView();
                break;
            case 'agent_performance':
                content = this.renderAgentPerformanceView();
                break;
            case 'contract_status':
                content = this.renderContractStatusView();
                break;
            case 'system_health':
                content = this.renderSystemHealthView();
                break;
            case 'performance_metrics':
                content = this.renderPerformanceMetricsView();
                break;
            case 'workload_distribution':
                content = this.renderWorkloadDistributionView();
                break;
            case 'message_history':
                content = this.renderMessageHistoryView();
                break;
            case 'agent_activity':
                content = this.renderAgentActivityView();
                break;
            case 'queue_status':
                content = this.renderQueueStatusView();
                break;
            case 'engine-discovery':
                content = await this.renderEngineDiscoveryView();
                break;
            case 'repository-merge':
                content = await this.renderRepositoryMergeView();
                // Initialize view after rendering container
                setTimeout(async () => {
                    try {
                        const { RepositoryMergeView } = await import('./dashboard/dashboard-view-repository-merge.js');
                        const view = new RepositoryMergeView();
                        await view.init();
                    } catch (error) {
                        console.error('Error initializing repository merge view:', error);
                    }
                }, 0);
                break;
            default:
                content = this.renderDefaultView(view);
        }

        contentDiv.innerHTML = content;

        // Emit view rendered event
        window.dispatchEvent(new CustomEvent('dashboard:viewRendered', {
            detail: { view: view, timestamp: new Date().toISOString() }
        }));
    }

    /**
     * Render overview view
     */
    renderOverviewView() {
        return `
            <div class="dashboard-view overview-view">
                <h3>System Overview</h3>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-value status-healthy">98%</div>
                        <div class="metric-label">System Health</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value status-healthy">8</div>
                        <div class="metric-label">Active Agents</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value status-healthy">95%</div>
                        <div class="metric-label">Task Completion</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value status-warning">2</div>
                        <div class="metric-label">Active Alerts</div>
                    </div>
                </div>
            </div>
        `;
    }

    /**
     * Render agent performance view
     */
    renderAgentPerformanceView() {
        return `
            <div class="dashboard-view agent-performance-view">
                <h3>Agent Performance</h3>
                <p>Agent performance metrics and analytics...</p>
            </div>
        `;
    }

    /**
     * Render contract status view
     */
    renderContractStatusView() {
        return `
            <div class="dashboard-view contract-status-view">
                <h3>Contract Status</h3>
                <p>Contract status and completion tracking...</p>
            </div>
        `;
    }

    /**
     * Render system health view
     */
    renderSystemHealthView() {
        return `
            <div class="dashboard-view system-health-view">
                <h3>System Health</h3>
                <p>System health monitoring and diagnostics...</p>
            </div>
        `;
    }

    /**
     * Render performance metrics view
     */
    renderPerformanceMetricsView() {
        return `
            <div class="dashboard-view performance-metrics-view">
                <h3>Performance Metrics</h3>
                <p>Performance metrics and benchmarking...</p>
            </div>
        `;
    }

    /**
     * Render workload distribution view
     */
    renderWorkloadDistributionView() {
        return `
            <div class="dashboard-view workload-distribution-view">
                <h3>Workload Distribution</h3>
                <p>Task distribution and workload analysis...</p>
            </div>
        `;
    }

    /**
     * Render message history view
     */
    renderMessageHistoryView() {
        // Use the message history view component if available
        if (typeof renderMessageHistoryView === 'function') {
            const data = this.getDashboardData();
            return renderMessageHistoryView(data);
        }
        return `
            <div class="dashboard-view message-history-view">
                <h3>Message History</h3>
                <p>Loading message history...</p>
                <script>
                    // Load message history data and render
                    fetch('/api/messages/history')
                        .then(res => res.json())
                        .then(data => {
                            if (typeof renderMessageHistoryView === 'function') {
                                document.getElementById('dashboardContent').innerHTML = 
                                    renderMessageHistoryView({ message_history: data });
                            }
                        });
                </script>
            </div>
        `;
    }

    /**
     * Render agent activity view
     */
    renderAgentActivityView() {
        // Use the agent activity view component if available
        if (typeof renderAgentActivityView === 'function') {
            const data = this.getDashboardData();
            return renderAgentActivityView(data);
        }
        return `
            <div class="dashboard-view agent-activity-view">
                <h3>Agent Activity</h3>
                <p>Loading agent activity...</p>
                <script>
                    // Load agent activity data and render
                    fetch('/api/messages/activity')
                        .then(res => res.json())
                        .then(data => {
                            if (typeof renderAgentActivityView === 'function') {
                                document.getElementById('dashboardContent').innerHTML = 
                                    renderAgentActivityView({ agent_activity: data.activity || [] });
                            }
                        });
                </script>
            </div>
        `;
    }

    /**
     * Render queue status view
     */
    renderQueueStatusView() {
        // Use the queue status view component if available
        if (typeof renderQueueStatusView === 'function') {
            const data = this.getDashboardData();
            return renderQueueStatusView(data);
        }
        return `
            <div class="dashboard-view queue-status-view">
                <h3>Queue Status</h3>
                <p>Loading queue status...</p>
                <script>
                    // Load queue status data and render
                    fetch('/api/messages/queue')
                        .then(res => res.json())
                        .then(data => {
                            if (typeof renderQueueStatusView === 'function') {
                                document.getElementById('dashboardContent').innerHTML = 
                                    renderQueueStatusView({ queue_status: data.queue || {} });
                            }
                        });
                </script>
            </div>
        `;
    }

    /**
     * Get dashboard data (placeholder - should be injected)
     */
    getDashboardData() {
        return window.dashboardData || {};
    }

    /**
     * Render engine discovery view
     */
    async renderEngineDiscoveryView() {
        try {
            // Import and use the engine discovery view
            const module = await import('./dashboard-view-engine-discovery.js');
            return await module.engineDiscoveryView.render();
        } catch (error) {
            this.logger.error('Error loading engine discovery view:', error);
            return `
                <div class="dashboard-view engine-discovery-view">
                    <div class="alert alert-danger">
                        <strong>Error loading engine discovery view:</strong> ${error.message}
                    </div>
                </div>
            `;
        }
    }

    /**
     * Render repository merge view
     */
    async renderRepositoryMergeView() {
        try {
            // Import and use the repository merge view
            const { RepositoryMergeView } = await import('./dashboard/dashboard-view-repository-merge.js');
            const view = new RepositoryMergeView();
            // Return container - view will render into it
            return `
                <div class="dashboard-view repository-merge-view" id="repository-merge-view">
                    <!-- Content will be rendered by RepositoryMergeView.init() -->
                </div>
            `;
        } catch (error) {
            this.logger.error('Error loading repository merge view:', error);
            return `
                <div class="dashboard-view repository-merge-view">
                    <div class="alert alert-danger">
                        <strong>Error loading repository merge view:</strong> ${error.message}
                    </div>
                </div>
            `;
        }
    }

    /**
     * Render default view
     */
    renderDefaultView(view) {
        return `
            <div class="dashboard-view default-view">
                <h3>${view || 'Unknown View'}</h3>
                <p>Dashboard view content...</p>
            </div>
        `;
    }
}

// ====
// FACTORY FUNCTIONS
// ====

/**
 * Create dashboard view renderer instance
 */
export function createDashboardViewRenderer() {
    return new DashboardViewRenderer();
}

// ====
// EXPORTS
// ====

export default DashboardViewRenderer;
