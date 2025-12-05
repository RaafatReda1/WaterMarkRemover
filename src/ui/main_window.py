from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                               QPushButton, QLabel, QFileDialog, QProgressBar, QGroupBox, QCheckBox)
from PySide6.QtCore import Qt, QSize
from src.ui.widgets.file_list import FileList
from src.core.file_manager import FileManager
from src.core.cleaner import PDFCleaner
from src.workers.clean_worker import CleanWorker
from src.workers.scan_worker import ScanWorker
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Watermark Cleaner Pro")
        self.setMinimumSize(900, 600)
        
        # Managers
        self.file_manager = FileManager()
        self.cleaner = PDFCleaner()
        
        self.setup_ui()
        
    def setup_ui(self):
        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # 1. Top Bar (Toolbar)
        top_bar = QHBoxLayout()
        
        self.btn_add_files = QPushButton("Add Files")
        self.btn_add_files.clicked.connect(self.add_files)
        
        self.btn_add_folder = QPushButton("Add Folder")
        self.btn_add_folder.clicked.connect(self.add_folder)
        
        top_bar.addWidget(self.btn_add_files)
        top_bar.addWidget(self.btn_add_folder)
        top_bar.addStretch()
        
        # 2. File List Area
        self.file_list = FileList()
        self.file_list.files_dropped.connect(self.process_dropped_files)
        
        # 3. Bottom Controls
        bottom_controls = QHBoxLayout()
        
        # Cleaning Options Group
        options_group = QGroupBox("Cleaning Options")
        options_layout = QHBoxLayout()
        self.chk_remove_links = QCheckBox("Remove Links")
        self.chk_remove_links.setChecked(True)
        options_layout.addWidget(self.chk_remove_links)
        options_group.setLayout(options_layout)
        
        # Start Button & Progress
        action_layout = QVBoxLayout()
        self.btn_start = QPushButton("Start Cleaning")
        self.btn_start.setMinimumHeight(40)
        self.btn_start.clicked.connect(self.start_cleaning)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        
        action_layout.addWidget(self.btn_start)
        action_layout.addWidget(self.progress_bar)
        
        bottom_controls.addWidget(options_group, 2)
        bottom_controls.addLayout(action_layout, 1)
        
        # Add to main layout
        main_layout.addLayout(top_bar)
        main_layout.addWidget(self.file_list)
        main_layout.addLayout(bottom_controls)
        
        # Status Bar
        self.statusBar().showMessage("Ready")

    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Select PDF Files", "", "PDF Files (*.pdf)"
        )
        if files:
            self.process_dropped_files(files)

    def add_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.process_dropped_files([folder])

    def process_dropped_files(self, paths):
        """
        Process list of file paths (files or folders) and add to list.
        """
        pdf_files = self.file_manager.resolve_paths(paths)
        files_to_scan = []
        
        for pdf_path in pdf_files:
            info = self.file_manager.get_file_info(pdf_path)
            if info:
                self.file_list.add_file_item(info)
                # Prepare for scanning (we need the row index)
                row_idx = self.file_list.rowCount() - 1
                files_to_scan.append({'path': pdf_path, 'row': row_idx})
                
                # Update status to scanning immediately? Or wait for worker?
                self.file_list.update_status(row_idx, "...", "Waiting to scan...")
        
        if files_to_scan:
            self.start_scanning(files_to_scan)
        
        self.statusBar().showMessage(f"Added {len(pdf_files)} files")

    def start_scanning(self, files_data):
        """
        Starts the background scanner for the given files.
        """
        # Create a new worker for this batch (simple approach)
        # Note: In a real app we might want a persistent queue, but this works for now.
        worker = ScanWorker(files_data)
        worker.file_scanned.connect(self.on_file_scanned)
        worker.finished.connect(lambda: self.cleanup_worker(worker))
        worker.start()
        
        # Keep reference to avoid GC
        if not hasattr(self, 'scan_workers'):
            self.scan_workers = []
        self.scan_workers.append(worker)

    def cleanup_worker(self, worker):
        if worker in self.scan_workers:
            self.scan_workers.remove(worker)

    def on_file_scanned(self, row, result):
        if 'error' in result:
             self.file_list.update_status(row, "❌", f"Error: {result['error']}")
             return

        # Determine status icon based on detections
        links = result.get('links', 0)
        patterns = len(result.get('text_patterns', []))
        images = result.get('images', 0)
        
        tooltip_parts = []
        if links > 0: tooltip_parts.append(f"{links} links")
        if patterns > 0: tooltip_parts.append(f"{patterns} text patterns")
        if images > 0: tooltip_parts.append(f"{images} recurring images")
        
        if not tooltip_parts:
            status = "✓"
            tooltip = "Clean (No watermarks detected)"
        else:
            status = "⚠️"
            tooltip = "Found: " + ", ".join(tooltip_parts)
            
        self.file_list.update_status(row, status, tooltip)


    def start_cleaning(self):
        files = self.file_list.get_files()
        files_to_process = [f for f in files if f['checked']]
        
        if not files_to_process:
            self.statusBar().showMessage("No files selected")
            return
            
        # Update UI
        self.btn_start.setEnabled(False)
        self.btn_add_files.setEnabled(False)
        self.btn_add_folder.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.progress_bar.setMaximum(len(files_to_process))
        
        # Prepare options
        options = {
            'remove_links': self.chk_remove_links.isChecked()
        }
        
        # Start Worker
        self.worker = CleanWorker(files_to_process, options)
        self.worker.progress.connect(self.on_progress)
        self.worker.file_finished.connect(self.on_file_finished)
        self.worker.finished.connect(self.on_finished)
        self.worker.start()
        
        self.statusBar().showMessage("Cleaning in progress...")

    def on_progress(self, current, total):
        self.progress_bar.setValue(current)

    def on_file_finished(self, row, success, message):
        status = "DONE" if success else "ERR"
        self.file_list.update_status(row, status, message)

    def on_finished(self):
        self.btn_start.setEnabled(True)
        self.btn_add_files.setEnabled(True)
        self.btn_add_folder.setEnabled(True)
        self.statusBar().showMessage("Cleaning completed")

