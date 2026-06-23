# ============================================================
# Module: gui/screen_lop_hp.py  -- P1
# Man hinh hien thi danh sach lop hoc phan dang mo trong he thong,
# kem si so hien tai / toi da va lich hoc.
# ============================================================

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from gui.ui_constants import STYLE_TIEU_DE, STYLE_NEN_TRANG, MAU_THANH_CONG, MAU_LOI


class ScreenLopHP(QWidget):
    """
    Man hinh "Danh sach lop hoc phan".

    Tham so:
        he_thong : dict du lieu he thong, co khoa "lop_hoc_phan" la list LopHocPhan
    """

    def __init__(self, he_thong):
        super().__init__()
        self.he_thong = he_thong
        self.setStyleSheet(STYLE_NEN_TRANG)
        self._tao_giao_dien()

    def _tao_giao_dien(self):
        layout_chinh = QVBoxLayout(self)

        tieu_de = QLabel("DANH SACH LOP HOC PHAN")
        tieu_de.setStyleSheet(STYLE_TIEU_DE)
        tieu_de.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_chinh.addWidget(tieu_de)

        self.bang = QTableWidget()
        self.bang.setColumnCount(6)
        self.bang.setHorizontalHeaderLabels(
            ["Ma lop HP", "Mon hoc", "Giang vien", "Lich hoc", "Si so", "Trang thai"]
        )
        self.bang.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.bang.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.bang.verticalHeader().setVisible(False)
        layout_chinh.addWidget(self.bang)

        self.cap_nhat_du_lieu()

    def _ten_thu(self, so_thu):
        """Doi so thu (2..7) thanh chu de hien thi de doc hon."""
        tu_dien_thu = {2: "Thu 2", 3: "Thu 3", 4: "Thu 4", 5: "Thu 5", 6: "Thu 6", 7: "Thu 7"}
        return tu_dien_thu.get(so_thu, "Thu " + str(so_thu))

    def cap_nhat_du_lieu(self):
        """
        Ve lai toan bo bang theo danh sach lop hoc phan hien tai.
        Goi lai ham nay sau khi co dang ky / huy dang ky / them lop moi.
        """
        danh_sach_lop = self.he_thong["lop_hoc_phan"]
        self.bang.setRowCount(len(danh_sach_lop))

        for hang, lop_hp in enumerate(danh_sach_lop):
            chu_lich = (self._ten_thu(lop_hp.lich_hoc["thu"])
                        + ", tiet " + str(lop_hp.lich_hoc["tiet_bat_dau"])
                        + "-" + str(lop_hp.lich_hoc["tiet_ket_thuc"]))
            chu_si_so = str(len(lop_hp.danh_sach_sv)) + "/" + str(lop_hp.si_so_toi_da)

            if not lop_hp.dang_mo:
                chu_trang_thai = "Da dong"
            elif lop_hp.la_day():
                chu_trang_thai = "Da day"
            else:
                chu_trang_thai = "Con cho"

            self.bang.setItem(hang, 0, QTableWidgetItem(lop_hp.ma_lop_hp))
            self.bang.setItem(hang, 1, QTableWidgetItem(lop_hp.mon_hoc.ten_mon))
            self.bang.setItem(hang, 2, QTableWidgetItem(lop_hp.giang_vien))
            self.bang.setItem(hang, 3, QTableWidgetItem(chu_lich))
            self.bang.setItem(hang, 4, QTableWidgetItem(chu_si_so))

            o_trang_thai = QTableWidgetItem(chu_trang_thai)
            if chu_trang_thai == "Da day" or chu_trang_thai == "Da dong":
                o_trang_thai.setForeground(QColor(MAU_LOI))
            else:
                o_trang_thai.setForeground(QColor(MAU_THANH_CONG))
            self.bang.setItem(hang, 5, o_trang_thai)
