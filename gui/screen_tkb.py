# ============================================================
# Module: gui/screen_tkb.py  -- P4
# ============================================================

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QHeaderView, QFrame,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor


class ScreenTKB(QWidget):

    def __init__(self, sinh_vien):
        super().__init__()
        self.sinh_vien = sinh_vien
        self._tao_giao_dien()

    def _tao_giao_dien(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(14)

        layout_top = QHBoxLayout()
        tieu_de = QLabel("Thời khóa biểu tạm thời")
        tieu_de.setStyleSheet("font-size: 16px; font-weight: 800; color: #F1F5F9;")
        layout_top.addWidget(tieu_de)
        layout_top.addStretch()
        self.nhan_tong = QLabel("Tổng: 0 tín chỉ")
        self.nhan_tong.setStyleSheet(
            "background-color: #1E3A5F; color: #93C5FD; border-radius: 12px;"
            "padding: 4px 14px; font-size: 13px; font-weight: 700;"
        )
        layout_top.addWidget(self.nhan_tong)
        layout.addLayout(layout_top)

        self.bang = QTableWidget()
        self.bang.setColumnCount(5)
        self.bang.setHorizontalHeaderLabels(
            ["Thứ", "Tiết", "Mã lớp HP", "Tên môn học", "Giảng viên"]
        )
        self.bang.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.bang.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.bang.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.bang.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.bang.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.bang.verticalHeader().setVisible(False)
        self.bang.setAlternatingRowColors(True)
        self.bang.setShowGrid(False)
        layout.addWidget(self.bang)

        self.cap_nhat_du_lieu()

    def _ten_thu(self, n):
        return {2:"Thứ 2",3:"Thứ 3",4:"Thứ 4",5:"Thứ 5",6:"Thứ 6",7:"Thứ 7"}.get(n,"Thứ ?")

    def cap_nhat_du_lieu(self):
        ds = sorted(
            self.sinh_vien.ds_mon_dang_ky.duyet(),
            key=lambda l: (l.lich_hoc["thu"], l.lich_hoc["tiet_bat_dau"])
        )
        self.bang.setRowCount(len(ds))
        tong_tc = 0

        mau_thu = {
            2:"#1E3A5F", 3:"#1B3A2E", 4:"#3B2A1E",
            5:"#2A1E3B", 6:"#1E2E3B", 7:"#3B1E2A"
        }

        for hang, l in enumerate(ds):
            tong_tc += l.mon_hoc.so_tin_chi
            tiet = str(l.lich_hoc["tiet_bat_dau"]) + "–" + str(l.lich_hoc["tiet_ket_thuc"])
            mau_nen = mau_thu.get(l.lich_hoc["thu"], "#1E293B")

            for cot, text in enumerate([
                self._ten_thu(l.lich_hoc["thu"]),
                tiet,
                l.ma_lop_hp,
                l.mon_hoc.ten_mon,
                l.giang_vien,
            ]):
                o = QTableWidgetItem(text)
                o.setBackground(QColor(mau_nen))
                self.bang.setItem(hang, cot, o)
            self.bang.setRowHeight(hang, 40)

        self.nhan_tong.setText("Tổng: " + str(tong_tc) + " tín chỉ")
