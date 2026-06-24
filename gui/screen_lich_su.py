# ============================================================
# Module: gui/screen_lich_su.py  -- P2
# ============================================================

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QHeaderView, QFrame,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor


class ScreenLichSu(QWidget):

    def __init__(self, sinh_vien, he_thong):
        super().__init__()
        self.sinh_vien = sinh_vien
        self.he_thong = he_thong
        self._tao_giao_dien()

    def _tao_giao_dien(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(14)

        layout_top = QHBoxLayout()
        tieu_de = QLabel("Lịch sử học tập")
        tieu_de.setStyleSheet("font-size: 16px; font-weight: 800; color: #F1F5F9;")
        layout_top.addWidget(tieu_de)
        layout_top.addStretch()
        self.nhan_dtb = QLabel("ĐTB: —")
        self.nhan_dtb.setStyleSheet(
            "background-color: #064E3B; color: #6EE7B7; border-radius: 12px;"
            "padding: 4px 14px; font-size: 13px; font-weight: 700;"
        )
        layout_top.addWidget(self.nhan_dtb)
        layout.addLayout(layout_top)

        self.bang = QTableWidget()
        self.bang.setColumnCount(4)
        self.bang.setHorizontalHeaderLabels(["Mã môn", "Tên môn học", "Số tín chỉ", "Điểm"])
        self.bang.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.bang.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.bang.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.bang.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.bang.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.bang.verticalHeader().setVisible(False)
        self.bang.setAlternatingRowColors(True)
        self.bang.setShowGrid(False)
        layout.addWidget(self.bang)

        self.cap_nhat_du_lieu()

    def cap_nhat_du_lieu(self):
        tu_dien = {m.ma_mon: m for m in self.he_thong["mon_hoc"]}
        ds = list(self.sinh_vien.diem_cac_mon.keys())
        self.bang.setRowCount(len(ds))

        for hang, ma in enumerate(ds):
            diem = self.sinh_vien.diem_cac_mon[ma]
            mon = tu_dien.get(ma)
            ten = mon.ten_mon if mon else "(không rõ)"
            tc  = str(mon.so_tin_chi) if mon else "—"

            for cot, val in enumerate([ma, ten, tc, str(diem)]):
                o = QTableWidgetItem(val)
                # Tô màu cột điểm theo mức
                if cot == 3:
                    if diem >= 8.5:
                        o.setForeground(QColor("#10B981"))
                    elif diem >= 7.0:
                        o.setForeground(QColor("#3B82F6"))
                    elif diem >= 5.0:
                        o.setForeground(QColor("#F59E0B"))
                    else:
                        o.setForeground(QColor("#EF4444"))
                self.bang.setItem(hang, cot, o)
            self.bang.setRowHeight(hang, 40)

        dtb = self.sinh_vien.tinh_dtb_co_trong_so(self.he_thong["mon_hoc"])
        self.nhan_dtb.setText("ĐTB: " + str(dtb))
