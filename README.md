# PDF Watermark Cleaner Pro

A professional desktop application for removing watermarks, links, and annotations from PDF files with intelligent detection and batch processing.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.10+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

## ✨ Features

- 🎯 **Remove UPDF Watermarks** - Completely removes UPDF logo and www.UPDF.COM text
- 🔗 **Remove Links** - Removes hyperlink annotations
- 📝 **Remove Annotations** - Removes highlights, comments, stamps, and markup
- 🔍 **Smart Detection** - Automatically scans files for watermarks
- ⚡ **Batch Processing** - Process multiple files simultaneously
- 🎨 **Professional UI** - Modern Material Design interface
- 📊 **Real-time Statistics** - Track file counts, sizes, and status
- 📝 **Activity Log** - Color-coded operation history
- ⚙️ **Customizable Settings** - Persistent configuration
- 💾 **Auto-save** - Remembers window position and preferences

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Installation

1. **Clone or download this repository**

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the application**:
```bash
python src/main.py
```

## 📖 Usage

### Basic Workflow

1. **Add Files**
   - Click "📄 Add Files" or "📁 Add Folder"
   - Or drag & drop PDFs directly onto the window

2. **Review Detection**
   - Files are automatically scanned
   - Check status icons: ✓ (clean), ⚠️ (watermarks found)

3. **Configure Options**
   - ☑ Remove Links
   - ☐ Remove Annotations
   - ☐ Remove Watermarks (UPDF, etc.)

4. **Start Cleaning**
   - Select files (Ctrl+A for all)
   - Click "▶ Start Cleaning"
   - Monitor progress in real-time

5. **Find Cleaned Files**
   - Saved with `cleaned_` prefix
   - Same directory as original

### Removing UPDF Watermarks

To remove the annoying UPDF logo and "www.UPDF.COM" text:

1. Add your PDF file
2. ✅ Check **"Remove Watermarks (UPDF, etc.)"**
3. Click "Start Cleaning"
4. Done! The watermark is completely removed.

## 🎯 Keyboard Shortcuts

- `Ctrl+O` - Open files
- `Ctrl+Shift+O` - Open folder
- `Ctrl+A` - Select all
- `Ctrl+D` - Deselect all
- `Ctrl+,` - Settings
- `Ctrl+Q` - Quit

## 🛠️ Technical Stack

- **Frontend**: PySide6 (Qt6)
- **PDF Engine**: PyMuPDF (fitz)
- **Threading**: QThread for background processing
- **Styling**: Custom QSS (Qt Style Sheets)
- **Settings**: JSON-based configuration

## 📁 Project Structure

```
pdf-watermark-remover/
├── src/
│   ├── main.py                 # Application entry point
│   ├── ui/
│   │   ├── main_window.py      # Main window
│   │   ├── widgets/            # Custom widgets
│   │   ├── dialogs/            # Dialogs (About, Settings)
│   │   └── styles/             # QSS styling
│   ├── core/
│   │   ├── detector.py         # Watermark detection
│   │   ├── cleaner.py          # PDF cleaning engine
│   │   └── file_manager.py     # File operations
│   ├── workers/
│   │   ├── scan_worker.py      # Background scanning
│   │   └── clean_worker.py     # Background cleaning
│   ├── utils/
│   │   ├── logger.py           # Application logger
│   │   └── settings.py         # Settings manager
│   └── models/
│       └── enums.py            # Enums and constants
├── requirements.txt
└── README.md
```

## 🎨 Screenshots

### Main Window
- Professional UI with menu bar
- Real-time statistics
- Color-coded activity log
- Batch file processing

### Features
- Smart watermark detection
- Progress tracking
- Settings dialog
- About dialog

## 🐛 Troubleshooting

### Import Errors
If you get `ModuleNotFoundError`, ensure you're running from the project root:
```bash
python src/main.py
```

### Watermark Still Visible
- **Highlights**: Enable "Remove Annotations"
- **UPDF Logo**: Enable "Remove Watermarks (UPDF, etc.)"
- **Text in content**: Only annotation-based watermarks currently supported

### Dependencies Issues
Reinstall dependencies:
```bash
pip install -r requirements.txt --upgrade
```

## 📝 Requirements

```
PySide6>=6.5.0
PyMuPDF>=1.23.0
Pillow>=10.0.0
watchdog>=3.0.0
python-dotenv>=1.0.0
```

## 🔮 Future Features

- [ ] Dark mode theme
- [ ] Preset profiles
- [ ] Backup system
- [ ] Statistics dashboard
- [ ] Batch rename tool
- [ ] Preview panel
- [ ] Multi-language support

## 📄 License

MIT License - feel free to use and modify!

## 🙏 Acknowledgments

- Built with Python and PySide6
- PDF processing powered by PyMuPDF
- Design inspired by Material Design

## 💡 Tips

- Use batch processing for multiple files
- Check the activity log for detailed results
- Customize settings for your workflow
- Use keyboard shortcuts for efficiency

---

**Made with ❤️ using Python & PySide6**
