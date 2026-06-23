# ============================================================
# Module: logic/sinh_vien.py  -- P2
# Lop SinhVien: dai dien cho mot sinh vien trong he thong.
# Xem chi tiet trong file INTERFACE.md, muc "logic/sinh_vien.py"
# ============================================================

from data_structures.doubly_linked_list import DanhSachLienKetDoi
from data_structures.hash_set import TapHopBam


class SinhVien:
    """
    Thuoc tinh:
        ma_sv          : ma sinh vien, vi du "SV001"
        ho_ten         : ho va ten day du
        lop_sh         : lop sinh hoat, vi du "CNTT01"
        ds_mon_da_hoc  : TapHopBam chua MA MON da hoc xong (P3 cung cap)
        ds_mon_dang_ky : DanhSachLienKetDoi chua cac LopHocPhan dang dang ky (P3 cung cap)
    """

    def __init__(self, ma_sv, ho_ten, lop_sh):
        self.ma_sv = ma_sv
        self.ho_ten = ho_ten
        self.lop_sh = lop_sh

        # Tap hop cac ma mon da hoc xong (dung Hash Set de tra cuu nhanh)
        self.ds_mon_da_hoc = TapHopBam()

        # Danh sach cac lop hoc phan dang dang ky (dung Danh sach lien ket doi)
        self.ds_mon_dang_ky = DanhSachLienKetDoi()

        # Tu dien luu diem cua tung mon da hoc, dung de tinh diem trung binh
        # vi du: {"CS101": 8.5, "CS201": 7.0}
        self.diem_cac_mon = {}

    def them_mon_da_hoc(self, ma_mon, diem):
        """
        Ham ho tro: ghi nhan sinh vien da hoc xong mot mon hoc, kem diem so.
        (Dung khi tao du lieu mau, hoac khi sinh vien hoan thanh mon hoc)
        """
        self.ds_mon_da_hoc.them(ma_mon)
        self.diem_cac_mon[ma_mon] = diem

    def tinh_dtb(self):
        """
        Tinh diem trung binh co trong so theo so tin chi.
        Cong thuc: tong(diem_mon * so_tin_chi_mon) / tong(so_tin_chi)
        Vi diem_cac_mon chi luu diem theo ma mon (khong luu so tin chi),
        ham nay can duoc goi voi danh sach MonHoc tuong ung de biet so tin chi.
        De don gian, neu khong co thong tin tin chi thi tinh trung binh thuong.
        Tra ve 0.0 neu chua hoc mon nao.
        """
        if len(self.diem_cac_mon) == 0:
            return 0.0

        tong_diem = 0
        for ma_mon in self.diem_cac_mon:
            tong_diem = tong_diem + self.diem_cac_mon[ma_mon]

        diem_trung_binh = tong_diem / len(self.diem_cac_mon)
        return round(diem_trung_binh, 2)

    def tinh_dtb_co_trong_so(self, danh_sach_mon_hoc):
        """
        Phien ban tinh DTB co trong so theo tin chi.
        Tham so danh_sach_mon_hoc la mot list cac object MonHoc,
        dung de tra ra so_tin_chi cua tung mon da hoc.
        """
        if len(self.diem_cac_mon) == 0:
            return 0.0

        tong_diem_x_tin_chi = 0
        tong_tin_chi = 0

        for mon in danh_sach_mon_hoc:
            if mon.ma_mon in self.diem_cac_mon:
                diem = self.diem_cac_mon[mon.ma_mon]
                tong_diem_x_tin_chi = tong_diem_x_tin_chi + diem * mon.so_tin_chi
                tong_tin_chi = tong_tin_chi + mon.so_tin_chi

        if tong_tin_chi == 0:
            return 0.0

        return round(tong_diem_x_tin_chi / tong_tin_chi, 2)

    def kiem_tra_dieu_kien_hoc(self, mon):
        """
        Kiem tra sinh vien co du dieu kien hoc mon "mon" hay khong.
        - Neu mon khong co mon tien quyet (ma_mon_tien_quyet la None)
          thi luon du dieu kien -> tra ve True.
        - Neu co mon tien quyet, kiem tra ma mon tien quyet do
          co nam trong ds_mon_da_hoc khong.
        """
        if mon.ma_mon_tien_quyet is None:
            return True

        da_hoc_mon_tien_quyet = self.ds_mon_da_hoc.chua(mon.ma_mon_tien_quyet)
        return da_hoc_mon_tien_quyet

    def dang_ky(self, lop_hp):
        """
        Dang ky mot lop hoc phan cho sinh vien.
        Buoc 1: them lop_hp vao ds_mon_dang_ky cua sinh vien.
        Buoc 2: goi lop_hp.them_sv(self) de dong bo hai chieu
                (lop hoc phan cung phai biet sinh vien nay da dang ky).
        Luu y: ham nay KHONG tu kiem tra dieu kien / xung dot lich / si so.
        Viec kiem tra do la trach nhiem cua logic/kiem_tra.py (P4),
        phai goi cac ham kiem tra TRUOC khi goi dang_ky().
        """
        self.ds_mon_dang_ky.them_cuoi(lop_hp)
        lop_hp.them_sv(self)

    def huy_dang_ky(self, lop_hp):
        """
        Huy dang ky mot lop hoc phan.
        Buoc 1: xoa lop_hp khoi ds_mon_dang_ky cua sinh vien.
        Buoc 2: goi lop_hp.xoa_sv(self) de dong bo hai chieu.
        """
        self.ds_mon_dang_ky.xoa(lop_hp)
        lop_hp.xoa_sv(self)

    def __str__(self):
        return self.ma_sv + " - " + self.ho_ten + " (" + self.lop_sh + ")"
