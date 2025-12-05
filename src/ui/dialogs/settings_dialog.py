from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, 
                               QWidget, QLabel, QLineEdit, QPushButton, QCheckBox,
                               QSpinBox, QComboBox, QFormLayout, QGroupBox)
from PySide6.QtCore import Qt

class SettingsDialog(QDialog):
    """Settings dialog with multiple tabs"""
    
    def __init__(self, settings_manager, parent=None):
        super().__init__(parent)
        self.settings = settings_manager
        self.setWindowTitle("Settings")
        self.setMinimumSize(500, 400)
        self.setup_ui()
        self.load_settings()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Tab widget
        tabs = QTabWidget()
        tabs.addTab(self.create_general_tab(), "General")
        tabs.addTab(self.create_appearance_tab(), "Appearance")
        tabs.addTab(self.create_advanced_tab(), "Advanced")
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_reset = QPushButton("Reset to Defaults")
        btn_reset.setProperty("class", "secondary")
        btn_reset.clicked.connect(self.reset_settings)
        
        btn_cancel = QPushButton("Cancel")
        btn_cancel.setProperty("class", "secondary")
        btn_cancel.clicked.connect(self.reject)
        
        btn_save = QPushButton("Save")
        btn_save.setProperty("class", "success")
        btn_save.clicked.connect(self.save_settings)
        
        btn_layout.addWidget(btn_reset)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_save)
        
        layout.addWidget(tabs)
        layout.addLayout(btn_layout)
        
    def create_general_tab(self):
        widget = QWidget()
        layout = QFormLayout(widget)
        
        # Output naming
        self.txt_output_template = QLineEdit()
        self.txt_output_template.setPlaceholderText("e.g., cleaned_{original}")
        layout.addRow("Output Template:", self.txt_output_template)
        
        # Save location
        self.cmb_save_location = QComboBox()
        self.cmb_save_location.addItems(["Same Directory", "Choose Directory"])
        layout.addRow("Save Location:", self.cmb_save_location)
        
        # Auto-scan
        self.chk_auto_scan = QCheckBox("Automatically scan files when added")
        layout.addRow("", self.chk_auto_scan)
        
        return widget
    
    def create_appearance_tab(self):
        widget = QWidget()
        layout = QFormLayout(widget)
        
        # Theme
        self.cmb_theme = QComboBox()
        self.cmb_theme.addItems(["Light", "Dark (Coming Soon)"])
        layout.addRow("Theme:", self.cmb_theme)
        
        # Font size
        self.spin_font_size = QSpinBox()
        self.spin_font_size.setRange(8, 16)
        self.spin_font_size.setValue(10)
        layout.addRow("Font Size:", self.spin_font_size)
        
        # Activity log visibility
        self.chk_activity_log = QCheckBox("Show activity log")
        layout.addRow("", self.chk_activity_log)
        
        # Statistics visibility
        self.chk_statistics = QCheckBox("Show statistics bar")
        layout.addRow("", self.chk_statistics)
        
        return widget
    
    def create_advanced_tab(self):
        widget = QWidget()
        layout = QFormLayout(widget)
        
        # Thread count
        self.spin_threads = QSpinBox()
        self.spin_threads.setRange(1, 16)
        self.spin_threads.setValue(4)
        layout.addRow("Worker Threads:", self.spin_threads)
        
        # Log level
        self.cmb_log_level = QComboBox()
        self.cmb_log_level.addItems(["DEBUG", "INFO", "WARNING", "ERROR"])
        layout.addRow("Log Level:", self.cmb_log_level)
        
        return widget
    
    def load_settings(self):
        """Load current settings into UI"""
        self.txt_output_template.setText(self.settings.get('output_template', 'cleaned_{original}'))
        self.chk_auto_scan.setChecked(True)
        self.chk_activity_log.setChecked(self.settings.get('activity_log_visible', True))
        self.chk_statistics.setChecked(self.settings.get('statistics_visible', True))
        self.spin_font_size.setValue(self.settings.get('font_size', 10))
        self.spin_threads.setValue(self.settings.get('thread_count', 4))
        
        log_level = self.settings.get('log_level', 'INFO')
        index = self.cmb_log_level.findText(log_level)
        if index >= 0:
            self.cmb_log_level.setCurrentIndex(index)
    
    def save_settings(self):
        """Save settings and close"""
        self.settings.set('output_template', self.txt_output_template.text())
        self.settings.set('activity_log_visible', self.chk_activity_log.isChecked())
        self.settings.set('statistics_visible', self.chk_statistics.isChecked())
        self.settings.set('font_size', self.spin_font_size.value())
        self.settings.set('thread_count', self.spin_threads.value())
        self.settings.set('log_level', self.cmb_log_level.currentText())
        
        self.accept()
    
    def reset_settings(self):
        """Reset to default settings"""
        self.settings.reset()
        self.load_settings()
