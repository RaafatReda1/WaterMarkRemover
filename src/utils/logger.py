import logging
import sys
from pathlib import Path
from datetime import datetime
from src.models.enums import LogLevel

class AppLogger:
    """Centralized application logger"""
    
    def __init__(self, name: str = "PDFCleaner", log_dir: Path = None):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Create log directory
        if log_dir is None:
            log_dir = Path.home() / '.pdfcleaner' / 'logs'
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # File handler (rotating)
        log_file = log_dir / f"app_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
            datefmt='%H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers
        if not self.logger.handlers:
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
    
    def debug(self, message: str):
        self.logger.debug(message)
    
    def info(self, message: str):
        self.logger.info(message)
    
    def warning(self, message: str):
        self.logger.warning(message)
    
    def error(self, message: str):
        self.logger.error(message)
    
    def success(self, message: str):
        # Custom success level (treated as INFO)
        self.logger.info(f"SUCCESS: {message}")

# Global logger instance
logger = AppLogger()
