"""
Professional styling for PDF Watermark Cleaner Pro
Complete theme system with Light and Dark modes
"""

# Light Theme Colors
LIGHT_THEME = {
    'primary': '#2196F3',
    'primary_dark': '#1976D2',
    'primary_light': '#BBDEFB',
    'success': '#4CAF50',
    'success_dark': '#388E3C',
    'warning': '#FF9800',
    'warning_dark': '#F57C00',
    'error': '#F44336',
    'error_dark': '#D32F2F',
    'background': '#F5F5F5',
    'surface': '#FFFFFF',
    'text': '#212121',
    'text_secondary': '#757575',
    'border': '#E0E0E0',
    'hover': '#F0F0F0',
    'selection': '#E3F2FD'
}

# Dark Theme Colors
DARK_THEME = {
    'primary': '#90CAF9',
    'primary_dark': '#42A5F5',
    'primary_light': '#1976D2',
    'success': '#66BB6A',
    'success_dark': '#4CAF50',
    'warning': '#FFA726',
    'warning_dark': '#FF9800',
    'error': '#EF5350',
    'error_dark': '#F44336',
    'background': '#121212',
    'surface': '#1E1E1E',
    'text': '#FFFFFF',
    'text_secondary': '#B0B0B0',
    'border': '#333333',
    'hover': '#2A2A2A',
    'selection': '#1565C0'
}

# Current theme (default to light)
current_theme = LIGHT_THEME

def set_theme(theme_name: str):
    """Set the current theme"""
    global current_theme
    if theme_name.lower() == 'dark':
        current_theme = DARK_THEME
    else:
        current_theme = LIGHT_THEME

def get_stylesheet() -> str:
    """Returns the complete QSS stylesheet for current theme"""
    c = current_theme  # Shorthand
    
    return f"""
    /* Main Window */
    QMainWindow {{
        background-color: {c['background']};
        color: {c['text']};
    }}
    
    QWidget {{
        color: {c['text']};
    }}
    
    /* Menu Bar */
    QMenuBar {{
        background-color: {c['surface']};
        border-bottom: 1px solid {c['border']};
        padding: 4px;
        color: {c['text']};
    }}
    
    QMenuBar::item {{
        padding: 6px 12px;
        background: transparent;
        border-radius: 4px;
        color: {c['text']};
    }}
    
    QMenuBar::item:selected {{
        background-color: {c['hover']};
    }}
    
    QMenu {{
        background-color: {c['surface']};
        border: 1px solid {c['border']};
        padding: 4px;
        color: {c['text']};
    }}
    
    QMenu::item {{
        padding: 6px 24px 6px 12px;
        border-radius: 4px;
    }}
    
    QMenu::item:selected {{
        background-color: {c['selection']};
    }}
    
    /* Buttons */
    QPushButton {{
        background-color: {c['primary']};
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
        font-weight: 500;
        min-width: 80px;
    }}
    
    QPushButton:hover {{
        background-color: {c['primary_dark']};
    }}
    
    QPushButton:pressed {{
        background-color: {c['primary_dark']};
        padding-top: 9px;
        padding-bottom: 7px;
    }}
    
    QPushButton:disabled {{
        background-color: {c['border']};
        color: {c['text_secondary']};
    }}
    
    /* Secondary Buttons */
    QPushButton[class="secondary"] {{
        background-color: {c['surface']};
        color: {c['text']};
        border: 1px solid {c['border']};
    }}
    
    QPushButton[class="secondary"]:hover {{
        background-color: {c['hover']};
    }}
    
    /* Success Button */
    QPushButton[class="success"] {{
        background-color: {c['success']};
        color: white;
    }}
    
    QPushButton[class="success"]:hover {{
        background-color: {c['success_dark']};
    }}
    
    /* Group Box */
    QGroupBox {{
        background-color: {c['surface']};
        border: 1px solid {c['border']};
        border-radius: 6px;
        margin-top: 12px;
        padding-top: 12px;
        font-weight: 500;
        color: {c['text']};
    }}
    
    QGroupBox::title {{
        subcontrol-origin: margin;
        subcontrol-position: top left;
        padding: 0 8px;
        color: {c['text']};
    }}
    
    /* Table Widget */
    QTableWidget {{
        background-color: {c['surface']};
        alternate-background-color: {c['background']};
        border: 1px solid {c['border']};
        border-radius: 4px;
        gridline-color: {c['border']};
        color: {c['text']};
    }}
    
    QTableWidget::item {{
        padding: 4px;
        color: {c['text']};
    }}
    
    QTableWidget::item:selected {{
        background-color: {c['selection']};
        color: {c['text']};
    }}
    
    QHeaderView::section {{
        background-color: {c['surface']};
        color: {c['text']};
        padding: 8px;
        border: none;
        border-bottom: 2px solid {c['primary']};
        font-weight: 600;
    }}
    
    /* Progress Bar */
    QProgressBar {{
        border: 1px solid {c['border']};
        border-radius: 4px;
        text-align: center;
        background-color: {c['surface']};
        height: 24px;
        color: {c['text']};
    }}
    
    QProgressBar::chunk {{
        background-color: {c['primary']};
        border-radius: 3px;
    }}
    
    /* Text Edit (Activity Log) */
    QTextEdit {{
        background-color: {c['surface']};
        border: 1px solid {c['border']};
        border-radius: 4px;
        padding: 8px;
        font-family: 'Consolas', 'Monaco', monospace;
        font-size: 9pt;
        color: {c['text']};
    }}
    
    /* Line Edit (Search) */
    QLineEdit {{
        background-color: {c['surface']};
        border: 1px solid {c['border']};
        border-radius: 4px;
        padding: 6px 12px;
        selection-background-color: {c['selection']};
        color: {c['text']};
    }}
    
    QLineEdit:focus {{
        border: 2px solid {c['primary']};
        padding: 5px 11px;
    }}
    
    /* Checkbox */
    QCheckBox {{
        spacing: 8px;
        color: {c['text']};
    }}
    
    QCheckBox::indicator {{
        width: 18px;
        height: 18px;
        border: 2px solid {c['border']};
        border-radius: 3px;
        background-color: {c['surface']};
    }}
    
    QCheckBox::indicator:checked {{
        background-color: {c['primary']};
        border-color: {c['primary']};
        image: url(none);
    }}
    
    QCheckBox::indicator:hover {{
        border-color: {c['primary']};
    }}
    
    /* Scrollbar */
    QScrollBar:vertical {{
        border: none;
        background: {c['background']};
        width: 12px;
        margin: 0;
    }}
    
    QScrollBar::handle:vertical {{
        background: {c['border']};
        min-height: 30px;
        border-radius: 6px;
    }}
    
    QScrollBar::handle:vertical:hover {{
        background: {c['text_secondary']};
    }}
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}
    
    QScrollBar:horizontal {{
        border: none;
        background: {c['background']};
        height: 12px;
        margin: 0;
    }}
    
    QScrollBar::handle:horizontal {{
        background: {c['border']};
        min-width: 30px;
        border-radius: 6px;
    }}
    
    QScrollBar::handle:horizontal:hover {{
        background: {c['text_secondary']};
    }}
    
    /* Status Bar */
    QStatusBar {{
        background-color: {c['surface']};
        border-top: 1px solid {c['border']};
        color: {c['text_secondary']};
    }}
    
    /* Label */
    QLabel {{
        color: {c['text']};
    }}
    
    QLabel[class="secondary"] {{
        color: {c['text_secondary']};
        font-size: 9pt;
    }}
    
    QLabel[class="title"] {{
        font-size: 14pt;
        font-weight: 600;
        color: {c['text']};
    }}
    
    /* Toolbar */
    QToolBar {{
        background-color: {c['surface']};
        border-bottom: 1px solid {c['border']};
        spacing: 8px;
        padding: 4px;
    }}
    
    QToolButton {{
        background-color: transparent;
        border: none;
        border-radius: 4px;
        padding: 6px;
        color: {c['text']};
    }}
    
    QToolButton:hover {{
        background-color: {c['hover']};
    }}
    
    QToolButton:pressed {{
        background-color: {c['border']};
    }}
    
    /* Tab Widget */
    QTabWidget::pane {{
        border: 1px solid {c['border']};
        background-color: {c['surface']};
    }}
    
    QTabBar::tab {{
        background-color: {c['background']};
        color: {c['text']};
        padding: 8px 16px;
        border: 1px solid {c['border']};
        border-bottom: none;
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;
    }}
    
    QTabBar::tab:selected {{
        background-color: {c['surface']};
        border-bottom: 2px solid {c['primary']};
    }}
    
    QTabBar::tab:hover {{
        background-color: {c['hover']};
    }}
    
    /* Spin Box */
    QSpinBox {{
        background-color: {c['surface']};
        border: 1px solid {c['border']};
        border-radius: 4px;
        padding: 4px;
        color: {c['text']};
    }}
    
    QSpinBox:focus {{
        border: 2px solid {c['primary']};
    }}
    
    /* Combo Box */
    QComboBox {{
        background-color: {c['surface']};
        border: 1px solid {c['border']};
        border-radius: 4px;
        padding: 4px 8px;
        color: {c['text']};
    }}
    
    QComboBox:focus {{
        border: 2px solid {c['primary']};
    }}
    
    QComboBox::drop-down {{
        border: none;
        width: 20px;
    }}
    
    QComboBox QAbstractItemView {{
        background-color: {c['surface']};
        border: 1px solid {c['border']};
        selection-background-color: {c['selection']};
        color: {c['text']};
    }}
    
    /* Dialog */
    QDialog {{
        background-color: {c['background']};
        color: {c['text']};
    }}
    """

def apply_stylesheet(app, theme='light'):
    """Apply the stylesheet to the application"""
    set_theme(theme)
    app.setStyleSheet(get_stylesheet())

def get_current_theme_name():
    """Get the name of the current theme"""
    return 'dark' if current_theme == DARK_THEME else 'light'
