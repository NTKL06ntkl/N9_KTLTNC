# ============================================================
# Module: gui/screen_login.py  -- P2
# ============================================================

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QFrame,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from gui.ui_constants import STYLE_NUT_CHINH, STYLE_NUT_OUTLINE
from gui.popup_error import hien_thi_popup_loi


class ScreenLogin(QWidget):

    def __init__(self, he_thong, khi_dang_nhap_xong):
        super().__init__()
        self.he_thong = he_thong
        self.khi_dang_nhap_xong = khi_dang_nhap_xong
        self._tao_giao_dien()

    def _tao_giao_dien(self):
        layout_chinh = QVBoxLayout(self)
        layout_chinh.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Card trung tâm
        card = QFrame()
        card.setFixedWidth(460)
        card.setStyleSheet("""
            QFrame {
                background-color: #1E293B;
                border-radius: 16px;
                border: 1px solid #334155;
            }
        """)
        layout_card = QVBoxLayout(card)
        layout_card.setContentsMargins(40, 40, 40, 40)
        layout_card.setSpacing(24)

        # Logo + Tiêu đề
        nhan_logo = QLabel("🎓")
        nhan_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        nhan_logo.setStyleSheet("font-size: 48px; background: transparent; border: none;")
        layout_card.addWidget(nhan_logo)

        tieu_de = QLabel("Cổng Đăng ký Tín chỉ")
        tieu_de.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tieu_de.setStyleSheet(
            "font-size: 22px; font-weight: 800; color: #F1F5F9;"
            "background: transparent; border: none;"
        )
        layout_card.addWidget(tieu_de)

        mo_ta = QLabel("Hệ thống Quản lý Khóa học — Đăng ký Tín chỉ")
        mo_ta.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mo_ta.setStyleSheet("color: #64748B; font-size: 12px; background: transparent; border: none;")
        layout_card.addWidget(mo_ta)

        # Đường kẻ ngang
        duong_ke = QFrame()
        duong_ke.setFrameShape(QFrame.Shape.HLine)
        duong_ke.setStyleSheet("color: #334155; background: #334155; border: none; max-height: 1px;")
        layout_card.addWidget(duong_ke)

        # Chọn sinh viên
        nhan_sv = QLabel("Đăng nhập với tư cách Sinh viên")
        nhan_sv.setStyleSheet("color: #94A3B8; font-size: 12px; font-weight: 600;"
                               "background: transparent; border: none;")
        layout_card.addWidget(nhan_sv)

        self.combo_sv = QComboBox()
        self.combo_sv.setFixedHeight(42)
        for sv in self.he_thong["sinh_vien"]:
            self.combo_sv.addItem(sv.ma_sv + "  —  " + sv.ho_ten, sv)
        layout_card.addWidget(self.combo_sv)

        nut_sv = QPushButton("  Đăng nhập Sinh viên")
        nut_sv.setStyleSheet(STYLE_NUT_CHINH)
        nut_sv.setFixedHeight(44)
        nut_sv.clicked.connect(self._dang_nhap_sv)
        layout_card.addWidget(nut_sv)

        # Đường kẻ + label "HOẶC"
        layout_hoac = QHBoxLayout()
        ke_trai = QFrame()
        ke_trai.setFrameShape(QFrame.Shape.HLine)
        ke_trai.setStyleSheet("color: #334155; background: #334155; border: none; max-height: 1px;")
        nhan_hoac = QLabel("HOẶC")
        nhan_hoac.setStyleSheet("color: #475569; font-size: 11px; font-weight: 700;"
                                 "background: transparent; border: none; padding: 0 8px;")
        ke_phai = QFrame()
        ke_phai.setFrameShape(QFrame.Shape.HLine)
        ke_phai.setStyleSheet("color: #334155; background: #334155; border: none; max-height: 1px;")
        layout_hoac.addWidget(ke_trai)
        layout_hoac.addWidget(nhan_hoac)
        layout_hoac.addWidget(ke_phai)
        layout_card.addLayout(layout_hoac)

        nut_admin = QPushButton("  Vào trang Quản lý (Admin)")
        nut_admin.setStyleSheet(STYLE_NUT_OUTLINE)
        nut_admin.setFixedHeight(44)
        nut_admin.clicked.connect(self._dang_nhap_admin)
        layout_card.addWidget(nut_admin)

        layout_chinh.addWidget(card)

    def _dang_nhap_sv(self):
        if self.combo_sv.count() == 0:
            hien_thi_popup_loi("Không có sinh viên nào trong hệ thống.", self)
            return
        self.khi_dang_nhap_xong("sinh_vien", self.combo_sv.currentData())

    def _dang_nhap_admin(self):
        self.khi_dang_nhap_xong("admin", None)
