<?php
/**
 * Template Name: Services
 * Template Post Type: page
 *
 * The template for displaying services page
 *
 * @package FreeRideInvestor_V2
 */

get_header();
?>

<main id="primary" class="site-main">
    <div class="container">
        <div class="content-area">
            <div class="main-content">

                <?php while (have_posts()) : the_post(); ?>

                    <article id="post-<?php the_ID(); ?>" <?php post_class('services-page'); ?>>
                        <header class="entry-header">
                            <div class="hero-section">
                                <h1 class="entry-title"><?php the_title(); ?></h1>
                                <div class="hero-subtitle">
                                    <?php if (get_field('hero_subtitle')) : ?>
                                        <p><?php echo esc_html(get_field('hero_subtitle')); ?></p>
                                    <?php else : ?>
                                        <p>Professional trading strategies and risk management tools</p>
                                    <?php endif; ?>
                                </div>
                            </div>
                        </header>

                        <div class="entry-content">
                            <div class="services-content">

                                <!-- Services Grid -->
                                <section class="services-grid-section">
                                    <div class="services-grid">
                                        <div class="service-card">
                                            <div class="service-icon">📊</div>
                                            <h3>Trading Strategies</h3>
                                            <p>Access proven, backtested trading strategies across multiple asset classes including equities, options, and futures.</p>
                                            <a href="#" class="service-link">Learn More</a>
                                        </div>

                                        <div class="service-card">
                                            <div class="service-icon">⚡</div>
                                            <h3>Real-Time Alerts</h3>
                                            <p>Get instant notifications for trading opportunities, risk warnings, and market-moving events.</p>
                                            <a href="#" class="service-link">Learn More</a>
                                        </div>

                                        <div class="service-card">
                                            <div class="service-icon">📈</div>
                                            <h3>Performance Analytics</h3>
                                            <p>Track your trading performance with detailed analytics, risk metrics, and portfolio optimization tools.</p>
                                            <a href="#" class="service-link">Learn More</a>
                                        </div>

                                        <div class="service-card">
                                            <div class="service-icon">🔒</div>
                                            <h3>Risk Management</h3>
                                            <p>Advanced risk management tools including position sizing, stop-loss optimization, and portfolio diversification.</p>
                                            <a href="#" class="service-link">Learn More</a>
                                        </div>

                                        <div class="service-card">
                                            <div class="service-icon">📚</div>
                                            <h3>Educational Resources</h3>
                                            <p>Comprehensive trading education including video tutorials, webinars, and detailed strategy guides.</p>
                                            <a href="#" class="service-link">Learn More</a>
                                        </div>

                                        <div class="service-card">
                                            <div class="service-icon">🤝</div>
                                            <h3>Community Support</h3>
                                            <p>Join our active trading community for strategy discussions, market insights, and peer support.</p>
                                            <a href="#" class="service-link">Learn More</a>
                                        </div>
                                    </div>
                                </section>

                                <!-- Pricing Section -->
                                <section class="pricing-section">
                                    <h2>Choose Your Plan</h2>
                                    <div class="pricing-grid">
                                        <div class="pricing-card">
                                            <div class="pricing-header">
                                                <h3>Free</h3>
                                                <div class="price">$0<span>/month</span></div>
                                            </div>
                                            <ul class="pricing-features">
                                                <li>Basic market analysis</li>
                                                <li>Community access</li>
                                                <li>Educational content</li>
                                                <li>Email updates</li>
                                            </ul>
                                            <a href="#" class="btn-pricing">Get Started</a>
                                        </div>

                                        <div class="pricing-card featured">
                                            <div class="pricing-header">
                                                <h3>Pro</h3>
                                                <div class="price">$49<span>/month</span></div>
                                            </div>
                                            <ul class="pricing-features">
                                                <li>All Free features</li>
                                                <li>Advanced strategies</li>
                                                <li>Real-time alerts</li>
                                                <li>Performance analytics</li>
                                                <li>Risk management tools</li>
                                            </ul>
                                            <a href="#" class="btn-pricing featured">Start Pro Trial</a>
                                        </div>

                                        <div class="pricing-card">
                                            <div class="pricing-header">
                                                <h3>Enterprise</h3>
                                                <div class="price">$199<span>/month</span></div>
                                            </div>
                                            <ul class="pricing-features">
                                                <li>All Pro features</li>
                                                <li>Custom strategies</li>
                                                <li>API access</li>
                                                <li>White-label solutions</li>
                                                <li>Dedicated support</li>
                                            </ul>
                                            <a href="#" class="btn-pricing">Contact Sales</a>
                                        </div>
                                    </div>
                                </section>

                                <!-- Main Content -->
                                <div class="additional-content">
                                    <?php the_content(); ?>
                                </div>

                                <!-- FAQ Section -->
                                <section class="faq-section">
                                    <h2>Frequently Asked Questions</h2>
                                    <div class="faq-grid">
                                        <div class="faq-item">
                                            <h3>How do I get started?</h3>
                                            <p>Simply sign up for a free account and start exploring our basic market analysis tools. Upgrade to Pro for access to advanced strategies and real-time alerts.</p>
                                        </div>
                                        <div class="faq-item">
                                            <h3>Are your strategies guaranteed to make money?</h3>
                                            <p>No trading strategy can guarantee profits. All investments carry risk, and past performance does not guarantee future results. Our tools are designed to help you make informed decisions.</p>
                                        </div>
                                        <div class="faq-item">
                                            <h3>Do you provide customer support?</h3>
                                            <p>Yes, all paid subscribers receive priority email support. Enterprise customers also receive phone support and dedicated account management.</p>
                                        </div>
                                        <div class="faq-item">
                                            <h3>Can I cancel my subscription anytime?</h3>
                                            <p>Yes, you can cancel your subscription at any time. Pro subscriptions can be cancelled within 30 days for a full refund.</p>
                                        </div>
                                    </div>
                                </section>
                            </div>
                        </div>
                    </article>

                <?php endwhile; ?>

            </div>

            <?php get_sidebar(); ?>
        </div>
    </div>
</main>

<style>
.services-page .hero-section {
    text-align: center;
    padding: 4rem 0;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}

.services-page .hero-subtitle {
    font-size: 1.3rem;
    margin: 1rem 0 0 0;
    opacity: 0.9;
}

.services-content {
    display: grid;
    gap: 4rem;
}

.services-grid-section h2 {
    font-size: 2.2rem;
    color: #2c3e50;
    text-align: center;
    margin-bottom: 3rem;
}

.services-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 2rem;
}

.service-card {
    background: white;
    padding: 2.5rem;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    text-align: center;
    transition: transform 0.2s ease;
}

.service-card:hover {
    transform: translateY(-2px);
}

.service-icon {
    font-size: 3rem;
    margin-bottom: 1.5rem;
}

.service-card h3 {
    color: #2c3e50;
    font-size: 1.3rem;
    margin-bottom: 1rem;
}

.service-card p {
    color: #666;
    line-height: 1.6;
    margin-bottom: 1.5rem;
}

.service-link {
    color: #667eea;
    text-decoration: none;
    font-weight: 500;
}

.service-link:hover {
    text-decoration: underline;
}

.pricing-section h2 {
    font-size: 2.2rem;
    color: #2c3e50;
    text-align: center;
    margin-bottom: 3rem;
}

.pricing-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
}

.pricing-card {
    background: white;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    overflow: hidden;
    transition: transform 0.2s ease;
}

.pricing-card:hover {
    transform: translateY(-2px);
}

.pricing-card.featured {
    border: 3px solid #667eea;
    position: relative;
}

.pricing-card.featured::before {
    content: "Most Popular";
    position: absolute;
    top: -10px;
    left: 50%;
    transform: translateX(-50%);
    background: #667eea;
    color: white;
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 0.8rem;
    font-weight: 500;
}

.pricing-header {
    text-align: center;
    padding: 2rem;
    background: #f8f9fa;
}

.pricing-header h3 {
    font-size: 1.5rem;
    color: #2c3e50;
    margin-bottom: 0.5rem;
}

.price {
    font-size: 2.5rem;
    font-weight: bold;
    color: #667eea;
}

.price span {
    font-size: 1rem;
    color: #666;
}

.pricing-features {
    padding: 2rem;
    list-style: none;
    margin: 0;
}

.pricing-features li {
    padding: 0.5rem 0;
    border-bottom: 1px solid #eee;
    color: #666;
}

.pricing-features li:last-child {
    border-bottom: none;
}

.btn-pricing {
    display: block;
    text-align: center;
    padding: 1rem;
    background: #667eea;
    color: white;
    text-decoration: none;
    font-weight: 500;
    transition: background 0.2s ease;
}

.btn-pricing:hover {
    background: #5a67d8;
}

.btn-pricing.featured {
    background: #48bb78;
}

.btn-pricing.featured:hover {
    background: #38a169;
}

.faq-section h2 {
    font-size: 2.2rem;
    color: #2c3e50;
    text-align: center;
    margin-bottom: 3rem;
}

.faq-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
    gap: 2rem;
}

.faq-item {
    background: white;
    padding: 2rem;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}

.faq-item h3 {
    color: #2c3e50;
    font-size: 1.2rem;
    margin-bottom: 1rem;
}

.faq-item p {
    color: #666;
    line-height: 1.6;
}

@media (max-width: 768px) {
    .services-grid {
        grid-template-columns: 1fr;
    }

    .pricing-grid {
        grid-template-columns: 1fr;
    }

    .faq-grid {
        grid-template-columns: 1fr;
    }

    .services-page .hero-section {
        padding: 3rem 1rem;
    }

    .service-card, .pricing-card, .faq-item {
        margin: 0 1rem;
    }
}
</style>

<?php
get_footer();
?>