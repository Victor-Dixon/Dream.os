<?php
/**
 * Credibility Integration - WordPress API Integration
 * ===================================================
 *
 * Integrates with Agent Cellphone V2 Credibility API to display dynamic
 * trust indicators, team information, and live statistics on About/Team pages.
 *
 * @package FreeRideInvestor
 * @author Agent-1 (Integration & Core Systems)
 * @date 2026-01-11
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

class CredibilityAPIIntegration {
    /** @var string API base URL */
    private $api_base_url;

    /** @var int Cache expiry in seconds */
    private $cache_expiry = 300; // 5 minutes

    public function __construct() {
        $this->api_base_url = get_theme_mod('credibility_api_url', 'http://localhost:8003');

        // Hook into WordPress
        add_action('wp_enqueue_scripts', array($this, 'enqueue_scripts'));
        add_shortcode('credibility_stats', array($this, 'render_stats_shortcode'));
        add_shortcode('credibility_team', array($this, 'render_team_shortcode'));
        add_shortcode('credibility_achievements', array($this, 'render_achievements_shortcode'));
        add_shortcode('credibility_trust_indicators', array($this, 'render_trust_indicators_shortcode'));
    }

    /**
     * Enqueue required scripts and styles
     */
    public function enqueue_scripts() {
        wp_enqueue_script(
            'credibility-api-integration',
            get_template_directory_uri() . '/js/credibility-integration.js',
            array('jquery'),
            '1.0.0',
            true
        );

        wp_localize_script('credibility-api-integration', 'credibilityAPI', array(
            'apiUrl' => $this->api_base_url,
            'nonce' => wp_create_nonce('credibility_api_nonce')
        ));

        wp_enqueue_style(
            'credibility-integration-styles',
            get_template_directory_uri() . '/css/credibility-integration.css',
            array(),
            '1.0.0'
        );
    }

    /**
     * Make API request with caching
     */
    private function api_request($endpoint) {
        $cache_key = 'credibility_api_' . md5($endpoint);
        $cached_data = get_transient($cache_key);

        if ($cached_data !== false) {
            return $cached_data;
        }

        $url = trailingslashit($this->api_base_url) . 'api/v1/' . $endpoint;

        $response = wp_remote_get($url, array(
            'timeout' => 10,
            'headers' => array(
                'Accept' => 'application/json',
                'User-Agent' => 'WordPress Credibility Integration/1.0'
            )
        ));

        if (is_wp_error($response)) {
            error_log('Credibility API Error: ' . $response->get_error_message());
            return null;
        }

        $body = wp_remote_retrieve_body($response);
        $data = json_decode($body, true);

        if (json_last_error() !== JSON_ERROR_NONE) {
            error_log('Credibility API JSON Error: ' . json_last_error_msg());
            return null;
        }

        // Cache for 5 minutes
        set_transient($cache_key, $data, $this->cache_expiry);

        return $data;
    }

    /**
     * Render live statistics shortcode
     */
    public function render_stats_shortcode($atts) {
        $atts = shortcode_atts(array(
            'show_users' => 'true',
            'show_projects' => 'true',
            'show_uptime' => 'true',
            'layout' => 'grid'
        ), $atts);

        $stats = $this->api_request('stats');

        if (!$stats) {
            return '<div class="credibility-error">Unable to load statistics</div>';
        }

        ob_start();
        ?>
        <div class="credibility-stats <?php echo esc_attr($atts['layout']); ?>">
            <?php if ($atts['show_users'] === 'true'): ?>
            <div class="stat-item">
                <div class="stat-number"><?php echo number_format($stats['total_users']); ?></div>
                <div class="stat-label">Active Users</div>
            </div>
            <?php endif; ?>

            <?php if ($atts['show_projects'] === 'true'): ?>
            <div class="stat-item">
                <div class="stat-number"><?php echo $stats['active_projects']; ?></div>
                <div class="stat-label">Active Projects</div>
            </div>
            <?php endif; ?>

            <?php if ($atts['show_uptime'] === 'true'): ?>
            <div class="stat-item">
                <div class="stat-number"><?php echo $stats['uptime_percentage']; ?>%</div>
                <div class="stat-label">Uptime</div>
            </div>
            <?php endif; ?>
        </div>
        <?php
        return ob_get_clean();
    }

    /**
     * Render team members shortcode
     */
    public function render_team_shortcode($atts) {
        $atts = shortcode_atts(array(
            'layout' => 'grid',
            'show_achievements' => 'true'
        ), $atts);

        $team = $this->api_request('team');

        if (!$team) {
            return '<div class="credibility-error">Unable to load team information</div>';
        }

        ob_start();
        ?>
        <div class="credibility-team <?php echo esc_attr($atts['layout']); ?>">
            <?php foreach ($team as $member): ?>
            <div class="team-member">
                <?php if (!empty($member['avatar_url'])): ?>
                <img src="<?php echo esc_url($member['avatar_url']); ?>" alt="<?php echo esc_attr($member['name']); ?>" class="team-avatar">
                <?php else: ?>
                <div class="team-avatar-placeholder">
                    <?php echo esc_html(substr($member['name'], 0, 1)); ?>
                </div>
                <?php endif; ?>

                <h3 class="team-name"><?php echo esc_html($member['name']); ?></h3>
                <div class="team-role"><?php echo esc_html($member['role']); ?></div>
                <div class="team-bio"><?php echo esc_html($member['bio']); ?></div>

                <?php if ($atts['show_achievements'] === 'true' && !empty($member['achievements'])): ?>
                <div class="team-achievements">
                    <h4>Key Achievements:</h4>
                    <ul>
                        <?php foreach ($member['achievements'] as $achievement): ?>
                        <li><?php echo esc_html($achievement); ?></li>
                        <?php endforeach; ?>
                    </ul>
                </div>
                <?php endif; ?>
            </div>
            <?php endforeach; ?>
        </div>
        <?php
        return ob_get_clean();
    }

    /**
     * Render achievements shortcode
     */
    public function render_achievements_shortcode($atts) {
        $atts = shortcode_atts(array(
            'limit' => 5,
            'category' => ''
        ), $atts);

        $achievements = $this->api_request('achievements');

        if (!$achievements) {
            return '<div class="credibility-error">Unable to load achievements</div>';
        }

        // Filter by category if specified
        if (!empty($atts['category'])) {
            $achievements = array_filter($achievements, function($achievement) use ($atts) {
                return $achievement['category'] === $atts['category'];
            });
        }

        // Limit results
        $achievements = array_slice($achievements, 0, intval($atts['limit']));

        ob_start();
        ?>
        <div class="credibility-achievements">
            <?php foreach ($achievements as $achievement): ?>
            <div class="achievement-item">
                <h4><?php echo esc_html($achievement['title']); ?></h4>
                <p><?php echo esc_html($achievement['description']); ?></p>
                <div class="achievement-meta">
                    <span class="achievement-date"><?php echo date('M j, Y', strtotime($achievement['date'])); ?></span>
                    <span class="achievement-category"><?php echo esc_html($achievement['category']); ?></span>
                </div>
            </div>
            <?php endforeach; ?>
        </div>
        <?php
        return ob_get_clean();
    }

    /**
     * Render trust indicators shortcode
     */
    public function render_trust_indicators_shortcode($atts) {
        $atts = shortcode_atts(array(
            'layout' => 'list'
        ), $atts);

        $indicators = $this->api_request('trust-indicators');

        if (!$indicators) {
            return '<div class="credibility-error">Unable to load trust indicators</div>';
        }

        ob_start();
        ?>
        <div class="credibility-trust-indicators <?php echo esc_attr($atts['layout']); ?>">
            <div class="trust-indicator <?php echo $indicators['security_certified'] ? 'active' : ''; ?>">
                <span class="indicator-icon">🔒</span>
                <span class="indicator-text">Security Certified</span>
            </div>

            <div class="trust-indicator <?php echo $indicators['data_encrypted'] ? 'active' : ''; ?>">
                <span class="indicator-icon">🛡️</span>
                <span class="indicator-text">Data Encrypted</span>
            </div>

            <div class="trust-indicator <?php echo $indicators['gdpr_compliant'] ? 'active' : ''; ?>">
                <span class="indicator-icon">📋</span>
                <span class="indicator-text">GDPR Compliant</span>
            </div>

            <div class="trust-indicator <?php echo $indicators['ssl_secured'] ? 'active' : ''; ?>">
                <span class="indicator-icon">🔐</span>
                <span class="indicator-text">SSL Secured</span>
            </div>

            <div class="trust-indicator">
                <span class="indicator-icon">⚡</span>
                <span class="indicator-text"><?php echo esc_html($indicators['uptime_guarantee']); ?> Uptime</span>
            </div>

            <div class="trust-indicator">
                <span class="indicator-icon">⏱️</span>
                <span class="indicator-text"><?php echo esc_html($indicators['support_response_time']); ?> Support</span>
            </div>
        </div>
        <?php
        return ob_get_clean();
    }
}

// Initialize the integration
new CredibilityAPIIntegration();

/**
 * Clear credibility API cache
 */
function credibility_clear_cache() {
    global $wpdb;

    // Clear all credibility-related transients
    $wpdb->query("DELETE FROM {$wpdb->options} WHERE option_name LIKE '_transient_credibility_api_%'");
    $wpdb->query("DELETE FROM {$wpdb->options} WHERE option_name LIKE '_transient_timeout_credibility_api_%'");
}
add_action('credibility_clear_cache', 'credibility_clear_cache');