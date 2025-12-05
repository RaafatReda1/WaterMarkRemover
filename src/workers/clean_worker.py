from PySide6.QtCore import QThread, Signal
from src.core.cleaner import PDFCleaner

class CleanWorker(QThread):
    progress = Signal(int, int) # item_idx, total
    file_finished = Signal(int, bool, str) # row_idx, success, message
    finished = Signal()
    
    def __init__(self, files, options=None):
        super().__init__()
        self.files = files # List of dicts: {'path': str, 'row': int}
        self.options = options
        self.cleaner = PDFCleaner()
        self._is_running = True

    def run(self):
        total = len(self.files)
        for i, file_data in enumerate(self.files):
            if not self._is_running:
                break
            
            input_path = file_data['path']
            row = file_data['row']
            
            # Generate output path
            output_path = self.cleaner.generate_output_path(input_path)
            
            # Run cleaning
            result = self.cleaner.clean_document(input_path, output_path, self.options)
            
            # Emit result
            if result['success']:
                msg = f"Removed {result.get('links_removed', 0)} links"
                self.file_finished.emit(row, True, msg)
            else:
                self.file_finished.emit(row, False, result.get('error', 'Unknown error'))
            
            self.progress.emit(i + 1, total)
            
        self.finished.emit()

    def stop(self):
        self._is_running = False
