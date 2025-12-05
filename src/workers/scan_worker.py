from PySide6.QtCore import QThread, Signal
from src.core.detector import WatermarkDetector

class ScanWorker(QThread):
    file_scanned = Signal(int, dict) # row, result
    finished = Signal()
    
    def __init__(self, files_to_scan):
        """
        files_to_scan: list of dicts {'path': str, 'row': int}
        """
        super().__init__()
        self.files = files_to_scan
        self.detector = WatermarkDetector()
        self._is_running = True

    def run(self):
        for file_data in self.files:
            if not self._is_running:
                break
                
            path = file_data['path']
            row = file_data['row']
            
            result = self.detector.scan_pdf(path)
            self.file_scanned.emit(row, result)
            
        self.finished.emit()

    def stop(self):
        self._is_running = False
