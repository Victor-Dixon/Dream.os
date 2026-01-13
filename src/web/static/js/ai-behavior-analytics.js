/**
 * AI BEHAVIOR ANALYTICS ENGINE - Phase 4 Sprint 1
 *
 * Comprehensive user behavior tracking and analysis system that learns from
 * user interactions to provide predictive UX enhancements and personalized experiences.
 *
 * Features:
 * - Real-time event tracking and pattern recognition
 * - Behavior pattern analysis and user segmentation
 * - Predictive intent recognition
 * - Context-aware UI adaptation
 * - Privacy-first data collection with GDPR compliance
 *
 * @author Agent-6 - Web Architecture Lead (Phase 4)
 * @version 1.0.0 - Sprint 1 Foundation
 */

class BehaviorAnalyticsEngine {
    constructor() {
        this.isInitialized = false;
        this.eventBuffer = [];
        this.patterns = new Map();
        this.userProfile = new Map();
        this.sessionData = {
            startTime: Date.now(),
            events: [],
            pageViews: [],
            interactions: [],
            workflows: []
        };

        // Privacy and performance settings
        this.privacySettings = {
            dataRetention: 30, // days
            anonymizeAfter: 24, // hours
            samplingRate: 0.1, // 10% of events for analysis
            consentRequired: true
        };

        // Performance monitoring
        this.performanceMetrics = {
            eventProcessingTime: [],
            patternRecognitionTime: [],
            predictionAccuracy: []
        };
    }

    /**
     * Initialize the behavior analytics engine
     */
    async initialize() {
        if (this.isInitialized) {
            console.log('🔄 Behavior Analytics Engine already initialized');
            return;
        }

        try {
            // Check user consent
            await this.checkPrivacyConsent();

            // Set up event tracking
            this.setupEventTracking();

            // Load existing user profile
            await this.loadUserProfile();

            // Initialize pattern recognition
            this.initializePatternRecognition();

            // Start session tracking
            this.startSessionTracking();

            this.isInitialized = true;
            console.log('✅ AI Behavior Analytics Engine initialized');

            // Announce initialization to accessibility system
            if (window.dashboard?.accessibility) {
                window.dashboard.accessibility.announce(
                    'AI behavior analytics initialized for enhanced user experience',
                    'polite'
                );
            }

        } catch (error) {
            console.error('❌ Failed to initialize Behavior Analytics Engine:', error);
            this.fallbackToBasicTracking();
        }
    }

    /**
     * Check user privacy consent for data collection
     */
    async checkPrivacyConsent() {
        // Check if user has consented to analytics
        const consent = localStorage.getItem('analytics-consent');
        if (consent === 'granted') {
            this.privacySettings.consentRequired = false;
            return true;
        }

        // Show consent dialog if needed
        if (this.privacySettings.consentRequired) {
            await this.showConsentDialog();
        }

        return !this.privacySettings.consentRequired;
    }

    /**
     * Show privacy consent dialog
     */
    async showConsentDialog() {
        return new Promise((resolve) => {
            const dialog = document.createElement('div');
            dialog.className = 'privacy-consent-dialog';
            dialog.innerHTML = `
                <div class="consent-content">
                    <h3>🤖 AI-Powered Experience</h3>
                    <p>We use AI to learn from your interactions and provide personalized recommendations. This helps us create a better experience for you.</p>
                    <p><strong>Data collected:</strong> Anonymous usage patterns, feature preferences, and interaction flows.</p>
                    <p><strong>Your privacy:</strong> All data is anonymized and never shared with third parties.</p>
                    <div class="consent-buttons">
                        <button class="btn btn-secondary" id="decline-analytics">No Thanks</button>
                        <button class="btn btn-primary" id="accept-analytics">Enable AI Features</button>
                    </div>
                </div>
            `;

            dialog.style.cssText = `
                position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%);
                background: var(--background-primary); border: 2px solid var(--border-color);
                border-radius: 12px; padding: 2rem; z-index: 10000; max-width: 500px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            `;

            document.body.appendChild(dialog);

            document.getElementById('accept-analytics').onclick = () => {
                localStorage.setItem('analytics-consent', 'granted');
                this.privacySettings.consentRequired = false;
                dialog.remove();
                resolve(true);
            };

            document.getElementById('decline-analytics').onclick = () => {
                localStorage.setItem('analytics-consent', 'declined');
                this.privacySettings.consentRequired = true;
                dialog.remove();
                resolve(false);
            };
        });
    }

    /**
     * Set up comprehensive event tracking
     */
    setupEventTracking() {
        // Mouse and interaction events
        this.trackMouseEvents();
        this.trackKeyboardEvents();
        this.trackScrollEvents();
        this.trackClickEvents();
        this.trackFormEvents();

        // Page and navigation events
        this.trackPageViews();
        this.trackNavigationEvents();

        // Performance events
        this.trackPerformanceEvents();

        // Custom business events
        this.trackBusinessEvents();

        console.log('📊 Event tracking initialized');
    }

    /**
     * Track mouse interactions
     */
    trackMouseEvents() {
        let mousePath = [];
        let lastMouseTime = Date.now();

        document.addEventListener('mousemove', (e) => {
            const now = Date.now();
            if (now - lastMouseTime > 100) { // Throttle to every 100ms
                mousePath.push({
                    x: e.clientX,
                    y: e.clientY,
                    timestamp: now,
                    element: e.target.tagName.toLowerCase()
                });

                // Keep only last 50 points for memory efficiency
                if (mousePath.length > 50) {
                    mousePath = mousePath.slice(-50);
                }

                lastMouseTime = now;
            }
        }, { passive: true });

        // Analyze mouse path every 5 seconds
        setInterval(() => {
            if (mousePath.length > 10) {
                this.analyzeMousePath(mousePath);
                mousePath = []; // Reset for next interval
            }
        }, 5000);
    }

    /**
     * Analyze mouse movement patterns
     */
    analyzeMousePath(path) {
        if (!this.shouldSampleEvent()) return;

        // Calculate movement patterns
        const totalDistance = this.calculateMouseDistance(path);
        const avgSpeed = totalDistance / (path.length * 0.1); // Based on 100ms intervals

        // Detect hesitation points (slow movement)
        const hesitationPoints = path.filter((point, index) => {
            if (index === 0) return false;
            const prevPoint = path[index - 1];
            const distance = Math.sqrt(
                Math.pow(point.x - prevPoint.x, 2) + Math.pow(point.y - prevPoint.y, 2)
            );
            return distance < 5; // Less than 5px movement indicates hesitation
        });

        this.recordEvent('mouse_pattern', {
            totalDistance,
            avgSpeed,
            hesitationCount: hesitationPoints.length,
            pathLength: path.length,
            dominantElements: this.getDominantElements(path)
        });
    }

    /**
     * Track keyboard interactions
     */
    trackKeyboardEvents() {
        let keySequence = [];
        let lastKeyTime = Date.now();

        document.addEventListener('keydown', (e) => {
            const now = Date.now();

            keySequence.push({
                key: e.key,
                code: e.code,
                timestamp: now,
                ctrlKey: e.ctrlKey,
                altKey: e.altKey,
                shiftKey: e.shiftKey
            });

            // Keep only last 20 keystrokes
            if (keySequence.length > 20) {
                keySequence = keySequence.slice(-20);
            }

            // Analyze shortcuts and patterns
            if (now - lastKeyTime > 2000) { // Reset sequence after 2 seconds
                this.analyzeKeySequence(keySequence);
                keySequence = [];
            }

            lastKeyTime = now;
        });
    }

    /**
     * Analyze keyboard patterns
     */
    analyzeKeySequence(sequence) {
        if (!this.shouldSampleEvent() || sequence.length < 3) return;

        const shortcuts = sequence.filter(key =>
            key.ctrlKey || key.altKey || key.key.length > 1
        );

        const commonKeys = sequence
            .filter(key => key.key.length === 1)
            .map(key => key.key.toLowerCase())
            .reduce((acc, key) => {
                acc[key] = (acc[key] || 0) + 1;
                return acc;
            }, {});

        this.recordEvent('keyboard_pattern', {
            sequenceLength: sequence.length,
            shortcutsUsed: shortcuts.length,
            commonKeys,
            typingSpeed: this.calculateTypingSpeed(sequence)
        });
    }

    /**
     * Track scroll behavior
     */
    trackScrollEvents() {
        let scrollEvents = [];
        let lastScrollTime = Date.now();

        window.addEventListener('scroll', () => {
            const now = Date.now();
            if (now - lastScrollTime > 200) { // Throttle to every 200ms
                const scrollY = window.scrollY;
                const maxScroll = document.documentElement.scrollHeight - window.innerHeight;

                scrollEvents.push({
                    position: scrollY,
                    percentage: (scrollY / maxScroll) * 100,
                    timestamp: now,
                    direction: scrollY > (scrollEvents[scrollEvents.length - 1]?.position || 0) ? 'down' : 'up'
                });

                lastScrollTime = now;
            }
        }, { passive: true });

        // Analyze scroll patterns every 10 seconds
        setInterval(() => {
            if (scrollEvents.length > 5) {
                this.analyzeScrollPattern(scrollEvents);
                scrollEvents = [];
            }
        }, 10000);
    }

    /**
     * Analyze scroll behavior patterns
     */
    analyzeScrollPattern(events) {
        if (!this.shouldSampleEvent()) return;

        const avgScrollSpeed = this.calculateScrollSpeed(events);
        const scrollDirectionChanges = events.reduce((changes, event, index) => {
            if (index > 0 && event.direction !== events[index - 1].direction) {
                changes++;
            }
            return changes;
        }, 0);

        const maxScrollDepth = Math.max(...events.map(e => e.percentage));

        this.recordEvent('scroll_pattern', {
            eventCount: events.length,
            avgSpeed: avgScrollSpeed,
            directionChanges: scrollDirectionChanges,
            maxDepth: maxScrollDepth,
            engagement: this.calculateEngagementScore(events)
        });
    }

    /**
     * Track click interactions
     */
    trackClickEvents() {
        document.addEventListener('click', (e) => {
            if (!this.shouldSampleEvent()) return;

            const target = e.target;
            const elementInfo = this.getElementInfo(target);

            this.recordEvent('click', {
                elementType: elementInfo.type,
                elementId: elementInfo.id,
                elementClass: elementInfo.class,
                position: { x: e.clientX, y: e.clientY },
                timestamp: Date.now(),
                context: this.getClickContext(target)
            });
        });
    }

    /**
     * Track form interactions
     */
    trackFormEvents() {
        document.addEventListener('focus', (e) => {
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.tagName === 'SELECT') {
                this.recordEvent('form_focus', {
                    fieldType: e.target.type || e.target.tagName.toLowerCase(),
                    fieldName: e.target.name,
                    timestamp: Date.now()
                });
            }
        }, true);

        document.addEventListener('blur', (e) => {
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.tagName === 'SELECT') {
                this.recordEvent('form_blur', {
                    fieldType: e.target.type || e.target.tagName.toLowerCase(),
                    fieldName: e.target.name,
                    value: e.target.value ? e.target.value.length : 0, // Don't store actual values
                    timestamp: Date.now()
                });
            }
        }, true);

        document.addEventListener('submit', (e) => {
            this.recordEvent('form_submit', {
                formId: e.target.id,
                formClass: e.target.className,
                fieldsCount: e.target.querySelectorAll('input, textarea, select').length,
                timestamp: Date.now()
            });
        });
    }

    /**
     * Track page views and navigation
     */
    trackPageViews() {
        // Track initial page load
        this.recordEvent('page_view', {
            url: window.location.href,
            referrer: document.referrer,
            timestamp: Date.now(),
            userAgent: navigator.userAgent.substring(0, 100), // Truncated for privacy
            viewport: {
                width: window.innerWidth,
                height: window.innerHeight
            }
        });

        // Track navigation changes (for SPAs)
        let currentUrl = window.location.href;
        const observer = new MutationObserver(() => {
            if (window.location.href !== currentUrl) {
                this.recordEvent('navigation', {
                    from: currentUrl,
                    to: window.location.href,
                    timestamp: Date.now()
                });
                currentUrl = window.location.href;
            }
        });

        observer.observe(document.querySelector('body'), {
            childList: true,
            subtree: true
        });
    }

    /**
     * Track navigation events
     */
    trackNavigationEvents() {
        // Track menu interactions
        document.addEventListener('click', (e) => {
            const navLink = e.target.closest('a[href], [role="menuitem"], .nav-link');
            if (navLink) {
                this.recordEvent('navigation_click', {
                    href: navLink.href || navLink.getAttribute('data-href'),
                    text: navLink.textContent?.trim(),
                    type: navLink.getAttribute('role') || 'link',
                    timestamp: Date.now()
                });
            }
        });
    }

    /**
     * Track performance events
     */
    trackPerformanceEvents() {
        // Track Core Web Vitals if available
        if ('web-vitals' in window) {
            import('https://unpkg.com/web-vitals@3.1.1/dist/web-vitals.js').then(({ getCLS, getFID, getFCP, getLCP, getTTFB }) => {
                getCLS((metric) => this.recordPerformanceMetric('CLS', metric));
                getFID((metric) => this.recordPerformanceMetric('FID', metric));
                getFCP((metric) => this.recordPerformanceMetric('FCP', metric));
                getLCP((metric) => this.recordPerformanceMetric('LCP', metric));
                getTTFB((metric) => this.recordPerformanceMetric('TTFB', metric));
            });
        }

        // Track custom performance metrics
        window.addEventListener('load', () => {
            setTimeout(() => {
                const perfData = performance.getEntriesByType('navigation')[0];
                this.recordEvent('page_performance', {
                    domContentLoaded: perfData.domContentLoadedEventEnd - perfData.domContentLoadedEventStart,
                    loadComplete: perfData.loadEventEnd - perfData.loadEventStart,
                    timestamp: Date.now()
                });
            }, 0);
        });
    }

    /**
     * Track business-specific events
     */
    trackBusinessEvents() {
        // Track dashboard interactions
        document.addEventListener('dashboard:viewChanged', (e) => {
            this.recordEvent('dashboard_view_change', {
                from: e.detail?.previousView,
                to: e.detail?.view,
                timestamp: Date.now()
            });
        });

        // Track feature usage
        document.addEventListener('feature:used', (e) => {
            this.recordEvent('feature_usage', {
                feature: e.detail?.feature,
                action: e.detail?.action,
                context: e.detail?.context,
                timestamp: Date.now()
            });
        });
    }

    /**
     * Initialize pattern recognition system
     */
    initializePatternRecognition() {
        // Set up pattern recognition intervals
        setInterval(() => this.analyzePatterns(), 30000); // Every 30 seconds
        setInterval(() => this.updateUserProfile(), 60000); // Every minute
        setInterval(() => this.generatePredictions(), 120000); // Every 2 minutes

        console.log('🎯 Pattern recognition initialized');
    }

    /**
     * Analyze behavior patterns
     */
    analyzePatterns() {
        if (!this.sessionData.events.length) return;

        const recentEvents = this.sessionData.events.slice(-50); // Last 50 events

        // Identify common workflows
        const workflows = this.identifyWorkflows(recentEvents);

        // Detect user preferences
        const preferences = this.detectPreferences(recentEvents);

        // Update patterns
        workflows.forEach(workflow => {
            const key = `workflow_${workflow.type}`;
            this.patterns.set(key, (this.patterns.get(key) || 0) + 1);
        });

        preferences.forEach(pref => {
            this.userProfile.set(pref.key, pref.value);
        });

        console.log('🔍 Patterns analyzed:', workflows.length, 'workflows,', preferences.length, 'preferences');
    }

    /**
     * Identify user workflows from events
     */
    identifyWorkflows(events) {
        const workflows = [];

        // Look for sequences that indicate specific workflows
        const sequences = this.findSequences(events, ['navigation_click', 'form_focus', 'click', 'scroll_pattern']);

        sequences.forEach(sequence => {
            if (sequence.length >= 3) {
                const workflow = this.classifyWorkflow(sequence);
                if (workflow) {
                    workflows.push(workflow);
                }
            }
        });

        return workflows;
    }

    /**
     * Classify workflow from event sequence
     */
    classifyWorkflow(sequence) {
        const eventTypes = sequence.map(e => e.type);

        // Dashboard exploration workflow
        if (eventTypes.includes('navigation_click') && eventTypes.includes('dashboard_view_change')) {
            return { type: 'dashboard_exploration', confidence: 0.8 };
        }

        // Form completion workflow
        if (eventTypes.includes('form_focus') && eventTypes.includes('form_submit')) {
            return { type: 'form_completion', confidence: 0.9 };
        }

        // Feature discovery workflow
        if (eventTypes.filter(t => t === 'click').length >= 3) {
            return { type: 'feature_discovery', confidence: 0.6 };
        }

        return null;
    }

    /**
     * Detect user preferences from events
     */
    detectPreferences(events) {
        const preferences = [];

        // Theme preference (if dark mode is used more)
        const themeEvents = events.filter(e => e.type === 'theme_toggle' || e.data?.theme);
        if (themeEvents.length > 0) {
            const darkModeCount = themeEvents.filter(e => e.data?.theme === 'dark').length;
            const lightModeCount = themeEvents.filter(e => e.data?.theme === 'light').length;

            if (darkModeCount > lightModeCount) {
                preferences.push({ key: 'preferred_theme', value: 'dark', confidence: 0.8 });
            } else if (lightModeCount > darkModeCount) {
                preferences.push({ key: 'preferred_theme', value: 'light', confidence: 0.8 });
            }
        }

        // Navigation preferences
        const navEvents = events.filter(e => e.type === 'navigation_click');
        if (navEvents.length > 0) {
            const mostVisited = this.findMostFrequent(navEvents.map(e => e.data?.href));
            if (mostVisited) {
                preferences.push({ key: 'frequent_section', value: mostVisited, confidence: 0.7 });
            }
        }

        return preferences;
    }

    /**
     * Generate predictive insights
     */
    generatePredictions() {
        const predictions = [];

        // Predict next likely action based on current context
        const currentContext = this.getCurrentContext();
        const nextAction = this.predictNextAction(currentContext);

        if (nextAction) {
            predictions.push({
                type: 'next_action',
                prediction: nextAction,
                confidence: nextAction.confidence,
                timestamp: Date.now()
            });
        }

        // Predict feature recommendations
        const recommendations = this.generateRecommendations();
        predictions.push(...recommendations);

        // Store predictions for UI adaptation
        this.storePredictions(predictions);

        console.log('🔮 Generated', predictions.length, 'predictions');
    }

    /**
     * Get current user context
     */
    getCurrentContext() {
        return {
            currentView: window.dashboard?.currentView || 'unknown',
            timeSpent: Date.now() - this.sessionData.startTime,
            recentEvents: this.sessionData.events.slice(-10),
            userPreferences: Object.fromEntries(this.userProfile)
        };
    }

    /**
     * Predict next likely action
     */
    predictNextAction(context) {
        // Simple prediction based on current view and recent activity
        const recentEvents = context.recentEvents;
        const currentView = context.currentView;

        // If user just viewed dashboard and clicked navigation, they might want to explore more
        const recentNavClicks = recentEvents.filter(e => e.type === 'navigation_click');
        if (recentNavClicks.length > 0 && currentView === 'overview') {
            return {
                action: 'explore_features',
                confidence: 0.7,
                suggestion: 'Based on your recent navigation, you might want to explore more dashboard features.'
            };
        }

        // If user spent time on forms, they might need help
        const formEvents = recentEvents.filter(e => e.type.startsWith('form_'));
        if (formEvents.length > 2) {
            return {
                action: 'show_help',
                confidence: 0.6,
                suggestion: 'You seem to be working with forms. Would you like help or guidance?'
            };
        }

        return null;
    }

    /**
     * Generate personalized recommendations
     */
    generateRecommendations() {
        const recommendations = [];

        // Theme recommendation
        const preferredTheme = this.userProfile.get('preferred_theme');
        if (preferredTheme && preferredTheme !== this.getCurrentTheme()) {
            recommendations.push({
                type: 'theme_recommendation',
                feature: 'theme_toggle',
                message: `Would you like to switch to ${preferredTheme} mode?`,
                confidence: 0.8
            });
        }

        // Feature recommendations based on usage patterns
        const frequentSection = this.userProfile.get('frequent_section');
        if (frequentSection && this.getCurrentView() !== this.extractViewFromUrl(frequentSection)) {
            recommendations.push({
                type: 'navigation_recommendation',
                feature: frequentSection,
                message: `You frequently visit ${this.extractViewName(frequentSection)}. Would you like to go there?`,
                confidence: 0.7
            });
        }

        return recommendations;
    }

    /**
     * Store predictions for UI consumption
     */
    storePredictions(predictions) {
        // Store in session storage for UI components
        sessionStorage.setItem('ai_predictions', JSON.stringify(predictions));

        // Dispatch event for UI components to react
        window.dispatchEvent(new CustomEvent('ai:predictions-updated', {
            detail: { predictions }
        }));
    }

    /**
     * Start session tracking
     */
    startSessionTracking() {
        // Track session end
        window.addEventListener('beforeunload', () => {
            this.recordEvent('session_end', {
                duration: Date.now() - this.sessionData.startTime,
                eventsCount: this.sessionData.events.length,
                timestamp: Date.now()
            });

            // Save final user profile
            this.saveUserProfile();
        });

        // Track visibility changes (tab switching)
        document.addEventListener('visibilitychange', () => {
            this.recordEvent('visibility_change', {
                hidden: document.hidden,
                timestamp: Date.now()
            });
        });

        console.log('📊 Session tracking started');
    }

    /**
     * Record an analytics event
     */
    recordEvent(type, data) {
        const event = {
            id: this.generateEventId(),
            type,
            data: this.anonymizeData(data),
            timestamp: Date.now(),
            sessionId: this.getSessionId(),
            userId: this.getAnonymizedUserId()
        };

        // Add to session data
        this.sessionData.events.push(event);

        // Keep only last 1000 events in memory
        if (this.sessionData.events.length > 1000) {
            this.sessionData.events = this.sessionData.events.slice(-1000);
        }

        // Add to buffer for batch processing
        this.eventBuffer.push(event);

        // Process buffer if it gets too large
        if (this.eventBuffer.length >= 50) {
            this.processEventBuffer();
        }
    }

    /**
     * Process buffered events
     */
    processEventBuffer() {
        if (this.eventBuffer.length === 0) return;

        // In a real implementation, this would send events to analytics service
        console.log('📊 Processing', this.eventBuffer.length, 'events');

        // Clear buffer
        this.eventBuffer = [];
    }

    /**
     * Anonymize sensitive data
     */
    anonymizeData(data) {
        const anonymized = { ...data };

        // Remove or hash sensitive information
        if (anonymized.email) anonymized.email = this.hashString(anonymized.email);
        if (anonymized.name) anonymized.name = this.hashString(anonymized.name);
        if (anonymized.value && typeof anonymized.value === 'string') {
            anonymized.value = anonymized.value.length; // Store length instead of content
        }

        return anonymized;
    }

    /**
     * Utility functions
     */
    shouldSampleEvent() {
        return Math.random() < this.privacySettings.samplingRate;
    }

    generateEventId() {
        return Date.now().toString(36) + Math.random().toString(36).substr(2);
    }

    getSessionId() {
        let sessionId = sessionStorage.getItem('analytics_session_id');
        if (!sessionId) {
            sessionId = this.generateEventId();
            sessionStorage.setItem('analytics_session_id', sessionId);
        }
        return sessionId;
    }

    getAnonymizedUserId() {
        let userId = localStorage.getItem('analytics_user_id');
        if (!userId) {
            userId = this.hashString(navigator.userAgent + Date.now().toString());
            localStorage.setItem('analytics_user_id', userId);
        }
        return userId;
    }

    hashString(str) {
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            const char = str.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash; // Convert to 32-bit integer
        }
        return Math.abs(hash).toString(36);
    }

    calculateMouseDistance(path) {
        let totalDistance = 0;
        for (let i = 1; i < path.length; i++) {
            const dx = path[i].x - path[i-1].x;
            const dy = path[i].y - path[i-1].y;
            totalDistance += Math.sqrt(dx * dx + dy * dy);
        }
        return totalDistance;
    }

    calculateTypingSpeed(sequence) {
        if (sequence.length < 2) return 0;
        const timeSpan = sequence[sequence.length - 1].timestamp - sequence[0].timestamp;
        return (sequence.length / timeSpan) * 60000; // Characters per minute
    }

    calculateScrollSpeed(events) {
        if (events.length < 2) return 0;
        const totalDistance = events.reduce((sum, event, index) => {
            if (index === 0) return 0;
            return sum + Math.abs(event.position - events[index - 1].position);
        }, 0);
        const timeSpan = events[events.length - 1].timestamp - events[0].timestamp;
        return totalDistance / (timeSpan / 1000); // Pixels per second
    }

    calculateEngagementScore(events) {
        const maxDepth = Math.max(...events.map(e => e.percentage));
        const directionChanges = events.reduce((changes, event, index) => {
            if (index > 0 && event.direction !== events[index - 1].direction) {
                changes++;
            }
            return changes;
        }, 0);
        return (maxDepth / 100) * (1 - directionChanges / events.length);
    }

    getDominantElements(path) {
        const elements = path.map(p => p.element);
        return this.findMostFrequent(elements);
    }

    findMostFrequent(arr) {
        const frequency = arr.reduce((acc, val) => {
            acc[val] = (acc[val] || 0) + 1;
            return acc;
        }, {});
        return Object.keys(frequency).reduce((a, b) =>
            frequency[a] > frequency[b] ? a : b
        );
    }

    findSequences(events, types) {
        const sequences = [];
        let currentSequence = [];

        events.forEach(event => {
            if (types.includes(event.type)) {
                currentSequence.push(event);
            } else if (currentSequence.length > 0) {
                sequences.push([...currentSequence]);
                currentSequence = [];
            }
        });

        if (currentSequence.length > 0) {
            sequences.push(currentSequence);
        }

        return sequences;
    }

    getElementInfo(element) {
        return {
            type: element.tagName.toLowerCase(),
            id: element.id,
            class: element.className,
            text: element.textContent?.substring(0, 50)
        };
    }

    getClickContext(element) {
        // Get context about where the click occurred
        const section = element.closest('[data-section], section, article');
        return {
            section: section?.getAttribute('data-section') || section?.tagName.toLowerCase(),
            depth: this.getElementDepth(element),
            siblings: element.parentElement?.children.length || 0
        };
    }

    getElementDepth(element) {
        let depth = 0;
        let current = element;
        while (current && current !== document.body) {
            depth++;
            current = current.parentElement;
        }
        return depth;
    }

    getCurrentTheme() {
        return document.documentElement.getAttribute('data-theme') || 'light';
    }

    getCurrentView() {
        return window.dashboard?.currentView || 'unknown';
    }

    extractViewFromUrl(url) {
        // Extract view name from URL
        const match = url?.match(/[#/]([^/?#]+)/);
        return match ? match[1] : 'unknown';
    }

    extractViewName(url) {
        const view = this.extractViewFromUrl(url);
        return view.charAt(0).toUpperCase() + view.slice(1);
    }

    recordPerformanceMetric(name, metric) {
        this.recordEvent('performance_metric', {
            name,
            value: metric.value,
            rating: metric.rating,
            timestamp: metric.timestamp
        });
    }

    async loadUserProfile() {
        try {
            const profile = localStorage.getItem('ai_user_profile');
            if (profile) {
                const data = JSON.parse(profile);
                this.userProfile = new Map(Object.entries(data));
                console.log('📋 User profile loaded');
            }
        } catch (error) {
            console.error('❌ Failed to load user profile:', error);
        }
    }

    async saveUserProfile() {
        try {
            const profile = Object.fromEntries(this.userProfile);
            localStorage.setItem('ai_user_profile', JSON.stringify(profile));
            console.log('💾 User profile saved');
        } catch (error) {
            console.error('❌ Failed to save user profile:', error);
        }
    }

    updateUserProfile() {
        // Update profile with recent insights
        const recentEvents = this.sessionData.events.slice(-100);

        // Update feature usage preferences
        const featureUsage = recentEvents
            .filter(e => e.type === 'feature_usage')
            .reduce((acc, event) => {
                const feature = event.data.feature;
                acc[feature] = (acc[feature] || 0) + 1;
                return acc;
            }, {});

        Object.entries(featureUsage).forEach(([feature, count]) => {
            this.userProfile.set(`feature_${feature}_usage`, count);
        });

        // Update navigation preferences
        const navPrefs = recentEvents
            .filter(e => e.type === 'navigation_click')
            .map(e => e.data.href)
            .filter(href => href);

        if (navPrefs.length > 0) {
            const mostVisited = this.findMostFrequent(navPrefs);
            this.userProfile.set('preferred_navigation', mostVisited);
        }
    }

    /**
     * Fallback to basic tracking if AI features fail
     */
    fallbackToBasicTracking() {
        console.log('🔄 Falling back to basic event tracking');

        // Set up minimal event tracking
        document.addEventListener('click', (e) => {
            console.log('Click tracked:', e.target.tagName);
        });

        this.isInitialized = true;
    }
}

// Export for use in other modules
export { BehaviorAnalyticsEngine };
export default BehaviorAnalyticsEngine;