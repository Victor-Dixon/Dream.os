<<<<<<< HEAD
<!-- SSOT Domain: gaming -->
/**
 * Gamification UI - Dream.OS Integration
 * XP, Skills, Quests, and Achievement System
 * 
 * V2 Compliance: Modern, responsive gamification interface
 * Author: Agent-7 - Repository Cloning Specialist
 * Version: 1.0.0 - C-084 Implementation
 * License: MIT
 */

// ================================
// GAMIFICATION UI SYSTEM
// ================================

/**
 * Main Gamification UI Controller
 */
export class GamificationUI {
    constructor(options = {}) {
        this.container = options.container || document.getElementById('gamificationContainer');
        this.config = {
            enableAnimations: options.enableAnimations !== false,
            autoRefresh: options.autoRefresh !== false,
            refreshInterval: options.refreshInterval || 30000,
            theme: options.theme || 'dark'
        };
        
        this.state = {
            currentXP: 0,
            currentLevel: 1,
            totalXP: 0,
            skills: [],
            activeQuests: [],
            completedQuests: [],
            achievements: []
        };
        
        this.refreshTimer = null;
        this.socket = null;
        this.realtimeEnabled = true;
    }
    
    /**
     * Initialize the gamification UI
     */
    async initialize() {
        console.log('🎮 Initializing Gamification UI...');

        try {
            await this.loadPlayerData();
            this.renderUI();
            this.setupEventListeners();

            if (this.config.autoRefresh) {
                this.startAutoRefresh();
            }

            // Initialize real-time WebSocket connection
            if (this.realtimeEnabled) {
                await this.initializeWebSocket();
            }

            // Load quests data
            await this.loadActiveQuests();
            await this.loadAvailableQuests();

            // Load social data
            await this.loadSocialData();

            // Load analytics data
            await this.loadAnalyticsData();

            console.log('✅ Gamification UI initialized with real-time support, quest system, social features, and analytics');
        } catch (error) {
            console.error('❌ Failed to initialize Gamification UI:', error);
            throw error;
        }
    }
    
    /**
     * Load player data from backend
     */
    async loadPlayerData() {
        try {
            const response = await fetch('/api/gaming/player/status');
            const data = await response.json();

            this.state.currentXP = data.current_xp || 0;
            this.state.currentLevel = data.level || 1;
            this.state.totalXP = data.total_xp || 0;
            this.state.skills = data.skills || [];
            this.state.activeQuests = data.active_quests || [];
            this.state.completedQuests = data.completed_quests || [];
            this.state.achievements = data.achievements || [];

        } catch (error) {
            console.warn('⚠️ Failed to load player data:', error);
        }
    }

    /**
     * Initialize WebSocket connection for real-time updates
     */
    async initializeWebSocket() {
        try {
            // Initialize Socket.IO connection
            if (typeof io !== 'undefined') {
                this.socket = io('/gamification');

                this.socket.on('connect', () => {
                    console.log('🔌 Connected to gamification real-time updates');
                    this.showConnectionStatus('connected');
                });

                this.socket.on('disconnect', () => {
                    console.log('🔌 Disconnected from gamification real-time updates');
                    this.showConnectionStatus('disconnected');
                });

                this.socket.on('leaderboard_update', (data) => {
                    console.log('📊 Real-time leaderboard update received:', data);
                    this.handleRealtimeLeaderboardUpdate(data);
                });

                this.socket.on('connect_error', (error) => {
                    console.error('❌ WebSocket connection error:', error);
                    this.showConnectionStatus('error');
                    // Fallback to polling if WebSocket fails
                    this.startAutoRefresh();
                });

            } else {
                console.warn('⚠️ Socket.IO not available, falling back to polling');
                this.realtimeEnabled = false;
            }

        } catch (error) {
            console.error('❌ Failed to initialize WebSocket:', error);
            this.realtimeEnabled = false;
        }
    }

    /**
     * Handle real-time leaderboard updates
     */
    handleRealtimeLeaderboardUpdate(data) {
        try {
            const { leaderboard, timestamp, agent_count, initial, forced } = data;

            // Update leaderboard display
            this.updateLeaderboardDisplay(leaderboard);

            // Show update notification
            this.showUpdateNotification(initial, forced, agent_count);

            console.log(`📊 Leaderboard updated: ${agent_count} agents, ${initial ? 'initial' : 'live'} update`);

        } catch (error) {
            console.error('❌ Error handling realtime leaderboard update:', error);
        }
    }

    /**
     * Update the leaderboard display with new data
     */
    updateLeaderboardDisplay(leaderboardData) {
        const leaderboardContainer = this.container.querySelector('.leaderboard-section');
        if (!leaderboardContainer) return;

        // Update or create leaderboard section
        let leaderboardList = leaderboardContainer.querySelector('.leaderboard-list');
        if (!leaderboardList) {
            leaderboardList = document.createElement('div');
            leaderboardList.className = 'leaderboard-list';
            leaderboardContainer.appendChild(leaderboardList);
        }

        leaderboardList.innerHTML = leaderboardData.map(entry => `
            <div class="leaderboard-entry rank-${entry.rank} ${entry.status.toLowerCase()}">
                <div class="rank">#${entry.rank}</div>
                <div class="agent-info">
                    <div class="agent-name">${entry.agent}</div>
                    <div class="agent-mission">${entry.mission}</div>
                    <div class="agent-phase">${entry.phase}</div>
                </div>
                <div class="stats">
                    <div class="points">${entry.points.toLocaleString()} pts</div>
                    <div class="level">Level ${entry.level}</div>
                </div>
                <div class="status-indicator ${entry.status.toLowerCase()}">${entry.status}</div>
            </div>
        `).join('');
    }

    /**
     * Show connection status indicator
     */
    showConnectionStatus(status) {
        let statusIndicator = this.container.querySelector('.realtime-status');
        if (!statusIndicator) {
            statusIndicator = document.createElement('div');
            statusIndicator.className = 'realtime-status';
            this.container.querySelector('.gamification-header').appendChild(statusIndicator);
        }

        const statusConfig = {
            connected: { text: '🔴 LIVE', class: 'connected' },
            disconnected: { text: '⚫ OFFLINE', class: 'disconnected' },
            error: { text: '❌ ERROR', class: 'error' }
        };

        const config = statusConfig[status] || statusConfig.disconnected;
        statusIndicator.textContent = config.text;
        statusIndicator.className = `realtime-status ${config.class}`;
    }

    /**
     * Show update notification
     */
    showUpdateNotification(initial, forced, agentCount) {
        const notification = document.createElement('div');
        notification.className = 'update-notification';
        notification.textContent = initial
            ? `📊 Leaderboard loaded (${agentCount} agents)`
            : forced
                ? `🔄 Leaderboard updated (${agentCount} agents)`
                : `⚡ Live update (${agentCount} agents)`;

        this.container.appendChild(notification);

        // Auto-remove after 3 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 3000);
    }

    /**
     * Request manual leaderboard update
     */
    requestLeaderboardUpdate() {
        if (this.socket && this.socket.connected) {
            console.log('📡 Requesting manual leaderboard update');
            this.socket.emit('request_leaderboard_update');
        } else {
            // Fallback to API call
            this.forceLeaderboardUpdate();
        }
    }

    /**
     * Force leaderboard update via API
     */
    async forceLeaderboardUpdate() {
        try {
            const response = await fetch('/api/gaming/leaderboard/force-update', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });

            if (response.ok) {
                console.log('✅ Forced leaderboard update requested');
            } else {
                console.error('❌ Failed to force leaderboard update');
            }
        } catch (error) {
            console.error('❌ Error forcing leaderboard update:', error);
        }
    }
    
    /**
     * Render complete UI
     */
    renderUI() {
        if (!this.container) return;
        
        this.container.innerHTML = `
            <div class="gamification-dashboard ${this.config.theme}">
                <div class="gamification-header">
                    <h2>🎮 Agent Progress</h2>
                </div>
                
                <div class="gamification-content">
                    ${this.renderXPSection()}
                    ${this.renderLeaderboardSection()}
                    ${this.renderSocialSection()}
                    ${this.renderAnalyticsSection()}
                    ${this.renderActiveQuestsSection()}
                    ${this.renderSkillsSection()}
                    ${this.renderQuestsSection()}
                    ${this.renderAchievementsSection()}
                </div>
            </div>
        `;
        
        if (this.config.enableAnimations) {
            this.addAnimations();
        }
    }
    
    /**
     * Render Active Quests section
     */
    renderActiveQuestsSection() {
        return `
            <div class="active-quests-section card">
                <div class="section-header">
                    <h3>🎯 Active Quests</h3>
                    <button class="refresh-btn" onclick="window.gamificationUI?.loadActiveQuests()">
                        🔄 Refresh
                    </button>
                </div>
                <div class="quests-loading">
                    <div class="loading-spinner"></div>
                    <span>Loading active quests...</span>
                </div>
            </div>
        `;
    }

    /**
     * Render Available Quests section
     */
    renderAvailableQuestsSection() {
        return `
            <div class="available-quests-section card">
                <div class="section-header">
                    <h3>📋 Available Quests</h3>
                    <button class="refresh-btn" onclick="window.gamificationUI?.loadAvailableQuests()">
                        🔄 Load New Quests
                    </button>
                </div>
                <div class="available-quests-loading">
                    <div class="loading-spinner"></div>
                    <span>Loading available quests...</span>
                </div>
            </div>
        `;
    }

    /**
     * Load available quests
     */
    async loadAvailableQuests() {
        try {
            const response = await fetch('/api/gaming/quests/Agent-6/available');
            const data = await response.json();

            this.updateAvailableQuestsDisplay(data.available_quests);
        } catch (error) {
            console.error('❌ Error loading available quests:', error);
        }
    }

    /**
     * Update the available quests display
     */
    updateAvailableQuestsDisplay(quests) {
        const questsContainer = this.container.querySelector('.available-quests-section');
        if (!questsContainer) return;

        let questsList = questsContainer.querySelector('.available-quests-list');
        if (!questsList) {
            questsList = document.createElement('div');
            questsList.className = 'available-quests-list';
            questsContainer.appendChild(questsList);
        }

        if (quests.length === 0) {
            questsList.innerHTML = '<div class="no-quests">No quests available at this time.</div>';
            return;
        }

        questsList.innerHTML = quests.map(quest => `
            <div class="available-quest-card ${quest.difficulty}">
                <div class="quest-header">
                    <h4>${quest.title}</h4>
                    <div class="quest-badges">
                        <span class="badge type-${quest.quest_type}">${quest.quest_type}</span>
                        <span class="badge difficulty-${quest.difficulty}">${quest.difficulty}</span>
                    </div>
                </div>
                <div class="quest-description">${quest.description}</div>
                <div class="quest-rewards-preview">
                    <div class="reward-item">🎖️ ${quest.rewards.xp_reward} XP</div>
                    ${quest.rewards.achievements.length > 0 ?
                        `<div class="reward-item">🏆 Achievement</div>` : ''}
                </div>
                <button class="accept-quest-btn" onclick="window.gamificationUI?.acceptQuest('${quest.quest_id}')">
                    ✅ Accept Quest
                </button>
            </div>
        `).join('');
    }

    /**
     * Accept a quest (creates it for the agent)
     */
    async acceptQuest(questId) {
        try {
            const response = await fetch(`/api/gaming/quests/Agent-6/create?type=collaboration&difficulty=medium`, {
                method: 'POST'
            });

            if (response.ok) {
                const data = await response.json();
                console.log(`✅ Quest accepted: ${data.quest.title}`);
                this.loadActiveQuests(); // Refresh active quests
                this.loadAvailableQuests(); // Refresh available quests
                this.showNotification(`Quest "${data.quest.title}" accepted!`, 'success');
            } else {
                console.error('❌ Failed to accept quest');
                this.showNotification('Failed to accept quest', 'error');
            }
        } catch (error) {
            console.error('❌ Error accepting quest:', error);
            this.showNotification('Error accepting quest', 'error');
        }
    }

    /**
     * Render Social section
     */
    renderSocialSection() {
        return `
            <div class="social-section card">
                <div class="section-header">
                    <h3>🤝 Agent Social Network</h3>
                    <button class="refresh-btn" onclick="window.gamificationUI?.loadSocialData()">
                        🔄 Refresh
                    </button>
                </div>
                <div class="social-content">
                    <div class="social-stats">
                        <div class="social-loading">
                            <div class="loading-spinner"></div>
                            <span>Loading social data...</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    /**
     * Load social data for current agent
     */
    async loadSocialData() {
        try {
            const [profileResponse, leaderboardResponse] = await Promise.all([
                fetch('/api/gaming/social/profile/Agent-6'),
                fetch('/api/gaming/social/leaderboard?limit=5')
            ]);

            const profileData = await profileResponse.json();
            const leaderboardData = await leaderboardResponse.json();

            this.updateSocialDisplay(profileData, leaderboardData);
        } catch (error) {
            console.error('❌ Error loading social data:', error);
        }
    }

    /**
     * Update social section display
     */
    updateSocialDisplay(profileData, leaderboardData) {
        const socialSection = this.container.querySelector('.social-section .social-content');
        if (!socialSection) return;

        const profile = profileData.profile;
        const leaderboard = leaderboardData.leaderboard;

        socialSection.innerHTML = `
            <div class="social-stats">
                <div class="stat-item">
                    <span class="stat-label">Social Score</span>
                    <span class="stat-value">${Math.round(profile.social_score)}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Reputation</span>
                    <span class="stat-value">${Math.round(profile.reputation_score)}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Relationships</span>
                    <span class="stat-value">${profileData.active_relationships}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Interactions</span>
                    <span class="stat-value">${profileData.total_interactions}</span>
                </div>
            </div>

            <div class="social-achievements">
                <h4>🏆 Social Achievements</h4>
                <div class="achievements-list">
                    ${profile.social_achievements.length > 0
                        ? profile.social_achievements.map(achievement =>
                            `<span class="achievement-badge">${achievement.replace('_', ' ')}</span>`
                          ).join('')
                        : '<span class="no-achievements">No achievements yet</span>'
                    }
                </div>
            </div>

            <div class="social-leaderboard">
                <h4>🌟 Social Leaders</h4>
                <div class="social-leaderboard-list">
                    ${leaderboard.map((agent, index) => `
                        <div class="social-leaderboard-entry ${agent.agent_id === 'Agent-6' ? 'current-agent' : ''}">
                            <span class="rank">#${index + 1}</span>
                            <span class="agent-name">${agent.agent_id}</span>
                            <span class="social-score">${Math.round(agent.social_score)}</span>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }

    /**
     * Record a social interaction
     */
    async recordSocialInteraction(toAgent, interactionType, context, impactScore = 0.5) {
        try {
            const response = await fetch('/api/gaming/social/interaction', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    from_agent: 'Agent-6',
                    to_agent: toAgent,
                    interaction_type: interactionType,
                    context: context,
                    impact_score: impactScore
                })
            });

            if (response.ok) {
                console.log(`✅ Social interaction recorded with ${toAgent}`);
                this.loadSocialData(); // Refresh social data
                this.showNotification('Social interaction recorded!', 'success');
            } else {
                console.error('❌ Failed to record social interaction');
                this.showNotification('Failed to record interaction', 'error');
            }
        } catch (error) {
            console.error('❌ Error recording social interaction:', error);
            this.showNotification('Error recording interaction', 'error');
        }
    }

    /**
     * Render Analytics section
     */
    renderAnalyticsSection() {
        return `
            <div class="analytics-section card">
                <div class="section-header">
                    <h3>📊 Performance Analytics</h3>
                    <button class="refresh-btn" onclick="window.gamificationUI?.loadAnalyticsData()">
                        🔄 Refresh
                    </button>
                </div>
                <div class="analytics-content">
                    <div class="analytics-loading">
                        <div class="loading-spinner"></div>
                        <span>Loading analytics...</span>
                    </div>
                </div>
            </div>
        `;
    }

    /**
     * Load analytics data
     */
    async loadAnalyticsData() {
        try {
            const [healthResponse, reportResponse] = await Promise.all([
                fetch('/api/gaming/analytics/health'),
                fetch('/api/gaming/analytics/report?hours=1')
            ]);

            const healthData = await healthResponse.json();
            const reportData = await reportResponse.json();

            this.updateAnalyticsDisplay(healthData, reportData);
        } catch (error) {
            console.error('❌ Error loading analytics data:', error);
        }
    }

    /**
     * Update analytics section display
     */
    updateAnalyticsDisplay(healthData, reportData) {
        const analyticsSection = this.container.querySelector('.analytics-section .analytics-content');
        if (!analyticsSection) return;

        const overallScore = healthData.overall_score || 0;
        const healthStatus = healthData.health_status || 'unknown';
        const components = healthData.components || {};
        const insights = reportData.insights || [];

        analyticsSection.innerHTML = `
            <div class="health-overview">
                <div class="health-score">
                    <div class="score-circle ${healthStatus}">
                        <span class="score-number">${overallScore}</span>
                        <span class="score-label">Health</span>
                    </div>
                    <div class="health-status ${healthStatus}">
                        ${healthStatus.toUpperCase()}
                    </div>
                </div>

                <div class="health-components">
                    ${Object.entries(components).map(([metric, data]) => `
                        <div class="component-metric ${data.assessment || 'unknown'}">
                            <div class="metric-name">${metric.replace('_', ' ')}</div>
                            <div class="metric-value">${data.current ? Math.round(data.current) : 'N/A'}</div>
                            <div class="metric-status">${data.assessment || 'unknown'}</div>
                        </div>
                    `).join('')}
                </div>
            </div>

            <div class="performance-insights">
                <h4>💡 Key Insights</h4>
                <div class="insights-list">
                    ${insights.length > 0
                        ? insights.map(insight => `<div class="insight-item">${insight}</div>`).join('')
                        : '<div class="no-insights">No insights available</div>'
                    }
                </div>
            </div>

            <div class="performance-metrics">
                <h4>📈 Recent Metrics</h4>
                <div class="metrics-grid">
                    ${this.renderKeyMetrics(reportData.metrics_summary || {})}
                </div>
            </div>
        `;
    }

    /**
     * Render key performance metrics
     */
    renderKeyMetrics(metricsSummary) {
        const keyMetrics = ['response_time', 'engagement_rate', 'completion_rate', 'social_interaction_rate'];

        return keyMetrics.map(metric => {
            const data = metricsSummary[metric];
            if (!data || data.status === 'no_data') {
                return `
                    <div class="metric-card">
                        <div class="metric-title">${metric.replace('_', ' ')}</div>
                        <div class="metric-value">No Data</div>
                        <div class="metric-trend">—</div>
                    </div>
                `;
            }

            const value = data.current;
            const trend = data.trend || 'stable';
            const assessment = data.assessment || 'unknown';

            return `
                <div class="metric-card ${assessment}">
                    <div class="metric-title">${metric.replace('_', ' ')}</div>
                    <div class="metric-value">${typeof value === 'number' ? Math.round(value) : value}</div>
                    <div class="metric-trend ${trend}">
                        ${trend === 'increasing' ? '📈' : trend === 'decreasing' ? '📉' : '➡️'} ${trend}
                    </div>
                    <div class="metric-status">${assessment}</div>
                </div>
            `;
        }).join('');
    }

    /**
     * Record a performance metric
     */
    async recordPerformanceMetric(metricName, value, metadata = {}) {
        try {
            const response = await fetch('/api/gaming/analytics/metrics', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    metric_name: metricName,
                    value: value,
                    metadata: metadata
                })
            });

            if (response.ok) {
                console.log(`✅ Performance metric recorded: ${metricName} = ${value}`);
            } else {
                console.error('❌ Failed to record performance metric');
            }
        } catch (error) {
            console.error('❌ Error recording performance metric:', error);
        }
    }

    /**
     * Render Leaderboard section
     */
    renderLeaderboardSection() {
        return `
            <div class="leaderboard-section card">
                <div class="section-header">
                    <h3>🏆 Agent Leaderboard</h3>
                    <button class="refresh-btn" onclick="window.gamificationUI?.requestLeaderboardUpdate()">
                        🔄 Refresh
                    </button>
                </div>
                <div class="leaderboard-loading">
                    <div class="loading-spinner"></div>
                    <span>Loading leaderboard...</span>
                </div>
            </div>
        `;
    }

    /**
     * Load active quests for the current agent
     */
    async loadActiveQuests() {
        try {
            const response = await fetch('/api/gaming/quests/Agent-6');
            const data = await response.json();

            this.updateActiveQuestsDisplay(data.quests);
        } catch (error) {
            console.error('❌ Error loading active quests:', error);
        }
    }

    /**
     * Update the active quests display
     */
    updateActiveQuestsDisplay(quests) {
        const questsContainer = this.container.querySelector('.active-quests-section');
        if (!questsContainer) return;

        let questsList = questsContainer.querySelector('.quests-list');
        if (!questsList) {
            questsList = document.createElement('div');
            questsList.className = 'quests-list';
            questsContainer.appendChild(questsList);
        }

        if (quests.length === 0) {
            questsList.innerHTML = '<div class="no-quests">No active quests. Check available quests below!</div>';
            return;
        }

        questsList.innerHTML = quests.map(quest => `
            <div class="quest-card ${quest.status} ${quest.difficulty}">
                <div class="quest-header">
                    <h4>${quest.title}</h4>
                    <div class="quest-badges">
                        <span class="badge type-${quest.quest_type}">${quest.quest_type}</span>
                        <span class="badge difficulty-${quest.difficulty}">${quest.difficulty}</span>
                        <span class="badge status-${quest.status}">${quest.status}</span>
                    </div>
                </div>
                <div class="quest-description">${quest.description}</div>
                <div class="quest-progress">
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${quest.progress_percentage}%"></div>
                    </div>
                    <span class="progress-text">${Math.round(quest.progress_percentage)}% Complete</span>
                </div>
                <div class="quest-objectives">
                    ${quest.objectives.map(obj => `
                        <div class="objective ${obj.completed ? 'completed' : 'pending'}">
                            <span class="objective-check">${obj.completed ? '✅' : '⏳'}</span>
                            <span class="objective-text">${obj.description}</span>
                            <span class="objective-progress">${obj.current_value}/${obj.target_value}</span>
                        </div>
                    `).join('')}
                </div>
                <div class="quest-rewards">
                    <div class="reward-item">🎖️ ${quest.rewards.xp_reward} XP</div>
                    ${quest.rewards.achievements.length > 0 ?
                        `<div class="reward-item">🏆 ${quest.rewards.achievements.join(', ')}</div>` : ''}
                </div>
                ${quest.status === 'available' ?
                    `<button class="start-quest-btn" onclick="window.gamificationUI?.startQuest('${quest.quest_id}')">
                        🚀 Start Quest
                    </button>` : ''}
            </div>
        `).join('');
    }

    /**
     * Start a quest
     */
    async startQuest(questId) {
        try {
            const response = await fetch(`/api/gaming/quests/${questId}/start`, {
                method: 'POST'
            });

            if (response.ok) {
                console.log(`✅ Quest ${questId} started`);
                this.loadActiveQuests(); // Refresh the display
                this.showNotification('Quest started successfully!', 'success');
            } else {
                console.error('❌ Failed to start quest');
                this.showNotification('Failed to start quest', 'error');
            }
        } catch (error) {
            console.error('❌ Error starting quest:', error);
            this.showNotification('Error starting quest', 'error');
        }
    }

    /**
     * Show notification
     */
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;

        this.container.appendChild(notification);

        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 3000);
    }

    /**
     * Render XP and Level section
     */
    renderXPSection() {
        const xpForNextLevel = this.calculateXPForNextLevel(this.state.currentLevel);
        const progress = (this.state.currentXP / xpForNextLevel) * 100;
        
        return `
            <div class="xp-section card">
                <div class="level-badge">
                    <span class="level-number">Level ${this.state.currentLevel}</span>
                </div>
                
                <div class="xp-info">
                    <div class="xp-text">
                        <span class="current-xp">${this.formatNumber(this.state.currentXP)}</span>
                        <span class="separator">/</span>
                        <span class="max-xp">${this.formatNumber(xpForNextLevel)}</span>
                        <span class="xp-label">XP</span>
                    </div>
                    
                    <div class="xp-bar-container">
                        <div class="xp-bar" style="width: ${progress}%">
                            <span class="xp-percentage">${Math.round(progress)}%</span>
                        </div>
                    </div>
                </div>
                
                <div class="total-xp">
                    Total XP: ${this.formatNumber(this.state.totalXP)}
                </div>
            </div>
        `;
    }
    
    /**
     * Render Skills section
     */
    renderSkillsSection() {
        const skillsHTML = this.state.skills.map(skill => `
            <div class="skill-item" data-skill="${skill.name}">
                <div class="skill-icon">${skill.icon || '⚡'}</div>
                <div class="skill-details">
                    <div class="skill-name">${skill.name}</div>
                    <div class="skill-level">Level ${skill.level}</div>
                    <div class="skill-progress-bar">
                        <div class="skill-progress" style="width: ${skill.progress}%"></div>
                    </div>
                </div>
                <div class="skill-points">+${skill.bonus}</div>
            </div>
        `).join('');
        
        return `
            <div class="skills-section card">
                <h3>⚡ Skills</h3>
                <div class="skills-grid">
                    ${skillsHTML || '<div class="no-skills">No skills unlocked yet</div>'}
                </div>
            </div>
        `;
    }
    
    /**
     * Render Quests section
     */
    renderQuestsSection() {
        const activeQuestsHTML = this.state.activeQuests.map(quest => `
            <div class="quest-item ${quest.priority}" data-quest-id="${quest.id}">
                <div class="quest-header">
                    <span class="quest-title">${quest.title}</span>
                    <span class="quest-reward">+${quest.xp_reward} XP</span>
                </div>
                <div class="quest-description">${quest.description}</div>
                <div class="quest-progress">
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${quest.progress}%"></div>
                    </div>
                    <span class="progress-text">${quest.progress}%</span>
                </div>
            </div>
        `).join('');
        
        return `
            <div class="quests-section card">
                <h3>📋 Active Quests</h3>
                <div class="quests-list">
                    ${activeQuestsHTML || '<div class="no-quests">No active quests</div>'}
                </div>
                <div class="completed-count">
                    ✅ Completed: ${this.state.completedQuests.length}
                </div>
            </div>
        `;
    }
    
    /**
     * Render Achievements section
     */
    renderAchievementsSection() {
        const achievementsHTML = this.state.achievements.slice(0, 5).map(achievement => `
            <div class="achievement-item ${achievement.unlocked ? 'unlocked' : 'locked'}">
                <div class="achievement-icon">${achievement.icon || '🏆'}</div>
                <div class="achievement-info">
                    <div class="achievement-name">${achievement.name}</div>
                    <div class="achievement-desc">${achievement.description}</div>
                </div>
            </div>
        `).join('');
        
        return `
            <div class="achievements-section card">
                <h3>🏆 Achievements</h3>
                <div class="achievements-grid">
                    ${achievementsHTML || '<div class="no-achievements">No achievements yet</div>'}
                </div>
                <div class="achievements-count">
                    ${this.state.achievements.filter(a => a.unlocked).length} / ${this.state.achievements.length}
                </div>
            </div>
        `;
    }
    
    /**
     * Setup event listeners
     */
    setupEventListeners() {
        // Quest click handlers
        this.container.querySelectorAll('.quest-item').forEach(item => {
            item.addEventListener('click', (e) => {
                const questId = e.currentTarget.dataset.questId;
                this.showQuestDetails(questId);
            });
        });
        
        // Skill hover handlers
        this.container.querySelectorAll('.skill-item').forEach(item => {
            item.addEventListener('mouseenter', (e) => {
                const skillName = e.currentTarget.dataset.skill;
                this.showSkillTooltip(skillName, e);
            });
        });
    }
    
    /**
     * Calculate XP required for next level
     */
    calculateXPForNextLevel(level) {
        // Formula: level * 100 + (level - 1) * 50
        return level * 100 + (level - 1) * 50;
    }
    
    /**
     * Format large numbers
     */
    formatNumber(num) {
        if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
        if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
        return num.toString();
    }
    
    /**
     * Add animations to elements
     */
    addAnimations() {
        this.container.querySelectorAll('.card').forEach((card, index) => {
            card.style.animation = `slideInUp 0.5s ease ${index * 0.1}s both`;
        });
        
        this.container.querySelectorAll('.xp-bar').forEach(bar => {
            bar.style.animation = 'fillProgress 1s ease-out';
        });
    }
    
    /**
     * Show quest details modal
     */
    showQuestDetails(questId) {
        const quest = this.state.activeQuests.find(q => q.id === questId);
        if (!quest) return;
        
        // Create modal overlay
        const modal = document.createElement('div');
        modal.className = 'quest-modal-overlay';
        modal.innerHTML = `
            <div class="quest-modal">
                <div class="quest-modal-header">
                    <h3>${quest.title}</h3>
                    <button class="quest-modal-close">&times;</button>
                </div>
                <div class="quest-modal-body">
                    <p class="quest-description">${quest.description}</p>
                    <div class="quest-progress">
                        <div class="quest-progress-bar" style="width: ${quest.progress}%"></div>
                    </div>
                    <p class="quest-progress-text">${quest.progress}% Complete</p>
                    <div class="quest-rewards">
                        <strong>Rewards:</strong> ${quest.rewards} XP
                    </div>
                </div>
            </div>
        `;
        
        // Add close handlers
        const closeBtn = modal.querySelector('.quest-modal-close');
        closeBtn.onclick = () => modal.remove();
        modal.onclick = (e) => { if (e.target === modal) modal.remove(); };
        
        document.body.appendChild(modal);
    }
    
    /**
     * Show skill tooltip
     */
    showSkillTooltip(skillName, event) {
        const skill = this.state.skills.find(s => s.name === skillName);
        if (!skill) return;
        
        // Remove existing tooltips
        const existing = document.querySelector('.skill-tooltip');
        if (existing) existing.remove();
        
        // Create tooltip
        const tooltip = document.createElement('div');
        tooltip.className = 'skill-tooltip';
        tooltip.innerHTML = `
            <div class="skill-tooltip-header">${skill.name}</div>
            <div class="skill-tooltip-body">
                <div class="skill-level">Level ${skill.level}</div>
                <div class="skill-xp">${skill.current_xp} / ${skill.required_xp} XP</div>
                <div class="skill-progress-bar">
                    <div class="skill-progress-fill" style="width: ${(skill.current_xp / skill.required_xp * 100)}%"></div>
                </div>
            </div>
        `;
        
        // Position near cursor
        tooltip.style.position = 'fixed';
        tooltip.style.left = `${event.clientX + 10}px`;
        tooltip.style.top = `${event.clientY + 10}px`;
        
        document.body.appendChild(tooltip);
        
        // Auto-remove after 3 seconds or on mouse leave
        setTimeout(() => tooltip.remove(), 3000);
        event.target.onmouseleave = () => tooltip.remove();
    }
    
    /**
     * Start auto-refresh timer
     */
    startAutoRefresh() {
        this.refreshTimer = setInterval(() => {
            this.refresh();
        }, this.config.refreshInterval);
    }
    
    /**
     * Refresh UI data
     */
    async refresh() {
        await this.loadPlayerData();
        this.renderUI();
        this.setupEventListeners();
    }
    
    /**
     * Cleanup
     */
    destroy() {
        if (this.refreshTimer) {
            clearInterval(this.refreshTimer);
        }
        if (this.container) {
            this.container.innerHTML = '';
        }
    }
}

// ================================
// FACTORY FUNCTION
// ================================

/**
 * Create gamification UI instance
 */
export function createGamificationUI(options) {
    return new GamificationUI(options);
}

// ================================
// INITIALIZATION
// ================================

/**
 * Initialize gamification UI on page load
 */
export async function initializeGamificationUI(containerId = 'gamificationContainer') {
    const container = document.getElementById(containerId);
    if (!container) {
        console.warn('⚠️ Gamification container not found');
        return null;
    }
    
    const ui = new GamificationUI({ container });
    await ui.initialize();
    return ui;
}



=======
<!-- SSOT Domain: gaming -->
/**
 * Gamification UI - Dream.OS Integration
 * XP, Skills, Quests, and Achievement System
 * 
 * V2 Compliance: Modern, responsive gamification interface
 * Author: Agent-7 - Repository Cloning Specialist
 * Version: 1.0.0 - C-084 Implementation
 * License: MIT
 */

// ================================
// GAMIFICATION UI SYSTEM
// ================================

/**
 * Main Gamification UI Controller
 */
export class GamificationUI {
    constructor(options = {}) {
        this.container = options.container || document.getElementById('gamificationContainer');
        this.config = {
            enableAnimations: options.enableAnimations !== false,
            autoRefresh: options.autoRefresh !== false,
            refreshInterval: options.refreshInterval || 30000,
            theme: options.theme || 'dark'
        };
        
        this.state = {
            currentXP: 0,
            currentLevel: 1,
            totalXP: 0,
            skills: [],
            activeQuests: [],
            completedQuests: [],
            achievements: []
        };
        
        this.refreshTimer = null;
    }
    
    /**
     * Initialize the gamification UI
     */
    async initialize() {
        console.log('🎮 Initializing Gamification UI...');
        
        try {
            await this.loadPlayerData();
            this.renderUI();
            this.setupEventListeners();
            
            if (this.config.autoRefresh) {
                this.startAutoRefresh();
            }
            
            console.log('✅ Gamification UI initialized');
        } catch (error) {
            console.error('❌ Failed to initialize Gamification UI:', error);
            throw error;
        }
    }
    
    /**
     * Load player data from backend
     */
    async loadPlayerData() {
        try {
            const response = await fetch('/api/gaming/player/status');
            const data = await response.json();
            
            this.state.currentXP = data.current_xp || 0;
            this.state.currentLevel = data.level || 1;
            this.state.totalXP = data.total_xp || 0;
            this.state.skills = data.skills || [];
            this.state.activeQuests = data.active_quests || [];
            this.state.completedQuests = data.completed_quests || [];
            this.state.achievements = data.achievements || [];
            
        } catch (error) {
            console.warn('⚠️ Failed to load player data:', error);
        }
    }
    
    /**
     * Render complete UI
     */
    renderUI() {
        if (!this.container) return;
        
        this.container.innerHTML = `
            <div class="gamification-dashboard ${this.config.theme}">
                <div class="gamification-header">
                    <h2>🎮 Agent Progress</h2>
                </div>
                
                <div class="gamification-content">
                    ${this.renderXPSection()}
                    ${this.renderSkillsSection()}
                    ${this.renderQuestsSection()}
                    ${this.renderAchievementsSection()}
                </div>
            </div>
        `;
        
        if (this.config.enableAnimations) {
            this.addAnimations();
        }
    }
    
    /**
     * Render XP and Level section
     */
    renderXPSection() {
        const xpForNextLevel = this.calculateXPForNextLevel(this.state.currentLevel);
        const progress = (this.state.currentXP / xpForNextLevel) * 100;
        
        return `
            <div class="xp-section card">
                <div class="level-badge">
                    <span class="level-number">Level ${this.state.currentLevel}</span>
                </div>
                
                <div class="xp-info">
                    <div class="xp-text">
                        <span class="current-xp">${this.formatNumber(this.state.currentXP)}</span>
                        <span class="separator">/</span>
                        <span class="max-xp">${this.formatNumber(xpForNextLevel)}</span>
                        <span class="xp-label">XP</span>
                    </div>
                    
                    <div class="xp-bar-container">
                        <div class="xp-bar" style="width: ${progress}%">
                            <span class="xp-percentage">${Math.round(progress)}%</span>
                        </div>
                    </div>
                </div>
                
                <div class="total-xp">
                    Total XP: ${this.formatNumber(this.state.totalXP)}
                </div>
            </div>
        `;
    }
    
    /**
     * Render Skills section
     */
    renderSkillsSection() {
        const skillsHTML = this.state.skills.map(skill => `
            <div class="skill-item" data-skill="${skill.name}">
                <div class="skill-icon">${skill.icon || '⚡'}</div>
                <div class="skill-details">
                    <div class="skill-name">${skill.name}</div>
                    <div class="skill-level">Level ${skill.level}</div>
                    <div class="skill-progress-bar">
                        <div class="skill-progress" style="width: ${skill.progress}%"></div>
                    </div>
                </div>
                <div class="skill-points">+${skill.bonus}</div>
            </div>
        `).join('');
        
        return `
            <div class="skills-section card">
                <h3>⚡ Skills</h3>
                <div class="skills-grid">
                    ${skillsHTML || '<div class="no-skills">No skills unlocked yet</div>'}
                </div>
            </div>
        `;
    }
    
    /**
     * Render Quests section
     */
    renderQuestsSection() {
        const activeQuestsHTML = this.state.activeQuests.map(quest => `
            <div class="quest-item ${quest.priority}" data-quest-id="${quest.id}">
                <div class="quest-header">
                    <span class="quest-title">${quest.title}</span>
                    <span class="quest-reward">+${quest.xp_reward} XP</span>
                </div>
                <div class="quest-description">${quest.description}</div>
                <div class="quest-progress">
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${quest.progress}%"></div>
                    </div>
                    <span class="progress-text">${quest.progress}%</span>
                </div>
            </div>
        `).join('');
        
        return `
            <div class="quests-section card">
                <h3>📋 Active Quests</h3>
                <div class="quests-list">
                    ${activeQuestsHTML || '<div class="no-quests">No active quests</div>'}
                </div>
                <div class="completed-count">
                    ✅ Completed: ${this.state.completedQuests.length}
                </div>
            </div>
        `;
    }
    
    /**
     * Render Achievements section
     */
    renderAchievementsSection() {
        const achievementsHTML = this.state.achievements.slice(0, 5).map(achievement => `
            <div class="achievement-item ${achievement.unlocked ? 'unlocked' : 'locked'}">
                <div class="achievement-icon">${achievement.icon || '🏆'}</div>
                <div class="achievement-info">
                    <div class="achievement-name">${achievement.name}</div>
                    <div class="achievement-desc">${achievement.description}</div>
                </div>
            </div>
        `).join('');
        
        return `
            <div class="achievements-section card">
                <h3>🏆 Achievements</h3>
                <div class="achievements-grid">
                    ${achievementsHTML || '<div class="no-achievements">No achievements yet</div>'}
                </div>
                <div class="achievements-count">
                    ${this.state.achievements.filter(a => a.unlocked).length} / ${this.state.achievements.length}
                </div>
            </div>
        `;
    }
    
    /**
     * Setup event listeners
     */
    setupEventListeners() {
        // Quest click handlers
        this.container.querySelectorAll('.quest-item').forEach(item => {
            item.addEventListener('click', (e) => {
                const questId = e.currentTarget.dataset.questId;
                this.showQuestDetails(questId);
            });
        });
        
        // Skill hover handlers
        this.container.querySelectorAll('.skill-item').forEach(item => {
            item.addEventListener('mouseenter', (e) => {
                const skillName = e.currentTarget.dataset.skill;
                this.showSkillTooltip(skillName, e);
            });
        });
    }
    
    /**
     * Calculate XP required for next level
     */
    calculateXPForNextLevel(level) {
        // Formula: level * 100 + (level - 1) * 50
        return level * 100 + (level - 1) * 50;
    }
    
    /**
     * Format large numbers
     */
    formatNumber(num) {
        if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
        if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
        return num.toString();
    }
    
    /**
     * Add animations to elements
     */
    addAnimations() {
        this.container.querySelectorAll('.card').forEach((card, index) => {
            card.style.animation = `slideInUp 0.5s ease ${index * 0.1}s both`;
        });
        
        this.container.querySelectorAll('.xp-bar').forEach(bar => {
            bar.style.animation = 'fillProgress 1s ease-out';
        });
    }
    
    /**
     * Show quest details modal
     */
    showQuestDetails(questId) {
        const quest = this.state.activeQuests.find(q => q.id === questId);
        if (!quest) return;
        
        // Create modal overlay
        const modal = document.createElement('div');
        modal.className = 'quest-modal-overlay';
        modal.innerHTML = `
            <div class="quest-modal">
                <div class="quest-modal-header">
                    <h3>${quest.title}</h3>
                    <button class="quest-modal-close">&times;</button>
                </div>
                <div class="quest-modal-body">
                    <p class="quest-description">${quest.description}</p>
                    <div class="quest-progress">
                        <div class="quest-progress-bar" style="width: ${quest.progress}%"></div>
                    </div>
                    <p class="quest-progress-text">${quest.progress}% Complete</p>
                    <div class="quest-rewards">
                        <strong>Rewards:</strong> ${quest.rewards} XP
                    </div>
                </div>
            </div>
        `;
        
        // Add close handlers
        const closeBtn = modal.querySelector('.quest-modal-close');
        closeBtn.onclick = () => modal.remove();
        modal.onclick = (e) => { if (e.target === modal) modal.remove(); };
        
        document.body.appendChild(modal);
    }
    
    /**
     * Show skill tooltip
     */
    showSkillTooltip(skillName, event) {
        const skill = this.state.skills.find(s => s.name === skillName);
        if (!skill) return;
        
        // Remove existing tooltips
        const existing = document.querySelector('.skill-tooltip');
        if (existing) existing.remove();
        
        // Create tooltip
        const tooltip = document.createElement('div');
        tooltip.className = 'skill-tooltip';
        tooltip.innerHTML = `
            <div class="skill-tooltip-header">${skill.name}</div>
            <div class="skill-tooltip-body">
                <div class="skill-level">Level ${skill.level}</div>
                <div class="skill-xp">${skill.current_xp} / ${skill.required_xp} XP</div>
                <div class="skill-progress-bar">
                    <div class="skill-progress-fill" style="width: ${(skill.current_xp / skill.required_xp * 100)}%"></div>
                </div>
            </div>
        `;
        
        // Position near cursor
        tooltip.style.position = 'fixed';
        tooltip.style.left = `${event.clientX + 10}px`;
        tooltip.style.top = `${event.clientY + 10}px`;
        
        document.body.appendChild(tooltip);
        
        // Auto-remove after 3 seconds or on mouse leave
        setTimeout(() => tooltip.remove(), 3000);
        event.target.onmouseleave = () => tooltip.remove();
    }
    
    /**
     * Start auto-refresh timer
     */
    startAutoRefresh() {
        this.refreshTimer = setInterval(() => {
            this.refresh();
        }, this.config.refreshInterval);
    }
    
    /**
     * Refresh UI data
     */
    async refresh() {
        await this.loadPlayerData();
        this.renderUI();
        this.setupEventListeners();
    }
    
    /**
     * Cleanup
     */
    destroy() {
        if (this.refreshTimer) {
            clearInterval(this.refreshTimer);
        }
        if (this.container) {
            this.container.innerHTML = '';
        }
    }
}

// ================================
// FACTORY FUNCTION
// ================================

/**
 * Create gamification UI instance
 */
export function createGamificationUI(options) {
    return new GamificationUI(options);
}

// ================================
// INITIALIZATION
// ================================

/**
 * Initialize gamification UI on page load
 */
export async function initializeGamificationUI(containerId = 'gamificationContainer') {
    const container = document.getElementById(containerId);
    if (!container) {
        console.warn('⚠️ Gamification container not found');
        return null;
    }
    
    const ui = new GamificationUI({ container });
    await ui.initialize();
    return ui;
}



>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
