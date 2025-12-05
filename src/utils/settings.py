import json
import os
from pathlib import Path
from typing import Any

class SettingsManager:
    """Manages application settings with persistence"""
    
    DEFAULT_SETTINGS = {
        'window_geometry': None,
        'last_directory': '',
        'remove_links': True,
        'remove_annotations': False,
        'remove_watermarks': False,
        'output_template': 'cleaned_{original}',
        'save_location': 'same_dir',
        'activity_log_visible': True,
        'statistics_visible': True,
        'theme': 'light',
        'font_size': 10,
        'thread_count': 4,
        'log_level': 'INFO'
    }
    
    def __init__(self):
        self.config_path = self._get_config_path()
        self.config_file = self.config_path / 'settings.json'
        self.settings = self.load()
    
    def _get_config_path(self) -> Path:
        """Get platform-specific config directory"""
        import platform
        
        if platform.system() == 'Windows':
            base = Path(os.getenv('APPDATA', ''))
        elif platform.system() == 'Darwin':
            base = Path.home() / 'Library' / 'Application Support'
        else:
            base = Path.home() / '.config'
        
        config_dir = base / 'PDFWatermarkCleaner'
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir
    
    def load(self) -> dict:
        """Load settings from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    loaded = json.load(f)
                    # Merge with defaults (in case new settings were added)
                    settings = self.DEFAULT_SETTINGS.copy()
                    settings.update(loaded)
                    return settings
            except Exception as e:
                print(f"Error loading settings: {e}")
                return self.DEFAULT_SETTINGS.copy()
        return self.DEFAULT_SETTINGS.copy()
    
    def save(self):
        """Save settings to file"""
        try:
            # Convert QByteArray to base64 string if present
            settings_to_save = self.settings.copy()
            if 'window_geometry' in settings_to_save and settings_to_save['window_geometry']:
                try:
                    # Convert QByteArray to bytes then to base64 string
                    from PySide6.QtCore import QByteArray
                    if isinstance(settings_to_save['window_geometry'], QByteArray):
                        settings_to_save['window_geometry'] = bytes(settings_to_save['window_geometry']).hex()
                except:
                    settings_to_save['window_geometry'] = None
            
            with open(self.config_file, 'w') as f:
                json.dump(settings_to_save, f, indent=2)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a setting value"""
        value = self.settings.get(key, default)
        
        # Convert hex string back to QByteArray for window_geometry
        if key == 'window_geometry' and value and isinstance(value, str):
            try:
                from PySide6.QtCore import QByteArray
                return QByteArray(bytes.fromhex(value))
            except:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """Set a setting value and save"""
        self.settings[key] = value
        self.save()
    
    def reset(self):
        """Reset to default settings"""
        self.settings = self.DEFAULT_SETTINGS.copy()
        self.save()
