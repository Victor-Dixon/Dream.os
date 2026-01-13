<?php
/**
 * Template Name: Resources
 * Template Post Type: page
 *
 * The template for displaying resources page
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

                    <article id="post-<?php the_ID(); ?>" <?php post_class('resources-page'); ?>>
                        <header class="entry-header">
                            <div class="hero-section">
                                <h1 class="entry-title"><?php the_title(); ?></h1>
                                <div class="hero-subtitle">
                                    <?php if (get_field('hero_subtitle')) : ?>
                                        <p><?php echo esc_html(get_field('hero_subtitle')); ?></p>
                                    <?php else : ?>
                                        <p>Comprehensive trading education and market insights</p>
                                    <?php endif; ?>
                                </div>
                            </div>
                        </header>

                        <div class="entry-content">
                            <div class="resources-content">

                                <!-- Resource Categories -->
                                <section class="resource-categories-section">
                                    <div class="resource-categories">
                                        <div class="category-card" data-category="education">
                                            <div class="category-icon">📚</div>
                                            <h3>Educational Content</h3>
                                            <p>Learn trading fundamentals, technical analysis, and risk management strategies.</p>
                                        </div>

                                        <div class="category-card" data-category="tools">
                                            <div class="category-icon">🛠️</div>
                                            <h3>Trading Tools</h3>
                                            <p>Access calculators, screeners, and analysis tools to enhance your trading.</p>
                                        </div>

                                        <div class="category-card" data-category="market-analysis">
                                            <div class="category-icon">📊</div>
                                            <h3>Market Analysis</h3>
                                            <p>Get detailed market analysis, sector reports, and economic indicators.</p>
                                        </div>

                                        <div class="category-card" data-category="community">
                                            <div class="category-icon">🤝</div>
                                            <h3>Community Resources</h3>
                                            <p>Connect with other traders, share insights, and learn from the community.</p>
                                        </div>
                                    </div>
                                </section>

                                <!-- Featured Resources -->
                                <section class="featured-resources-section">
                                    <h2>Featured Resources</h2>
                                    <div class="featured-resources-grid">
                                        <div class="resource-card featured">
                                            <div class="resource-image">
                                                <img src="/wp-content/themes/freerideinvestor-v2/images/trading-guide.jpg" alt="Trading Guide" onerror="this.style.display='none'">
                                                <div class="resource-icon">📈</div>
                                            </div>
                                            <div class="resource-content">
                                                <h3>Complete Trading Guide</h3>
                                                <p>From beginner to advanced: Everything you need to know about successful trading.</p>
                                                <div class="resource-meta">
                                                    <span class="resource-type">Guide</span>
                                                    <span class="resource-duration">45 min read</span>
                                                </div>
                                                <a href="#" class="resource-link">Read Now</a>
                                            </div>
                                        </div>

                                        <div class="resource-card">
                                            <div class="resource-image">
                                                <div class="resource-icon">⚡</div>
                                            </div>
                                            <div class="resource-content">
                                                <h3>Risk Management Masterclass</h3>
                                                <p>Learn how to protect your capital and maximize returns through proper risk management.</p>
                                                <div class="resource-meta">
                                                    <span class="resource-type">Video</span>
                                                    <span class="resource-duration">32 min</span>
                                                </div>
                                                <a href="#" class="resource-link">Watch Now</a>
                                            </div>
                                        </div>

                                        <div class="resource-card">
                                            <div class="resource-image">
                                                <div class="resource-icon">🧮</div>
                                            </div>
                                            <div class="resource-content">
                                                <h3>Position Size Calculator</h3>
                                            <p>Calculate optimal position sizes based on your risk tolerance and account balance.</p>
                                                <div class="resource-meta">
                                                    <span class="resource-type">Tool</span>
                                                    <span class="resource-duration">Interactive</span>
                                                </div>
                                                <a href="#" class="resource-link">Use Tool</a>
                                            </div>
                                        </div>
                                    </div>
                                </section>

                                <!-- Resource Library -->
                                <section class="resource-library-section">
                                    <h2>Resource Library</h2>

                                    <!-- Filter Tabs -->
                                    <div class="resource-filters">
                                        <button class="filter-tab active" data-filter="all">All Resources</button>
                                        <button class="filter-tab" data-filter="guides">Guides</button>
                                        <button class="filter-tab" data-filter="videos">Videos</button>
                                        <button class="filter-tab" data-filter="tools">Tools</button>
                                        <button class="filter-tab" data-filter="webinars">Webinars</button>
                                    </div>

                                    <!-- Resources Grid -->
                                    <div class="resources-grid">
                                        <!-- Educational Guides -->
                                        <div class="resource-item" data-type="guides">
                                            <div class="resource-item-icon">📖</div>
                                            <div class="resource-item-content">
                                                <h4>Technical Analysis Fundamentals</h4>
                                                <p>Master the basics of chart patterns, indicators, and price action.</p>
                                                <span class="resource-badge guide">Guide</span>
                                            </div>
                                            <a href="#" class="resource-item-link">Read</a>
                                        </div>

                                        <div class="resource-item" data-type="guides">
                                            <div class="resource-item-icon">📊</div>
                                            <div class="resource-item-content">
                                                <h4>Options Trading Strategies</h4>
                                                <p>Learn covered calls, protective puts, spreads, and advanced options strategies.</p>
                                                <span class="resource-badge guide">Guide</span>
                                            </div>
                                            <a href="#" class="resource-item-link">Read</a>
                                        </div>

                                        <!-- Videos -->
                                        <div class="resource-item" data-type="videos">
                                            <div class="resource-item-icon">🎥</div>
                                            <div class="resource-item-content">
                                                <h4>Market Analysis Weekly Review</h4>
                                                <p>Weekly market analysis covering major indices, sectors, and key economic data.</p>
                                                <span class="resource-badge video">Video</span>
                                            </div>
                                            <a href="#" class="resource-item-link">Watch</a>
                                        </div>

                                        <div class="resource-item" data-type="videos">
                                            <div class="resource-item-icon">📈</div>
                                            <div class="resource-item-content">
                                                <h4>Live Trading Session</h4>
                                                <p>Watch real-time trading decisions and strategy execution in live market conditions.</p>
                                                <span class="resource-badge video">Video</span>
                                            </div>
                                            <a href="#" class="resource-item-link">Watch</a>
                                        </div>

                                        <!-- Tools -->
                                        <div class="resource-item" data-type="tools">
                                            <div class="resource-item-icon">🧮</div>
                                            <div class="resource-item-content">
                                                <h4>Portfolio Risk Calculator</h4>
                                                <p>Calculate portfolio risk metrics including VaR, Sharpe ratio, and maximum drawdown.</p>
                                                <span class="resource-badge tool">Tool</span>
                                            </div>
                                            <a href="#" class="resource-item-link">Use</a>
                                        </div>

                                        <div class="resource-item" data-type="tools">
                                            <div class="resource-item-icon">📊</div>
                                            <div class="resource-item-content">
                                                <h4>Stock Screener</h4>
                                                <p>Filter stocks based on technical indicators, fundamental data, and custom criteria.</p>
                                                <span class="resource-badge tool">Tool</span>
                                            </div>
                                            <a href="#" class="resource-item-link">Use</a>
                                        </div>

                                        <!-- Webinars -->
                                        <div class="resource-item" data-type="webinars">
                                            <div class="resource-item-icon">🎙️</div>
                                            <div class="resource-item-content">
                                                <h4>Advanced Risk Management</h4>
                                                <p>Learn institutional-grade risk management techniques used by hedge funds.</p>
                                                <span class="resource-badge webinar">Webinar</span>
                                            </div>
                                            <a href="#" class="resource-item-link">Register</a>
                                        </div>

                                        <div class="resource-item" data-type="webinars">
                                            <div class="resource-item-icon">💡</div>
                                            <div class="resource-item-content">
                                                <h4>Trading Psychology Masterclass</h4>
                                                <p>Master your mindset and emotions to become a more disciplined trader.</p>
                                                <span class="resource-badge webinar">Webinar</span>
                                            </div>
                                            <a href="#" class="resource-item-link">Register</a>
                                        </div>
                                    </div>
                                </section>

                                <!-- Newsletter Signup -->
                                <section class="newsletter-section">
                                    <div class="newsletter-content">
                                        <h2>Stay Updated</h2>
                                        <p>Get the latest trading insights, market analysis, and educational content delivered to your inbox.</p>
                                        <form class="newsletter-form">
                                            <input type="email" placeholder="Enter your email address" required>
                                            <button type="submit" class="btn-newsletter">Subscribe</button>
                                        </form>
                                    </div>
                                </section>

                                <!-- Main Content -->
                                <div class="additional-content">
                                    <?php the_content(); ?>
                                </div>
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
.resources-page .hero-section {
    text-align: center;
    padding: 4rem 0;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}

.resources-page .hero-subtitle {
    font-size: 1.3rem;
    margin: 1rem 0 0 0;
    opacity: 0.9;
}

.resources-content {
    display: grid;
    gap: 4rem;
}

.resource-categories {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    margin-bottom: 2rem;
}

.category-card {
    background: white;
    padding: 2rem;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    text-align: center;
    transition: transform 0.2s ease;
    cursor: pointer;
}

.category-card:hover {
    transform: translateY(-2px);
}

.category-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.category-card h3 {
    color: #2c3e50;
    font-size: 1.3rem;
    margin-bottom: 0.5rem;
}

.category-card p {
    color: #666;
    line-height: 1.6;
}

.featured-resources-section h2 {
    font-size: 2.2rem;
    color: #2c3e50;
    text-align: center;
    margin-bottom: 3rem;
}

.featured-resources-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 2rem;
}

.resource-card {
    background: white;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    overflow: hidden;
    transition: transform 0.2s ease;
}

.resource-card:hover {
    transform: translateY(-2px);
}

.resource-card.featured {
    border: 3px solid #667eea;
}

.resource-image {
    height: 200px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
}

.resource-icon {
    font-size: 4rem;
    color: rgba(255,255,255,0.8);
}

.resource-content {
    padding: 1.5rem;
}

.resource-content h3 {
    color: #2c3e50;
    font-size: 1.3rem;
    margin-bottom: 0.5rem;
}

.resource-content p {
    color: #666;
    line-height: 1.6;
    margin-bottom: 1rem;
}

.resource-meta {
    display: flex;
    gap: 1rem;
    margin-bottom: 1rem;
}

.resource-type, .resource-duration {
    font-size: 0.8rem;
    color: #999;
    background: #f8f9fa;
    padding: 2px 8px;
    border-radius: 12px;
}

.resource-link {
    color: #667eea;
    text-decoration: none;
    font-weight: 500;
}

.resource-link:hover {
    text-decoration: underline;
}

.resource-filters {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin-bottom: 3rem;
    flex-wrap: wrap;
}

.filter-tab {
    padding: 0.5rem 1rem;
    border: 2px solid #e9ecef;
    background: white;
    border-radius: 25px;
    cursor: pointer;
    transition: all 0.2s ease;
    font-size: 0.9rem;
}

.filter-tab.active {
    background: #667eea;
    color: white;
    border-color: #667eea;
}

.filter-tab:hover {
    border-color: #667eea;
}

.resources-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
}

.resource-item {
    display: flex;
    align-items: center;
    background: white;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    transition: transform 0.2s ease;
}

.resource-item:hover {
    transform: translateY(-2px);
}

.resource-item-icon {
    font-size: 2rem;
    margin-right: 1rem;
    flex-shrink: 0;
}

.resource-item-content {
    flex: 1;
}

.resource-item-content h4 {
    color: #2c3e50;
    font-size: 1.1rem;
    margin-bottom: 0.5rem;
}

.resource-item-content p {
    color: #666;
    font-size: 0.9rem;
    line-height: 1.4;
    margin-bottom: 0.5rem;
}

.resource-badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 0.7rem;
    font-weight: 500;
    text-transform: uppercase;
}

.resource-badge.guide {
    background: #e3f2fd;
    color: #1976d2;
}

.resource-badge.video {
    background: #f3e5f5;
    color: #7b1fa2;
}

.resource-badge.tool {
    background: #e8f5e8;
    color: #388e3c;
}

.resource-badge.webinar {
    background: #fff3e0;
    color: #f57c00;
}

.resource-item-link {
    color: #667eea;
    text-decoration: none;
    font-weight: 500;
    font-size: 0.9rem;
}

.resource-item-link:hover {
    text-decoration: underline;
}

.newsletter-section {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 4rem 2rem;
    border-radius: 12px;
    text-align: center;
    color: white;
}

.newsletter-content h2 {
    font-size: 2rem;
    margin-bottom: 1rem;
}

.newsletter-content p {
    font-size: 1.2rem;
    margin-bottom: 2rem;
    opacity: 0.9;
}

.newsletter-form {
    display: flex;
    max-width: 500px;
    margin: 0 auto;
    gap: 1rem;
}

.newsletter-form input {
    flex: 1;
    padding: 1rem;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
}

.btn-newsletter {
    background: #48bb78;
    color: white;
    border: none;
    padding: 1rem 2rem;
    border-radius: 8px;
    font-weight: 500;
    cursor: pointer;
    transition: background 0.2s ease;
}

.btn-newsletter:hover {
    background: #38a169;
}

@media (max-width: 768px) {
    .resource-categories {
        grid-template-columns: 1fr;
    }

    .featured-resources-grid {
        grid-template-columns: 1fr;
    }

    .resources-grid {
        grid-template-columns: 1fr;
    }

    .resource-filters {
        justify-content: center;
    }

    .newsletter-form {
        flex-direction: column;
    }

    .resources-page .hero-section {
        padding: 3rem 1rem;
    }

    .newsletter-section {
        padding: 3rem 1rem;
    }
}
</style>

<script>
// Resource filtering functionality
document.addEventListener('DOMContentLoaded', function() {
    const filterTabs = document.querySelectorAll('.filter-tab');
    const resourceItems = document.querySelectorAll('.resource-item');

    filterTabs.forEach(tab => {
        tab.addEventListener('click', function() {
            // Remove active class from all tabs
            filterTabs.forEach(t => t.classList.remove('active'));
            // Add active class to clicked tab
            this.classList.add('active');

            const filter = this.dataset.filter;

            resourceItems.forEach(item => {
                if (filter === 'all' || item.dataset.type === filter) {
                    item.style.display = 'flex';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    });

    // Newsletter form handling
    const newsletterForm = document.querySelector('.newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const email = this.querySelector('input[type="email"]').value;

            // Simple validation
            if (email && email.includes('@')) {
                alert('Thank you for subscribing! We\'ll send you our best trading insights.');
                this.reset();
            } else {
                alert('Please enter a valid email address.');
            }
        });
    }
});
</script>

<?php
get_footer();
?>