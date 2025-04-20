import sys
from PySide6 import QtWidgets
from ui.main_window import PrimaryMainWindow
from ui.theme import apply_theme

def main():
    app = QtWidgets.QApplication(sys.argv)
    apply_theme(app)  # Apply modern theme at startup
    window = PrimaryMainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
