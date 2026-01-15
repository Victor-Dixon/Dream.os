/**
 * Logging Utilities Module - V2 Compliant
 * Unified logging system with level-based and operation-focused logging
 * Consolidates LoggingUtils and UnifiedLoggingSystem into single SSOT
 * 
 * @SSOT Domain: logging-operations
 * @SSOT Location: utilities/logging-utils.js
 * @SSOT Scope: Logging, error reporting, operation tracking
 *
 * @author Agent-7 - Web Development Specialist
 * @version 2.0.0 - CONSOLIDATED (LoggingUtils + UnifiedLoggingSystem)
 * @license MIT
 */

export const LOG_LEVELS = {
    ERROR: 0,
    WARN: 1,
    INFO: 2,
    DEBUG: 3,
    TRACE: 4
};

export const LOG_LEVEL_NAMES = {
    [LOG_LEVELS.ERROR]: 'ERROR',
    [LOG_LEVELS.WARN]: 'WARN',
    [LOG_LEVELS.INFO]: 'INFO',
    [LOG_LEVELS.DEBUG]: 'DEBUG',
    [LOG_LEVELS.TRACE]: 'TRACE'
};

export class LoggingUtils {
    constructor(options = {}) {
        this.level = options.level || LOG_LEVELS.INFO;
        this.enableTimestamp = options.enableTimestamp !== false;
        this.enableColors = options.enableColors !== false;
        this.maxLogSize = options.maxLogSize || 1000;
        this.logs = [];
        this.listeners = new Set();
        // Operation tracking (from UnifiedLoggingSystem)
        this.name = options.name || "LoggingUtils";
        this.operationTimers = new Map();
    }

    /**
     * Log error message
     */
    error(message, ...args) {
        this.log(LOG_LEVELS.ERROR, message, ...args);
    }

    /**
     * Log warning message
     */
    warn(message, ...args) {
        this.log(LOG_LEVELS.WARN, message, ...args);
    }

    /**
     * Log info message
     */
    info(message, ...args) {
        this.log(LOG_LEVELS.INFO, message, ...args);
    }

    /**
     * Log debug message
     */
    debug(message, ...args) {
        this.log(LOG_LEVELS.DEBUG, message, ...args);
    }

    /**
     * Log trace message
     */
    trace(message, ...args) {
        this.log(LOG_LEVELS.TRACE, message, ...args);
    }

    /**
     * Core logging function
     */
    log(level, message, ...args) {
        if (level > this.level) return;

        const logEntry = this.createLogEntry(level, message, args);
        const formattedMessage = this.formatLogEntry(logEntry);

        // Store log entry
        this.storeLogEntry(logEntry);

        // Notify listeners
        this.notifyListeners(logEntry);

        // Output to console
        this.outputToConsole(level, formattedMessage);
    }

    /**
     * Create log entry object
     */
    createLogEntry(level, message, args) {
        return {
            level,
            levelName: LOG_LEVEL_NAMES[level],
            message,
            args,
            timestamp: new Date(),
            stack: level === LOG_LEVELS.ERROR ? new Error().stack : null
        };
    }

    /**
     * Format log entry for output
     */
    formatLogEntry(entry) {
        let formatted = '';

        if (this.enableTimestamp) {
            formatted += `[${entry.timestamp.toISOString()}] `;
        }

        if (this.enableColors) {
            formatted += this.colorizeLevel(entry.level);
        } else {
            formatted += `[${entry.levelName}] `;
        }

        formatted += entry.message;

        if (entry.args && entry.args.length > 0) {
            formatted += ' ' + entry.args.map(arg =>
                typeof arg === 'object' ? JSON.stringify(arg, null, 2) : String(arg)
            ).join(' ');
        }

        return formatted;
    }

    /**
     * Colorize log level
     */
    colorizeLevel(level) {
        const colors = {
            [LOG_LEVELS.ERROR]: '\x1b[31m[ERROR]\x1b[0m ', // Red
            [LOG_LEVELS.WARN]: '\x1b[33m[WARN]\x1b[0m  ',  // Yellow
            [LOG_LEVELS.INFO]: '\x1b[36m[INFO]\x1b[0m  ',  // Cyan
            [LOG_LEVELS.DEBUG]: '\x1b[35m[DEBUG]\x1b[0m ', // Magenta
            [LOG_LEVELS.TRACE]: '\x1b[37m[TRACE]\x1b[0m '  // White
        };
        return colors[level] || '[UNKNOWN] ';
    }

    /**
     * Store log entry in memory
     */
    storeLogEntry(entry) {
        this.logs.push(entry);

        // Maintain max log size
        if (this.logs.length > this.maxLogSize) {
            this.logs.shift();
        }
    }

    /**
     * Notify all listeners
     */
    notifyListeners(entry) {
        this.listeners.forEach(listener => {
            try {
                listener(entry);
            } catch (error) {
                console.error('Log listener error:', error);
            }
        });
    }

    /**
     * Output to console
     */
    outputToConsole(level, message) {
        switch (level) {
            case LOG_LEVELS.ERROR:
                console.error(message);
                break;
            case LOG_LEVELS.WARN:
                console.warn(message);
                break;
            case LOG_LEVELS.INFO:
                console.info(message);
                break;
            case LOG_LEVELS.DEBUG:
            case LOG_LEVELS.TRACE:
                console.debug(message);
                break;
        }
    }

    /**
     * Add log listener
     */
    addListener(callback) {
        this.listeners.add(callback);
    }

    /**
     * Remove log listener
     */
    removeListener(callback) {
        this.listeners.delete(callback);
    }

    /**
     * Get recent logs
     */
    getLogs(count = 100, level = null) {
        let filteredLogs = this.logs;

        if (level !== null) {
            filteredLogs = filteredLogs.filter(log => log.level <= level);
        }

        return filteredLogs.slice(-count);
    }

    /**
     * Clear all logs
     */
    clearLogs() {
        this.logs = [];
    }

    /**
     * Set log level
     */
    setLevel(level) {
        if (typeof level === 'string') {
            const levelKey = Object.keys(LOG_LEVELS).find(key => key === level.toUpperCase());
            this.level = levelKey ? LOG_LEVELS[levelKey] : LOG_LEVELS.INFO;
        } else {
            this.level = level;
        }
    }

    /**
     * Export logs to JSON
     */
    exportLogs() {
        return JSON.stringify(this.logs, null, 2);
    }

    // ====
    // OPERATION-FOCUSED LOGGING (from UnifiedLoggingSystem)
    // ====

    /**
     * Log operation start with timer tracking
     */
    logOperationStart(operationName, extra = {}) {
        const message = `Starting ${operationName}`;
        this.info(`[${this.name}] ${message}`, extra);
        this.operationTimers.set(operationName, Date.now());
    }

    /**
     * Log operation completion with duration tracking
     */
    logOperationComplete(operationName, extra = {}) {
        const message = `Completed ${operationName}`;
        this.info(`[${this.name}] ${message}`, extra);

        if (this.operationTimers.has(operationName)) {
            const duration = Date.now() - this.operationTimers.get(operationName);
            this.logPerformanceMetric(`${operationName}_duration`, duration);
            this.operationTimers.delete(operationName);
        }
    }

    /**
     * Log operation failure
     */
    logOperationFailed(operationName, error, extra = {}) {
        const message = `Failed to ${operationName}: ${error}`;
        this.error(`[${this.name}] ${message}`, extra);
        this.operationTimers.delete(operationName);
    }

    /**
     * Log performance metric
     */
    logPerformanceMetric(metricName, metricValue, extra = {}) {
        const message = `Performance metric: ${metricName} = ${metricValue}`;
        this.info(`[${this.name}] ${message}`, extra);
    }

    /**
     * Log generic error
     */
    logErrorGeneric(moduleName, error, extra = {}) {
        const message = `Error in ${moduleName}: ${error}`;
        this.error(`[${this.name}] ${message}`, extra);
    }

    /**
     * Log validation start
     */
    logValidationStart(itemType, itemId, extra = {}) {
        const message = `Starting validation of ${itemType}: ${itemId}`;
        this.info(`[${this.name}] ${message}`, extra);
    }

    /**
     * Log validation passed
     */
    logValidationPassed(itemType, itemId, extra = {}) {
        const message = `Validation passed for ${itemType}: ${itemId}`;
        this.info(`[${this.name}] ${message}`, extra);
    }

    /**
     * Log validation failed
     */
    logValidationFailed(itemType, itemId, error, extra = {}) {
        const message = `Validation failed for ${itemType}: ${itemId} - ${error}`;
        this.error(`[${this.name}] ${message}`, extra);
    }
}

// Factory function for creating logging utils instance
export function createLoggingUtils(options = {}) {
    return new LoggingUtils(options);
}

// Backward compatibility: Export UnifiedLoggingSystem as alias
// This allows existing code using UnifiedLoggingSystem to continue working
export const UnifiedLoggingSystem = LoggingUtils;

// Global logger instance
export const globalLogger = createLoggingUtils();
