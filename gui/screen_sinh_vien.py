# ============================================================
# Module: gui/screen_sinh_vien.py  -- P2
# ============================================================

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QTabWidget, QFrame,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from gui.ui_constants import (
    STYLE_NUT_CHINH, STYLE_NUT_THANH_CONG, STYLE_NUT_LOI, STYLE_NUT_PHU,
    MAU_CHINH, MAU_THANH_CONG, MAU_LOI, MAU_CANH_BAO,
    CO_CHU_NHO,
)
from gui.popup_error import hien_thi_popup_loi, hien_thi_popup_thanh_cong, hien_thi_popup_xac_nhan
from gui.screen_tkb import ScreenTKB
from gui.screen_lich_su import ScreenLichSu

from logic.kiem_tra import (
    kiem_tra_tien_quyet, kiem_tra_da_dang_ky, kiem_tra_xung_dot_lich, kiem_tra_si_so,
    LoiChuaDuDieuKienTienQuyet, LoiXungDotLichHoc, LoiLopHocDayCho, LoiDaDangKyMonNay,
)
from logic.file_handler import luu, xuat_phieu_dang_ky


class ScreenSinhVien(QWidget):

    def __init__(self, he_thong, sinh_vien):
        super().__init__()
        self.he_thong = he_thong
        self.sinh_vien = sinh_vien
        self._tao_giao_dien()

    def _tao_giao_dien(self):
        layout_chinh = QVBoxLayout(self)
        layout_chinh.setContentsMargins(0, 0, 0, 0)
        layout_chinh.setSpacing(0)

        # ── Thanh thông tin sinh viên ──
        thanh_sv = QWidget()
        thanh_sv.setStyleSheet("background-color: #1E293B; border-bottom: 1px solid #334155;")
        thanh_sv.setFixedHeight(56)
        layout_thanh = QHBoxLayout(thanh_sv)
        layout_thanh.setContentsMargins(24, 0, 24, 0)

        nhan_avatar = QLabel("👤")
        nhan_avatar.setStyleSheet("font-size: 20px; background: transparent;")
        layout_thanh.addWidget(nhan_avatar)

        nhan_ten = QLabel(self.sinh_vien.ho_ten)
        nhan_ten.setStyleSheet("color: #F1F5F9; font-size: 14px; font-weight: 700; background: transparent;")
        layout_thanh.addWidget(nhan_ten)

        layout_thanh.addSpacing(16)

        for nhan, gia_tri in [("Mã SV", self.sinh_vien.ma_sv), ("Lớp", self.sinh_vien.lop_sh)]:
            chip = QLabel(nhan + ": " + gia_tri)
            chip.setStyleSheet(
                "background-color: #334155; color: #93C5FD; border-radius: 12px;"
                "padding: 3px 12px; font-size: 12px; font-weight: 600;"
            )
            layout_thanh.addWidget(chip)
            layout_thanh.addSpacing(6)

        layout_thanh.addStretch()

        layout_chinh.addWidget(thanh_sv)

        # ── Tabs ──
        so_tab = QTabWidget()
        so_tab.setContentsMargins(12, 8, 12, 8)
        layout_chinh.addWidget(so_tab)

        tab_dk = QWidget()
        so_tab.addTab(tab_dk, "📋  Đăng ký học phần")
        self._tao_tab_dang_ky(tab_dk)

        self.man_hinh_tkb = ScreenTKB(self.sinh_vien)
        so_tab.addTab(self.man_hinh_tkb, "🗓  Thời khóa biểu")

        self.man_hinh_lich_su = ScreenLichSu(self.sinh_vien, self.he_thong)
        so_tab.addTab(self.man_hinh_lich_su, "📊  Lịch sử học tập")

    # ── Tab Đăng ký ──────────────────────────────────────────
    def _tao_tab_dang_ky(self, khung_cha):
        layout = QVBoxLayout(khung_cha)
        layout.setContentsMargins(16, 16, 16, 12)
        layout.setSpacing(12)

        # Tiêu đề + hướng dẫn
        layout_top = QHBoxLayout()
        tieu_de = QLabel("Danh sách lớp học phần mở trong học kỳ")
        tieu_de.setStyleSheet(
            "font-size: 16px; font-weight: 800; color: #F1F5F9;"
        )
        layout_top.addWidget(tieu_de)
        layout_top.addStretch()
        chu_thich = QLabel("💡 Chọn một dòng rồi bấm nút bên dưới")
        chu_thich.setStyleSheet("color: #64748B; font-size: 11px;")
        layout_top.addWidget(chu_thich)
        layout.addLayout(layout_top)

        # Bảng lớp học phần
        self.bang_lop = QTableWidget()
        self.bang_lop.setColumnCount(6)
        self.bang_lop.setHorizontalHeaderLabels(
            ["Mã lớp HP", "Tên môn học", "TC", "Giảng viên", "Lịch học", "Sĩ số"]
        )
        self.bang_lop.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.bang_lop.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.bang_lop.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.bang_lop.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.bang_lop.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.bang_lop.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.bang_lop.verticalHeader().setVisible(False)
        self.bang_lop.setAlternatingRowColors(True)
        self.bang_lop.setShowGrid(False)
        layout.addWidget(self.bang_lop)

        # Nhóm nút hành động
        layout_nut = QHBoxLayout()
        layout_nut.setSpacing(10)

        nut_dk = QPushButton("Đăng ký")
        nut_dk.setStyleSheet(STYLE_NUT_THANH_CONG)
        nut_dk.setFixedHeight(42)
        nut_dk.clicked.connect(self._xu_ly_dang_ky)
        layout_nut.addWidget(nut_dk)

        nut_huy = QPushButton("Hủy đăng ký")
        nut_huy.setStyleSheet(STYLE_NUT_LOI)
        nut_huy.setFixedHeight(42)
        nut_huy.clicked.connect(self._xu_ly_huy_dang_ky)
        layout_nut.addWidget(nut_huy)

        layout_nut.addStretch()

        nut_txt = QPushButton("📄  Xuất phiếu .txt")
        nut_txt.setStyleSheet(STYLE_NUT_PHU)
        nut_txt.setFixedHeight(42)
        nut_txt.clicked.connect(lambda: self._xu_ly_xuat_phieu("txt"))
        layout_nut.addWidget(nut_txt)

        nut_pdf = QPushButton("🖨  Xuất phiếu PDF")
        nut_pdf.setStyleSheet(STYLE_NUT_CHINH)
        nut_pdf.setFixedHeight(42)
        nut_pdf.clicked.connect(lambda: self._xu_ly_xuat_phieu("pdf"))
        layout_nut.addWidget(nut_pdf)

        layout.addLayout(layout_nut)
        self._ve_lai_bang_lop()

    def _ten_thu(self, so_thu):
        return {2:"Thứ 2",3:"Thứ 3",4:"Thứ 4",5:"Thứ 5",6:"Thứ 6",7:"Thứ 7"}.get(so_thu, "Thứ ?")

    def _ve_lai_bang_lop(self):
        ds = self.he_thong["lop_hoc_phan"]
        self.bang_lop.setRowCount(len(ds))

        # Tập hợp mã môn sinh viên đang đăng ký
        mon_da_dk = {l.mon_hoc.ma_mon for l in self.sinh_vien.ds_mon_dang_ky.duyet()}

        for hang, lop_hp in enumerate(ds):
            chu_lich = (self._ten_thu(lop_hp.lich_hoc["thu"])
                        + " · tiết " + str(lop_hp.lich_hoc["tiet_bat_dau"])
                        + "–" + str(lop_hp.lich_hoc["tiet_ket_thuc"]))
            chu_ss = str(len(lop_hp.danh_sach_sv)) + " / " + str(lop_hp.si_so_toi_da)

            cac_gia_tri = [
                lop_hp.ma_lop_hp,
                lop_hp.mon_hoc.ten_mon,
                str(lop_hp.mon_hoc.so_tin_chi),
                lop_hp.giang_vien,
                chu_lich,
                chu_ss,
            ]
            for cot, gia_tri in enumerate(cac_gia_tri):
                o = QTableWidgetItem(gia_tri)
                o.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)

                # Tô màu theo trạng thái
                if lop_hp.mon_hoc.ma_mon in mon_da_dk:
                    o.setForeground(QColor(MAU_THANH_CONG))
                elif not lop_hp.dang_mo or lop_hp.la_day():
                    o.setForeground(QColor("#64748B"))

                self.bang_lop.setItem(hang, cot, o)

            self.bang_lop.setRowHeight(hang, 40)

    def _lay_lop_chon(self):
        hang = self.bang_lop.currentRow()
        if hang < 0:
            return None
        o = self.bang_lop.item(hang, 0)
        if o is None:
            return None
        ma = o.text()
        for l in self.he_thong["lop_hoc_phan"]:
            if l.ma_lop_hp == ma:
                return l
        return None

    def _xu_ly_dang_ky(self):
        lop_hp = self._lay_lop_chon()
        if lop_hp is None:
            hien_thi_popup_loi("Vui lòng chọn một lớp học phần để đăng ký.", self)
            return
        if not lop_hp.dang_mo:
            hien_thi_popup_loi("Lớp học phần này đã bị đóng, không thể đăng ký.", self)
            return
        try:
            kiem_tra_tien_quyet(self.sinh_vien, lop_hp.mon_hoc)
            kiem_tra_da_dang_ky(self.sinh_vien, lop_hp)
            kiem_tra_xung_dot_lich(self.sinh_vien, lop_hp)
            kiem_tra_si_so(lop_hp)
            self.sinh_vien.dang_ky(lop_hp)
            luu(self.he_thong)
            hien_thi_popup_thanh_cong(
                "✅  Đăng ký thành công!\n\nMôn: " + lop_hp.mon_hoc.ten_mon
                + "\nLớp: " + lop_hp.ma_lop_hp, self
            )
        except (LoiChuaDuDieuKienTienQuyet, LoiXungDotLichHoc,
                LoiLopHocDayCho, LoiDaDangKyMonNay) as loi:
            hien_thi_popup_loi(loi.thong_bao, self)

        self._ve_lai_bang_lop()
        self.man_hinh_tkb.cap_nhat_du_lieu()

    def _xu_ly_huy_dang_ky(self):
        lop_hp = self._lay_lop_chon()
        if lop_hp is None:
            hien_thi_popup_loi("Vui lòng chọn một lớp học phần để hủy đăng ký.", self)
            return

        co_dang_ky = any(
            l.ma_lop_hp == lop_hp.ma_lop_hp
            for l in self.sinh_vien.ds_mon_dang_ky.duyet()
        )
        if not co_dang_ky:
            hien_thi_popup_loi("Bạn chưa đăng ký lớp học phần này.", self)
            return

        if not hien_thi_popup_xac_nhan(
            "Bạn có chắc muốn hủy đăng ký môn\n" + lop_hp.mon_hoc.ten_mon + " không?", self
        ):
            return

        self.sinh_vien.huy_dang_ky(lop_hp)
        luu(self.he_thong)
        hien_thi_popup_thanh_cong("Đã hủy đăng ký môn " + lop_hp.mon_hoc.ten_mon + ".", self)
        self._ve_lai_bang_lop()
        self.man_hinh_tkb.cap_nhat_du_lieu()

    def _xu_ly_xuat_phieu(self, dinh_dang):
        if len(self.sinh_vien.ds_mon_dang_ky) == 0:
            hien_thi_popup_loi("Bạn chưa đăng ký môn học nào để xuất phiếu.", self)
            return
        duong_dan = xuat_phieu_dang_ky(self.sinh_vien, dinh_dang)
        hien_thi_popup_thanh_cong("Đã xuất phiếu đăng ký tại:\n" + duong_dan, self)
