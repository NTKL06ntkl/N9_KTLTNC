# ============================================================
# Module: logic/file_handler.py  -- P5
# Phu trach luu va doc du lieu he thong ra file JSON,
# va xuat phieu dang ky ra file .txt / .pdf cho sinh vien.
#
# QUAN TRONG: module nay KHONG sua doi gi trong cac lop
# MonHoc, LopHocPhan, SinhVien ca. No chi IMPORT cac lop do
# va TU DOC thuoc tinh co san (vi du mon.ma_mon, sv.ho_ten...)
# de gom thanh dict, roi ghi ra file JSON.
#
# Xem chi tiet trong file INTERFACE.md, muc "logic/file_handler.py"
# ============================================================

import json
import os
from datetime import datetime

from logic.mon_hoc import MonHoc
from logic.lop_hoc_phan import LopHocPhan
from logic.sinh_vien import SinhVien


# ------------------------------------------------------------
# CAC HAM RIENG, CHUYEN 1 OBJECT THANH DICT (P5 tu viet,
# KHONG nam trong class MonHoc / LopHocPhan / SinhVien)
# ------------------------------------------------------------

def _mon_hoc_thanh_dict(mon):
    """Doc thuoc tinh cua object MonHoc va gom thanh dict."""
    return {
        "ma_mon": mon.ma_mon,
        "ten_mon": mon.ten_mon,
        "so_tin_chi": mon.so_tin_chi,
        "ma_mon_tien_quyet": mon.ma_mon_tien_quyet,
    }


def _dict_thanh_mon_hoc(d):
    """Tao lai object MonHoc tu mot dict da doc duoc trong file JSON."""
    return MonHoc(
        ma_mon=d["ma_mon"],
        ten_mon=d["ten_mon"],
        so_tin_chi=d["so_tin_chi"],
        ma_mon_tien_quyet=d["ma_mon_tien_quyet"],
    )


def _lop_hoc_phan_thanh_dict(lop_hp):
    """Doc thuoc tinh cua object LopHocPhan va gom thanh dict."""
    # Lay danh sach ma sinh vien da dang ky lop nay (de luu lai quan he)
    danh_sach_ma_sv = []
    for sv in lop_hp.danh_sach_sv.duyet():
        danh_sach_ma_sv.append(sv.ma_sv)

    return {
        "ma_lop_hp": lop_hp.ma_lop_hp,
        "ma_mon": lop_hp.mon_hoc.ma_mon,     # chi luu MA mon, khong luu nguyen object
        "giang_vien": lop_hp.giang_vien,
        "si_so_toi_da": lop_hp.si_so_toi_da,
        "lich_hoc": lop_hp.lich_hoc,
        "dang_mo": lop_hp.dang_mo,
        "ds_ma_sv": danh_sach_ma_sv,
    }


def _dict_thanh_lop_hoc_phan(d, mon_hoc_tuong_ung):
    """
    Tao lai object LopHocPhan tu dict.
    Tham so mon_hoc_tuong_ung la object MonHoc da duoc tao truoc do
    (vi LopHocPhan can mot object MonHoc thuc su, khong phai chi ma mon).
    """
    lop_hp = LopHocPhan(
        ma_lop_hp=d["ma_lop_hp"],
        mon_hoc=mon_hoc_tuong_ung,
        giang_vien=d["giang_vien"],
        si_so_toi_da=d["si_so_toi_da"],
        lich_hoc=d["lich_hoc"],
    )
    lop_hp.dang_mo = d["dang_mo"]
    return lop_hp


def _sinh_vien_thanh_dict(sv):
    """Doc thuoc tinh cua object SinhVien va gom thanh dict."""
    # Lay danh sach ma lop hoc phan dang dang ky
    danh_sach_ma_lop = []
    for lop_hp in sv.ds_mon_dang_ky.duyet():
        danh_sach_ma_lop.append(lop_hp.ma_lop_hp)

    return {
        "ma_sv": sv.ma_sv,
        "ho_ten": sv.ho_ten,
        "lop_sh": sv.lop_sh,
        "diem_cac_mon": sv.diem_cac_mon,     # dict {ma_mon: diem}
        "ds_ma_lop_dang_ky": danh_sach_ma_lop,
    }


def _dict_thanh_sinh_vien(d):
    """Tao lai object SinhVien tu dict (chua khoi phuc dang ky lop)."""
    sv = SinhVien(
        ma_sv=d["ma_sv"],
        ho_ten=d["ho_ten"],
        lop_sh=d["lop_sh"],
    )
    # Khoi phuc lai cac mon da hoc va diem so
    for ma_mon in d["diem_cac_mon"]:
        diem = d["diem_cac_mon"][ma_mon]
        sv.them_mon_da_hoc(ma_mon, diem)
    return sv


# ------------------------------------------------------------
# HAM CHINH: LUU VA TAI (theo dung ten trong INTERFACE.md)
# ------------------------------------------------------------

def luu(he_thong, duong_dan="data/data.json"):
    """
    Ghi trang thai toan bo he thong ra file JSON.

    Tham so he_thong la mot dict co 3 khoa:
        "mon_hoc"      : list cac object MonHoc
        "lop_hoc_phan" : list cac object LopHocPhan
        "sinh_vien"    : list cac object SinhVien
    """
    # Tao thu muc chua file neu chua ton tai
    thu_muc = os.path.dirname(duong_dan)
    if thu_muc and not os.path.exists(thu_muc):
        os.makedirs(thu_muc)

    # Chuyen tat ca object thanh dict don gian de ghi JSON
    danh_sach_mon_dict = []
    for mon in he_thong["mon_hoc"]:
        danh_sach_mon_dict.append(_mon_hoc_thanh_dict(mon))

    danh_sach_lop_dict = []
    for lop_hp in he_thong["lop_hoc_phan"]:
        danh_sach_lop_dict.append(_lop_hoc_phan_thanh_dict(lop_hp))

    danh_sach_sv_dict = []
    for sv in he_thong["sinh_vien"]:
        danh_sach_sv_dict.append(_sinh_vien_thanh_dict(sv))

    noi_dung_luu = {
        "mon_hoc": danh_sach_mon_dict,
        "lop_hoc_phan": danh_sach_lop_dict,
        "sinh_vien": danh_sach_sv_dict,
    }

    with open(duong_dan, "w", encoding="utf-8") as file_json:
        json.dump(noi_dung_luu, file_json, ensure_ascii=False, indent=2)


def tai(duong_dan="data/data.json"):
    """
    Doc file JSON va tao lai cac object MonHoc, LopHocPhan, SinhVien.
    Tra ve dict co 3 khoa: "mon_hoc", "lop_hoc_phan", "sinh_vien".
    Neu file chua ton tai, tra ve dict voi 3 list rong.
    """
    if not os.path.exists(duong_dan):
        return {"mon_hoc": [], "lop_hoc_phan": [], "sinh_vien": []}

    with open(duong_dan, "r", encoding="utf-8") as file_json:
        du_lieu_doc = json.load(file_json)

    # ----- Tai lai danh sach mon hoc -----
    danh_sach_mon_hoc = []
    tu_dien_mon_theo_ma = {}   # de tra cuu nhanh MonHoc theo ma_mon khi tao LopHocPhan
    for d_mon in du_lieu_doc["mon_hoc"]:
        mon = _dict_thanh_mon_hoc(d_mon)
        danh_sach_mon_hoc.append(mon)
        tu_dien_mon_theo_ma[mon.ma_mon] = mon

    # ----- Tai lai danh sach sinh vien -----
    danh_sach_sinh_vien = []
    tu_dien_sv_theo_ma = {}    # de tra cuu nhanh SinhVien theo ma_sv khi khoi phuc dang ky
    for d_sv in du_lieu_doc["sinh_vien"]:
        sv = _dict_thanh_sinh_vien(d_sv)
        danh_sach_sinh_vien.append(sv)
        tu_dien_sv_theo_ma[sv.ma_sv] = sv

    # ----- Tai lai danh sach lop hoc phan -----
    danh_sach_lop_hoc_phan = []
    for d_lop in du_lieu_doc["lop_hoc_phan"]:
        mon_tuong_ung = tu_dien_mon_theo_ma.get(d_lop["ma_mon"])
        if mon_tuong_ung is None:
            continue   # bo qua neu khong tim thay mon hoc tuong ung

        lop_hp = _dict_thanh_lop_hoc_phan(d_lop, mon_tuong_ung)
        danh_sach_lop_hoc_phan.append(lop_hp)

        # Khoi phuc lai quan he dang ky 2 chieu giua sinh vien va lop hoc phan
        for ma_sv in d_lop["ds_ma_sv"]:
            sv_tuong_ung = tu_dien_sv_theo_ma.get(ma_sv)
            if sv_tuong_ung is not None:
                # Them truc tiep vao danh sach lien ket, khong goi dang_ky()
                # vi dang_ky() se goi lai them_sv() gay trung lap
                lop_hp.danh_sach_sv.them_cuoi(sv_tuong_ung)
                sv_tuong_ung.ds_mon_dang_ky.them_cuoi(lop_hp)

    return {
        "mon_hoc": danh_sach_mon_hoc,
        "lop_hoc_phan": danh_sach_lop_hoc_phan,
        "sinh_vien": danh_sach_sinh_vien,
    }


# ------------------------------------------------------------
# XUAT PHIEU DANG KY RA FILE (.txt hoac .pdf)
# ------------------------------------------------------------

def _tao_noi_dung_phieu(sv):
    """
    Ham phu: tao noi dung van ban cua phieu dang ky tin chi
    cho sinh vien sv, dua tren sv.ds_mon_dang_ky.
    """
    dong_chu = []
    dong_chu.append("=" * 56)
    dong_chu.append("PHIEU DANG KY TIN CHI".center(56))
    dong_chu.append("=" * 56)
    dong_chu.append("Ma SV   : " + sv.ma_sv)
    dong_chu.append("Ho ten  : " + sv.ho_ten)
    dong_chu.append("Lop SH  : " + sv.lop_sh)
    dong_chu.append("Ngay in : " + datetime.now().strftime("%d/%m/%Y %H:%M"))
    dong_chu.append("-" * 56)

    danh_sach_lop_dang_ky = sv.ds_mon_dang_ky.duyet()
    tong_tin_chi = 0

    for lop_hp in danh_sach_lop_dang_ky:
        so_tin_chi = lop_hp.mon_hoc.so_tin_chi
        tong_tin_chi = tong_tin_chi + so_tin_chi

        dong = (lop_hp.ma_lop_hp + " | " + lop_hp.mon_hoc.ten_mon
                + " | " + str(so_tin_chi) + " TC"
                + " | Thu " + str(lop_hp.lich_hoc["thu"])
                + " tiet " + str(lop_hp.lich_hoc["tiet_bat_dau"])
                + "-" + str(lop_hp.lich_hoc["tiet_ket_thuc"]))
        dong_chu.append(dong)

    dong_chu.append("-" * 56)
    dong_chu.append("Tong so tin chi da dang ky: " + str(tong_tin_chi))
    dong_chu.append("=" * 56)

    return "\n".join(dong_chu)


def xuat_phieu_dang_ky(sv, dinh_dang="pdf"):
    """
    Xuat phieu dang ky cho sinh vien sv ra file.
    Tham so dinh_dang: "pdf" hoac "txt".
    Tra ve duong dan file vua tao, vi du "output/phieu_SV001.pdf".

    Neu chon "pdf" nhung may chua cai thu vien reportlab,
    ham se tu dong xuat ra file .txt thay the va bao trong duong dan tra ve.
    """
    # Dam bao thu muc output ton tai
    if not os.path.exists("output"):
        os.makedirs("output")

    noi_dung = _tao_noi_dung_phieu(sv)

    if dinh_dang == "txt":
        duong_dan = "output/phieu_" + sv.ma_sv + ".txt"
        with open(duong_dan, "w", encoding="utf-8") as file_txt:
            file_txt.write(noi_dung)
        return duong_dan

    # dinh_dang == "pdf"
    duong_dan_pdf = "output/phieu_" + sv.ma_sv + ".pdf"
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas

        c = canvas.Canvas(duong_dan_pdf, pagesize=A4)
        chieu_rong, chieu_cao = A4

        c.setFont("Helvetica", 11)
        vi_tri_y = chieu_cao - 50

        # Ghi tung dong noi dung vao file PDF
        for dong in noi_dung.split("\n"):
            c.drawString(50, vi_tri_y, dong)
            vi_tri_y = vi_tri_y - 14
            if vi_tri_y < 50:
                c.showPage()
                c.setFont("Helvetica", 11)
                vi_tri_y = chieu_cao - 50

        c.save()
        return duong_dan_pdf

    except ImportError:
        # Chua cai reportlab -> xuat tam ra .txt thay the
        duong_dan_txt = "output/phieu_" + sv.ma_sv + ".txt"
        with open(duong_dan_txt, "w", encoding="utf-8") as file_txt:
            file_txt.write(noi_dung)
        return duong_dan_txt
