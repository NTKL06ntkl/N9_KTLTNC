# ============================================================
# Module: data/data_mau.py  -- P2
# Tao san mot bo du lieu mau (mon hoc, lop hoc phan, sinh vien)
# de ca nhom dung chung khi kiem thu, khong can nhap tay tu dau.
# Xem chi tiet trong file INTERFACE.md, muc "Du lieu mau".
# ============================================================

from logic.mon_hoc import MonHoc
from logic.lop_hoc_phan import LopHocPhan
from logic.sinh_vien import SinhVien


def tao_du_lieu_mau():
    """
    Tao va tra ve mot dict gom 3 khoa:
        "mon_hoc"      : list cac object MonHoc
        "lop_hoc_phan" : list cac object LopHocPhan
        "sinh_vien"    : list cac object SinhVien

    Cach dung:
        from data.data_mau import tao_du_lieu_mau
        du_lieu = tao_du_lieu_mau()
        danh_sach_mon = du_lieu["mon_hoc"]
    """

    # ----- 1. Tao danh sach mon hoc -----
    mon_toan1 = MonHoc("TOAN1", "Toan cao cap 1", 3)
    mon_toan2 = MonHoc("TOAN2", "Toan cao cap 2", 3, ma_mon_tien_quyet="TOAN1")
    mon_ltcb = MonHoc("CS101", "Lap trinh co ban", 3)
    mon_ctdl = MonHoc("CS201", "Cau truc du lieu", 3, ma_mon_tien_quyet="CS101")
    mon_csdl = MonHoc("CS202", "Co so du lieu", 3, ma_mon_tien_quyet="CS101")
    mon_mang = MonHoc("CS301", "Mang may tinh", 3, ma_mon_tien_quyet="CS201")
    mon_nnlt = MonHoc("CS102", "Ngon ngu lap trinh", 2, ma_mon_tien_quyet="CS101")

    danh_sach_mon_hoc = [
        mon_toan1, mon_toan2, mon_ltcb, mon_ctdl, mon_csdl, mon_mang, mon_nnlt
    ]

    # ----- 2. Tao danh sach lop hoc phan -----
    # lich_hoc dang dict: {"thu": 2..7, "tiet_bat_dau": 1..10, "tiet_ket_thuc": 1..10}
    lop_toan1_01 = LopHocPhan(
        "TOAN1-01", mon_toan1, "Nguyen Van An", 40,
        {"thu": 2, "tiet_bat_dau": 1, "tiet_ket_thuc": 3}
    )
    lop_toan2_01 = LopHocPhan(
        "TOAN2-01", mon_toan2, "Nguyen Van An", 40,
        {"thu": 3, "tiet_bat_dau": 1, "tiet_ket_thuc": 3}
    )
    lop_ltcb_01 = LopHocPhan(
        "CS101-01", mon_ltcb, "Tran Thi Binh", 3,   # si so nho de de test "lop day"
        {"thu": 4, "tiet_bat_dau": 4, "tiet_ket_thuc": 6}
    )
    lop_ctdl_01 = LopHocPhan(
        "CS201-01", mon_ctdl, "Le Minh Cuong", 40,
        {"thu": 5, "tiet_bat_dau": 1, "tiet_ket_thuc": 3}
    )
    lop_csdl_01 = LopHocPhan(
        "CS202-01", mon_csdl, "Pham Thi Dung", 40,
        {"thu": 6, "tiet_bat_dau": 1, "tiet_ket_thuc": 3}
    )
    lop_mang_01 = LopHocPhan(
        "CS301-01", mon_mang, "Hoang Van Em", 40,
        {"thu": 2, "tiet_bat_dau": 7, "tiet_ket_thuc": 9}
    )
    lop_nnlt_01 = LopHocPhan(
        "CS102-01", mon_nnlt, "Dang Van Quan", 40,
        {"thu": 4, "tiet_bat_dau": 1, "tiet_ket_thuc": 2}
    )

    danh_sach_lop_hoc_phan = [
        lop_toan1_01, lop_toan2_01, lop_ltcb_01, lop_ctdl_01,
        lop_csdl_01, lop_mang_01, lop_nnlt_01
    ]

    # ----- 3. Tao danh sach sinh vien -----
    sv1 = SinhVien("SV001", "Nguyen Thanh Hai", "CNTT01")
    sv2 = SinhVien("SV002", "Tran Thi Mai Linh", "CNTT01")
    sv3 = SinhVien("SV003", "Le Quoc Bao", "CNTT02")
    sv4 = SinhVien("SV004", "Pham Ngoc Huong", "CNTT02")

    # SV001 da hoc xong TOAN1 va CS101 -> du dieu kien hoc CS201, TOAN2, CS102
    sv1.them_mon_da_hoc("TOAN1", 8.5)
    sv1.them_mon_da_hoc("CS101", 9.0)

    # SV002 da hoc xong CS101
    sv2.them_mon_da_hoc("CS101", 7.5)

    # SV003 chua hoc mon nao
    # SV004 da hoc TOAN1
    sv4.them_mon_da_hoc("TOAN1", 7.0)

    danh_sach_sinh_vien = [sv1, sv2, sv3, sv4]

    # ----- Tra ve dict tong hop -----
    return {
        "mon_hoc": danh_sach_mon_hoc,
        "lop_hoc_phan": danh_sach_lop_hoc_phan,
        "sinh_vien": danh_sach_sinh_vien,
    }
