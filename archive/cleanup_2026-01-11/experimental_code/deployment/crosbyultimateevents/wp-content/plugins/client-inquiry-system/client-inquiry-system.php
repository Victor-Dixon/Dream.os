<?php
/**
 * Plugin Name: Client Inquiry System
 * Plugin URI: https://crosbyultimateevents.com
 * Description: Professional client inquiry and lead management system
 * Version: 1.0.0
 * Author: Agent-3 Infrastructure & DevOps
 * License: GPL v2 or later
 * Text Domain: client-inquiry-system
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

class ClientInquirySystem {

    public function __construct() {
        add_action('init', array($this, 'register_inquiry_post_type'));
        add_action('init', array($this, 'register_inquiry_taxonomies'));
        add_action('wp_ajax_submit_inquiry', array($this, 'handle_inquiry_submission'));
        add_action('wp_ajax_nopriv_submit_inquiry', array($this, 'handle_inquiry_submission'));
        add_shortcode('inquiry_form', array($this, 'inquiry_form_shortcode'));
        add_action('admin_menu', array($this, 'add_admin_menu'));
        add_action('admin_enqueue_scripts', array($this, 'enqueue_admin_scripts'));
    }

    public function register_inquiry_post_type() {
        register_post_type('client_inquiry', array(
            'labels' => array(
                'name' => __('Client Inquiries', 'client-inquiry-system'),
                'singular_name' => __('Client Inquiry', 'client-inquiry-system'),
            ),
            'public' => false,
            'show_ui' => true,
            'supports' => array('title', 'editor', 'custom-fields'),
            'menu_icon' => 'dashicons-email-alt',
            'capabilities' => array(
                'create_posts' => false, // Only through form submissions
            ),
            'map_meta_cap' => true,
        ));
    }

    public function register_inquiry_taxonomies() {
        register_taxonomy('inquiry_status', 'client_inquiry', array(
            'labels' => array(
                'name' => __('Inquiry Status', 'client-inquiry-system'),
                'singular_name' => __('Inquiry Status', 'client-inquiry-system'),
            ),
            'hierarchical' => false,
            'show_admin_column' => true,
        ));

        register_taxonomy('inquiry_type', 'client_inquiry', array(
            'labels' => array(
                'name' => __('Inquiry Type', 'client-inquiry-system'),
                'singular_name' => __('Inquiry Type', 'client-inquiry-system'),
            ),
            'hierarchical' => false,
            'show_admin_column' => true,
        ));
    }

    public function inquiry_form_shortcode($atts) {
        $atts = shortcode_atts(array(
            'type' => 'general',
            'show_budget' => true,
            'show_timeline' => true,
        ), $atts, 'inquiry_form');

        wp_enqueue_script('jquery');

        ob_start();
        ?>
        <div class="client-inquiry-form">
            <form id="inquiry-form" method="post">
                <?php wp_nonce_field('submit_inquiry', 'inquiry_nonce'); ?>
                <input type="hidden" name="inquiry_type" value="<?php echo esc_attr($atts['type']); ?>">

                <div class="form-section">
                    <h4><?php _e('Contact Information', 'client-inquiry-system'); ?></h4>

                    <div class="form-row">
                        <div class="form-group">
                            <label for="first_name"><?php _e('First Name *', 'client-inquiry-system'); ?></label>
                            <input type="text" id="first_name" name="first_name" required>
                        </div>

                        <div class="form-group">
                            <label for="last_name"><?php _e('Last Name *', 'client-inquiry-system'); ?></label>
                            <input type="text" id="last_name" name="last_name" required>
                        </div>
                    </div>

                    <div class="form-row">
                        <div class="form-group">
                            <label for="email"><?php _e('Email *', 'client-inquiry-system'); ?></label>
                            <input type="email" id="email" name="email" required>
                        </div>

                        <div class="form-group">
                            <label for="phone"><?php _e('Phone *', 'client-inquiry-system'); ?></label>
                            <input type="tel" id="phone" name="phone" required>
                        </div>
                    </div>
                </div>

                <div class="form-section">
                    <h4><?php _e('Event Details', 'client-inquiry-system'); ?></h4>

                    <div class="form-group">
                        <label for="event_type"><?php _e('Event Type *', 'client-inquiry-system'); ?></label>
                        <select id="event_type" name="event_type" required>
                            <option value=""><?php _e('Select Event Type', 'client-inquiry-system'); ?></option>
                            <option value="wedding"><?php _e('Wedding', 'client-inquiry-system'); ?></option>
                            <option value="corporate"><?php _e('Corporate Event', 'client-inquiry-system'); ?></option>
                            <option value="birthday"><?php _e('Birthday Party', 'client-inquiry-system'); ?></option>
                            <option value="anniversary"><?php _e('Anniversary', 'client-inquiry-system'); ?></option>
                            <option value="graduation"><?php _e('Graduation', 'client-inquiry-system'); ?></option>
                            <option value="other"><?php _e('Other', 'client-inquiry-system'); ?></option>
                        </select>
                    </div>

                    <div class="form-row">
                        <div class="form-group">
                            <label for="event_date"><?php _e('Event Date', 'client-inquiry-system'); ?></label>
                            <input type="date" id="event_date" name="event_date">
                        </div>

                        <div class="form-group">
                            <label for="guest_count"><?php _e('Number of Guests', 'client-inquiry-system'); ?></label>
                            <input type="number" id="guest_count" name="guest_count" min="1">
                        </div>
                    </div>

                    <?php if ($atts['show_budget']): ?>
                    <div class="form-group">
                        <label for="budget_range"><?php _e('Budget Range', 'client-inquiry-system'); ?></label>
                        <select id="budget_range" name="budget_range">
                            <option value=""><?php _e('Select Budget Range', 'client-inquiry-system'); ?></option>
                            <option value="under_5000"><?php _e('Under $5,000', 'client-inquiry-system'); ?></option>
                            <option value="5000_10000"><?php _e('$5,000 - $10,000', 'client-inquiry-system'); ?></option>
                            <option value="10000_25000"><?php _e('$10,000 - $25,000', 'client-inquiry-system'); ?></option>
                            <option value="25000_50000"><?php _e('$25,000 - $50,000', 'client-inquiry-system'); ?></option>
                            <option value="over_50000"><?php _e('Over $50,000', 'client-inquiry-system'); ?></option>
                        </select>
                    </div>
                    <?php endif; ?>

                    <?php if ($atts['show_timeline']): ?>
                    <div class="form-group">
                        <label for="timeline"><?php _e('Planning Timeline', 'client-inquiry-system'); ?></label>
                        <select id="timeline" name="timeline">
                            <option value=""><?php _e('How soon are you planning?', 'client-inquiry-system'); ?></option>
                            <option value="asap"><?php _e('ASAP (within 1 month)', 'client-inquiry-system'); ?></option>
                            <option value="3_months"><?php _e('Within 3 months', 'client-inquiry-system'); ?></option>
                            <option value="6_months"><?php _e('Within 6 months', 'client-inquiry-system'); ?></option>
                            <option value="1_year"><?php _e('Within 1 year', 'client-inquiry-system'); ?></option>
                            <option value="planning"><?php _e('Just starting to plan', 'client-inquiry-system'); ?></option>
                        </select>
                    </div>
                    <?php endif; ?>

                    <div class="form-group">
                        <label for="event_details"><?php _e('Additional Details', 'client-inquiry-system'); ?></label>
                        <textarea id="event_details" name="event_details" rows="4" placeholder="<?php _e('Tell us about your vision, special requirements, or any questions you have...', 'client-inquiry-system'); ?>"></textarea>
                    </div>
                </div>

                <div class="form-section">
                    <div class="form-group">
                        <label>
                            <input type="checkbox" name="newsletter" value="1">
                            <?php _e('Subscribe to our newsletter for event planning tips and special offers', 'client-inquiry-system'); ?>
                        </label>
                    </div>
                </div>

                <div class="form-actions">
                    <button type="submit" class="submit-inquiry-btn">
                        <?php _e('Submit Inquiry', 'client-inquiry-system'); ?>
                    </button>
                    <div id="form-messages"></div>
                </div>
            </form>
        </div>

        <script>
        jQuery(document).ready(function($) {
            $('#inquiry-form').on('submit', function(e) {
                e.preventDefault();

                var formData = $(this).serialize();

                $.ajax({
                    url: '<?php echo admin_url('admin-ajax.php'); ?>',
                    type: 'POST',
                    data: formData + '&action=submit_inquiry',
                    beforeSend: function() {
                        $('.submit-inquiry-btn').prop('disabled', true).text('<?php _e('Submitting...', 'client-inquiry-system'); ?>');
                    },
                    success: function(response) {
                        if (response.success) {
                            $('#form-messages').html('<div class="success-message"><?php _e('Thank you! We\'ve received your inquiry and will contact you within 24 hours.', 'client-inquiry-system'); ?></div>');
                            $('#inquiry-form')[0].reset();
                        } else {
                            $('#form-messages').html('<div class="error-message">' + response.data + '</div>');
                        }
                    },
                    error: function() {
                        $('#form-messages').html('<div class="error-message"><?php _e('Sorry, there was an error submitting your inquiry. Please try again.', 'client-inquiry-system'); ?></div>');
                    },
                    complete: function() {
                        $('.submit-inquiry-btn').prop('disabled', false).text('<?php _e('Submit Inquiry', 'client-inquiry-system'); ?>');
                    }
                });
            });
        });
        </script>
        <?php
        return ob_get_clean();
    }

    public function handle_inquiry_submission() {
        // Verify nonce
        if (!wp_verify_nonce($_POST['inquiry_nonce'], 'submit_inquiry')) {
            wp_die(__('Security check failed', 'client-inquiry-system'));
        }

        // Sanitize and validate data
        $first_name = sanitize_text_field($_POST['first_name']);
        $last_name = sanitize_text_field($_POST['last_name']);
        $email = sanitize_email($_POST['email']);
        $phone = sanitize_text_field($_POST['phone']);
        $event_type = sanitize_text_field($_POST['event_type']);
        $event_date = sanitize_text_field($_POST['event_date']);
        $guest_count = intval($_POST['guest_count']);
        $budget_range = sanitize_text_field($_POST['budget_range']);
        $timeline = sanitize_text_field($_POST['timeline']);
        $event_details = sanitize_textarea_field($_POST['event_details']);
        $newsletter = isset($_POST['newsletter']) ? 1 : 0;

        // Create inquiry post
        $inquiry_data = array(
            'post_title' => sprintf('%s %s - %s Inquiry', $first_name, $last_name, ucfirst($event_type)),
            'post_content' => $event_details,
            'post_status' => 'publish',
            'post_type' => 'client_inquiry',
        );

        $inquiry_id = wp_insert_post($inquiry_data);

        if ($inquiry_id) {
            // Save meta data
            update_post_meta($inquiry_id, '_first_name', $first_name);
            update_post_meta($inquiry_id, '_last_name', $last_name);
            update_post_meta($inquiry_id, '_email', $email);
            update_post_meta($inquiry_id, '_phone', $phone);
            update_post_meta($inquiry_id, '_event_type', $event_type);
            update_post_meta($inquiry_id, '_event_date', $event_date);
            update_post_meta($inquiry_id, '_guest_count', $guest_count);
            update_post_meta($inquiry_id, '_budget_range', $budget_range);
            update_post_meta($inquiry_id, '_timeline', $timeline);
            update_post_meta($inquiry_id, '_newsletter', $newsletter);

            // Set taxonomies
            wp_set_object_terms($inquiry_id, 'new', 'inquiry_status');
            wp_set_object_terms($inquiry_id, $event_type, 'inquiry_type');

            // Send notification email
            $this->send_notification_email($inquiry_id);

            wp_send_json_success(__('Inquiry submitted successfully', 'client-inquiry-system'));
        } else {
            wp_send_json_error(__('Failed to submit inquiry', 'client-inquiry-system'));
        }
    }

    private function send_notification_email($inquiry_id) {
        $admin_email = get_option('admin_email');
        $site_name = get_bloginfo('name');

        $subject = sprintf('[%s] New Client Inquiry - %s', $site_name, get_the_title($inquiry_id));

        $message = sprintf(
            "New client inquiry received:\n\n%s\n\nView details: %s",
            get_post_field('post_content', $inquiry_id),
            admin_url('post.php?post=' . $inquiry_id . '&action=edit')
        );

        wp_mail($admin_email, $subject, $message);
    }

    public function add_admin_menu() {
        add_submenu_page(
            'edit.php?post_type=client_inquiry',
            __('Inquiry Settings', 'client-inquiry-system'),
            __('Settings', 'client-inquiry-system'),
            'manage_options',
            'inquiry-settings',
            array($this, 'settings_page')
        );
    }

    public function settings_page() {
        ?>
        <div class="wrap">
            <h1><?php _e('Client Inquiry System Settings', 'client-inquiry-system'); ?></h1>
            <form method="post" action="options.php">
                <?php
                settings_fields('inquiry_settings_group');
                do_settings_sections('inquiry-settings');
                submit_button();
                ?>
            </form>
        </div>
        <?php
    }

    public function enqueue_admin_scripts($hook) {
        if ($hook === 'edit.php' && isset($_GET['post_type']) && $_GET['post_type'] === 'client_inquiry') {
            wp_enqueue_style('inquiry-admin-css', plugins_url('admin/css/admin.css', __FILE__));
            wp_enqueue_script('inquiry-admin-js', plugins_url('admin/js/admin.js', __FILE__), array('jquery'));
        }
    }
}

new ClientInquirySystem();