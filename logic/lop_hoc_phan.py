from data_structures.doubly_linked_list import DanhSachLienKetDoi
from logic.kiem_tra import LoiLopHocDayCho


class LopHocPhan:
    """
    Thuoc tinh:
        ma_lop_hp     : ma lop hoc phan, vi du "CS101-01"
        mon_hoc       : object MonHoc (khong phai chi la ma mon)
        giang_vien    : ten giang vien
        si_so_toi_da  : so sinh vien toi da duoc dang ky vao lop
        danh_sach_sv  : DanhSachLienKetDoi chua cac SinhVien da dang ky
        lich_hoc      : dict dang {"thu": int, "tiet_bat_dau": int, "tiet_ket_thuc": int}
    """

    def __init__(self, ma_lop_hp, mon_hoc, giang_vien, si_so_toi_da, lich_hoc=None):
        self.ma_lop_hp = ma_lop_hp
        self.mon_hoc = mon_hoc
        self.giang_vien = giang_vien
        self.si_so_toi_da = si_so_toi_da
        self.danh_sach_sv = DanhSachLienKetDoi()
        if lich_hoc is None:
            lich_hoc = {"thu": 2, "tiet_bat_dau": 1, "tiet_ket_thuc": 3}
        self.lich_hoc = lich_hoc
        self.dang_mo = True

    def la_day(self):
        """
        Tra ve True neu so sinh vien hien tai >= si so toi da.
        """
        so_sv_hien_tai = len(self.danh_sach_sv)
        return so_sv_hien_tai >= self.si_so_toi_da

    def them_sv(self, sv):
        """
        Them sinh vien vao danh_sach_sv.
        Neu lop da day (la_day() == True) thi bao loi LoiLopHocDayCho.
        """
        if self.la_day():
            raise LoiLopHocDayCho(self.ma_lop_hp)
        self.danh_sach_sv.them_cuoi(sv)

    def xoa_sv(self, sv):
        """
        Xoa sinh vien khoi danh_sach_sv.
        """
        self.danh_sach_sv.xoa(sv)

    def __str__(self):
        return self.ma_lop_hp + " - " + self.mon_hoc.ten_mon + " (GV: " + self.giang_vien + ")"
