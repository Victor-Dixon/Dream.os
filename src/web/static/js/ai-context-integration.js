/**
 * AI Context Integration - Phase 5 Real-time Intelligence
 * =====================================================
 *
 * JavaScript client for AI-powered context processing and real-time suggestions.
 *
 * <!-- SSOT Domain: ai_context -->
 *
 * Navigation References:
 * ├── WebSocket Server → src/services/ai_context_websocket.py::AIContextWebSocketServer
 * ├── Context Engine → src/services/ai_context_engine.py::AIContextEngine
 * ├── FastAPI Endpoints → src/web/fastapi_app.py (/api/context/*)
 * ├── Risk Integration → src/web/static/js/trading-robot/risk-dashboard-integration.js
 * ├── Dashboard UI → src/web/static/js/dashboard.js
 * └── Performance Monitoring → docs/analytics/TRADINGROBOTPLUG_ANALYTICS_ARCHITECTURE.md
 *
 * Features:
 * - Real-time context processing and suggestions
 * - Intelligent UX personalization
 * - Collaborative context sharing
 * - Performance monitoring and optimization
 *
 * @author Agent-5 (Business Intelligence Specialist)
 * @version 1.0.0 - Phase 5 AI Context Integration
 * @license MIT
 */

class AIContextIntegration {
    /**
     * AI-powered context processing integration for real-time collaboration.
     */
    constructor() {
        this.websocket = null;
        this.restApiUrl = '/api';
        this.websocketUrl = `ws://${window.location.host}/ws/ai`;

        // Session management
        this.currentSession = null;
        this.contextData = {};
        this.suggestions = [];
        this.isConnected = false;

        // Performance tracking
        this.performanceMetrics = {
            suggestionsApplied: 0,
            contextUpdates: 0,
            responseTime: 0,
            errorCount: 0
        };

        // V2 Compliance: Structured logging
        this.logger = {
            log: (message) => {
                const timestamp = new Date().toISOString();
                const logEntry = `[${timestamp}] AI-CONTEXT: ${message}`;
                console.log(logEntry);
            },
            error: (message, error) => {
                const timestamp = new Date().toISOString();
                const errorEntry = `[${timestamp}] AI-CONTEXT ERROR: ${message}`;
                console.error(errorEntry, error);
                this.performanceMetrics.errorCount++;
            }
        };

        // Auto-reconnection
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 3000;
    }

    /**
     * Initialize AI Context Integration
     */
    async initialize(userId = 'anonymous', contextType = 'general') {
        this.logger.log('🚀 Initializing AI Context Integration...');

        try {
            // Create context session
            await this.createSession(userId, contextType);

            // Connect to WebSocket
            await this.connectWebSocket();

            // Initialize with current page context
            await this.updateContext({
                page_url: window.location.href,
                user_agent: navigator.userAgent,
                viewport_size: {
                    width: window.innerWidth,
                    height: window.innerHeight
                },
                timestamp: Date.now()
            });

            this.logger.log('✅ AI Context Integration initialized successfully');
            return true;

        } catch (error) {
            this.logger.error('❌ AI Context Integration initialization failed:', error);
            throw error;
        }
    }

    /**
     * Create a new context processing session
     */
    async createSession(userId, contextType) {
        try {
            this.logger.log(`📝 Creating context session for user ${userId} (${contextType})`);

            const response = await fetch(`${this.restApiUrl}/context/session`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    user_id: userId,
                    context_type: contextType,
                    initial_context: {
                        user_id: userId,
                        context_type: contextType,
                        session_start: Date.now(),
                        browser_info: {
                            language: navigator.language,
                            platform: navigator.platform,
                            cookie_enabled: navigator.cookieEnabled
                        }
                    }
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const result = await response.json();
            this.currentSession = result.session_id;

            this.logger.log(`✅ Created session: ${this.currentSession}`);
            return this.currentSession;

        } catch (error) {
            this.logger.error('Failed to create context session:', error);
            throw error;
        }
    }

    /**
     * Connect to AI Context WebSocket server
     */
    async connectWebSocket() {
        try {
            this.logger.log(`🔌 Connecting to AI Context WebSocket: ${this.websocketUrl}/context`);

            this.websocket = new WebSocket(`${this.websocketUrl}/context`);

            return new Promise((resolve, reject) => {
                this.websocket.onopen = () => {
                    this.isConnected = true;
                    this.reconnectAttempts = 0;
                    this.logger.log('🟢 Connected to AI Context WebSocket');
                    resolve();
                };

                this.websocket.onmessage = (event) => {
                    this.handleWebSocketMessage(event.data);
                };

                this.websocket.onclose = () => {
                    this.isConnected = false;
                    this.logger.log('🔴 Disconnected from AI Context WebSocket');
                    this.handleReconnect();
                };

                this.websocket.onerror = (error) => {
                    this.logger.error('WebSocket connection error:', error);
                    reject(error);
                };

                // Connection timeout
                setTimeout(() => {
                    if (!this.isConnected) {
                        reject(new Error('WebSocket connection timeout'));
                    }
                }, 10000);
            });

        } catch (error) {
            this.logger.error('Failed to connect to WebSocket:', error);
            throw error;
        }
    }

    /**
     * Handle WebSocket reconnection
     */
    async handleReconnect() {
        if (this.reconnectAttempts >= this.maxReconnectAttempts) {
            this.logger.error('Max reconnection attempts reached');
            return;
        }

        this.reconnectAttempts++;
        this.logger.log(`🔄 Attempting reconnection ${this.reconnectAttempts}/${this.maxReconnectAttempts} in ${this.reconnectDelay}ms`);

        setTimeout(async () => {
            try {
                await this.connectWebSocket();
            } catch (error) {
                this.logger.error('Reconnection failed:', error);
            }
        }, this.reconnectDelay);
    }

    /**
     * Handle incoming WebSocket messages
     */
    handleWebSocketMessage(data) {
        try {
            const message = JSON.parse(data);

            switch (message.type) {
                case 'context_updated':
                    this.handleContextUpdate(message);
                    break;
                case 'suggestion_applied_broadcast':
                    this.handleSuggestionApplied(message);
                    break;
                case 'heartbeat':
                    // Server is alive, no action needed
                    break;
                default:
                    this.logger.log(`Unknown message type: ${message.type}`);
            }
        } catch (error) {
            this.logger.error('Failed to parse WebSocket message:', error);
        }
    }

    /**
     * Handle context update messages
     */
    handleContextUpdate(message) {
        const result = message.result;
        this.performanceMetrics.contextUpdates++;

        // Update local context data
        this.contextData = result.updated_context;

        // Process new suggestions
        if (result.new_suggestions && result.new_suggestions.length > 0) {
            result.new_suggestions.forEach(suggestion => {
                this.suggestions.push(suggestion);
                this.displaySuggestion(suggestion);
            });
        }

        // Update performance metrics
        if (result.processing_time) {
            this.performanceMetrics.responseTime = result.processing_time;
        }

        this.logger.log(`📊 Context updated with ${result.new_suggestions?.length || 0} new suggestions`);
    }

    /**
     * Handle suggestion applied broadcasts
     */
    handleSuggestionApplied(message) {
        const suggestionId = message.suggestion_id;

        // Update local suggestion status
        const suggestion = this.suggestions.find(s => s.suggestion_id === suggestionId);
        if (suggestion) {
            suggestion.applied = true;
            this.updateSuggestionDisplay(suggestion);
        }

        this.logger.log(`✅ Suggestion ${suggestionId} applied`);
    }

    /**
     * Update context data and trigger processing
     */
    async updateContext(contextUpdates) {
        if (!this.currentSession) {
            throw new Error('No active session');
        }

        try {
            const startTime = Date.now();

            const response = await fetch(`${this.restApiUrl}/context/${this.currentSession}/update`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    context_updates: contextUpdates
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const result = await response.json();
            const responseTime = Date.now() - startTime;

            this.logger.log(`📝 Context updated in ${responseTime}ms`);
            return result;

        } catch (error) {
            this.logger.error('Failed to update context:', error);
            throw error;
        }
    }

    /**
     * Apply a suggestion
     */
    async applySuggestion(suggestionId) {
        if (!this.currentSession) {
            throw new Error('No active session');
        }

        try {
            const response = await fetch(`${this.restApiUrl}/context/${this.currentSession}/suggestion/${suggestionId}/apply`, {
                method: 'POST'
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const result = await response.json();
            this.performanceMetrics.suggestionsApplied++;

            // Update local suggestion status
            const suggestion = this.suggestions.find(s => s.suggestion_id === suggestionId);
            if (suggestion) {
                suggestion.applied = true;
            }

            this.logger.log(`✅ Applied suggestion: ${suggestionId}`);
            return result;

        } catch (error) {
            this.logger.error('Failed to apply suggestion:', error);
            throw error;
        }
    }

    /**
     * Get current context
     */
    async getCurrentContext() {
        if (!this.currentSession) {
            throw new Error('No active session');
        }

        try {
            const response = await fetch(`${this.restApiUrl}/context/${this.currentSession}`);

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const context = await response.json();
            this.contextData = context.context_data || {};
            this.suggestions = context.ai_suggestions || [];

            return context;

        } catch (error) {
            this.logger.error('Failed to get context:', error);
            throw error;
        }
    }

    /**
     * End the current session
     */
    async endSession() {
        if (!this.currentSession) {
            return;
        }

        try {
            const response = await fetch(`${this.restApiUrl}/context/${this.currentSession}`, {
                method: 'DELETE'
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const result = await response.json();
            this.logger.log(`🏁 Session ended: ${this.currentSession}`);
            this.currentSession = null;
            this.contextData = {};
            this.suggestions = [];

            return result;

        } catch (error) {
            this.logger.error('Failed to end session:', error);
            throw error;
        }
    }

    /**
     * Display a suggestion to the user
     */
    displaySuggestion(suggestion) {
        // Create suggestion notification
        const suggestionElement = document.createElement('div');
        suggestionElement.className = `ai-suggestion ai-suggestion-${suggestion.suggestion_type}`;
        suggestionElement.setAttribute('data-suggestion-id', suggestion.suggestion_id);

        suggestionElement.innerHTML = `
            <div class="suggestion-header">
                <span class="suggestion-type">${this.formatSuggestionType(suggestion.suggestion_type)}</span>
                <span class="confidence-score">${(suggestion.confidence_score * 100).toFixed(0)}% confidence</span>
            </div>
            <div class="suggestion-content">${suggestion.content.message || suggestion.reasoning}</div>
            <div class="suggestion-actions">
                <button class="apply-btn" onclick="aiContextIntegration.applySuggestion('${suggestion.suggestion_id}')">
                    Apply
                </button>
                <button class="dismiss-btn" onclick="this.parentElement.parentElement.remove()">
                    Dismiss
                </button>
            </div>
        `;

        // Add to suggestions container
        let container = document.getElementById('ai-suggestions-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'ai-suggestions-container';
            container.className = 'ai-suggestions-container';
            document.body.appendChild(container);
        }

        container.appendChild(suggestionElement);

        // Auto-hide after 30 seconds
        setTimeout(() => {
            if (suggestionElement.parentElement) {
                suggestionElement.remove();
            }
        }, 30000);
    }

    /**
     * Update suggestion display when applied
     */
    updateSuggestionDisplay(suggestion) {
        const element = document.querySelector(`[data-suggestion-id="${suggestion.suggestion_id}"]`);
        if (element) {
            element.classList.add('applied');
            const applyBtn = element.querySelector('.apply-btn');
            if (applyBtn) {
                applyBtn.textContent = 'Applied';
                applyBtn.disabled = true;
            }
        }
    }

    /**
     * Format suggestion type for display
     */
    formatSuggestionType(type) {
        const typeMap = {
            'risk_alert': '⚠️ Risk Alert',
            'optimization': '🚀 Optimization',
            'insight': '💡 Insight',
            'action': '🎯 Action',
            'collaboration': '🤝 Collaboration'
        };
        return typeMap[type] || type;
    }

    /**
     * Get performance statistics
     */
    getPerformanceStats() {
        return {
            ...this.performanceMetrics,
            sessionId: this.currentSession,
            isConnected: this.isConnected,
            suggestionsCount: this.suggestions.length,
            contextKeys: Object.keys(this.contextData).length
        };
    }

    /**
     * Track user interactions for context
     */
    trackInteraction(interactionType, details = {}) {
        const interaction = {
            type: interactionType,
            details: details,
            timestamp: Date.now(),
            url: window.location.href,
            userAgent: navigator.userAgent
        };

        // Add to context and trigger update
        this.updateContext({
            interaction: interaction
        }).catch(error => {
            this.logger.error('Failed to track interaction:', error);
        });
    }

    /**
     * Cleanup resources
     */
    cleanup() {
        if (this.websocket) {
            this.websocket.close();
        }

        // Remove suggestion container
        const container = document.getElementById('ai-suggestions-container');
        if (container) {
            container.remove();
        }

        this.logger.log('🧹 AI Context Integration cleaned up');
    }
}

// ================================
// GLOBAL AI CONTEXT INTEGRATION INSTANCE
// ================================

/**
 * Global AI context integration instance
 */
const aiContextIntegration = new AIContextIntegration();

/**
 * Factory function for creating AI context integration
 */
export function createAIContextIntegration() {
    return new AIContextIntegration();
}

// ================================
// EXPORTS
// ================================

export { aiContextIntegration as aiContextIntegration };
export default AIContextIntegration;

// ================================
// AUTO-INITIALIZATION (Optional)
// ================================

// Auto-initialize if running in a browser environment
if (typeof window !== 'undefined' && window.document) {
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            // Auto-initialization can be enabled here if desired
            console.log('🤖 AI Context Integration ready for manual initialization');
        });
    }
}