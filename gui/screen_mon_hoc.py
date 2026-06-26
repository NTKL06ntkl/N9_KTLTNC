from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QHeaderView,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor


class ScreenMonHoc(QWidget):

    def __init__(self, he_thong):
        super().__init__()
        self.he_thong = he_thong
        self._tao_giáo_dien()

    def _tao_giao_dien(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        layout_top = QHBoxLayout()
        tieu_de = QLabel("Danh sách môn học")
        tieu_de.setStyleSheet("font-size: 16px; font-weight: 800; color: #F1F5F9;")
        layout_top.addWidget(tieu_de)
        layout_top.addStretch()
        nhan_so = QLabel(str(len(self.he_thong["mon_hoc"])) + " môn học")
        nhan_so.setStyleSheet(
            "background-color: #334155; color: #94A3B8; border-radius: 10px;"
            "padding: 3px 12px; font-size: 11px; font-weight: 700;"
        )
        layout_top.addWidget(nhan_so)
        layout.addLayout(layout_top)

        self.bang = QTableWidget()
        self.bang.setColumnCount(4)
        self.bang.setHorizontalHeaderLabels(
            ["Mã môn", "Tên môn học", "Số tín chỉ", "Môn tiên quyết"]
        )
        self.bang.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.bang.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.bang.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.bang.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.bang.verticalHeader().setVisible(False)
        self.bang.setAlternatingRowColors(True)
        self.bang.setShowGrid(False)
        layout.addWidget(self.bang)

        self.cap_nhat_du_lieu()

    def cap_nhat_du_lieu(self):
        tu_dien = {m.ma_mon: m.ten_mon for m in self.he_thong["mon_hoc"]}
        ds = self.he_thong["mon_hoc"]
        self.bang.setRowCount(len(ds))

        for hang, mon in enumerate(ds):
            tq = ("—" if mon.ma_mon_tien_quyet is None
                  else mon.ma_mon_tien_quyet + "  ·  " + tu_dien.get(mon.ma_mon_tien_quyet, ""))

            for cot, val in enumerate([mon.ma_mon, mon.ten_mon, str(mon.so_tin_chi), tq]):
                o = QTableWidgetItem(val)
                if cot == 2:
                    o.setTextAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
                    o.setForeground(QColor("#93C5FD"))
                if cot == 3 and mon.ma_mon_tien_quyet:
                    o.setForeground(QColor("#F59E0B"))
                self.bang.setItem(hang, cot, o)
            self.bang.setRowHeight(hang, 40)
