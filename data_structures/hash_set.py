class TapHopBam:
    def __init__(self, dung_luong=16):
        self.dung_luong = dung_luong
        self.buckets = [[] for _ in range(dung_luong)]

    def _tinh_chi_so(self, phan_tu):
        return hash(phan_tu) % self.dung_luong

    def them(self, phan_tu):
        chi_so = self._tinh_chi_so(phan_tu)

        if phan_tu not in self.buckets[chi_so]:
            self.buckets[chi_so].append(phan_tu)

    def chua(self, phan_tu):
        chi_so = self._tinh_chi_so(phan_tu)

        return phan_tu in self.buckets[chi_so]

    def xoa(self, phan_tu):
        chi_so = self._tinh_chi_so(phan_tu)

        if phan_tu in self.buckets[chi_so]:
            self.buckets[chi_so].remove(phan_tu)
