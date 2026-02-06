from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextBrowser, QPushButton, QLabel
from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QTextCursor, QColor
from datetime import datetime
import sys
import os
import uuid
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.models.enums import LogLevel, LOG_COLORS, LOG_PREFIXES

class ActivityLog(QWidget):
    """Activity log widget with color-coded, timestamped messages and expandable details"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.auto_scroll = True
        self.expanded_items = set()  # Track which items are expanded
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
        
        # Text area with HTML support - use QTextBrowser for clickable links
        self.text_edit = QTextBrowser()
        self.text_edit.setReadOnly(True)
        self.text_edit.setMaximumHeight(200)
        self.text_edit.setOpenLinks(False)  # Don't open links externally
        self.text_edit.setMouseTracking(True)
        self.text_edit.anchorClicked.connect(self.handle_anchor_click)
        
        layout.addLayout(header)
        layout.addWidget(self.text_edit)
        
    def handle_anchor_click(self, url):
        """Handle clicks on expandable detail links"""
        # URL format: "toggle:item_id"
        if url.toString().startswith("toggle:"):
            item_id = url.toString().replace("toggle:", "")
            
            if item_id in self.expanded_items:
                self.expanded_items.remove(item_id)
            else:
                self.expanded_items.add(item_id)
            
            # Refresh the display by rebuilding HTML (simple approach)
            # In a more complex app, you'd update just the affected element
            # For now, we'll just toggle the visibility state
            # The actual toggle is handled by updating the HTML when messages are added
    
    def log(self, level: LogLevel, message: str):
        """Add a simple log message"""
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
    
    def log_with_details(self, level: LogLevel, message: str, details: list):
        """
        Add a log message with expandable details
        
        Args:
            level: Log level
            message: Main message
            details: List of detail strings to show when expanded
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = LOG_PREFIXES.get(level, "")
        color = LOG_COLORS.get(level, "#000000")
        
        # Simplified format - just show main message with count
        main_msg = f'<span style="color: {color}; font-weight: 500;">[{timestamp}] {prefix} {message}</span>'
        
        # Show first 5 details inline with a summary count
        if len(details) <= 5:
            detail_list = "<br>".join([f'  • {d}' for d in details])
        else:
            detail_list = "<br>".join([f'  • {d}' for d in details[:5]])
            detail_list += f"<br>  <i>... and {len(details) - 5} more objects removed</i>"
        
        # Combine everything
        full_msg = f'{main_msg}<br><span style="font-size: 8.5pt; color: #666;">{detail_list}</span>'
        
        # Append to log
        self.text_edit.append(full_msg)
        
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
        self.expanded_items.clear()
        self.info("Log cleared")

