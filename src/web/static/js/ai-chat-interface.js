/**
 * AI Chat Interface - Web Dashboard Integration
 * ============================================
 *
 * Real-time AI chat interface with Thea integration for project guidance,
 * code suggestions, and intelligent assistance.
 *
 * Features:
 * - Real-time chat with AI
 * - Code suggestions and analysis
 * - Context-aware responses
 * - Conversation memory
 * - Responsive design
 *
 * V2 Compliance: Modular design, error handling, accessibility
 * Author: Agent-7 (Web Development Specialist)
 * Date: 2026-01-07
 */

class AIChatInterface {
    constructor(options = {}) {
        this.container = options.container || document.body;
        this.endpoint = options.endpoint || '/api/ai/chat';
        this.contextEndpoint = options.contextEndpoint || '/api/ai/context';
        this.suggestionsEndpoint = options.suggestionsEndpoint || '/api/ai/code-suggestions';
        this.maxRetries = options.maxRetries || 3;
        this.retryDelay = options.retryDelay || 1000;

        this.conversationId = null;
        this.isTyping = false;
        this.messageHistory = [];
        this.context = {};

        this.init();
    }

    async init() {
        try {
            // Get AI capabilities and status
            const context = await this.getAIContext();

            // Create chat interface
            this.createChatInterface(context);

            // Load conversation history if available
            this.loadConversationHistory();

            // Bind events
            this.bindEvents();

            console.log('🤖 AI Chat Interface initialized');
        } catch (error) {
            console.error('Failed to initialize AI Chat Interface:', error);
            this.showFallbackInterface(error);
        }
    }

    async getAIContext() {
        try {
            const response = await fetch(this.contextEndpoint);
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return await response.json();
        } catch (error) {
            console.warn('Failed to get AI context, using defaults:', error);
            return {
                capabilities: ['Basic chat support'],
                status: 'limited',
                features: {
                    chat_interface: true,
                    code_suggestions: false,
                    context_awareness: false,
                    real_time_responses: false,
                    conversation_memory: false
                }
            };
        }
    }

    createChatInterface(context) {
        const chatHTML = `
            <div id="ai-chat-container" class="ai-chat-container" role="region" aria-label="AI Assistant Chat">
                <div class="ai-chat-header">
                    <div class="ai-chat-title">
                        <span class="ai-icon">🤖</span>
                        <span>AI Assistant</span>
                        <span class="ai-status ${context.status === 'operational' ? 'online' : 'offline'}"
                              title="${context.status === 'operational' ? 'Online' : 'Limited functionality'}"></span>
                    </div>
                    <div class="ai-chat-controls">
                        <button class="ai-chat-toggle" aria-label="Minimize chat">
                            <span class="minimize-icon">−</span>
                        </button>
                        <button class="ai-chat-close" aria-label="Close chat">
                            <span class="close-icon">×</span>
                        </button>
                    </div>
                </div>

                <div class="ai-chat-messages" role="log" aria-label="Chat messages">
                    <div class="ai-welcome-message">
                        <div class="ai-message ai-message-bot">
                            <div class="ai-avatar">🤖</div>
                            <div class="ai-message-content">
                                <p>Hello! I'm your AI assistant. I can help you with:</p>
                                <ul>
                                    ${context.capabilities.map(cap => `<li>${cap}</li>`).join('')}
                                </ul>
                                <p>How can I assist you today?</p>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="ai-chat-input-area">
                    <div class="ai-chat-suggestions" style="display: none;">
                        <div class="ai-suggestions-list"></div>
                    </div>

                    <div class="ai-chat-input-container">
                        <textarea
                            class="ai-chat-input"
                            placeholder="Ask me anything about your project..."
                            rows="1"
                            maxlength="2000"
                            aria-label="Type your message to AI assistant"
                        ></textarea>
                        <button class="ai-chat-send" disabled aria-label="Send message">
                            <span class="send-icon">➤</span>
                        </button>
                    </div>

                    <div class="ai-chat-actions">
                        <button class="ai-action-code" title="Get code suggestions">
                            <span class="code-icon">⟨⟩</span> Code
                        </button>
                        <button class="ai-action-context" title="Update context">
                            <span class="context-icon">📋</span> Context
                        </button>
                        <button class="ai-action-clear" title="Clear conversation">
                            <span class="clear-icon">🗑️</span> Clear
                        </button>
                    </div>
                </div>
            </div>
        `;

        // Add CSS
        this.addStyles();

        // Insert into container
        this.container.insertAdjacentHTML('beforeend', chatHTML);

        // Cache DOM elements
        this.cacheElements();
    }

    addStyles() {
        if (document.getElementById('ai-chat-styles')) return;

        const styles = `
            <style id="ai-chat-styles">
                .ai-chat-container {
                    position: fixed;
                    bottom: 20px;
                    right: 20px;
                    width: 380px;
                    height: 600px;
                    background: white;
                    border-radius: 12px;
                    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
                    display: flex;
                    flex-direction: column;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    z-index: 10000;
                    overflow: hidden;
                    transition: all 0.3s ease;
                }

                .ai-chat-header {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 16px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }

                .ai-chat-title {
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    font-weight: 600;
                }

                .ai-status {
                    width: 8px;
                    height: 8px;
                    border-radius: 50%;
                    background: #28a745;
                }

                .ai-status.offline {
                    background: #ffc107;
                }

                .ai-chat-controls {
                    display: flex;
                    gap: 8px;
                }

                .ai-chat-toggle, .ai-chat-close {
                    background: rgba(255,255,255,0.2);
                    border: none;
                    color: white;
                    width: 32px;
                    height: 32px;
                    border-radius: 6px;
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 16px;
                    transition: background-color 0.2s;
                }

                .ai-chat-toggle:hover, .ai-chat-close:hover {
                    background: rgba(255,255,255,0.3);
                }

                .ai-chat-messages {
                    flex: 1;
                    overflow-y: auto;
                    padding: 16px;
                    background: #f8f9fa;
                }

                .ai-message {
                    display: flex;
                    margin-bottom: 16px;
                    max-width: 85%;
                }

                .ai-message-user {
                    margin-left: auto;
                    flex-direction: row-reverse;
                }

                .ai-avatar {
                    width: 36px;
                    height: 36px;
                    border-radius: 18px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 16px;
                    flex-shrink: 0;
                    margin: 0 12px;
                }

                .ai-message-user .ai-avatar {
                    background: #007bff;
                    color: white;
                }

                .ai-message-bot .ai-avatar {
                    background: #e9ecef;
                    color: #495057;
                }

                .ai-message-content {
                    background: white;
                    padding: 12px 16px;
                    border-radius: 18px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                    line-height: 1.4;
                }

                .ai-message-user .ai-message-content {
                    background: #007bff;
                    color: white;
                }

                .ai-typing {
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    color: #6c757d;
                    font-style: italic;
                }

                .ai-chat-input-area {
                    border-top: 1px solid #e9ecef;
                    background: white;
                }

                .ai-chat-input-container {
                    display: flex;
                    padding: 16px;
                    gap: 8px;
                    align-items: flex-end;
                }

                .ai-chat-input {
                    flex: 1;
                    border: 2px solid #e9ecef;
                    border-radius: 24px;
                    padding: 12px 16px;
                    font-size: 14px;
                    resize: none;
                    outline: none;
                    transition: border-color 0.2s;
                    max-height: 120px;
                    min-height: 20px;
                }

                .ai-chat-input:focus {
                    border-color: #007bff;
                }

                .ai-chat-send {
                    width: 44px;
                    height: 44px;
                    border-radius: 22px;
                    background: #007bff;
                    border: none;
                    color: white;
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 18px;
                    transition: background-color 0.2s;
                }

                .ai-chat-send:hover:not(:disabled) {
                    background: #0056b3;
                }

                .ai-chat-send:disabled {
                    background: #6c757d;
                    cursor: not-allowed;
                }

                .ai-chat-actions {
                    display: flex;
                    justify-content: center;
                    gap: 12px;
                    padding: 8px 16px 16px;
                    border-top: 1px solid #e9ecef;
                }

                .ai-action-code, .ai-action-context, .ai-action-clear {
                    padding: 8px 12px;
                    border: 1px solid #dee2e6;
                    background: white;
                    border-radius: 6px;
                    cursor: pointer;
                    font-size: 12px;
                    transition: all 0.2s;
                    display: flex;
                    align-items: center;
                    gap: 4px;
                }

                .ai-action-code:hover, .ai-action-context:hover, .ai-action-clear:hover {
                    background: #f8f9fa;
                    border-color: #adb5bd;
                }

                .ai-chat-suggestions {
                    border-top: 1px solid #e9ecef;
                    background: #f8f9fa;
                }

                .ai-suggestions-list {
                    display: flex;
                    flex-wrap: wrap;
                    gap: 8px;
                    padding: 12px 16px;
                }

                .ai-suggestion-chip {
                    background: #007bff;
                    color: white;
                    padding: 6px 12px;
                    border-radius: 16px;
                    font-size: 12px;
                    cursor: pointer;
                    transition: background-color 0.2s;
                }

                .ai-suggestion-chip:hover {
                    background: #0056b3;
                }

                @media (max-width: 480px) {
                    .ai-chat-container {
                        width: calc(100vw - 40px);
                        height: calc(100vh - 40px);
                        bottom: 20px;
                        right: 20px;
                    }
                }

                /* Accessibility */
                .ai-chat-container:focus-within {
                    box-shadow: 0 8px 32px rgba(0,123,255,0.3);
                }

                /* Dark mode support */
                @media (prefers-color-scheme: dark) {
                    .ai-chat-container {
                        background: #2d3748;
                        color: #e2e8f0;
                    }

                    .ai-chat-messages {
                        background: #1a202c;
                    }

                    .ai-message-content {
                        background: #4a5568;
                        color: #e2e8f0;
                    }
                }
            </style>
        `;

        document.head.insertAdjacentHTML('beforeend', styles);
    }

    cacheElements() {
        this.chatContainer = document.getElementById('ai-chat-container');
        this.messagesContainer = this.chatContainer.querySelector('.ai-chat-messages');
        this.inputElement = this.chatContainer.querySelector('.ai-chat-input');
        this.sendButton = this.chatContainer.querySelector('.ai-chat-send');
        this.toggleButton = this.chatContainer.querySelector('.ai-chat-toggle');
        this.closeButton = this.chatContainer.querySelector('.ai-chat-close');
        this.suggestionsContainer = this.chatContainer.querySelector('.ai-chat-suggestions');
        this.suggestionsList = this.chatContainer.querySelector('.ai-suggestions-list');
        this.actionButtons = {
            code: this.chatContainer.querySelector('.ai-action-code'),
            context: this.chatContainer.querySelector('.ai-action-context'),
            clear: this.chatContainer.querySelector('.ai-action-clear')
        };
    }

    bindEvents() {
        // Send message events
        this.inputElement.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        this.inputElement.addEventListener('input', () => {
            this.updateSendButton();
            this.autoResizeTextarea();
        });

        this.sendButton.addEventListener('click', () => this.sendMessage());

        // Control events
        this.toggleButton.addEventListener('click', () => this.toggleChat());
        this.closeButton.addEventListener('click', () => this.closeChat());

        // Action events
        this.actionButtons.code.addEventListener('click', () => this.requestCodeSuggestions());
        this.actionButtons.context.addEventListener('click', () => this.updateContext());
        this.actionButtons.clear.addEventListener('click', () => this.clearConversation());

        // Click outside to close suggestions
        document.addEventListener('click', (e) => {
            if (!this.suggestionsContainer.contains(e.target)) {
                this.hideSuggestions();
            }
        });

        // Update context periodically
        setInterval(() => this.updateContext(), 30000); // Every 30 seconds
    }

    async sendMessage() {
        const message = this.inputElement.value.trim();
        if (!message || this.isTyping) return;

        // Add user message to chat
        this.addMessage(message, 'user');

        // Clear input
        this.inputElement.value = '';
        this.updateSendButton();
        this.autoResizeTextarea();

        // Show typing indicator
        this.showTypingIndicator();

        try {
            // Send to AI
            const response = await this.sendToAI(message);

            // Hide typing indicator
            this.hideTypingIndicator();

            // Add AI response
            this.addMessage(response.response, 'bot', response.suggestions);

            // Store conversation ID
            this.conversationId = response.conversation_id;

            // Show suggestions if available
            if (response.suggestions && response.suggestions.length > 0) {
                this.showSuggestions(response.suggestions);
            }

        } catch (error) {
            console.error('Failed to send message:', error);
            this.hideTypingIndicator();
            this.addMessage('Sorry, I encountered an error. Please try again.', 'bot');
        }
    }

    async sendToAI(message) {
        const payload = {
            message: message,
            context: this.context,
            conversation_id: this.conversationId
        };

        let retries = 0;
        while (retries < this.maxRetries) {
            try {
                const response = await fetch(this.endpoint, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(payload)
                });

                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }

                return await response.json();

            } catch (error) {
                retries++;
                if (retries >= this.maxRetries) {
                    throw error;
                }

                // Wait before retry
                await new Promise(resolve => setTimeout(resolve, this.retryDelay * retries));
            }
        }
    }

    addMessage(content, sender, suggestions = null) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `ai-message ai-message-${sender}`;

        const avatar = sender === 'user' ? '👤' : '🤖';
        const avatarClass = sender === 'user' ? 'user' : 'bot';

        messageDiv.innerHTML = `
            <div class="ai-avatar">${avatar}</div>
            <div class="ai-message-content">
                ${this.formatMessage(content)}
                ${suggestions ? this.formatSuggestions(suggestions) : ''}
            </div>
        `;

        this.messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();

        // Store in history
        this.messageHistory.push({
            content,
            sender,
            timestamp: Date.now(),
            suggestions
        });
    }

    formatMessage(content) {
        // Basic markdown-like formatting
        return content
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/`([^`]+)`/g, '<code>$1</code>')
            .replace(/\n/g, '<br>');
    }

    formatSuggestions(suggestions) {
        if (!suggestions || suggestions.length === 0) return '';

        const suggestionsHTML = suggestions.map(suggestion =>
            `<button class="ai-suggestion-chip" onclick="aiChat.useSuggestion('${suggestion.replace(/'/g, "\\'")}')">${suggestion}</button>`
        ).join('');

        return `<div class="ai-message-suggestions">${suggestionsHTML}</div>`;
    }

    useSuggestion(suggestion) {
        this.inputElement.value = suggestion;
        this.updateSendButton();
        this.inputElement.focus();
        this.hideSuggestions();
    }

    showTypingIndicator() {
        this.isTyping = true;
        const typingDiv = document.createElement('div');
        typingDiv.className = 'ai-message ai-message-bot ai-typing-indicator';
        typingDiv.innerHTML = `
            <div class="ai-avatar">🤖</div>
            <div class="ai-message-content ai-typing">
                <span>AI is thinking</span>
                <div class="typing-dots">
                    <span></span><span></span><span></span>
                </div>
            </div>
        `;

        this.messagesContainer.appendChild(typingDiv);
        this.scrollToBottom();
    }

    hideTypingIndicator() {
        this.isTyping = false;
        const typingIndicator = this.messagesContainer.querySelector('.ai-typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    showSuggestions(suggestions) {
        this.suggestionsList.innerHTML = suggestions.map(suggestion =>
            `<button class="ai-suggestion-chip" onclick="aiChat.useSuggestion('${suggestion.replace(/'/g, "\\'")}')">${suggestion}</button>`
        ).join('');

        this.suggestionsContainer.style.display = 'block';
    }

    hideSuggestions() {
        this.suggestionsContainer.style.display = 'none';
    }

    async requestCodeSuggestions() {
        const code = window.getSelection().toString();

        if (!code) {
            this.addMessage('Please select some code first, then click the Code button to get suggestions.', 'bot');
            return;
        }

        this.showTypingIndicator();

        try {
            const response = await this.getCodeSuggestions(code);

            this.hideTypingIndicator();

            let responseText = `**Code Analysis Results:**\n\n${response.explanation}\n\n**Key Improvements:**\n`;
            response.improvements.forEach(improvement => {
                responseText += `• ${improvement}\n`;
            });

            this.addMessage(responseText, 'bot', ['Apply suggestions', 'Show detailed analysis', 'Ask for implementation']);

        } catch (error) {
            console.error('Code suggestions failed:', error);
            this.hideTypingIndicator();
            this.addMessage('Sorry, I couldn\'t analyze the code right now. Please try again.', 'bot');
        }
    }

    async getCodeSuggestions(code) {
        const payload = {
            code: code,
            language: 'javascript', // Could be detected
            context: 'Web dashboard code analysis'
        };

        const response = await fetch(this.suggestionsEndpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        return await response.json();
    }

    updateContext() {
        // Update context with current page information
        this.context = {
            current_page: window.location.pathname,
            user_agent: navigator.userAgent,
            timestamp: Date.now(),
            dashboard_state: this.getDashboardState(),
            project_context: {
                domain: 'web',
                component: 'ai_chat_interface',
                version: '2.0.0'
            }
        };
    }

    getDashboardState() {
        // Get current dashboard state for context
        try {
            const activeTab = document.querySelector('.tab-active');
            const activeSection = document.querySelector('.section-active');

            return {
                active_tab: activeTab ? activeTab.dataset.tab : null,
                active_section: activeSection ? activeSection.id : null,
                has_errors: document.querySelectorAll('.error').length > 0,
                performance_metrics: performance.getEntriesByType('navigation')[0]
            };
        } catch (error) {
            return { error: 'Could not determine dashboard state' };
        }
    }

    clearConversation() {
        if (confirm('Are you sure you want to clear the conversation?')) {
            // Keep welcome message
            const welcomeMessage = this.messagesContainer.querySelector('.ai-welcome-message');
            this.messagesContainer.innerHTML = '';
            if (welcomeMessage) {
                this.messagesContainer.appendChild(welcomeMessage);
            }

            this.messageHistory = [];
            this.conversationId = null;
            this.hideSuggestions();
        }
    }

    toggleChat() {
        const isMinimized = this.chatContainer.classList.contains('minimized');

        if (isMinimized) {
            this.chatContainer.classList.remove('minimized');
            this.chatContainer.style.height = '600px';
            this.toggleButton.innerHTML = '<span class="minimize-icon">−</span>';
            this.toggleButton.setAttribute('aria-label', 'Minimize chat');
        } else {
            this.chatContainer.classList.add('minimized');
            this.chatContainer.style.height = 'auto';
            this.toggleButton.innerHTML = '<span class="minimize-icon">+</span>';
            this.toggleButton.setAttribute('aria-label', 'Maximize chat');
        }
    }

    closeChat() {
        if (confirm('Are you sure you want to close the AI chat?')) {
            this.chatContainer.remove();
        }
    }

    updateSendButton() {
        const hasText = this.inputElement.value.trim().length > 0;
        this.sendButton.disabled = !hasText;
    }

    autoResizeTextarea() {
        this.inputElement.style.height = 'auto';
        this.inputElement.style.height = Math.min(this.inputElement.scrollHeight, 120) + 'px';
    }

    scrollToBottom() {
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }

    loadConversationHistory() {
        try {
            const history = localStorage.getItem('ai_chat_history');
            if (history) {
                this.messageHistory = JSON.parse(history);
                // Restore recent messages (last 10)
                const recentMessages = this.messageHistory.slice(-10);
                recentMessages.forEach(msg => {
                    this.addMessage(msg.content, msg.sender, msg.suggestions);
                });
            }
        } catch (error) {
            console.warn('Failed to load conversation history:', error);
        }
    }

    saveConversationHistory() {
        try {
            localStorage.setItem('ai_chat_history', JSON.stringify(this.messageHistory));
        } catch (error) {
            console.warn('Failed to save conversation history:', error);
        }
    }

    showFallbackInterface(error) {
        const fallbackHTML = `
            <div id="ai-chat-fallback" style="
                position: fixed;
                bottom: 20px;
                right: 20px;
                background: #fff3cd;
                border: 1px solid #ffeaa7;
                border-radius: 8px;
                padding: 16px;
                max-width: 300px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                z-index: 10000;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            ">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                    <span style="font-size: 20px;">⚠️</span>
                    <strong>AI Chat Unavailable</strong>
                </div>
                <p style="margin: 0 0 12px 0; color: #856404;">
                    The AI assistant is currently unavailable. Please check that the Thea service is running.
                </p>
                <button onclick="this.parentElement.remove()" style="
                    background: #856404;
                    color: white;
                    border: none;
                    padding: 6px 12px;
                    border-radius: 4px;
                    cursor: pointer;
                    font-size: 12px;
                ">
                    Dismiss
                </button>
            </div>
        `;

        this.container.insertAdjacentHTML('beforeend', fallbackHTML);
    }
}

// Global instance
let aiChat;

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    aiChat = new AIChatInterface();
});

// Export for global access
window.AIChatInterface = AIChatInterface;
window.aiChat = aiChat;