from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                               QPushButton, QLabel, QFileDialog, QProgressBar, 
                               QGroupBox, QCheckBox, QMenuBar, QMenu, QMessageBox,
                               QApplication)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QAction, QKeySequence
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.ui.widgets.file_list import FileList
from src.ui.widgets.activity_log import ActivityLog
from src.ui.widgets.statistics_bar import StatisticsBar
from src.ui.dialogs.about_dialog import AboutDialog
from src.ui.dialogs.settings_dialog import SettingsDialog
from src.core.file_manager import FileManager
from src.core.cleaner import PDFCleaner
from src.workers.clean_worker import CleanWorker
from src.workers.scan_worker import ScanWorker
from src.utils.settings import SettingsManager
from src.models.enums import FileStatus

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WaterMarkEraser - Professional PDF Cleaner")
        self.setMinimumSize(1000, 700)
        
        # Managers
        self.file_manager = FileManager()
        self.cleaner = PDFCleaner()
        self.settings_manager = SettingsManager()
        
        # Workers list
        self.scan_workers = []
        
        self.setup_ui()
        self.create_menu_bar()
        self.load_settings()
        
    def setup_ui(self):
        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(8)
        
        # 1. Top Toolbar
        toolbar = self.create_toolbar()
        
        # 2. Statistics Bar
        self.statistics_bar = StatisticsBar()
        
        # 3. File List Area
        self.file_list = FileList()
        self.file_list.files_dropped.connect(self.process_dropped_files)
        
        # 4. Bottom Controls
        controls = self.create_controls()
        
        # 5. Activity Log
        self.activity_log = ActivityLog()
        
        # Add to main layout
        main_layout.addLayout(toolbar)
        main_layout.addWidget(self.statistics_bar)
        main_layout.addWidget(self.file_list, 1)  # Stretch factor
        main_layout.addLayout(controls)
        main_layout.addWidget(self.activity_log)
        
        # Status Bar
        self.statusBar().showMessage("Ready")
        
        # Log welcome message
        self.activity_log.info("WaterMarkEraser started - Ready to clean PDFs!")
        
    def create_toolbar(self):
        """Create top toolbar with action buttons"""
        layout = QHBoxLayout()
        
        self.btn_add_files = QPushButton("📄 Add Files")
        self.btn_add_files.clicked.connect(self.add_files)
        
        self.btn_add_folder = QPushButton("📁 Add Folder")
        self.btn_add_folder.clicked.connect(self.add_folder)
        
        self.btn_clear_list = QPushButton("🗑️ Clear List")
        self.btn_clear_list.setProperty("class", "secondary")
        self.btn_clear_list.clicked.connect(self.clear_list)
        
        layout.addWidget(self.btn_add_files)
        layout.addWidget(self.btn_add_folder)
        layout.addWidget(self.btn_clear_list)
        layout.addStretch()
        
        return layout
    
    def create_controls(self):
        """Create bottom control panel"""
        layout = QHBoxLayout()
        
        # Cleaning Options Group
        options_group = QGroupBox("Cleaning Options")
        options_layout = QVBoxLayout()
        
        # First row - removal options
        removal_row = QHBoxLayout()
        self.chk_remove_links = QCheckBox("Remove Links")
        self.chk_remove_links.setChecked(self.settings_manager.get('remove_links', True))
        
        self.chk_remove_annotations = QCheckBox("Remove Annotations")
        self.chk_remove_annotations.setChecked(self.settings_manager.get('remove_annotations', False))
        
        self.chk_remove_watermarks = QCheckBox("Remove Watermarks (UPDF, etc.)")
        self.chk_remove_watermarks.setChecked(self.settings_manager.get('remove_watermarks', False))
        
        removal_row.addWidget(self.chk_remove_links)
        removal_row.addWidget(self.chk_remove_annotations)
        removal_row.addWidget(self.chk_remove_watermarks)
        
        # Second row - output options
        output_row = QHBoxLayout()
        self.chk_overwrite = QCheckBox("Overwrite original files (⚠️ No backup)")
        self.chk_overwrite.setChecked(False)
        self.chk_overwrite.setStyleSheet("QCheckBox { color: #F44336; font-weight: 500; }")
        
        output_row.addWidget(self.chk_overwrite)
        output_row.addStretch()
        
        options_layout.addLayout(removal_row)
        options_layout.addLayout(output_row)
        options_group.setLayout(options_layout)
        
        # Progress Section
        progress_layout = QVBoxLayout()
        
        self.btn_start = QPushButton("▶ Start Cleaning")
        self.btn_start.setProperty("class", "success")
        self.btn_start.setMinimumHeight(40)
        self.btn_start.clicked.connect(self.start_cleaning)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        
        self.lbl_progress = QLabel("")
        self.lbl_progress.setProperty("class", "secondary")
        self.lbl_progress.setVisible(False)
        
        progress_layout.addWidget(self.btn_start)
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.lbl_progress)
        
        layout.addWidget(options_group, 2)
        layout.addLayout(progress_layout, 1)
        
        return layout
    
    def create_menu_bar(self):
        """Create menu bar"""
        menubar = self.menuBar()
        
        # File Menu
        file_menu = menubar.addMenu("&File")
        
        action_open_files = QAction("Open Files...", self)
        action_open_files.setShortcut(QKeySequence.Open)
        action_open_files.triggered.connect(self.add_files)
        
        action_open_folder = QAction("Open Folder...", self)
        action_open_folder.setShortcut(QKeySequence("Ctrl+Shift+O"))
        action_open_folder.triggered.connect(self.add_folder)
        
        action_clear = QAction("Clear List", self)
        action_clear.triggered.connect(self.clear_list)
        
        action_exit = QAction("Exit", self)
        action_exit.setShortcut(QKeySequence.Quit)
        action_exit.triggered.connect(self.close)
        
        file_menu.addAction(action_open_files)
        file_menu.addAction(action_open_folder)
        file_menu.addSeparator()
        file_menu.addAction(action_clear)
        file_menu.addSeparator()
        file_menu.addAction(action_exit)
        
        # Edit Menu
        edit_menu = menubar.addMenu("&Edit")
        
        action_select_all = QAction("Select All", self)
        action_select_all.setShortcut(QKeySequence.SelectAll)
        action_select_all.triggered.connect(self.select_all_files)
        
        action_deselect_all = QAction("Deselect All", self)
        action_deselect_all.setShortcut(QKeySequence("Ctrl+D"))
        action_deselect_all.triggered.connect(self.deselect_all_files)
        
        edit_menu.addAction(action_select_all)
        edit_menu.addAction(action_deselect_all)
        
        # Tools Menu
        tools_menu = menubar.addMenu("&Tools")
        
        action_settings = QAction("Settings...", self)
        action_settings.setShortcut(QKeySequence.Preferences)
        action_settings.triggered.connect(self.show_settings)
        
        tools_menu.addAction(action_settings)
        
        # Help Menu
        help_menu = menubar.addMenu("&Help")
        
        action_about = QAction("About", self)
        action_about.triggered.connect(self.show_about)
        
        help_menu.addAction(action_about)
    
    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Select PDF Files", 
            self.settings_manager.get('last_directory', ''),
            "PDF Files (*.pdf)"
        )
        if files:
            # Save last directory
            self.settings_manager.set('last_directory', os.path.dirname(files[0]))
            self.process_dropped_files(files)
            self.activity_log.info(f"Added {len(files)} file(s)")

    def add_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self, "Select Folder",
            self.settings_manager.get('last_directory', '')
        )
        if folder:
            self.settings_manager.set('last_directory', folder)
            self.process_dropped_files([folder])
            self.activity_log.info(f"Scanning folder: {folder}")

    def process_dropped_files(self, paths):
        """Process list of file paths (files or folders) and add to list"""
        pdf_files = self.file_manager.resolve_paths(paths)
        files_to_scan = []
        
        for pdf_path in pdf_files:
            info = self.file_manager.get_file_info(pdf_path)
            if info:
                self.file_list.add_file_item(info)
                row_idx = self.file_list.rowCount() - 1
                files_to_scan.append({'path': pdf_path, 'row': row_idx})
                self.file_list.update_status(row_idx, "⏳", "Waiting to scan...")
        
        if files_to_scan:
            self.start_scanning(files_to_scan)
        
        self.update_statistics()
        self.statusBar().showMessage(f"Added {len(pdf_files)} files")

    def start_scanning(self, files_data):
        """Starts the background scanner for the given files"""
        worker = ScanWorker(files_data)
        worker.file_scanned.connect(self.on_file_scanned)
        worker.finished.connect(lambda: self.cleanup_worker(worker))
        worker.start()
        
        if not hasattr(self, 'scan_workers'):
            self.scan_workers = []
        self.scan_workers.append(worker)

    def cleanup_worker(self, worker):
        if hasattr(self, 'scan_workers') and worker in self.scan_workers:
            self.scan_workers.remove(worker)

    def on_file_scanned(self, row, result):
        if 'error' in result:
             self.file_list.update_status(row, "❌", f"Error: {result['error']}")
             self.activity_log.error(f"Scan error on row {row+1}: {result['error']}")
             return

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
        self.update_statistics()

    def start_cleaning(self):
        files = self.file_list.get_files()
        files_to_process = [f for f in files if f['checked']]
        
        if not files_to_process:
            self.activity_log.warning("No files selected for cleaning")
            QMessageBox.warning(self, "No Files", "Please select files to clean.")
            return
        
        # Check if overwrite is enabled and confirm
        if self.chk_overwrite.isChecked():
            reply = QMessageBox.warning(
                self, 
                "⚠️ Overwrite Original Files",
                f"You are about to OVERWRITE {len(files_to_process)} original file(s).\n\n"
                "⚠️ WARNING: This action cannot be undone!\n"
                "The original files will be permanently modified.\n\n"
                "Are you sure you want to continue?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.No:
                self.activity_log.info("Cleaning cancelled by user")
                return
            
        # Update UI
        self.btn_start.setEnabled(False)
        self.btn_add_files.setEnabled(False)
        self.btn_add_folder.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.progress_bar.setMaximum(len(files_to_process))
        self.lbl_progress.setVisible(True)
        
        # Prepare options
        options = {
            'remove_links': self.chk_remove_links.isChecked(),
            'remove_annotations': self.chk_remove_annotations.isChecked(),
            'remove_watermarks': self.chk_remove_watermarks.isChecked(),
            'overwrite_original': self.chk_overwrite.isChecked()
        }
        
        # Save options (except overwrite - too dangerous to save as default)
        self.settings_manager.set('remove_links', options['remove_links'])
        self.settings_manager.set('remove_annotations', options['remove_annotations'])
        self.settings_manager.set('remove_watermarks', options['remove_watermarks'])
        
        # Start Worker
        self.worker = CleanWorker(files_to_process, options)
        self.worker.progress.connect(self.on_progress)
        self.worker.file_finished.connect(self.on_file_finished)
        self.worker.finished.connect(self.on_finished)
        self.worker.start()
        
        mode = "OVERWRITING" if options['overwrite_original'] else "cleaning"
        self.activity_log.info(f"Started {mode} {len(files_to_process)} file(s)")
        self.statusBar().showMessage(f"{mode.capitalize()} in progress...")


    def on_progress(self, current, total):
        self.progress_bar.setValue(current)
        self.lbl_progress.setText(f"Processing: {current}/{total} files")

    def on_file_finished(self, row, success, message):
        status = "✅" if success else "❌"
        self.file_list.update_status(row, status, message)
        
        # Get file name for logging
        name_item = self.file_list.item(row, 2)
        file_name = name_item.text() if name_item else f"File {row+1}"
        
        if success:
            self.activity_log.success(f"{file_name}: {message}")
        else:
            self.activity_log.error(f"{file_name}: {message}")

    def on_finished(self):
        self.btn_start.setEnabled(True)
        self.btn_add_files.setEnabled(True)
        self.btn_add_folder.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.lbl_progress.setVisible(False)
        self.statusBar().showMessage("Cleaning completed")
        self.activity_log.success("All files processed!")
        self.update_statistics()

    def clear_list(self):
        """Clear all files from the list"""
        if self.file_list.rowCount() > 0:
            reply = QMessageBox.question(
                self, "Clear List",
                "Are you sure you want to clear all files?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.file_list.setRowCount(0)
                self.update_statistics()
                self.activity_log.info("File list cleared")
    
    def select_all_files(self):
        """Select all files in the list"""
        for row in range(self.file_list.rowCount()):
            chk_item = self.file_list.item(row, 0)
            if chk_item:
                chk_item.setCheckState(Qt.Checked)
        self.update_statistics()
    
    def deselect_all_files(self):
        """Deselect all files in the list"""
        for row in range(self.file_list.rowCount()):
            chk_item = self.file_list.item(row, 0)
            if chk_item:
                chk_item.setCheckState(Qt.Unchecked)
        self.update_statistics()
    
    def update_statistics(self):
        """Update the statistics bar"""
        total = self.file_list.rowCount()
        selected = 0
        clean = 0
        marked = 0
        errors = 0
        total_size = 0
        
        for row in range(total):
            # Count selected
            chk_item = self.file_list.item(row, 0)
            if chk_item and chk_item.checkState() == Qt.Checked:
                selected += 1
            
            # Count by status
            status_item = self.file_list.item(row, 1)
            if status_item:
                status = status_item.text()
                if status == "✓":
                    clean += 1
                elif status == "⚠️":
                    marked += 1
                elif status == "❌":
                    errors += 1
            
            # Sum size
            name_item = self.file_list.item(row, 2)
            if name_item:
                file_data = name_item.data(Qt.UserRole)
                if file_data:
                    total_size += file_data.get('size', 0)
        
        self.statistics_bar.update_stats(total, total_size, selected, clean, marked, errors)
    
    def show_settings(self):
        """Show settings dialog"""
        dialog = SettingsDialog(self.settings_manager, self)
        if dialog.exec():
            self.activity_log.info("Settings saved")
            # Reapply theme
            from src.ui.styles.styles import apply_stylesheet
            theme = self.settings_manager.get('theme', 'light')
            apply_stylesheet(QApplication.instance(), theme)
            self.activity_log.info(f"Theme changed to: {theme}")
            # Apply other settings
            self.load_settings()
    
    def show_about(self):
        """Show about dialog"""
        dialog = AboutDialog(self)
        dialog.exec()
    
    def load_settings(self):
        """Load and apply saved settings"""
        # Restore window geometry if saved
        geometry = self.settings_manager.get('window_geometry')
        if geometry:
            try:
                self.restoreGeometry(geometry)
            except:
                pass
        
        # Apply visibility settings
        activity_visible = self.settings_manager.get('activity_log_visible', True)
        self.activity_log.setVisible(activity_visible)
        
        stats_visible = self.settings_manager.get('statistics_visible', True)
        self.statistics_bar.setVisible(stats_visible)
        
        # Apply theme
        from src.ui.styles.styles import apply_stylesheet
        theme = self.settings_manager.get('theme', 'light')
        apply_stylesheet(QApplication.instance(), theme)
    
    def closeEvent(self, event):
        """Save settings on close"""
        self.settings_manager.set('window_geometry', self.saveGeometry())
        event.accept()
