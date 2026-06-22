class LoiLopHocDayCho(Exception):
    pass
from data_structures.doubly_linked_list import DanhSachLienKetDoi
class LopHocPhan:
    def __init__(self, ma_lop_hp, mon_hoc, giang_vien, si_so_toi_da):
        self.ma_lop_hp = ma_lop_hp          
        self.mon_hoc = mon_hoc              
        self.giang_vien = giang_vien        
        self.si_so_toi_da = si_so_toi_da    
        self.danh_sach_sv = DanhSachLienKetDoi() 
        
        self.lich_hoc = {"thu": 2, "tiet_bat_dau": 1, "tiet_ket_thuc": 3}

    def la_day(self):
        return len(self.danh_sach_sv) >= self.si_so_toi_da

    def them_sv(self, sv):
        if self.la_day():
            raise LoiLopHocDayCho("Lớp học phần đã đạt sĩ số tối đa!")
        self.danh_sach_sv.them_cuoi(sv)

    def xoa_sv(self, sv):
        self.danh_sach_sv.xoa(sv)

    def hien_thi(self):
        print("Mã lớp học phần:", self.ma_lop_hp)
        print("Thuộc môn học:", self.mon_hoc.ten_mon)
        print("Giảng viên:", self.giang_vien)
        print("Sĩ số hiện tại:", len(self.danh_sach_sv), "/", self.si_so_toi_da)
        print("Lịch học: Thứ", self.lich_hoc["thu"], "từ tiết", self.lich_hoc["tiet_bat_dau"], "đến", self.lich_hoc["tiet_ket_thuc"])