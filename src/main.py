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
    app.setApplicationName("WaterMarkEraser")
    app.setOrganizationName("Raafat Shahin")
    
    # Load settings to get theme preference
    from src.utils.settings import SettingsManager
    settings = SettingsManager()
    theme = settings.get('theme', 'light')
    
    # Apply theme
    apply_stylesheet(app, theme)
    
    window = MainWindow()
    
    # Set window icon
    icon_path = os.path.join(os.path.dirname(__file__), 'resources', 'logo.ico')
    if os.path.exists(icon_path):
        window.setWindowIcon(QIcon(icon_path))
    
    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
