# ============================================================
# Module: data/data_mau.py  -- P2
# ============================================================

from logic.mon_hoc import MonHoc
from logic.lop_hoc_phan import LopHocPhan
from logic.sinh_vien import SinhVien


def tao_du_lieu_mau():
    # ----- Môn học -----
    mon_toan1  = MonHoc("TINDC01",  "Tin học đại cương ",       2)
    mon_toan2  = MonHoc("TH01",  "Triết học Mac-Lenin",       3)
    mon_ltcb   = MonHoc("CS101",  "Lập trình cơ bản",     3)
    mon_ctdl   = MonHoc("CS201",  "Cấu trúc dữ liệu",     3, ma_mon_tien_quyet="CS101")
    mon_csdl   = MonHoc("CS202",  "Cơ sở dữ liệu",        3, ma_mon_tien_quyet="CS101")
    mon_mang   = MonHoc("CS301",  "Mạng máy tính",         3, ma_mon_tien_quyet="CS201")
    mon_nnlt   = MonHoc("CS102",  "Ngôn ngữ lập trình",   2, ma_mon_tien_quyet="CS101")

    danh_sach_mon_hoc = [mon_toan1, mon_toan2, mon_ltcb, mon_ctdl, mon_csdl, mon_mang, mon_nnlt]

    # ----- Lớp học phần -----
    lop_toan1 = LopHocPhan("TINDC01-01", mon_toan1, "Nguyễn Văn An",   40, {"thu": 2, "tiet_bat_dau": 1, "tiet_ket_thuc": 3})
    lop_toan2 = LopHocPhan("TH01-01", mon_toan2, "Nguyễn Văn An",   40, {"thu": 3, "tiet_bat_dau": 1, "tiet_ket_thuc": 3})
    lop_ltcb  = LopHocPhan("CS101-01", mon_ltcb,  "Trần Thị Bình",    3, {"thu": 4, "tiet_bat_dau": 4, "tiet_ket_thuc": 6})
    lop_ctdl  = LopHocPhan("CS201-01", mon_ctdl,  "Lê Minh Cường",   40, {"thu": 5, "tiet_bat_dau": 1, "tiet_ket_thuc": 3})
    lop_csdl  = LopHocPhan("CS202-01", mon_csdl,  "Phạm Thị Dung",   40, {"thu": 6, "tiet_bat_dau": 1, "tiet_ket_thuc": 3})
    lop_mang  = LopHocPhan("CS301-01", mon_mang,  "Hoàng Văn Em",    40, {"thu": 2, "tiet_bat_dau": 7, "tiet_ket_thuc": 9})
    lop_nnlt  = LopHocPhan("CS102-01", mon_nnlt,  "Đặng Văn Quân",   40, {"thu": 4, "tiet_bat_dau": 1, "tiet_ket_thuc": 2})

    danh_sach_lop_hoc_phan = [lop_toan1, lop_toan2, lop_ltcb, lop_ctdl, lop_csdl, lop_mang, lop_nnlt]

    # ----- Sinh viên -----
    sv1 = SinhVien("SV001", "Nguyễn Thanh Hải",   "TIN01")
    sv2 = SinhVien("SV002", "Trần Thị Mai Linh",  "TIN01")
    sv3 = SinhVien("SV003", "Lê Quốc Bảo",        "TIN02")
    sv4 = SinhVien("SV004", "Phạm Ngọc Hương",    "TIN02")

    sv1.them_mon_da_hoc("TOAN1", 8.5)
    sv1.them_mon_da_hoc("CS101", 9.0)

    sv2.them_mon_da_hoc("CS101", 7.5)

    sv4.them_mon_da_hoc("TOAN1", 7.0)

    danh_sach_sinh_vien = [sv1, sv2, sv3, sv4]

    return {
        "mon_hoc": danh_sach_mon_hoc,
        "lop_hoc_phan": danh_sach_lop_hoc_phan,
        "sinh_vien": danh_sach_sinh_vien,
    }
