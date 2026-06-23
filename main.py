# ============================================================
# main.py
# Diem khoi chay chinh cua ung dung.
#
# Cach chay:
#   1. Cai dat thu vien can thiet:
#        pip install -r requirements.txt
#   2. Chay lenh:
#        python main.py
# ============================================================

import sys
from PyQt6.QtWidgets import QApplication

from gui.main_window import MainWindow


def main():
    ung_dung = QApplication(sys.argv)

    cua_so_chinh = MainWindow()
    cua_so_chinh.show()

    sys.exit(ung_dung.exec())


if __name__ == "__main__":
    main()
