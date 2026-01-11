/**
 * Credibility Integration JavaScript
 * ==================================
 * Dynamic loading and updating of credibility content from Agent Cellphone API
 */

(function($) {
    'use strict';

    class CredibilityIntegration {
        constructor() {
            this.apiUrl = credibilityAPI.apiUrl;
            this.nonce = credibilityAPI.nonce;
            this.cache = new Map();
            this.cacheExpiry = 5 * 60 * 1000; // 5 minutes

            this.init();
        }

        init() {
            this.bindEvents();
            this.loadDynamicContent();
            this.setupAutoRefresh();
        }

        bindEvents() {
            // Add loading states
            $(document).on('credibility:loading', (e, element) => {
                this.showLoading(element);
            });

            $(document).on('credibility:loaded', (e, element) => {
                this.hideLoading(element);
            });

            // Handle API errors
            $(document).on('credibility:error', (e, element, error) => {
                this.showError(element, error);
            });
        }

        async loadDynamicContent() {
            // Load stats with real-time updates
            $('.credibility-stats').each((i, element) => {
                this.loadStats($(element));
            });

            // Load team information
            $('.credibility-team').each((i, element) => {
                this.loadTeam($(element));
            });

            // Load achievements
            $('.credibility-achievements').each((i, element) => {
                this.loadAchievements($(element));
            });

            // Load trust indicators
            $('.credibility-trust-indicators').each((i, element) => {
                this.loadTrustIndicators($(element));
            });
        }

        async apiRequest(endpoint) {
            const cacheKey = endpoint;
            const cached = this.cache.get(cacheKey);

            if (cached && (Date.now() - cached.timestamp) < this.cacheExpiry) {
                return cached.data;
            }

            try {
                const response = await fetch(`${this.apiUrl}/api/v1/${endpoint}`, {
                    method: 'GET',
                    headers: {
                        'Accept': 'application/json',
                        'X-WP-Nonce': this.nonce
                    }
                });

                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }

                const data = await response.json();
                this.cache.set(cacheKey, { data, timestamp: Date.now() });

                return data;
            } catch (error) {
                console.error('Credibility API Error:', error);
                throw error;
            }
        }

        async loadStats($element) {
            $(document).trigger('credibility:loading', [$element]);

            try {
                const stats = await this.apiRequest('stats');

                $element.find('.stat-item').each((i, item) => {
                    const $item = $(item);

                    // Update user count
                    if ($item.find('.stat-label').text().includes('Users')) {
                        $item.find('.stat-number').text(this.formatNumber(stats.total_users));
                    }

                    // Update projects
                    if ($item.find('.stat-label').text().includes('Projects')) {
                        $item.find('.stat-number').text(stats.active_projects);
                    }

                    // Update uptime
                    if ($item.find('.stat-label').text().includes('Uptime')) {
                        $item.find('.stat-number').text(`${stats.uptime_percentage}%`);
                    }
                });

                $(document).trigger('credibility:loaded', [$element]);
            } catch (error) {
                $(document).trigger('credibility:error', [$element, error]);
            }
        }

        async loadTeam($element) {
            $(document).trigger('credibility:loading', [$element]);

            try {
                const team = await this.apiRequest('team');

                $element.empty(); // Clear existing content

                team.forEach(member => {
                    const memberHtml = `
                        <div class="team-member">
                            ${member.avatar_url ?
                                `<img src="${this.escapeHtml(member.avatar_url)}" alt="${this.escapeHtml(member.name)}" class="team-avatar">` :
                                `<div class="team-avatar-placeholder">${this.escapeHtml(member.name.charAt(0))}</div>`
                            }
                            <h3 class="team-name">${this.escapeHtml(member.name)}</h3>
                            <div class="team-role">${this.escapeHtml(member.role)}</div>
                            <div class="team-bio">${this.escapeHtml(member.bio)}</div>
                            ${member.achievements && member.achievements.length > 0 ? `
                                <div class="team-achievements">
                                    <h4>Key Achievements:</h4>
                                    <ul>
                                        ${member.achievements.map(achievement =>
                                            `<li>${this.escapeHtml(achievement)}</li>`
                                        ).join('')}
                                    </ul>
                                </div>
                            ` : ''}
                        </div>
                    `;
                    $element.append(memberHtml);
                });

                $(document).trigger('credibility:loaded', [$element]);
            } catch (error) {
                $(document).trigger('credibility:error', [$element, error]);
            }
        }

        async loadAchievements($element) {
            $(document).trigger('credibility:loading', [$element]);

            try {
                const achievements = await this.apiRequest('achievements');

                $element.empty();

                achievements.forEach(achievement => {
                    const achievementHtml = `
                        <div class="achievement-item">
                            <h4>${this.escapeHtml(achievement.title)}</h4>
                            <p>${this.escapeHtml(achievement.description)}</p>
                            <div class="achievement-meta">
                                <span class="achievement-date">${this.formatDate(achievement.date)}</span>
                                <span class="achievement-category">${this.escapeHtml(achievement.category)}</span>
                            </div>
                        </div>
                    `;
                    $element.append(achievementHtml);
                });

                $(document).trigger('credibility:loaded', [$element]);
            } catch (error) {
                $(document).trigger('credibility:error', [$element, error]);
            }
        }

        async loadTrustIndicators($element) {
            $(document).trigger('credibility:loading', [$element]);

            try {
                const indicators = await this.apiRequest('trust-indicators');

                // Update existing indicators with real data
                $element.find('.trust-indicator').each((i, indicator) => {
                    const $indicator = $(indicator);
                    const text = $indicator.find('.indicator-text').text();

                    if (text.includes('Uptime')) {
                        $indicator.find('.indicator-text').text(`${indicators.uptime_guarantee} Uptime`);
                    } else if (text.includes('Support')) {
                        $indicator.find('.indicator-text').text(`${indicators.support_response_time} Support`);
                    }

                    // Add/remove active class based on boolean values
                    const isActive = this.getIndicatorStatus(indicators, text);
                    $indicator.toggleClass('active', isActive);
                });

                $(document).trigger('credibility:loaded', [$element]);
            } catch (error) {
                $(document).trigger('credibility:error', [$element, error]);
            }
        }

        getIndicatorStatus(indicators, text) {
            if (text.includes('Security Certified')) return indicators.security_certified;
            if (text.includes('Data Encrypted')) return indicators.data_encrypted;
            if (text.includes('GDPR Compliant')) return indicators.gdpr_compliant;
            if (text.includes('SSL Secured')) return indicators.ssl_secured;
            return true; // Default for uptime/support indicators
        }

        setupAutoRefresh() {
            // Refresh stats every 5 minutes
            setInterval(() => {
                $('.credibility-stats').each((i, element) => {
                    this.loadStats($(element));
                });
            }, 5 * 60 * 1000);
        }

        showLoading($element) {
            $element.addClass('credibility-loading');
        }

        hideLoading($element) {
            $element.removeClass('credibility-loading');
        }

        showError($element, error) {
            this.hideLoading($element);
            const errorHtml = `<div class="credibility-error">Failed to load content: ${this.escapeHtml(error.message)}</div>`;
            $element.after(errorHtml);
        }

        formatNumber(num) {
            return new Intl.NumberFormat().format(num);
        }

        formatDate(dateString) {
            const date = new Date(dateString);
            return date.toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'short',
                day: 'numeric'
            });
        }

        escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
    }

    // Initialize when DOM is ready
    $(document).ready(() => {
        new CredibilityIntegration();
    });

})(jQuery);