from enum import Enum, auto

class FileStatus(Enum):
    """Status of a file in the processing queue"""
    QUEUED = auto()
    SCANNING = auto()
    CLEAN = auto()
    MARKED = auto()
    PROCESSING = auto()
    DONE = auto()
    ERROR = auto()

class LogLevel(Enum):
    """Logging levels"""
    DEBUG = auto()
    INFO = auto()
    SUCCESS = auto()
    WARNING = auto()
    ERROR = auto()

class SaveLocation(Enum):
    """Where to save cleaned files"""
    SAME_DIR = auto()
    CHOOSE_DIR = auto()
    CUSTOM_DIR = auto()

# Status icons mapping
STATUS_ICONS = {
    FileStatus.QUEUED: "⏳",
    FileStatus.SCANNING: "🔍",
    FileStatus.CLEAN: "✓",
    FileStatus.MARKED: "⚠️",
    FileStatus.PROCESSING: "⚙️",
    FileStatus.DONE: "✅",
    FileStatus.ERROR: "❌"
}

# Log level colors (for activity log)
LOG_COLORS = {
    LogLevel.DEBUG: "#9E9E9E",     # Gray
    LogLevel.INFO: "#2196F3",      # Blue
    LogLevel.SUCCESS: "#4CAF50",   # Green
    LogLevel.WARNING: "#FF9800",   # Orange
    LogLevel.ERROR: "#F44336"      # Red
}

# Log level prefixes
LOG_PREFIXES = {
    LogLevel.DEBUG: "🔧",
    LogLevel.INFO: "ℹ️",
    LogLevel.SUCCESS: "✅",
    LogLevel.WARNING: "⚠️",
    LogLevel.ERROR: "❌"
}
