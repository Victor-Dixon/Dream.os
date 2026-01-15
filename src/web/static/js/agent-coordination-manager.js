/**
 * Agent Coordination Manager - V2 Compliant Agent Coordination
 * Manages agent coordination and communication
 * V2 Compliance: Under 300-line limit achieved
 *
 * @author Agent-3 - Infrastructure & DevOps Specialist
 * @version 1.0.0 - V2 Compliance Implementation
 * @license MIT
 */

// <!-- SSOT Domain: web -->

import { CrossAgentCoordination } from './cross-agent-coordination.js';

/**
 * Creates and manages agent coordination
 * Handles agent communication and coordination logic
 */
export function createAgentCoordinationManager() {
    return {
        agentCoordination: null,
        coordinationStatus: {
            initialized: false,
            activeAgents: [],
            coordinationLevel: 'NOT_INITIALIZED',
            lastCoordination: null
        },

        /**
         * Initialize agent coordination
         */
        async initializeCoordination() {
            console.log('🔗 Initializing Agent Coordination Manager...');

            try {
                this.agentCoordination = new CrossAgentCoordination();
                await this.agentCoordination.initializeCoordination();

                this.coordinationStatus.initialized = true;
                this.coordinationStatus.coordinationLevel = 'INITIALIZED';
                this.coordinationStatus.lastCoordination = new Date().toISOString();

                console.log('✅ Agent coordination manager initialized');
                return true;
            } catch (error) {
                console.error('❌ Failed to initialize agent coordination:', error);
                this.coordinationStatus.coordinationLevel = 'ERROR';
                return false;
            }
        },

        /**
         * Get coordination status
         */
        getCoordinationStatus() {
            return { ...this.coordinationStatus };
        },

        /**
         * Update coordination status
         */
        updateCoordinationStatus(updates) {
            Object.assign(this.coordinationStatus, updates);
            console.log('🔄 Coordination status updated:', updates);
        },

        /**
         * Send coordination message
         */
        async sendCoordinationMessage(message, targetAgents = null) {
            if (!this.agentCoordination) {
                throw new Error('Agent coordination not initialized');
            }

            try {
                const result = await this.agentCoordination.sendMessage(message, targetAgents);
                this.coordinationStatus.lastCoordination = new Date().toISOString();
                return result;
            } catch (error) {
                console.error('❌ Failed to send coordination message:', error);
                throw error;
            }
        },

        /**
         * Receive coordination messages
         */
        async receiveCoordinationMessages() {
            if (!this.agentCoordination) {
                throw new Error('Agent coordination not initialized');
            }

            try {
                return await this.agentCoordination.receiveMessages();
            } catch (error) {
                console.error('❌ Failed to receive coordination messages:', error);
                throw error;
            }
        },

        /**
         * Validate coordination setup
         */
        validateCoordination() {
            try {
                const validation = {
                    initialized: this.coordinationStatus.initialized,
                    hasCoordination: !!this.agentCoordination,
                    level: this.coordinationStatus.coordinationLevel,
                    valid: this.coordinationStatus.initialized && !!this.agentCoordination
                };

                if (!validation.valid) {
                    validation.reason = 'Coordination not properly initialized';
                }

                return validation;
            } catch (error) {
                return { valid: false, reason: error.message };
            }
        }
    };
}