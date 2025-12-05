from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QTextCursor, QColor
from datetime import datetime
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.models.enums import LogLevel, LOG_COLORS, LOG_PREFIXES

class ActivityLog(QWidget):
    """Activity log widget with color-coded, timestamped messages"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.auto_scroll = True
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        header = QHBoxLayout()
        title = QLabel("Activity Log")
        title.setProperty("class", "title")
        
        self.btn_auto_scroll = QPushButton("Auto-scroll: ON")
        self.btn_auto_scroll.setProperty("class", "secondary")
        self.btn_auto_scroll.setMaximumWidth(120)
        self.btn_auto_scroll.clicked.connect(self.toggle_auto_scroll)
        
        self.btn_clear = QPushButton("Clear")
        self.btn_clear.setProperty("class", "secondary")
        self.btn_clear.setMaximumWidth(80)
        self.btn_clear.clicked.connect(self.clear)
        
        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.btn_auto_scroll)
        header.addWidget(self.btn_clear)
        
        # Text area
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setMaximumHeight(200)
        
        layout.addLayout(header)
        layout.addWidget(self.text_edit)
        
    def log(self, level: LogLevel, message: str):
        """Add a log message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = LOG_PREFIXES.get(level, "")
        color = LOG_COLORS.get(level, "#000000")
        
        # Format message
        formatted = f'<span style="color: {color};">[{timestamp}] {prefix} {message}</span>'
        
        # Append to log
        self.text_edit.append(formatted)
        
        # Auto-scroll
        if self.auto_scroll:
            cursor = self.text_edit.textCursor()
            cursor.movePosition(QTextCursor.End)
            self.text_edit.setTextCursor(cursor)
    
    def info(self, message: str):
        self.log(LogLevel.INFO, message)
    
    def success(self, message: str):
        self.log(LogLevel.SUCCESS, message)
    
    def warning(self, message: str):
        self.log(LogLevel.WARNING, message)
    
    def error(self, message: str):
        self.log(LogLevel.ERROR, message)
    
    def debug(self, message: str):
        self.log(LogLevel.DEBUG, message)
    
    def toggle_auto_scroll(self):
        self.auto_scroll = not self.auto_scroll
        status = "ON" if self.auto_scroll else "OFF"
        self.btn_auto_scroll.setText(f"Auto-scroll: {status}")
    
    def clear(self):
        self.text_edit.clear()
        self.info("Log cleared")
