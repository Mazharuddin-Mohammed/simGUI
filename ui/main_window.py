from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QStatusBar, QFileDialog, QListWidget, QListWidgetItem, QMessageBox, QStyle
from PySide6.QtCore import Qt
from ui.log_window import SharedLogWindow
from ui.secondary_window import SecondaryMainWindow
from settings import load_settings, save_settings, add_recent_file
from ui.dialogs import SettingsDialog
import os

class PrimaryMainWindow(QMainWindow):
    """Primary window for project management, logo/banner, recent projects, and shared log."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulation Project Manager")
        self.settings = load_settings()
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        # Logo and banner
        logo_banner = QHBoxLayout()
        logo = QLabel()
        logo.setPixmap(self.style().standardIcon(QStyle.SP_ComputerIcon).pixmap(48, 48))
        logo_banner.addWidget(logo)
        banner = QLabel("<h1>Simulation Project Manager</h1>")
        logo_banner.addWidget(banner)
        logo_banner.addStretch(1)
        layout.addLayout(logo_banner)
        # Project management buttons
        btn_layout = QHBoxLayout()
        new_btn = QPushButton("New Project")
        open_btn = QPushButton("Open Project")
        edit_btn = QPushButton("Edit Project")
        prefs_btn = QPushButton("Preferences")
        btn_layout.addWidget(new_btn)
        btn_layout.addWidget(open_btn)
        btn_layout.addWidget(edit_btn)
        btn_layout.addWidget(prefs_btn)
        btn_layout.addStretch(1)
        layout.addLayout(btn_layout)
        # Recent projects list
        self.recent_label = QLabel("<b>Recent Projects:</b>")
        layout.addWidget(self.recent_label)
        self.recent_list = QListWidget()
        self.recent_list.itemClicked.connect(self.open_recent_project)
        layout.addWidget(self.recent_list)
        self.update_recent_projects()
        # Project info display
        self.project_info = QLabel()
        layout.addWidget(self.project_info)
        # Shared log window button
        log_btn = QPushButton("Show Log")
        log_btn.clicked.connect(self.show_log)
        layout.addWidget(log_btn, alignment=Qt.AlignLeft)
        self.setCentralWidget(central_widget)
        self.log_window = SharedLogWindow(self)
        self.secondary_window = None
        # Connect project management actions
        new_btn.clicked.connect(self.new_project)
        open_btn.clicked.connect(self.open_project)
        edit_btn.clicked.connect(self.edit_project)
        prefs_btn.clicked.connect(self.show_preferences)
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.log("Primary window started.")

    def update_recent_projects(self):
        self.recent_list.clear()
        for path in self.settings.get("recent_files", []):
            item = QListWidgetItem(os.path.basename(path))
            item.setToolTip(path)
            self.recent_list.addItem(item)

    def new_project(self):
        fname, _ = QFileDialog.getSaveFileName(self, "Create New Project", "", "Simulation Project (*.simproj)")
        if fname:
            if not fname.endswith('.simproj'):
                fname += '.simproj'
            with open(fname, 'w') as f:
                f.write("{}")  # Empty project file
            add_recent_file(self.settings, fname)
            save_settings(self.settings)
            self.update_recent_projects()
            self.display_project_info(fname)
            self.status_bar.showMessage(f"Created new project: {fname}")
            self.log(f"Created new project: {fname}")

    def open_project(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Open Project", "", "Simulation Project (*.simproj)")
        if fname:
            add_recent_file(self.settings, fname)
            save_settings(self.settings)
            self.update_recent_projects()
            self.display_project_info(fname)
            self.status_bar.showMessage(f"Opened project: {fname}")
            self.log(f"Opened project: {fname}")
            self.open_secondary(fname)

    def edit_project(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Edit Project", "", "Simulation Project (*.simproj)")
        if fname:
            add_recent_file(self.settings, fname)
            save_settings(self.settings)
            self.update_recent_projects()
            self.display_project_info(fname)
            self.status_bar.showMessage(f"Editing project: {fname}")
            self.log(f"Editing project: {fname}")
            self.open_secondary(fname)

    def open_recent_project(self, item):
        fname = item.toolTip()
        if os.path.exists(fname):
            add_recent_file(self.settings, fname)
            save_settings(self.settings)
            self.display_project_info(fname)
            self.status_bar.showMessage(f"Opened recent project: {fname}")
            self.log(f"Opened recent project: {fname}")
        else:
            QMessageBox.warning(self, "File Not Found", f"Project file not found: {fname}")
            self.settings["recent_files"].remove(fname)
            save_settings(self.settings)
            self.update_recent_projects()

    def display_project_info(self, fname):
        self.project_info.setText(f"<b>Project:</b> {os.path.basename(fname)}<br><b>Path:</b> {fname}")

    def show_preferences(self):
        dlg = SettingsDialog(self, self.settings)
        if dlg.exec():
            self.settings = dlg.get_settings()
            save_settings(self.settings)
            from ui.theme import apply_theme
            from PySide6.QtWidgets import QApplication
            apply_theme(QApplication.instance())
            self.status_bar.showMessage("Preferences updated.")
            self.log("Preferences updated.")

    def open_secondary(self, project_path=None):
        if not self.secondary_window:
            self.secondary_window = SecondaryMainWindow(self.log_window)
        self.secondary_window.show()
        self.log("Opened secondary window.")
        if project_path:
            self.secondary_window.setWindowTitle(f"Simulation Workflow - {os.path.basename(project_path)}")

    def show_log(self):
        from ui.theme import apply_theme
        from PySide6.QtWidgets import QApplication
        apply_theme(QApplication.instance())
        self.log_window.show()

    def log(self, msg):
        self.log_window.append_log(f"[Primary] {msg}")
