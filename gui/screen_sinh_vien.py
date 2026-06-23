# ============================================================
# Module: gui/screen_sinh_vien.py  -- P2
# Man hinh chinh cua phan he Sinh vien: hien thi danh sach
# lop hoc phan mo, cho phep dang ky / huy dang ky, xem TKB,
# xem lich su hoc tap, va xuat phieu dang ky.
# ============================================================

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QTabWidget,
)
from PyQt6.QtCore import Qt

from gui.ui_constants import (
    STYLE_NUT_CHINH, STYLE_NUT_THANH_CONG, STYLE_NUT_LOI, STYLE_NUT_PHU,
    STYLE_TIEU_DE, STYLE_NEN_TRANG, STYLE_THANH_THONG_TIN, CO_CHU_NHO,
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
    """
    Man hinh chinh cho Sinh vien.

    Tham so:
        he_thong  : dict du lieu he thong (mon_hoc, lop_hoc_phan, sinh_vien)
        sinh_vien : object SinhVien dang dang nhap
    """

    def __init__(self, he_thong, sinh_vien):
        super().__init__()
        self.he_thong = he_thong
        self.sinh_vien = sinh_vien
        self.setStyleSheet(STYLE_NEN_TRANG)
        self._tao_giao_dien()

    def _tao_giao_dien(self):
        layout_chinh = QVBoxLayout(self)
        layout_chinh.setContentsMargins(0, 0, 0, 0)

        # ----- Thanh thong tin sinh vien dang dang nhap -----
        thanh_thong_tin = QLabel(
            "Sinh vien: " + self.sinh_vien.ho_ten
            + "   |   Ma SV: " + self.sinh_vien.ma_sv
            + "   |   Lop: " + self.sinh_vien.lop_sh
        )
        thanh_thong_tin.setStyleSheet(STYLE_THANH_THONG_TIN)
        layout_chinh.addWidget(thanh_thong_tin)

        # ----- Tab dieu huong: Dang ky / TKB / Lich su -----
        so_tab = QTabWidget()
        layout_chinh.addWidget(so_tab)

        # Tab 1: Dang ky hoc phan
        tab_dang_ky = QWidget()
        so_tab.addTab(tab_dang_ky, "Dang ky hoc phan")
        self._tao_tab_dang_ky(tab_dang_ky)

        # Tab 2: Thoi khoa bieu
        self.man_hinh_tkb = ScreenTKB(self.sinh_vien)
        so_tab.addTab(self.man_hinh_tkb, "Thoi khoa bieu")

        # Tab 3: Lich su hoc tap
        self.man_hinh_lich_su = ScreenLichSu(self.sinh_vien, self.he_thong)
        so_tab.addTab(self.man_hinh_lich_su, "Lich su hoc tap")

    # ------------------------------------------------------------
    # TAB 1: DANG KY HOC PHAN
    # ------------------------------------------------------------
    def _tao_tab_dang_ky(self, khung_cha):
        layout_tab = QVBoxLayout(khung_cha)

        tieu_de = QLabel("DANH SACH LOP HOC PHAN MO TRONG HOC KY")
        tieu_de.setStyleSheet(STYLE_TIEU_DE)
        tieu_de.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_tab.addWidget(tieu_de)

        self.bang_lop = QTableWidget()
        self.bang_lop.setColumnCount(6)
        self.bang_lop.setHorizontalHeaderLabels(
            ["Ma lop HP", "Mon hoc", "TC", "Giang vien", "Lich hoc", "Si so"]
        )
        self.bang_lop.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.bang_lop.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.bang_lop.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.bang_lop.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.bang_lop.verticalHeader().setVisible(False)
        layout_tab.addWidget(self.bang_lop)

        # ----- Khu vuc nut hanh dong -----
        layout_nut = QHBoxLayout()

        nut_dang_ky = QPushButton("Dang ky lop da chon")
        nut_dang_ky.setStyleSheet(STYLE_NUT_THANH_CONG)
        nut_dang_ky.clicked.connect(self._xu_ly_dang_ky)
        layout_nut.addWidget(nut_dang_ky)

        nut_huy = QPushButton("Huy dang ky lop da chon")
        nut_huy.setStyleSheet(STYLE_NUT_LOI)
        nut_huy.clicked.connect(self._xu_ly_huy_dang_ky)
        layout_nut.addWidget(nut_huy)

        nut_xuat_txt = QPushButton("Xuat phieu (.txt)")
        nut_xuat_txt.setStyleSheet(STYLE_NUT_PHU)
        nut_xuat_txt.clicked.connect(lambda: self._xu_ly_xuat_phieu("txt"))
        layout_nut.addWidget(nut_xuat_txt)

        nut_xuat_pdf = QPushButton("Xuat phieu (.pdf)")
        nut_xuat_pdf.setStyleSheet(STYLE_NUT_CHINH)
        nut_xuat_pdf.clicked.connect(lambda: self._xu_ly_xuat_phieu("pdf"))
        layout_nut.addWidget(nut_xuat_pdf)

        layout_tab.addLayout(layout_nut)

        # Chu thich nho huong dan
        chu_thich = QLabel("Chon mot dong trong bang roi bam nut tuong ung de dang ky / huy dang ky.")
        chu_thich.setStyleSheet("font-size: " + str(CO_CHU_NHO) + "px; color: #64748B;")
        chu_thich.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_tab.addWidget(chu_thich)

        self._ve_lai_bang_lop()

    def _ten_thu(self, so_thu):
        tu_dien_thu = {2: "Thu 2", 3: "Thu 3", 4: "Thu 4", 5: "Thu 5", 6: "Thu 6", 7: "Thu 7"}
        return tu_dien_thu.get(so_thu, "Thu " + str(so_thu))

    def _ve_lai_bang_lop(self):
        """Ve lai toan bo bang danh sach lop hoc phan mo."""
        danh_sach_lop = self.he_thong["lop_hoc_phan"]
        self.bang_lop.setRowCount(len(danh_sach_lop))

        for hang, lop_hp in enumerate(danh_sach_lop):
            chu_lich = (self._ten_thu(lop_hp.lich_hoc["thu"])
                        + ", tiet " + str(lop_hp.lich_hoc["tiet_bat_dau"])
                        + "-" + str(lop_hp.lich_hoc["tiet_ket_thuc"]))
            chu_si_so = str(len(lop_hp.danh_sach_sv)) + "/" + str(lop_hp.si_so_toi_da)

            self.bang_lop.setItem(hang, 0, QTableWidgetItem(lop_hp.ma_lop_hp))
            self.bang_lop.setItem(hang, 1, QTableWidgetItem(lop_hp.mon_hoc.ten_mon))
            self.bang_lop.setItem(hang, 2, QTableWidgetItem(str(lop_hp.mon_hoc.so_tin_chi)))
            self.bang_lop.setItem(hang, 3, QTableWidgetItem(lop_hp.giang_vien))
            self.bang_lop.setItem(hang, 4, QTableWidgetItem(chu_lich))
            self.bang_lop.setItem(hang, 5, QTableWidgetItem(chu_si_so))

    def _lay_lop_hp_dang_chon(self):
        """
        Tra ve object LopHocPhan tuong ung voi dong dang duoc chon
        trong bang_lop. Tra ve None neu chua chon dong nao.
        """
        hang_dang_chon = self.bang_lop.currentRow()
        if hang_dang_chon < 0:
            return None

        o_ma_lop = self.bang_lop.item(hang_dang_chon, 0)
        if o_ma_lop is None:
            return None

        ma_lop_hp_dang_chon = o_ma_lop.text()

        for lop_hp in self.he_thong["lop_hoc_phan"]:
            if lop_hp.ma_lop_hp == ma_lop_hp_dang_chon:
                return lop_hp

        return None

    # ------------------------------------------------------------
    # XU LY DANG KY (theo dung luong trong INTERFACE.md)
    # ------------------------------------------------------------
    def _xu_ly_dang_ky(self):
        lop_hp = self._lay_lop_hp_dang_chon()
        if lop_hp is None:
            hien_thi_popup_loi("Vui long chon mot lop hoc phan de dang ky.", self)
            return

        if not lop_hp.dang_mo:
            hien_thi_popup_loi("Lop hoc phan nay da bi Admin dong, khong the dang ky.", self)
            return

        try:
            # Goi du 4 buoc kiem tra dung thu tu nhu mo ta trong INTERFACE.md
            kiem_tra_tien_quyet(self.sinh_vien, lop_hp.mon_hoc)
            kiem_tra_da_dang_ky(self.sinh_vien, lop_hp)
            kiem_tra_xung_dot_lich(self.sinh_vien, lop_hp)
            kiem_tra_si_so(lop_hp)

            # Tat ca dieu kien deu dat -> tien hanh dang ky
            self.sinh_vien.dang_ky(lop_hp)

            # Luu lai he thong ra file ngay sau khi dang ky thanh cong
            luu(self.he_thong)

            hien_thi_popup_thanh_cong(
                "Dang ky thanh cong mon " + lop_hp.mon_hoc.ten_mon + " (" + lop_hp.ma_lop_hp + ").",
                self
            )

        except (LoiChuaDuDieuKienTienQuyet, LoiXungDotLichHoc,
                LoiLopHocDayCho, LoiDaDangKyMonNay) as loi:
            hien_thi_popup_loi(loi.thong_bao, self)

        # Du thanh cong hay khong, ve lai man hinh de cap nhat si so / trang thai
        self._ve_lai_bang_lop()
        self.man_hinh_tkb.cap_nhat_du_lieu()

    def _xu_ly_huy_dang_ky(self):
        lop_hp = self._lay_lop_hp_dang_chon()
        if lop_hp is None:
            hien_thi_popup_loi("Vui long chon mot lop hoc phan de huy dang ky.", self)
            return

        # Kiem tra xem sinh vien co dang dang ky lop nay khong
        dang_co_dang_ky = False
        for l in self.sinh_vien.ds_mon_dang_ky.duyet():
            if l.ma_lop_hp == lop_hp.ma_lop_hp:
                dang_co_dang_ky = True
                break

        if not dang_co_dang_ky:
            hien_thi_popup_loi("Ban chua dang ky lop hoc phan nay.", self)
            return

        dong_y = hien_thi_popup_xac_nhan(
            "Ban co chac muon huy dang ky mon " + lop_hp.mon_hoc.ten_mon + " khong?", self
        )
        if not dong_y:
            return

        self.sinh_vien.huy_dang_ky(lop_hp)
        luu(self.he_thong)

        hien_thi_popup_thanh_cong("Da huy dang ky mon " + lop_hp.mon_hoc.ten_mon + ".", self)

        self._ve_lai_bang_lop()
        self.man_hinh_tkb.cap_nhat_du_lieu()

    def _xu_ly_xuat_phieu(self, dinh_dang):
        if len(self.sinh_vien.ds_mon_dang_ky) == 0:
            hien_thi_popup_loi("Ban chua dang ky mon hoc nao de xuat phieu.", self)
            return

        duong_dan = xuat_phieu_dang_ky(self.sinh_vien, dinh_dang)
        hien_thi_popup_thanh_cong("Da xuat phieu dang ky tai:\n" + duong_dan, self)
