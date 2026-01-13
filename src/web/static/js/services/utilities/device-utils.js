/**
 * Device Utilities - V2 Compliant Module
 * Device and browser detection utilities (SSOT for device operations)
 * MODULAR: ~80 lines (V2 compliant)
 * 
 * @SSOT Domain: device-operations
 * @SSOT Location: services/utilities/device-utils.js
 * @SSOT Scope: isMobileDevice, getBrowserInfo, getDeviceType
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - SSOT CREATION
 * @license MIT
 */

import { LoggingUtils } from '../../../utilities/logging-utils.js';

export class DeviceUtils {
    constructor() {
        this.logger = new LoggingUtils({ name: "DeviceUtils" });
    }

    /**
     * Check if running on mobile device (SSOT)
     */
    isMobileDevice() {
        if (typeof window === 'undefined' || !window.navigator) {
            return false;
        }
        const userAgent = window.navigator.userAgent || '';
        const mobileRegex = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i;
        return mobileRegex.test(userAgent);
    }

    /**
     * Get browser information (SSOT)
     */
    getBrowserInfo() {
        if (typeof window === 'undefined' || !window.navigator) {
            return { name: 'unknown', version: 'unknown' };
        }

        const userAgent = window.navigator.userAgent || '';
        let browserName = 'unknown';
        let version = 'unknown';

        if (userAgent.indexOf('Chrome') > -1 && userAgent.indexOf('Edg') === -1) {
            browserName = 'Chrome';
            const match = userAgent.match(/Chrome\/(\d+)/);
            version = match ? match[1] : 'unknown';
        } else if (userAgent.indexOf('Firefox') > -1) {
            browserName = 'Firefox';
            const match = userAgent.match(/Firefox\/(\d+)/);
            version = match ? match[1] : 'unknown';
        } else if (userAgent.indexOf('Safari') > -1 && userAgent.indexOf('Chrome') === -1) {
            browserName = 'Safari';
            const match = userAgent.match(/Version\/(\d+)/);
            version = match ? match[1] : 'unknown';
        } else if (userAgent.indexOf('Edg') > -1) {
            browserName = 'Edge';
            const match = userAgent.match(/Edg\/(\d+)/);
            version = match ? match[1] : 'unknown';
        }

        return { name: browserName, version: version };
    }

    /**
     * Get device type (SSOT)
     */
    getDeviceType() {
        if (typeof window === 'undefined') {
            return 'desktop';
        }

        if (this.isMobileDevice()) {
            const userAgent = window.navigator.userAgent || '';
            if (/iPad/i.test(userAgent)) {
                return 'tablet';
            }
            return 'mobile';
        }

        return 'desktop';
    }
}

// Factory function for creating device utils instance
export function createDeviceUtils() {
    return new DeviceUtils();
}

