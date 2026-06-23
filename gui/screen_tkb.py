# ============================================================
# Module: gui/screen_tkb.py  -- P4
# Man hinh hien thi thoi khoa bieu tam thoi cua sinh vien
# dang dang nhap, dua tren cac lop hoc phan da dang ky.
# ============================================================

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView,
)
from PyQt6.QtCore import Qt

from gui.ui_constants import STYLE_TIEU_DE, STYLE_NEN_TRANG, CO_CHU_THAN


class ScreenTKB(QWidget):
    """
    Man hinh "Thoi khoa bieu tam thoi".

    Tham so:
        sinh_vien : object SinhVien dang dang nhap
    """

    def __init__(self, sinh_vien):
        super().__init__()
        self.sinh_vien = sinh_vien
        self.setStyleSheet(STYLE_NEN_TRANG)
        self._tao_giao_dien()

    def _tao_giao_dien(self):
        layout_chinh = QVBoxLayout(self)

        tieu_de = QLabel("THOI KHOA BIEU TAM THOI")
        tieu_de.setStyleSheet(STYLE_TIEU_DE)
        tieu_de.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_chinh.addWidget(tieu_de)

        self.bang = QTableWidget()
        self.bang.setColumnCount(5)
        self.bang.setHorizontalHeaderLabels(
            ["Thu", "Tiet hoc", "Ma lop HP", "Mon hoc", "Giang vien"]
        )
        self.bang.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.bang.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.bang.verticalHeader().setVisible(False)
        layout_chinh.addWidget(self.bang)

        self.nhan_tong_tin_chi = QLabel("")
        self.nhan_tong_tin_chi.setStyleSheet(
            "font-size: " + str(CO_CHU_THAN) + "px; font-weight: bold;"
        )
        layout_chinh.addWidget(self.nhan_tong_tin_chi)

        self.cap_nhat_du_lieu()

    def _ten_thu(self, so_thu):
        tu_dien_thu = {2: "Thu 2", 3: "Thu 3", 4: "Thu 4", 5: "Thu 5", 6: "Thu 6", 7: "Thu 7"}
        return tu_dien_thu.get(so_thu, "Thu " + str(so_thu))

    def cap_nhat_du_lieu(self):
        """
        Ve lai bang thoi khoa bieu theo danh sach lop hoc phan
        ma sinh vien dang dang ky (sinh_vien.ds_mon_dang_ky).
        Goi lai ham nay ngay sau khi dang ky / huy dang ky thanh cong.
        """
        danh_sach_lop = self.sinh_vien.ds_mon_dang_ky.duyet()

        # Sap xep theo thu, sau do theo tiet bat dau, de de nhin
        danh_sach_lop_sap_xep = sorted(
            danh_sach_lop,
            key=lambda lop: (lop.lich_hoc["thu"], lop.lich_hoc["tiet_bat_dau"])
        )

        self.bang.setRowCount(len(danh_sach_lop_sap_xep))

        tong_tin_chi = 0
        for hang, lop_hp in enumerate(danh_sach_lop_sap_xep):
            tong_tin_chi = tong_tin_chi + lop_hp.mon_hoc.so_tin_chi

            chu_tiet = str(lop_hp.lich_hoc["tiet_bat_dau"]) + "-" + str(lop_hp.lich_hoc["tiet_ket_thuc"])

            self.bang.setItem(hang, 0, QTableWidgetItem(self._ten_thu(lop_hp.lich_hoc["thu"])))
            self.bang.setItem(hang, 1, QTableWidgetItem(chu_tiet))
            self.bang.setItem(hang, 2, QTableWidgetItem(lop_hp.ma_lop_hp))
            self.bang.setItem(hang, 3, QTableWidgetItem(lop_hp.mon_hoc.ten_mon))
            self.bang.setItem(hang, 4, QTableWidgetItem(lop_hp.giang_vien))

        self.nhan_tong_tin_chi.setText("Tong so tin chi da dang ky: " + str(tong_tin_chi))
