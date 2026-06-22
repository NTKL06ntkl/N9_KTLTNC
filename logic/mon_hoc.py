class MonHoc:
    def __init__(self, ma_mon, ten_mon, so_tin_chi, ma_mon_tien_quyet=None):
        self.ma_mon = ma_mon
        self.ten_mon = ten_mon
        self.so_tin_chi = so_tin_chi
        self.ma_mon_tien_quyet = ma_mon_tien_quyet

    def co_mon_tien_quyet(self):
        return self.ma_mon_tien_quyet is not None

    def lay_thong_tin(self):
        return {
            "ma_mon": self.ma_mon,
            "ten_mon": self.ten_mon,
            "so_tin_chi": self.so_tin_chi,
            "ma_mon_tien_quyet": self.ma_mon_tien_quyet
        }

    def hien_thi(self):
        print("Mã môn:", self.ma_mon)
        print("Tên môn:", self.ten_mon)
        print("Số tín chỉ:", self.so_tin_chi)

        if self.co_mon_tien_quyet():
            print("Môn tiên quyết:", self.ma_mon_tien_quyet)
        else:
            print("Không có môn tiên quyết")