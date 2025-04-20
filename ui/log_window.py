from PySide6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QLineEdit, QHBoxLayout

class LogWindow(QDialog):
    """Window for displaying and filtering application logs."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Log")
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.filter_bar = QLineEdit(self)
        self.filter_bar.setPlaceholderText("Filter logs...")
        self.filter_bar.textChanged.connect(self.filter_logs)
        layout = QVBoxLayout(self)
        layout.addWidget(self.filter_bar)
        layout.addWidget(self.text_edit)
        self._all_logs = []
        # Modern dark style for log window
        self.setStyleSheet('''
            QDialog, QTextEdit, QLineEdit {
                background: #23232b;
                color: #fff;
                font-family: "Segoe UI", "Arial", sans-serif;
                font-size: 13px;
            }
            QLineEdit {
                border-radius: 8px;
                background: #29293a;
                color: #fff;
                border: 1px solid #444;
                padding: 5px;
            }
            QTextEdit {
                border-radius: 8px;
                background: #23232b;
                color: #fff;
            }
        ''')

    def set_log_level(self, level):
        self.log_level = level

    def append_log(self, message, level="info"):
        levels = ["debug", "info", "warning", "error"]
        if not hasattr(self, 'log_level'):
            self.log_level = "info"
        if levels.index(level) >= levels.index(self.log_level):
            self._all_logs.append(f"[{level.upper()}] {message}")
            self.filter_logs(self.filter_bar.text())

    def filter_logs(self, text):
        filtered = [log for log in self._all_logs if text.lower() in log.lower()]
        self.text_edit.setPlainText("\n".join(filtered))

class SharedLogWindow(LogWindow):
    """A log window shared between primary and secondary windows (singleton)."""
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    def __init__(self, parent=None):
        if hasattr(self, '_initialized') and self._initialized:
            return
        super().__init__(parent)
        self._initialized = True
