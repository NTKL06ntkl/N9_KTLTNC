# ============================================================
# Module: gui/screen_lich_su.py  -- P2
# Man hinh hien thi lich su hoc tap: cac mon da hoc xong,
# diem so tung mon, va diem trung binh (DTB) cua sinh vien.
# ============================================================

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView,
)
from PyQt6.QtCore import Qt

from gui.ui_constants import STYLE_TIEU_DE, STYLE_NEN_TRANG, CO_CHU_THAN


class ScreenLichSu(QWidget):
    """
    Man hinh "Lich su hoc tap".

    Tham so:
        sinh_vien : object SinhVien dang dang nhap
        he_thong  : dict du lieu he thong, dung de tra ten mon + tin chi
    """

    def __init__(self, sinh_vien, he_thong):
        super().__init__()
        self.sinh_vien = sinh_vien
        self.he_thong = he_thong
        self.setStyleSheet(STYLE_NEN_TRANG)
        self._tao_giao_dien()

    def _tao_giao_dien(self):
        layout_chinh = QVBoxLayout(self)

        tieu_de = QLabel("LICH SU HOC TAP")
        tieu_de.setStyleSheet(STYLE_TIEU_DE)
        tieu_de.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_chinh.addWidget(tieu_de)

        self.bang = QTableWidget()
        self.bang.setColumnCount(4)
        self.bang.setHorizontalHeaderLabels(
            ["Ma mon", "Ten mon", "So tin chi", "Diem"]
        )
        self.bang.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.bang.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.bang.verticalHeader().setVisible(False)
        layout_chinh.addWidget(self.bang)

        self.nhan_dtb = QLabel("")
        self.nhan_dtb.setStyleSheet(
            "font-size: " + str(CO_CHU_THAN) + "px; font-weight: bold;"
        )
        layout_chinh.addWidget(self.nhan_dtb)

        self.cap_nhat_du_lieu()

    def cap_nhat_du_lieu(self):
        """
        Ve lai bang ket qua hoc tap theo sinh_vien.diem_cac_mon.
        Goi lai ham nay sau khi sinh vien duoc cap nhat them mon da hoc.
        """
        # Tao tu dien tra cuu MonHoc theo ma mon, de biet ten mon + so tin chi
        tu_dien_mon = {}
        for mon in self.he_thong["mon_hoc"]:
            tu_dien_mon[mon.ma_mon] = mon

        danh_sach_ma_mon = list(self.sinh_vien.diem_cac_mon.keys())
        self.bang.setRowCount(len(danh_sach_ma_mon))

        for hang, ma_mon in enumerate(danh_sach_ma_mon):
            diem = self.sinh_vien.diem_cac_mon[ma_mon]
            mon = tu_dien_mon.get(ma_mon)

            if mon is not None:
                ten_mon = mon.ten_mon
                chu_so_tin_chi = str(mon.so_tin_chi)
            else:
                ten_mon = "(khong ro)"
                chu_so_tin_chi = "-"

            self.bang.setItem(hang, 0, QTableWidgetItem(ma_mon))
            self.bang.setItem(hang, 1, QTableWidgetItem(ten_mon))
            self.bang.setItem(hang, 2, QTableWidgetItem(chu_so_tin_chi))
            self.bang.setItem(hang, 3, QTableWidgetItem(str(diem)))

        # Tinh DTB co trong so tin chi
        dtb = self.sinh_vien.tinh_dtb_co_trong_so(self.he_thong["mon_hoc"])
        self.nhan_dtb.setText("Diem trung binh (DTB): " + str(dtb))
