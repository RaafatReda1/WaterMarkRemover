import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from src.ui.main_window import MainWindow
from src.ui.styles.styles import apply_stylesheet

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("PDF Watermark Cleaner Pro")
    app.setOrganizationName("Antigravity")
    
    # Apply professional styling
    apply_stylesheet(app)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
