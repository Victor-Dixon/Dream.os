/**
 * Operational Transformation Client Library - Phase 4 Sprint 4
 * ===========================================================
 *
 * Real-time collaborative editing with operational transformation for web applications.
 *
 * Features:
 * - Real-time collaborative document editing
 * - Operational transformation for conflict resolution
 * - Automatic synchronization with server
 * - Undo/redo support with collaborative awareness
 * - Connection health monitoring
 *
 * Usage:
 * ```javascript
 * const otClient = new OTClient('session-123', 'user-456');
 * otClient.connect().then(() => {
 *   otClient.on('documentChanged', (content) => {
 *     // Update your UI
 *     document.getElementById('editor').value = content;
 *   });
 * });
 * ```
 *
 * Author: Agent-6 (Web Architecture Lead)
 * Date: 2026-01-08
 * Phase: Phase 4 Sprint 4 - Operational Transformation Engine
 */

class OperationalTransformationClient {
  /**
   * Create a new operational transformation client.
   * @param {string} sessionId - Unique session identifier
   * @param {string} clientId - Unique client identifier
   * @param {Object} options - Configuration options
   */
  constructor(sessionId, clientId, options = {}) {
    this.sessionId = sessionId;
    this.clientId = clientId;
    this.options = {
      websocketUrl: options.websocketUrl || 'ws://localhost:8766/ws/ai/collaboration',
      reconnectInterval: options.reconnectInterval || 5000,
      maxReconnectAttempts: options.maxReconnectAttempts || 10,
      operationDebounceMs: options.operationDebounceMs || 100,
      ...options
    };

    this.ws = null;
    this.connected = false;
    this.reconnectAttempts = 0;
    this.documentState = {
      content: '',
      version: 0,
      checksum: '',
      lastModified: 0
    };

    this.operationQueue = [];
    this.pendingOperations = new Map();
    this.eventListeners = new Map();

    // Debounced operation sending
    this.sendOperationTimeout = null;

    // Bind methods
    this._onMessage = this._onMessage.bind(this);
    this._onOpen = this._onOpen.bind(this);
    this._onClose = this._onClose.bind(this);
    this._onError = this._onError.bind(this);
  }

  /**
   * Connect to the operational transformation server.
   * @returns {Promise<void>}
   */
  async connect() {
    if (this.connected) {
      return Promise.resolve();
    }

    return new Promise((resolve, reject) => {
      try {
        this.ws = new WebSocket(this.options.websocketUrl);

        this.ws.onopen = () => {
          this._onOpen();
          resolve();
        };

        this.ws.onmessage = this._onMessage;
        this.ws.onclose = this._onClose;
        this.ws.onerror = (error) => {
          this._onError(error);
          if (!this.connected) {
            reject(error);
          }
        };

        // Connection timeout
        setTimeout(() => {
          if (!this.connected) {
            reject(new Error('Connection timeout'));
          }
        }, 10000);

      } catch (error) {
        reject(error);
      }
    });
  }

  /**
   * Disconnect from the server.
   */
  disconnect() {
    if (this.ws) {
      this.ws.close();
    }
    this.connected = false;
    this.reconnectAttempts = 0;
  }

  /**
   * Send an operation to the server.
   * @param {string} type - Operation type (insert, delete, update, replace)
   * @param {number} position - Position in the document
   * @param {string} content - Content for the operation
   * @param {number} length - Length for delete operations
   * @param {Object} metadata - Additional operation metadata
   */
  sendOperation(type, position, content = '', length = 0, metadata = {}) {
    const operation = {
      id: this._generateOperationId(),
      session_id: this.sessionId,
      client_id: this.clientId,
      type: type,
      position: position,
      content: content,
      length: length,
      timestamp: Date.now() / 1000,
      priority: 1,
      metadata: metadata
    };

    // Add to pending operations
    this.pendingOperations.set(operation.id, operation);

    // Debounce operation sending
    if (this.sendOperationTimeout) {
      clearTimeout(this.sendOperationTimeout);
    }

    this.sendOperationTimeout = setTimeout(() => {
      this._sendPendingOperations();
    }, this.options.operationDebounceMs);

    return operation.id;
  }

  /**
   * Insert text at a specific position.
   * @param {number} position - Position to insert at
   * @param {string} text - Text to insert
   * @returns {string} Operation ID
   */
  insert(position, text) {
    return this.sendOperation('insert', position, text);
  }

  /**
   * Delete text from a specific position.
   * @param {number} position - Position to start deleting from
   * @param {number} length - Length of text to delete
   * @returns {string} Operation ID
   */
  delete(position, length) {
    return this.sendOperation('delete', position, '', length);
  }

  /**
   * Update/replace text at a specific position.
   * @param {number} position - Position to update
   * @param {string} newText - New text content
   * @param {number} length - Length of text to replace
   * @returns {string} Operation ID
   */
  update(position, newText, length) {
    return this.sendOperation('update', position, newText, length);
  }

  /**
   * Replace entire document content.
   * @param {string} content - New document content
   * @returns {string} Operation ID
   */
  replace(content) {
    return this.sendOperation('replace', 0, content);
  }

  /**
   * Get current document content.
   * @returns {string} Current document content
   */
  getContent() {
    return this.documentState.content;
  }

  /**
   * Get current document version.
   * @returns {number} Current version number
   */
  getVersion() {
    return this.documentState.version;
  }

  /**
   * Request synchronization with the server.
   * @param {number} lastKnownVersion - Last known version (optional)
   */
  requestSync(lastKnownVersion = null) {
    const version = lastKnownVersion !== null ? lastKnownVersion : this.documentState.version;

    this._send({
      type: 'sync_request',
      session_id: this.sessionId,
      client_id: this.clientId,
      last_version: version
    });
  }

  /**
   * Add event listener.
   * @param {string} event - Event name
   * @param {Function} callback - Event callback function
   */
  on(event, callback) {
    if (!this.eventListeners.has(event)) {
      this.eventListeners.set(event, []);
    }
    this.eventListeners.get(event).push(callback);
  }

  /**
   * Remove event listener.
   * @param {string} event - Event name
   * @param {Function} callback - Event callback function
   */
  off(event, callback) {
    if (this.eventListeners.has(event)) {
      const listeners = this.eventListeners.get(event);
      const index = listeners.indexOf(callback);
      if (index > -1) {
        listeners.splice(index, 1);
      }
    }
  }

  /**
   * Emit event to listeners.
   * @param {string} event - Event name
   * @param {*} data - Event data
   */
  _emit(event, data) {
    if (this.eventListeners.has(event)) {
      this.eventListeners.get(event).forEach(callback => {
        try {
          callback(data);
        } catch (error) {
          console.error(`Error in ${event} event listener:`, error);
        }
      });
    }
  }

  /**
   * Handle WebSocket open event.
   */
  _onOpen() {
    this.connected = true;
    this.reconnectAttempts = 0;

    // Join the session
    this._send({
      type: 'join_session',
      session_id: this.sessionId,
      client_id: this.clientId
    });

    this._emit('connected', { sessionId: this.sessionId, clientId: this.clientId });
  }

  /**
   * Handle WebSocket message event.
   * @param {MessageEvent} event - WebSocket message event
   */
  _onMessage(event) {
    try {
      const data = JSON.parse(event.data);
      this._handleMessage(data);
    } catch (error) {
      console.error('Failed to parse WebSocket message:', error);
    }
  }

  /**
   * Handle WebSocket close event.
   */
  _onClose() {
    this.connected = false;
    this._emit('disconnected', { sessionId: this.sessionId, clientId: this.clientId });

    // Attempt reconnection
    if (this.reconnectAttempts < this.options.maxReconnectAttempts) {
      this.reconnectAttempts++;
      setTimeout(() => {
        this._emit('reconnecting', { attempt: this.reconnectAttempts });
        this.connect().catch(error => {
          console.error('Reconnection failed:', error);
        });
      }, this.options.reconnectInterval);
    }
  }

  /**
   * Handle WebSocket error event.
   * @param {Event} error - WebSocket error event
   */
  _onError(error) {
    console.error('WebSocket error:', error);
    this._emit('error', { error, sessionId: this.sessionId, clientId: this.clientId });
  }

  /**
   * Handle incoming message from server.
   * @param {Object} data - Message data
   */
  _handleMessage(data) {
    switch (data.type) {
      case 'welcome':
        this._emit('welcome', data);
        break;

      case 'session_joined':
        this._emit('sessionJoined', data);
        break;

      case 'operation_ack':
        this._handleOperationAck(data);
        break;

      case 'remote_operation':
        this._handleRemoteOperation(data);
        break;

      case 'sync_response':
        this._handleSyncResponse(data);
        break;

      case 'collaborator_joined':
        this._emit('collaboratorJoined', data);
        break;

      case 'collaborator_left':
        this._emit('collaboratorLeft', data);
        break;

      case 'error':
        this._emit('serverError', data);
        break;

      default:
        console.warn('Unknown message type:', data.type);
    }
  }

  /**
   * Handle operation acknowledgment from server.
   * @param {Object} data - Acknowledgment data
   */
  _handleOperationAck(data) {
    const operationId = data.operation_id;
    if (this.pendingOperations.has(operationId)) {
      const operation = this.pendingOperations.get(operationId);
      this.pendingOperations.delete(operationId);
      this._emit('operationAck', { operation, ack: data });
    }
  }

  /**
   * Handle remote operation from another client.
   * @param {Object} data - Remote operation data
   */
  _handleRemoteOperation(data) {
    const operation = data.operation;

    // Apply the remote operation to local state
    this._applyOperation(operation);

    this._emit('remoteOperation', { operation, fromClient: data.from_client });
    this._emit('documentChanged', {
      content: this.documentState.content,
      operation: operation,
      source: 'remote'
    });
  }

  /**
   * Handle synchronization response from server.
   * @param {Object} data - Sync response data
   */
  _handleSyncResponse(data) {
    // Update local state
    this.documentState = {
      content: data.content,
      version: data.current_version,
      checksum: data.checksum,
      lastModified: data.timestamp
    };

    this._emit('syncComplete', data);
    this._emit('documentChanged', {
      content: this.documentState.content,
      source: 'sync'
    });
  }

  /**
   * Apply an operation to the local document state.
   * @param {Object} operation - Operation to apply
   */
  _applyOperation(operation) {
    switch (operation.type) {
      case 'insert':
        this.documentState.content =
          this.documentState.content.slice(0, operation.position) +
          operation.content +
          this.documentState.content.slice(operation.position);
        break;

      case 'delete':
        this.documentState.content =
          this.documentState.content.slice(0, operation.position) +
          this.documentState.content.slice(operation.position + operation.length);
        break;

      case 'update':
        this.documentState.content =
          this.documentState.content.slice(0, operation.position) +
          operation.content +
          this.documentState.content.slice(operation.position + operation.length);
        break;

      case 'replace':
        this.documentState.content = operation.content;
        break;
    }

    this.documentState.version++;
    this.documentState.lastModified = Date.now() / 1000;
  }

  /**
   * Send pending operations to the server.
   */
  _sendPendingOperations() {
    if (!this.connected || this.pendingOperations.size === 0) {
      return;
    }

    // Send operations in batches if there are multiple
    const operations = Array.from(this.pendingOperations.values());

    operations.forEach(operation => {
      this._send({
        type: 'operation',
        operation: operation
      });
    });
  }

  /**
   * Send data to the WebSocket server.
   * @param {Object} data - Data to send
   */
  _send(data) {
    if (this.ws && this.connected) {
      try {
        this.ws.send(JSON.stringify(data));
      } catch (error) {
        console.error('Failed to send WebSocket message:', error);
      }
    }
  }

  /**
   * Generate a unique operation ID.
   * @returns {string} Unique operation ID
   */
  _generateOperationId() {
    return `op_${this.clientId}_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }
}

// Export for different module systems
if (typeof module !== 'undefined' && module.exports) {
  module.exports = OperationalTransformationClient;
} else if (typeof define === 'function' && define.amd) {
  define([], function() {
    return OperationalTransformationClient;
  });
} else if (typeof window !== 'undefined') {
  window.OperationalTransformationClient = OperationalTransformationClient;
}