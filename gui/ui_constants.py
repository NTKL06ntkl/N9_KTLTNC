# ============================================================
# Module: gui/ui_constants.py  -- P1 (dung chung cho toan nhom)
# Chua cac hang so ve mau sac va phong chu, dung trong toan bo
# giao dien PyQt6, de moi man hinh deu co phong cach giong nhau.
# ============================================================

# ----- MAU SAC (dang chuoi hex, dung trong stylesheet CSS cua Qt) -----
MAU_CHINH = "#2563EB"        # xanh duong chu dao (nut chinh, tieu de)
MAU_PHU = "#64748B"          # xam (nut phu, chu mo ta)
MAU_THANH_CONG = "#16A34A"   # xanh la (con cho / thanh cong)
MAU_LOI = "#DC2626"          # do (day / loi)
MAU_NEN = "#F8FAFC"          # nen trang nhat
MAU_CHU_TRANG = "#FFFFFF"

# ----- TEN FONT VA KICH THUOC CHU -----
TEN_FONT = "Arial"
CO_CHU_TIEU_DE = 16
CO_CHU_THAN = 12
CO_CHU_NHO = 10

# ----- STYLESHEET (CSS) CHO CAC LOAI NUT, DE GAN BANG setStyleSheet() -----
STYLE_NUT_CHINH = (
    "QPushButton { background-color: " + MAU_CHINH + "; color: white; "
    "font-size: " + str(CO_CHU_THAN) + "px; padding: 8px; border-radius: 5px; }"
    "QPushButton:hover { background-color: #1D4ED8; }"
)

STYLE_NUT_THANH_CONG = (
    "QPushButton { background-color: " + MAU_THANH_CONG + "; color: white; "
    "font-size: " + str(CO_CHU_THAN) + "px; padding: 8px; border-radius: 5px; }"
    "QPushButton:hover { background-color: #15803D; }"
)

STYLE_NUT_LOI = (
    "QPushButton { background-color: " + MAU_LOI + "; color: white; "
    "font-size: " + str(CO_CHU_THAN) + "px; padding: 8px; border-radius: 5px; }"
    "QPushButton:hover { background-color: #B91C1C; }"
)

STYLE_NUT_PHU = (
    "QPushButton { background-color: " + MAU_PHU + "; color: white; "
    "font-size: " + str(CO_CHU_THAN) + "px; padding: 8px; border-radius: 5px; }"
    "QPushButton:hover { background-color: #475569; }"
)

STYLE_TIEU_DE = (
    "font-size: " + str(CO_CHU_TIEU_DE) + "px; font-weight: bold; color: " + MAU_CHINH + ";"
)

STYLE_NEN_TRANG = "background-color: " + MAU_NEN + ";"

STYLE_THANH_THONG_TIN = (
    "background-color: " + MAU_CHINH + "; color: white; "
    "font-size: " + str(CO_CHU_THAN) + "px; padding: 10px;"
)
