# ============================================================
# Module: gui/popup_error.py  -- P4
# Cac ham hien thi cua so thong bao (popup) cho nguoi dung,
# dung khi co loi xay ra hoac khi thao tac thanh cong.
# Su dung QMessageBox cua PyQt6.
# ============================================================

from PyQt6.QtWidgets import QMessageBox


def hien_thi_popup_loi(thong_bao, cha=None):
    """
    Hien thi mot popup canh bao loi.
    Tham so thong_bao la chuoi noi dung can hien thi,
    thuong la e.thong_bao lay tu cac Exception trong logic/kiem_tra.py.
    Tham so cha (tuy chon) la widget cha, giup popup hien giua man hinh cha.
    """
    hop_thoai = QMessageBox(cha)
    hop_thoai.setIcon(QMessageBox.Icon.Critical)
    hop_thoai.setWindowTitle("Thong bao loi")
    hop_thoai.setText(thong_bao)
    hop_thoai.exec()


def hien_thi_popup_thanh_cong(thong_bao, cha=None):
    """
    Hien thi mot popup bao thanh cong (vi du: dang ky thanh cong).
    """
    hop_thoai = QMessageBox(cha)
    hop_thoai.setIcon(QMessageBox.Icon.Information)
    hop_thoai.setWindowTitle("Thanh cong")
    hop_thoai.setText(thong_bao)
    hop_thoai.exec()


def hien_thi_popup_xac_nhan(cau_hoi, cha=None):
    """
    Hien thi popup hoi Co/Khong, dung khi can nguoi dung xac nhan
    truoc khi thuc hien mot hanh dong (vi du: huy dang ky, xoa sinh vien).
    Tra ve True neu nguoi dung chon "Yes", False neu chon "No".
    """
    ket_qua = QMessageBox.question(
        cha, "Xac nhan", cau_hoi,
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
    )
    return ket_qua == QMessageBox.StandardButton.Yes
