#!/usr/bin/env python3
"""
Conversational AI Component
===========================

This component handles conversational AI functionality including:
- Chat interface
- Conversation management
- Quick actions
- AI responses
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QTextEdit, QLineEdit, QComboBox, QGroupBox, QGridLayout
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from dreamscape.core.memory_system import MemoryManager
from dreamscape.core.mmorpg.mmorpg_engine import MMORPGEngine
from dreamscape.gui.debug_handler import debug_button

logger = logging.getLogger(__name__)

class ConversationalAIComponent(QWidget):
    """Conversational AI component for chat interface and conversation management."""
    
    # Signals
    message_sent = pyqtSignal(str)  # Message sent to AI
    conversation_loaded = pyqtSignal(str)  # Conversation loaded
    quick_action_triggered = pyqtSignal(str)  # Quick action triggered
    
    def __init__(self, memory_manager: MemoryManager = None, mmorpg_engine: MMORPGEngine = None):
        super().__init__()
        self.memory_manager = memory_manager or MemoryManager()
        self.mmorpg_engine = mmorpg_engine or MMORPGEngine()
        
        # UI Components
        self.conversation_combo = None
        self.chat_history = None
        self.chat_input = None
        self.send_chat_btn = None
        self.load_conversations_btn = None
        
        # Quick action buttons
        self.analyze_btn = None
        self.suggest_btn = None
        self.explain_btn = None
        self.debug_btn = None
        
        self.init_ui()
        self.connect_signals()
    
    def init_ui(self):
        """Initialize the conversational AI user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Header
        header = QLabel("💬 Conversational AI - Chat with Your Work")
        header.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(header)
        
        # Conversation selection
        conv_group = QGroupBox("Select Conversation Context")
        conv_layout = QVBoxLayout(conv_group)
        
        self.conversation_combo = QComboBox()
        self.conversation_combo.addItem("Select a conversation...")
        conv_layout.addWidget(self.conversation_combo)
        
        self.load_conversations_btn = QPushButton("🔄 Load Recent Conversations")
        conv_layout.addWidget(self.load_conversations_btn)
        
        layout.addWidget(conv_group)
        
        # Chat interface
        chat_group = QGroupBox("AI Chat Interface")
        chat_layout = QVBoxLayout(chat_group)
        
        # Chat history
        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        self.chat_history.setMaximumHeight(300)
        chat_layout.addWidget(QLabel("Chat History:"))
        chat_layout.addWidget(self.chat_history)
        
        # Input area
        input_layout = QHBoxLayout()
        self.chat_input = QLineEdit()
        self.chat_input.setPlaceholderText("Ask the AI about your work...")
        input_layout.addWidget(self.chat_input)
        
        self.send_chat_btn = QPushButton("Send")
        input_layout.addWidget(self.send_chat_btn)
        
        chat_layout.addLayout(input_layout)
        layout.addWidget(chat_group)
        
        # Quick actions
        actions_group = QGroupBox("Quick Actions")
        actions_layout = QGridLayout(actions_group)
        
        self.analyze_btn = QPushButton("🔍 Analyze Current Work")
        actions_layout.addWidget(self.analyze_btn, 0, 0)
        
        self.suggest_btn = QPushButton("💡 Get Suggestions")
        actions_layout.addWidget(self.suggest_btn, 0, 1)
        
        self.explain_btn = QPushButton("📚 Explain Concepts")
        actions_layout.addWidget(self.explain_btn, 1, 0)
        
        self.debug_btn = QPushButton("🐛 Debug Help")
        actions_layout.addWidget(self.debug_btn, 1, 1)
        
        layout.addWidget(actions_group)
        layout.addStretch()
    
    def connect_signals(self):
        """Connect all signals and slots."""
        self.load_conversations_btn.clicked.connect(self.load_conversations)
        self.send_chat_btn.clicked.connect(self.send_chat_message)
        self.chat_input.returnPressed.connect(self.send_chat_message)
        
        # Quick actions
        self.analyze_btn.clicked.connect(lambda: self.quick_action_triggered.emit("analyze"))
        self.suggest_btn.clicked.connect(lambda: self.quick_action_triggered.emit("suggest"))
        self.explain_btn.clicked.connect(lambda: self.quick_action_triggered.emit("explain"))
        self.debug_btn.clicked.connect(lambda: self.quick_action_triggered.emit("debug"))
    
    @debug_button("load_conversations", "Conversational AI Component")
    def load_conversations(self):
        """Load recent conversations into the combo box."""
        try:
            # Clear existing items except the first one
            self.conversation_combo.clear()
            self.conversation_combo.addItem("Select a conversation...")
            
            # Load conversations from memory manager
            conversations = self.memory_manager.get_recent_conversations(limit=10)
            
            for conv in conversations:
                self.conversation_combo.addItem(conv.get('title', 'Untitled'), conv.get('id'))
            
            logger.info(f"Loaded {len(conversations)} conversations")
            
        except Exception as e:
            logger.error(f"Error loading conversations: {e}")
    
    @debug_button("send_chat_message", "Conversational AI Component")
    def send_chat_message(self):
        """Send a chat message to the AI."""
        message = self.chat_input.text().strip()
        if not message:
            return
        
        # Add message to chat history
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_history.append(f"[{timestamp}] You: {message}")
        
        # Clear input
        self.chat_input.clear()
        
        # Emit signal for AI processing
        self.message_sent.emit(message)
        
        logger.info(f"Sent chat message: {message[:50]}...")
    
    def add_ai_response(self, response: str):
        """Add AI response to chat history."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_history.append(f"[{timestamp}] AI: {response}")
    
    def clear_chat_history(self):
        """Clear the chat history."""
        self.chat_history.clear()
    
    def get_current_conversation_id(self) -> Optional[str]:
        """Get the currently selected conversation ID."""
        current_data = self.conversation_combo.currentData()
        return current_data if current_data else None
    
    def set_conversation_context(self, conversation_id: str, title: str):
        """Set the conversation context."""
        # Find and select the conversation
        for i in range(self.conversation_combo.count()):
            if self.conversation_combo.itemData(i) == conversation_id:
                self.conversation_combo.setCurrentIndex(i)
                break
    
    def get_chat_history_text(self) -> str:
        """Get the current chat history as text."""
        return self.chat_history.toPlainText()
    
    def is_input_empty(self) -> bool:
        """Check if the chat input is empty."""
        return not self.chat_input.text().strip()
    
    def focus_input(self):
        """Focus the chat input field."""
        self.chat_input.setFocus()
    
    def disable_input(self):
        """Disable the chat input during processing."""
        self.chat_input.setEnabled(False)
        self.send_chat_btn.setEnabled(False)
    
    def enable_input(self):
        """Enable the chat input after processing."""
        self.chat_input.setEnabled(True)
        self.send_chat_btn.setEnabled(True) 