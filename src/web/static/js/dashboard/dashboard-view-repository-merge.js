/**
 * Repository Merge Status Dashboard View
 * ======================================
 * 
 * Dashboard view component for repository merge status tracking.
 * Displays merge improvements data: status tracking, error classification,
 * duplicate prevention, and name resolution.
 * 
 * <!-- SSOT Domain: web -->
 * 
 * Author: Agent-7 (Web Development Specialist)
 * Date: 2025-12-04
 */

class RepositoryMergeView {
    constructor() {
        this.apiBase = '/api/repository-merge';
        this.data = null;
        this.refreshInterval = null;
    }

    /**
     * Initialize the repository merge view.
     */
    async init() {
        await this.loadData();
        this.render();
        this.setupEventListeners();
        this.startAutoRefresh();
    }

    /**
     * Load merge status data from API.
     */
    async loadData() {
        try {
            const response = await fetch(`${this.apiBase}/status`);
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            this.data = await response.json();
        } catch (error) {
            console.error('Error loading merge status:', error);
            this.data = {
                summary: {
                    total_repositories: 0,
                    status_breakdown: {},
                    total_merge_attempts: 0,
                    successful_attempts: 0,
                    failed_attempts: 0,
                    permanent_errors: 0,
                    transient_errors: 0
                },
                repository_statuses: {},
                merge_attempts: {}
            };
        }
    }

    /**
     * Render the repository merge dashboard view.
     */
    render() {
        const container = document.getElementById('repository-merge-view');
        if (!container) {
            console.warn('Repository merge view container not found');
            return;
        }

        container.innerHTML = `
            <div class="repository-merge-dashboard">
                <h2>🔗 Repository Merge Status</h2>
                
                <!-- Summary Cards -->
                <div class="merge-summary-cards">
                    ${this.renderSummaryCards()}
                </div>
                
                <!-- Status Breakdown -->
                <div class="merge-status-section">
                    <h3>📊 Repository Status Breakdown</h3>
                    ${this.renderStatusBreakdown()}
                </div>
                
                <!-- Error Classification -->
                <div class="merge-error-section">
                    <h3>⚠️ Error Classification</h3>
                    ${this.renderErrorClassification()}
                </div>
                
                <!-- Recent Attempts -->
                <div class="merge-attempts-section">
                    <h3>📋 Recent Merge Attempts</h3>
                    ${this.renderRecentAttempts()}
                </div>
                
                <!-- Name Resolution Tool -->
                <div class="merge-tools-section">
                    <h3>🔧 Merge Tools</h3>
                    ${this.renderTools()}
                </div>
            </div>
        `;

        // Setup tool event listeners
        this.setupToolListeners();
    }

    /**
     * Render summary cards.
     */
    renderSummaryCards() {
        const summary = this.data.summary;
        
        return `
            <div class="summary-card">
                <div class="card-icon">📦</div>
                <div class="card-content">
                    <div class="card-value">${summary.total_repositories}</div>
                    <div class="card-label">Total Repositories</div>
                </div>
            </div>
            <div class="summary-card">
                <div class="card-icon">✅</div>
                <div class="card-content">
                    <div class="card-value">${summary.successful_attempts}</div>
                    <div class="card-label">Successful Merges</div>
                </div>
            </div>
            <div class="summary-card">
                <div class="card-icon">❌</div>
                <div class="card-content">
                    <div class="card-value">${summary.failed_attempts}</div>
                    <div class="card-label">Failed Attempts</div>
                </div>
            </div>
            <div class="summary-card">
                <div class="card-icon">🚫</div>
                <div class="card-content">
                    <div class="card-value">${summary.permanent_errors}</div>
                    <div class="card-label">Permanent Errors</div>
                </div>
            </div>
        `;
    }

    /**
     * Render status breakdown.
     */
    renderStatusBreakdown() {
        const breakdown = this.data.summary.status_breakdown;
        const statusColors = {
            'exists': '#4CAF50',
            'merged': '#2196F3',
            'deleted': '#F44336',
            'unknown': '#FF9800',
            'not_accessible': '#9E9E9E'
        };
        
        const statusLabels = {
            'exists': 'Exists',
            'merged': 'Merged',
            'deleted': 'Deleted',
            'unknown': 'Unknown',
            'not_accessible': 'Not Accessible'
        };
        
        const items = Object.entries(breakdown).map(([status, count]) => `
            <div class="status-item">
                <div class="status-indicator" style="background-color: ${statusColors[status] || '#9E9E9E'}"></div>
                <div class="status-label">${statusLabels[status] || status}</div>
                <div class="status-count">${count}</div>
            </div>
        `).join('');
        
        return `<div class="status-breakdown">${items}</div>`;
    }

    /**
     * Render error classification section.
     */
    renderErrorClassification() {
        const summary = this.data.summary;
        
        return `
            <div class="error-classification">
                <div class="error-type permanent">
                    <div class="error-icon">🚫</div>
                    <div class="error-info">
                        <div class="error-label">Permanent Errors</div>
                        <div class="error-count">${summary.permanent_errors}</div>
                        <div class="error-description">Don't retry - repo not available, deleted, or access denied</div>
                    </div>
                </div>
                <div class="error-type transient">
                    <div class="error-icon">🔄</div>
                    <div class="error-info">
                        <div class="error-label">Transient Errors</div>
                        <div class="error-count">${summary.transient_errors}</div>
                        <div class="error-description">Retry with backoff - network issues, rate limits</div>
                    </div>
                </div>
            </div>
        `;
    }

    /**
     * Render recent merge attempts.
     */
    renderRecentAttempts() {
        const attempts = Object.values(this.data.merge_attempts)
            .sort((a, b) => new Date(b.last_attempt) - new Date(a.last_attempt))
            .slice(0, 10);
        
        if (attempts.length === 0) {
            return '<div class="no-data">No merge attempts recorded</div>';
        }
        
        const items = attempts.map(attempt => {
            const statusClass = attempt.success ? 'success' : 'failed';
            const statusIcon = attempt.success ? '✅' : '❌';
            const errorTypeBadge = attempt.error_type ? 
                `<span class="error-type-badge ${attempt.error_type}">${attempt.error_type}</span>` : '';
            
            return `
                <div class="attempt-item ${statusClass}">
                    <div class="attempt-status">${statusIcon}</div>
                    <div class="attempt-details">
                        <div class="attempt-pair">
                            <strong>${attempt.source_repo}</strong> → <strong>${attempt.target_repo}</strong>
                        </div>
                        <div class="attempt-meta">
                            <span>Attempts: ${attempt.attempt_count}</span>
                            <span>Last: ${new Date(attempt.last_attempt).toLocaleString()}</span>
                            ${errorTypeBadge}
                        </div>
                        ${attempt.last_error ? `<div class="attempt-error">${attempt.last_error}</div>` : ''}
                    </div>
                </div>
            `;
        }).join('');
        
        return `<div class="attempts-list">${items}</div>`;
    }

    /**
     * Render merge tools section.
     */
    renderTools() {
        return `
            <div class="merge-tools">
                <div class="tool-section">
                    <h4>🔍 Validate Merge</h4>
                    <div class="tool-form">
                        <input type="text" id="validate-source" placeholder="Source repository" />
                        <input type="text" id="validate-target" placeholder="Target repository" />
                        <button id="validate-btn">Validate</button>
                    </div>
                    <div id="validate-result"></div>
                </div>
                
                <div class="tool-section">
                    <h4>📝 Normalize Repository Name</h4>
                    <div class="tool-form">
                        <input type="text" id="normalize-input" placeholder="Repository name" />
                        <button id="normalize-btn">Normalize</button>
                    </div>
                    <div id="normalize-result"></div>
                </div>
                
                <div class="tool-section">
                    <h4>⚠️ Classify Error</h4>
                    <div class="tool-form">
                        <textarea id="classify-input" placeholder="Error message"></textarea>
                        <button id="classify-btn">Classify</button>
                    </div>
                    <div id="classify-result"></div>
                </div>
            </div>
        `;
    }

    /**
     * Setup event listeners for tools.
     */
    setupToolListeners() {
        // Validate merge
        const validateBtn = document.getElementById('validate-btn');
        if (validateBtn) {
            validateBtn.addEventListener('click', () => this.validateMerge());
        }
        
        // Normalize name
        const normalizeBtn = document.getElementById('normalize-btn');
        if (normalizeBtn) {
            normalizeBtn.addEventListener('click', () => this.normalizeName());
        }
        
        // Classify error
        const classifyBtn = document.getElementById('classify-btn');
        if (classifyBtn) {
            classifyBtn.addEventListener('click', () => this.classifyError());
        }
    }

    /**
     * Validate a merge.
     */
    async validateMerge() {
        const source = document.getElementById('validate-source')?.value;
        const target = document.getElementById('validate-target')?.value;
        const resultDiv = document.getElementById('validate-result');
        
        if (!source || !target) {
            resultDiv.innerHTML = '<div class="error">Please enter both source and target repositories</div>';
            return;
        }
        
        try {
            const response = await fetch(`${this.apiBase}/validate`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ source_repo: source, target_repo: target })
            });
            
            const data = await response.json();
            
            if (data.should_proceed) {
                resultDiv.innerHTML = `
                    <div class="success">
                        ✅ Validation passed! Merge can proceed.
                        <pre>${JSON.stringify(data.validation_details, null, 2)}</pre>
                    </div>
                `;
            } else {
                resultDiv.innerHTML = `
                    <div class="error">
                        ❌ Validation failed: ${data.error}
                        <pre>${JSON.stringify(data.validation_details, null, 2)}</pre>
                    </div>
                `;
            }
        } catch (error) {
            resultDiv.innerHTML = `<div class="error">Error: ${error.message}</div>`;
        }
    }

    /**
     * Normalize a repository name.
     */
    async normalizeName() {
        const input = document.getElementById('normalize-input')?.value;
        const resultDiv = document.getElementById('normalize-result');
        
        if (!input) {
            resultDiv.innerHTML = '<div class="error">Please enter a repository name</div>';
            return;
        }
        
        try {
            const response = await fetch(`${this.apiBase}/normalize-name`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ repo_name: input })
            });
            
            const data = await response.json();
            
            resultDiv.innerHTML = `
                <div class="result">
                    <div><strong>Original:</strong> ${data.original}</div>
                    <div><strong>Normalized:</strong> ${data.normalized}</div>
                    ${data.changed ? '<div class="info">Name was normalized</div>' : '<div class="info">Name unchanged</div>'}
                </div>
            `;
        } catch (error) {
            resultDiv.innerHTML = `<div class="error">Error: ${error.message}</div>`;
        }
    }

    /**
     * Classify an error message.
     */
    async classifyError() {
        const input = document.getElementById('classify-input')?.value;
        const resultDiv = document.getElementById('classify-result');
        
        if (!input) {
            resultDiv.innerHTML = '<div class="error">Please enter an error message</div>';
            return;
        }
        
        try {
            const response = await fetch(`${this.apiBase}/classify-error`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ error_message: input })
            });
            
            const data = await response.json();
            
            const typeClass = data.is_permanent ? 'permanent' : data.should_retry ? 'transient' : 'unknown';
            
            resultDiv.innerHTML = `
                <div class="result ${typeClass}">
                    <div><strong>Error Type:</strong> <span class="error-type-badge ${data.error_type}">${data.error_type}</span></div>
                    <div><strong>Should Retry:</strong> ${data.should_retry ? 'Yes (with backoff)' : 'No'}</div>
                    <div><strong>Description:</strong> ${data.description}</div>
                </div>
            `;
        } catch (error) {
            resultDiv.innerHTML = `<div class="error">Error: ${error.message}</div>`;
        }
    }

    /**
     * Setup event listeners.
     */
    setupEventListeners() {
        // Auto-refresh button
        const refreshBtn = document.getElementById('refresh-merge-status');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => this.refresh());
        }
    }

    /**
     * Refresh data and re-render.
     */
    async refresh() {
        await this.loadData();
        this.render();
    }

    /**
     * Start auto-refresh.
     */
    startAutoRefresh() {
        // Refresh every 30 seconds
        this.refreshInterval = setInterval(() => {
            this.loadData().then(() => this.render());
        }, 30000);
    }

    /**
     * Stop auto-refresh.
     */
    stopAutoRefresh() {
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
            this.refreshInterval = null;
        }
    }
}

// Export for use in dashboard
if (typeof module !== 'undefined' && module.exports) {
    module.exports = RepositoryMergeView;
}

