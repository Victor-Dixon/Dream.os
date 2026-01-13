// Service Worker for TradingRobotPlug Dashboard - Phase 3 PWA Enhancement
// Implements offline functionality and caching strategies

const CACHE_NAME = 'trp-dashboard-v3.0.0';
const STATIC_CACHE = 'trp-static-v3.0.0';
const API_CACHE = 'trp-api-v3.0.0';

// Resources to cache immediately on install
const STATIC_ASSETS = [
  '/',
  '/static/css/unified.css',
  '/static/js/dashboard.js',
  '/static/js/dashboard-communication.js',
  '/static/js/dashboard-navigation.js',
  '/static/js/dashboard-data-manager.js',
  '/static/js/dashboard-ui-helpers.js',
  '/static/js/dashboard-accessibility.js',
  '/static/js/performance-utils.js',
  '/static/pwa-manifest.json',
  '/static/icons/icon-192x192.png',
  '/static/icons/icon-512x512.png'
];

// API endpoints to cache with Network First strategy
const API_ENDPOINTS = [
  '/api/dashboard-data',
  '/api/swarm-status',
  '/api/trading-stats',
  '/api/agent-status'
];

// Install event - cache static assets
self.addEventListener('install', (event) => {
  console.log('🔧 Service Worker installing...');
  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then((cache) => {
        console.log('📦 Caching static assets...');
        return cache.addAll(STATIC_ASSETS);
      })
      .then(() => {
        console.log('✅ Static assets cached');
        return self.skipWaiting();
      })
      .catch((error) => {
        console.error('❌ Failed to cache static assets:', error);
      })
  );
});

// Activate event - clean up old caches and claim clients
self.addEventListener('activate', (event) => {
  console.log('🚀 Service Worker activating...');
  event.waitUntil(
    Promise.all([
      // Clean up old caches
      caches.keys().then((cacheNames) => {
        return Promise.all(
          cacheNames.map((cacheName) => {
            if (cacheName !== STATIC_CACHE && cacheName !== API_CACHE) {
              console.log('🗑️ Deleting old cache:', cacheName);
              return caches.delete(cacheName);
            }
          })
        );
      }),
      // Take control of all clients
      self.clients.claim()
    ]).then(() => {
      console.log('✅ Service Worker activated and caches cleaned');
    })
  );
});

// Fetch event - implement different caching strategies
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Skip non-GET requests
  if (request.method !== 'GET') return;

  // Handle different resource types
  if (url.pathname.startsWith('/static/')) {
    // Static assets: Cache First strategy
    event.respondWith(cacheFirstStrategy(request));
  } else if (API_ENDPOINTS.some(endpoint => url.pathname.startsWith(endpoint))) {
    // API calls: Network First strategy
    event.respondWith(networkFirstStrategy(request));
  } else if (url.pathname.startsWith('/api/')) {
    // Other API calls: Network First with cache fallback
    event.respondWith(networkFirstStrategy(request));
  } else if (request.destination === 'document') {
    // HTML pages: Network First strategy
    event.respondWith(networkFirstStrategy(request));
  } else {
    // Other resources: Cache First strategy
    event.respondWith(cacheFirstStrategy(request));
  }
});

// Cache First strategy - check cache first, then network
async function cacheFirstStrategy(request) {
  try {
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }

    const networkResponse = await fetch(request);
    if (networkResponse.ok) {
      const cache = await caches.open(STATIC_CACHE);
      cache.put(request, networkResponse.clone());
    }
    return networkResponse;
  } catch (error) {
    console.error('Cache First strategy failed:', error);
    // Return offline fallback for critical resources
    if (request.destination === 'document') {
      return caches.match('/offline.html') || new Response('Offline', { status: 503 });
    }
    throw error;
  }
}

// Network First strategy - try network first, fallback to cache
async function networkFirstStrategy(request) {
  try {
    const networkResponse = await fetch(request);

    if (networkResponse.ok) {
      const cache = await caches.open(API_CACHE);
      cache.put(request, networkResponse.clone());
    }

    return networkResponse;
  } catch (error) {
    console.log('Network failed, trying cache:', error);

    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }

    // Return offline response for API calls
    return new Response(
      JSON.stringify({
        error: 'Offline',
        message: 'Content not available offline',
        timestamp: new Date().toISOString()
      }),
      {
        status: 503,
        headers: { 'Content-Type': 'application/json' }
      }
    );
  }
}

// Background sync for offline actions
self.addEventListener('sync', (event) => {
  console.log('🔄 Background sync triggered:', event.tag);

  if (event.tag === 'background-sync') {
    event.waitUntil(doBackgroundSync());
  }
});

// Perform background synchronization
async function doBackgroundSync() {
  try {
    // Sync any pending actions stored in IndexedDB
    const pendingActions = await getPendingActions();

    for (const action of pendingActions) {
      try {
        await fetch(action.url, action.options);
        await removePendingAction(action.id);
        console.log('✅ Synced pending action:', action.id);
      } catch (error) {
        console.error('❌ Failed to sync action:', action.id, error);
      }
    }
  } catch (error) {
    console.error('❌ Background sync failed:', error);
  }
}

// Push notification handling
self.addEventListener('push', (event) => {
  console.log('📱 Push notification received');

  if (!event.data) return;

  const data = event.data.json();

  const options = {
    body: data.body,
    icon: '/static/icons/icon-192x192.png',
    badge: '/static/icons/icon-72x72.png',
    vibrate: [100, 50, 100],
    data: data.data || {},
    actions: data.actions || [],
    requireInteraction: true
  };

  event.waitUntil(
    self.registration.showNotification(data.title || 'TradingRobotPlug', options)
  );
});

// Notification click handling
self.addEventListener('notificationclick', (event) => {
  console.log('🔔 Notification clicked:', event.action);

  event.notification.close();

  const urlToOpen = event.notification.data?.url || '/';

  event.waitUntil(
    self.clients.matchAll({ type: 'window', includeUncontrolled: true })
      .then((clients) => {
        // Check if there's already a window open
        for (const client of clients) {
          if (client.url === urlToOpen && 'focus' in client) {
            return client.focus();
          }
        }

        // Open new window
        if (self.clients.openWindow) {
          return self.clients.openWindow(urlToOpen);
        }
      })
  );
});

// Periodic background tasks
self.addEventListener('periodicsync', (event) => {
  if (event.tag === 'update-market-data') {
    event.waitUntil(updateMarketData());
  }
});

// Update market data in background
async function updateMarketData() {
  try {
    console.log('📊 Updating market data in background...');

    // This would typically fetch and cache updated market data
    const response = await fetch('/api/market-data');
    if (response.ok) {
      const cache = await caches.open(API_CACHE);
      await cache.put('/api/market-data', response);
      console.log('✅ Market data updated in cache');
    }
  } catch (error) {
    console.error('❌ Background market data update failed:', error);
  }
}

// Utility functions for IndexedDB operations (simplified)
async function getPendingActions() {
  // This would interact with IndexedDB to get pending offline actions
  return [];
}

async function removePendingAction(id) {
  // This would remove a completed action from IndexedDB
  return Promise.resolve();
}

// Error handling and logging
self.addEventListener('error', (event) => {
  console.error('💥 Service Worker error:', event.error);
});

self.addEventListener('unhandledrejection', (event) => {
  console.error('💥 Service Worker unhandled rejection:', event.reason);
});

console.log('🎯 TradingRobotPlug Service Worker loaded - PWA ready!');