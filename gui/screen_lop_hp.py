# ============================================================
# Module: gui/screen_lop_hp.py  -- P1
# ============================================================

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QHeaderView,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor


class ScreenLopHP(QWidget):

    def __init__(self, he_thong):
        super().__init__()
        self.he_thong = he_thong
        self._tao_giao_dien()

    def _tao_giao_dien(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        layout_top = QHBoxLayout()
        tieu_de = QLabel("Danh sách lớp học phần")
        tieu_de.setStyleSheet("font-size: 16px; font-weight: 800; color: #F1F5F9;")
        layout_top.addWidget(tieu_de)
        layout_top.addStretch()
        layout.addLayout(layout_top)

        self.bang = QTableWidget()
        self.bang.setColumnCount(6)
        self.bang.setHorizontalHeaderLabels(
            ["Mã lớp HP", "Môn học", "Giảng viên", "Lịch học", "Sĩ số", "Trạng thái"]
        )
        self.bang.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.bang.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.bang.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.bang.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        self.bang.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.bang.verticalHeader().setVisible(False)
        self.bang.setAlternatingRowColors(True)
        self.bang.setShowGrid(False)
        layout.addWidget(self.bang)

        self.cap_nhat_du_lieu()

    def _ten_thu(self, n):
        return {2:"Thứ 2",3:"Thứ 3",4:"Thứ 4",5:"Thứ 5",6:"Thứ 6",7:"Thứ 7"}.get(n,"?")

    def cap_nhat_du_lieu(self):
        ds = self.he_thong["lop_hoc_phan"]
        self.bang.setRowCount(len(ds))
        for hang, l in enumerate(ds):
            lich = (self._ten_thu(l.lich_hoc["thu"])
                    + " · tiết " + str(l.lich_hoc["tiet_bat_dau"])
                    + "–" + str(l.lich_hoc["tiet_ket_thuc"]))
            ss = str(len(l.danh_sach_sv)) + " / " + str(l.si_so_toi_da)

            if not l.dang_mo:
                tt, mau_tt = "Đã đóng", "#EF4444"
            elif l.la_day():
                tt, mau_tt = "Đã đầy", "#F59E0B"
            else:
                tt, mau_tt = "Còn chỗ", "#10B981"

            for cot, val in enumerate([l.ma_lop_hp, l.mon_hoc.ten_mon, l.giang_vien, lich, ss, tt]):
                o = QTableWidgetItem(val)
                if cot == 5:
                    o.setForeground(QColor(mau_tt))
                self.bang.setItem(hang, cot, o)
            self.bang.setRowHeight(hang, 40)
