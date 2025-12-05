import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication
from src.ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("PDF Watermark Cleaner Pro")
    app.setOrganizationName("Antigravity")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
