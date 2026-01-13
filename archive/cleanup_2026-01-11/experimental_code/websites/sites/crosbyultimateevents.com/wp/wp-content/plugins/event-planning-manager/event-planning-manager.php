<?php
/**
 * Plugin Name: Event Planning Manager
 * Plugin URI: https://crosbyultimateevents.com
 * Description: Professional event planning management system for Crosby Ultimate Events
 * Version: 1.0.0
 * Author: Agent-3 Infrastructure & DevOps
 * License: GPL v2 or later
 * Text Domain: event-planning-manager
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

// Define plugin constants
define('EPM_VERSION', '1.0.0');
define('EPM_PLUGIN_DIR', plugin_dir_path(__FILE__));
define('EPM_PLUGIN_URL', plugin_dir_url(__FILE__));

/**
 * Main Event Planning Manager Class
 */
class EventPlanningManager {

    /**
     * Constructor
     */
    public function __construct() {
        $this->init();
        $this->setup_hooks();
    }

    /**
     * Initialize the plugin
     */
    private function init() {
        $this->load_dependencies();
        $this->define_admin_hooks();
        $this->define_public_hooks();
    }

    /**
     * Load plugin dependencies
     */
    private function load_dependencies() {
        require_once EPM_PLUGIN_DIR . 'includes/class-event-post-type.php';
        require_once EPM_PLUGIN_DIR . 'includes/class-event-admin.php';
        require_once EPM_PLUGIN_DIR . 'includes/class-event-calendar.php';
        require_once EPM_PLUGIN_DIR . 'includes/class-event-checklist.php';
    }

    /**
     * Setup WordPress hooks
     */
    private function setup_hooks() {
        register_activation_hook(__FILE__, array($this, 'activate'));
        register_deactivation_hook(__FILE__, array($this, 'deactivate'));

        add_action('plugins_loaded', array($this, 'load_textdomain'));
        add_action('init', array($this, 'register_post_types'));
        add_action('init', array($this, 'register_taxonomies'));
    }

    /**
     * Plugin activation
     */
    public function activate() {
        $this->create_database_tables();
        $this->set_default_options();
        flush_rewrite_rules();
    }

    /**
     * Plugin deactivation
     */
    public function deactivate() {
        flush_rewrite_rules();
    }

    /**
     * Load plugin textdomain
     */
    public function load_textdomain() {
        load_plugin_textdomain(
            'event-planning-manager',
            false,
            dirname(plugin_basename(__FILE__)) . '/languages/'
        );
    }

    /**
     * Register custom post types
     */
    public function register_post_types() {
        register_post_type('epm_event', array(
            'labels' => array(
                'name' => __('Events', 'event-planning-manager'),
                'singular_name' => __('Event', 'event-planning-manager'),
                'add_new' => __('Add New Event', 'event-planning-manager'),
                'add_new_item' => __('Add New Event', 'event-planning-manager'),
                'edit_item' => __('Edit Event', 'event-planning-manager'),
                'new_item' => __('New Event', 'event-planning-manager'),
                'view_item' => __('View Event', 'event-planning-manager'),
                'search_items' => __('Search Events', 'event-planning-manager'),
                'not_found' => __('No events found', 'event-planning-manager'),
                'not_found_in_trash' => __('No events found in trash', 'event-planning-manager'),
            ),
            'public' => true,
            'has_archive' => true,
            'supports' => array('title', 'editor', 'thumbnail', 'custom-fields', 'author'),
            'menu_icon' => 'dashicons-calendar-alt',
            'show_in_rest' => true,
        ));

        register_post_type('epm_client', array(
            'labels' => array(
                'name' => __('Clients', 'event-planning-manager'),
                'singular_name' => __('Client', 'event-planning-manager'),
                'add_new' => __('Add New Client', 'event-planning-manager'),
                'add_new_item' => __('Add New Client', 'event-planning-manager'),
            ),
            'public' => false,
            'show_ui' => true,
            'supports' => array('title', 'editor', 'custom-fields'),
            'menu_icon' => 'dashicons-businessperson',
            'show_in_rest' => true,
        ));
    }

    /**
     * Register taxonomies
     */
    public function register_taxonomies() {
        register_taxonomy('event_type', 'epm_event', array(
            'labels' => array(
                'name' => __('Event Types', 'event-planning-manager'),
                'singular_name' => __('Event Type', 'event-planning-manager'),
            ),
            'hierarchical' => true,
            'show_in_rest' => true,
        ));

        register_taxonomy('event_status', 'epm_event', array(
            'labels' => array(
                'name' => __('Event Status', 'event-planning-manager'),
                'singular_name' => __('Event Status', 'event-planning-manager'),
            ),
            'hierarchical' => false,
            'show_in_rest' => true,
        ));
    }

    /**
     * Create database tables
     */
    private function create_database_tables() {
        global $wpdb;

        $charset_collate = $wpdb->get_charset_collate();

        // Event timeline table
        $table_name = $wpdb->prefix . 'epm_event_timeline';
        $sql = "CREATE TABLE $table_name (
            id mediumint(9) NOT NULL AUTO_INCREMENT,
            event_id bigint(20) NOT NULL,
            timeline_date datetime DEFAULT CURRENT_TIMESTAMP,
            description text NOT NULL,
            status varchar(50) DEFAULT 'pending',
            assigned_to bigint(20),
            created_at datetime DEFAULT CURRENT_TIMESTAMP,
            updated_at datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            PRIMARY KEY (id),
            KEY event_id (event_id)
        ) $charset_collate;";

        require_once(ABSPATH . 'wp-admin/includes/upgrade.php');
        dbDelta($sql);

        // Event checklist table
        $table_name = $wpdb->prefix . 'epm_event_checklist';
        $sql = "CREATE TABLE $table_name (
            id mediumint(9) NOT NULL AUTO_INCREMENT,
            event_id bigint(20) NOT NULL,
            item_name varchar(255) NOT NULL,
            description text,
            is_completed boolean DEFAULT false,
            due_date datetime,
            assigned_to bigint(20),
            created_at datetime DEFAULT CURRENT_TIMESTAMP,
            updated_at datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            PRIMARY KEY (id),
            KEY event_id (event_id)
        ) $charset_collate;";

        dbDelta($sql);
    }

    /**
     * Set default options
     */
    private function set_default_options() {
        add_option('epm_default_event_status', 'planning');
        add_option('epm_enable_timeline', true);
        add_option('epm_enable_checklist', true);
        add_option('epm_notification_email', get_option('admin_email'));
    }

    /**
     * Define admin hooks
     */
    private function define_admin_hooks() {
        if (is_admin()) {
            add_action('admin_menu', array($this, 'add_admin_menu'));
            add_action('admin_enqueue_scripts', array($this, 'enqueue_admin_scripts'));
            add_action('add_meta_boxes', array($this, 'add_event_meta_boxes'));
            add_action('save_post', array($this, 'save_event_meta'));
        }
    }

    /**
     * Define public hooks
     */
    private function define_public_hooks() {
        add_action('wp_enqueue_scripts', array($this, 'enqueue_public_scripts'));
        add_shortcode('event_timeline', array($this, 'event_timeline_shortcode'));
        add_shortcode('event_checklist', array($this, 'event_checklist_shortcode'));
    }

    /**
     * Add admin menu
     */
    public function add_admin_menu() {
        add_menu_page(
            __('Event Planning', 'event-planning-manager'),
            __('Event Planning', 'event-planning-manager'),
            'manage_options',
            'event-planning-manager',
            array($this, 'admin_page'),
            'dashicons-calendar-alt',
            30
        );
    }

    /**
     * Admin page callback
     */
    public function admin_page() {
        include EPM_PLUGIN_DIR . 'admin/admin-page.php';
    }

    /**
     * Enqueue admin scripts
     */
    public function enqueue_admin_scripts($hook) {
        if (strpos($hook, 'event-planning-manager') !== false) {
            wp_enqueue_style('epm-admin-css', EPM_PLUGIN_URL . 'admin/css/admin.css', array(), EPM_VERSION);
            wp_enqueue_script('epm-admin-js', EPM_PLUGIN_URL . 'admin/js/admin.js', array('jquery'), EPM_VERSION, true);
        }
    }

    /**
     * Enqueue public scripts
     */
    public function enqueue_public_scripts() {
        wp_enqueue_style('epm-public-css', EPM_PLUGIN_URL . 'public/css/public.css', array(), EPM_VERSION);
        wp_enqueue_script('epm-public-js', EPM_PLUGIN_URL . 'public/js/public.js', array('jquery'), EPM_VERSION, true);
    }

    /**
     * Add event meta boxes
     */
    public function add_event_meta_boxes() {
        add_meta_box(
            'epm_event_details',
            __('Event Details', 'event-planning-manager'),
            array($this, 'event_details_meta_box'),
            'epm_event',
            'normal',
            'high'
        );

        add_meta_box(
            'epm_event_timeline',
            __('Event Timeline', 'event-planning-manager'),
            array($this, 'event_timeline_meta_box'),
            'epm_event',
            'normal',
            'default'
        );

        add_meta_box(
            'epm_event_checklist',
            __('Event Checklist', 'event-planning-manager'),
            array($this, 'event_checklist_meta_box'),
            'epm_event',
            'normal',
            'default'
        );
    }

    /**
     * Event details meta box
     */
    public function event_details_meta_box($post) {
        include EPM_PLUGIN_DIR . 'admin/partials/event-details-meta-box.php';
    }

    /**
     * Event timeline meta box
     */
    public function event_timeline_meta_box($post) {
        include EPM_PLUGIN_DIR . 'admin/partials/event-timeline-meta-box.php';
    }

    /**
     * Event checklist meta box
     */
    public function event_checklist_meta_box($post) {
        include EPM_PLUGIN_DIR . 'admin/partials/event-checklist-meta-box.php';
    }

    /**
     * Save event meta
     */
    public function save_event_meta($post_id) {
        if (!isset($_POST['epm_event_meta_nonce']) ||
            !wp_verify_nonce($_POST['epm_event_meta_nonce'], 'epm_save_event_meta')) {
            return;
        }

        if (!current_user_can('edit_post', $post_id)) {
            return;
        }

        // Save event details
        if (isset($_POST['epm_event_date'])) {
            update_post_meta($post_id, '_epm_event_date', sanitize_text_field($_POST['epm_event_date']));
        }

        if (isset($_POST['epm_guest_count'])) {
            update_post_meta($post_id, '_epm_guest_count', intval($_POST['epm_guest_count']));
        }

        if (isset($_POST['epm_budget'])) {
            update_post_meta($post_id, '_epm_budget', floatval($_POST['epm_budget']));
        }

        if (isset($_POST['epm_venue'])) {
            update_post_meta($post_id, '_epm_venue', sanitize_text_field($_POST['epm_venue']));
        }

        if (isset($_POST['epm_client_id'])) {
            update_post_meta($post_id, '_epm_client_id', intval($_POST['epm_client_id']));
        }
    }

    /**
     * Event timeline shortcode
     */
    public function event_timeline_shortcode($atts) {
        $atts = shortcode_atts(array(
            'event_id' => get_the_ID(),
        ), $atts);

        ob_start();
        include EPM_PLUGIN_DIR . 'public/partials/event-timeline.php';
        return ob_get_clean();
    }

    /**
     * Event checklist shortcode
     */
    public function event_checklist_shortcode($atts) {
        $atts = shortcode_atts(array(
            'event_id' => get_the_ID(),
        ), $atts);

        ob_start();
        include EPM_PLUGIN_DIR . 'public/partials/event-checklist.php';
        return ob_get_clean();
    }
}

// Initialize the plugin
function run_event_planning_manager() {
    new EventPlanningManager();
}
run_event_planning_manager();