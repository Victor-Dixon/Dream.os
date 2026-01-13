<?php
/**
 * Animated Hero Section Component for WordPress
 *
 * Features:
 * - Tailwind CSS animations
 * - Gradient backgrounds
 * - Floating particles
 * - Typewriter effect
 * - Responsive design
 * - WordPress integration ready
 *
 * Usage in WordPress theme:
 * 1. Include this file in your theme
 * 2. Call get_animated_hero_section() function
 * 3. Customize content via WordPress Customizer or ACF
 *
 * @author Agent-2 (Architecture & Design Specialist)
 * @version 1.0.0
 */
?>

<?php
function get_animated_hero_css() {
    ob_start();
    ?>
    <style>
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-20px); }
        }

        @keyframes pulse-glow {
            0%, 100% { box-shadow: 0 0 20px rgba(59, 130, 246, 0.5); }
            50% { box-shadow: 0 0 40px rgba(59, 130, 246, 0.8), 0 0 60px rgba(59, 130, 246, 0.4); }
        }

        @keyframes gradient-shift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        @keyframes slide-in-left {
            from { transform: translateX(-100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }

        @keyframes slide-in-right {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }

        @keyframes fade-in-up {
            from { transform: translateY(30px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }

        @keyframes typewriter {
            from { width: 0; }
            to { width: 100%; }
        }

        @keyframes blink {
            50% { border-color: transparent; }
        }

        .hero-float-animation { animation: float 6s ease-in-out infinite; }
        .hero-pulse-glow { animation: pulse-glow 2s ease-in-out infinite; }
        .hero-gradient-shift { animation: gradient-shift 8s ease infinite; }
        .hero-slide-in-left { animation: slide-in-left 1s ease-out; }
        .hero-slide-in-right { animation: slide-in-right 1s ease-out 0.3s both; }
        .hero-fade-in-up { animation: fade-in-up 1s ease-out 0.6s both; }
        .hero-typewriter { animation: typewriter 3s steps(40, end) 1s both; }
        .hero-blink { animation: blink 1s infinite; }

        /* Responsive adjustments */
        @media (max-width: 768px) {
            .hero-typewriter { font-size: 2rem; }
            .hero-float-animation { animation-duration: 4s; }
        }
    </style>
    <?php
    return ob_get_clean();
}

function get_animated_hero_section($args = []) {
    // Default arguments
    $defaults = [
        'title' => 'Welcome to the Future',
        'subtitle' => 'Experience innovation like never before with our cutting-edge platform that redefines possibilities.',
        'primary_button_text' => 'Get Started Now',
        'primary_button_url' => '#',
        'secondary_button_text' => 'Learn More',
        'secondary_button_url' => '#',
        'features' => [
            [
                'icon' => '⚡',
                'title' => 'Lightning Fast',
                'description' => 'Experience blazing-fast performance with our optimized infrastructure.'
            ],
            [
                'icon' => '🔒',
                'title' => 'Secure & Reliable',
                'description' => 'Your data is protected with enterprise-grade security measures.'
            ],
            [
                'icon' => '❤️',
                'title' => 'User Friendly',
                'description' => 'Intuitive design that makes complex tasks feel effortless.'
            ]
        ],
        'background_class' => 'from-purple-900 via-blue-900 to-indigo-900',
        'particles_enabled' => true,
        'typewriter_enabled' => true
    ];

    $args = wp_parse_args($args, $defaults);
    extract($args);

    ob_start();
    ?>

    <!-- Animated Hero Section -->
    <section class="relative min-h-screen flex items-center justify-center overflow-hidden bg-gray-900">
        <!-- Animated Background -->
        <div class="absolute inset-0 bg-gradient-to-br <?php echo esc_attr($background_class); ?> hero-gradient-shift">
            <?php if ($particles_enabled): ?>
            <!-- Floating Particles -->
            <div class="absolute top-20 left-20 w-4 h-4 bg-blue-400 rounded-full opacity-60 hero-float-animation"></div>
            <div class="absolute top-40 right-32 w-6 h-6 bg-purple-400 rounded-full opacity-40 hero-float-animation" style="animation-delay: 2s;"></div>
            <div class="absolute bottom-32 left-40 w-3 h-3 bg-pink-400 rounded-full opacity-50 hero-float-animation" style="animation-delay: 4s;"></div>
            <div class="absolute bottom-40 right-20 w-5 h-5 bg-green-400 rounded-full opacity-45 hero-float-animation" style="animation-delay: 1s;"></div>
            <div class="absolute top-60 left-60 w-2 h-2 bg-yellow-400 rounded-full opacity-70 hero-float-animation" style="animation-delay: 3s;"></div>

            <!-- Geometric Shapes -->
            <div class="absolute top-16 right-16 w-32 h-32 border-2 border-blue-400/30 rounded-full animate-spin" style="animation-duration: 20s;"></div>
            <div class="absolute bottom-16 left-16 w-24 h-24 border-2 border-purple-400/30 transform rotate-45 animate-pulse"></div>
            <div class="absolute top-1/2 left-1/4 w-16 h-16 bg-gradient-to-r from-pink-500 to-purple-500 rounded-lg transform rotate-12 hero-float-animation" style="animation-delay: 5s;"></div>
            <?php endif; ?>
        </div>

        <!-- Content Container -->
        <div class="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">

            <!-- Main Headline -->
            <div class="mb-8">
                <h1 class="text-5xl md:text-7xl lg:text-8xl font-bold mb-6 text-white">
                    <?php if ($typewriter_enabled): ?>
                    <span class="bg-gradient-to-r from-blue-400 via-purple-500 to-pink-500 bg-clip-text text-transparent">
                        Welcome to
                    </span>
                    <br>
                    <span class="relative inline-block">
                        <span class="hero-typewriter overflow-hidden whitespace-nowrap border-r-4 border-blue-400 text-white">
                            the Future
                        </span>
                    </span>
                    <?php else: ?>
                    <span class="bg-gradient-to-r from-blue-400 via-purple-500 to-pink-500 bg-clip-text text-transparent">
                        <?php echo esc_html($title); ?>
                    </span>
                    <?php endif; ?>
                </h1>

                <p class="text-xl md:text-2xl lg:text-3xl text-gray-300 mb-8 hero-fade-in-up max-w-4xl mx-auto leading-relaxed">
                    <?php echo esc_html($subtitle); ?>
                </p>
            </div>

            <!-- CTA Buttons -->
            <div class="flex flex-col sm:flex-row gap-6 justify-center items-center mb-16 hero-fade-in-up">
                <a href="<?php echo esc_url($primary_button_url); ?>"
                   class="group relative px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full font-semibold text-lg transition-all duration-300 transform hover:scale-105 hover:shadow-2xl hero-pulse-glow text-white no-underline">
                    <span class="relative z-10"><?php echo esc_html($primary_button_text); ?></span>
                    <div class="absolute inset-0 bg-gradient-to-r from-purple-600 to-blue-600 rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                </a>

                <a href="<?php echo esc_url($secondary_button_url); ?>"
                   class="px-8 py-4 border-2 border-white/30 rounded-full font-semibold text-lg hover:bg-white/10 hover:border-white/60 transition-all duration-300 transform hover:scale-105 text-white no-underline">
                    <?php echo esc_html($secondary_button_text); ?>
                </a>
            </div>

            <!-- Feature Highlights -->
            <?php if (!empty($features)): ?>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
                <?php foreach ($features as $index => $feature): ?>
                <div class="bg-white/10 backdrop-blur-lg rounded-2xl p-6 transform hover:scale-105 transition-all duration-300
                           <?php
                           if ($index === 0) echo 'hero-slide-in-left';
                           elseif ($index === count($features) - 1) echo 'hero-slide-in-right';
                           else echo 'hero-fade-in-up';
                           ?>">
                    <div class="w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg mb-4 mx-auto flex items-center justify-center text-2xl">
                        <?php echo esc_html($feature['icon']); ?>
                    </div>
                    <h3 class="text-xl font-semibold mb-2 text-white"><?php echo esc_html($feature['title']); ?></h3>
                    <p class="text-gray-400"><?php echo esc_html($feature['description']); ?></p>
                </div>
                <?php endforeach; ?>
            </div>
            <?php endif; ?>
        </div>

        <!-- Scroll Indicator -->
        <div class="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
            <svg class="w-6 h-6 text-white/60" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3"></path>
            </svg>
        </div>
    </section>

    <?php
    return ob_get_clean();
}

/**
 * WordPress Shortcode for Hero Section
 * Usage: [animated_hero title="Custom Title" subtitle="Custom subtitle"]
 */
function animated_hero_shortcode($atts) {
    $atts = shortcode_atts([
        'title' => 'Welcome to the Future',
        'subtitle' => 'Experience innovation like never before with our cutting-edge platform.',
        'primary_button_text' => 'Get Started Now',
        'primary_button_url' => '#',
        'secondary_button_text' => 'Learn More',
        'secondary_button_url' => '#',
        'background_class' => 'from-purple-900 via-blue-900 to-indigo-900',
        'particles_enabled' => 'true',
        'typewriter_enabled' => 'true'
    ], $atts);

    // Convert string booleans to actual booleans
    $atts['particles_enabled'] = $atts['particles_enabled'] === 'true';
    $atts['typewriter_enabled'] = $atts['typewriter_enabled'] === 'true';

    // Add CSS if not already added
    if (!wp_style_is('tailwindcss', 'enqueued')) {
        wp_enqueue_style('tailwindcss', 'https://cdn.tailwindcss.com');
    }

    // Add custom CSS
    wp_add_inline_style('tailwindcss', get_animated_hero_css());

    return get_animated_hero_section($atts);
}
add_shortcode('animated_hero', 'animated_hero_shortcode');

/**
 * Enqueue required scripts and styles
 */
function animated_hero_enqueue_scripts() {
    // Only enqueue on pages that might use the hero
    if (is_front_page() || has_shortcode(get_post()->post_content, 'animated_hero')) {
        wp_enqueue_style('tailwindcss', 'https://cdn.tailwindcss.com');
        wp_add_inline_style('tailwindcss', get_animated_hero_css());
    }
}
add_action('wp_enqueue_scripts', 'animated_hero_enqueue_scripts');

/**
 * Gutenberg Block Registration (Optional)
 */
function register_animated_hero_block() {
    wp_register_script(
        'animated-hero-block',
        get_template_directory_uri() . '/js/animated-hero-block.js',
        ['wp-blocks', 'wp-element', 'wp-editor']
    );

    register_block_type('custom/animated-hero', [
        'editor_script' => 'animated-hero-block',
        'render_callback' => 'render_animated_hero_block'
    ]);
}

function render_animated_hero_block($attributes) {
    return get_animated_hero_section($attributes);
}

// Uncomment to enable Gutenberg block
// add_action('init', 'register_animated_hero_block');
?>