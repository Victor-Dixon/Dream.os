<!-- SSOT Domain: core -->
/**
 * Unified Frontend Utilities - V2 Compliant Modular Architecture
 * =====
 *
 * Modular frontend utilities with clean separation of concerns.
 * Each utility module handles a specific type of functionality.
 *
 * V2 Compliance: < 300 lines per module, single responsibility.
 *
 * Author: Agent-7 - Web Development Specialist
 * License: MIT
 */

// DOM Utils SSOT: Use orchestrator instead of legacy utilities/dom-utils.js
export { DOMUtilsOrchestrator as DOMUtils } from '../dashboard/dom-utils-orchestrator.js';
export { ValidationUtils } from './validation-utils.js';
// NOTE: CacheUtils and EventUtils removed - use DOMUtilsOrchestrator for cache/event operations (SSOT)
// NOTE: UnifiedFrontendUtilities removed - use individual utility modules (SSOT)
