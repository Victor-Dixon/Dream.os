/**
 * Data Utilities - V2 Compliant Module
 * Data formatting utilities (SSOT for data-specific operations)
 * NOTE: deepClone and formatDate moved to SSOT utilities (ArrayUtils, TimeUtils)
 * NOTE: Validation methods (isValidEmail, isValidUrl) delegate to ValidationUtils SSOT
 * MODULAR: ~40 lines (V2 compliant, duplicates removed)
 * 
 * @SSOT Domain: data-formatting
 * @SSOT Location: services/utilities/data-utils.js
 * @SSOT Scope: formatCurrency, data operations (delegates validation to ValidationUtils)
 *
 * @author Agent-7 - Web Development Specialist
 * @version 2.2.0 - CONSOLIDATED (validation delegates to ValidationUtils SSOT)
 * @license MIT
 */

import { LoggingUtils } from '../../../utilities/logging-utils.js';
import { ValidationUtils } from '../../../utilities/validation-utils.js';

export class DataUtils {
    constructor() {
        this.logger = new LoggingUtils({ name: "DataUtils" });
        this.validationUtils = new ValidationUtils(this.logger);
    }

    /**
     * Validate email format (delegates to ValidationUtils SSOT)
     */
    isValidEmail(email) {
        return this.validationUtils.isValidEmail(email);
    }

    /**
     * Validate URL format (delegates to ValidationUtils SSOT)
     */
    isValidUrl(url) {
        return this.validationUtils.isValidUrl(url);
    }

    /**
     * Format number as currency (SSOT with validation)
     */
    formatCurrency(amount, currency = 'USD') {
        if (typeof amount !== 'number' || isNaN(amount)) {
            return new Intl.NumberFormat('en-US', {
                style: 'currency',
                currency: currency
            }).format(0);
        }
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: currency
        }).format(amount);
    }

    // NOTE: deepClone removed - use ArrayUtils.deepClone() from utilities/array-utils.js (SSOT)
    // NOTE: formatDate removed - use TimeUtils.formatDate() from utilities/time-utils.js (SSOT)
}
