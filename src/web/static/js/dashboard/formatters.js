/**
 * Dashboard Formatters Module - V2 Compliant
 * Number and data formatting utilities for dashboard components
 * NOTE: formatCurrency and formatDuration delegate to SSOT utilities (DataUtils, TimeUtils)
 * 
 * @SSOT Domain: dashboard-formatting
 * @SSOT Location: dashboard/formatters.js
 * @SSOT Scope: formatNumber, formatPercentage, formatFileSize (delegates formatCurrency/formatDuration to SSOT)
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.1.0 - CONSOLIDATED (using SSOT utilities)
 * @license MIT
 */

import { DataUtils } from '../../services/utilities/data-utils.js';
import { TimeUtils } from '../../utilities/time-utils.js';

// SSOT instances for delegation
const dataUtils = new DataUtils();
const timeUtils = new TimeUtils();

export const DashboardFormatters = {
    /**
     * Format number with appropriate suffix
     */
    formatNumber(num) {
        if (typeof num !== 'number' || isNaN(num)) {
            return '0';
        }

        if (num >= 1000000000) {
            return (num / 1000000000).toFixed(1) + 'B';
        }
        if (num >= 1000000) {
            return (num / 1000000).toFixed(1) + 'M';
        }
        if (num >= 1000) {
            return (num / 1000).toFixed(1) + 'K';
        }
        return num.toString();
    },

    /**
     * Format percentage with validation
     */
    formatPercentage(value) {
        if (typeof value !== 'number' || isNaN(value)) {
            return '0%';
        }
        return `${(value * 100).toFixed(1)}%`;
    },

    /**
     * Format currency value (delegates to DataUtils SSOT)
     */
    formatCurrency(amount, currency = 'USD') {
        return dataUtils.formatCurrency(amount, currency);
    },

    /**
     * Format file size
     */
    formatFileSize(bytes) {
        if (typeof bytes !== 'number' || isNaN(bytes)) {
            return '0 B';
        }

        const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
        if (bytes === 0) return '0 B';

        const i = Math.floor(Math.log(bytes) / Math.log(1024));
        return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i];
    },

    /**
     * Format duration in milliseconds (delegates to TimeUtils SSOT)
     */
    formatDuration(ms) {
        if (typeof ms !== 'number' || isNaN(ms)) {
            return '0ms';
        }
        // Use TimeUtils SSOT for duration formatting
        return timeUtils.formatDuration(ms);
    }
};

// Factory function for creating formatters instance
export function createDashboardFormatters() {
    return { ...DashboardFormatters };
}
