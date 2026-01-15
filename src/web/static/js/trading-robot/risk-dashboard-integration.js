/**
 * Risk Dashboard Integration - V2 Compliant
 * Integration module for Trading Robot to consume risk metrics from WebSocket server
 * Enables trading plugins to display real-time risk analytics
 *
 * <!-- SSOT Domain: trading_robot -->
 *
 * Navigation References:
 * ├── Related Files:
 * │   ├── WebSocket Server → src/services/risk_analytics/risk_websocket_server.py
 * │   ├── Risk Calculator → src/services/risk_analytics/risk_calculator_service.py
 * │   ├── API Endpoints → src/services/risk_analytics/risk_api_endpoints.py
 * │   └── Trading Dashboard → src/web/static/js/trading-robot/trading-dashboard.js
 * ├── Documentation:
 * │   ├── Architecture → docs/analytics/TRADINGROBOTPLUG_ANALYTICS_ARCHITECTURE.md
 * │   ├── Integration Demo → docs/analytics/trading_robot_risk_integration_demo.html
 * │   └── Risk Dashboard → docs/analytics/risk_dashboard.html
 * └── Usage:
 *     └── Risk Integration → new RiskDashboardIntegration().initialize()
 *
 * Bidirectional Links:
 * ├── From Code to Docs:
 * │   ├── This integration → docs/analytics/TRADINGROBOTPLUG_ANALYTICS_ARCHITECTURE.md
 * │   ├── This integration → docs/analytics/trading_robot_risk_integration_demo.html
 * │   └── This integration → docs/analytics/risk_dashboard.html
 * └── From Docs to Code:
 *     ├── docs/analytics/TRADINGROBOTPLUG_ANALYTICS_ARCHITECTURE.md → This integration
 *     ├── docs/analytics/trading_robot_risk_integration_demo.html → This integration
 *     └── docs/analytics/risk_dashboard.html → This integration
 *
 * @author Agent-4 (Captain) - Working Solo Implementation
 * @version 1.0.0 - Risk Dashboard Integration for Trading Plugins
 * @license MIT
 */

import { AppManagementModules } from './app-management-modules.js';

/**
 * Risk Dashboard Integration for Trading Robot
 * Provides real-time risk metrics to trading plugins and dashboard components
 */
export class RiskDashboardIntegration {
    constructor() {
        this.websocket = null;
        this.isConnected = false;
        this.riskMetrics = {};
        this.alerts = [];
        this.subscribers = new Set();
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 3000; // 3 seconds

        // WebSocket server URL for risk metrics
        this.wsUrl = 'ws://localhost:8765/ws/risk/live';

        // V2 Compliance: Structured logging
        this.logger = {
            log: (message) => {
                const timestamp = new Date().toISOString();
                const logEntry = `[${timestamp}] RISK-DASHBOARD: ${message}`;
                console.log(logEntry);
            },
            error: (message, error) => {
                const timestamp = new Date().toISOString();
                const errorEntry = `[${timestamp}] RISK-DASHBOARD ERROR: ${message}`;
                console.error(errorEntry, error);
            }
        };
    }

    /**
     * Initialize risk dashboard integration
     */
    async initialize() {
        this.logger.log('🚀 Initializing Risk Dashboard Integration...');

        try {
            await this.connectWebSocket();
            this.logger.log('✅ Risk Dashboard Integration initialized successfully');
        } catch (error) {
            this.logger.error('❌ Risk Dashboard Integration initialization failed:', error);
            throw error;
        }
    }

    /**
     * Connect to risk WebSocket server
     */
    async connectWebSocket() {
        try {
            this.logger.log(`🔌 Connecting to risk WebSocket server: ${this.wsUrl}`);
            this.websocket = new WebSocket(this.wsUrl);

            return new Promise((resolve, reject) => {
                this.websocket.onopen = () => {
                    this.isConnected = true;
                    this.reconnectAttempts = 0;
                    this.logger.log('🟢 Connected to risk WebSocket server');
                    resolve();
                };

                this.websocket.onmessage = (event) => {
                    this.handleMessage(event.data);
                };

                this.websocket.onclose = () => {
                    this.isConnected = false;
                    this.logger.log('🔴 Disconnected from risk WebSocket server');
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
            this.logger.error('Failed to connect to risk WebSocket:', error);
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




     *
     * Navigation References:
     * ├── WebSocket Server → src/services/risk_analytics/risk_websocket_server.py::_handle_live_connection()
     * ├── Risk Calculator → src/services/risk_analytics/risk_calculator_service.py::calculate_comprehensive_risk_metrics()
     * ├── Trading Dashboard → src/web/static/js/trading-robot/trading-dashboard.js
     * ├── Risk Alerts → src/web/static/js/trading-robot/risk-alerts.js
     * ├── Chart Updates → src/web/static/js/trading-robot/risk-charts.js::updateRiskCharts()
     * └── Message Format → docs/analytics/TRADINGROBOTPLUG_ANALYTICS_ARCHITECTURE.md#websocket-protocol
     *
     * Message processing pipeline:
     * 1. Parse JSON message from WebSocket server
     * 2. Route by message type (risk_metrics_live, heartbeat, etc.)
     * 3. Update local risk metrics state
     * 4. Check and generate risk alerts
     * 5. Notify all dashboard subscribers
     * 6. Trigger UI updates and chart refreshes

     */

     */
    handleMessage(data) {


     */

        try {
            const message = JSON.parse(data);

            switch (message.type) {
                case 'risk_metrics_live':
                    this.updateRiskMetrics(message);
                    break;
                case 'heartbeat':
                    // Heartbeat received, server is alive
                    break;
                default:
                    this.logger.log(`Unknown message type: ${message.type}`);
            }
        } catch (error) {
            this.logger.error('Failed to parse WebSocket message:', error);
        }
    }

    /**
     * Update risk metrics and notify subscribers
     */
    updateRiskMetrics(message) {
        this.riskMetrics = {
            ...message.metrics,
            timestamp: message.timestamp,
            portfolioId: message.portfolio_id
        };

        // Check for risk alerts
        this.checkRiskAlerts();

        // Notify all subscribers
        this.notifySubscribers();
    }

    /**
     * Check for risk alerts based on current metrics
     */
    checkRiskAlerts() {
        const alerts = [];

        // VaR threshold alert
        if (this.riskMetrics.var_95 > 0.20) {
            alerts.push({
                level: 'high',
                type: 'var_threshold',
                message: `VaR ${this.formatPercent(this.riskMetrics.var_95)} exceeds 20% threshold`,
                value: this.riskMetrics.var_95,
                threshold: 0.20,
                timestamp: Date.now()
            });
        }

        // Sharpe ratio alert
        if (this.riskMetrics.sharpe_ratio < 1.0) {
            alerts.push({
                level: 'medium',
                type: 'sharpe_ratio',
                message: `Sharpe ratio ${this.riskMetrics.sharpe_ratio.toFixed(2)} below 1.0 minimum`,
                value: this.riskMetrics.sharpe_ratio,
                threshold: 1.0,
                timestamp: Date.now()
            });
        }

        // Drawdown alert
        if (this.riskMetrics.max_drawdown > 0.10) {
            alerts.push({
                level: 'critical',
                type: 'max_drawdown',
                message: `Drawdown ${this.formatPercent(this.riskMetrics.max_drawdown)} exceeds 10% threshold`,
                value: this.riskMetrics.max_drawdown,
                threshold: 0.10,
                timestamp: Date.now()
            });
        }

        this.alerts = alerts;
    }

    /**
     * Subscribe to risk metrics updates
     */
    subscribe(callback) {
        this.subscribers.add(callback);

        // Immediately send current metrics if available
        if (Object.keys(this.riskMetrics).length > 0) {
            callback({
                type: 'risk_update',
                metrics: this.riskMetrics,
                alerts: this.alerts
            });
        }

        // Return unsubscribe function
        return () => {
            this.subscribers.delete(callback);
        };
    }

    /**
     * Notify all subscribers of updates
     */
    notifySubscribers() {
        const update = {
            type: 'risk_update',
            metrics: this.riskMetrics,
            alerts: this.alerts
        };

        this.subscribers.forEach(callback => {
            try {
                callback(update);
            } catch (error) {
                this.logger.error('Subscriber callback error:', error);
            }
        });
    }

    /**
     * Get current risk metrics
     */
    getCurrentMetrics() {
        return {
            metrics: this.riskMetrics,
            alerts: this.alerts,
            isConnected: this.isConnected
        };
    }

    /**
     * Format percentage values
     */
    formatPercent(value) {
        return (value * 100).toFixed(1) + '%';
    }

    /**
     * Cleanup resources
     */
    cleanup() {
        if (this.websocket) {
            this.websocket.close();
        }
        this.subscribers.clear();
        this.logger.log('🧹 Risk Dashboard Integration cleaned up');
    }
}

// ====
// GLOBAL RISK DASHBOARD INTEGRATION INSTANCE
// ====

/**
 * Global risk dashboard integration instance
 */
const globalRiskDashboardIntegration = new RiskDashboardIntegration();

/**
 * Factory function for creating risk dashboard integration
 */
export function createRiskDashboardIntegration() {
    return new RiskDashboardIntegration();
}

// ====
// EXPORTS
// ====

export { globalRiskDashboardIntegration as riskDashboardIntegration };
export default RiskDashboardIntegration;