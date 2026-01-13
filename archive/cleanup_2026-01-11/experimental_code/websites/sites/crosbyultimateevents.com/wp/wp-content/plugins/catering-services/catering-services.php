<?php
/**
 * Plugin Name: Catering Services
 * Plugin URI: https://crosbyultimateevents.com
 * Description: Professional catering management system for event services
 * Version: 1.0.0
 * Author: Agent-3 Infrastructure & DevOps
 * License: GPL v2 or later
 * Text Domain: catering-services
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

class CateringServices {

    public function __construct() {
        add_action('init', array($this, 'register_menu_post_type'));
        add_action('init', array($this, 'register_dietary_taxonomy'));
        add_action('add_meta_boxes', array($this, 'add_menu_meta_boxes'));
        add_action('save_post', array($this, 'save_menu_meta'));
        add_shortcode('catering_menu', array($this, 'catering_menu_shortcode'));
        add_shortcode('catering_calculator', array($this, 'catering_calculator_shortcode'));
    }

    public function register_menu_post_type() {
        register_post_type('catering_menu', array(
            'labels' => array(
                'name' => __('Catering Menus', 'catering-services'),
                'singular_name' => __('Catering Menu', 'catering-services'),
            ),
            'public' => true,
            'supports' => array('title', 'editor', 'thumbnail'),
            'menu_icon' => 'dashicons-food',
        ));
    }

    public function register_dietary_taxonomy() {
        register_taxonomy('dietary_restriction', 'catering_menu', array(
            'labels' => array(
                'name' => __('Dietary Restrictions', 'catering-services'),
                'singular_name' => __('Dietary Restriction', 'catering-services'),
            ),
            'hierarchical' => false,
        ));
    }

    public function add_menu_meta_boxes() {
        add_meta_box('menu_items', __('Menu Items', 'catering-services'), array($this, 'menu_items_meta_box'), 'catering_menu');
        add_meta_box('pricing_info', __('Pricing Information', 'catering-services'), array($this, 'pricing_meta_box'), 'catering_menu');
    }

    public function menu_items_meta_box($post) {
        $menu_items = get_post_meta($post->ID, '_menu_items', true) ?: array();
        ?>
        <div id="menu-items-container">
            <?php foreach ($menu_items as $index => $item): ?>
                <div class="menu-item">
                    <input type="text" name="menu_items[<?php echo $index; ?>][name]" value="<?php echo esc_attr($item['name']); ?>" placeholder="Item name">
                    <input type="text" name="menu_items[<?php echo $index; ?>][description]" value="<?php echo esc_attr($item['description']); ?>" placeholder="Description">
                    <input type="number" step="0.01" name="menu_items[<?php echo $index; ?>][price]" value="<?php echo esc_attr($item['price']); ?>" placeholder="Price">
                    <button type="button" class="remove-item">Remove</button>
                </div>
            <?php endforeach; ?>
        </div>
        <button type="button" id="add-menu-item">Add Menu Item</button>
        <?php
    }

    public function pricing_meta_box($post) {
        $base_price = get_post_meta($post->ID, '_base_price', true);
        $price_per_person = get_post_meta($post->ID, '_price_per_person', true);
        ?>
        <p><label>Base Price: $<input type="number" step="0.01" name="base_price" value="<?php echo esc_attr($base_price); ?>"></label></p>
        <p><label>Price per Person: $<input type="number" step="0.01" name="price_per_person" value="<?php echo esc_attr($price_per_person); ?>"></label></p>
        <?php
    }

    public function save_menu_meta($post_id) {
        if (isset($_POST['menu_items'])) {
            update_post_meta($post_id, '_menu_items', $_POST['menu_items']);
        }
        if (isset($_POST['base_price'])) {
            update_post_meta($post_id, '_base_price', $_POST['base_price']);
        }
        if (isset($_POST['price_per_person'])) {
            update_post_meta($post_id, '_price_per_person', $_POST['price_per_person']);
        }
    }

    public function catering_menu_shortcode($atts) {
        $atts = shortcode_atts(array('menu' => ''), $atts);

        ob_start();

        if ($atts['menu']) {
            $menu = get_page_by_title($atts['menu'], OBJECT, 'catering_menu');
            if ($menu) {
                echo '<h3>' . esc_html($menu->post_title) . '</h3>';
                $menu_items = get_post_meta($menu->ID, '_menu_items', true);
                if ($menu_items) {
                    echo '<ul class="catering-menu-items">';
                    foreach ($menu_items as $item) {
                        echo '<li>';
                        echo '<strong>' . esc_html($item['name']) . '</strong>';
                        if ($item['description']) echo ' - ' . esc_html($item['description']);
                        if ($item['price']) echo ' ($' . esc_html($item['price']) . ')';
                        echo '</li>';
                    }
                    echo '</ul>';
                }
            }
        } else {
            // Default sample menu
            echo '<h3>Sample Catering Menu</h3>';
            echo '<div class="menu-categories">';
            echo '<div class="menu-category"><h4>Appetizers</h4><ul>';
            echo '<li>Stuffed Mushrooms - $2.50 each</li>';
            echo '<li>Mini Quiches - $3.00 each</li>';
            echo '</ul></div>';
            echo '<div class="menu-category"><h4>Main Courses</h4><ul>';
            echo '<li>Grilled Salmon - $45.00 per person</li>';
            echo '<li>Herb-Crusted Prime Rib - $55.00 per person</li>';
            echo '</ul></div>';
            echo '</div>';
        }

        return ob_get_clean();
    }

    public function catering_calculator_shortcode() {
        ob_start();
        ?>
        <div class="catering-calculator">
            <h4>Catering Cost Calculator</h4>
            <form id="catering-calc-form">
                <label>Number of Guests: <input type="number" id="guest-count" min="1" required></label>
                <label>Service Level:
                    <select id="service-level">
                        <option value="basic">Basic ($35/person)</option>
                        <option value="standard" selected>Standard ($45/person)</option>
                        <option value="premium">Premium ($65/person)</option>
                    </select>
                </label>
                <button type="submit">Calculate</button>
            </form>
            <div id="calculation-result" style="display:none;">
                <h5>Total Estimate: $<span id="total-cost">0</span></h5>
                <p>Includes food, service, and basic setup.</p>
            </div>
        </div>
        <script>
        jQuery(document).ready(function($) {
            $('#catering-calc-form').submit(function(e) {
                e.preventDefault();
                var guests = parseInt($('#guest-count').val());
                var level = $('#service-level').val();
                var rates = {basic: 35, standard: 45, premium: 65};
                var total = guests * rates[level];
                $('#total-cost').text(total.toLocaleString());
                $('#calculation-result').show();
            });
        });
        </script>
        <?php
        return ob_get_clean();
    }
}

new CateringServices();