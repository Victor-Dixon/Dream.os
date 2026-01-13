/**
 * PERFORMANCE UTILITIES - Phase 3 Enhancement
 *
 * Implements performance optimizations including:
 * - Lazy loading for images
 * - Service worker for caching
 * - Code splitting utilities
 * - Bundle size monitoring
 *
 * @author Agent-6 - Web Development Lead (Phase 3)
 * @version 1.0.0
 */

class PerformanceUtils {
    constructor() {
        this.observers = new Map();
        this.serviceWorkerRegistered = false;
        this.lazyLoadObserver = null;
        this.bundleSize = 0;
    }

    /**
     * Initialize performance optimizations
     */
    async initialize() {
        this.setupLazyLoading();
        this.registerServiceWorker();
        this.setupPerformanceMonitoring();
        this.optimizeBundleLoading();
        this.setupResourceHints();

        console.log('⚡ Performance optimizations initialized');
    }

    /**
     * Set up lazy loading for images and other resources
     */
    setupLazyLoading() {
        // Create intersection observer for lazy loading
        this.lazyLoadObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.loadLazyElement(entry.target);
                    this.lazyLoadObserver.unobserve(entry.target);
                }
            });
        }, {
            rootMargin: '50px 0px',
            threshold: 0.01
        });

        // Observe all lazy elements
        this.observeLazyElements();

        // Also handle scroll-based lazy loading as fallback
        this.setupScrollLazyLoading();
    }

    /**
     * Observe elements that should be lazy loaded
     */
    observeLazyElements() {
        // Images
        const lazyImages = document.querySelectorAll('img[data-src], img[data-srcset]');
        lazyImages.forEach(img => this.lazyLoadObserver.observe(img));

        // Background images
        const lazyBackgrounds = document.querySelectorAll('[data-bg]');
        lazyBackgrounds.forEach(el => this.lazyLoadObserver.observe(el));

        // Iframes
        const lazyIframes = document.querySelectorAll('iframe[data-src]');
        lazyIframes.forEach(iframe => this.lazyLoadObserver.observe(iframe));
    }

    /**
     * Load a lazy element
     */
    loadLazyElement(element) {
        if (element.tagName === 'IMG') {
            this.loadLazyImage(element);
        } else if (element.hasAttribute('data-bg')) {
            this.loadLazyBackground(element);
        } else if (element.tagName === 'IFRAME') {
            this.loadLazyIframe(element);
        }
    }

    /**
     * Load lazy image
     */
    loadLazyImage(img) {
        const src = img.getAttribute('data-src');
        const srcset = img.getAttribute('data-srcset');
        const sizes = img.getAttribute('data-sizes');

        if (src) {
            img.src = src;
            img.removeAttribute('data-src');
        }

        if (srcset) {
            img.srcset = srcset;
            img.removeAttribute('data-srcset');
        }

        if (sizes) {
            img.sizes = sizes;
            img.removeAttribute('data-sizes');
        }

        img.classList.remove('lazy');
        img.classList.add('lazy-loaded');
    }

    /**
     * Load lazy background image
     */
    loadLazyBackground(element) {
        const bg = element.getAttribute('data-bg');
        if (bg) {
            element.style.backgroundImage = `url(${bg})`;
            element.removeAttribute('data-bg');
            element.classList.add('lazy-bg-loaded');
        }
    }

    /**
     * Load lazy iframe
     */
    loadLazyIframe(iframe) {
        const src = iframe.getAttribute('data-src');
        if (src) {
            iframe.src = src;
            iframe.removeAttribute('data-src');
            iframe.classList.add('lazy-iframe-loaded');
        }
    }

    /**
     * Set up scroll-based lazy loading as fallback
     */
    setupScrollLazyLoading() {
        let scrollTimeout;

        const handleScroll = () => {
            clearTimeout(scrollTimeout);
            scrollTimeout = setTimeout(() => {
                this.checkScrollLazyLoad();
            }, 100);
        };

        window.addEventListener('scroll', handleScroll, { passive: true });
        window.addEventListener('resize', handleScroll, { passive: true });
    }

    /**
     * Check elements for scroll-based lazy loading
     */
    checkScrollLazyLoad() {
        const lazyElements = document.querySelectorAll('.lazy:not(.lazy-loaded)');
        const viewportHeight = window.innerHeight;

        lazyElements.forEach(element => {
            const rect = element.getBoundingClientRect();
            const elementTop = rect.top;
            const elementBottom = rect.bottom;

            // Load if element is within viewport + buffer
            if (elementTop < viewportHeight + 200 && elementBottom > -200) {
                this.loadLazyElement(element);
            }
        });
    }

    /**
     * Register service worker for caching
     */
    async registerServiceWorker() {
        if ('serviceWorker' in navigator && !this.serviceWorkerRegistered) {
            try {
                const registration = await navigator.serviceWorker.register('/sw.js', {
                    scope: '/'
                });

                console.log('✅ Service worker registered:', registration.scope);

                // Handle updates
                registration.addEventListener('updatefound', () => {
                    const newWorker = registration.installing;
                    if (newWorker) {
                        newWorker.addEventListener('statechange', () => {
                            if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                                this.notifyUpdateAvailable();
                            }
                        });
                    }
                });

                this.serviceWorkerRegistered = true;
            } catch (error) {
                console.error('❌ Service worker registration failed:', error);
            }
        }
    }

    /**
     * Notify user of available update
     */
    notifyUpdateAvailable() {
        const event = new CustomEvent('sw:update-available', {
            detail: { message: 'A new version is available. Refresh to update.' }
        });
        window.dispatchEvent(event);
    }

    /**
     * Set up performance monitoring
     */
    setupPerformanceMonitoring() {
        // Monitor Core Web Vitals
        this.monitorCoreWebVitals();

        // Monitor bundle size
        this.monitorBundleSize();

        // Monitor memory usage
        this.monitorMemoryUsage();
    }

    /**
     * Monitor Core Web Vitals
     */
    monitorCoreWebVitals() {
        // Largest Contentful Paint (LCP)
        new PerformanceObserver((list) => {
            const entries = list.getEntries();
            const lastEntry = entries[entries.length - 1];
            console.log('📊 LCP:', lastEntry.startTime, 'ms');
        }).observe({ entryTypes: ['largest-contentful-paint'] });

        // First Input Delay (FID)
        new PerformanceObserver((list) => {
            const entries = list.getEntries();
            entries.forEach((entry) => {
                console.log('📊 FID:', entry.processingStart - entry.startTime, 'ms');
            });
        }).observe({ entryTypes: ['first-input'] });

        // Cumulative Layout Shift (CLS)
        let clsValue = 0;
        new PerformanceObserver((list) => {
            const entries = list.getEntries();
            entries.forEach((entry) => {
                if (!entry.hadRecentInput) {
                    clsValue += entry.value;
                }
            });
            console.log('📊 CLS:', clsValue);
        }).observe({ entryTypes: ['layout-shift'] });
    }

    /**
     * Monitor bundle size
     */
    monitorBundleSize() {
        // Monitor transferred bytes
        new PerformanceObserver((list) => {
            const entries = list.getEntries();
            entries.forEach((entry) => {
                if (entry.transferSize > 0) {
                    this.bundleSize += entry.transferSize;
                }
            });
            console.log('📦 Bundle size:', this.formatBytes(this.bundleSize));
        }).observe({ entryTypes: ['resource'] });
    }

    /**
     * Monitor memory usage
     */
    monitorMemoryUsage() {
        if ('memory' in performance) {
            setInterval(() => {
                const memInfo = performance.memory;
                const usedPercent = (memInfo.usedJSHeapSize / memInfo.totalJSHeapSize) * 100;
                console.log(`🧠 Memory: ${this.formatBytes(memInfo.usedJSHeapSize)} / ${this.formatBytes(memInfo.totalJSHeapSize)} (${usedPercent.toFixed(1)}%)`);
            }, 10000); // Check every 10 seconds
        }
    }

    /**
     * Optimize bundle loading with code splitting hints
     */
    optimizeBundleLoading() {
        // Preload critical resources
        this.addPreloadLinks();

        // Prefetch likely-to-be-needed resources
        this.addPrefetchLinks();
    }

    /**
     * Add preload links for critical resources
     */
    addPreloadLinks() {
        const criticalResources = [
            { href: '/static/css/unified.css', as: 'style' },
            { href: '/static/js/dashboard.js', as: 'script' },
            { href: '/static/js/dashboard-communication.js', as: 'script' }
        ];

        criticalResources.forEach(resource => {
            const link = document.createElement('link');
            link.rel = 'preload';
            link.href = resource.href;
            link.as = resource.as;
            link.crossOrigin = 'anonymous';
            document.head.appendChild(link);
        });
    }

    /**
     * Add prefetch links for likely resources
     */
    addPrefetchLinks() {
        const prefetchResources = [
            '/static/js/dashboard-navigation.js',
            '/static/js/dashboard-data-manager.js',
            '/api/dashboard-data'
        ];

        prefetchResources.forEach(href => {
            const link = document.createElement('link');
            link.rel = 'prefetch';
            link.href = href;
            document.head.appendChild(link);
        });
    }

    /**
     * Set up resource hints
     */
    setupResourceHints() {
        // DNS prefetch for external domains
        const dnsPrefetchDomains = [
            'fonts.googleapis.com',
            'fonts.gstatic.com',
            'www.gstatic.com'
        ];

        dnsPrefetchDomains.forEach(domain => {
            const link = document.createElement('link');
            link.rel = 'dns-prefetch';
            link.href = `//${domain}`;
            document.head.appendChild(link);
        });
    }

    /**
     * Format bytes for display
     */
    formatBytes(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    /**
     * Create service worker file
     */
    createServiceWorker() {
        const swContent = `
self.addEventListener('install', (event) => {
    console.log('Service worker installing...');
    // Skip waiting to activate immediately
    self.skipWaiting();
});

self.addEventListener('activate', (event) => {
    console.log('Service worker activating...');
    // Clean up old caches
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cache => {
                    if (cache !== 'dashboard-v1') {
                        console.log('Deleting old cache:', cache);
                        return caches.delete(cache);
                    }
                })
            );
        })
    );
});

self.addEventListener('fetch', (event) => {
    // Only cache GET requests
    if (event.request.method !== 'GET') return;

    // Cache static assets
    if (event.request.url.includes('/static/')) {
        event.respondWith(
            caches.open('dashboard-v1').then(cache => {
                return cache.match(event.request).then(response => {
                    if (response) {
                        return response;
                    }
                    return fetch(event.request).then(networkResponse => {
                        cache.put(event.request, networkResponse.clone());
                        return networkResponse;
                    });
                });
            })
        );
    }
});
`;

        // This would need to be saved as /sw.js on the server
        console.log('📝 Service worker content generated (needs to be saved as /sw.js)');
        return swContent;
    }

    /**
     * Get performance metrics
     */
    getPerformanceMetrics() {
        const navigation = performance.getEntriesByType('navigation')[0];
        const paint = performance.getEntriesByType('paint');
        const resources = performance.getEntriesByType('resource');

        return {
            domContentLoaded: navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart,
            loadComplete: navigation.loadEventEnd - navigation.loadEventStart,
            firstPaint: paint.find(entry => entry.name === 'first-paint')?.startTime,
            firstContentfulPaint: paint.find(entry => entry.name === 'first-contentful-paint')?.startTime,
            resourceCount: resources.length,
            totalResourceSize: resources.reduce((total, resource) => total + (resource.transferSize || 0), 0)
        };
    }
}

// Export for use in other modules
export { PerformanceUtils };
export default PerformanceUtils;