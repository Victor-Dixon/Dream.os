<!-- SSOT Domain: integration -->
/**
 * Utility Function Service - V2 Compliant with Modular Architecture
 * Main orchestrator importing specialized utility modules
 * REFACTORED: 337 lines → ~195 lines (42% reduction)
 * V2 COMPLIANCE: Under 300-line limit achieved
 *
 * @author Agent-7 - Web Development Specialist, Agent-8 - Integration & Performance Specialist
 * @version 4.0.0 - V2 COMPLIANCE MODULAR REFACTORING
 * @license MIT
 */

// ================================
// IMPORT MODULAR UTILITY COMPONENTS
// ================================

import { DataUtils } from './utilities/data-utils.js';
import { DeviceUtils } from './utilities/device-utils.js';
import { FunctionUtils } from './utilities/function-utils.js';
import { MathUtils } from './utilities/math-utils.js';
import { StringUtils } from '../../utilities/string-utils.js';
import { LoggingUtils } from '../../utilities/logging-utils.js';
import { ValidationUtils } from '../../utilities/validation-utils.js';
import { ArrayUtils } from '../../utilities/array-utils.js';
import { TimeUtils } from '../../utilities/time-utils.js';

// ================================
// UTILITY FUNCTION SERVICE V4
// ================================

/**
 * Main orchestrator for utility functions using modular architecture
 * V2 COMPLIANT: Delegates to specialized modules for specific functionality
 */
export class UtilityFunctionService {
    constructor() {
        this.logger = new LoggingUtils({ name: "UtilityFunctionService" });
        this.functionUtils = new FunctionUtils();
        this.dataUtils = new DataUtils();
        this.mathUtils = new MathUtils();
        this.stringUtils = new StringUtils();
        this.deviceUtils = new DeviceUtils();
        this.validationUtils = new ValidationUtils();
        this.arrayUtils = new ArrayUtils(this.logger);
        this.timeUtils = new TimeUtils(this.logger);
    }

    // ================================
    // DELEGATION METHODS - FUNCTION UTILS
    // ================================

    /**
     * Debounce function calls
     */
    debounce(func, delay) {
        return this.functionUtils.debounce(func, delay);
    }

    /**
     * Throttle function calls
     */
    throttle(func, limit) {
        return this.functionUtils.throttle(func, limit);
    }

    /**
     * Retry function with exponential backoff
     */
    async retry(func, maxRetries = 3, baseDelay = 1000) {
        return this.functionUtils.retry(func, maxRetries, baseDelay);
    }

    /**
     * Memoize function results
     */
    memoize(func, getKey = null) {
        return this.functionUtils.memoize(func, getKey);
    }

    // ================================
    // DELEGATION METHODS - DATA UTILS
    // ================================

    /**
     * Format currency
     */
    formatCurrency(amount, currency = 'USD') {
        return this.dataUtils.formatCurrency(amount, currency);
    }

    /**
     * Format date (delegates to TimeUtils SSOT)
     */
    formatDate(date, format = 'MM/DD/YYYY') {
        // Use TimeUtils SSOT for date formatting
        // TimeUtils uses Intl.DateTimeFormat, so convert simple format to options
        if (format === 'MM/DD/YYYY') {
            // Simple format - use TimeUtils with medium date style
            return this.timeUtils.formatDate(date, { dateStyle: 'medium' });
        }
        // For other formats, try to map to TimeUtils options or use as-is
        return this.timeUtils.formatDate(date, { dateStyle: format });
    }

    /**
     * Deep clone an object (delegates to ArrayUtils SSOT)
     */
    deepClone(obj) {
        return this.arrayUtils.deepClone(obj);
    }

    // ================================
    // DELEGATION METHODS - MATH UTILS
    // ================================

    /**
     * Calculate percentage
     */
    percentage(part, total) {
        return this.mathUtils.percentage(part, total);
    }

    /**
     * Round to specified decimal places
     */
    roundToDecimal(num, decimals = 2) {
        return this.mathUtils.roundToDecimal(num, decimals);
    }

    /**
     * Generate random number between min and max
     */
    randomBetween(min, max) {
        return this.mathUtils.randomBetween(min, max);
    }

    // ================================
    // DELEGATION METHODS - STRING UTILS
    // ================================

    /**
     * Capitalize first letter of string
     */
    capitalize(str) {
        return this.stringUtils.capitalize(str);
    }

    /**
     * Convert to camelCase
     */
    toCamelCase(str) {
        return this.stringUtils.toCamelCase(str);
    }

    /**
     * Convert to kebab-case
     */
    toKebabCase(str) {
        return this.stringUtils.toKebabCase(str);
    }

    /**
     * Truncate string with ellipsis
     */
    truncate(str, maxLength = 100, suffix = '...') {
        return this.stringUtils.truncate(str, maxLength, suffix);
    }

    // ================================
    // DELEGATION METHODS - DEVICE UTILS
    // ================================

    /**
     * Check if running on mobile device
     */
    isMobileDevice() {
        return this.deviceUtils.isMobileDevice();
    }

    /**
     * Get browser information
     */
    getBrowserInfo() {
        return this.deviceUtils.getBrowserInfo();
    }

    /**
     * Get device type
     */
    getDeviceType() {
        return this.deviceUtils.getDeviceType();
    }

    // ================================
    // DELEGATION METHODS - VALIDATION UTILS
    // ================================

    /**
     * Validate email format
     */
    isValidEmail(email) {
        return this.validationUtils.isValidEmail(email);
    }

    /**
     * Validate phone number format
     */
    isValidPhone(phone) {
        return this.validationUtils.isValidPhone(phone);
    }

    /**
     * Validate URL format
     */
    isValidUrl(url) {
        return this.validationUtils.isValidUrl(url);
    }

    /**
     * Sanitize string input
     */
    sanitizeString(str) {
        return this.validationUtils.sanitizeString(str);
    }

    /**
     * Validate required fields
     */
    validateRequired(value, fieldName) {
        return this.validationUtils.validateRequired(value, fieldName);
    }

    /**
     * Validate string length
     */
    validateLength(str, min = 0, max = Infinity, fieldName = 'string') {
        return this.validationUtils.validateLength(str, min, max, fieldName);
    }

    /**
     * Create timeout wrapper
     */
    withTimeout(func, timeoutMs) {
        return (...args) => {
            return Promise.race([
                func.apply(this, args),
                new Promise((_, reject) =>
                    setTimeout(() => reject(new Error('Operation timed out')), timeoutMs)
                )
            ]);
        };
    }
}

// ================================
// LEGACY EXPORTS FOR BACKWARD COMPATIBILITY
// ================================

const utilityFunctionService = new UtilityFunctionService();

/**
 * Legacy debounce function export
 */
export function debounce(func, delay) {
    return utilityFunctionService.debounce(func, delay);
}

/**
 * Legacy throttle function export
 */
export function throttle(func, limit) {
    return utilityFunctionService.throttle(func, limit);
}

/**
 * Legacy percentage calculation export
 */
export function calculatePercentage(part, total) {
    return utilityFunctionService.percentage(part, total);
}

// ================================
// EXPORTS
// ================================

export default UtilityFunctionService;
