# ============================================================
# main.py -- Điểm khởi chạy ứng dụng
# Chạy: python main.py
# ============================================================
import sys
from PyQt6.QtWidgets import QApplication
from gui.main_window import MainWindow
from gui.ui_constants import GLOBAL_STYLE


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(GLOBAL_STYLE)
    cua_so = MainWindow()
    cua_so.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
