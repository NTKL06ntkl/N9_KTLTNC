# ============================================================
# Module: gui/ui_constants.py  -- P1
# Giao diện sáng thanh lịch - Đã đồng bộ F-String hoàn toàn
# ============================================================

# ── Hệ màu sắc đồng bộ (Màu bạn đã chọn) ──────────────────────
MAU_NEN_CHINH   = "#F8FAFC"   # Trắng xám nhẹ (Slate 50)
MAU_NEN_CARD    = "#FFFFFF"   # Khung nội dung màu trắng tinh
MAU_NEN_INPUT   = "#F1F5F9"   # Ô nhập liệu xám nhạt
MAU_NEN_INPUT_FOCUS = "#E2E8F0" 
MAU_VIEN        = "#CBD5E1"   # Viền xám nhạt thanh lịch
MAU_CHINH       = "#3B82F6"   # Xanh dương làm điểm nhấn nổi bật trên nền trắng
MAU_CHINH_HOVER = "#2563EB"   
MAU_CHINH_PRESS = "#1D4ED8"   

MAU_THANH_CONG  = "#10B981"   
MAU_LOI         = "#EF4444"   
MAU_CANH_BAO    = "#F59E0B"   
MAU_PHU         = "#64748B"   

MAU_CHU_CHINH   = "#0F172A"   # CHỮ ĐEN XÁM ĐẬM
MAU_CHU_MO      = "#64748B"   # Chữ phụ mờ
MAU_HANG_CHAN   = "#F1F5F9"   # Dòng chẵn bảng xen kẽ xám nhạt

# ── Cấu hình Font ───────────────────────────────────────────
TEN_FONT     = "Segoe UI"
CO_TIEU_DE   = 18
CO_THAN      = 13
CO_NHO       = 11

# ── Stylesheet toàn cục (Đã thay f-string để nhận màu mới) ──
GLOBAL_STYLE = f"""
QMainWindow, QWidget {{
    background-color: {MAU_NEN_CHINH};
    color: {MAU_CHU_CHINH};
    font-family: "{TEN_FONT}";
    font-size: {CO_THAN}px;
}}

/* ── Tab ── */
QTabWidget::pane {{
    border: 1px solid {MAU_VIEN};
    border-radius: 8px;
    background-color: {MAU_NEN_CARD};
}}
QTabBar::tab {{
    background: {MAU_NEN_CHINH};
    color: {MAU_CHU_MO};
    padding: 10px 22px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    margin-right: 3px;
    font-weight: 600;
}}
QTabBar::tab:selected {{
    background: {MAU_NEN_CARD};
    color: {MAU_CHINH};
    border-top: 2px solid {MAU_CHINH};
}}
QTabBar::tab:hover:!selected {{ background: {MAU_NEN_CARD}; color: {MAU_CHU_CHINH}; }}

/* ── Bảng ── */
QTableWidget {{
    background-color: {MAU_NEN_CARD};
    alternate-background-color: {MAU_HANG_CHAN};
    border: 1px solid {MAU_VIEN};
    border-radius: 8px;
    gridline-color: {MAU_VIEN};
    outline: none;
    color: {MAU_CHU_CHINH};
}}
QTableWidget::item {{
    padding: 8px 12px;
    border: none;
}}
QTableWidget::item:selected {{
    background-color: #E0F2FE;
    color: {MAU_CHINH};
}}
QHeaderView::section {{
    background-color: {MAU_NEN_CHINH};
    color: {MAU_CHU_MO};
    font-weight: 700;
    font-size: {CO_NHO}px;
    text-transform: uppercase;
    letter-spacing: 1px;
    padding: 10px 12px;
    border: none;
    border-bottom: 2px solid {MAU_CHINH};
}}

/* ── Input ── */
QLineEdit, QComboBox {{
    background-color: {MAU_NEN_INPUT};
    border: 1px solid {MAU_VIEN};
    border-radius: 6px;
    padding: 7px 12px;
    color: {MAU_CHU_CHINH};
    selection-background-color: {MAU_CHINH};
}}
QLineEdit:focus, QComboBox:focus {{
    border: 1px solid {MAU_CHINH};
    background-color: {MAU_NEN_INPUT_FOCUS};
}}
QComboBox::drop-down {{ border: none; width: 20px; }}
QComboBox QAbstractItemView {{
    background-color: {MAU_NEN_CARD};
    border: 1px solid {MAU_VIEN};
    selection-background-color: {MAU_CHINH};
    color: {MAU_CHU_CHINH};
    padding: 4px;
}}

/* ── GroupBox ── */
QGroupBox {{
    border: 1px solid {MAU_VIEN};
    border-radius: 8px;
    margin-top: 16px;
    padding: 16px 12px 12px 12px;
    color: {MAU_CHU_MO};
    font-weight: 600;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    left: 14px;
    padding: 0 6px;
    color: {MAU_CHINH};
    font-size: 12px;
}}

/* ── ScrollBar ── */
QScrollBar:vertical {{
    background: {MAU_NEN_INPUT}; width: 6px; border-radius: 3px;
}}
QScrollBar::handle:vertical {{
    background: {MAU_VIEN}; border-radius: 3px; min-height: 30px;
}}
QScrollBar:horizontal {{
    background: {MAU_NEN_INPUT}; height: 6px; border-radius: 3px;
}}
QScrollBar::handle:horizontal {{
    background: {MAU_VIEN}; border-radius: 3px;
}}
QScrollBar::add-line, QScrollBar::sub-line {{ height:0; width:0; }}

/* ── Message Box ── */
QMessageBox {{ background-color: {MAU_NEN_CARD}; }}
QMessageBox QLabel {{ color: {MAU_CHU_CHINH}; font-size: {CO_THAN}px; }}
QMessageBox QPushButton {{
    background-color: {MAU_CHINH}; color: white;
    border-radius: 6px; padding: 6px 20px; min-width: 80px;
}}
QMessageBox QPushButton:hover {{ background-color: {MAU_CHINH_HOVER}; }}
"""

# ── Stylesheet cho từng loại nút ────────────────────────────
STYLE_NUT_CHINH = f"""
QPushButton {{
    background-color: {MAU_CHINH}; color: white; font-weight: 700;
    border: none; border-radius: 8px; padding: 10px 20px; font-size: {CO_THAN}px;
}}
QPushButton:hover {{ background-color: {MAU_CHINH_HOVER}; }}
QPushButton:pressed {{ background-color: {MAU_CHINH_PRESS}; }}
"""

STYLE_NUT_THANH_CONG = f"""
QPushButton {{
    background-color: {MAU_THANH_CONG}; color: white; font-weight: 700;
    border: none; border-radius: 8px; padding: 10px 20px; font-size: {CO_THAN}px;
}}
QPushButton:hover {{ background-color: #059669; }}
QPushButton:pressed {{ background-color: #047857; }}
"""

STYLE_NUT_LOI = f"""
QPushButton {{
    background-color: {MAU_LOI}; color: white; font-weight: 700;
    border: none; border-radius: 8px; padding: 10px 20px; font-size: {CO_THAN}px;
}}
QPushButton:hover {{ background-color: #DC2626; }}
QPushButton:pressed {{ background-color: #B91C1C; }}
"""

STYLE_NUT_PHU = f"""
QPushButton {{
    background-color: {MAU_PHU}; color: white; font-weight: 700;
    border: none; border-radius: 8px; padding: 10px 20px; font-size: {CO_THAN}px;
}}
QPushButton:hover {{ background-color: #4B5563; }}
QPushButton:pressed {{ background-color: #374151; }}
"""

STYLE_NUT_OUTLINE = f"""
QPushButton {{
    background-color: transparent; color: {MAU_CHINH}; font-weight: 700;
    border: 2px solid {MAU_CHINH}; border-radius: 8px; padding: 8px 20px; font-size: {CO_THAN}px;
}}
QPushButton:hover {{ background-color: #E0F2FE; }}
"""

STYLE_TIEU_DE = (
    f"font-size: {CO_TIEU_DE}px; font-weight: 800; color: {MAU_CHU_CHINH}; letter-spacing: 1px;"
)

STYLE_NEN_TRANG = f"background-color: {MAU_NEN_CHINH};"

STYLE_THANH_THONG_TIN = f"""
    background-color: {MAU_NEN_INPUT};
    color: {MAU_CHINH};
    font-size: {CO_THAN}px;
    font-weight: 600;
    padding: 12px 20px;
    border-bottom: 1px solid {MAU_VIEN};
"""

# Giữ lại để tránh lỗi tương thích ngược với file screen_sinh_vien.py
CO_CHU_THAN = CO_THAN
CO_CHU_NHO  = CO_NHO