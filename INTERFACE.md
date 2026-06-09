# INTERFACE.md — Hệ thống Quản lý Khóa học & Đăng ký Tín chỉ

> **Mục đích:** File này liệt kê toàn bộ class, hàm, tham số, kiểu trả về và ngoại lệ của tất cả module.
> Mọi người đọc file này để biết cách gọi code của nhau **mà không cần đọc toàn bộ mã nguồn**.

---

## Cấu trúc thư mục dự án

```
course-management/
├── logic/
│   ├── mon_hoc.py          # P1
│   ├── lop_hoc_phan.py     # P1
│   ├── sinh_vien.py        # P2
│   ├── kiem_tra.py         # P4
│   └── file_handler.py     # P5
├── data_structures/
│   ├── doubly_linked_list.py   # P3
│   └── hash_set.py             # P3
├── gui/
│   ├── ui_constants.py     # P1 (dùng chung toàn nhóm)
│   ├── main_window.py      # P1
│   ├── screen_mon_hoc.py   # P1
│   ├── screen_lop_hp.py    # P1
│   ├── screen_login.py     # P2
│   ├── screen_sinh_vien.py # P2
│   ├── screen_lich_su.py   # P2
│   ├── screen_tkb.py       # P4
│   ├── popup_error.py      # P4
│   └── screen_admin.py     # P5
├── data/
│   ├── data_mau.py         # P2
│   └── data.json           # P5 (sinh ra khi lưu)
├── tests/
└── main.py
```

---

## Module: `logic/mon_hoc.py` — **P1**

### Lớp `MonHoc`

```python
MonHoc(ma_mon: str, ten_mon: str, so_tin_chi: int, ma_mon_tien_quyet: str | None = None)
```

| Thuộc tính | Kiểu | Mô tả |
|---|---|---|
| `ma_mon` | `str` | Mã định danh duy nhất (VD: "CS101") |
| `ten_mon` | `str` | Tên hiển thị (VD: "Lập trình cơ bản") |
| `so_tin_chi` | `int` | Số tín chỉ (VD: 3) |
| `ma_mon_tien_quyet` | `str \| None` | Mã môn phải học trước; `None` nếu không có |

**Ví dụ khởi tạo:**
```python
m1 = MonHoc("CS101", "Lập trình cơ bản", 3)
m2 = MonHoc("CS201", "Cấu trúc dữ liệu", 3, ma_mon_tien_quyet="CS101")
```

---

## Module: `logic/lop_hoc_phan.py` — **P1**

### Lớp `LopHocPhan`

```python
LopHocPhan(ma_lop_hp: str, mon_hoc: MonHoc, giang_vien: str, si_so_toi_da: int)
```

| Thuộc tính | Kiểu | Mô tả |
|---|---|---|
| `ma_lop_hp` | `str` | Mã lớp học phần (VD: "CS101-01") |
| `mon_hoc` | `MonHoc` | Đối tượng MonHoc (không phải chỉ mã) |
| `giang_vien` | `str` | Tên giảng viên |
| `si_so_toi_da` | `int` | Số sinh viên tối đa |
| `danh_sach_sv` | `DanhSachLienKetDoi` | Danh sách SinhVien đã đăng ký (P3 cung cấp) |
| `lich_hoc` | `dict` | `{"thu": int, "tiet_bat_dau": int, "tiet_ket_thuc": int}` |

#### Hàm `them_sv(sv: SinhVien) -> None`
- Thêm sinh viên vào `danh_sach_sv`
- **Ngoại lệ:** `LoiLopHocDayCho` nếu `la_day()` trả về `True`

#### Hàm `xoa_sv(sv: SinhVien) -> None`
- Xóa sinh viên khỏi `danh_sach_sv`

#### Hàm `la_day() -> bool`
- Trả về `True` nếu `len(danh_sach_sv) >= si_so_toi_da`

**Ví dụ sử dụng:**
```python
lop = LopHocPhan("CS101-01", m1, "Nguyễn Văn A", 30)
lop.them_sv(sv)      # thêm SV vào lớp
lop.la_day()         # → True/False
lop.xoa_sv(sv)       # xóa SV khỏi lớp
```

---

## Module: `logic/sinh_vien.py` — **P2**

### Lớp `SinhVien`

```python
SinhVien(ma_sv: str, ho_ten: str, lop_sh: str)
```

| Thuộc tính | Kiểu | Mô tả |
|---|---|---|
| `ma_sv` | `str` | Mã sinh viên (VD: "SV001") |
| `ho_ten` | `str` | Họ và tên đầy đủ |
| `lop_sh` | `str` | Lớp sinh hoạt (VD: "CNTT01") |
| `ds_mon_da_hoc` | `TapHopBam` | Tập hợp mã môn đã hoàn thành (P3) |
| `ds_mon_dang_ky` | `DanhSachLienKetDoi` | Danh sách `LopHocPhan` đang đăng ký (P3) |

#### Hàm `tinh_dtb() -> float`
- Tính điểm trung bình có trọng số theo số tín chỉ
- Trả về `0.0` nếu chưa học môn nào

#### Hàm `kiem_tra_dieu_kien_hoc(mon: MonHoc) -> bool`
- Kiểm tra `mon.ma_mon_tien_quyet` có trong `ds_mon_da_hoc` không
- Trả về `True` nếu đủ điều kiện hoặc môn không có tiên quyết

#### Hàm `dang_ky(lop_hp: LopHocPhan) -> None`
- Thêm `lop_hp` vào `ds_mon_dang_ky` của sinh viên
- Đồng thời gọi `lop_hp.them_sv(self)` để đồng bộ hai chiều

#### Hàm `huy_dang_ky(lop_hp: LopHocPhan) -> None`
- Xóa `lop_hp` khỏi `ds_mon_dang_ky` của sinh viên
- Đồng thời gọi `lop_hp.xoa_sv(self)` để đồng bộ hai chiều

**Ví dụ sử dụng:**
```python
sv = SinhVien("SV001", "Trần Thị B", "CNTT01")
sv.kiem_tra_dieu_kien_hoc(mon_cs201)   # → True/False
sv.dang_ky(lop_cs101_01)               # đăng ký lớp
sv.tinh_dtb()                          # → 7.5
sv.huy_dang_ky(lop_cs101_01)           # hủy đăng ký
```

---

## Module: `data_structures/doubly_linked_list.py` — **P3**

### Lớp `DanhSachLienKetDoi`

```python
DanhSachLienKetDoi()
```

| Hàm | Tham số | Trả về | Mô tả |
|---|---|---|---|
| `them_cuoi(du_lieu)` | `du_lieu: any` | `None` | Thêm vào cuối |
| `them_dau(du_lieu)` | `du_lieu: any` | `None` | Thêm vào đầu |
| `xoa(du_lieu)` | `du_lieu: any` | `None` | Xóa nút chứa `du_lieu` |
| `tim(du_lieu)` | `du_lieu: any` | `Nut \| None` | Tìm nút, trả về `None` nếu không có |
| `duyet()` | — | `list` | Trả về danh sách các `du_lieu` theo thứ tự |
| `__len__()` | — | `int` | Số lượng phần tử |

**Ví dụ sử dụng:**
```python
ds = DanhSachLienKetDoi()
ds.them_cuoi(sv1)
ds.them_cuoi(sv2)
ds.duyet()       # → [sv1, sv2]
ds.xoa(sv1)
len(ds)          # → 1
```

---

## Module: `data_structures/hash_set.py` — **P3**

### Lớp `TapHopBam`

```python
TapHopBam(dung_luong: int = 16)
```

| Hàm | Tham số | Trả về | Mô tả |
|---|---|---|---|
| `them(phan_tu)` | `phan_tu: any` | `None` | Thêm phần tử; bỏ qua nếu đã tồn tại |
| `chua(phan_tu)` | `phan_tu: any` | `bool` | Kiểm tra tồn tại — O(1) trung bình |
| `xoa(phan_tu)` | `phan_tu: any` | `None` | Xóa phần tử |

**Ví dụ sử dụng:**
```python
tap = TapHopBam()
tap.them("CS101")
tap.chua("CS101")    # → True
tap.chua("CS999")    # → False
tap.xoa("CS101")
```

---

## Module: `logic/kiem_tra.py` — **P4**

### Hàm `kiem_tra_tien_quyet(sv: SinhVien, mon: MonHoc) -> None`
- Kiểm tra sinh viên đã học môn tiên quyết chưa
- **Ngoại lệ:** `LoiChuaDuDieuKienTienQuyet` nếu chưa học

### Hàm `kiem_tra_xung_dot_lich(sv: SinhVien, lop_hp: LopHocPhan) -> None`
- So sánh lịch `lop_hp` với tất cả lớp trong `sv.ds_mon_dang_ky`
- **Ngoại lệ:** `LoiXungDotLichHoc` nếu trùng buổi/tiết

### Hàm `kiem_tra_si_so(lop_hp: LopHocPhan) -> None`
- **Ngoại lệ:** `LoiLopHocDayCho` nếu `lop_hp.la_day()` = `True`

### Các ngoại lệ (kế thừa từ `Exception`)

```python
class LoiChuaDuDieuKienTienQuyet(Exception):
    # thong_bao: "Chưa hoàn thành môn tiên quyết: <ten_mon>"

class LoiXungDotLichHoc(Exception):
    # thong_bao: "Xung đột lịch với lớp: <ma_lop_hp>"

class LoiLopHocDayCho(Exception):
    # thong_bao: "Lớp <ma_lop_hp> đã đủ sĩ số tối đa"
```

**Ví dụ bắt ngoại lệ (P2 dùng khi gọi đăng ký):**
```python
try:
    kiem_tra_tien_quyet(sv, mon)
    kiem_tra_xung_dot_lich(sv, lop_hp)
    kiem_tra_si_so(lop_hp)
    sv.dang_ky(lop_hp)
except (LoiChuaDuDieuKienTienQuyet, LoiXungDotLichHoc, LoiLopHocDayCho) as e:
    hien_thi_popup_loi(str(e))   # gọi hàm P4 để hiển thị popup
```

---

## Module: `logic/file_handler.py` — **P5**

### Hàm `luu(he_thong: dict, duong_dan: str = "data/data.json") -> None`
- Ghi trạng thái toàn bộ hệ thống ra file JSON

### Hàm `tai(duong_dan: str = "data/data.json") -> dict`
- Đọc JSON, tái tạo các đối tượng `MonHoc`, `LopHocPhan`, `SinhVien`
- Trả về `dict` có 3 khóa: `"mon_hoc"`, `"lop_hoc_phan"`, `"sinh_vien"`

### Hàm `xuat_phieu_dang_ky(sv: SinhVien, dinh_dang: str = "pdf") -> str`
- `dinh_dang`: `"pdf"` hoặc `"txt"`
- Trả về đường dẫn file vừa tạo

**Ví dụ sử dụng:**
```python
luu(he_thong)                          # lưu
du_lieu = tai()                        # tải
duong_dan = xuat_phieu_dang_ky(sv, "pdf")   # xuất phiếu → "output/phieu_SV001.pdf"
```

---

## Giao diện: `gui/ui_constants.py` — **P1 (dùng chung)**

```python
# Màu sắc
MAU_CHINH        = "#2563EB"   # xanh dương chủ đạo
MAU_PHU          = "#64748B"   # xám
MAU_THANH_CONG   = "#16A34A"   # xanh lá (còn chỗ)
MAU_LOI          = "#DC2626"   # đỏ (đầy / lỗi)
MAU_NEN          = "#F8FAFC"   # nền trắng nhạt

# Phông chữ
FONT_TIEU_DE  = ("Arial", 16, "bold")
FONT_THAN     = ("Arial", 12)
FONT_NHO      = ("Arial", 10)

# Kích thước
RONG_NUT      = 120
CAO_NUT       = 35
KHOANG_CACH   = 10
```

---

## Luồng đăng ký tổng thể

```
Giao diện (P2: nút "Đăng ký")
    → kiem_tra_tien_quyet(sv, mon)      [P4]
    → kiem_tra_xung_dot_lich(sv, lop)   [P4]
    → kiem_tra_si_so(lop)               [P4]
    → sv.dang_ky(lop)                   [P2]
        → lop.them_sv(sv)               [P1]
            → TapHopBam / DanhSachLienKetDoi   [P3]
    → luu(he_thong)                     [P5]
    
Nếu có ngoại lệ → hien_thi_popup_loi()  [P4]
```

---

## Ghi chú & Quy ước chung

- **Mã hóa:** UTF-8 cho tất cả file
- **Import cấu trúc dữ liệu:** `from data_structures.doubly_linked_list import DanhSachLienKetDoi`
- **Import ngoại lệ:** `from logic.kiem_tra import LoiChuaDuDieuKienTienQuyet, LoiXungDotLichHoc, LoiLopHocDayCho`
- **Dữ liệu mẫu:** Xem `data/data_mau.py` (P2 cung cấp) để lấy dữ liệu mẫu kiểm thử
- **Hạn nội bộ ngày 13:** Tất cả nộp bản nháp giao diện cho P1 để ghép