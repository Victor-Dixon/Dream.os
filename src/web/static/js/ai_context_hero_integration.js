/**
 * AI Context Hero Integration - Real-time UX Adaptation
 * ==
 *
 * Phase 5 AI Context Engine integration for hero sections.
 *
 * Features:
 * - Real-time hero personalization based on AI context
 * - WebSocket integration with AI Context Engine
 * - Predictive content loading and animation adaptation
 * - User interaction tracking and engagement analysis
 *
 * Author: Agent-7 (Web Development Specialist)
 * Date: 2026-01-11
 * Phase: Phase 5 - AI Context Engine Integration
 */

class AIContextHeroIntegration {
    constructor(heroType, options = {}) {
        this.heroType = heroType;
        this.options = {
            websocketUrl: options.websocketUrl || 'ws://localhost:8080/ai-context',
            sessionId: options.sessionId || this._generateSessionId(),
            updateInterval: options.updateInterval || 5000,
            engagementThreshold: options.engagementThreshold || 0.7,
            ...options
        };

        this.websocket = null;
        this.sessionData = {
            session_id: this.options.sessionId,
            user_id: this._getUserId(),
            context_type: 'ux',
            context_data: {
                hero_type: heroType,
                user_interactions: [],
                engagement_metrics: {
                    score: 0.5,
                    time_on_page: 0,
                    interaction_rate: 0,
                    content_views: 0
                }
            },
            ai_suggestions: [],
            performance_metrics: {}
        };

        this.startTime = Date.now();
        this.interactionCount = 0;
        this.lastUpdate = Date.now();
        this.lastMessageTime = Date.now();
        this.isConnected = false;
        this.fallbackMode = false;
        this.reconnectAttempts = 0;
        this.heartbeatInterval = null;
        this.connectionTimeout = null;

        this._init();
    }

    _init() {
        this._setupInteractionTracking();
        this._connectWebSocket();
        this._startPeriodicUpdates();
        this._applyInitialPersonalization();

        console.log(`🧠 AI Context Hero Integration initialized for ${this.heroType} hero`);
    }

    _generateSessionId() {
        return `hero_${this.heroType}_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }

    _getUserId() {
        // Check for existing user ID in localStorage or generate new one
        let userId = localStorage.getItem('ai_context_user_id');
        if (!userId) {
            userId = `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
            localStorage.setItem('ai_context_user_id', userId);
        }
        return userId;
    }

    _connectWebSocket() {
        try {
            console.log(`🧠 Connecting to AI Context WebSocket: ${this.options.websocketUrl}`);
            this.websocket = new WebSocket(this.options.websocketUrl);

            // Connection timeout
            this.connectionTimeout = setTimeout(() => {
                if (this.websocket.readyState === WebSocket.CONNECTING) {
                    console.warn('🧠 AI Context WebSocket connection timeout, falling back to HTTP polling');
                    this.websocket.close();
                    this._enableFallbackMode();
                }
            }, 10000);

            this.websocket.onopen = (event) => {
                console.log('🧠 AI Context WebSocket connected successfully');
                clearTimeout(this.connectionTimeout);
                this.isConnected = true;
                this._sendSessionData();
                this._startHeartbeat();
            };

            this.websocket.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    this._handleAISuggestion(data);
                    this.lastMessageTime = Date.now();
                } catch (error) {
                    console.error('🧠 Error parsing AI context message:', error);
                }
            };

            this.websocket.onclose = (event) => {
                console.log(`🧠 AI Context WebSocket disconnected (code: ${event.code}), attempting reconnect...`);
                clearTimeout(this.connectionTimeout);
                this.isConnected = false;
                this._stopHeartbeat();

                if (!this.fallbackMode) {
                    // Exponential backoff for reconnection
                    const reconnectDelay = Math.min(5000 * Math.pow(2, this.reconnectAttempts), 30000);
                    setTimeout(() => {
                        this.reconnectAttempts++;
                        this._connectWebSocket();
                    }, reconnectDelay);
                }
            };

            this.websocket.onerror = (error) => {
                console.error('🧠 AI Context WebSocket error:', error);
                clearTimeout(this.connectionTimeout);
            };

        } catch (error) {
            console.error('🧠 Failed to create WebSocket connection:', error);
            this._enableFallbackMode();
        }
    }

    _startHeartbeat() {
        this.heartbeatInterval = setInterval(() => {
            if (this.websocket && this.websocket.readyState === WebSocket.OPEN) {
                // Send heartbeat ping
                this.websocket.send(JSON.stringify({
                    type: 'ping',
                    session_id: this.sessionData.session_id,
                    timestamp: Date.now()
                }));

                // Check if we've received messages recently
                const timeSinceLastMessage = Date.now() - this.lastMessageTime;
                if (timeSinceLastMessage > 60000) { // 1 minute
                    console.warn('🧠 No messages received for 1 minute, connection may be stale');
                }
            }
        }, 30000); // Every 30 seconds
    }

    _stopHeartbeat() {
        if (this.heartbeatInterval) {
            clearInterval(this.heartbeatInterval);
            this.heartbeatInterval = null;
        }
    }

    _enableFallbackMode() {
        console.log('🧠 Enabling fallback mode - using local AI suggestions');
        this.fallbackMode = true;
        this.isConnected = false;

        // Start polling for local AI suggestions
        this._startFallbackPolling();
    }

    _startFallbackPolling() {
        // Simulate AI suggestions based on local interaction patterns
        this.fallbackInterval = setInterval(() => {
            this._generateLocalAISuggestion();
        }, 10000); // Every 10 seconds
    }

    _generateLocalAISuggestion() {
        // Generate basic suggestions based on current engagement
        const engagement = this.sessionData.context_data.engagement_metrics.score;
        const timeOnPage = (Date.now() - this.startTime) / 1000; // seconds

        let suggestion = null;

        if (engagement > 0.7 && timeOnPage > 30) {
            suggestion = {
                suggestion_type: 'real_time_adaptation',
                content: {
                    adaptation_type: 'high_engagement',
                    suggested_changes: {
                        animation_speed: 'increase_25_percent',
                        hover_effects: 'amplify_feedback'
                    }
                }
            };
        } else if (engagement < 0.3 && timeOnPage > 60) {
            suggestion = {
                suggestion_type: 'ux_personalization',
                content: {
                    personalization: {
                        animations: ['enhanced_glow_effects'],
                        content: {
                            description: 'Discover how our AI-powered system adapts to your preferences in real-time.'
                        },
                        strategy: 'engagement_boost'
                    }
                }
            };
        }

        if (suggestion) {
            console.log('🧠 Generated local AI suggestion:', suggestion.suggestion_type);
            this._handleAISuggestion(suggestion);
        }
    }

            this.websocket.onerror = (error) => {
                console.error('🧠 AI Context WebSocket error:', error);
            };

        } catch (error) {
            console.error('🧠 Failed to connect to AI Context WebSocket:', error);
            // Continue without WebSocket - fallback to local processing
        }
    }

    _setupInteractionTracking() {
        // Track user interactions for AI context analysis
        const trackInteraction = (type, details = {}) => {
            const interaction = {
                type: type,
                timestamp: Date.now(),
                details: details,
                element: details.element || 'unknown'
            };

            this.sessionData.context_data.user_interactions.push(interaction);
            this.interactionCount++;

            // Update engagement metrics
            this._updateEngagementMetrics();

            // Send immediate update for important interactions
            if (type === 'click' || type === 'form_submit') {
                this._sendImmediateUpdate();
            }
        };

        // Scroll tracking
        let scrollTimeout;
        window.addEventListener('scroll', () => {
            clearTimeout(scrollTimeout);
            scrollTimeout = setTimeout(() => {
                const scrollPercent = (window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100;
                trackInteraction('scroll', {
                    scroll_percent: Math.round(scrollPercent),
                    scroll_depth: window.scrollY
                });
            }, 100);
        });

        // Click tracking
        document.addEventListener('click', (event) => {
            trackInteraction('click', {
                element: event.target.tagName.toLowerCase(),
                text: event.target.textContent?.substring(0, 50) || '',
                href: event.target.href || '',
                class: event.target.className || ''
            });
        });

        // Time on page tracking
        setInterval(() => {
            this.sessionData.context_data.engagement_metrics.time_on_page =
                Math.floor((Date.now() - this.startTime) / 1000);
        }, 1000);

        // Mouse movement tracking (subtle engagement indicator)
        let mouseMoveCount = 0;
        document.addEventListener('mousemove', () => {
            mouseMoveCount++;
            if (mouseMoveCount % 50 === 0) { // Every 50 mouse moves
                trackInteraction('mouse_activity', { count: mouseMoveCount });
            }
        });

        console.log('🧠 Interaction tracking initialized');
    }

    _updateEngagementMetrics() {
        const interactions = this.sessionData.context_data.user_interactions;
        const timeOnPage = this.sessionData.context_data.engagement_metrics.time_on_page;

        // Calculate engagement score based on interactions per minute
        const interactionsPerMinute = (this.interactionCount / Math.max(timeOnPage / 60, 1));
        const scrollInteractions = interactions.filter(i => i.type === 'scroll').length;
        const clickInteractions = interactions.filter(i => i.type === 'click').length;

        // Engagement score algorithm
        let engagementScore = 0.3; // Base score

        // Time factor
        if (timeOnPage > 30) engagementScore += 0.2;
        if (timeOnPage > 60) engagementScore += 0.2;

        // Interaction factor
        if (interactionsPerMinute > 1) engagementScore += 0.2;
        if (interactionsPerMinute > 3) engagementScore += 0.2;

        // Specific interaction bonuses
        if (scrollInteractions > 2) engagementScore += 0.1;
        if (clickInteractions > 1) engagementScore += 0.2;

        // Cap at 1.0
        engagementScore = Math.min(1.0, engagementScore);

        this.sessionData.context_data.engagement_metrics.score = engagementScore;
        this.sessionData.context_data.engagement_metrics.interaction_rate = interactionsPerMinute;
        this.sessionData.context_data.engagement_metrics.content_views = interactions.length;
    }

    _startPeriodicUpdates() {
        setInterval(() => {
            this._sendSessionData();
        }, this.options.updateInterval);
    }

    _sendSessionData() {
        if (this.websocket && this.websocket.readyState === WebSocket.OPEN) {
            this.websocket.send(JSON.stringify({
                type: 'session_update',
                data: this.sessionData
            }));
        }
    }

    _sendImmediateUpdate() {
        if (this.websocket && this.websocket.readyState === WebSocket.OPEN) {
            this.websocket.send(JSON.stringify({
                type: 'immediate_update',
                data: this.sessionData
            }));
        }
    }

    _handleAISuggestion(data) {
        if (data.type === 'ai_suggestion' && data.suggestions) {
            data.suggestions.forEach(suggestion => {
                this._applyAISuggestion(suggestion);
            });
        }
    }

    _applyAISuggestion(suggestion) {
        console.log('🧠 Applying AI suggestion:', suggestion.suggestion_type, suggestion);

        // First try to apply to hero section if it exists
        if (window.heroSection && window.heroSection.applyAISuggestion) {
            window.heroSection.applyAISuggestion(suggestion);
        } else {
            // Fallback to original implementation
            switch (suggestion.suggestion_type) {
                case 'ux_personalization':
                    this._applyHeroPersonalization(suggestion.content);
                    break;
                case 'real_time_adaptation':
                    this._applyRealTimeAdaptation(suggestion.content);
                    break;
                case 'predictive_content':
                    this._applyPredictiveContent(suggestion.content);
                    break;
                default:
                    console.log('🧠 Unknown suggestion type:', suggestion.suggestion_type);
            }
        }

        // Mark suggestion as applied
        suggestion.applied = true;
        this.sessionData.ai_suggestions.push(suggestion);
    }

    _applyHeroPersonalization(content) {
        const { personalization, hero_type } = content;

        console.log(`🧠 Applying ${personalization.strategy} personalization for ${hero_type} hero`);

        // Apply animation changes
        personalization.animations.forEach(animation => {
            this._applyAnimationStyle(animation);
        });

        // Update content based on personalization strategy
        this._updateHeroContent(personalization.content, personalization.strategy);
    }

    _applyRealTimeAdaptation(content) {
        const { adaptation_type, suggested_changes } = content;

        console.log(`🧠 Applying real-time adaptation: ${adaptation_type}`);

        // Apply animation speed changes
        if (suggested_changes.animation_speed === 'increase_25_percent') {
            this._accelerateAnimations(1.25);
        }

        // Enhance interactivity
        if (suggested_changes.hover_effects === 'amplify_feedback') {
            this._enhanceHoverEffects();
        }

        // Activate additional elements
        if (suggested_changes.interactive_elements === 'activate_additional_ctas') {
            this._activateAdditionalCTAs();
        }
    }

    _applyPredictiveContent(content) {
        const { prediction } = content;

        console.log(`🧠 Loading predictive content: ${prediction.content_type}`);

        // Load additional content based on prediction
        prediction.elements.forEach(element => {
            this._loadContentElement(element);
        });
    }

    _applyAnimationStyle(animationType) {
        const styleId = `ai-context-style-${animationType}`;
        let styleElement = document.getElementById(styleId);

        if (!styleElement) {
            styleElement = document.createElement('style');
            styleElement.id = styleId;
            document.head.appendChild(styleElement);
        }

        let css = '';
        switch (animationType) {
            case 'accelerated_pixel_float':
                css = `
                    .pixel-float {
                        animation-duration: 2s !important;
                        animation-timing-function: cubic-bezier(0.25, 0.46, 0.45, 0.94) !important;
                    }
                `;
                break;
            case 'enhanced_glow_effects':
                css = `
                    .hero-game-glow {
                        box-shadow: 0 0 30px rgba(255, 0, 255, 0.8), 0 0 60px rgba(255, 0, 255, 0.4) !important;
                    }
                `;
                break;
            case 'accelerated_growth_charts':
                css = `
                    .chart-rise {
                        animation-duration: 1.5s !important;
                    }
                `;
                break;
            case 'professional_network':
                css = `
                    .network-connect {
                        animation-duration: 2.5s !important;
                    }
                `;
                break;
            case 'dynamic_frisbee_physics':
                css = `
                    .frisbee-throw {
                        animation-timing-function: cubic-bezier(0.68, -0.55, 0.265, 1.55) !important;
                    }
                `;
                break;
            case 'crowd_energy':
                css = `
                    .crowd-wave {
                        animation-duration: 1.5s !important;
                    }
                `;
                break;
        }

        styleElement.textContent = css;
    }

    _accelerateAnimations(multiplier) {
        const styleId = 'ai-context-acceleration';
        let styleElement = document.getElementById(styleId);

        if (!styleElement) {
            styleElement = document.createElement('style');
            styleElement.id = styleId;
            document.head.appendChild(styleElement);
        }

        styleElement.textContent = `
            .hero-fade-in-up, .pixel-float, .frisbee-throw, .chart-rise, .network-connect {
                animation-duration: calc(var(--original-duration, 3s) / ${multiplier}) !important;
            }
        `;
    }

    _enhanceHoverEffects() {
        const styleId = 'ai-context-hover-enhancement';
        let styleElement = document.getElementById(styleId);

        if (!styleElement) {
            styleElement = document.createElement('style');
            styleElement.id = styleId;
            document.head.appendChild(styleElement);
        }

        styleElement.textContent = `
            .cta-button-enhanced:hover {
                transform: scale(1.05) translateY(-2px) !important;
                box-shadow: 0 10px 25px rgba(0,0,0,0.3) !important;
                transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
            }
        `;
    }

    _activateAdditionalCTAs() {
        // Find hidden or secondary CTAs and activate them
        const hiddenCTAs = document.querySelectorAll('.cta-button-enhanced[style*="display: none"], .cta-button-enhanced.hidden, .cta-button-enhanced.opacity-0');

        hiddenCTAs.forEach(cta => {
            cta.style.display = 'inline-block';
            cta.style.opacity = '1';
            cta.style.animation = 'fadeInUp 0.8s ease-out';
        });
    }

    _updateHeroContent(content, strategy) {
        // Update hero content based on personalization strategy
        const heroContent = document.querySelector('.hero-content, .hero-section h1, .hero-section p');
        if (heroContent && content) {
            // Add personalized content indicator
            const indicator = document.createElement('div');
            indicator.className = 'ai-personalization-indicator';
            indicator.textContent = `✨ AI Personalized for ${strategy.replace('_', ' ')}`;
            indicator.style.cssText = `
                position: absolute;
                top: 20px;
                right: 20px;
                background: rgba(255, 255, 255, 0.9);
                padding: 5px 10px;
                border-radius: 20px;
                font-size: 12px;
                color: #333;
                opacity: 0.8;
            `;

            const heroSection = document.querySelector('.hero-section, section[class*="hero"]');
            if (heroSection && !heroSection.querySelector('.ai-personalization-indicator')) {
                heroSection.style.position = 'relative';
                heroSection.appendChild(indicator);

                // Fade out indicator after 5 seconds
                setTimeout(() => {
                    indicator.style.transition = 'opacity 1s';
                    indicator.style.opacity = '0';
                    setTimeout(() => indicator.remove(), 1000);
                }, 5000);
            }
        }
    }

    _loadContentElement(elementType) {
        // Load additional content based on prediction
        const contentContainer = document.querySelector('.predictive-content-container');

        if (!contentContainer) {
            // Create container if it doesn't exist
            const container = document.createElement('div');
            container.className = 'predictive-content-container';
            container.style.cssText = `
                margin-top: 40px;
                padding: 20px;
                background: rgba(255, 255, 255, 0.05);
                border-radius: 10px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            `;

            const heroSection = document.querySelector('.hero-section, section[class*="hero"]');
            if (heroSection) {
                heroSection.appendChild(container);
            }
        }

        // Add predictive content based on type
        this._addPredictiveContentElement(elementType);
    }

    _addPredictiveContentElement(elementType) {
        const container = document.querySelector('.predictive-content-container');
        if (!container) return;

        let content = '';
        switch (elementType) {
            case 'game_engine_demos':
                content = '<div class="predictive-item"><h4>🎮 Game Engine Demo</h4><p>Experience our advanced 2D gaming engine with real-time physics and AI companions.</p></div>';
                break;
            case 'case_studies':
                content = '<div class="predictive-item"><h4>📊 Case Studies</h4><p>Explore how our consulting transformed businesses with measurable ROI improvements.</p></div>';
                break;
            case 'live_scores':
                content = '<div class="predictive-item"><h4>🏆 Live Tournament Scores</h4><p>Follow current matches and championship standings in real-time.</p></div>';
                break;
            default:
                content = '<div class="predictive-item"><h4>✨ Premium Feature</h4><p>Discover advanced capabilities tailored to your interests.</p></div>';
        }

        container.insertAdjacentHTML('beforeend', content);

        // Add fade-in animation
        const newItem = container.lastElementChild;
        newItem.style.opacity = '0';
        newItem.style.transform = 'translateY(20px)';
        newItem.style.transition = 'all 0.5s ease-out';

        setTimeout(() => {
            newItem.style.opacity = '1';
            newItem.style.transform = 'translateY(0)';
        }, 100);
    }

    _applyInitialPersonalization() {
        // Apply initial personalization based on hero type
        switch (this.heroType) {
            case 'gaming':
                this._applyAnimationStyle('enhanced_glow_effects');
                break;
            case 'business':
                this._applyAnimationStyle('professional_network');
                break;
            case 'sports':
                this._applyAnimationStyle('crowd_energy');
                break;
        }
    }

    // Public API methods
    getSessionData() {
        return { ...this.sessionData };
    }

    updateEngagementScore(score) {
        this.sessionData.context_data.engagement_metrics.score = score;
        this._sendImmediateUpdate();
    }

    disconnect() {
        console.log('🧠 Disconnecting AI Context Hero Integration');

        // Close WebSocket connection
        if (this.websocket) {
            this.websocket.close(1000, 'Client disconnecting');
        }

        // Clear all timers and intervals
        this._stopHeartbeat();

        if (this.connectionTimeout) {
            clearTimeout(this.connectionTimeout);
            this.connectionTimeout = null;
        }

        if (this.fallbackInterval) {
            clearInterval(this.fallbackInterval);
            this.fallbackInterval = null;
        }

        // Clear session data
        this.sessionData = null;
        this.isConnected = false;

        console.log('🧠 AI Context Hero Integration disconnected');
    }
}

// Global initialization function
function initAIContextHeroIntegration(heroType, options = {}) {
    if (typeof window !== 'undefined') {
        window.aiContextHeroIntegration = new AIContextHeroIntegration(heroType, options);
        return window.aiContextHeroIntegration;
    }
    return null;
}

// Auto-initialize based on page content
document.addEventListener('DOMContentLoaded', () => {
    // Detect hero type from page content
    let heroType = 'general';

    if (document.querySelector('[class*="gaming"], [class*="game"]')) {
        heroType = 'gaming';
    } else if (document.querySelector('[class*="business"], [class*="consulting"]')) {
        heroType = 'business';
    } else if (document.querySelector('[class*="sports"], [class*="event"]')) {
        heroType = 'sports';
    }

    // Initialize with detected hero type
    initAIContextHeroIntegration(heroType, {
        websocketUrl: window.AI_CONTEXT_WS_URL || 'ws://localhost:8080/ai-context'
    });
});

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { AIContextHeroIntegration, initAIContextHeroIntegration };
}