<?php
/**
 * Template Name: Blog
 * Template Post Type: page
 *
 * The template for displaying blog/news page
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

                    <article id="post-<?php the_ID(); ?>" <?php post_class('blog-page'); ?>>
                        <header class="entry-header">
                            <div class="hero-section">
                                <h1 class="entry-title"><?php the_title(); ?></h1>
                                <div class="hero-subtitle">
                                    <?php if (get_field('hero_subtitle')) : ?>
                                        <p><?php echo esc_html(get_field('hero_subtitle')); ?></p>
                                    <?php else : ?>
                                        <p>Latest market insights, trading strategies, and educational content</p>
                                    <?php endif; ?>
                                </div>
                            </div>
                        </header>

                        <div class="entry-content">
                            <div class="blog-content">

                                <!-- Featured Post -->
                                <?php
                                $featured_args = array(
                                    'posts_per_page' => 1,
                                    'meta_key' => 'featured_post',
                                    'meta_value' => '1',
                                    'post_status' => 'publish'
                                );

                                $featured_query = new WP_Query($featured_args);

                                if ($featured_query->have_posts()) :
                                    while ($featured_query->have_posts()) : $featured_query->the_post();
                                ?>
                                <section class="featured-post-section">
                                    <div class="featured-post">
                                        <div class="featured-image">
                                            <?php if (has_post_thumbnail()) : ?>
                                                <?php the_post_thumbnail('large'); ?>
                                            <?php else : ?>
                                                <div class="featured-placeholder">
                                                    <span>📈</span>
                                                </div>
                                            <?php endif; ?>
                                        </div>
                                        <div class="featured-content">
                                            <div class="featured-meta">
                                                <span class="featured-badge">Featured</span>
                                                <span class="post-date"><?php echo get_the_date(); ?></span>
                                                <span class="post-category">
                                                    <?php
                                                    $categories = get_the_category();
                                                    if (!empty($categories)) {
                                                        echo esc_html($categories[0]->name);
                                                    }
                                                    ?>
                                                </span>
                                            </div>
                                            <h2 class="featured-title">
                                                <a href="<?php the_permalink(); ?>"><?php the_title(); ?></a>
                                            </h2>
                                            <p class="featured-excerpt">
                                                <?php echo wp_trim_words(get_the_excerpt(), 30); ?>
                                            </p>
                                            <a href="<?php the_permalink(); ?>" class="btn-featured">Read More</a>
                                        </div>
                                    </div>
                                </section>
                                <?php
                                    endwhile;
                                    wp_reset_postdata();
                                endif;
                                ?>

                                <!-- Blog Posts Grid -->
                                <section class="blog-posts-section">
                                    <div class="blog-controls">
                                        <div class="blog-categories">
                                            <a href="#" class="category-filter active" data-category="all">All Posts</a>
                                            <?php
                                            $categories = get_categories(array(
                                                'exclude' => array(1), // Exclude 'Uncategorized'
                                                'hide_empty' => true
                                            ));

                                            foreach ($categories as $category) :
                                            ?>
                                            <a href="#" class="category-filter" data-category="<?php echo esc_attr($category->slug); ?>">
                                                <?php echo esc_html($category->name); ?>
                                            </a>
                                            <?php endforeach; ?>
                                        </div>

                                        <div class="blog-search">
                                            <input type="text" placeholder="Search articles..." class="search-input">
                                            <button class="search-btn">🔍</button>
                                        </div>
                                    </div>

                                    <div class="blog-posts-grid">
                                        <?php
                                        $paged = (get_query_var('paged')) ? get_query_var('paged') : 1;
                                        $blog_args = array(
                                            'post_type' => 'post',
                                            'posts_per_page' => 12,
                                            'paged' => $paged,
                                            'post_status' => 'publish'
                                        );

                                        $blog_query = new WP_Query($blog_args);

                                        if ($blog_query->have_posts()) :
                                            while ($blog_query->have_posts()) : $blog_query->the_post();
                                        ?>
                                        <article class="blog-post-card" data-category="<?php
                                            $post_categories = get_the_category();
                                            echo esc_attr($post_categories[0]->slug ?? 'uncategorized');
                                        ?>">
                                            <div class="post-image">
                                                <?php if (has_post_thumbnail()) : ?>
                                                    <?php the_post_thumbnail('medium'); ?>
                                                <?php else : ?>
                                                    <div class="post-placeholder">
                                                        <span>📊</span>
                                                    </div>
                                                <?php endif; ?>
                                            </div>

                                            <div class="post-content">
                                                <div class="post-meta">
                                                    <span class="post-date"><?php echo get_the_date('M j, Y'); ?></span>
                                                    <span class="post-category">
                                                        <?php
                                                        $categories = get_the_category();
                                                        if (!empty($categories)) {
                                                            echo esc_html($categories[0]->name);
                                                        }
                                                        ?>
                                                    </span>
                                                    <span class="reading-time">
                                                        <?php
                                                        $content = get_post_field('post_content', get_the_ID());
                                                        $word_count = str_word_count(strip_tags($content));
                                                        $reading_time = ceil($word_count / 200);
                                                        echo $reading_time . ' min read';
                                                        ?>
                                                    </span>
                                                </div>

                                                <h3 class="post-title">
                                                    <a href="<?php the_permalink(); ?>"><?php the_title(); ?></a>
                                                </h3>

                                                <p class="post-excerpt">
                                                    <?php echo wp_trim_words(get_the_excerpt(), 20); ?>
                                                </p>

                                                <div class="post-footer">
                                                    <a href="<?php the_permalink(); ?>" class="read-more">Read More</a>
                                                    <div class="post-stats">
                                                        <span class="comments-count">
                                                            💬 <?php echo get_comments_number(); ?>
                                                        </span>
                                                    </div>
                                                </div>
                                            </div>
                                        </article>
                                        <?php
                                            endwhile;

                                            // Pagination
                                            echo '<div class="blog-pagination">';
                                            echo paginate_links(array(
                                                'total' => $blog_query->max_num_pages,
                                                'current' => $paged,
                                                'prev_text' => '« Previous',
                                                'next_text' => 'Next »'
                                            ));
                                            echo '</div>';

                                            wp_reset_postdata();
                                        else :
                                        ?>
                                        <div class="no-posts">
                                            <div class="no-posts-icon">📝</div>
                                            <h3>No articles found</h3>
                                            <p>We haven't published any articles yet. Check back soon for the latest market insights and trading strategies.</p>
                                        </div>
                                        <?php endif; ?>
                                    </div>
                                </section>

                                <!-- Newsletter Signup -->
                                <section class="blog-newsletter-section">
                                    <div class="newsletter-content">
                                        <h2>Never Miss an Update</h2>
                                        <p>Get our latest market analysis, trading strategies, and educational content delivered straight to your inbox.</p>
                                        <form class="newsletter-form" id="blog-newsletter-form">
                                            <input type="email" name="email" placeholder="Enter your email address" required>
                                            <input type="hidden" name="source" value="blog_page">
                                            <button type="submit" class="btn-newsletter">Subscribe to Updates</button>
                                        </form>
                                        <p class="newsletter-disclaimer">We respect your privacy. Unsubscribe at any time.</p>
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
.blog-page .hero-section {
    text-align: center;
    padding: 4rem 0;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}

.blog-page .hero-subtitle {
    font-size: 1.3rem;
    margin: 1rem 0 0 0;
    opacity: 0.9;
}

.blog-content {
    display: grid;
    gap: 4rem;
}

.featured-post-section {
    margin-bottom: 2rem;
}

.featured-post {
    display: grid;
    grid-template-columns: 2fr 3fr;
    gap: 3rem;
    background: white;
    border-radius: 12px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    overflow: hidden;
}

.featured-image {
    position: relative;
    overflow: hidden;
}

.featured-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.featured-placeholder {
    width: 100%;
    height: 300px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 4rem;
}

.featured-content {
    padding: 3rem;
}

.featured-meta {
    display: flex;
    gap: 1rem;
    margin-bottom: 1rem;
    align-items: center;
}

.featured-badge {
    background: #667eea;
    color: white;
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 0.8rem;
    font-weight: 500;
}

.post-date, .post-category {
    color: #666;
    font-size: 0.9rem;
}

.featured-title {
    font-size: 2rem;
    color: #2c3e50;
    margin-bottom: 1rem;
    line-height: 1.2;
}

.featured-title a {
    color: inherit;
    text-decoration: none;
}

.featured-title a:hover {
    color: #667eea;
}

.featured-excerpt {
    color: #666;
    font-size: 1.1rem;
    line-height: 1.6;
    margin-bottom: 2rem;
}

.btn-featured {
    background: #667eea;
    color: white;
    padding: 0.75rem 2rem;
    border-radius: 8px;
    text-decoration: none;
    font-weight: 500;
    display: inline-block;
    transition: background 0.2s ease;
}

.btn-featured:hover {
    background: #5a67d8;
}

.blog-controls {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 3rem;
    flex-wrap: wrap;
    gap: 2rem;
}

.blog-categories {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
}

.category-filter {
    color: #666;
    text-decoration: none;
    padding: 0.5rem 1rem;
    border-radius: 25px;
    transition: all 0.2s ease;
    border: 2px solid transparent;
}

.category-filter:hover, .category-filter.active {
    color: #667eea;
    border-color: #667eea;
    background: rgba(102, 126, 234, 0.1);
}

.blog-search {
    display: flex;
    gap: 0.5rem;
}

.search-input {
    padding: 0.5rem 1rem;
    border: 2px solid #e9ecef;
    border-radius: 25px;
    outline: none;
    width: 250px;
}

.search-input:focus {
    border-color: #667eea;
}

.search-btn {
    background: #667eea;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 25px;
    cursor: pointer;
    transition: background 0.2s ease;
}

.search-btn:hover {
    background: #5a67d8;
}

.blog-posts-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 2rem;
}

.blog-post-card {
    background: white;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    overflow: hidden;
    transition: transform 0.2s ease;
}

.blog-post-card:hover {
    transform: translateY(-2px);
}

.post-image {
    position: relative;
    overflow: hidden;
    height: 200px;
}

.post-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.2s ease;
}

.blog-post-card:hover .post-image img {
    transform: scale(1.05);
}

.post-placeholder {
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 3rem;
}

.post-content {
    padding: 1.5rem;
}

.post-meta {
    display: flex;
    gap: 1rem;
    margin-bottom: 1rem;
    align-items: center;
    flex-wrap: wrap;
}

.post-title {
    font-size: 1.3rem;
    color: #2c3e50;
    margin-bottom: 0.5rem;
    line-height: 1.3;
}

.post-title a {
    color: inherit;
    text-decoration: none;
}

.post-title a:hover {
    color: #667eea;
}

.post-excerpt {
    color: #666;
    line-height: 1.5;
    margin-bottom: 1rem;
}

.post-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.read-more {
    color: #667eea;
    text-decoration: none;
    font-weight: 500;
}

.read-more:hover {
    text-decoration: underline;
}

.post-stats {
    display: flex;
    gap: 1rem;
}

.comments-count {
    color: #666;
    font-size: 0.9rem;
}

.blog-pagination {
    grid-column: 1 / -1;
    text-align: center;
    margin-top: 3rem;
}

.blog-pagination .page-numbers {
    color: #667eea;
    text-decoration: none;
    padding: 0.5rem 1rem;
    margin: 0 0.25rem;
    border-radius: 6px;
    transition: all 0.2s ease;
}

.blog-pagination .page-numbers:hover, .blog-pagination .current {
    background: #667eea;
    color: white;
}

.no-posts {
    grid-column: 1 / -1;
    text-align: center;
    background: white;
    padding: 4rem 2rem;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}

.no-posts-icon {
    font-size: 4rem;
    margin-bottom: 1rem;
}

.no-posts h3 {
    color: #2c3e50;
    font-size: 1.5rem;
    margin-bottom: 1rem;
}

.no-posts p {
    color: #666;
    max-width: 500px;
    margin: 0 auto;
}

.blog-newsletter-section {
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

.newsletter-disclaimer {
    font-size: 0.9rem;
    margin-top: 1rem;
    opacity: 0.8;
}

@media (max-width: 768px) {
    .featured-post {
        grid-template-columns: 1fr;
    }

    .blog-controls {
        flex-direction: column;
        align-items: stretch;
        gap: 1rem;
    }

    .blog-categories {
        justify-content: center;
    }

    .blog-posts-grid {
        grid-template-columns: 1fr;
    }

    .blog-page .hero-section {
        padding: 3rem 1rem;
    }

    .featured-content {
        padding: 2rem;
    }

    .post-footer {
        flex-direction: column;
        gap: 0.5rem;
        align-items: stretch;
    }

    .newsletter-form {
        flex-direction: column;
    }

    .search-input {
        width: 100%;
    }
}
</style>

<script>
// Blog filtering and search functionality
document.addEventListener('DOMContentLoaded', function() {
    const categoryFilters = document.querySelectorAll('.category-filter');
    const blogPosts = document.querySelectorAll('.blog-post-card');
    const searchInput = document.querySelector('.search-input');
    const searchBtn = document.querySelector('.search-btn');

    // Category filtering
    categoryFilters.forEach(filter => {
        filter.addEventListener('click', function(e) {
            e.preventDefault();

            // Remove active class from all filters
            categoryFilters.forEach(f => f.classList.remove('active'));
            // Add active class to clicked filter
            this.classList.add('active');

            const category = this.dataset.category;

            blogPosts.forEach(post => {
                if (category === 'all' || post.dataset.category === category) {
                    post.style.display = 'block';
                } else {
                    post.style.display = 'none';
                }
            });
        });
    });

    // Search functionality
    function performSearch() {
        const searchTerm = searchInput.value.toLowerCase().trim();

        blogPosts.forEach(post => {
            const title = post.querySelector('.post-title').textContent.toLowerCase();
            const excerpt = post.querySelector('.post-excerpt').textContent.toLowerCase();
            const content = title + ' ' + excerpt;

            if (content.includes(searchTerm) || searchTerm === '') {
                post.style.display = 'block';
            } else {
                post.style.display = 'none';
            }
        });
    }

    searchBtn.addEventListener('click', performSearch);
    searchInput.addEventListener('keyup', function(e) {
        if (e.key === 'Enter') {
            performSearch();
        }
    });

    // Newsletter form handling
    const newsletterForm = document.getElementById('blog-newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const email = this.querySelector('input[name="email"]').value;

            if (email && email.includes('@')) {
                alert('Thank you for subscribing! You\'ll receive our latest market insights and trading strategies.');
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