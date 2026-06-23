# ============================================================
# Module: logic/kiem_tra.py  -- P4
# Chua cac ham kiem tra dieu kien nghiep vu (tien quyet, xung dot
# lich hoc, si so lop) va cac loai loi (Exception) dung chung
# cho toan he thong.
# Xem chi tiet trong file INTERFACE.md, muc "logic/kiem_tra.py"
# ============================================================


# ------------------------------------------------------------
# CAC NGOAI LE (Exception) DUNG CHUNG
# ------------------------------------------------------------

class LoiChuaDuDieuKienTienQuyet(Exception):
    """
    Loi nay phat sinh khi sinh vien chua hoc mon tien quyet.
    thong_bao: "Chua hoan thanh mon tien quyet: <ten_mon>"
    """
    def __init__(self, ten_mon):
        self.ten_mon = ten_mon
        self.thong_bao = "Chua hoan thanh mon tien quyet: " + str(ten_mon)
        super().__init__(self.thong_bao)


class LoiXungDotLichHoc(Exception):
    """
    Loi nay phat sinh khi lich cua lop moi dang ky bi trung
    voi mot lop da dang ky truoc do.
    thong_bao: "Xung dot lich voi lop: <ma_lop_hp>"
    """
    def __init__(self, ma_lop_hp):
        self.ma_lop_hp = ma_lop_hp
        self.thong_bao = "Xung dot lich voi lop: " + str(ma_lop_hp)
        super().__init__(self.thong_bao)


class LoiLopHocDayCho(Exception):
    """
    Loi nay phat sinh khi lop hoc phan da du si so toi da.
    thong_bao: "Lop <ma_lop_hp> da du si so toi da"
    """
    def __init__(self, ma_lop_hp):
        self.ma_lop_hp = ma_lop_hp
        self.thong_bao = "Lop " + str(ma_lop_hp) + " da du si so toi da"
        super().__init__(self.thong_bao)


class LoiDaDangKyMonNay(Exception):
    """
    Loi nay phat sinh khi sinh vien da dang ky mot lop hoc phan
    cua mon hoc nay roi (khong duoc dang ky trung mon).
    """
    def __init__(self, ten_mon):
        self.ten_mon = ten_mon
        self.thong_bao = "Ban da dang ky mon: " + str(ten_mon)
        super().__init__(self.thong_bao)


# ------------------------------------------------------------
# CAC HAM KIEM TRA DIEU KIEN
# ------------------------------------------------------------

def kiem_tra_tien_quyet(sv, mon):
    """
    Kiem tra sinh vien da hoc mon tien quyet cua "mon" hay chua.
    Neu mon khong co tien quyet (ma_mon_tien_quyet la None) thi luon hop le.
    Neu chua du dieu kien -> bao loi LoiChuaDuDieuKienTienQuyet.
    """
    da_du_dieu_kien = sv.kiem_tra_dieu_kien_hoc(mon)
    if not da_du_dieu_kien:
        raise LoiChuaDuDieuKienTienQuyet(mon.ma_mon_tien_quyet)


def _hai_lich_co_trung_khong(lich_1, lich_2):
    """
    Ham phu: so sanh 2 lich hoc (dict co "thu", "tiet_bat_dau", "tiet_ket_thuc").
    Tra ve True neu 2 lich bi trung (cung thu va co tiet hoc giao nhau).
    """
    # Khac thu thi chac chan khong trung
    if lich_1["thu"] != lich_2["thu"]:
        return False

    # Cung thu -> kiem tra xem khoang tiet hoc co giao nhau khong
    bat_dau_1 = lich_1["tiet_bat_dau"]
    ket_thuc_1 = lich_1["tiet_ket_thuc"]
    bat_dau_2 = lich_2["tiet_bat_dau"]
    ket_thuc_2 = lich_2["tiet_ket_thuc"]

    # Khong giao nhau khi: lop 1 ket thuc truoc khi lop 2 bat dau
    #                  hoac lop 2 ket thuc truoc khi lop 1 bat dau
    khong_giao_nhau = (ket_thuc_1 < bat_dau_2) or (ket_thuc_2 < bat_dau_1)

    return not khong_giao_nhau


def kiem_tra_xung_dot_lich(sv, lop_hp):
    """
    So sanh lich hoc cua lop_hp voi tat ca cac lop ma sinh vien
    da dang ky truoc do (sv.ds_mon_dang_ky).
    Neu trung lich voi bat ky lop nao -> bao loi LoiXungDotLichHoc.
    """
    danh_sach_lop_da_dang_ky = sv.ds_mon_dang_ky.duyet()

    for lop_da_dang_ky in danh_sach_lop_da_dang_ky:
        bi_trung = _hai_lich_co_trung_khong(lop_da_dang_ky.lich_hoc, lop_hp.lich_hoc)
        if bi_trung:
            raise LoiXungDotLichHoc(lop_da_dang_ky.ma_lop_hp)


def kiem_tra_si_so(lop_hp):
    """
    Kiem tra lop hoc phan con cho trong hay khong.
    Neu lop da day -> bao loi LoiLopHocDayCho.
    """
    if lop_hp.la_day():
        raise LoiLopHocDayCho(lop_hp.ma_lop_hp)


def kiem_tra_da_dang_ky(sv, lop_hp):
    """
    Kiem tra sinh vien co dang ky mon hoc cua lop_hp roi chua
    (mot sinh vien khong duoc dang ky 2 lop cung mon hoc).
    Neu da dang ky roi -> bao loi LoiDaDangKyMonNay.
    """
    danh_sach_lop_da_dang_ky = sv.ds_mon_dang_ky.duyet()

    for lop_da_dang_ky in danh_sach_lop_da_dang_ky:
        cung_mon_hoc = (lop_da_dang_ky.mon_hoc.ma_mon == lop_hp.mon_hoc.ma_mon)
        if cung_mon_hoc:
            raise LoiDaDangKyMonNay(lop_hp.mon_hoc.ten_mon)
