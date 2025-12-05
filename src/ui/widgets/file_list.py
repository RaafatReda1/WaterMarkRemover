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
        self.setColumnCount(5)
        self.setHorizontalHeaderLabels(["✓", "Status", "Name", "Pages", "Size"])
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.setAlternatingRowColors(True)
        self.horizontalHeader().setStretchLastSection(False)
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.setColumnWidth(0, 40)
        self.setColumnWidth(1, 60)
        self.setColumnWidth(3, 80)
        self.setColumnWidth(4, 100)
        
        # Enable drag and drop
        self.setAcceptDrops(True)
        
        # Connect double-click to open file
        self.itemDoubleClicked.connect(self.on_item_double_clicked)

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
        status_item = QTableWidgetItem("QUE")  # Default to queued
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
            # Get file data from name item
            name_item = self.item(row, 2)
            if not name_item:
                continue
                
            file_data = name_item.data(Qt.UserRole)
            if not file_data:
                continue
            
            # Checkbox state
            chk_item = self.item(row, 0)
            checked = chk_item.checkState() == Qt.Checked if chk_item else False
            
            files.append({
                'path': file_data.get('path', ''),
                'checked': checked,
                'row': row
            })
        
        return files

    def update_status(self, row, status, tooltip=""):
        """
        Updates the status column for a specific row.
        """
        item = self.item(row, 1)
        if item:
            item.setText(status)
            item.setToolTip(tooltip)
    
    def on_item_double_clicked(self, item):
        """Open the PDF file when double-clicked"""
        row = item.row()
        name_item = self.item(row, 2)
        
        if name_item:
            file_data = name_item.data(Qt.UserRole)
            if file_data and 'path' in file_data:
                file_path = file_data['path']
                
                # Open file with default PDF viewer
                import os
                import platform
                import subprocess
                
                try:
                    if platform.system() == 'Windows':
                        os.startfile(file_path)
                    elif platform.system() == 'Darwin':  # macOS
                        subprocess.run(['open', file_path])
                    else:  # Linux
                        subprocess.run(['xdg-open', file_path])
                except Exception as e:
                    print(f"Error opening file: {e}")
