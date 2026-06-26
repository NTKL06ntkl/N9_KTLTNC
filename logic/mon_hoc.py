class MonHoc:
    """
    Lop MonHoc dung de luu thong tin cua mot mon hoc.

    Thuoc tinh:
        ma_mon            : ma dinh danh duy nhat, vi du "CS101"
        ten_mon           : ten hien thi, vi du "Lap trinh co ban"
        so_tin_chi        : so tin chi, vi du 3
        ma_mon_tien_quyet : ma mon hoc phai hoc truoc, hoac None neu khong co
    """

    def __init__(self, ma_mon, ten_mon, so_tin_chi, ma_mon_tien_quyet=None):
        self.ma_mon = ma_mon
        self.ten_mon = ten_mon
        self.so_tin_chi = so_tin_chi
        self.ma_mon_tien_quyet = ma_mon_tien_quyet

    def __str__(self):
        # dùng định dạng chuỗi để hiển thị đối tượng
        return self.ma_mon + " - " + self.ten_mon + " (" + str(self.so_tin_chi) + " TC)"
