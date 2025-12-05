from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt

class AboutDialog(QDialog):
    """About dialog showing application information"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About PDF Watermark Cleaner Pro")
        self.setFixedSize(400, 300)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        
        # App name
        name = QLabel("PDF Watermark Cleaner Pro")
        name.setProperty("class", "title")
        name.setAlignment(Qt.AlignCenter)
        
        # Version
        version = QLabel("Version 1.0.0")
        version.setAlignment(Qt.AlignCenter)
        
        # Description
        desc = QLabel(
            "A professional desktop application for removing watermarks, "
            "links, and annotations from PDF files with intelligent detection "
            "and batch processing capabilities."
        )
        desc.setWordWrap(True)
        desc.setAlignment(Qt.AlignCenter)
        desc.setProperty("class", "secondary")
        
        # Author
        author = QLabel("Developed with ❤️ using Python & PySide6")
        author.setAlignment(Qt.AlignCenter)
        author.setProperty("class", "secondary")
        
        # Features
        features = QLabel(
            "✓ Remove UPDF watermarks\n"
            "✓ Remove links and annotations\n"
            "✓ Batch processing\n"
            "✓ Smart detection\n"
            "✓ Professional UI"
        )
        features.setAlignment(Qt.AlignCenter)
        
        # Close button
        btn_layout = QHBoxLayout()
        btn_close = QPushButton("Close")
        btn_close.setProperty("class", "primary")
        btn_close.clicked.connect(self.accept)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_close)
        btn_layout.addStretch()
        
        # Add all to layout
        layout.addWidget(name)
        layout.addWidget(version)
        layout.addSpacing(8)
        layout.addWidget(desc)
        layout.addSpacing(8)
        layout.addWidget(features)
        layout.addStretch()
        layout.addWidget(author)
        layout.addLayout(btn_layout)
