<?php
/**
 * Hero Section Template - Free Ride Investor Theme
 * Animated hero section with investment growth visualization
 *
 * @package FreeRideInvestor
 */

// Get hero content from custom fields or defaults
$hero_title = get_theme_mod('hero_title', 'Invest Smarter, Ride Higher');
$hero_subtitle = get_theme_mod('hero_subtitle', 'Unlock your financial potential with data-driven investment strategies');
$hero_cta_text = get_theme_mod('hero_cta_text', 'Start Investing Today');
$hero_cta_url = get_theme_mod('hero_cta_url', '#contact');
?>

<section class="relative min-h-screen flex items-center justify-center overflow-hidden bg-gradient-to-br from-slate-900 via-blue-900 to-slate-800">
    <!-- Animated Background Elements -->
    <div class="absolute inset-0">
        <!-- Floating geometric shapes -->
        <div class="absolute top-20 left-10 w-20 h-20 bg-blue-500/20 rounded-full animate-float"></div>
        <div class="absolute top-40 right-20 w-16 h-16 bg-green-500/20 rounded-lg animate-float-delayed"></div>
        <div class="absolute bottom-32 left-1/4 w-12 h-12 bg-purple-500/20 rounded-full animate-float"></div>
        <div class="absolute bottom-20 right-10 w-24 h-24 bg-yellow-500/20 rounded-lg animate-float-delayed"></div>

        <!-- Grid overlay -->
        <div class="absolute inset-0 bg-[url('data:image/svg+xml,%3Csvg width="60" height="60" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg"%3E%3Cg fill="none" fill-rule="evenodd"%3E%3Cg fill="%23ffffff" fill-opacity="0.03"%3E%3Ccircle cx="30" cy="30" r="1"/%3E%3C/g%3E%3C/g%3E%3C/svg%3E')] opacity-30"></div>
    </div>

    <div class="relative z-10 container mx-auto px-6 text-center">
        <!-- Main Content -->
        <div class="max-w-4xl mx-auto">
            <!-- Animated Title -->
            <h1 class="text-5xl md:text-7xl font-bold text-white mb-6 animate-slide-in-up">
                <span class="bg-gradient-to-r from-blue-400 via-green-400 to-blue-400 bg-clip-text text-transparent animate-gradient-shift">
                    <?php echo esc_html($hero_title); ?>
                </span>
            </h1>

            <!-- Subtitle with glow effect -->
            <p class="text-xl md:text-2xl text-blue-100 mb-8 animate-slide-in-up animation-delay-200 max-w-2xl mx-auto">
                <?php echo esc_html($hero_subtitle); ?>
            </p>

            <!-- Investment Growth Chart Animation -->
            <div class="my-12 animate-slide-in-up animation-delay-400">
                <div class="bg-white/10 backdrop-blur-sm rounded-xl p-8 border border-white/20">
                    <h3 class="text-white text-lg font-semibold mb-6">Projected Growth: 5 Years</h3>
                    <div class="flex items-end justify-center space-x-4 h-32">
                        <!-- Animated bars representing growth -->
                        <div class="w-8 bg-gradient-to-t from-blue-500 to-blue-300 rounded-t animate-grow-bar animation-delay-600" style="height: 40%; animation-delay: 0.6s;"></div>
                        <div class="w-8 bg-gradient-to-t from-green-500 to-green-300 rounded-t animate-grow-bar animation-delay-800" style="height: 55%; animation-delay: 0.8s;"></div>
                        <div class="w-8 bg-gradient-to-t from-purple-500 to-purple-300 rounded-t animate-grow-bar animation-delay-1000" style="height: 70%; animation-delay: 1.0s;"></div>
                        <div class="w-8 bg-gradient-to-t from-yellow-500 to-yellow-300 rounded-t animate-grow-bar animation-delay-1200" style="height: 85%; animation-delay: 1.2s;"></div>
                        <div class="w-8 bg-gradient-to-t from-red-500 to-red-300 rounded-t animate-grow-bar animation-delay-1400" style="height: 100%; animation-delay: 1.4s;"></div>
                    </div>
                    <div class="flex justify-center space-x-4 mt-4 text-sm text-blue-200">
                        <span>Y1</span>
                        <span>Y2</span>
                        <span>Y3</span>
                        <span>Y4</span>
                        <span>Y5</span>
                    </div>
                </div>
            </div>

            <!-- CTA Buttons -->
            <div class="flex flex-col sm:flex-row gap-4 justify-center items-center animate-slide-in-up animation-delay-600">
                <a href="<?php echo esc_url($hero_cta_url); ?>"
                   class="group relative px-8 py-4 bg-gradient-to-r from-blue-600 to-blue-700 text-white font-semibold rounded-lg shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-300 animate-pulse-glow">
                    <span class="relative z-10"><?php echo esc_html($hero_cta_text); ?></span>
                    <div class="absolute inset-0 bg-gradient-to-r from-blue-500 to-green-500 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                </a>

                <a href="#learn-more"
                   class="px-8 py-4 border-2 border-white/30 text-white font-semibold rounded-lg hover:bg-white/10 hover:border-white/50 transition-all duration-300 backdrop-blur-sm">
                    Learn More
                </a>
            </div>

            <!-- Scroll indicator -->
            <div class="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
                <svg class="w-6 h-6 text-white/70" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3"></path>
                </svg>
            </div>
        </div>
    </div>
</section>

<style>
/* Custom animations */
@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-20px); }
}

@keyframes float-delayed {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-15px); }
}

@keyframes gradient-shift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

@keyframes slide-in-up {
    from { transform: translateY(30px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}

@keyframes grow-bar {
    from { height: 0%; }
    to { height: var(--target-height); }
}

@keyframes pulse-glow {
    0%, 100% { box-shadow: 0 0 20px rgba(59, 130, 246, 0.5); }
    50% { box-shadow: 0 0 40px rgba(59, 130, 246, 0.8), 0 0 60px rgba(59, 130, 246, 0.4); }
}

/* Animation classes */
.animate-float { animation: float 6s ease-in-out infinite; }
.animate-float-delayed { animation: float-delayed 8s ease-in-out infinite; animation-delay: 2s; }
.animate-gradient-shift { background-size: 200% 200%; animation: gradient-shift 4s ease infinite; }
.animate-slide-in-up { animation: slide-in-up 0.8s ease-out forwards; }
.animate-pulse-glow { animation: pulse-glow 2s ease-in-out infinite; }
.animate-grow-bar { animation: grow-bar 1.5s ease-out forwards; }

/* Animation delays */
.animation-delay-200 { animation-delay: 0.2s; }
.animation-delay-400 { animation-delay: 0.4s; }
.animation-delay-600 { animation-delay: 0.6s; }
.animation-delay-800 { animation-delay: 0.8s; }
.animation-delay-1000 { animation-delay: 1.0s; }
.animation-delay-1200 { animation-delay: 1.2s; }
.animation-delay-1400 { animation-delay: 1.4s; }
</style>
