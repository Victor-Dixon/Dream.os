# conversation_viewer.py
# Conversation history viewer for Dream.OS GUI demo

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class ConversationViewer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        layout.addWidget(QLabel('Conversation Viewer'))
        self.setLayout(layout) 