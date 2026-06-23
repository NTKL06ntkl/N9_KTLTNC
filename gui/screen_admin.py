# ============================================================
# Module: gui/screen_admin.py  -- P5
# Man hinh quan ly (Admin): them mon hoc, them lop hoc phan,
# dong/mo lop hoc phan, xem danh sach SV cua tung lop,
# them/xoa sinh vien.
# ============================================================

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QTabWidget,
    QGroupBox, QComboBox, QLineEdit,
)
from PyQt6.QtCore import Qt

from gui.ui_constants import (
    STYLE_NUT_THANH_CONG, STYLE_NUT_LOI, STYLE_NUT_PHU,
    STYLE_TIEU_DE, STYLE_NEN_TRANG, STYLE_THANH_THONG_TIN,
)
from gui.popup_error import hien_thi_popup_loi, hien_thi_popup_thanh_cong, hien_thi_popup_xac_nhan

from logic.mon_hoc import MonHoc
from logic.lop_hoc_phan import LopHocPhan
from logic.sinh_vien import SinhVien
from logic.file_handler import luu


class ScreenAdmin(QWidget):
    """
    Man hinh chinh cho Admin (Quan ly).

    Tham so:
        he_thong : dict du lieu he thong (mon_hoc, lop_hoc_phan, sinh_vien)
    """

    def __init__(self, he_thong):
        super().__init__()
        self.he_thong = he_thong
        self.setStyleSheet(STYLE_NEN_TRANG)
        self._tao_giao_dien()

    def _tao_giao_dien(self):
        layout_chinh = QVBoxLayout(self)
        layout_chinh.setContentsMargins(0, 0, 0, 0)

        thanh_thong_tin = QLabel("TRANG QUAN LY (ADMIN)")
        thanh_thong_tin.setStyleSheet(STYLE_THANH_THONG_TIN)
        layout_chinh.addWidget(thanh_thong_tin)

        so_tab = QTabWidget()
        layout_chinh.addWidget(so_tab)

        tab_lop = QWidget()
        so_tab.addTab(tab_lop, "Lop hoc phan")
        self._tao_tab_lop_hp(tab_lop)

        tab_mon = QWidget()
        so_tab.addTab(tab_mon, "Mon hoc")
        self._tao_tab_mon_hoc(tab_mon)

        tab_sv = QWidget()
        so_tab.addTab(tab_sv, "Sinh vien")
        self._tao_tab_sinh_vien(tab_sv)

    # ============================================================
    # TAB 1: LOP HOC PHAN
    # ============================================================
    def _tao_tab_lop_hp(self, khung_cha):
        layout_tab = QVBoxLayout(khung_cha)

        tieu_de = QLabel("QUAN LY LOP HOC PHAN")
        tieu_de.setStyleSheet(STYLE_TIEU_DE)
        tieu_de.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_tab.addWidget(tieu_de)

        self.bang_lop_admin = QTableWidget()
        self.bang_lop_admin.setColumnCount(5)
        self.bang_lop_admin.setHorizontalHeaderLabels(
            ["Ma lop HP", "Mon hoc", "Giang vien", "Si so", "Trang thai"]
        )
        self.bang_lop_admin.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.bang_lop_admin.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.bang_lop_admin.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.bang_lop_admin.verticalHeader().setVisible(False)
        layout_tab.addWidget(self.bang_lop_admin)

        layout_nut = QHBoxLayout()
        nut_dong_mo = QPushButton("Dong / Mo lop da chon")
        nut_dong_mo.setStyleSheet(STYLE_NUT_LOI)
        nut_dong_mo.clicked.connect(self._xu_ly_dong_mo_lop)
        layout_nut.addWidget(nut_dong_mo)

        nut_xem_sv = QPushButton("Xem danh sach SV cua lop")
        nut_xem_sv.setStyleSheet(STYLE_NUT_PHU)
        nut_xem_sv.clicked.connect(self._xu_ly_xem_ds_sv)
        layout_nut.addWidget(nut_xem_sv)
        layout_tab.addLayout(layout_nut)

        khung_them = QGroupBox("Them lop hoc phan moi")
        luoi_them = QGridLayout()

        luoi_them.addWidget(QLabel("Ma lop HP:"), 0, 0)
        self.o_nhap_ma_lop = QLineEdit()
        luoi_them.addWidget(self.o_nhap_ma_lop, 0, 1)

        luoi_them.addWidget(QLabel("Mon hoc:"), 0, 2)
        self.combo_mon = QComboBox()
        luoi_them.addWidget(self.combo_mon, 0, 3)

        luoi_them.addWidget(QLabel("Giang vien:"), 1, 0)
        self.o_nhap_gv = QLineEdit()
        luoi_them.addWidget(self.o_nhap_gv, 1, 1)

        luoi_them.addWidget(QLabel("Si so toi da:"), 1, 2)
        self.o_nhap_si_so = QLineEdit()
        luoi_them.addWidget(self.o_nhap_si_so, 1, 3)

        luoi_them.addWidget(QLabel("Thu hoc (2-7):"), 2, 0)
        self.o_nhap_thu = QLineEdit()
        luoi_them.addWidget(self.o_nhap_thu, 2, 1)

        luoi_them.addWidget(QLabel("Tiet bat dau - ket thuc:"), 2, 2)
        khung_tiet = QHBoxLayout()
        self.o_nhap_tiet_bd = QLineEdit()
        self.o_nhap_tiet_bd.setFixedWidth(50)
        khung_tiet.addWidget(self.o_nhap_tiet_bd)
        khung_tiet.addWidget(QLabel("-"))
        self.o_nhap_tiet_kt = QLineEdit()
        self.o_nhap_tiet_kt.setFixedWidth(50)
        khung_tiet.addWidget(self.o_nhap_tiet_kt)
        luoi_them.addLayout(khung_tiet, 2, 3)

        nut_them_lop = QPushButton("Them lop hoc phan")
        nut_them_lop.setStyleSheet(STYLE_NUT_THANH_CONG)
        nut_them_lop.clicked.connect(self._xu_ly_them_lop_hp)
        luoi_them.addWidget(nut_them_lop, 3, 0, 1, 4)

        khung_them.setLayout(luoi_them)
        layout_tab.addWidget(khung_them)

        khung_ds_sv = QGroupBox("Danh sach SV cua lop hoc phan da chon")
        layout_ds_sv = QVBoxLayout()
        self.bang_sv_cua_lop = QTableWidget()
        self.bang_sv_cua_lop.setColumnCount(3)
        self.bang_sv_cua_lop.setHorizontalHeaderLabels(["Ma SV", "Ho ten", "Lop SH"])
        self.bang_sv_cua_lop.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.bang_sv_cua_lop.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.bang_sv_cua_lop.verticalHeader().setVisible(False)
        layout_ds_sv.addWidget(self.bang_sv_cua_lop)
        khung_ds_sv.setLayout(layout_ds_sv)
        layout_tab.addWidget(khung_ds_sv)

        self._lam_moi_combo_mon()
        self._ve_lai_bang_lop_admin()

    def _lam_moi_combo_mon(self):
        self.combo_mon.clear()
        for mon in self.he_thong["mon_hoc"]:
            self.combo_mon.addItem(mon.ma_mon + " - " + mon.ten_mon, mon.ma_mon)

    def _ve_lai_bang_lop_admin(self):
        danh_sach_lop = self.he_thong["lop_hoc_phan"]
        self.bang_lop_admin.setRowCount(len(danh_sach_lop))

        for hang, lop_hp in enumerate(danh_sach_lop):
            chu_si_so = str(len(lop_hp.danh_sach_sv)) + "/" + str(lop_hp.si_so_toi_da)
            if not lop_hp.dang_mo:
                chu_trang_thai = "Da dong"
            elif lop_hp.la_day():
                chu_trang_thai = "Da day"
            else:
                chu_trang_thai = "Dang mo"

            self.bang_lop_admin.setItem(hang, 0, QTableWidgetItem(lop_hp.ma_lop_hp))
            self.bang_lop_admin.setItem(hang, 1, QTableWidgetItem(lop_hp.mon_hoc.ten_mon))
            self.bang_lop_admin.setItem(hang, 2, QTableWidgetItem(lop_hp.giang_vien))
            self.bang_lop_admin.setItem(hang, 3, QTableWidgetItem(chu_si_so))
            self.bang_lop_admin.setItem(hang, 4, QTableWidgetItem(chu_trang_thai))

    def _lay_lop_dang_chon_trong_bang_admin(self):
        hang_dang_chon = self.bang_lop_admin.currentRow()
        if hang_dang_chon < 0:
            return None
        o_ma_lop = self.bang_lop_admin.item(hang_dang_chon, 0)
        if o_ma_lop is None:
            return None
        ma_lop = o_ma_lop.text()
        for lop_hp in self.he_thong["lop_hoc_phan"]:
            if lop_hp.ma_lop_hp == ma_lop:
                return lop_hp
        return None

    def _xu_ly_dong_mo_lop(self):
        lop_hp = self._lay_lop_dang_chon_trong_bang_admin()
        if lop_hp is None:
            hien_thi_popup_loi("Vui long chon mot lop hoc phan trong bang.", self)
            return

        lop_hp.dang_mo = not lop_hp.dang_mo
        luu(self.he_thong)

        if lop_hp.dang_mo:
            hien_thi_popup_thanh_cong("Da MO lop " + lop_hp.ma_lop_hp + ".", self)
        else:
            hien_thi_popup_thanh_cong("Da DONG lop " + lop_hp.ma_lop_hp + ".", self)

        self._ve_lai_bang_lop_admin()

    def _xu_ly_xem_ds_sv(self):
        lop_hp = self._lay_lop_dang_chon_trong_bang_admin()
        if lop_hp is None:
            hien_thi_popup_loi("Vui long chon mot lop hoc phan trong bang.", self)
            return

        danh_sach_sv = lop_hp.danh_sach_sv.duyet()
        self.bang_sv_cua_lop.setRowCount(len(danh_sach_sv))
        for hang, sv in enumerate(danh_sach_sv):
            self.bang_sv_cua_lop.setItem(hang, 0, QTableWidgetItem(sv.ma_sv))
            self.bang_sv_cua_lop.setItem(hang, 1, QTableWidgetItem(sv.ho_ten))
            self.bang_sv_cua_lop.setItem(hang, 2, QTableWidgetItem(sv.lop_sh))

    def _xu_ly_them_lop_hp(self):
        ma_lop = self.o_nhap_ma_lop.text().strip()
        ma_mon = self.combo_mon.currentData()
        giang_vien = self.o_nhap_gv.text().strip()
        chu_si_so = self.o_nhap_si_so.text().strip()
        chu_thu = self.o_nhap_thu.text().strip()
        chu_tiet_bd = self.o_nhap_tiet_bd.text().strip()
        chu_tiet_kt = self.o_nhap_tiet_kt.text().strip()

        if ma_lop == "" or ma_mon is None or giang_vien == "":
            hien_thi_popup_loi("Vui long dien day du Ma lop HP, Mon hoc va Giang vien.", self)
            return

        for lop_hp_cu in self.he_thong["lop_hoc_phan"]:
            if lop_hp_cu.ma_lop_hp == ma_lop:
                hien_thi_popup_loi("Ma lop hoc phan nay da ton tai.", self)
                return

        try:
            si_so_toi_da = int(chu_si_so)
            thu = int(chu_thu)
            tiet_bat_dau = int(chu_tiet_bd)
            tiet_ket_thuc = int(chu_tiet_kt)
        except ValueError:
            hien_thi_popup_loi("Si so / Thu / Tiet phai la so nguyen.", self)
            return

        if thu < 2 or thu > 7:
            hien_thi_popup_loi("Thu hoc phai trong khoang 2 den 7.", self)
            return

        if tiet_bat_dau < 1 or tiet_ket_thuc < tiet_bat_dau:
            hien_thi_popup_loi("Tiet hoc khong hop le.", self)
            return

        mon_hoc_tuong_ung = None
        for mon in self.he_thong["mon_hoc"]:
            if mon.ma_mon == ma_mon:
                mon_hoc_tuong_ung = mon
                break

        if mon_hoc_tuong_ung is None:
            hien_thi_popup_loi("Khong tim thay mon hoc tuong ung.", self)
            return

        lich_hoc_moi = {"thu": thu, "tiet_bat_dau": tiet_bat_dau, "tiet_ket_thuc": tiet_ket_thuc}
        lop_hp_moi = LopHocPhan(ma_lop, mon_hoc_tuong_ung, giang_vien, si_so_toi_da, lich_hoc_moi)

        self.he_thong["lop_hoc_phan"].append(lop_hp_moi)
        luu(self.he_thong)

        hien_thi_popup_thanh_cong("Da them lop hoc phan " + ma_lop + ".", self)

        self.o_nhap_ma_lop.clear()
        self.o_nhap_gv.clear()
        self.o_nhap_si_so.clear()
        self.o_nhap_thu.clear()
        self.o_nhap_tiet_bd.clear()
        self.o_nhap_tiet_kt.clear()

        self._ve_lai_bang_lop_admin()

    # ============================================================
    # TAB 2: MON HOC
    # ============================================================
    def _tao_tab_mon_hoc(self, khung_cha):
        layout_tab = QVBoxLayout(khung_cha)

        tieu_de = QLabel("QUAN LY MON HOC")
        tieu_de.setStyleSheet(STYLE_TIEU_DE)
        tieu_de.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_tab.addWidget(tieu_de)

        self.bang_mon_admin = QTableWidget()
        self.bang_mon_admin.setColumnCount(4)
        self.bang_mon_admin.setHorizontalHeaderLabels(
            ["Ma mon", "Ten mon", "So tin chi", "Mon tien quyet"]
        )
        self.bang_mon_admin.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.bang_mon_admin.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.bang_mon_admin.verticalHeader().setVisible(False)
        layout_tab.addWidget(self.bang_mon_admin)

        khung_them = QGroupBox("Them mon hoc moi")
        luoi_them = QGridLayout()

        luoi_them.addWidget(QLabel("Ma mon:"), 0, 0)
        self.o_nhap_ma_mon = QLineEdit()
        luoi_them.addWidget(self.o_nhap_ma_mon, 0, 1)

        luoi_them.addWidget(QLabel("Ten mon:"), 0, 2)
        self.o_nhap_ten_mon = QLineEdit()
        luoi_them.addWidget(self.o_nhap_ten_mon, 0, 3)

        luoi_them.addWidget(QLabel("So tin chi:"), 1, 0)
        self.o_nhap_so_tc = QLineEdit()
        luoi_them.addWidget(self.o_nhap_so_tc, 1, 1)

        luoi_them.addWidget(QLabel("Mon tien quyet:"), 1, 2)
        self.combo_tien_quyet = QComboBox()
        luoi_them.addWidget(self.combo_tien_quyet, 1, 3)

        nut_them_mon = QPushButton("Them mon hoc")
        nut_them_mon.setStyleSheet(STYLE_NUT_THANH_CONG)
        nut_them_mon.clicked.connect(self._xu_ly_them_mon_hoc)
        luoi_them.addWidget(nut_them_mon, 2, 0, 1, 4)

        khung_them.setLayout(luoi_them)
        layout_tab.addWidget(khung_them)

        self._lam_moi_combo_tien_quyet()
        self._ve_lai_bang_mon_admin()

    def _lam_moi_combo_tien_quyet(self):
        self.combo_tien_quyet.clear()
        self.combo_tien_quyet.addItem("Khong co", None)
        for mon in self.he_thong["mon_hoc"]:
            self.combo_tien_quyet.addItem(mon.ma_mon + " - " + mon.ten_mon, mon.ma_mon)

    def _ve_lai_bang_mon_admin(self):
        tu_dien_ten_mon = {}
        for mon in self.he_thong["mon_hoc"]:
            tu_dien_ten_mon[mon.ma_mon] = mon.ten_mon

        danh_sach_mon = self.he_thong["mon_hoc"]
        self.bang_mon_admin.setRowCount(len(danh_sach_mon))

        for hang, mon in enumerate(danh_sach_mon):
            if mon.ma_mon_tien_quyet is None:
                chu_tien_quyet = "Khong co"
            else:
                chu_tien_quyet = mon.ma_mon_tien_quyet + " - " + tu_dien_ten_mon.get(mon.ma_mon_tien_quyet, "")

            self.bang_mon_admin.setItem(hang, 0, QTableWidgetItem(mon.ma_mon))
            self.bang_mon_admin.setItem(hang, 1, QTableWidgetItem(mon.ten_mon))
            self.bang_mon_admin.setItem(hang, 2, QTableWidgetItem(str(mon.so_tin_chi)))
            self.bang_mon_admin.setItem(hang, 3, QTableWidgetItem(chu_tien_quyet))

    def _xu_ly_them_mon_hoc(self):
        ma_mon = self.o_nhap_ma_mon.text().strip()
        ten_mon = self.o_nhap_ten_mon.text().strip()
        chu_so_tc = self.o_nhap_so_tc.text().strip()
        ma_mon_tien_quyet = self.combo_tien_quyet.currentData()

        if ma_mon == "" or ten_mon == "":
            hien_thi_popup_loi("Vui long dien day du Ma mon va Ten mon.", self)
            return

        for mon_cu in self.he_thong["mon_hoc"]:
            if mon_cu.ma_mon == ma_mon:
                hien_thi_popup_loi("Ma mon nay da ton tai.", self)
                return

        try:
            so_tin_chi = int(chu_so_tc)
        except ValueError:
            hien_thi_popup_loi("So tin chi phai la so nguyen.", self)
            return

        mon_moi = MonHoc(ma_mon, ten_mon, so_tin_chi, ma_mon_tien_quyet)
        self.he_thong["mon_hoc"].append(mon_moi)
        luu(self.he_thong)

        hien_thi_popup_thanh_cong("Da them mon hoc " + ma_mon + ".", self)

        self.o_nhap_ma_mon.clear()
        self.o_nhap_ten_mon.clear()
        self.o_nhap_so_tc.clear()

        self._ve_lai_bang_mon_admin()
        self._lam_moi_combo_tien_quyet()
        self._lam_moi_combo_mon()

    # ============================================================
    # TAB 3: SINH VIEN
    # ============================================================
    def _tao_tab_sinh_vien(self, khung_cha):
        layout_tab = QVBoxLayout(khung_cha)

        tieu_de = QLabel("QUAN LY SINH VIEN")
        tieu_de.setStyleSheet(STYLE_TIEU_DE)
        tieu_de.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_tab.addWidget(tieu_de)

        self.bang_sv_admin = QTableWidget()
        self.bang_sv_admin.setColumnCount(5)
        self.bang_sv_admin.setHorizontalHeaderLabels(
            ["Ma SV", "Ho ten", "Lop SH", "DTB", "So lop dang ky"]
        )
        self.bang_sv_admin.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.bang_sv_admin.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.bang_sv_admin.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.bang_sv_admin.verticalHeader().setVisible(False)
        layout_tab.addWidget(self.bang_sv_admin)

        nut_xoa_sv = QPushButton("Xoa sinh vien da chon")
        nut_xoa_sv.setStyleSheet(STYLE_NUT_LOI)
        nut_xoa_sv.clicked.connect(self._xu_ly_xoa_sinh_vien)
        layout_tab.addWidget(nut_xoa_sv)

        khung_them = QGroupBox("Them sinh vien moi")
        luoi_them = QGridLayout()

        luoi_them.addWidget(QLabel("Ma SV:"), 0, 0)
        self.o_nhap_ma_sv = QLineEdit()
        luoi_them.addWidget(self.o_nhap_ma_sv, 0, 1)

        luoi_them.addWidget(QLabel("Ho ten:"), 0, 2)
        self.o_nhap_ho_ten = QLineEdit()
        luoi_them.addWidget(self.o_nhap_ho_ten, 0, 3)

        luoi_them.addWidget(QLabel("Lop sinh hoat:"), 1, 0)
        self.o_nhap_lop_sh = QLineEdit()
        luoi_them.addWidget(self.o_nhap_lop_sh, 1, 1)

        nut_them_sv = QPushButton("Them sinh vien")
        nut_them_sv.setStyleSheet(STYLE_NUT_THANH_CONG)
        nut_them_sv.clicked.connect(self._xu_ly_them_sinh_vien)
        luoi_them.addWidget(nut_them_sv, 2, 0, 1, 4)

        khung_them.setLayout(luoi_them)
        layout_tab.addWidget(khung_them)

        self._ve_lai_bang_sv_admin()

    def _ve_lai_bang_sv_admin(self):
        danh_sach_sv = self.he_thong["sinh_vien"]
        self.bang_sv_admin.setRowCount(len(danh_sach_sv))

        for hang, sv in enumerate(danh_sach_sv):
            dtb = sv.tinh_dtb_co_trong_so(self.he_thong["mon_hoc"])
            so_lop_dk = len(sv.ds_mon_dang_ky)

            self.bang_sv_admin.setItem(hang, 0, QTableWidgetItem(sv.ma_sv))
            self.bang_sv_admin.setItem(hang, 1, QTableWidgetItem(sv.ho_ten))
            self.bang_sv_admin.setItem(hang, 2, QTableWidgetItem(sv.lop_sh))
            self.bang_sv_admin.setItem(hang, 3, QTableWidgetItem(str(dtb)))
            self.bang_sv_admin.setItem(hang, 4, QTableWidgetItem(str(so_lop_dk)))

    def _xu_ly_them_sinh_vien(self):
        ma_sv = self.o_nhap_ma_sv.text().strip()
        ho_ten = self.o_nhap_ho_ten.text().strip()
        lop_sh = self.o_nhap_lop_sh.text().strip()

        if ma_sv == "" or ho_ten == "" or lop_sh == "":
            hien_thi_popup_loi("Vui long dien day du thong tin sinh vien.", self)
            return

        for sv_cu in self.he_thong["sinh_vien"]:
            if sv_cu.ma_sv == ma_sv:
                hien_thi_popup_loi("Ma sinh vien nay da ton tai.", self)
                return

        sv_moi = SinhVien(ma_sv, ho_ten, lop_sh)
        self.he_thong["sinh_vien"].append(sv_moi)
        luu(self.he_thong)

        hien_thi_popup_thanh_cong("Da them sinh vien " + ma_sv + ".", self)

        self.o_nhap_ma_sv.clear()
        self.o_nhap_ho_ten.clear()
        self.o_nhap_lop_sh.clear()

        self._ve_lai_bang_sv_admin()

    def _xu_ly_xoa_sinh_vien(self):
        hang_dang_chon = self.bang_sv_admin.currentRow()
        if hang_dang_chon < 0:
            hien_thi_popup_loi("Vui long chon mot sinh vien trong bang.", self)
            return

        o_ma_sv = self.bang_sv_admin.item(hang_dang_chon, 0)
        if o_ma_sv is None:
            return
        ma_sv_can_xoa = o_ma_sv.text()

        sv_can_xoa = None
        for sv in self.he_thong["sinh_vien"]:
            if sv.ma_sv == ma_sv_can_xoa:
                sv_can_xoa = sv
                break

        if sv_can_xoa is None:
            return

        dong_y = hien_thi_popup_xac_nhan(
            "Xoa sinh vien " + sv_can_xoa.ho_ten + "? Tat ca dang ky cua SV nay se bi huy.", self
        )
        if not dong_y:
            return

        danh_sach_lop_dang_dang_ky = list(sv_can_xoa.ds_mon_dang_ky.duyet())
        for lop_hp in danh_sach_lop_dang_dang_ky:
            sv_can_xoa.huy_dang_ky(lop_hp)

        self.he_thong["sinh_vien"].remove(sv_can_xoa)
        luu(self.he_thong)

        hien_thi_popup_thanh_cong("Da xoa sinh vien " + ma_sv_can_xoa + ".", self)
        self._ve_lai_bang_sv_admin()
