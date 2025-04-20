from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox, QComboBox, QCheckBox, QSpinBox
from settings import load_settings

class SettingsDialog(QDialog):
    """Dialog for editing application settings."""
    def __init__(self, parent=None, settings=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.settings = settings or load_settings()
        layout = QVBoxLayout(self)
        # Theme selection
        theme_label = QLabel("Theme:")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["dark", "light"])
        self.theme_combo.setCurrentText(self.settings.get("theme", "dark"))
        layout.addWidget(theme_label)
        layout.addWidget(self.theme_combo)
        # VSync
        self.vsync_check = QCheckBox("Enable VSync")
        self.vsync_check.setChecked(self.settings["performance"].get("vsync", True))
        layout.addWidget(self.vsync_check)
        # Max FPS
        fps_label = QLabel("Max FPS:")
        self.fps_spin = QSpinBox()
        self.fps_spin.setRange(1, 240)
        self.fps_spin.setValue(self.settings["performance"].get("max_fps", 60))
        layout.addWidget(fps_label)
        layout.addWidget(self.fps_spin)
        # Debug overlay options
        self.fps_overlay_check = QCheckBox("Show FPS in overlay")
        self.fps_overlay_check.setChecked(self.settings["debug_overlay"].get("show_fps", True))
        self.memory_overlay_check = QCheckBox("Show memory usage in overlay")
        self.memory_overlay_check.setChecked(self.settings["debug_overlay"].get("show_memory", False))
        self.device_overlay_check = QCheckBox("Show device info in overlay")
        self.device_overlay_check.setChecked(self.settings["debug_overlay"].get("show_device_info", False))
        layout.addWidget(self.fps_overlay_check)
        layout.addWidget(self.memory_overlay_check)
        layout.addWidget(self.device_overlay_check)
        # Log level
        log_label = QLabel("Log level:")
        self.log_combo = QComboBox()
        self.log_combo.addItems(["debug", "info", "warning", "error"])
        self.log_combo.setCurrentText(self.settings.get("log_level", "info"))
        layout.addWidget(log_label)
        layout.addWidget(self.log_combo)
        # Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_settings(self):
        self.settings["theme"] = self.theme_combo.currentText()
        self.settings["performance"]["vsync"] = self.vsync_check.isChecked()
        self.settings["performance"]["max_fps"] = self.fps_spin.value()
        self.settings["debug_overlay"]["show_fps"] = self.fps_overlay_check.isChecked()
        self.settings["debug_overlay"]["show_memory"] = self.memory_overlay_check.isChecked()
        self.settings["debug_overlay"]["show_device_info"] = self.device_overlay_check.isChecked()
        self.settings["log_level"] = self.log_combo.currentText()
        return self.settings

class AboutDialog(QDialog):
    """Dialog showing application and system information."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About")
        layout = QVBoxLayout(self)
        import platform
        import datetime
        info = f"Vulkan GUI Application\nVersion 1.0\n(c) 2025\nOS: {platform.system()} {platform.release()}\nPython: {platform.python_version()}\nDate: {datetime.datetime.now().strftime('%Y-%m-%d')}"
        layout.addWidget(QLabel(info))
        buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)
