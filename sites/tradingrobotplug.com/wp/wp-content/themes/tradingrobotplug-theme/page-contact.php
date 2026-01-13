<?php
/**
 * Contact Page Template
 * Low-friction contact form for trading platform
 * 
 * @package TradingRobotPlug
 * @version 2.0.0
 * @since 2025-12-26
 */

if (!defined('ABSPATH')) {
    exit;
}

get_header(); ?>

<div id="primary" class="content-area">
    <main id="main" class="site-main" role="main">
        <?php
        while (have_posts()) : the_post();
        ?>
        
        <article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
            <header class="entry-header">
                <h1 class="entry-title"><?php the_title(); ?></h1>
            </header>

            <div class="entry-content">
                <?php
                // Display page content
                the_content();
                ?>

                <!-- Low-Friction Contact Form - Tier 1 Quick Win WEB-04 -->
                <section class="contact-form-section" style="max-width: 600px; margin: 2rem auto;">
                    <?php
                    // Display success/error messages
                    if (isset($_GET['contact_success'])) {
                        echo '<div class="contact-message success" style="background: #d4edda; color: #155724; padding: 1rem; margin-bottom: 1rem; border-radius: 4px; border: 1px solid #c3e6cb;">Thank you! You\'ve been added to our waitlist. We\'ll notify you when our trading robots are ready.</div>';
                    }
                    if (isset($_GET['contact_error'])) {
                        $error_msg = isset($_GET['contact_error']) && $_GET['contact_error'] === 'invalid_email' ? 'Please enter a valid email address.' : 'An error occurred. Please try again.';
                        echo '<div class="contact-message error" style="background: #f8d7da; color: #721c24; padding: 1rem; margin-bottom: 1rem; border-radius: 4px; border: 1px solid #f5c6cb;">' . esc_html($error_msg) . '</div>';
                    }
                    ?>
                    <div class="subscription-form low-friction">
                        <p class="subscription-intro">Get started with our trading platform. Join our waitlist for early access.</p>
                        <form action="<?php echo esc_url(admin_url('admin-post.php')); ?>" method="POST" class="subscription-form-simple" aria-label="Contact Form">
                            <?php wp_nonce_field('contact_form', 'contact_nonce'); ?>
                            <input type="hidden" name="action" value="handle_contact_form">
                            <input
                                type="email"
                                name="email"
                                class="email-only-input"
                                placeholder="Enter your email address"
                                required
                                aria-label="Email address"
                            >
                            <button type="submit" class="cta-button primary">Get Started</button>
                        </form>
                        <p class="subscription-note">We'll notify you when our trading robots are ready and give you priority access.</p>
                        <div class="premium-upgrade-cta">
                            <p><strong>Ready to get started?</strong> Book a free consultation to discuss your trading needs.</p>
                            <a href="<?php echo esc_url('mailto:support@tradingrobotplug.com?subject=Consultation%20Request'); ?>" class="cta-button secondary">Schedule Consultation</a>
                        </div>
                    </div>
                </section>
            </div>
        </article>

        <?php
        endwhile;
        ?>
    </main>
</div>

<?php
get_footer();

