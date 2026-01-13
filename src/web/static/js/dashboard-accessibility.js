/**
 * DASHBOARD ACCESSIBILITY MODULE - PHASE 3 ENHANCEMENT
 *
 * Provides comprehensive accessibility support for the dashboard including:
 * - Keyboard navigation
 * - Screen reader announcements
 * - ARIA live regions
 * - Focus management
 * - High contrast support
 *
 * @author Agent-6 - Web Development Lead (Phase 3)
 * @version 1.0.0
 */

class DashboardAccessibility {
    constructor() {
        this.liveRegion = null;
        this.skipLinks = [];
        this.focusableElements = [];
        this.keyboardShortcuts = new Map();
        this.announcementQueue = [];
        this.isHighContrast = false;
        this.reducedMotion = false;
    }

    /**
     * Initialize accessibility features
     */
    async initialize() {
        this.checkUserPreferences();
        this.createSkipLinks();
        this.createLiveRegion();
        this.setupKeyboardNavigation();
        this.setupKeyboardShortcuts();
        this.setupAriaAnnouncements();
        this.setupFocusManagement();
        this.setupMutationObserver();

        console.log('♿ Dashboard accessibility features initialized');
    }

    /**
     * Check user accessibility preferences
     */
    checkUserPreferences() {
        // Check for reduced motion preference
        this.reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

        // Check for high contrast preference
        this.isHighContrast = window.matchMedia('(prefers-contrast: high)').matches;

        // Apply preferences
        if (this.reducedMotion) {
            document.documentElement.classList.add('reduced-motion');
        }

        if (this.isHighContrast) {
            document.documentElement.classList.add('high-contrast');
        }
    }

    /**
     * Create skip links for keyboard navigation
     */
    createSkipLinks() {
        const skipLinks = [
            { href: '#main-content', text: 'Skip to main content' },
            { href: '#navigation', text: 'Skip to navigation' },
            { href: '#dashboard-overview', text: 'Skip to dashboard overview' }
        ];

        const container = document.createElement('div');
        container.className = 'skip-links';
        container.setAttribute('aria-label', 'Skip navigation links');

        skipLinks.forEach(link => {
            const a = document.createElement('a');
            a.href = link.href;
            a.className = 'skip-link sr-only-focusable';
            a.textContent = link.text;
            container.appendChild(a);
            this.skipLinks.push(a);
        });

        document.body.insertBefore(container, document.body.firstChild);
    }

    /**
     * Create ARIA live region for announcements
     */
    createLiveRegion() {
        this.liveRegion = document.createElement('div');
        this.liveRegion.id = 'accessibility-live-region';
        this.liveRegion.setAttribute('aria-live', 'polite');
        this.liveRegion.setAttribute('aria-atomic', 'true');
        this.liveRegion.className = 'sr-only';
        document.body.appendChild(this.liveRegion);
    }

    /**
     * Set up keyboard navigation enhancements
     */
    setupKeyboardNavigation() {
        document.addEventListener('keydown', (event) => {
            this.handleKeyboardNavigation(event);
        });

        // Update focusable elements when DOM changes
        this.updateFocusableElements();
    }

    /**
     * Handle keyboard navigation
     */
    handleKeyboardNavigation(event) {
        // Tab navigation through focusable elements
        if (event.key === 'Tab') {
            this.handleTabNavigation(event);
        }

        // Escape key handling
        if (event.key === 'Escape') {
            this.handleEscapeKey(event);
        }

        // Arrow key navigation for certain components
        if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(event.key)) {
            this.handleArrowNavigation(event);
        }
    }

    /**
     * Handle tab navigation with improved focus management
     */
    handleTabNavigation(event) {
        const activeElement = document.activeElement;

        // Skip hidden or disabled elements
        if (activeElement && (activeElement.hidden || activeElement.disabled)) {
            const focusableElements = this.getFocusableElements();
            const currentIndex = focusableElements.indexOf(activeElement);

            if (event.shiftKey) {
                // Shift+Tab: move to previous focusable element
                const prevIndex = currentIndex > 0 ? currentIndex - 1 : focusableElements.length - 1;
                focusableElements[prevIndex]?.focus();
            } else {
                // Tab: move to next focusable element
                const nextIndex = currentIndex < focusableElements.length - 1 ? currentIndex + 1 : 0;
                focusableElements[nextIndex]?.focus();
            }

            event.preventDefault();
        }
    }

    /**
     * Handle escape key
     */
    handleEscapeKey(event) {
        // Close modals, dropdowns, etc.
        const openModal = document.querySelector('.modal.show');
        const openDropdown = document.querySelector('.dropdown-menu.show');

        if (openModal) {
            const closeButton = openModal.querySelector('[data-bs-dismiss="modal"], .btn-close');
            closeButton?.click();
            event.preventDefault();
        } else if (openDropdown) {
            const toggle = document.querySelector('[aria-expanded="true"]');
            toggle?.click();
            event.preventDefault();
        }
    }

    /**
     * Handle arrow key navigation
     */
    handleArrowNavigation(event) {
        const activeElement = document.activeElement;

        // Handle navigation in lists, menus, etc.
        if (activeElement.closest('[role="menu"], [role="listbox"], .nav-tabs')) {
            this.handleListNavigation(event, activeElement);
        }
    }

    /**
     * Handle navigation within lists and menus
     */
    handleListNavigation(event, activeElement) {
        const container = activeElement.closest('[role="menu"], [role="listbox"], .nav-tabs');
        if (!container) return;

        const items = Array.from(container.querySelectorAll('[role="menuitem"], [role="option"], .nav-link'));
        const currentIndex = items.indexOf(activeElement);

        if (currentIndex === -1) return;

        let newIndex = currentIndex;

        switch (event.key) {
            case 'ArrowUp':
                newIndex = currentIndex > 0 ? currentIndex - 1 : items.length - 1;
                break;
            case 'ArrowDown':
                newIndex = currentIndex < items.length - 1 ? currentIndex + 1 : 0;
                break;
            case 'ArrowLeft':
            case 'ArrowRight':
                // Handle horizontal navigation if applicable
                this.handleHorizontalNavigation(event, items, currentIndex);
                return;
        }

        if (newIndex !== currentIndex) {
            items[newIndex]?.focus();
            event.preventDefault();
        }
    }

    /**
     * Handle horizontal navigation
     */
    handleHorizontalNavigation(event, items, currentIndex) {
        // Implementation for horizontal navigation if needed
        // This could be used for tab navigation, carousel controls, etc.
    }

    /**
     * Set up keyboard shortcuts
     */
    setupKeyboardShortcuts() {
        // Define keyboard shortcuts
        this.keyboardShortcuts.set('KeyH', () => this.announceHelp());
        this.keyboardShortcuts.set('KeyS', () => this.announceStatus());
        this.keyboardShortcuts.set('KeyF', () => this.focusSearch());
        this.keyboardShortcuts.set('Slash', () => this.focusSearch()); // Alternative for search

        document.addEventListener('keydown', (event) => {
            // Only trigger shortcuts if not in an input field
            if (event.target.tagName === 'INPUT' || event.target.tagName === 'TEXTAREA' || event.target.contentEditable === 'true') {
                return;
            }

            // Check for Ctrl/Cmd + key combinations
            if ((event.ctrlKey || event.metaKey) && this.keyboardShortcuts.has(event.code)) {
                event.preventDefault();
                this.keyboardShortcuts.get(event.code)();
            }
        });
    }

    /**
     * Set up ARIA announcements
     */
    setupAriaAnnouncements() {
        // Override console methods to announce important messages
        const originalLog = console.log;
        const originalError = console.error;
        const originalWarn = console.warn;

        console.log = (...args) => {
            this.announce('Info: ' + args.join(' '), 'polite');
            originalLog.apply(console, args);
        };

        console.error = (...args) => {
            this.announce('Error: ' + args.join(' '), 'assertive');
            originalError.apply(console, args);
        };

        console.warn = (...args) => {
            this.announce('Warning: ' + args.join(' '), 'polite');
            originalWarn.apply(console, args);
        };
    }

    /**
     * Set up focus management
     */
    setupFocusManagement() {
        // Manage focus when modals open/close
        document.addEventListener('show.bs.modal', (event) => {
            const modal = event.target;
            const previouslyFocused = document.activeElement;

            modal.setAttribute('data-previous-focus', previouslyFocused);
            setTimeout(() => {
                const focusableElement = modal.querySelector('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
                focusableElement?.focus();
            }, 100);
        });

        document.addEventListener('hidden.bs.modal', (event) => {
            const modal = event.target;
            const previousFocus = modal.getAttribute('data-previous-focus');
            if (previousFocus) {
                document.querySelector(previousFocus)?.focus();
            }
        });
    }

    /**
     * Set up mutation observer for dynamic content
     */
    setupMutationObserver() {
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === 'childList') {
                    // Announce new content
                    mutation.addedNodes.forEach((node) => {
                        if (node.nodeType === Node.ELEMENT_NODE && node.matches('[aria-live]')) {
                            return; // Skip live regions
                        }
                        if (node.textContent && node.textContent.trim()) {
                            this.announce(`New content added: ${node.textContent.trim().substring(0, 100)}`, 'polite');
                        }
                    });
                }
            });
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }

    /**
     * Announce message to screen readers
     */
    announce(message, priority = 'polite') {
        if (!this.liveRegion) return;

        // Clear any existing content
        this.liveRegion.textContent = '';

        // Set the message
        this.liveRegion.textContent = message;

        // Set priority
        this.liveRegion.setAttribute('aria-live', priority);

        // Clear after a delay for assertive messages
        if (priority === 'assertive') {
            setTimeout(() => {
                this.liveRegion.textContent = '';
            }, 1000);
        }
    }

    /**
     * Get all focusable elements
     */
    getFocusableElements() {
        return Array.from(document.querySelectorAll(
            'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"]), ' +
            '[contenteditable="true"], details, summary, video[controls], audio[controls], ' +
            'iframe, object, embed'
        )).filter(el => {
            return el.offsetWidth > 0 && el.offsetHeight > 0 && !el.hidden && !el.disabled;
        });
    }

    /**
     * Update focusable elements cache
     */
    updateFocusableElements() {
        this.focusableElements = this.getFocusableElements();
    }

    /**
     * Keyboard shortcut handlers
     */
    announceHelp() {
        this.announce(
            'Keyboard shortcuts: Ctrl+H for help, Ctrl+S for status, Ctrl+F for search. ' +
            'Use Tab to navigate, Escape to close dialogs.',
            'polite'
        );
    }

    announceStatus() {
        const status = document.querySelector('.status-indicator, .connection-status');
        if (status) {
            this.announce(`Current status: ${status.textContent || status.getAttribute('aria-label') || 'Unknown'}`, 'polite');
        }
    }

    focusSearch() {
        const searchInput = document.querySelector('input[type="search"], input[placeholder*="search"], #search-input');
        if (searchInput) {
            searchInput.focus();
            this.announce('Search input focused', 'polite');
        }
    }

    /**
     * Utility method to make elements focusable
     */
    makeFocusable(element, tabIndex = 0) {
        element.setAttribute('tabindex', tabIndex);
        element.setAttribute('aria-hidden', 'false');
    }

    /**
     * Utility method to make elements unfocusable
     */
    makeUnfocusable(element) {
        element.setAttribute('tabindex', '-1');
        element.setAttribute('aria-hidden', 'true');
    }

    /**
     * Trap focus within a container (for modals, etc.)
     */
    trapFocus(container) {
        const focusableElements = container.querySelectorAll(
            'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );

        if (focusableElements.length === 0) return;

        const firstElement = focusableElements[0];
        const lastElement = focusableElements[focusableElements.length - 1];

        const handleTabKey = (e) => {
            if (e.key !== 'Tab') return;

            if (e.shiftKey) {
                if (document.activeElement === firstElement) {
                    lastElement.focus();
                    e.preventDefault();
                }
            } else {
                if (document.activeElement === lastElement) {
                    firstElement.focus();
                    e.preventDefault();
                }
            }
        };

        container.addEventListener('keydown', handleTabKey);

        // Return cleanup function
        return () => {
            container.removeEventListener('keydown', handleTabKey);
        };
    }
}

// Export for use in other modules
export { DashboardAccessibility };
export default DashboardAccessibility;