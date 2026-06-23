# ============================================================
# Module: gui/screen_mon_hoc.py  -- P1
# Man hinh hien thi danh sach mon hoc trong he thong,
# kem mon tien quyet cua tung mon (neu co).
# ============================================================

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView,
)
from PyQt6.QtCore import Qt

from gui.ui_constants import STYLE_TIEU_DE, STYLE_NEN_TRANG


class ScreenMonHoc(QWidget):
    """
    Man hinh "Danh sach mon hoc".

    Tham so:
        he_thong : dict du lieu he thong, co khoa "mon_hoc" la list MonHoc
    """

    def __init__(self, he_thong):
        super().__init__()
        self.he_thong = he_thong
        self.setStyleSheet(STYLE_NEN_TRANG)
        self._tao_giao_dien()

    def _tao_giao_dien(self):
        layout_chinh = QVBoxLayout(self)

        tieu_de = QLabel("DANH SACH MON HOC")
        tieu_de.setStyleSheet(STYLE_TIEU_DE)
        tieu_de.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_chinh.addWidget(tieu_de)

        # Bang hien thi danh sach mon hoc bang QTableWidget
        self.bang = QTableWidget()
        self.bang.setColumnCount(4)
        self.bang.setHorizontalHeaderLabels(
            ["Ma mon", "Ten mon", "So tin chi", "Mon tien quyet"]
        )
        self.bang.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.bang.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.bang.verticalHeader().setVisible(False)
        layout_chinh.addWidget(self.bang)

        self.cap_nhat_du_lieu()

    def cap_nhat_du_lieu(self):
        """
        Xoa toan bo du lieu cu trong bang va ve lai theo
        danh sach mon hoc hien tai trong self.he_thong.
        Goi ham nay moi khi danh sach mon hoc thay doi (P5 them mon moi).
        """
        # Tao tu dien tra cuu ten mon theo ma mon (de hien ten mon tien quyet)
        tu_dien_ten_mon = {}
        for mon in self.he_thong["mon_hoc"]:
            tu_dien_ten_mon[mon.ma_mon] = mon.ten_mon

        danh_sach_mon = self.he_thong["mon_hoc"]
        self.bang.setRowCount(len(danh_sach_mon))

        for hang, mon in enumerate(danh_sach_mon):
            if mon.ma_mon_tien_quyet is None:
                chu_tien_quyet = "Khong co"
            else:
                ten_mon_tq = tu_dien_ten_mon.get(mon.ma_mon_tien_quyet, mon.ma_mon_tien_quyet)
                chu_tien_quyet = mon.ma_mon_tien_quyet + " - " + ten_mon_tq

            self.bang.setItem(hang, 0, QTableWidgetItem(mon.ma_mon))
            self.bang.setItem(hang, 1, QTableWidgetItem(mon.ten_mon))
            self.bang.setItem(hang, 2, QTableWidgetItem(str(mon.so_tin_chi)))
            self.bang.setItem(hang, 3, QTableWidgetItem(chu_tien_quyet))
