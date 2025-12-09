/**
 * Math Utilities - V2 Compliant Module
 * Mathematical functions and calculations
 * MODULAR: ~90 lines (V2 compliant)
 * 
 * @SSOT Domain: math-operations
 * @SSOT Location: services/utilities/math-utils.js
 * @SSOT Scope: percentage, roundToDecimal, randomBetween, clamp, lerp
 *
 * @author Agent-7 - Web Development Specialist
 * @version 2.0.0 - V2 COMPLIANCE MODULAR EXTRACTION
 * @license MIT
 */

import { LoggingUtils } from '../../../utilities/logging-utils.js';

export class MathUtils {
    constructor() {
        this.logger = new LoggingUtils({ name: "MathUtils" });
    }

    /**
     * Calculate percentage
     */
    percentage(part, total) {
        if (total === 0) return 0;
        return (part / total) * 100;
    }

    /**
     * Round to specified decimal places
     */
    roundToDecimal(num, decimals = 2) {
        return Number(Math.round(num + 'e' + decimals) + 'e-' + decimals);
    }

    /**
     * Generate random number between min and max
     */
    randomBetween(min, max) {
        return Math.random() * (max - min) + min;
    }

    /**
     * Clamp value between min and max
     */
    clamp(value, min, max) {
        return Math.min(Math.max(value, min), max);
    }

    /**
     * Linear interpolation
     */
    lerp(start, end, factor) {
        return start + (end - start) * factor;
    }
}
