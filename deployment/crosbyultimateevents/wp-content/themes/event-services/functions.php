<?php
/**
 * Event Services Theme Functions
 * Professional event planning and catering services theme
 */

// Enqueue theme styles and scripts
function event_services_enqueue_scripts() {
    wp_enqueue_style('event-services-style', get_stylesheet_uri(), array(), '1.0.0');
    wp_enqueue_script('event-services-js', get_template_directory_uri() . '/js/main.js', array('jquery'), '1.0.0', true);
}
add_action('wp_enqueue_scripts', 'event_services_enqueue_scripts');

// Add theme support
function event_services_theme_setup() {
    add_theme_support('post-thumbnails');
    add_theme_support('title-tag');
    add_theme_support('custom-logo');
    add_theme_support('html5', array('search-form', 'comment-form', 'comment-list'));
    add_theme_support('woocommerce'); // For catering services integration

    // Register navigation menus
    register_nav_menus(array(
        'primary' => __('Primary Menu', 'event-services'),
        'footer' => __('Footer Menu', 'event-services'),
    ));
}
add_action('after_setup_theme', 'event_services_theme_setup');

// Custom post types for events
function event_services_register_post_types() {
    register_post_type('event', array(
        'labels' => array(
            'name' => __('Events', 'event-services'),
            'singular_name' => __('Event', 'event-services'),
        ),
        'public' => true,
        'supports' => array('title', 'editor', 'thumbnail', 'custom-fields'),
        'menu_icon' => 'dashicons-calendar-alt',
    ));

    register_post_type('service', array(
        'labels' => array(
            'name' => __('Services', 'event-services'),
            'singular_name' => __('Service', 'event-services'),
        ),
        'public' => true,
        'supports' => array('title', 'editor', 'thumbnail', 'custom-fields'),
        'menu_icon' => 'dashicons-store',
    ));
}
add_action('init', 'event_services_register_post_types');

// Event Services shortcodes
function event_services_booking_form_shortcode() {
    ob_start();
    ?>
    <div class="booking-form">
        <h3><?php _e('Book Your Event', 'event-services'); ?></h3>
        <form id="event-booking-form">
            <div class="form-group">
                <label for="event-type"><?php _e('Event Type', 'event-services'); ?></label>
                <select id="event-type" name="event_type" required>
                    <option value=""><?php _e('Select Event Type', 'event-services'); ?></option>
                    <option value="wedding"><?php _e('Wedding', 'event-services'); ?></option>
                    <option value="corporate"><?php _e('Corporate Event', 'event-services'); ?></option>
                    <option value="birthday"><?php _e('Birthday Party', 'event-services'); ?></option>
                    <option value="graduation"><?php _e('Graduation', 'event-services'); ?></option>
                    <option value="other"><?php _e('Other', 'event-services'); ?></option>
                </select>
            </div>

            <div class="form-group">
                <label for="event-date"><?php _e('Event Date', 'event-services'); ?></label>
                <input type="date" id="event-date" name="event_date" required>
            </div>

            <div class="form-group">
                <label for="guest-count"><?php _e('Number of Guests', 'event-services'); ?></label>
                <input type="number" id="guest-count" name="guest_count" min="1" required>
            </div>

            <div class="form-group">
                <label for="contact-name"><?php _e('Contact Name', 'event-services'); ?></label>
                <input type="text" id="contact-name" name="contact_name" required>
            </div>

            <div class="form-group">
                <label for="contact-email"><?php _e('Email', 'event-services'); ?></label>
                <input type="email" id="contact-email" name="contact_email" required>
            </div>

            <div class="form-group">
                <label for="contact-phone"><?php _e('Phone', 'event-services'); ?></label>
                <input type="tel" id="contact-phone" name="contact_phone" required>
            </div>

            <div class="form-group">
                <label for="message"><?php _e('Additional Details', 'event-services'); ?></label>
                <textarea id="message" name="message" rows="4"></textarea>
            </div>

            <button type="submit" class="cta-button"><?php _e('Request Quote', 'event-services'); ?></button>
        </form>
    </div>
    <?php
    return ob_get_clean();
}
add_shortcode('event_booking_form', 'event_services_booking_form_shortcode');

// Catering services shortcode
function event_services_catering_menu_shortcode() {
    ob_start();
    ?>
    <div class="catering-menu">
        <h3><?php _e('Catering Services', 'event-services'); ?></h3>
        <div class="menu-categories">
            <div class="menu-category">
                <h4><?php _e('Appetizers', 'event-services'); ?></h4>
                <ul>
                    <li><?php _e('Stuffed Mushrooms', 'event-services'); ?> - $2.50 each</li>
                    <li><?php _e('Mini Quiches', 'event-services'); ?> - $3.00 each</li>
                    <li><?php _e('Shrimp Cocktail', 'event-services'); ?> - $4.00 each</li>
                </ul>
            </div>

            <div class="menu-category">
                <h4><?php _e('Main Courses', 'event-services'); ?></h4>
                <ul>
                    <li><?php _e('Grilled Salmon', 'event-services'); ?> - $45.00 per person</li>
                    <li><?php _e('Herb-Crusted Prime Rib', 'event-services'); ?> - $55.00 per person</li>
                    <li><?php _e('Chicken Marsala', 'event-services'); ?> - $35.00 per person</li>
                    <li><?php _e('Vegetarian Wellington', 'event-services'); ?> - $32.00 per person</li>
                </ul>
            </div>

            <div class="menu-category">
                <h4><?php _e('Desserts', 'event-services'); ?></h4>
                <ul>
                    <li><?php _e('Chocolate Mousse', 'event-services'); ?> - $6.00 each</li>
                    <li><?php _e('Tiramisu', 'event-services'); ?> - $7.00 each</li>
                    <li><?php _e('Fruit Tart', 'event-services'); ?> - $5.50 each</li>
                </ul>
            </div>
        </div>
    </div>
    <?php
    return ob_get_clean();
}
add_shortcode('catering_menu', 'event_services_catering_menu_shortcode');

// Testimonials shortcode
function event_services_testimonials_shortcode() {
    ob_start();
    $testimonials = get_posts(array(
        'post_type' => 'testimonial',
        'posts_per_page' => 3,
        'orderby' => 'rand'
    ));

    if ($testimonials) {
        echo '<div class="testimonials-grid">';
        foreach ($testimonials as $testimonial) {
            echo '<div class="testimonial-card">';
            echo '<div class="testimonial-content">' . get_the_content(null, false, $testimonial->ID) . '</div>';
            echo '<div class="testimonial-author">- ' . get_the_title($testimonial) . '</div>';
            echo '</div>';
        }
        echo '</div>';
    }
    return ob_get_clean();
}
add_shortcode('testimonials', 'event_services_testimonials_shortcode');

?>