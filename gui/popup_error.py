# ============================================================
# Module: gui/popup_error.py  -- P4
# ============================================================

from PyQt6.QtWidgets import QMessageBox


def hien_thi_popup_loi(thong_bao, cha=None):
    hop_thoai = QMessageBox(cha)
    hop_thoai.setIcon(QMessageBox.Icon.Critical)
    hop_thoai.setWindowTitle("Thông báo lỗi")
    hop_thoai.setText(thong_bao)
    hop_thoai.exec()


def hien_thi_popup_thanh_cong(thong_bao, cha=None):
    hop_thoai = QMessageBox(cha)
    hop_thoai.setIcon(QMessageBox.Icon.Information)
    hop_thoai.setWindowTitle("Thành công")
    hop_thoai.setText(thong_bao)
    hop_thoai.exec()


def hien_thi_popup_xac_nhan(cau_hoi, cha=None):
    ket_qua = QMessageBox.question(
        cha, "Xác nhận", cau_hoi,
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
    )
    return ket_qua == QMessageBox.StandardButton.Yes
