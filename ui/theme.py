"""
theme.py - Modern QSS theme management for dynamic UI/UX
"""
from PySide6.QtWidgets import QApplication
from settings import load_settings
import os

def get_qss(theme="dark"):
    """Return QSS string for the given theme."""
    # Modern, fluid, accessible QSS for light/dark
    base_qss = """
    QWidget {
        font-family: 'Segoe UI', 'Arial', sans-serif;
        font-size: 13px;
        background: #23232b;
        color: #f0f0f0;
    }
    QPushButton {
        border-radius: 12px;
        background: #3a3a4a;
        color: #fff;
        padding: 7px 20px;
        font-weight: 600;
    }
    QPushButton:hover {
        background: #6a8cff;
        color: #fff;
    }
    QPushButton:pressed {
        background: #3451a1;
    }
    QLineEdit, QTextEdit, QComboBox {
        border-radius: 8px;
        background: #29293a;
        color: #f0f0f0;
        border: 1px solid #444;
        padding: 5px;
    }
    QListWidget {
        background: #23232b;
        color: #f0f0f0;
        border-radius: 8px;
    }
    QStatusBar {
        background: #1a1a22;
        color: #b0b0b0;
    }
    QDialog {
        background: #23232b;
    }
    QTabBar::tab {
        background: #3a3a4a;
        color: #fff;
        border-radius: 10px;
        padding: 6px 18px;
        margin: 2px;
    }
    QTabBar::tab:selected {
        background: #6a8cff;
        color: #fff;
    }
    """
    light_qss = base_qss.replace("#23232b", "#f8f8fa").replace("#3a3a4a", "#e0e0f0").replace("#29293a", "#ffffff").replace("#1a1a22", "#eaeaf0").replace("#f0f0f0", "#23232b").replace("#fff", "#23232b")
    return base_qss if theme == "dark" else light_qss

def apply_theme(app: QApplication, theme=None):
    """Apply the selected theme to the QApplication."""
    if theme is None:
        settings = load_settings()
        theme = settings.get("theme", "dark")
    qss = get_qss(theme)
    app.setStyleSheet(qss)
