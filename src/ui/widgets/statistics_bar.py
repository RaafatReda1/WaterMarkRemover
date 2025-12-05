from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PySide6.QtCore import Qt

class StatisticsBar(QWidget):
    """Statistics bar showing file counts and sizes"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        
        self.lbl_files = QLabel("Files: 0")
        self.lbl_size = QLabel("Size: 0 MB")
        self.lbl_selected = QLabel("Selected: 0")
        self.lbl_clean = QLabel("Clean: 0")
        self.lbl_marked = QLabel("Marked: 0")
        self.lbl_errors = QLabel("Errors: 0")
        
        # Style labels
        for lbl in [self.lbl_files, self.lbl_size, self.lbl_selected, 
                    self.lbl_clean, self.lbl_marked, self.lbl_errors]:
            lbl.setProperty("class", "secondary")
        
        # Add to layout with separators
        layout.addWidget(self.lbl_files)
        layout.addWidget(self._separator())
        layout.addWidget(self.lbl_size)
        layout.addWidget(self._separator())
        layout.addWidget(self.lbl_selected)
        layout.addWidget(self._separator())
        layout.addWidget(self.lbl_clean)
        layout.addWidget(self._separator())
        layout.addWidget(self.lbl_marked)
        layout.addWidget(self._separator())
        layout.addWidget(self.lbl_errors)
        layout.addStretch()
    
    def _separator(self):
        sep = QLabel("|")
        sep.setProperty("class", "secondary")
        return sep
    
    def update_stats(self, total=0, size_bytes=0, selected=0, clean=0, marked=0, errors=0):
        """Update all statistics"""
        self.lbl_files.setText(f"Files: {total}")
        self.lbl_size.setText(f"Size: {self._format_size(size_bytes)}")
        self.lbl_selected.setText(f"Selected: {selected}")
        self.lbl_clean.setText(f"Clean: {clean}")
        self.lbl_marked.setText(f"Marked: {marked}")
        self.lbl_errors.setText(f"Errors: {errors}")
    
    def _format_size(self, size_bytes):
        """Format bytes to human-readable size"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f} TB"
