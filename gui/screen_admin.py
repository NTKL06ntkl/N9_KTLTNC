# ============================================================
# Module: gui/screen_admin.py  -- P5
# ============================================================

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QTabWidget,
    QGroupBox, QComboBox, QLineEdit, QScrollArea,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from gui.ui_constants import STYLE_NUT_THANH_CONG, STYLE_NUT_LOI, STYLE_NUT_PHU
from gui.popup_error import hien_thi_popup_loi, hien_thi_popup_thanh_cong, hien_thi_popup_xac_nhan

from logic.mon_hoc import MonHoc
from logic.lop_hoc_phan import LopHocPhan
from logic.sinh_vien import SinhVien
from logic.file_handler import luu


class ScreenAdmin(QWidget):

    def __init__(self, he_thong):
        super().__init__()
        self.he_thong = he_thong
        self._tao_giao_dien()

    def _tao_giao_dien(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Thanh thông tin admin
        thanh = QWidget()
        thanh.setStyleSheet("background-color: #1E293B; border-bottom: 1px solid #334155;")
        thanh.setFixedHeight(56)
        layout_thanh = QHBoxLayout(thanh)
        layout_thanh.setContentsMargins(24, 0, 24, 0)

        nhan = QLabel("🛠  Trang Quản lý hệ thống")
        nhan.setStyleSheet("color: #F1F5F9; font-size: 14px; font-weight: 800; background: transparent;")
        layout_thanh.addWidget(nhan)
        layout_thanh.addStretch()

        for txt, mau in [("Môn học: " + str(len(self.he_thong["mon_hoc"])), "#3B82F6"),
                          ("Lớp HP: " + str(len(self.he_thong["lop_hoc_phan"])), "#10B981"),
                          ("Sinh viên: " + str(len(self.he_thong["sinh_vien"])), "#F59E0B")]:
            chip = QLabel(txt)
            chip.setStyleSheet(
                "background-color: #334155; color: " + mau + "; border-radius: 12px;"
                "padding: 3px 12px; font-size: 12px; font-weight: 700;"
            )
            layout_thanh.addWidget(chip)
            layout_thanh.addSpacing(6)

        layout.addWidget(thanh)

        so_tab = QTabWidget()
        so_tab.setContentsMargins(12, 8, 12, 8)
        layout.addWidget(so_tab)

        t1 = QWidget(); so_tab.addTab(t1, "🏫  Lớp học phần"); self._tao_tab_lop(t1)
        t2 = QWidget(); so_tab.addTab(t2, "📘  Môn học");      self._tao_tab_mon(t2)
        t3 = QWidget(); so_tab.addTab(t3, "👥  Sinh viên");    self._tao_tab_sv(t3)

    # ── Hàm dựng bảng chung ──────────────────────────────────
    def _tao_bang(self, cot_headers):
        b = QTableWidget()
        b.setColumnCount(len(cot_headers))
        b.setHorizontalHeaderLabels(cot_headers)
        b.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        b.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        b.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        b.verticalHeader().setVisible(False)
        b.setAlternatingRowColors(True)
        b.setShowGrid(False)
        return b

    # ── TAB 1: Lớp học phần ──────────────────────────────────
    def _tao_tab_lop(self, cha):
        # Bọc toàn bộ nội dung trong QScrollArea
        # để cửa sổ nhỏ vẫn cuộn được, không bị chèn nhau
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        noi_dung = QWidget()
        layout = QVBoxLayout(noi_dung)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        layout.addWidget(self._nhan_tieu_de("Quản lý lớp học phần"))

        # Bảng danh sách lớp — chiều cao cố định đủ thấy
        self.bang_lop_admin = self._tao_bang(
            ["Mã lớp HP", "Môn học", "Giảng viên", "Sĩ số", "Trạng thái"]
        )
        self.bang_lop_admin.setFixedHeight(220)
        layout.addWidget(self.bang_lop_admin)

        # Nút Đóng/Mở + Xem SV
        layout_nut = QHBoxLayout()
        nut_dm = QPushButton("🔒  Đóng / Mở lớp")
        nut_dm.setStyleSheet(STYLE_NUT_LOI); nut_dm.setFixedHeight(38)
        nut_dm.clicked.connect(self._dong_mo_lop)
        layout_nut.addWidget(nut_dm)

        nut_xem = QPushButton("👁  Xem SV của lớp")
        nut_xem.setStyleSheet(STYLE_NUT_PHU); nut_xem.setFixedHeight(38)
        nut_xem.clicked.connect(self._xem_sv_lop)
        layout_nut.addWidget(nut_xem)
        layout_nut.addStretch()
        layout.addLayout(layout_nut)

        # Form thêm lớp
        khung = QGroupBox("Thêm lớp học phần mới")
        luoi = QGridLayout()
        luoi.setSpacing(10)
        luoi.setContentsMargins(12, 20, 12, 12)

        luoi.addWidget(QLabel("Mã lớp HP:"), 0, 0)
        self.o_ma_lop = QLineEdit(); self.o_ma_lop.setFixedHeight(36)
        luoi.addWidget(self.o_ma_lop, 0, 1)

        luoi.addWidget(QLabel("Môn học:"), 0, 2)
        self.combo_mon = QComboBox(); self.combo_mon.setFixedHeight(36)
        luoi.addWidget(self.combo_mon, 0, 3)

        luoi.addWidget(QLabel("Giảng viên:"), 1, 0)
        self.o_gv = QLineEdit(); self.o_gv.setFixedHeight(36)
        luoi.addWidget(self.o_gv, 1, 1)

        luoi.addWidget(QLabel("Sĩ số tối đa:"), 1, 2)
        self.o_siso = QLineEdit(); self.o_siso.setFixedHeight(36)
        luoi.addWidget(self.o_siso, 1, 3)

        luoi.addWidget(QLabel("Thứ (2–7):"), 2, 0)
        self.o_thu = QLineEdit(); self.o_thu.setFixedHeight(36)
        luoi.addWidget(self.o_thu, 2, 1)

        luoi.addWidget(QLabel("Tiết bắt đầu – kết thúc:"), 2, 2)
        row_tiet = QHBoxLayout()
        self.o_tbd = QLineEdit(); self.o_tbd.setFixedSize(70, 36)
        self.o_tkt = QLineEdit(); self.o_tkt.setFixedSize(70, 36)
        row_tiet.addWidget(self.o_tbd)
        row_tiet.addWidget(QLabel("–"))
        row_tiet.addWidget(self.o_tkt)
        row_tiet.addStretch()
        luoi.addLayout(row_tiet, 2, 3)

        nut = QPushButton("➕  Thêm lớp học phần")
        nut.setStyleSheet(STYLE_NUT_THANH_CONG); nut.setFixedHeight(40)
        nut.clicked.connect(self._them_lop)
        luoi.addWidget(nut, 3, 0, 1, 4)

        khung.setLayout(luoi)
        layout.addWidget(khung)

        # Bảng SV của lớp đã chọn — chiều cao cố định
        khung_sv = QGroupBox("Danh sách sinh viên của lớp đã chọn")
        lsv = QVBoxLayout()
        lsv.setContentsMargins(8, 8, 8, 8)
        self.bang_sv_lop = self._tao_bang(["Mã SV", "Họ tên", "Lớp SH"])
        self.bang_sv_lop.setFixedHeight(160)
        lsv.addWidget(self.bang_sv_lop)
        khung_sv.setLayout(lsv)
        layout.addWidget(khung_sv)

        layout.addStretch()

        scroll.setWidget(noi_dung)

        # Đặt scroll vào layout của tab cha
        layout_cha = QVBoxLayout(cha)
        layout_cha.setContentsMargins(0, 0, 0, 0)
        layout_cha.addWidget(scroll)

        self._refresh_combo_mon()
        self._refresh_bang_lop()

    def _nhan_tieu_de(self, text):
        l = QLabel(text)
        l.setStyleSheet("font-size: 15px; font-weight: 800; color: #F1F5F9;")
        return l

    def _refresh_combo_mon(self):
        self.combo_mon.clear()
        for m in self.he_thong["mon_hoc"]:
            self.combo_mon.addItem(m.ma_mon + " — " + m.ten_mon, m.ma_mon)

    def _refresh_bang_lop(self):
        ds = self.he_thong["lop_hoc_phan"]
        self.bang_lop_admin.setRowCount(len(ds))
        for i, l in enumerate(ds):
            ss = str(len(l.danh_sach_sv)) + "/" + str(l.si_so_toi_da)
            if not l.dang_mo:   tt, mc = "Đã đóng", "#EF4444"
            elif l.la_day():    tt, mc = "Đã đầy",  "#F59E0B"
            else:               tt, mc = "Đang mở", "#10B981"

            for c, v in enumerate([l.ma_lop_hp, l.mon_hoc.ten_mon, l.giang_vien, ss, tt]):
                o = QTableWidgetItem(v)
                if c == 4: o.setForeground(QColor(mc))
                self.bang_lop_admin.setItem(i, c, o)
            self.bang_lop_admin.setRowHeight(i, 40)

    def _lay_lop_chon(self):
        r = self.bang_lop_admin.currentRow()
        if r < 0: return None
        o = self.bang_lop_admin.item(r, 0)
        if o is None: return None
        return next((l for l in self.he_thong["lop_hoc_phan"] if l.ma_lop_hp == o.text()), None)

    def _dong_mo_lop(self):
        l = self._lay_lop_chon()
        if l is None:
            hien_thi_popup_loi("Vui lòng chọn một lớp học phần.", self); return
        l.dang_mo = not l.dang_mo
        luu(self.he_thong)
        trang_thai = "MỞ" if l.dang_mo else "ĐÓNG"
        hien_thi_popup_thanh_cong("Đã " + trang_thai + " lớp " + l.ma_lop_hp + ".", self)
        self._refresh_bang_lop()

    def _xem_sv_lop(self):
        l = self._lay_lop_chon()
        if l is None:
            hien_thi_popup_loi("Vui lòng chọn một lớp học phần.", self); return
        ds = l.danh_sach_sv.duyet()
        self.bang_sv_lop.setRowCount(len(ds))
        for i, sv in enumerate(ds):
            for c, v in enumerate([sv.ma_sv, sv.ho_ten, sv.lop_sh]):
                self.bang_sv_lop.setItem(i, c, QTableWidgetItem(v))
            self.bang_sv_lop.setRowHeight(i, 36)

    def _them_lop(self):
        ma = self.o_ma_lop.text().strip()
        ma_mon = self.combo_mon.currentData()
        gv = self.o_gv.text().strip()
        if not ma or ma_mon is None or not gv:
            hien_thi_popup_loi("Vui lòng điền đầy đủ Mã lớp, Môn học và Giảng viên.", self); return
        if any(l.ma_lop_hp == ma for l in self.he_thong["lop_hoc_phan"]):
            hien_thi_popup_loi("Mã lớp học phần này đã tồn tại.", self); return
        try:
            ss = int(self.o_siso.text()); thu = int(self.o_thu.text())
            tbd = int(self.o_tbd.text()); tkt = int(self.o_tkt.text())
        except ValueError:
            hien_thi_popup_loi("Sĩ số / Thứ / Tiết phải là số nguyên.", self); return
        if not (2 <= thu <= 7):
            hien_thi_popup_loi("Thứ học phải trong khoảng 2–7.", self); return
        if tbd < 1 or tkt < tbd:
            hien_thi_popup_loi("Tiết học không hợp lệ.", self); return
        mon = next((m for m in self.he_thong["mon_hoc"] if m.ma_mon == ma_mon), None)
        if mon is None:
            hien_thi_popup_loi("Không tìm thấy môn học.", self); return
        lop = LopHocPhan(ma, mon, gv, ss, {"thu": thu, "tiet_bat_dau": tbd, "tiet_ket_thuc": tkt})
        self.he_thong["lop_hoc_phan"].append(lop)
        luu(self.he_thong)
        hien_thi_popup_thanh_cong("Đã thêm lớp học phần " + ma + ".", self)
        for o in [self.o_ma_lop, self.o_gv, self.o_siso, self.o_thu, self.o_tbd, self.o_tkt]:
            o.clear()
        self._refresh_bang_lop()

    # ── TAB 2: Môn học ───────────────────────────────────────
    def _tao_tab_mon(self, cha):
        layout = QVBoxLayout(cha)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        layout.addWidget(self._nhan_tieu_de("Quản lý môn học"))

        self.bang_mon_admin = self._tao_bang(
            ["Mã môn", "Tên môn học", "Số tín chỉ", "Môn tiên quyết"]
        )
        layout.addWidget(self.bang_mon_admin)

        khung = QGroupBox("Thêm môn học mới")
        luoi = QGridLayout(); luoi.setSpacing(8)

        luoi.addWidget(QLabel("Mã môn:"), 0, 0)
        self.o_ma_mon = QLineEdit(); self.o_ma_mon.setFixedHeight(36)
        luoi.addWidget(self.o_ma_mon, 0, 1)

        luoi.addWidget(QLabel("Tên môn:"), 0, 2)
        self.o_ten_mon = QLineEdit(); self.o_ten_mon.setFixedHeight(36)
        luoi.addWidget(self.o_ten_mon, 0, 3)

        luoi.addWidget(QLabel("Số tín chỉ:"), 1, 0)
        self.o_sotc = QLineEdit(); self.o_sotc.setFixedHeight(36)
        luoi.addWidget(self.o_sotc, 1, 1)

        luoi.addWidget(QLabel("Môn tiên quyết:"), 1, 2)
        self.combo_tq = QComboBox(); self.combo_tq.setFixedHeight(36)
        luoi.addWidget(self.combo_tq, 1, 3)

        nut = QPushButton("➕  Thêm môn học")
        nut.setStyleSheet(STYLE_NUT_THANH_CONG); nut.setFixedHeight(40)
        nut.clicked.connect(self._them_mon)
        luoi.addWidget(nut, 2, 0, 1, 4)
        khung.setLayout(luoi)
        layout.addWidget(khung)

        self._refresh_combo_tq()
        self._refresh_bang_mon()

    def _refresh_combo_tq(self):
        self.combo_tq.clear()
        self.combo_tq.addItem("— Không có —", None)
        for m in self.he_thong["mon_hoc"]:
            self.combo_tq.addItem(m.ma_mon + " — " + m.ten_mon, m.ma_mon)

    def _refresh_bang_mon(self):
        td = {m.ma_mon: m.ten_mon for m in self.he_thong["mon_hoc"]}
        ds = self.he_thong["mon_hoc"]
        self.bang_mon_admin.setRowCount(len(ds))
        for i, m in enumerate(ds):
            tq = "—" if not m.ma_mon_tien_quyet else m.ma_mon_tien_quyet + " · " + td.get(m.ma_mon_tien_quyet, "")
            for c, v in enumerate([m.ma_mon, m.ten_mon, str(m.so_tin_chi), tq]):
                o = QTableWidgetItem(v)
                if c == 2:
                    o.setTextAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
                    o.setForeground(QColor("#93C5FD"))
                if c == 3 and m.ma_mon_tien_quyet:
                    o.setForeground(QColor("#F59E0B"))
                self.bang_mon_admin.setItem(i, c, o)
            self.bang_mon_admin.setRowHeight(i, 40)

    def _them_mon(self):
        ma = self.o_ma_mon.text().strip(); ten = self.o_ten_mon.text().strip()
        if not ma or not ten:
            hien_thi_popup_loi("Vui lòng điền đầy đủ Mã môn và Tên môn.", self); return
        if any(m.ma_mon == ma for m in self.he_thong["mon_hoc"]):
            hien_thi_popup_loi("Mã môn này đã tồn tại.", self); return
        try:
            tc = int(self.o_sotc.text())
        except ValueError:
            hien_thi_popup_loi("Số tín chỉ phải là số nguyên.", self); return
        tq = self.combo_tq.currentData()
        self.he_thong["mon_hoc"].append(MonHoc(ma, ten, tc, tq))
        luu(self.he_thong)
        hien_thi_popup_thanh_cong("Đã thêm môn học " + ma + " — " + ten + ".", self)
        self.o_ma_mon.clear(); self.o_ten_mon.clear(); self.o_sotc.clear()
        self._refresh_bang_mon(); self._refresh_combo_tq(); self._refresh_combo_mon()

    # ── TAB 3: Sinh viên ─────────────────────────────────────
    def _tao_tab_sv(self, cha):
        layout = QVBoxLayout(cha)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        layout.addWidget(self._nhan_tieu_de("Quản lý sinh viên"))

        self.bang_sv_admin = self._tao_bang(
            ["Mã SV", "Họ tên", "Lớp SH", "ĐTB", "Số lớp ĐK"]
        )
        layout.addWidget(self.bang_sv_admin)

        nut_xoa = QPushButton("🗑  Xóa sinh viên đã chọn")
        nut_xoa.setStyleSheet(STYLE_NUT_LOI); nut_xoa.setFixedHeight(40)
        nut_xoa.clicked.connect(self._xoa_sv)
        layout.addWidget(nut_xoa)

        khung = QGroupBox("Thêm sinh viên mới")
        luoi = QGridLayout(); luoi.setSpacing(8)

        luoi.addWidget(QLabel("Mã SV:"), 0, 0)
        self.o_ma_sv = QLineEdit(); self.o_ma_sv.setFixedHeight(36)
        luoi.addWidget(self.o_ma_sv, 0, 1)

        luoi.addWidget(QLabel("Họ tên:"), 0, 2)
        self.o_ho_ten = QLineEdit(); self.o_ho_ten.setFixedHeight(36)
        luoi.addWidget(self.o_ho_ten, 0, 3)

        luoi.addWidget(QLabel("Lớp sinh hoạt:"), 1, 0)
        self.o_lop_sh = QLineEdit(); self.o_lop_sh.setFixedHeight(36)
        luoi.addWidget(self.o_lop_sh, 1, 1)

        nut = QPushButton("➕  Thêm sinh viên")
        nut.setStyleSheet(STYLE_NUT_THANH_CONG); nut.setFixedHeight(40)
        nut.clicked.connect(self._them_sv)
        luoi.addWidget(nut, 2, 0, 1, 4)
        khung.setLayout(luoi)
        layout.addWidget(khung)

        self._refresh_bang_sv()

    def _refresh_bang_sv(self):
        ds = self.he_thong["sinh_vien"]
        self.bang_sv_admin.setRowCount(len(ds))
        for i, sv in enumerate(ds):
            dtb = sv.tinh_dtb_co_trong_so(self.he_thong["mon_hoc"])
            for c, v in enumerate([sv.ma_sv, sv.ho_ten, sv.lop_sh, str(dtb), str(len(sv.ds_mon_dang_ky))]):
                o = QTableWidgetItem(v)
                if c == 3:
                    mau = "#10B981" if dtb >= 7.0 else ("#F59E0B" if dtb >= 5.0 else "#EF4444")
                    if dtb > 0: o.setForeground(QColor(mau))
                self.bang_sv_admin.setItem(i, c, o)
            self.bang_sv_admin.setRowHeight(i, 40)

    def _them_sv(self):
        ma = self.o_ma_sv.text().strip(); ten = self.o_ho_ten.text().strip(); lop = self.o_lop_sh.text().strip()
        if not ma or not ten or not lop:
            hien_thi_popup_loi("Vui lòng điền đầy đủ thông tin sinh viên.", self); return
        if any(s.ma_sv == ma for s in self.he_thong["sinh_vien"]):
            hien_thi_popup_loi("Mã sinh viên này đã tồn tại.", self); return
        self.he_thong["sinh_vien"].append(SinhVien(ma, ten, lop))
        luu(self.he_thong)
        hien_thi_popup_thanh_cong("Đã thêm sinh viên " + ma + " — " + ten + ".", self)
        self.o_ma_sv.clear(); self.o_ho_ten.clear(); self.o_lop_sh.clear()
        self._refresh_bang_sv()

    def _xoa_sv(self):
        r = self.bang_sv_admin.currentRow()
        if r < 0:
            hien_thi_popup_loi("Vui lòng chọn một sinh viên trong bảng.", self); return
        o = self.bang_sv_admin.item(r, 0)
        if o is None: return
        ma = o.text()
        sv = next((s for s in self.he_thong["sinh_vien"] if s.ma_sv == ma), None)
        if sv is None: return
        if not hien_thi_popup_xac_nhan(
            "Xóa sinh viên " + sv.ho_ten + "?\nTất cả đăng ký của SV này sẽ bị hủy.", self
        ): return
        for l in list(sv.ds_mon_dang_ky.duyet()):
            sv.huy_dang_ky(l)
        self.he_thong["sinh_vien"].remove(sv)
        luu(self.he_thong)
        hien_thi_popup_thanh_cong("Đã xóa sinh viên " + ma + ".", self)
        self._refresh_bang_sv()
