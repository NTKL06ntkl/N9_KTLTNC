from PyQt6.QtWidgets import (
    QMainWindow, QStackedWidget, QWidget, QVBoxLayout,
    QPushButton, QHBoxLayout, QLabel,
)
from PyQt6.QtCore import Qt

from gui.ui_constants import STYLE_NUT_OUTLINE
from gui.screen_login import ScreenLogin
from gui.screen_sinh_vien import ScreenSinhVien
from gui.screen_admin import ScreenAdmin

from logic.file_handler import tai, luu
from data.data_mau import tao_du_lieu_mau


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hệ thống Quản lý Khóa học & Đăng ký Tín chỉ")
        self.resize(1200, 780)

        self.he_thong = tai("data/data.json")
        if len(self.he_thong["mon_hoc"]) == 0 and len(self.he_thong["sinh_vien"]) == 0:
            self.he_thong = tao_du_lieu_mau()
            luu(self.he_thong, "data/data.json")

        self.khung_xep_lop = QStackedWidget()
        self.setCentralWidget(self.khung_xep_lop)
        self._hien_thi_man_hinh_dang_nhap()

    def _hien_thi_man_hinh_dang_nhap(self):
        self._xoa_het_man_hinh_cu()
        man_hinh_login = ScreenLogin(self.he_thong, self._khi_dang_nhap_xong)
        self.khung_xep_lop.addWidget(man_hinh_login)
        self.khung_xep_lop.setCurrentWidget(man_hinh_login)

    def _xoa_het_man_hinh_cu(self):
        while self.khung_xep_lop.count() > 0:
            w = self.khung_xep_lop.widget(0)
            self.khung_xep_lop.removeWidget(w)
            w.deleteLater()

    def _khi_dang_nhap_xong(self, vai_tro, sinh_vien):
        self._xoa_het_man_hinh_cu()

        if vai_tro == "sinh_vien":
            man_hinh = ScreenSinhVien(self.he_thong, sinh_vien)
        else:
            man_hinh = ScreenAdmin(self.he_thong)

        # Wrapper thêm thanh top với nút đăng xuất
        wrapper = QWidget()
        layout = QVBoxLayout(wrapper)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Thanh top
        thanh_top = QWidget()
        thanh_top.setStyleSheet("background-color: #0F172A; border-bottom: 1px solid #334155;")
        thanh_top.setFixedHeight(48)
        layout_top = QHBoxLayout(thanh_top)
        layout_top.setContentsMargins(16, 0, 16, 0)

        logo = QLabel("🎓  Cổng Đăng ký Tín chỉ")
        logo.setStyleSheet("color: #3B82F6; font-size: 15px; font-weight: 800;")
        layout_top.addWidget(logo)
        layout_top.addStretch()

        nut_xuat = QPushButton("⬅  Đăng xuất")
        nut_xuat.setStyleSheet(STYLE_NUT_OUTLINE)
        nut_xuat.setFixedHeight(32)
        nut_xuat.clicked.connect(self._hien_thi_man_hinh_dang_nhap)
        layout_top.addWidget(nut_xuat)

        layout.addWidget(thanh_top)
        layout.addWidget(man_hinh)

        self.khung_xep_lop.addWidget(wrapper)
        self.khung_xep_lop.setCurrentWidget(wrapper)
