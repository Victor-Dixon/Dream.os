/**
 * String Utilities Module - V2 Compliant
 * Unified string manipulation functions (SSOT)
 * Consolidates utilities/string-utils.js and services/utilities/string-utils.js
 * 
 * @SSOT Domain: string-operations
 * @SSOT Location: utilities/string-utils.js
 * @SSOT Scope: String formatting, sanitization, escapeHTML, string utilities
 *
 * @author Agent-7 - Web Development Specialist
 * @version 2.0.0 - CONSOLIDATED (merged services/utilities/string-utils.js)
 * @license MIT
 */

import { LoggingUtils } from './logging-utils.js';

export class StringUtils {
    constructor(options = {}) {
        this.logger = options.logger || new LoggingUtils({ name: "StringUtils" });
    }

    /**
     * Format string template with data
     */
    formatString(template, data) {
        try {
            if (!template || typeof template !== 'string') {
                throw new Error('Invalid template provided');
            }

            return template.replace(/\{(\w+)\}/g, (match, key) => {
                return data[key] !== undefined ? data[key] : match;
            });
        } catch (error) {
            this.logger.error('String formatting failed', error);
            return template;
        }
    }

    /**
     * Sanitize input string
     */
    sanitizeInput(input, options = {}) {
        const defaultOptions = {
            maxLength: 1000,
            allowHtml: false,
            allowScripts: false
        };

        const config = { ...defaultOptions, ...options };

        if (typeof input !== 'string') {
            return '';
        }

        let sanitized = input.trim();

        if (sanitized.length > config.maxLength) {
            sanitized = sanitized.substring(0, config.maxLength);
        }

        if (!config.allowHtml) {
            sanitized = sanitized.replace(/<[^>]*>/g, '');
        }

        if (!config.allowScripts) {
            sanitized = sanitized.replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '');
            sanitized = sanitized.replace(/javascript:/gi, '');
            sanitized = sanitized.replace(/on\w+\s*=/gi, '');
        }

        return sanitized;
    }

    /**
     * Generate slug from string
     */
    generateSlug(text) {
        try {
            return text
                .toLowerCase()
                .trim()
                .replace(/[^\w\s-]/g, '')
                .replace(/[\s_-]+/g, '-')
                .replace(/^-+|-+$/g, '');
        } catch (error) {
            this.logger.error('Slug generation failed', error);
            return '';
        }
    }

    /**
     * Capitalize first letter
     */
    capitalize(str) {
        if (typeof str !== 'string' || str.length === 0) {
            return str;
        }
        return str.charAt(0).toUpperCase() + str.slice(1);
    }

    /**
     * Truncate text with ellipsis
     */
    truncate(text, maxLength = 100, suffix = '...') {
        if (typeof text !== 'string' || text.length <= maxLength) {
            return text;
        }
        return text.substring(0, maxLength - suffix.length) + suffix;
    }

    /**
     * Convert to camelCase (from services/utilities/string-utils.js)
     */
    toCamelCase(str) {
        if (typeof str !== 'string') return str;
        return str
            .replace(/(?:^\w|[A-Z]|\b\w)/g, (word, index) => {
                return index === 0 ? word.toLowerCase() : word.toUpperCase();
            })
            .replace(/\s+/g, '');
    }

    /**
     * Convert to kebab-case (from services/utilities/string-utils.js)
     */
    toKebabCase(str) {
        if (typeof str !== 'string') return str;
        return str
            .replace(/([a-z])([A-Z])/g, '$1-$2')
            .replace(/[\s_]+/g, '-')
            .toLowerCase();
    }

    /**
     * Remove extra whitespace (from services/utilities/string-utils.js)
     */
    normalizeWhitespace(str) {
        if (typeof str !== 'string') return str;
        return str.replace(/\s+/g, ' ').trim();
    }

    /**
     * Escape HTML to prevent XSS (SSOT)
     */
    escapeHTML(str) {
        if (typeof str !== 'string') {
            return '';
        }
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }
}

// Factory function for creating string utils instance
export function createStringUtils(options = {}) {
    return new StringUtils(options);
}
