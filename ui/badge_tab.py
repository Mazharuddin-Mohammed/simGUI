from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton

class BadgeTabBar(QWidget):
    """A horizontal bar of badge-style tab buttons."""
    def __init__(self, tab_names, on_tab_clicked, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        self.buttons = []
        for name in tab_names:
            btn = QPushButton(name)
            btn.setCheckable(True)
            # Remove per-button setStyleSheet to allow global QSS to apply
            btn.clicked.connect(lambda checked, n=name: on_tab_clicked(n))
            layout.addWidget(btn)
            self.buttons.append(btn)
        layout.addStretch(1)
    def set_active(self, name):
        for btn in self.buttons:
            btn.setChecked(btn.text() == name)

from PySide6.QtWidgets import QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt

class TabContentWidget(QWidget):
    """A simple content widget for each tab with a Back button."""
    def __init__(self, title, on_back, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        label = QLabel(f"<h2>{title}</h2>")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        layout.addStretch(1)
        back_btn = QPushButton("Back")
        back_btn.setStyleSheet('padding: 6px 18px; border-radius: 10px; background: #6a8cff; color: #fff;')
        back_btn.clicked.connect(on_back)
        layout.addWidget(back_btn, alignment=Qt.AlignCenter)
