<?php
/**
 * Front Page Template
 * Professional event planning and catering services homepage
 */
get_header();
?>

<main id="main" class="site-main">
    <!-- Hero Section -->
    <section class="hero-section">
        <div class="hero-content">
            <h1><?php _e('Professional Event Planning & Catering Services', 'event-services'); ?></h1>
            <p><?php _e('Creating unforgettable experiences with exceptional service and culinary excellence', 'event-services'); ?></p>
            <a href="#booking" class="cta-button"><?php _e('Plan Your Event', 'event-services'); ?></a>
        </div>
    </section>

    <!-- Services Section -->
    <section class="services-section">
        <div class="container">
            <h2><?php _e('Our Services', 'event-services'); ?></h2>
            <div class="services-grid">
                <div class="service-card">
                    <h3><?php _e('Event Planning', 'event-services'); ?></h3>
                    <p><?php _e('Full-service event coordination from concept to execution. We handle every detail so you can enjoy your special day.', 'event-services'); ?></p>
                    <ul>
                        <li><?php _e('Venue selection and negotiation', 'event-services'); ?></li>
                        <li><?php _e('Timeline and logistics management', 'event-services'); ?></li>
                        <li><?php _e('Vendor coordination', 'event-services'); ?></li>
                        <li><?php _e('On-site event management', 'event-services'); ?></li>
                    </ul>
                </div>

                <div class="service-card">
                    <h3><?php _e('Catering Services', 'event-services'); ?></h3>
                    <p><?php _e('Exceptional cuisine crafted for your event. From intimate gatherings to grand celebrations, we cater to all dietary needs.', 'event-services'); ?></p>
                    <ul>
                        <li><?php _e('Custom menu design', 'event-services'); ?></li>
                        <li><?php _e('Dietary accommodation', 'event-services'); ?></li>
                        <li><?php _e('Professional service staff', 'event-services'); ?></li>
                        <li><?php _e('Bar and beverage service', 'event-services'); ?></li>
                    </ul>
                </div>

                <div class="service-card">
                    <h3><?php _e('Wedding Services', 'event-services'); ?></h3>
                    <p><?php _e('Your dream wedding brought to life. We specialize in creating magical moments that last a lifetime.', 'event-services'); ?></p>
                    <ul>
                        <li><?php _e('Wedding planning and design', 'event-services'); ?></li>
                        <li><?php _e('Ceremony and reception coordination', 'event-services'); ?></li>
                        <li><?php _e('Vendor management', 'event-services'); ?></li>
                        <li><?php _e('Day-of coordination', 'event-services'); ?></li>
                    </ul>
                </div>

                <div class="service-card">
                    <h3><?php _e('Corporate Events', 'event-services'); ?></h3>
                    <p><?php _e('Professional events that impress. From conferences to team building, we deliver exceptional corporate experiences.', 'event-services'); ?></p>
                    <ul>
                        <li><?php _e('Conference and meeting planning', 'event-services'); ?></li>
                        <li><?php _e('Team building events', 'event-services'); ?></li>
                        <li><?php _e('Product launches', 'event-services'); ?></li>
                        <li><?php _e('Executive retreats', 'event-services'); ?></li>
                    </ul>
                </div>
            </div>
        </div>
    </section>

    <!-- Event Showcase -->
    <section class="event-showcase">
        <div class="container">
            <h2><?php _e('Recent Events', 'event-services'); ?></h2>
            <div class="events-grid">
                <?php
                $recent_events = get_posts(array(
                    'post_type' => 'event',
                    'posts_per_page' => 3,
                    'orderby' => 'date',
                    'order' => 'DESC'
                ));

                if ($recent_events) {
                    foreach ($recent_events as $event) {
                        echo '<div class="event-card">';
                        if (has_post_thumbnail($event->ID)) {
                            echo get_the_post_thumbnail($event->ID, 'medium');
                        }
                        echo '<h3>' . get_the_title($event) . '</h3>';
                        echo '<p>' . get_the_excerpt($event) . '</p>';
                        echo '<a href="' . get_permalink($event) . '" class="read-more">' . __('Learn More', 'event-services') . '</a>';
                        echo '</div>';
                    }
                } else {
                    // Default showcase content
                    echo '<div class="event-card">';
                    echo '<h3>' . __('Elegant Wedding Reception', 'event-services') . '</h3>';
                    echo '<p>' . __('A beautiful outdoor wedding with custom catering and professional coordination.', 'event-services') . '</p>';
                    echo '</div>';

                    echo '<div class="event-card">';
                    echo '<h3>' . __('Corporate Conference', 'event-services') . '</h3>';
                    echo '<p>' . __('Large-scale corporate event with full catering and audiovisual services.', 'event-services') . '</p>';
                    echo '</div>';

                    echo '<div class="event-card">';
                    echo '<h3>' . __('Birthday Celebration', 'event-services') . '</h3>';
                    echo '<p>' . __('Memorable birthday party with themed catering and entertainment.', 'event-services') . '</p>';
                    echo '</div>';
                }
                ?>
            </div>
        </div>
    </section>

    <!-- Testimonials -->
    <section class="testimonials">
        <div class="container">
            <h2><?php _e('What Our Clients Say', 'event-services'); ?></h2>
            <?php echo do_shortcode('[testimonials]'); ?>
        </div>
    </section>

    <!-- Booking Section -->
    <section id="booking" class="booking-section">
        <div class="container">
            <h2><?php _e('Ready to Plan Your Event?', 'event-services'); ?></h2>
            <?php echo do_shortcode('[event_booking_form]'); ?>
        </div>
    </section>

    <!-- Catering Menu Preview -->
    <section class="catering-preview">
        <div class="container">
            <h2><?php _e('Sample Catering Menu', 'event-services'); ?></h2>
            <?php echo do_shortcode('[catering_menu]'); ?>
            <div class="menu-cta">
                <p><?php _e('Contact us for a custom menu tailored to your event and dietary requirements.', 'event-services'); ?></p>
                <a href="#booking" class="cta-button"><?php _e('Get Custom Quote', 'event-services'); ?></a>
            </div>
        </div>
    </section>
</main>

<?php get_footer(); ?>