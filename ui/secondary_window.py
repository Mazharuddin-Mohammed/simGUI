from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QStackedWidget, QStatusBar, QFormLayout, QLabel, QLineEdit, QTextEdit, QComboBox
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QObject, QEvent, Qt
from PySide6.QtWidgets import QGraphicsOpacityEffect
from settings import load_settings, save_settings, add_recent_file, get_timestamp
from vulkan.vulkan_widget import VulkanWidget
from ui.log_window import LogWindow
from ui.badge_tab import BadgeTabBar
from ui.dialogs import SettingsDialog, AboutDialog

class DeviceTab(QWidget):
    """Widget for Device tab."""
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QFormLayout(self)
        layout.addRow("Device Name:", QLineEdit())
        layout.addRow("Device Type:", QComboBox())
        layout.addRow("Description:", QTextEdit())

class MeshTab(QWidget):
    """Widget for Mesh tab."""
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QFormLayout(self)
        layout.addRow("Mesh File:", QLineEdit())
        layout.addRow("Vertices:", QLabel("0"))
        layout.addRow("Faces:", QLabel("0"))

class MaterialPropertiesTab(QWidget):
    """Widget for Material Properties tab."""
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QFormLayout(self)
        layout.addRow("Material Name:", QLineEdit())
        layout.addRow("Density:", QLineEdit())
        layout.addRow("Elasticity:", QLineEdit())

class PhysicalModelsTab(QWidget):
    """Widget for Physical Models tab."""
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Select and configure physical models here."))

class SolutionTab(QWidget):
    """Widget for Solution tab."""
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Set up and run the simulation solution."))

class VisualizationTab(QWidget):
    """Widget for Visualization tab."""
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("View simulation results and visualizations."))

class HelpSupportTab(QWidget):
    """Widget for Help & Support tab."""
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Access help and support resources."))

class AboutTab(QWidget):
    """Widget for About tab."""
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("About this application."))

class SecondaryMainWindow(QMainWindow):
    """Secondary window for simulation workflow (badge tabs, Vulkan, etc)."""
    def __init__(self, shared_log_window=None):
        super().__init__()
        self.setWindowTitle("Simulation Workflow")
        self.tab_names = [
            "Device", "Mesh", "Material Properties", "Physical Models", "Solution", "Visualization", "Help & Support", "About"
        ]
        central_widget = QWidget()
        self.central_layout = QVBoxLayout(central_widget)
        self.badge_bar = BadgeTabBar(self.tab_names, self.on_tab_clicked)
        self.central_layout.addWidget(self.badge_bar)
        self.stack = QStackedWidget()
        # Main VulkanWidget page
        self.vulkan_widget = VulkanWidget(self)
        self.stack.addWidget(self.vulkan_widget)
        # Tab content pages (custom widgets)
        self.tab_pages = {
            "Device": DeviceTab(),
            "Mesh": MeshTab(),
            "Material Properties": MaterialPropertiesTab(),
            "Physical Models": PhysicalModelsTab(),
            "Solution": SolutionTab(),
            "Visualization": VisualizationTab(),
            "Help & Support": HelpSupportTab(),
            "About": AboutTab(),
        }
        for page in self.tab_pages.values():
            self.stack.addWidget(page)
        self.central_layout.addWidget(self.stack)
        self.setCentralWidget(central_widget)
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        if shared_log_window:
            self.log_window = shared_log_window
        else:
            self.log_window = LogWindow(self)
        self.settings = load_settings()
        self.apply_settings()
        self._create_menu()
        self._connect_signals()
        self.show_main_page()
        self._log_action("Secondary window started.")

    def show_main_page(self):
        self.stack.setCurrentWidget(self.vulkan_widget)
        self.badge_bar.set_active("")

    def on_tab_clicked(self, name):
        new_widget = self.tab_pages[name]
        current_widget = self.stack.currentWidget()
        if current_widget is new_widget:
            return
        # Fade out current, fade in new
        fade_out = QGraphicsOpacityEffect(current_widget)
        current_widget.setGraphicsEffect(fade_out)
        anim_out = QPropertyAnimation(fade_out, b"opacity")
        anim_out.setDuration(180)
        anim_out.setStartValue(1.0)
        anim_out.setEndValue(0.0)
        anim_out.setEasingCurve(QEasingCurve.InOutQuad)
        def on_fade_out_finished():
            self.stack.setCurrentWidget(new_widget)
            fade_in = QGraphicsOpacityEffect(new_widget)
            new_widget.setGraphicsEffect(fade_in)
            anim_in = QPropertyAnimation(fade_in, b"opacity")
            anim_in.setDuration(180)
            anim_in.setStartValue(0.0)
            anim_in.setEndValue(1.0)
            anim_in.setEasingCurve(QEasingCurve.InOutQuad)
            anim_in.finished.connect(lambda: new_widget.setGraphicsEffect(None))
            anim_in.start(QPropertyAnimation.DeleteWhenStopped)
        anim_out.finished.connect(on_fade_out_finished)
        anim_out.start(QPropertyAnimation.DeleteWhenStopped)
        self.badge_bar.set_active(name)

    def on_back_to_main(self):
        self.show_main_page()

    def _create_menu(self):
        # ...existing code for menu creation...
        pass

    def _connect_signals(self):
        # ...existing code for connecting signals...
        pass

    def apply_settings(self):
        # ...existing code for applying settings...
        pass

    def open_file(self):
        # ...existing code for open_file...
        pass

    def save_file(self):
        # ...existing code for save_file...
        pass

    def show_settings(self):
        dlg = SettingsDialog(self, self.settings)
        if dlg.exec():
            self.settings = dlg.get_settings()
            save_settings(self.settings)
            from ui.theme import apply_theme
            from PySide6.QtWidgets import QApplication
            apply_theme(QApplication.instance())
            self.apply_settings()
            self.status_bar.showMessage("Settings updated.")
            self._log_action("Settings updated.")

    def toggle_theme(self):
        # ...existing code for toggle_theme...
        pass

    def toggle_debug_overlay(self):
        # ...existing code for toggle_debug_overlay...
        pass

    def show_log(self):
        self.log_window.show()
        self._log_action("Opened log window.")

    def show_about(self):
        # ...existing code for show_about...
        pass

    def screenshot(self):
        # ...existing code for screenshot...
        pass

    def keyPressEvent(self, event):
        # ...existing code for keyPressEvent...
        pass

    def mousePressEvent(self, event):
        # ...existing code for mousePressEvent...
        pass

    def mouseMoveEvent(self, event):
        # ...existing code for mouseMoveEvent...
        pass

    def mouseReleaseEvent(self, event):
        # ...existing code for mouseReleaseEvent...
        pass

    def _log_action(self, msg):
        self.log_window.append_log(f"[Secondary] {msg}")
