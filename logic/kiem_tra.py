class LoiChuaDuDieuKienTienQuyet(Exception):
    def __init__(self, ten_mon):
        self.ten_mon = ten_mon
        self.thong_bao = "Chưa hoàn thành môn tiên quyết: " + str(ten_mon)
        super().__init__(self.thong_bao)


class LoiXungDotLichHoc(Exception):
    def __init__(self, ma_lop_hp):
        self.ma_lop_hp = ma_lop_hp
        self.thong_bao = "Xung đột lịch với lớp: " + str(ma_lop_hp)
        super().__init__(self.thong_bao)


class LoiLopHocDayCho(Exception):
    def __init__(self, ma_lop_hp):
        self.ma_lop_hp = ma_lop_hp
        self.thong_bao = "Lớp " + str(ma_lop_hp) + " đã đủ sĩ số tối đa"
        super().__init__(self.thong_bao)


class LoiDaDangKyMonNay(Exception):
    def __init__(self, ten_mon):
        self.ten_mon = ten_mon
        self.thong_bao = "Bạn đã đăng ký môn: " + str(ten_mon)
        super().__init__(self.thong_bao)


def kiem_tra_tien_quyet(sv, mon):
    if not sv.kiem_tra_dieu_kien_hoc(mon):
        raise LoiChuaDuDieuKienTienQuyet(mon.ma_mon_tien_quyet)


def _hai_lich_co_trung_khong(lich_1, lich_2):
    if lich_1["thu"] != lich_2["thu"]:
        return False
    khong_giao = (lich_1["tiet_ket_thuc"] < lich_2["tiet_bat_dau"]) or \
                 (lich_2["tiet_ket_thuc"] < lich_1["tiet_bat_dau"])
    return not khong_giao


def kiem_tra_xung_dot_lich(sv, lop_hp):
    for lop_da_dk in sv.ds_mon_dang_ky.duyet():
        if _hai_lich_co_trung_khong(lop_da_dk.lich_hoc, lop_hp.lich_hoc):
            raise LoiXungDotLichHoc(lop_da_dk.ma_lop_hp)


def kiem_tra_si_so(lop_hp):
    if lop_hp.la_day():
        raise LoiLopHocDayCho(lop_hp.ma_lop_hp)


def kiem_tra_da_dang_ky(sv, lop_hp):
    for lop_da_dk in sv.ds_mon_dang_ky.duyet():
        if lop_da_dk.mon_hoc.ma_mon == lop_hp.mon_hoc.ma_mon:
            raise LoiDaDangKyMonNay(lop_hp.mon_hoc.ten_mon)
