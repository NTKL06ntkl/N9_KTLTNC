# ============================================================
# Module: gui/ui_constants.py  -- P1
# Theme tối hiện đại
# ============================================================

# Màu sắc
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

# Font
TEN_FONT     = "Segoe UI"
CO_TIEU_DE   = 18
CO_THAN      = 13
CO_NHO       = 11

# ── Stylesheet toàn cục ──────────────────────────────────────
GLOBAL_STYLE = """
QMainWindow, QWidget {
    background-color: #0F172A;
    color: #F1F5F9;
    font-family: "Segoe UI";
    font-size: 13px;
}

/* ── Tab ── */
QTabWidget::pane {
    border: 1px solid #334155;
    border-radius: 8px;
    background-color: #1E293B;
}
QTabBar::tab {
    background: #0F172A;
    color: #94A3B8;
    padding: 10px 22px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    margin-right: 3px;
    font-weight: 600;
}
QTabBar::tab:selected {
    background: #1E293B;
    color: #3B82F6;
    border-top: 2px solid #3B82F6;
}
QTabBar::tab:hover:!selected { background: #1E293B; color: #F1F5F9; }

/* ── Bảng ── */
QTableWidget {
    background-color: #1E293B;
    alternate-background-color: #1A2744;
    border: 1px solid #334155;
    border-radius: 8px;
    gridline-color: #2D3F55;
    outline: none;
    color: #F1F5F9;
}
QTableWidget::item {
    padding: 8px 12px;
    border: none;
}
QTableWidget::item:selected {
    background-color: #1E3A5F;
    color: #93C5FD;
}
QHeaderView::section {
    background-color: #0F172A;
    color: #94A3B8;
    font-weight: 700;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1px;
    padding: 10px 12px;
    border: none;
    border-bottom: 2px solid #3B82F6;
}

/* ── Input ── */
QLineEdit, QComboBox {
    background-color: #334155;
    border: 1px solid #475569;
    border-radius: 6px;
    padding: 7px 12px;
    color: #F1F5F9;
    selection-background-color: #3B82F6;
}
QLineEdit:focus, QComboBox:focus {
    border: 1px solid #3B82F6;
    background-color: #3D4F65;
}
QComboBox::drop-down { border: none; width: 20px; }
QComboBox QAbstractItemView {
    background-color: #1E293B;
    border: 1px solid #334155;
    selection-background-color: #3B82F6;
    color: #F1F5F9;
    padding: 4px;
}

/* ── GroupBox ── */
QGroupBox {
    border: 1px solid #334155;
    border-radius: 8px;
    margin-top: 16px;
    padding: 16px 12px 12px 12px;
    color: #94A3B8;
    font-weight: 600;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 14px;
    padding: 0 6px;
    color: #3B82F6;
    font-size: 12px;
}

/* ── ScrollBar ── */
QScrollBar:vertical {
    background: #1E293B; width: 6px; border-radius: 3px;
}
QScrollBar::handle:vertical {
    background: #475569; border-radius: 3px; min-height: 30px;
}
QScrollBar:horizontal {
    background: #1E293B; height: 6px; border-radius: 3px;
}
QScrollBar::handle:horizontal {
    background: #475569; border-radius: 3px;
}
QScrollBar::add-line, QScrollBar::sub-line { height:0; width:0; }

/* ── Message Box ── */
QMessageBox { background-color: #1E293B; }
QMessageBox QLabel { color: #F1F5F9; font-size: 13px; }
QMessageBox QPushButton {
    background-color: #3B82F6; color: white;
    border-radius: 6px; padding: 6px 20px; min-width: 80px;
}
QMessageBox QPushButton:hover { background-color: #2563EB; }
"""

# ── Stylesheet cho từng loại nút ────────────────────────────
STYLE_NUT_CHINH = """
QPushButton {
    background-color: #3B82F6; color: white; font-weight: 700;
    border: none; border-radius: 8px; padding: 10px 20px; font-size: 13px;
}
QPushButton:hover { background-color: #2563EB; }
QPushButton:pressed { background-color: #1D4ED8; }
"""

STYLE_NUT_THANH_CONG = """
QPushButton {
    background-color: #10B981; color: white; font-weight: 700;
    border: none; border-radius: 8px; padding: 10px 20px; font-size: 13px;
}
QPushButton:hover { background-color: #059669; }
QPushButton:pressed { background-color: #047857; }
"""

STYLE_NUT_LOI = """
QPushButton {
    background-color: #EF4444; color: white; font-weight: 700;
    border: none; border-radius: 8px; padding: 10px 20px; font-size: 13px;
}
QPushButton:hover { background-color: #DC2626; }
QPushButton:pressed { background-color: #B91C1C; }
"""

STYLE_NUT_PHU = """
QPushButton {
    background-color: #475569; color: white; font-weight: 700;
    border: none; border-radius: 8px; padding: 10px 20px; font-size: 13px;
}
QPushButton:hover { background-color: #64748B; }
QPushButton:pressed { background-color: #334155; }
"""

STYLE_NUT_OUTLINE = """
QPushButton {
    background-color: transparent; color: #3B82F6; font-weight: 700;
    border: 2px solid #3B82F6; border-radius: 8px; padding: 8px 20px; font-size: 13px;
}
QPushButton:hover { background-color: #1E3A5F; }
"""

STYLE_TIEU_DE = (
    "font-size: 18px; font-weight: 800; color: #F1F5F9; letter-spacing: 1px;"
)

STYLE_NEN_TRANG = "background-color: #0F172A;"

STYLE_THANH_THONG_TIN = """
    background-color: #1E293B;
    color: #93C5FD;
    font-size: 13px;
    font-weight: 600;
    padding: 12px 20px;
    border-bottom: 1px solid #334155;
"""

CO_CHU_THAN = 13
CO_CHU_NHO  = 11

