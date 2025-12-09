/**
 * Validation Utilities - V2 Compliant Module
 * Data validation utilities (SSOT for validation operations)
 * MODULAR: ~80 lines (V2 compliant)
 * 
 * @SSOT Domain: validation-operations
 * @SSOT Location: utilities/validation-utils.js
 * @SSOT Scope: Email, URL, phone validation, field validation
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - SSOT CREATION (consolidates DataUtils validation)
 * @license MIT
 */

import { LoggingUtils } from './logging-utils.js';

export class ValidationUtils {
    constructor(logger = null) {
        this.logger = logger || new LoggingUtils({ name: "ValidationUtils" });
    }

    /**
     * Validate email format (SSOT)
     */
    isValidEmail(email) {
        if (!email || typeof email !== 'string') {
            return false;
        }
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    /**
     * Validate URL format (SSOT)
     */
    isValidUrl(url) {
        if (!url || typeof url !== 'string') {
            return false;
        }
        try {
            new URL(url);
            return true;
        } catch {
            return false;
        }
    }

    /**
     * Validate phone number format
     */
    isValidPhone(phone) {
        if (!phone || typeof phone !== 'string') {
            return false;
        }
        // Basic phone validation - accepts digits, spaces, dashes, parentheses, plus
        const phoneRegex = /^[\d\s\-\(\)\+]+$/;
        const digitsOnly = phone.replace(/\D/g, '');
        return phoneRegex.test(phone) && digitsOnly.length >= 10;
    }

    /**
     * Validate required field
     */
    validateRequired(value, fieldName = 'Field') {
        if (value === null || value === undefined || value === '') {
            throw new Error(`${fieldName} is required`);
        }
        if (typeof value === 'string' && value.trim() === '') {
            throw new Error(`${fieldName} cannot be empty`);
        }
    }

    /**
     * Validate string length
     */
    validateLength(str, min = 0, max = Infinity, fieldName = 'String') {
        if (typeof str !== 'string') {
            throw new Error(`${fieldName} must be a string`);
        }
        if (str.length < min) {
            throw new Error(`${fieldName} must be at least ${min} characters`);
        }
        if (str.length > max) {
            throw new Error(`${fieldName} must be at most ${max} characters`);
        }
    }

    /**
     * Sanitize string input
     */
    sanitizeString(str) {
        if (typeof str !== 'string') {
            return '';
        }
        return str.trim().replace(/[<>]/g, '');
    }
}

// Factory function for creating validation utils instance
export function createValidationUtils(logger = null) {
    return new ValidationUtils(logger);
}

