# ============================================================
# Module: gui/screen_login.py  -- P2
# Man hinh dang nhap: cho phep nguoi dung chon vai tro
# (Sinh vien hoac Quan ly) va chon ma sinh vien (neu la sinh vien).
# ============================================================

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QGroupBox, QFrame,
)
from PyQt6.QtCore import Qt

from gui.ui_constants import (
    STYLE_NUT_CHINH, STYLE_TIEU_DE, STYLE_NEN_TRANG, CO_CHU_THAN,
)
from gui.popup_error import hien_thi_popup_loi


class ScreenLogin(QWidget):
    """
    Man hinh dang nhap.

    Tham so:
        he_thong : dict du lieu he thong, co khoa "sinh_vien" la list SinhVien
        khi_dang_nhap_xong : ham callback, duoc goi voi 2 tham so
                              (vai_tro, sinh_vien_hoac_None)
                              vai_tro la chuoi "sinh_vien" hoac "admin"
    """

    def __init__(self, he_thong, khi_dang_nhap_xong):
        super().__init__()
        self.he_thong = he_thong
        self.khi_dang_nhap_xong = khi_dang_nhap_xong
        self.setStyleSheet(STYLE_NEN_TRANG)
        self._tao_giao_dien()

    def _tao_giao_dien(self):
        layout_chinh = QVBoxLayout(self)
        layout_chinh.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ----- Tieu de -----
        tieu_de = QLabel("CONG DANG KY TIN CHI")
        tieu_de.setStyleSheet(STYLE_TIEU_DE)
        tieu_de.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_chinh.addWidget(tieu_de)
        layout_chinh.addSpacing(20)

        # ----- Khung dang nhap Sinh vien -----
        khung_sv = QGroupBox("Dang nhap Sinh vien")
        khung_sv.setFixedWidth(400)
        layout_sv = QVBoxLayout()

        nhan_chon_sv = QLabel("Chon ma sinh vien:")
        layout_sv.addWidget(nhan_chon_sv)

        self.combo_sv = QComboBox()
        for sv in self.he_thong["sinh_vien"]:
            # Luu object SinhVien lam "data" gan kem voi dong hien thi
            self.combo_sv.addItem(sv.ma_sv + " - " + sv.ho_ten, sv)
        layout_sv.addWidget(self.combo_sv)

        nut_dang_nhap_sv = QPushButton("Dang nhap Sinh vien")
        nut_dang_nhap_sv.setStyleSheet(STYLE_NUT_CHINH)
        nut_dang_nhap_sv.clicked.connect(self._dang_nhap_sinh_vien)
        layout_sv.addWidget(nut_dang_nhap_sv)

        khung_sv.setLayout(layout_sv)
        layout_chinh.addWidget(khung_sv)
        layout_chinh.addSpacing(15)

        # ----- Khung dang nhap Admin -----
        khung_admin = QGroupBox("Dang nhap Quan ly (Admin)")
        khung_admin.setFixedWidth(400)
        layout_admin = QVBoxLayout()

        nut_dang_nhap_admin = QPushButton("Vao trang Quan ly")
        nut_dang_nhap_admin.setStyleSheet(STYLE_NUT_CHINH)
        nut_dang_nhap_admin.clicked.connect(self._dang_nhap_admin)
        layout_admin.addWidget(nut_dang_nhap_admin)

        khung_admin.setLayout(layout_admin)
        layout_chinh.addWidget(khung_admin)

    def _dang_nhap_sinh_vien(self):
        if self.combo_sv.count() == 0:
            hien_thi_popup_loi("Khong co sinh vien nao trong he thong.", self)
            return

        # Lay object SinhVien da gan kem theo dong dang chon trong combo box
        sinh_vien_dang_chon = self.combo_sv.currentData()
        self.khi_dang_nhap_xong("sinh_vien", sinh_vien_dang_chon)

    def _dang_nhap_admin(self):
        self.khi_dang_nhap_xong("admin", None)
