from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFrame
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QPixmap, QDesktopServices, QFont
import os

class AboutDialog(QDialog):
    """About dialog showing application information"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About WaterMarkEraser")
        self.setFixedSize(550, 650)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # App logo
        logo_path = os.path.join(os.path.dirname(__file__), '..', '..', 'resources', 'logo.png')
        if os.path.exists(logo_path):
            logo_label = QLabel()
            pixmap = QPixmap(logo_path)
            scaled_pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
            logo_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(logo_label)
        
        # App name
        name = QLabel("WaterMarkEraser")
        name.setAlignment(Qt.AlignCenter)
        name.setStyleSheet("font-size: 24pt; font-weight: bold; color: #2196F3;")
        layout.addWidget(name)
        
        # Version
        version = QLabel("Version 1.0.0")
        version.setAlignment(Qt.AlignCenter)
        version.setStyleSheet("font-size: 10pt; color: #757575;")
        layout.addWidget(version)
        
        # Separator
        layout.addWidget(self._create_separator())
        
        # Description
        desc = QLabel(
            "WaterMarkEraser is a professional application for removing watermarks, links, "
            "and annotations from PDF files. It uses intelligent detection to safely eliminate "
            "repeated watermark elements while preserving the original document content. "
            "The application supports batch processing and features a clean, modern interface "
            "with Dark and Light themes."
        )
        desc.setWordWrap(True)
        desc.setAlignment(Qt.AlignCenter)
        desc.setStyleSheet("font-size: 10pt; padding: 10px;")
        layout.addWidget(desc)
        
        # Separator
        layout.addWidget(self._create_separator())
        
        # Developer section title
        dev_title = QLabel("Developer")
        dev_title.setAlignment(Qt.AlignCenter)
        from src.ui.styles.styles import current_theme
        dev_title.setStyleSheet(f"font-size: 14pt; font-weight: 600; color: {current_theme['primary']};")
        layout.addWidget(dev_title)
        
        # Developer photo
        dev_photo_path = os.path.join(os.path.dirname(__file__), '..', '..', 'resources', 'developer.jpg')
        if os.path.exists(dev_photo_path):
            photo_label = QLabel()
            photo_pixmap = QPixmap(dev_photo_path)
            scaled_photo = photo_pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            photo_label.setPixmap(scaled_photo)
            photo_label.setAlignment(Qt.AlignCenter)
            photo_label.setStyleSheet("border-radius: 60px; margin: 10px;")
            layout.addWidget(photo_label)
        
        # Developer name
        dev_name = QLabel("Raafat Shahin")
        dev_name.setAlignment(Qt.AlignCenter)
        dev_name.setText(
            "Developed by Raafat Shahin, WaterMarkEraser focuses on accuracy, "
            "performance, and a professional user experience."
        )
        dev_name.setWordWrap(True)
        dev_name.setStyleSheet("font-weight: 600; font-size: 11pt; margin-top: 10px;")
        layout.addWidget(dev_name)
        
        # Contact buttons
        contact_layout = QHBoxLayout()
        contact_layout.setSpacing(10)
        
        # WhatsApp button
        btn_whatsapp = QPushButton("📱 WhatsApp")
        btn_whatsapp.setStyleSheet("""
            QPushButton {
                background-color: #25D366;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: 500;
                font-size: 10pt;
            }
            QPushButton:hover {
                background-color: #20BA5A;
            }
        """)
        btn_whatsapp.clicked.connect(lambda: self.open_whatsapp())
        
        # Facebook button
        btn_facebook = QPushButton("📘 Facebook")
        btn_facebook.setStyleSheet("""
            QPushButton {
                background-color: #1877F2;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: 500;
                font-size: 10pt;
            }
            QPushButton:hover {
                background-color: #166FE5;
            }
        """)
        btn_facebook.clicked.connect(lambda: self.open_facebook())
        
        contact_layout.addStretch()
        contact_layout.addWidget(btn_whatsapp)
        contact_layout.addWidget(btn_facebook)
        contact_layout.addStretch()
        layout.addLayout(contact_layout)
        
        # Separator
        layout.addWidget(self._create_separator())
        
        # Features
        features_title = QLabel("Features")
        features_title.setAlignment(Qt.AlignCenter)
        features_title.setStyleSheet(f"font-size: 12pt; font-weight: 600; color: {current_theme['primary']};")
        layout.addWidget(features_title)
        
        features = QLabel(
            "• Remove PDF watermarks\n"
            "• Remove links and annotations\n"
            "• Batch processing support\n"
            "• Smart watermark detection\n"
            "• Dark/Light themes\n"
            "• Professional UI/UX"
        )
        features.setAlignment(Qt.AlignCenter)
        features.setStyleSheet("font-size: 9pt; line-height: 1.6;")
        layout.addWidget(features)
        
        layout.addStretch()
        
        # Copyright
        copyright_text = QLabel("© 2024 Raafat Shahin. All rights reserved.")
        copyright_text.setAlignment(Qt.AlignCenter)
        copyright_text.setStyleSheet("font-size: 8pt; color: grey;")
        layout.addWidget(copyright_text)
        
        # Close button
        btn_layout = QHBoxLayout()
        btn_close = QPushButton("Close")
        btn_close.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 10px 30px;
                border-radius: 6px;
                font-weight: 500;
                font-size: 10pt;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        btn_close.clicked.connect(self.accept)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_close)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
    
    def _create_separator(self):
        """Create a horizontal separator line"""
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: #E0E0E0;")
        return line
    
    def open_whatsapp(self):
        """Open WhatsApp with the phone number"""
        # WhatsApp link format: https://wa.me/PHONENUMBER
        phone = "201022779263"  # Country code + number (Egypt +20)
        url = f"https://wa.me/{phone}"
        QDesktopServices.openUrl(QUrl(url))
    
    def open_facebook(self):
        """Open Facebook profile"""
        url = "https://www.facebook.com/raafat.reda.366930"
        QDesktopServices.openUrl(QUrl(url))
