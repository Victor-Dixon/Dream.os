<?php
/**
 * Main template file
 * Displays posts when no more specific template matches a query
 */
get_header();
?>

<main id="main" class="site-main">
    <div class="container">
        <div class="content-area">
            <?php if (have_posts()) : ?>
                <div class="posts-grid">
                    <?php while (have_posts()) : the_post(); ?>
                        <article id="post-<?php the_ID(); ?>" <?php post_class('post-card'); ?>>
                            <header class="entry-header">
                                <?php if (has_post_thumbnail()) : ?>
                                    <div class="post-thumbnail">
                                        <?php the_post_thumbnail('medium'); ?>
                                    </div>
                                <?php endif; ?>

                                <h2 class="entry-title">
                                    <a href="<?php the_permalink(); ?>"><?php the_title(); ?></a>
                                </h2>

                                <div class="entry-meta">
                                    <span class="posted-on">
                                        <?php _e('Posted on', 'event-services'); ?> <?php the_date(); ?>
                                    </span>
                                    <span class="byline">
                                        <?php _e('by', 'event-services'); ?> <?php the_author(); ?>
                                    </span>
                                </div>
                            </header>

                            <div class="entry-content">
                                <?php the_excerpt(); ?>
                            </div>

                            <footer class="entry-footer">
                                <a href="<?php the_permalink(); ?>" class="read-more">
                                    <?php _e('Read More', 'event-services'); ?>
                                </a>
                            </footer>
                        </article>
                    <?php endwhile; ?>

                    <div class="pagination">
                        <?php
                        the_posts_pagination(array(
                            'prev_text' => __('Previous', 'event-services'),
                            'next_text' => __('Next', 'event-services'),
                        ));
                        ?>
                    </div>
                </div>

            <?php else : ?>
                <div class="no-posts">
                    <h2><?php _e('Nothing Found', 'event-services'); ?></h2>
                    <p><?php _e('Sorry, no posts matched your criteria.', 'event-services'); ?></p>
                </div>
            <?php endif; ?>
        </div>

        <?php get_sidebar(); ?>
    </div>
</main>

<?php get_footer(); ?>