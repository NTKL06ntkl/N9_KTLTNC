# ============================================================
# tests/test_logic.py
# File kiem thu co ban cho phan logic nghiep vu, khong dung GUI.
# Chay bang lenh: python -m pytest tests/  (neu co cai pytest)
# Hoac chay truc tiep: python tests/test_logic.py
# ============================================================

import sys
import os

# Them thu muc goc cua du an vao duong dan import, de "from logic..." hoat dong
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic.mon_hoc import MonHoc
from logic.lop_hoc_phan import LopHocPhan
from logic.sinh_vien import SinhVien
from logic.kiem_tra import (
    kiem_tra_tien_quyet, kiem_tra_xung_dot_lich, kiem_tra_si_so, kiem_tra_da_dang_ky,
    LoiChuaDuDieuKienTienQuyet, LoiXungDotLichHoc, LoiLopHocDayCho, LoiDaDangKyMonNay,
)


def test_kiem_tra_dieu_kien_hoc():
    """Mon khong co tien quyet thi luon du dieu kien."""
    mon_a = MonHoc("A", "Mon A", 3)
    sv = SinhVien("SV001", "Test", "L1")
    assert sv.kiem_tra_dieu_kien_hoc(mon_a) == True


def test_chua_du_tien_quyet():
    """Sinh vien chua hoc mon tien quyet thi khong du dieu kien."""
    mon_a = MonHoc("A", "Mon A", 3)
    mon_b = MonHoc("B", "Mon B", 3, ma_mon_tien_quyet="A")
    sv = SinhVien("SV001", "Test", "L1")

    assert sv.kiem_tra_dieu_kien_hoc(mon_b) == False

    da_bao_loi = False
    try:
        kiem_tra_tien_quyet(sv, mon_b)
    except LoiChuaDuDieuKienTienQuyet:
        da_bao_loi = True
    assert da_bao_loi == True


def test_dang_ky_thanh_cong():
    """Dang ky hop le phai cap nhat ca 2 phia (SV va LopHocPhan)."""
    mon_a = MonHoc("A", "Mon A", 3)
    lop_a = LopHocPhan("A-01", mon_a, "GV A", 30, {"thu": 2, "tiet_bat_dau": 1, "tiet_ket_thuc": 3})
    sv = SinhVien("SV001", "Test", "L1")

    sv.dang_ky(lop_a)

    assert len(sv.ds_mon_dang_ky) == 1
    assert len(lop_a.danh_sach_sv) == 1


def test_lop_day_cho():
    """Lop du si so phai bao loi LoiLopHocDayCho."""
    mon_a = MonHoc("A", "Mon A", 3)
    lop_a = LopHocPhan("A-01", mon_a, "GV A", 1, {"thu": 2, "tiet_bat_dau": 1, "tiet_ket_thuc": 3})

    sv1 = SinhVien("SV001", "Test 1", "L1")
    sv2 = SinhVien("SV002", "Test 2", "L1")

    sv1.dang_ky(lop_a)
    assert lop_a.la_day() == True

    da_bao_loi = False
    try:
        kiem_tra_si_so(lop_a)
    except LoiLopHocDayCho:
        da_bao_loi = True
    assert da_bao_loi == True


def test_xung_dot_lich():
    """Hai lop hoc cung thu, trung tiet thi phai bao loi LoiXungDotLichHoc."""
    mon_a = MonHoc("A", "Mon A", 3)
    mon_b = MonHoc("B", "Mon B", 3)

    lop_a = LopHocPhan("A-01", mon_a, "GV A", 30, {"thu": 2, "tiet_bat_dau": 1, "tiet_ket_thuc": 3})
    lop_b = LopHocPhan("B-01", mon_b, "GV B", 30, {"thu": 2, "tiet_bat_dau": 2, "tiet_ket_thuc": 4})

    sv = SinhVien("SV001", "Test", "L1")
    sv.dang_ky(lop_a)

    da_bao_loi = False
    try:
        kiem_tra_xung_dot_lich(sv, lop_b)
    except LoiXungDotLichHoc:
        da_bao_loi = True
    assert da_bao_loi == True


def test_dang_ky_trung_mon():
    """Dang ky 2 lan cung mot mon hoc phai bao loi LoiDaDangKyMonNay."""
    mon_a = MonHoc("A", "Mon A", 3)
    lop_a1 = LopHocPhan("A-01", mon_a, "GV A", 30, {"thu": 2, "tiet_bat_dau": 1, "tiet_ket_thuc": 3})
    lop_a2 = LopHocPhan("A-02", mon_a, "GV B", 30, {"thu": 4, "tiet_bat_dau": 1, "tiet_ket_thuc": 3})

    sv = SinhVien("SV001", "Test", "L1")
    sv.dang_ky(lop_a1)

    da_bao_loi = False
    try:
        kiem_tra_da_dang_ky(sv, lop_a2)
    except LoiDaDangKyMonNay:
        da_bao_loi = True
    assert da_bao_loi == True


def test_huy_dang_ky():
    """Huy dang ky phai xoa ca 2 phia (SV va LopHocPhan)."""
    mon_a = MonHoc("A", "Mon A", 3)
    lop_a = LopHocPhan("A-01", mon_a, "GV A", 30, {"thu": 2, "tiet_bat_dau": 1, "tiet_ket_thuc": 3})
    sv = SinhVien("SV001", "Test", "L1")

    sv.dang_ky(lop_a)
    sv.huy_dang_ky(lop_a)

    assert len(sv.ds_mon_dang_ky) == 0
    assert len(lop_a.danh_sach_sv) == 0


def test_tinh_dtb():
    """Kiem tra tinh diem trung binh co trong so tin chi."""
    mon_a = MonHoc("A", "Mon A", 2)
    mon_b = MonHoc("B", "Mon B", 4)
    sv = SinhVien("SV001", "Test", "L1")

    sv.them_mon_da_hoc("A", 8.0)
    sv.them_mon_da_hoc("B", 6.0)

    # DTB = (8*2 + 6*4) / (2+4) = (16+24)/6 = 6.67
    dtb = sv.tinh_dtb_co_trong_so([mon_a, mon_b])
    assert abs(dtb - 6.67) < 0.01


# ----- Chay truc tiep neu khong dung pytest -----
if __name__ == "__main__":
    danh_sach_ham_test = [
        test_kiem_tra_dieu_kien_hoc,
        test_chua_du_tien_quyet,
        test_dang_ky_thanh_cong,
        test_lop_day_cho,
        test_xung_dot_lich,
        test_dang_ky_trung_mon,
        test_huy_dang_ky,
        test_tinh_dtb,
    ]

    so_thanh_cong = 0
    so_that_bai = 0

    for ham_test in danh_sach_ham_test:
        ten_ham = ham_test.__name__
        try:
            ham_test()
            print("[PASS] " + ten_ham)
            so_thanh_cong += 1
        except AssertionError:
            print("[FAIL] " + ten_ham)
            so_that_bai += 1

    print("")
    print("Ket qua: " + str(so_thanh_cong) + " PASS / " + str(so_that_bai) + " FAIL")
