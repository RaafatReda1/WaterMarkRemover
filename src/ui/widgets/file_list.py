from PySide6.QtWidgets import (QTableWidget, QTableWidgetItem, QHeaderView, 
                               QWidget, QHBoxLayout, QPushButton, QAbstractItemView)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon

class FileList(QTableWidget):
    """
    Widget to display the list of PDF files to be processed.
    """
    files_dropped = Signal(list)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setColumnCount(6)
        self.setHorizontalHeaderLabels([
            "", "Status", "File Name", "Pages", "Size", "Actions"
        ])
        
        # Configure look and feel
        self.verticalHeader().setVisible(False)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setShowGrid(False)
        self.setAlternatingRowColors(True)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setViewportMargins(0, 0, 0, 0)
        
        # Configure columns
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)  # Checkbox
        header.setSectionResizeMode(1, QHeaderView.Fixed)  # Status
        header.setSectionResizeMode(2, QHeaderView.Stretch) # Name
        header.setSectionResizeMode(3, QHeaderView.Fixed)  # Pages
        header.setSectionResizeMode(4, QHeaderView.Fixed)  # Size
        header.setSectionResizeMode(5, QHeaderView.Fixed)  # Actions
        
        self.setColumnWidth(0, 30)
        self.setColumnWidth(1, 40)
        self.setColumnWidth(3, 60)
        self.setColumnWidth(4, 80)
        self.setColumnWidth(5, 80)

    def add_file_item(self, file_data):
        """
        Adds a file to the list.
        file_data: dict containing 'name', 'path', 'pages', 'size'
        """
        row = self.rowCount()
        self.insertRow(row)
        
        # 0. Checkbox
        chk_item = QTableWidgetItem()
        chk_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        chk_item.setCheckState(Qt.Checked)
        self.setItem(row, 0, chk_item)
        
        # 1. Status Icon
        status_item = QTableWidgetItem("QUE") # Default to queued
        status_item.setTextAlignment(Qt.AlignCenter)
        self.setItem(row, 1, status_item)
        
        # 2. Name
        name_item = QTableWidgetItem(file_data.get('name', 'Unknown'))
        name_item.setToolTip(file_data.get('path', ''))
        # Store full file data in the name item for easy access
        name_item.setData(Qt.UserRole, file_data) 
        self.setItem(row, 2, name_item)
        
        # 3. Pages
        pages_item = QTableWidgetItem(str(file_data.get('pages', '-')))
        pages_item.setTextAlignment(Qt.AlignCenter)
        self.setItem(row, 3, pages_item)
        
        # 4. Size
        size_str = self._format_size(file_data.get('size', 0))
        size_item = QTableWidgetItem(size_str)
        size_item.setTextAlignment(Qt.AlignCenter)
        self.setItem(row, 4, size_item)
        
        # 5. Actions (Button)
        # For phase 1 we might skip the button or add a placeholder
        pass

    def _format_size(self, size_bytes):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f} TB"
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()
            
    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()
            
    def dropEvent(self, event):
        files = []
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            files.append(path)
        
        if files:
            self.files_dropped.emit(files)

    def get_files(self):
        """
        Returns a list of dicts for all files in the table.
        """
        files = []
        for row in range(self.rowCount()):
            # Assuming we store the full path in the tooltip of the name column (col 2)
            name_item = self.item(row, 2)
            path = name_item.toolTip()
            
            # Checkbox state
            chk_item = self.item(row, 0)
            checked = chk_item.checkState() == Qt.Checked
            
            files.append({
                'path': path,
                'checked': checked,
                'row': row
            })
        return files

    def update_status(self, row, status, tooltip=""):
        """
        Updates the status column for a specific row.
        """
        item = self.item(row, 1)
        item.setText(status)
        item.setToolTip(tooltip)


