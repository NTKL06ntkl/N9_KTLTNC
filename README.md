# He thong Quan ly Khoa hoc va Dang ky Tin chi

Do an mon Ky thuat Lap trinh Nang cao - Nhom 9 (N9_KTLTNC)
Giao dien: **PyQt6**

## Cach chay

```bash
# Buoc 1: Cai dat thu vien can thiet
pip install -r requirements.txt

# Buoc 2: Chay ung dung (trong VS Code, mo Terminal roi go)
python main.py
```

Neu may chua co `reportlab`, chuc nang "Xuat phieu PDF" se tu dong xuat ra file `.txt` thay the. Cai `pip install reportlab` de co PDF thuc su.

## Cau truc thu muc (theo dung INTERFACE.md)

```
course-management/
├── main.py                      # Diem khoi chay ung dung
├── requirements.txt
├── INTERFACE.md                 # Dac ta interface chung cua nhom
├── README.md
│
├── logic/                       # Toan bo logic nghiep vu (khong dung GUI)
│   ├── mon_hoc.py                -- P1: lop MonHoc
│   ├── lop_hoc_phan.py            -- P1: lop LopHocPhan
│   ├── sinh_vien.py               -- P2: lop SinhVien
│   ├── kiem_tra.py                -- P4: cac ham kiem tra dieu kien + Exception
│   └── file_handler.py            -- P5: luu/doc JSON, xuat phieu (TACH RIENG)
│
├── data_structures/             # Cau truc du lieu tu cai dat -- P3
│   ├── doubly_linked_list.py      Danh sach lien ket doi (Nut, DanhSachLienKetDoi)
│   └── hash_set.py                 Hash Set (TapHopBam)
│
├── data/
│   ├── data_mau.py                -- P2: du lieu mau de test
│   └── data.json                  (tu tao khi chay lan dau, luu trang thai he thong)
│
├── gui/                          # Giao dien PyQt6
│   ├── ui_constants.py            -- P1: mau sac, font, stylesheet chung
│   ├── main_window.py             -- P1: cua so chinh, dieu phoi man hinh
│   ├── screen_mon_hoc.py          -- P1: man hinh danh sach mon hoc
│   ├── screen_lop_hp.py           -- P1: man hinh danh sach lop hoc phan
│   ├── screen_login.py            -- P2: man hinh dang nhap
│   ├── screen_sinh_vien.py       -- P2: man hinh chinh Sinh vien (dang ky/huy/xuat phieu)
│   ├── screen_lich_su.py         -- P2: man hinh ket qua hoc tap
│   ├── screen_tkb.py              -- P4: man hinh thoi khoa bieu tam thoi
│   ├── popup_error.py             -- P4: cac popup thong bao loi/thanh cong
│   └── screen_admin.py            -- P5: man hinh quan ly (Admin)
│
└── output/                       # Cac phieu dang ky duoc xuat ra (.txt / .pdf)
```

## Phan cong theo INTERFACE.md

| Phan | Phu trach | File |
|------|-----------|------|
| P1 | MonHoc, LopHocPhan, GUI khung chinh + danh sach mon/lop | logic/mon_hoc.py, logic/lop_hoc_phan.py, gui/main_window.py, gui/screen_mon_hoc.py, gui/screen_lop_hp.py, gui/ui_constants.py |
| P2 | SinhVien, man hinh dang nhap + man hinh Sinh vien | logic/sinh_vien.py, gui/screen_login.py, gui/screen_sinh_vien.py, gui/screen_lich_su.py, data/data_mau.py |
| P3 | Cau truc du lieu (DLL, Hash Set) | data_structures/doubly_linked_list.py, data_structures/hash_set.py |
| P4 | Kiem tra dieu kien, Exception, TKB, popup | logic/kiem_tra.py, gui/screen_tkb.py, gui/popup_error.py |
| P5 | Luu/doc file JSON, xuat phieu, man hinh Admin | logic/file_handler.py, gui/screen_admin.py |

**Quan trong:** `logic/file_handler.py` (P5) khong sua doi gi trong cac lop
`MonHoc`, `LopHocPhan`, `SinhVien`. No chi `import` cac lop nay va tu doc thuoc
tinh co san (vi du `mon.ma_mon`, `sv.ho_ten`) de gom thanh dict roi ghi ra JSON.
Cac phan P1/P2/P3 hoan toan doc lap, khong can biet P5 luu file nhu the nao.

## Tinh nang da cai dat

### Phan he Sinh vien
- Dang nhap chon theo ma SV
- Xem danh sach lop hoc phan dang mo trong hoc ky
- Dang ky lop hoc phan, voi kiem tra du 4 dieu kien theo dung thu tu:
  1. Da hoc mon tien quyet chua (kiem_tra_tien_quyet)
  2. Da dang ky mon nay roi chua (kiem_tra_da_dang_ky)
  3. Co trung lich voi lop da dang ky khong (kiem_tra_xung_dot_lich)
  4. Lop con cho khong (kiem_tra_si_so)
- Huy dang ky (co hoi xac nhan)
- Xem thoi khoa bieu tam thoi (sap xep theo thu, tiet)
- Xem lich su hoc tap + diem trung binh co trong so tin chi
- Xuat phieu dang ky ra file .txt hoac .pdf

### Phan he Quan ly (Admin)
- Tab Lop hoc phan: them lop moi, dong/mo lop, xem danh sach SV cua lop
- Tab Mon hoc: them mon hoc moi, chon mon tien quyet
- Tab Sinh vien: them/xoa sinh vien, xem DTB va so lop dang ky

## Cau truc du lieu va ky thuat nang cao

- Danh sach lien ket doi (Doubly Linked List) tu cai dat (data_structures/doubly_linked_list.py):
  dung de luu danh_sach_sv trong moi LopHocPhan va ds_mon_dang_ky trong moi SinhVien.
- Hash Set (Tap Hop Bam) tu cai dat (data_structures/hash_set.py):
  dung de luu ds_mon_da_hoc cua sinh vien, kiem tra mon da hoc voi do phuc tap O(1).
- Exception Handling: LoiChuaDuDieuKienTienQuyet, LoiXungDotLichHoc,
  LoiLopHocDayCho, LoiDaDangKyMonNay -- dinh nghia trong logic/kiem_tra.py.
- Luu tru file: toan bo he thong duoc luu trong mot file JSON duy nhat
  (data/data.json), tu dong tai lai khi mo ung dung lan sau.
- Cap nhat tham chieu 2 chieu: khi dang ky / huy dang ky, ca SinhVien.ds_mon_dang_ky
  va LopHocPhan.danh_sach_sv deu duoc cap nhat dong thoi, dam bao du lieu luon dong bo.

## Du lieu mau

4 sinh vien (SV001-SV004), 7 mon hoc co quan he tien quyet, 7 lop hoc phan voi
lich hoc va giang vien cu the. Lop "CS101-01" co si so toi da chi 3 de de test
truong hop lop bi day.
