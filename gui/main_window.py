# ============================================================
# Module: gui/main_window.py  -- P1
# Cua so chinh cua ung dung, dieu phoi viec chuyen doi giua
# man hinh dang nhap, man hinh Sinh vien, va man hinh Admin.
# ============================================================

from PyQt6.QtWidgets import QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt

from gui.ui_constants import STYLE_NUT_PHU
from gui.screen_login import ScreenLogin
from gui.screen_sinh_vien import ScreenSinhVien
from gui.screen_admin import ScreenAdmin

from logic.file_handler import tai, luu
from data.data_mau import tao_du_lieu_mau


class MainWindow(QMainWindow):
    """
    Cua so chinh: chua mot QStackedWidget de chuyen doi qua lai
    giua man hinh dang nhap, man hinh Sinh vien, va man hinh Admin.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("He thong Quan ly Khoa hoc va Dang ky Tin chi")
        self.resize(1100, 750)

        # ----- Nap du lieu he thong -----
        # Thu doc tu file JSON truoc, neu chua co thi tao du lieu mau
        self.he_thong = tai("data/data.json")

        if len(self.he_thong["mon_hoc"]) == 0 and len(self.he_thong["sinh_vien"]) == 0:
            self.he_thong = tao_du_lieu_mau()
            luu(self.he_thong, "data/data.json")

        # ----- Khung chua, dung de chuyen doi giua cac man hinh -----
        self.khung_xep_lop = QStackedWidget()
        self.setCentralWidget(self.khung_xep_lop)

        self._hien_thi_man_hinh_dang_nhap()

    # ------------------------------------------------------------
    def _hien_thi_man_hinh_dang_nhap(self):
        """Xoa cac man hinh cu va hien thi man hinh dang nhap."""
        self._xoa_het_man_hinh_cu()

        man_hinh_login = ScreenLogin(self.he_thong, self._khi_dang_nhap_xong)
        self.khung_xep_lop.addWidget(man_hinh_login)
        self.khung_xep_lop.setCurrentWidget(man_hinh_login)

    def _xoa_het_man_hinh_cu(self):
        """Don dep cac widget cu trong QStackedWidget de tranh ton bo nho."""
        while self.khung_xep_lop.count() > 0:
            widget_cu = self.khung_xep_lop.widget(0)
            self.khung_xep_lop.removeWidget(widget_cu)
            widget_cu.deleteLater()

    def _khi_dang_nhap_xong(self, vai_tro, sinh_vien_hoac_None):
        """
        Callback duoc goi tu ScreenLogin sau khi nguoi dung chon vai tro.
        """
        self._xoa_het_man_hinh_cu()

        if vai_tro == "sinh_vien":
            man_hinh_chinh = ScreenSinhVien(self.he_thong, sinh_vien_hoac_None)
        else:  # vai_tro == "admin"
            man_hinh_chinh = ScreenAdmin(self.he_thong)

        # Boc them mot nut "Dang xuat" phia tren man hinh chinh
        khung_boc = QWidget()
        layout_boc = QVBoxLayout(khung_boc)
        layout_boc.setContentsMargins(0, 0, 0, 0)
        layout_boc.setSpacing(0)

        thanh_tren = QHBoxLayout()
        thanh_tren.setContentsMargins(10, 5, 10, 5)
        nut_dang_xuat = QPushButton("Đăng xuất / Quay lai đăng nhập")
        nut_dang_xuat.setStyleSheet(STYLE_NUT_PHU)
        nut_dang_xuat.setFixedWidth(250)
        nut_dang_xuat.clicked.connect(self._hien_thi_man_hinh_dang_nhap)
        thanh_tren.addStretch()
        thanh_tren.addWidget(nut_dang_xuat)
        layout_boc.addLayout(thanh_tren)

        layout_boc.addWidget(man_hinh_chinh)

        self.khung_xep_lop.addWidget(khung_boc)
        self.khung_xep_lop.setCurrentWidget(khung_boc)
