class Nut:
    def __init__(self, du_lieu):
        self.du_lieu = du_lieu
        self.prev = None
        self.next = None

class DanhSachLienKetDoi:
    def __init__(self):
        self.head = None
        self.tail = None
        self.so_luong = 0

    def __len__(self):
        return self.so_luong

    def them_cuoi(self, du_lieu):
        nut_moi = Nut(du_lieu)

        if self.head is None:
            self.head = nut_moi
            self.tail = nut_moi
        else:
            nut_moi.prev = self.tail
            self.tail.next = nut_moi
            self.tail = nut_moi

        self.so_luong += 1

    def them_dau(self, du_lieu):
        nut_moi = Nut(du_lieu)
        if self.head is None:
            self.head = nut_moi
            self.tail = nut_moi
        else:
            nut_moi.next = self.head
            self.head.prev = nut_moi
            self.head = nut_moi
        
        self.so_luong += 1

    def duyet(self):
        ket_qua = []
        hien_tai = self.head
        
        while hien_tai is not None:
            ket_qua.append(hien_tai.du_lieu)
            hien_tai = hien_tai.next
        
        return ket_qua
    
    def tim(self, du_lieu):
        hien_tai = self.head
        
        while hien_tai is not None:
            if hien_tai.du_lieu == du_lieu:
                return hien_tai
            
            hien_tai = hien_tai.next
        
        return None
    
    def xoa(self, du_lieu):
        nut_can_xoa = self.tim(du_lieu)

        if nut_can_xoa is None:
            return
        
        if nut_can_xoa == self.head and nut_can_xoa == self.tail:
            self.head = None
            self.tail = None
        
        elif nut_can_xoa == self.head:
            self.head = nut_can_xoa.next
            self.head.prev = None
        
        elif nut_can_xoa == self.tail:
            self.tail = nut_can_xoa.prev
            self.tail.next = None
            
        else:
            nut_can_xoa.prev.next = nut_can_xoa.next
            nut_can_xoa.next.prev = nut_can_xoa.prev

        self.so_luong -= 1
