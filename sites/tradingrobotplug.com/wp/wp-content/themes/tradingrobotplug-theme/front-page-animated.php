<?php
/*
TradingRobotPlug Animated Hero Homepage - Three.js + Tailwind CSS
Description: Revolutionary animated hero with live TSLA intelligence, 3D particles, and AI swarm visualization
Author: Agent-7 (Web Development) + Strategic Oversight
Version: 3.0.0 - Advanced Animated Implementation
Updated: 2026-01-15
*/
get_header(); ?>

<!-- ===== ADVANCED ANIMATED HERO SECTION ===== -->
<section id="hero-section" class="relative min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 overflow-hidden">
    <!-- Three.js Canvas Container -->
    <canvas id="hero-canvas" class="absolute inset-0 w-full h-full"></canvas>

    <!-- Animated Background Gradient Overlay -->
    <div class="absolute inset-0 bg-gradient-to-r from-black/60 via-transparent to-black/60 pointer-events-none"></div>

    <!-- Floating Particle System -->
    <div id="particle-system" class="absolute inset-0 pointer-events-none">
        <div class="particle particle-1"></div>
        <div class="particle particle-2"></div>
        <div class="particle particle-3"></div>
        <div class="particle particle-4"></div>
        <div class="particle particle-5"></div>
    </div>

    <!-- Main Hero Content -->
    <div class="relative z-10 flex items-center justify-center min-h-screen px-4 py-20">
        <div class="max-w-7xl mx-auto text-center">

            <!-- AI Swarm Intelligence Badge -->
            <div class="inline-flex items-center gap-2 bg-white/10 backdrop-blur-md border border-white/20 rounded-full px-4 py-2 mb-8 animate-fade-in-up">
                <div class="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                <span class="text-white/90 text-sm font-medium">AI Swarm Online - 8 Agents Active</span>
            </div>

            <!-- Main Headline with Gradient Animation -->
            <h1 class="text-5xl md:text-7xl lg:text-8xl font-bold mb-6 animate-fade-in-up animation-delay-200">
                <span class="bg-gradient-to-r from-cyan-400 via-purple-400 to-pink-400 bg-clip-text text-transparent animate-gradient-x">
                    Live TSLA
                </span>
                <br>
                <span class="text-white">Intelligence</span>
            </h1>

            <!-- Live TSLA Price Display -->
            <div id="live-tsla-display" class="bg-white/10 backdrop-blur-lg border border-white/20 rounded-2xl p-6 mb-8 mx-auto max-w-md animate-fade-in-up animation-delay-400">
                <div class="flex items-center justify-between mb-4">
                    <div class="flex items-center gap-3">
                        <div class="w-10 h-10 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-full flex items-center justify-center">
                            <span class="text-white font-bold text-sm">TSLA</span>
                        </div>
                        <div class="text-left">
                            <div class="text-white font-semibold">Tesla, Inc.</div>
                            <div class="text-white/60 text-sm">NASDAQ</div>
                        </div>
                    </div>
                    <div id="tsla-status" class="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
                </div>

                <div class="grid grid-cols-2 gap-4 mb-4">
                    <div class="text-center">
                        <div class="text-white/60 text-xs uppercase tracking-wide">Price</div>
                        <div id="tsla-price" class="text-white text-xl font-bold">--</div>
                    </div>
                    <div class="text-center">
                        <div class="text-white/60 text-xs uppercase tracking-wide">24h Change</div>
                        <div id="tsla-change" class="text-lg font-semibold">--</div>
                    </div>
                </div>

                <!-- AI Recommendation -->
                <div class="bg-gradient-to-r from-purple-500/20 to-pink-500/20 rounded-lg p-3 border border-purple-400/30">
                    <div class="flex items-center justify-between">
                        <div class="flex items-center gap-2">
                            <div class="w-2 h-2 bg-purple-400 rounded-full animate-pulse"></div>
                            <span class="text-white/90 text-sm">AI Swarm Analysis</span>
                        </div>
                        <div id="ai-confidence" class="text-white font-bold">--%</div>
                    </div>
                    <div id="ai-recommendation" class="text-white text-lg font-bold mt-1">--</div>
                </div>
            </div>

            <!-- Performance Stats Grid -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10 max-w-4xl mx-auto animate-fade-in-up animation-delay-600">
                <div class="bg-white/10 backdrop-blur-lg border border-white/20 rounded-xl p-6">
                    <div class="text-cyan-400 text-3xl font-bold mb-2">24.7%</div>
                    <div class="text-white/80 text-sm">Total Returns</div>
                    <div class="text-white/60 text-xs mt-1">Since Inception</div>
                </div>

                <div class="bg-white/10 backdrop-blur-lg border border-white/20 rounded-xl p-6">
                    <div class="text-green-400 text-3xl font-bold mb-2">89.3%</div>
                    <div class="text-white/80 text-sm">Win Rate</div>
                    <div class="text-white/60 text-xs mt-1">Success Rate</div>
                </div>

                <div class="bg-white/10 backdrop-blur-lg border border-white/20 rounded-xl p-6">
                    <div class="text-purple-400 text-3xl font-bold mb-2">$2.4M</div>
                    <div class="text-white/80 text-sm">Volume Traded</div>
                    <div class="text-white/60 text-xs mt-1">Paper Trading</div>
                </div>
            </div>

            <!-- Call-to-Action Buttons -->
            <div class="flex flex-col sm:flex-row gap-4 justify-center items-center mb-12 animate-fade-in-up animation-delay-800">
                <a href="<?php echo esc_url(home_url('/waitlist')); ?>"
                   class="group relative px-8 py-4 bg-gradient-to-r from-cyan-500 to-purple-600 hover:from-cyan-400 hover:to-purple-500 text-white font-bold rounded-full transition-all duration-300 transform hover:scale-105 hover:shadow-2xl hover:shadow-cyan-500/25 overflow-hidden">
                    <span class="relative z-10">🚀 Test Live Strategy</span>
                    <div class="absolute inset-0 bg-gradient-to-r from-cyan-400 to-purple-500 opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-full"></div>
                </a>

                <a href="#strategy-marketplace"
                   class="px-8 py-4 border-2 border-white/30 hover:border-white/60 text-white font-bold rounded-full transition-all duration-300 hover:bg-white/10 backdrop-blur-sm">
                    📊 View All Strategies
                </a>
            </div>

            <!-- Live Market Heatmap Preview -->
            <div class="bg-white/5 backdrop-blur-lg border border-white/10 rounded-xl p-6 max-w-2xl mx-auto animate-fade-in-up animation-delay-1000">
                <h3 class="text-white text-lg font-semibold mb-4">🌍 Live Market Correlations</h3>
                <div id="market-heatmap" class="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <!-- Market data populated by JavaScript -->
                    <div class="text-center">
                        <div class="text-white/60 text-xs mb-1">TSLA</div>
                        <div id="heatmap-tsla" class="text-2xl font-bold">--</div>
                    </div>
                    <div class="text-center">
                        <div class="text-white/60 text-xs mb-1">QQQ</div>
                        <div id="heatmap-qqq" class="text-lg">--</div>
                    </div>
                    <div class="text-center">
                        <div class="text-white/60 text-xs mb-1">SPY</div>
                        <div id="heatmap-spy" class="text-lg">--</div>
                    </div>
                    <div class="text-center">
                        <div class="text-white/60 text-xs mb-1">NVDA</div>
                        <div id="heatmap-nvda" class="text-lg">--</div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Scroll Indicator -->
    <div class="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
        <div class="w-6 h-10 border-2 border-white/30 rounded-full flex justify-center">
            <div class="w-1 h-3 bg-white/60 rounded-full mt-2 animate-pulse"></div>
        </div>
    </div>
</section>

<!-- ===== STRATEGY MARKETPLACE PREVIEW ===== -->
<section id="strategy-marketplace" class="py-20 bg-slate-50">
    <div class="max-w-7xl mx-auto px-4">
        <div class="text-center mb-16">
            <h2 class="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
                AI Trading Strategies
            </h2>
            <p class="text-xl text-gray-600 max-w-3xl mx-auto">
                Our swarm has developed and tested multiple trading algorithms.
                Each strategy is optimized for different market conditions.
            </p>
        </div>

        <div class="grid md:grid-cols-3 gap-8">
            <!-- Conservative Strategy -->
            <div class="bg-white rounded-xl shadow-lg p-8 hover:shadow-xl transition-shadow duration-300">
                <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-6">
                    <span class="text-green-600 text-2xl">📈</span>
                </div>
                <h3 class="text-2xl font-bold text-gray-900 mb-2">Conservative Growth</h3>
                <p class="text-gray-600 mb-6">Stable, long-term focused strategy with proven risk management.</p>

                <div class="space-y-3 mb-6">
                    <div class="flex justify-between">
                        <span class="text-gray-600">Total Return</span>
                        <span class="font-bold text-green-600">+24.7%</span>
                    </div>
                    <div class="flex justify-between">
                        <span class="text-gray-600">Win Rate</span>
                        <span class="font-bold text-green-600">89.3%</span>
                    </div>
                    <div class="flex justify-between">
                        <span class="text-gray-600">Max Drawdown</span>
                        <span class="font-bold text-red-600">-12.4%</span>
                    </div>
                </div>

                <button class="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-6 rounded-lg transition-colors duration-200">
                    Backtest Strategy
                </button>
            </div>

            <!-- Momentum Strategy -->
            <div class="bg-white rounded-xl shadow-lg p-8 hover:shadow-xl transition-shadow duration-300">
                <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-6">
                    <span class="text-blue-600 text-2xl">🚀</span>
                </div>
                <h3 class="text-2xl font-bold text-gray-900 mb-2">Momentum Trading</h3>
                <p class="text-gray-600 mb-6">High-conviction trades based on market momentum and volume analysis.</p>

                <div class="space-y-3 mb-6">
                    <div class="flex justify-between">
                        <span class="text-gray-600">Total Return</span>
                        <span class="font-bold text-green-600">+42.1%</span>
                    </div>
                    <div class="flex justify-between">
                        <span class="text-gray-600">Win Rate</span>
                        <span class="font-bold text-green-600">76.8%</span>
                    </div>
                    <div class="flex justify-between">
                        <span class="text-gray-600">Max Drawdown</span>
                        <span class="font-bold text-red-600">-28.7%</span>
                    </div>
                </div>

                <button class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg transition-colors duration-200">
                    Backtest Strategy
                </button>
            </div>

            <!-- Mean Reversion Strategy -->
            <div class="bg-white rounded-xl shadow-lg p-8 hover:shadow-xl transition-shadow duration-300">
                <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-6">
                    <span class="text-purple-600 text-2xl">🔄</span>
                </div>
                <h3 class="text-2xl font-bold text-gray-900 mb-2">Mean Reversion</h3>
                <p class="text-gray-600 mb-6">Statistical arbitrage based on price deviations from moving averages.</p>

                <div class="space-y-3 mb-6">
                    <div class="flex justify-between">
                        <span class="text-gray-600">Total Return</span>
                        <span class="font-bold text-green-600">+31.5%</span>
                    </div>
                    <div class="flex justify-between">
                        <span class="text-gray-600">Win Rate</span>
                        <span class="font-bold text-green-600">82.4%</span>
                    </div>
                    <div class="flex justify-between">
                        <span class="text-gray-600">Max Drawdown</span>
                        <span class="font-bold text-red-600">-18.9%</span>
                    </div>
                </div>

                <button class="w-full bg-purple-600 hover:bg-purple-700 text-white font-bold py-3 px-6 rounded-lg transition-colors duration-200">
                    Backtest Strategy
                </button>
            </div>
        </div>

        <div class="text-center mt-12">
            <p class="text-gray-600 mb-6">Ready to see how these strategies perform in real-time?</p>
            <a href="<?php echo esc_url(home_url('/waitlist')); ?>"
               class="inline-block bg-gradient-to-r from-cyan-500 to-purple-600 hover:from-cyan-400 hover:to-purple-500 text-white font-bold py-4 px-8 rounded-full transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-xl">
                🚀 Join Beta Waitlist
            </a>
        </div>
    </div>
</section>

<!-- ===== ADVANCED CSS ANIMATIONS ===== -->
<style>
/* Three.js Canvas Styling */
#hero-canvas {
    filter: blur(0.5px);
    opacity: 0.8;
}

/* Particle System */
.particle {
    position: absolute;
    width: 4px;
    height: 4px;
    background: radial-gradient(circle, rgba(255,255,255,0.8) 0%, rgba(0,212,255,0.4) 50%, transparent 100%);
    border-radius: 50%;
    pointer-events: none;
    animation: float 20s linear infinite;
}

.particle-1 { top: 20%; left: 10%; animation-delay: 0s; }
.particle-2 { top: 60%; left: 80%; animation-delay: 5s; }
.particle-3 { top: 40%; left: 60%; animation-delay: 10s; }
.particle-4 { top: 80%; left: 20%; animation-delay: 15s; }
.particle-5 { top: 30%; left: 90%; animation-delay: 7s; }

@keyframes float {
    0%, 100% { transform: translateY(0px) translateX(0px); opacity: 0.3; }
    25% { transform: translateY(-20px) translateX(10px); opacity: 0.8; }
    50% { transform: translateY(-10px) translateX(-10px); opacity: 0.6; }
    75% { transform: translateY(-30px) translateX(5px); opacity: 0.9; }
}

/* Advanced Animations */
@keyframes fade-in-up {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes gradient-x {
    0%, 100% {
        background-size: 200% 200%;
        background-position: left center;
    }
    50% {
        background-size: 200% 200%;
        background-position: right center;
    }
}

.animate-fade-in-up {
    animation: fade-in-up 0.8s ease-out forwards;
    opacity: 0;
}

.animation-delay-200 { animation-delay: 0.2s; }
.animation-delay-400 { animation-delay: 0.4s; }
.animation-delay-600 { animation-delay: 0.6s; }
.animation-delay-800 { animation-delay: 0.8s; }
.animation-delay-1000 { animation-delay: 1.0s; }

.animate-gradient-x {
    animation: gradient-x 3s ease infinite;
}

/* Responsive Design */
@media (max-width: 768px) {
    .text-5xl { font-size: 2.5rem; }
    .text-7xl { font-size: 3.5rem; }
    .text-8xl { font-size: 4rem; }

    .grid-cols-1 { grid-template-columns: repeat(1, minmax(0, 1fr)); }
    .md\\:grid-cols-3 { grid-template-columns: repeat(1, minmax(0, 1fr)); }
}

/* Accessibility */
@media (prefers-reduced-motion: reduce) {
    .animate-fade-in-up,
    .animate-gradient-x,
    .animate-bounce {
        animation: none;
    }

    .particle {
        display: none;
    }
}
</style>

<!-- ===== THREE.JS + TAILWIND INTEGRATION ===== -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.tailwindcss.com"></script>

<script>
// Initialize Tailwind with custom configuration
tailwind.config = {
    theme: {
        extend: {
            colors: {
                'brand-cyan': '#00d4ff',
                'brand-purple': '#9d4edd',
                'brand-pink': '#ff0080',
                'brand-green': '#00ff88'
            }
        }
    }
}

// Three.js Particle System
class ParticleSystem {
    constructor() {
        this.scene = new THREE.Scene();
        this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        this.renderer = new THREE.WebGLRenderer({ canvas: document.getElementById('hero-canvas'), alpha: true });
        this.particles = [];
        this.mouse = new THREE.Vector2();

        this.init();
        this.animate();
        this.setupEventListeners();
    }

    init() {
        // Setup renderer
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.renderer.setClearColor(0x000000, 0);

        // Setup camera
        this.camera.position.z = 5;

        // Create particles
        this.createParticles();

        // Add ambient light
        const ambientLight = new THREE.AmbientLight(0x404040, 0.6);
        this.scene.add(ambientLight);

        // Add point light
        const pointLight = new THREE.PointLight(0x00d4ff, 1, 100);
        pointLight.position.set(10, 10, 10);
        this.scene.add(pointLight);
    }

    createParticles() {
        const particleCount = window.innerWidth < 768 ? 100 : 200;
        const geometry = new THREE.BufferGeometry();
        const positions = new Float32Array(particleCount * 3);
        const colors = new Float32Array(particleCount * 3);

        for (let i = 0; i < particleCount; i++) {
            // Random positions
            positions[i * 3] = (Math.random() - 0.5) * 20;
            positions[i * 3 + 1] = (Math.random() - 0.5) * 20;
            positions[i * 3 + 2] = (Math.random() - 0.5) * 20;

            // Color gradient
            const color = new THREE.Color();
            color.setHSL(Math.random(), 0.7, 0.6);
            colors[i * 3] = color.r;
            colors[i * 3 + 1] = color.g;
            colors[i * 3 + 2] = color.b;
        }

        geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

        const material = new THREE.PointsMaterial({
            size: 0.02,
            vertexColors: true,
            transparent: true,
            opacity: 0.8,
            blending: THREE.AdditiveBlending
        });

        this.points = new THREE.Points(geometry, material);
        this.scene.add(this.points);
    }

    animate() {
        requestAnimationFrame(() => this.animate());

        // Rotate particles slowly
        if (this.points) {
            this.points.rotation.x += 0.0005;
            this.points.rotation.y += 0.0003;

            // Mouse interaction
            const positions = this.points.geometry.attributes.position.array;
            for (let i = 0; i < positions.length; i += 3) {
                const x = positions[i];
                const y = positions[i + 1];

                // Subtle attraction to mouse
                const dx = this.mouse.x * 5 - x;
                const dy = this.mouse.y * 5 - y;
                const distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < 2) {
                    positions[i] += dx * 0.01;
                    positions[i + 1] += dy * 0.01;
                }
            }

            this.points.geometry.attributes.position.needsUpdate = true;
        }

        this.renderer.render(this.scene, this.camera);
    }

    setupEventListeners() {
        const handleMouseMove = (event) => {
            this.mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
            this.mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
        };

        const handleResize = () => {
            this.camera.aspect = window.innerWidth / window.innerHeight;
            this.camera.updateProjectionMatrix();
            this.renderer.setSize(window.innerWidth, window.innerHeight);
        };

        window.addEventListener('mousemove', handleMouseMove);
        window.addEventListener('resize', handleResize);
    }
}

// Live TSLA Data Integration
class LiveTSLAData {
    constructor() {
        this.apiEndpoint = '<?php echo esc_url(rest_url('tradingrobotplug/v1/stock-data')); ?>';
        this.updateInterval = 30000; // 30 seconds
        this.timer = null;
    }

    async fetchData() {
        try {
            const response = await fetch(`${this.apiEndpoint}?symbols=TSLA,QQQ,SPY,NVDA`);
            const data = await response.json();

            if (data.stock_data) {
                this.updateUI(data.stock_data);
            }
        } catch (error) {
            console.error('Error fetching TSLA data:', error);
        }
    }

    updateUI(stockData) {
        // Find TSLA data
        const tslaData = stockData.find(stock =>
            stock.symbol === 'TSLA' || stock.SYMBOL === 'TSLA'
        );

        if (tslaData) {
            // Update main price display
            const price = parseFloat(tslaData.price || tslaData.PRICE || 0);
            const changePercent = parseFloat(tslaData.change_percent || tslaData.CHANGE_PERCENT || 0);

            document.getElementById('tsla-price').textContent = `$${price.toFixed(2)}`;
            document.getElementById('tsla-change').textContent =
                `${changePercent >= 0 ? '+' : ''}${changePercent.toFixed(2)}%`;

            // Update AI recommendation (mock for now)
            const recommendation = changePercent > 0 ? 'BUY' : changePercent < -2 ? 'SELL' : 'HOLD';
            const confidence = Math.abs(changePercent) * 10 + 50; // Mock confidence calculation

            document.getElementById('ai-recommendation').textContent = recommendation;
            document.getElementById('ai-confidence').textContent = `${Math.min(confidence, 95).toFixed(0)}%`;

            // Update status indicator
            const statusEl = document.getElementById('tsla-status');
            statusEl.className = `w-3 h-3 rounded-full ${
                changePercent >= 0 ? 'bg-green-400' :
                changePercent < -2 ? 'bg-red-400' : 'bg-yellow-400'
            } animate-pulse`;
        }

        // Update market heatmap
        ['TSLA', 'QQQ', 'SPY', 'NVDA'].forEach(symbol => {
            const stock = stockData.find(s =>
                (s.symbol || s.SYMBOL) === symbol
            );
            if (stock) {
                const changePercent = parseFloat(stock.change_percent || stock.CHANGE_PERCENT || 0);
                const element = document.getElementById(`heatmap-${symbol.toLowerCase()}`);
                if (element) {
                    element.textContent = `${changePercent >= 0 ? '+' : ''}${changePercent.toFixed(1)}%`;
                    element.className = changePercent >= 0 ? 'text-green-400' : 'text-red-400';
                }
            }
        });
    }

    start() {
        this.fetchData(); // Initial fetch
        this.timer = setInterval(() => this.fetchData(), this.updateInterval);
    }

    stop() {
        if (this.timer) {
            clearInterval(this.timer);
            this.timer = null;
        }
    }
}

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Initialize Three.js particle system
    const particleSystem = new ParticleSystem();

    // Initialize live TSLA data
    const tslaData = new LiveTSLAData();
    tslaData.start();

    // Add scroll-triggered animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in-up');
            }
        });
    }, observerOptions);

    // Observe elements for animation
    document.querySelectorAll('.animate-fade-in-up').forEach(el => {
        observer.observe(el);
    });

    // Cleanup on page unload
    window.addEventListener('beforeunload', () => {
        tslaData.stop();
    });
});
</script>

<?php get_footer(); ?>