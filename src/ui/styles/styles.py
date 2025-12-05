"""
Professional styling for PDF Watermark Cleaner Pro
Modern, clean design with Material Design principles
"""

# Color Palette
COLORS = {
    'primary': '#2196F3',
    'primary_dark': '#1976D2',
    'primary_light': '#BBDEFB',
    'success': '#4CAF50',
    'success_dark': '#388E3C',
    'warning': '#FF9800',
    'warning_dark': '#F57C00',
    'error': '#F44336',
    'error_dark': '#D32F2F',
    'background': '#FAFAFA',
    'surface': '#FFFFFF',
    'text': '#212121',
    'text_secondary': '#757575',
    'border': '#E0E0E0',
    'hover': '#F5F5F5'
}

def get_stylesheet() -> str:
    """Returns the complete QSS stylesheet"""
    return f"""
    /* Main Window */
    QMainWindow {{
        background-color: {COLORS['background']};
    }}
    
    /* Menu Bar */
    QMenuBar {{
        background-color: {COLORS['surface']};
        border-bottom: 1px solid {COLORS['border']};
        padding: 4px;
    }}
    
    QMenuBar::item {{
        padding: 6px 12px;
        background: transparent;
        border-radius: 4px;
    }}
    
    QMenuBar::item:selected {{
        background-color: {COLORS['hover']};
    }}
    
    QMenu {{
        background-color: {COLORS['surface']};
        border: 1px solid {COLORS['border']};
        padding: 4px;
    }}
    
    QMenu::item {{
        padding: 6px 24px 6px 12px;
        border-radius: 4px;
    }}
    
    QMenu::item:selected {{
        background-color: {COLORS['primary_light']};
    }}
    
    /* Buttons */
    QPushButton {{
        background-color: {COLORS['primary']};
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
        font-weight: 500;
        min-width: 80px;
    }}
    
    QPushButton:hover {{
        background-color: {COLORS['primary_dark']};
    }}
    
    QPushButton:pressed {{
        background-color: {COLORS['primary_dark']};
        padding-top: 9px;
        padding-bottom: 7px;
    }}
    
    QPushButton:disabled {{
        background-color: {COLORS['border']};
        color: {COLORS['text_secondary']};
    }}
    
    /* Secondary Buttons */
    QPushButton[class="secondary"] {{
        background-color: {COLORS['surface']};
        color: {COLORS['text']};
        border: 1px solid {COLORS['border']};
    }}
    
    QPushButton[class="secondary"]:hover {{
        background-color: {COLORS['hover']};
    }}
    
    /* Success Button */
    QPushButton[class="success"] {{
        background-color: {COLORS['success']};
    }}
    
    QPushButton[class="success"]:hover {{
        background-color: {COLORS['success_dark']};
    }}
    
    /* Group Box */
    QGroupBox {{
        background-color: {COLORS['surface']};
        border: 1px solid {COLORS['border']};
        border-radius: 6px;
        margin-top: 12px;
        padding-top: 12px;
        font-weight: 500;
    }}
    
    QGroupBox::title {{
        subcontrol-origin: margin;
        subcontrol-position: top left;
        padding: 0 8px;
        color: {COLORS['text']};
    }}
    
    /* Table Widget */
    QTableWidget {{
        background-color: {COLORS['surface']};
        alternate-background-color: {COLORS['background']};
        border: 1px solid {COLORS['border']};
        border-radius: 4px;
        gridline-color: {COLORS['border']};
    }}
    
    QTableWidget::item {{
        padding: 4px;
    }}
    
    QTableWidget::item:selected {{
        background-color: {COLORS['primary_light']};
        color: {COLORS['text']};
    }}
    
    QHeaderView::section {{
        background-color: {COLORS['surface']};
        color: {COLORS['text']};
        padding: 8px;
        border: none;
        border-bottom: 2px solid {COLORS['primary']};
        font-weight: 600;
    }}
    
    /* Progress Bar */
    QProgressBar {{
        border: 1px solid {COLORS['border']};
        border-radius: 4px;
        text-align: center;
        background-color: {COLORS['surface']};
        height: 24px;
    }}
    
    QProgressBar::chunk {{
        background-color: {COLORS['primary']};
        border-radius: 3px;
    }}
    
    /* Text Edit (Activity Log) */
    QTextEdit {{
        background-color: {COLORS['surface']};
        border: 1px solid {COLORS['border']};
        border-radius: 4px;
        padding: 8px;
        font-family: 'Consolas', 'Monaco', monospace;
        font-size: 9pt;
    }}
    
    /* Line Edit (Search) */
    QLineEdit {{
        background-color: {COLORS['surface']};
        border: 1px solid {COLORS['border']};
        border-radius: 4px;
        padding: 6px 12px;
        selection-background-color: {COLORS['primary_light']};
    }}
    
    QLineEdit:focus {{
        border: 2px solid {COLORS['primary']};
        padding: 5px 11px;
    }}
    
    /* Checkbox */
    QCheckBox {{
        spacing: 8px;
    }}
    
    QCheckBox::indicator {{
        width: 18px;
        height: 18px;
        border: 2px solid {COLORS['border']};
        border-radius: 3px;
        background-color: {COLORS['surface']};
    }}
    
    QCheckBox::indicator:checked {{
        background-color: {COLORS['primary']};
        border-color: {COLORS['primary']};
        image: url(none);
    }}
    
    QCheckBox::indicator:hover {{
        border-color: {COLORS['primary']};
    }}
    
    /* Scrollbar */
    QScrollBar:vertical {{
        border: none;
        background: {COLORS['background']};
        width: 12px;
        margin: 0;
    }}
    
    QScrollBar::handle:vertical {{
        background: {COLORS['border']};
        min-height: 30px;
        border-radius: 6px;
    }}
    
    QScrollBar::handle:vertical:hover {{
        background: {COLORS['text_secondary']};
    }}
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}
    
    QScrollBar:horizontal {{
        border: none;
        background: {COLORS['background']};
        height: 12px;
        margin: 0;
    }}
    
    QScrollBar::handle:horizontal {{
        background: {COLORS['border']};
        min-width: 30px;
        border-radius: 6px;
    }}
    
    QScrollBar::handle:horizontal:hover {{
        background: {COLORS['text_secondary']};
    }}
    
    /* Status Bar */
    QStatusBar {{
        background-color: {COLORS['surface']};
        border-top: 1px solid {COLORS['border']};
        color: {COLORS['text_secondary']};
    }}
    
    /* Label */
    QLabel {{
        color: {COLORS['text']};
    }}
    
    QLabel[class="secondary"] {{
        color: {COLORS['text_secondary']};
        font-size: 9pt;
    }}
    
    QLabel[class="title"] {{
        font-size: 14pt;
        font-weight: 600;
        color: {COLORS['text']};
    }}
    
    /* Toolbar */
    QToolBar {{
        background-color: {COLORS['surface']};
        border-bottom: 1px solid {COLORS['border']};
        spacing: 8px;
        padding: 4px;
    }}
    
    QToolButton {{
        background-color: transparent;
        border: none;
        border-radius: 4px;
        padding: 6px;
    }}
    
    QToolButton:hover {{
        background-color: {COLORS['hover']};
    }}
    
    QToolButton:pressed {{
        background-color: {COLORS['border']};
    }}
    """

def apply_stylesheet(app):
    """Apply the stylesheet to the application"""
    app.setStyleSheet(get_stylesheet())
