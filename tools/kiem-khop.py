"""KIỂM KHỚP JS ↔ Python: chạy cùng bộ ví dụ qua máy tính Python của P4 (apps/finance) và qua lõi JS nằm trong
app/daovang.html (bằng node). Tiền lệch > 1 đ = HỎNG; tỷ lệ lệch > 0,0001 = HỎNG; chữ (cảnh báo, tên khoản, nguồn)
phải giống hệt (biên ròng / ROAS: cho phép mức lệch tương ứng 1 đ lợi nhuận); ví dụ Python báo lỗi thì JS cũng phải báo lỗi cùng nội dung.

Bộ ví dụ:
  1. 3 ví dụ kiểm ngược của P4 (taichinh.kiem_nguoc.VI_DU) × (mức giữa, mức cao) × (có hoàn, không hoàn)
  2. ví dụ tự sinh ngẫu nhiên có hạt giống cố định (mọi ngành, cả hai sàn, mọi cờ, cả ví dụ nhập sai)
  3. ví dụ tự sinh cho dropship, affiliate, vốn ứng trước, sổ lãi lỗ (Đợt 1 của P4)
  4. apps/finance/vi-du-kiem-khop.json của P4 (18 ví dụ, 6 loại) — chạy ĐỦ mọi mục; "mong_doi" so với Python theo
     dung sai ghi trong tệp. Loại ví dụ lạ → KHÔNG CHẠY ĐƯỢC (không lặng lẽ bỏ qua).

Chạy (gốc repo):  python3 tools/kiem-khop.py            (cần node ≥ 18)
                  python3 tools/kiem-khop.py --so-ngau-nhien 1000 --chi-tiet
Mã thoát: 0 = ĐẠT, 1 = HỎNG, 2 = không chạy được (thiếu node / tệp).
"""
from __future__ import annotations

import argparse
import json
import math
import random
import shutil
import subprocess
import sys
import inspect
from dataclasses import fields
from datetime import date
from pathlib import Path

GOC = Path(__file__).resolve().parents[1]
APP = GOC / "app" / "daovang.html"
CHAY_JS = GOC / "tools" / "kiem-khop-chay.js"
VI_DU_P4 = GOC / "apps" / "finance" / "vi-du-kiem-khop.json"

sys.path.insert(0, str(GOC / "apps" / "finance"))
from taichinh import BangPhi, DauVao, MayTinh, ThieuDuLieu  # noqa: E402
from taichinh import kiem_nguoc  # noqa: E402
from taichinh import affiliate as aff  # noqa: E402
from taichinh.dropship import tinh_dropship, von_ung_truoc  # noqa: E402
from taichinh.so_lai_lo import kiem_cong_dot1, kiem_dong  # noqa: E402

LECH_TIEN = 1.0      # đ
LECH_TY_LE = 1e-4    # cho biên ròng, ROAS, tỷ lệ %
TRUONG_TIEN = ("rev", "cm", "chi_phi_moi_don_hoan", "ln_truoc_qc", "quang_cao", "ln", "gia_hoa_von",
               "gia_hoa_von_truoc_qc", "thue_tam_khau_tru")
TRUONG_TY_LE = ("bien_rong", "roas_hoa_von")
TRUONG_TY_LE_PHI = ("ty_le_phi_san_aff_chua_thue", "ty_le_phi_gom_thue_khau_tru")
TRUONG_CHU = ("san", "nganh", "ngay_ban", "khong_dam_bao")
AFF_TIEN = ("hoa_hong_ky_vong_moi_don", "quang_cao", "ln_affiliate", "von_hang_moi_don_nhap_truc_tiep",
            "von_hang_moi_don_affiliate", "chenh_lech_nhap_truc_tiep_tru_affiliate")
AFF_TY_LE = ("hoa_hong_nhan_pct", "roas_hoa_von_affiliate")

TEN_DAU_VAO = {f.name for f in fields(DauVao)}
TRUONG_SO = {"gia_ban", "gia_von", "giam_gia_shop", "dong_goi", "ship_shop_chiu", "hoa_hong_aff_shop_tra",
             "quang_cao_pct", "ty_le_hoan", "ship_tra_hang", "ty_le_hong_hang_hoan", "thue_gtgt", "thue_tncn",
             "phi_nganh_tu_nhap", "hoa_hong_aff_nhan", "thue_aff"}


# tham số của từng loại ví dụ: (tên được phép, tên số thực → float, bắt buộc)
TRUONG_DROPSHIP = {"phi_ncc", "ty_le_huy", "chi_phi_moi_don_huy", "ngay_giao", "loai_shop"}
SO_THUC_DROPSHIP = {"phi_ncc", "ty_le_huy", "chi_phi_moi_don_huy"}


def _tham_so(ham, bo=()):
    return {k for k in inspect.signature(ham).parameters if k not in bo and k != "kw"}


LOAI = {
    "affiliate": (_tham_so(aff.thuc_nhan), {"hoa_hong_goc", "chi_phi_noi_dung", "phi_nen_tang_pct", "thue_pct"},
                  {"hoa_hong_goc"}),
    "affiliate_tu_don": (_tham_so(aff.thuc_nhan_tu_don) | (_tham_so(aff.thuc_nhan) - {"hoa_hong_goc", "chi_phi_noi_dung"}),
                         {"gia_tri_don", "ty_le_hoa_hong", "ty_le_huy_hoan", "chi_phi_noi_dung", "phi_nen_tang_pct",
                          "thue_pct"}, {"gia_tri_don", "ty_le_hoa_hong"}),
    "von_ung_truoc": (_tham_so(von_ung_truoc), {"don_moi_ngay", "chi_ra_moi_don", "tien_ve_moi_don"},
                      {"don_moi_ngay", "chi_ra_moi_don", "tien_ve_moi_don", "ngay_tre"}),
    "so_lai_lo": ({"dong", "ngay_cuoi", "so_ngay"}, set(), {"dong", "ngay_cuoi"}),
}


# ---------------- bộ ví dụ ----------------
def chuan_vi_du(loai: str, d: dict) -> dict:
    """Chuẩn hóa đầu vào theo loại ví dụ. Báo lỗi nếu loại lạ / trường lạ / thiếu trường."""
    if loai == "don":
        return chuan_dau_vao(d)
    if loai == "dropship":
        ra = chuan_dau_vao({k: v for k, v in d.items() if k not in TRUONG_DROPSHIP})
        for k in TRUONG_DROPSHIP & set(d):
            v = d[k]
            ra[k] = float(v) if k in SO_THUC_DROPSHIP and v is not None else v
        return ra
    if loai not in LOAI:
        raise ValueError(f"loại ví dụ lạ '{loai}' — kiểm khớp chưa hỗ trợ (cần P9 thêm vào lõi JS)")
    duoc, so_thuc, bat_buoc = LOAI[loai]
    if set(d) - duoc:
        raise ValueError(f"{loai}: trường lạ {sorted(set(d) - duoc)}")
    if bat_buoc - set(d):
        raise ValueError(f"{loai}: thiếu {sorted(bat_buoc - set(d))}")
    return {k: (float(v) if k in so_thuc and v is not None and not isinstance(v, bool) else v) for k, v in d.items()}


def chuan_dau_vao(d: dict) -> dict:
    """Số → float (như dòng lệnh P4), ngày → chuỗi ISO. Báo lỗi nếu có trường lạ."""
    la = set(d) - TEN_DAU_VAO
    if la:
        raise ValueError(f"trường không có trong DauVao: {sorted(la)}")
    ra = {}
    for k, v in d.items():
        if k == "ngay_ban" and isinstance(v, date):
            v = v.isoformat()
        elif k in TRUONG_SO and v is not None and not isinstance(v, bool):
            v = float(v)
        ra[k] = v
    if "ngay_ban" not in ra:
        raise ValueError("ví dụ kiểm khớp phải ghi ngay_ban (không dùng 'hôm nay')")
    return ra


def vi_du_kiem_nguoc() -> list[dict]:
    ra = []
    for ten, dv, _ in kiem_nguoc.VI_DU:
        for che_do in ("giua", "cao"):
            for hoan in (True, False):
                d = dict(dv, ngay_ban=kiem_nguoc.NGAY, che_do_khoang=che_do)
                if not hoan:
                    d["ty_le_hoan"] = 0
                ra.append({"ten": f"kiểm ngược P4 · {ten} · {che_do} · {'có' if hoan else 'không'} hoàn",
                           "dau_vao": chuan_dau_vao(d)})
    return ra


NGAY_THU = ["2025-03-01", "2025-08-15", "2026-04-30", "2026-05-01", "2026-05-08", "2026-05-22", "2026-05-23",
            "2026-07-02", "2026-07-03", "2026-10-31", "2026-11-01", "2026-11-12", "2026-12-31", "2027-01-01",
            "2027-06-30"]


def vi_du_ngau_nhien(n: int, hat: int = 20261112) -> list[dict]:
    rd = random.Random(hat)
    bp = BangPhi()
    nganh = {"shopee": bp.nganh_cua("Shopee", "phi_co_dinh"),
             "tiktok": bp.nganh_cua("TikTok Shop", "phi_hoa_hong_nen_tang")}
    tien = lambda a, b, buoc=500: float(rd.randrange(a // buoc, b // buoc + 1) * buoc)  # noqa: E731
    ra = []
    for i in range(n):
        san = rd.choice(["shopee", "tiktok"])
        ten_san = {"shopee": rd.choice(["shopee", "Shopee", "SHOPEE"]),
                   "tiktok": rd.choice(["tiktok", "TikTok Shop", "tik tok"])}[san]
        gia_ban = tien(10_000, 2_000_000)
        d = {
            "san": ten_san,
            "nganh": rd.choice(nganh[san]),
            "gia_ban": gia_ban,
            "gia_von": tien(0, int(gia_ban * 1.2)),
            # 30% ngày bất kỳ (gồm ngày trước hiệu lực → đường lỗi), 70% ngày bảng phí TikTok đã hiệu lực
            "ngay_ban": rd.choice(NGAY_THU) if rd.random() < 0.3 else rd.choice(NGAY_THU[9:]),
            "giam_gia_shop": rd.choice([0.0, 0.0, tien(0, int(gia_ban * 0.3))]),
            "dong_goi": rd.choice([0.0, tien(1_000, 8_000)]),
            "ship_shop_chiu": rd.choice([0.0, 0.0, tien(5_000, 30_000)]),
            "tham_gia_voucher_san": rd.random() < 0.4,
            "hoa_hong_aff_shop_tra": rd.choice([0.0, 0.0, round(rd.uniform(1, 20), 1)]),
            "quang_cao_pct": rd.choice([0.0, round(rd.uniform(0, 30), 2)]),
            "ty_le_hoan": rd.choice([0.0, round(rd.uniform(0, 25), 1)]),
            "ship_tra_hang": rd.choice([None, None, tien(0, 50_000)]),
            "ty_le_hong_hang_hoan": rd.choice([30.0, round(rd.uniform(0, 100), 1)]),
            "thue_gtgt": rd.choice([None, None, 1.0, 0.0]),
            "thue_tncn": rd.choice([None, None, 0.5, 0.0]),
            "che_do_khoang": rd.choice(["thap", "giua", "cao"]),
            "phi_nganh_tu_nhap": rd.choice([None] * 5 + [round(rd.uniform(0, 20), 2)]),
            "shop_moi_mien_phi_co_dinh": rd.random() < 0.15,
            "tinh_phi_ha_tang": rd.random() > 0.15,
            "hoa_hong_aff_nhan": rd.choice([None, None, round(rd.uniform(1, 30), 1)]),
            "thue_aff": rd.choice([0.0, 10.0]),
        }
        # biến thể đặc biệt (đường lỗi, chuỗi ngành gõ tắt, giá rất cao / rất thấp)
        k = rd.random()
        if k < 0.04:
            d["nganh"] = rd.choice(["thoi trang", "dien tu", "nha cua", "sac dep", "xyz", "", "Me & Be"])
        elif k < 0.06:
            d["ty_le_hoan"] = rd.choice([-1.0, 120.0])
        elif k < 0.08:
            d["giam_gia_shop"] = gia_ban + rd.choice([0.0, 1000.0])
        elif k < 0.09:
            d["gia_von"] = -1000.0
        elif k < 0.11:
            d["gia_ban"] = rd.choice([1_000.0, 2_500.0, 50_000_000.0])
        elif k < 0.12:
            d["san"] = "lazada"
        if san == "tiktok" and rd.random() < 0.1:
            d["nganh"] = ""
        ra.append({"ten": f"ngẫu nhiên #{i + 1}", "dau_vao": chuan_dau_vao(d)})
    return ra


def vi_du_dot1_ngau_nhien(n: int, hat: int = 20261113) -> list[dict]:
    """Ví dụ tự sinh cho phần Đợt 1 của P4: dropship, affiliate, affiliate từ đơn, vốn ứng trước, sổ lãi lỗ."""
    rd = random.Random(hat)
    don = vi_du_ngau_nhien(n, hat)
    ra = []
    for i in range(n):
        # dropship: lấy một đơn tự sinh, thêm tham số NCC
        dv = dict(don[i]["dau_vao"])
        ds = {"phi_ncc": rd.choice([0.0, float(rd.randrange(0, 20) * 500)]),
              "ty_le_huy": rd.choice([0.0, round(rd.uniform(0, 30), 1)]),
              "ngay_giao": rd.choice([1, 3, 5]),
              "loai_shop": rd.choice(["moi", "thuong", "rui_ro", "mall"])}
        if rd.random() < 0.3:
            ds["chi_phi_moi_don_huy"] = float(rd.randrange(0, 30) * 500)
        k = rd.random()
        if k < 0.04:
            ds["ty_le_huy"] = rd.choice([100.0, -1.0])
        elif k < 0.06:
            ds["phi_ncc"] = -500.0
        elif k < 0.08:
            ds["loai_shop"] = rd.choice(["xyz", "it's"])
        ra.append({"ten": f"dropship tự sinh #{i + 1}", "loai": "dropship", "dau_vao": chuan_vi_du("dropship", {**dv, **ds})})

        # affiliate một khoản
        hh = rd.choice([float(rd.randrange(0, 2_000_000)), 250_000.0, 249_999.0, 252_470.0, 225_000.0, 0.0])
        a = {"hoa_hong_goc": hh, "chi_phi_noi_dung": rd.choice([0.0, float(rd.randrange(0, 400_000))]),
             "san": rd.choice(["shopee", "Shopee", "tiktok", "TikTok Shop"]),
             "nguong_tinh_tren": rd.choice(["truoc_phi", "sau_phi"])}
        if rd.random() < 0.3:
            a["ngay"] = rd.choice(["2025-01-01", "2025-06-01", "2025-11-20", "2026-11-12"])
        if rd.random() < 0.2:
            a["phi_nen_tang_pct"] = round(rd.uniform(0, 5), 2)
        if rd.random() < 0.2:
            a["thue_pct"] = rd.choice([0.0, 5.0, 10.0])
        if rd.random() < 0.04:
            a[rd.choice(["hoa_hong_goc", "chi_phi_noi_dung"])] = -1.0
        if rd.random() < 0.03:
            a["san"] = "lazada"
        if rd.random() < 0.03:
            a["nguong_tinh_tren"] = "khac"
        ra.append({"ten": f"affiliate tự sinh #{i + 1}", "loai": "affiliate", "dau_vao": chuan_vi_du("affiliate", a)})

        # affiliate gộp nhiều đơn một kỳ
        b = {"gia_tri_don": float(rd.randrange(10_000, 1_000_000, 1000)), "ty_le_hoa_hong": round(rd.uniform(0, 25), 1),
             "so_don": rd.randrange(0, 200), "ty_le_huy_hoan": rd.choice([0.0, round(rd.uniform(0, 40), 1)]),
             "chi_phi_noi_dung": rd.choice([0.0, float(rd.randrange(0, 500_000))]),
             "san": rd.choice(["shopee", "tiktok"])}
        if rd.random() < 0.05:
            b["ty_le_hoa_hong"] = rd.choice([101.0, -2.0])
        ra.append({"ten": f"affiliate từ đơn tự sinh #{i + 1}", "loai": "affiliate_tu_don",
                   "dau_vao": chuan_vi_du("affiliate_tu_don", b)})

        # vốn ứng trước
        v = {"don_moi_ngay": float(rd.randrange(0, 30)), "chi_ra_moi_don": float(rd.randrange(0, 300_000, 500)),
             "tien_ve_moi_don": float(rd.randrange(0, 400_000, 500)), "ngay_tre": rd.randrange(0, 20),
             "so_ngay": rd.choice([1, 14, 30, 56, 90])}
        if rd.random() < 0.04:
            v["so_ngay"] = 0
        ra.append({"ten": f"vốn ứng trước tự sinh #{i + 1}", "loai": "von_ung_truoc",
                   "dau_vao": chuan_vi_du("von_ung_truoc", v)})

        # sổ lãi lỗ: 1–12 dòng, đôi khi có dòng sai
        so = _so_ngau_nhien(rd)
        if i == 0:
            so["dong"] = []  # luôn có ca "sổ trống"
        ra.append({"ten": f"sổ lãi lỗ tự sinh #{i + 1}", "loai": "so_lai_lo", "dau_vao": chuan_vi_du("so_lai_lo", so)})
    return ra


def _so_ngau_nhien(rd: random.Random) -> dict:
    from taichinh.so_lai_lo import LOAI_CHI, LOAI_THU
    cuoi = date(2026, rd.randrange(10, 13), rd.randrange(1, 29))
    dong = []
    for _ in range(rd.randrange(0, 13)):
        tc = rd.choice(["thu", "chi", "Chi"])
        ng = date.fromordinal(cuoi.toordinal() - rd.randrange(-5, 70))
        r = {"ngay": ng.isoformat(), "thu_chi": tc,
             "loai": rd.choice(sorted(LOAI_THU if tc == "thu" else LOAI_CHI)),
             "mo_hinh": rd.choice(["affiliate", "dropship", "chung"]), "kenh": rd.choice(["shopee", "tiktok", "", "chung"]),
             "so_tien_vnd": rd.choice([str(rd.randrange(1, 9_000_000)), f"{rd.randrange(1, 9999)}.000", rd.randrange(1, 5_000_000)]),
             "mo_ta": "GIA DINH", "nguon": "GIA DINH"}
        if rd.random() < 0.25:
            a = date.fromordinal(ng.toordinal() - rd.randrange(0, 40))
            r["phan_bo_tu"], r["phan_bo_den"] = a.isoformat(), date.fromordinal(a.toordinal() + rd.randrange(0, 60)).isoformat()
        k = rd.random()
        if k < 0.02:
            r["thu_chi"] = "vay"
        elif k < 0.04:
            r["loai"] = "doanh_thu_don" if tc != "thu" else "cong_cu"
        elif k < 0.05:
            r["mo_hinh"] = "khac"
        elif k < 0.06:
            r["so_tien_vnd"] = rd.choice(["0", "-5", "abc", ""])
        elif k < 0.07:
            r["ngay"] = rd.choice(["2026-13-01", "2026/11/02", "2026-02-30"])
        elif k < 0.08:
            r.pop("phan_bo_den", None)
            r["phan_bo_tu"] = "2026-11-01"
        elif k < 0.09:
            r["kenh"] = "lazada"
        dong.append(r)
    return {"dong": dong, "ngay_cuoi": cuoi.isoformat(), "so_ngay": rd.choice([7, 28, 28, 60])}


def vi_du_p4(duong: Path = VI_DU_P4) -> list[dict]:
    """Đọc tệp ví dụ của P4. Nhận: [ {...} ] hoặc {"vi_du": [ ... ]}; mỗi mục là đầu vào DauVao, hoặc
    {"ten", "dau_vao": {...}, "mong_doi": {...}}. Dạng lạ → lỗi (không lặng lẽ bỏ qua)."""
    if not duong.exists():
        return []
    goc = json.loads(duong.read_text(encoding="utf-8"))
    ds = goc.get("vi_du") if isinstance(goc, dict) else goc
    if not isinstance(ds, list):
        raise ValueError(f"{duong.name}: cần danh sách ví dụ hoặc khóa 'vi_du'")
    ra = []
    for i, m in enumerate(ds):
        if not isinstance(m, dict):
            raise ValueError(f"{duong.name}: mục {i + 1} không phải object")
        dv = m.get("dau_vao", m if "dau_vao" not in m and "san" in m else None)
        if not isinstance(dv, dict):
            raise ValueError(f"{duong.name}: mục {i + 1} thiếu 'dau_vao'")
        loai = m.get("loai", "don")
        ten = m.get("ten") or m.get("id") or f"mục {i + 1}"
        mong = m.get("mong_doi")
        if loai == "dropship" and isinstance(mong, dict) and "don_khong_huy" in mong:
            # P4 đặt tên "don_khong_huy" cho trường `don` của KetQuaDropship (vi_du_kiem_khop.py)
            mong = {("don" if k == "don_khong_huy" else k): v for k, v in mong.items()}
        ra.append({"ten": f"P4 · {ten}", "loai": loai, "dau_vao": chuan_vi_du(loai, dv), "mong_doi": mong})
    return ra


def dung_sai_p4(duong: Path = VI_DU_P4) -> dict:
    """Dung sai P4 ghi trong tệp (cho phép so 'mong_doi'); không có thì dùng ngưỡng của P9."""
    ds = {"tien_vnd": LECH_TIEN, "ty_le": 1e-6, "roas": LECH_TY_LE, "gia_hoa_von_vnd": LECH_TIEN}
    if duong.exists():
        goc = json.loads(duong.read_text(encoding="utf-8"))
        if isinstance(goc, dict) and isinstance(goc.get("dung_sai"), dict):
            ds.update(goc["dung_sai"])
    return ds


# ---------------- chạy ----------------
def _python_mot(mt: MayTinh, loai: str, dau_vao: dict):
    d = dict(dau_vao)
    if loai == "don":
        d["ngay_ban"] = date.fromisoformat(d["ngay_ban"])
        return mt.tinh(DauVao(**d)).to_dict()
    if loai == "dropship":
        ds = {k: d.pop(k) for k in list(d) if k in TRUONG_DROPSHIP}
        d["ngay_ban"] = date.fromisoformat(d["ngay_ban"])
        return tinh_dropship(DauVao(**d), mt=mt, **ds).to_dict()
    if loai in ("affiliate", "affiliate_tu_don"):
        if d.get("ngay") is not None:
            d["ngay"] = date.fromisoformat(d["ngay"])
        return (aff.thuc_nhan if loai == "affiliate" else aff.thuc_nhan_tu_don)(**d).to_dict()
    if loai == "von_ung_truoc":
        return von_ung_truoc(**d)
    if loai == "so_lai_lo":  # cùng thứ tự như P4 (vi_du_kiem_khop.py): kiểm từng dòng → ngày cuối → cổng
        dong = [kiem_dong(r) for r in d["dong"]]
        return kiem_cong_dot1(dong, date.fromisoformat(d["ngay_cuoi"]), d.get("so_ngay", 28))
    raise ValueError(f"loại ví dụ lạ '{loai}'")


def chay_python(vi_du: list[dict]) -> list[dict]:
    mt = MayTinh(BangPhi())
    ra = []
    for v in vi_du:
        try:
            ra.append({"ok": json.loads(json.dumps(_python_mot(mt, v.get("loai", "don"), v["dau_vao"])))})
        except ThieuDuLieu as e:
            ra.append({"loi": "ThieuDuLieu", "thong_diep": str(e)})
        except ValueError as e:
            ra.append({"loi": "ValueError", "thong_diep": str(e)})
    return ra


def tim_node() -> str | None:
    return shutil.which("node") or shutil.which("node.exe")


def chay_js(vi_du: list[dict], app: Path = APP, node: str | None = None) -> list[dict]:
    node = node or tim_node()
    if not node:
        raise FileNotFoundError("không thấy node — cài Node.js (nodejs.org) rồi chạy lại")
    p = subprocess.run([node, str(CHAY_JS), str(app)], input=json.dumps(vi_du, ensure_ascii=False),
                       capture_output=True, text=True, encoding="utf-8", timeout=600)
    if p.returncode != 0:
        raise RuntimeError(f"node lỗi (mã {p.returncode}): {p.stderr.strip()[:2000]}")
    return json.loads(p.stdout)


def _lech_so(a, b, nguong) -> float | None:
    """None nếu khớp; ngược lại trả độ lệch (inf nếu một bên None)."""
    if a is None and b is None:
        return None
    if a is None or b is None:
        return math.inf
    d = abs(float(a) - float(b))
    return d if d > nguong else None


def so_sanh(py: dict, js: dict, loai: str = "don") -> tuple[list[str], float]:
    """Trả (danh sách chỗ lệch, độ lệch tiền lớn nhất)."""
    lech: list[str] = []
    lon_nhat = 0.0
    if "ok" not in py or "ok" not in js:
        if ("ok" in py) != ("ok" in js):
            lech.append(f"Python {'tính được' if 'ok' in py else 'lỗi: ' + py.get('thong_diep', '')} | "
                        f"JS {'tính được' if 'ok' in js else 'lỗi: ' + js.get('thong_diep', '')}")
        elif py["loi"] != js["loi"] or py["thong_diep"] != js["thong_diep"]:
            lech.append(f"lỗi khác nhau: Python [{py['loi']}] {py['thong_diep']} | JS [{js['loi']}] {js['thong_diep']}")
        return lech, lon_nhat
    a, b = py["ok"], js["ok"]
    if loai == "dropship":
        l1, m1 = so_sanh({"ok": a.get("don")}, {"ok": b.get("don")})
        l2, m2 = so_sau({k: v for k, v in a.items() if k != "don"}, {k: v for k, v in b.items() if k != "don"})
        return [f"don_khong_huy.{x}" for x in l1] + l2, max(m1, m2)
    if loai != "don":
        return so_sau(a, b)

    def tien(ten, x, y):
        nonlocal lon_nhat
        if x is not None and y is not None:
            lon_nhat = max(lon_nhat, abs(float(x) - float(y)))
        d = _lech_so(x, y, LECH_TIEN)
        if d is not None:
            lech.append(f"{ten}: Python {x} | JS {y}")

    def ty_le(ten, x, y):
        if _lech_so(x, y, LECH_TY_LE) is not None:
            lech.append(f"{ten}: Python {x} | JS {y}")

    for k in TRUONG_TIEN:
        tien(k, a.get(k), b.get(k))
    # tỷ lệ suy ra từ tiền: cho phép đúng mức lệch tương ứng 1 đ trên lợi nhuận (biên = LN/Rev, ROAS = Rev/LN)
    rev = abs(float(a.get("rev") or 0)) or 1.0
    if _lech_so(a.get("bien_rong"), b.get("bien_rong"), max(LECH_TY_LE, LECH_TIEN / rev)) is not None:
        lech.append(f"bien_rong: Python {a.get('bien_rong')} | JS {b.get('bien_rong')}")
    for k in TRUONG_TY_LE_PHI:
        if _lech_so(a.get(k), b.get(k), max(1e-6, LECH_TIEN / rev)) is not None:
            lech.append(f"{k}: Python {a.get(k)} | JS {b.get(k)}")
    roas = a.get("roas_hoa_von")
    ng_roas = max(LECH_TY_LE, (roas or 0) ** 2 / rev * LECH_TIEN * 1.01)
    if _lech_so(roas, b.get("roas_hoa_von"), ng_roas) is not None:
        lech.append(f"roas_hoa_von: Python {roas} | JS {b.get('roas_hoa_von')}")
    for k in TRUONG_CHU:
        if a.get(k) != b.get(k):
            lech.append(f"{k}: Python {a.get(k)!r} | JS {b.get(k)!r}")
    ca, cb = a.get("chi_phi", []), b.get("chi_phi", [])
    if len(ca) != len(cb):
        lech.append(f"số khoản chi phí: Python {len(ca)} | JS {len(cb)}")
    for x, y in zip(ca, cb):
        if x["ten"] != y["ten"]:
            lech.append(f"tên khoản: Python {x['ten']!r} | JS {y['ten']!r}")
        tien(f"chi phí '{x['ten']}'", x["so_tien"], y["so_tien"])
        ty_le(f"tỷ lệ '{x['ten']}'", x["ty_le"], y["ty_le"])
        for k in ("nguon", "do_tin_cay", "hieu_luc"):
            if x[k] != y[k]:
                lech.append(f"{k} '{x['ten']}': Python {x[k]!r} | JS {y[k]!r}")
    if a.get("canh_bao") != b.get("canh_bao"):
        sa, sb = a.get("canh_bao", []), b.get("canh_bao", [])
        for i in range(max(len(sa), len(sb))):
            x = sa[i] if i < len(sa) else None
            y = sb[i] if i < len(sb) else None
            if x != y:
                lech.append(f"cảnh báo #{i + 1}: Python {x!r} | JS {y!r}")
                break
    fa, fb = a.get("affiliate"), b.get("affiliate")
    if (fa is None) != (fb is None):
        lech.append(f"affiliate: Python {fa} | JS {fb}")
    elif fa:
        for k in AFF_TIEN:
            tien(f"affiliate.{k}", fa.get(k), fb.get(k))
        for k in AFF_TY_LE:
            ty_le(f"affiliate.{k}", fa.get(k), fb.get(k))
    return lech, lon_nhat


def so_sau(a, b, duong: str = "", nguong: float = LECH_TIEN) -> tuple[list[str], float]:
    """So sâu hai kết quả (dict / list / số / chữ). Số: lệch > `nguong` (mặc định 1 đ) = lệch; chữ, đúng/sai: giống hệt."""
    lech: list[str] = []
    lon = 0.0
    so = lambda x: isinstance(x, (int, float)) and not isinstance(x, bool)  # noqa: E731
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                lech.append(f"{duong}{k}: chỉ có ở {'Python' if k in a else 'JS'}")
                continue
            # số ngày / số đếm (ngay_*, so_ngay*) phải bằng hệt; tiền: lệch ≤ 1 đ
            ng = 0.0 if str(k).startswith(("ngay", "so_ngay")) else nguong
            l, m = so_sau(a[k], b[k], f"{duong}{k}.", ng)
            lech += l
            lon = max(lon, m if ng else 0.0)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            lech.append(f"{duong.rstrip('.')}: số phần tử Python {len(a)} | JS {len(b)}")
        for i, (x, y) in enumerate(zip(a, b)):
            l, m = so_sau(x, y, f"{duong}{i}.", nguong)
            lech += l[:1]
            lon = max(lon, m)
    elif so(a) and so(b):
        lon = abs(float(a) - float(b))
        if lon > nguong:
            lech.append(f"{duong.rstrip('.')}: Python {a} | JS {b}")
    elif a != b or type(a) is not type(b) and not (so(a) and so(b)):
        lech.append(f"{duong.rstrip('.')}: Python {a!r} | JS {b!r}")
    return lech, lon


def _nguong_mong_doi(khoa: str, ds: dict) -> float:
    if khoa.startswith(("ngay", "so_ngay")):
        return 0.0
    if khoa.startswith("roas"):
        return ds["roas"]
    if khoa.startswith("gia_hoa_von"):
        return ds["gia_hoa_von_vnd"]
    if khoa == "bien_rong" or khoa.startswith("ty_le_phi"):
        return ds["ty_le"]
    return ds["tien_vnd"]


def so_mong_doi_sau(ra, mong, ds: dict, duong: str = "") -> list[str]:
    """So kết quả Python với 'mong_doi' của P4 (chỉ các khóa P4 ghi), theo dung sai trong tệp P4."""
    lech: list[str] = []
    if isinstance(mong, dict):
        if not isinstance(ra, dict):
            return [f"{duong or 'kết quả'}: mong đợi object, Python có {ra!r}"[:200]]
        for k, v in mong.items():
            if k not in ra:
                lech.append(f"{duong}{k}: có trong mong_doi nhưng Python không trả")
            else:
                lech += so_mong_doi_sau(ra[k], v, ds, f"{duong}{k}.")
    elif isinstance(mong, list):
        if not isinstance(ra, list) or len(ra) != len(mong):
            return [f"{duong.rstrip('.')}: số phần tử mong đợi {len(mong)} | Python {len(ra) if isinstance(ra, list) else ra!r}"]
        for i, (x, y) in enumerate(zip(ra, mong)):
            lech += so_mong_doi_sau(x, y, ds, f"{duong}{i}.")
    elif isinstance(mong, (int, float)) and not isinstance(mong, bool):
        khoa = duong.rstrip(".").split(".")[-1]
        if _lech_so(ra, mong, _nguong_mong_doi(khoa, ds)) is not None:
            lech.append(f"mong đợi P4 {duong.rstrip('.')}={mong} | Python {ra}")
    elif ra != mong:
        lech.append(f"mong đợi P4 {duong.rstrip('.')}={mong!r} | Python {ra!r}")
    return lech


def so_mong_doi(py: dict, mong: dict | None) -> list[str]:
    """So kết quả Python với 'mong_doi' P4 ghi sẵn (chỉ các trường số có mặt)."""
    if not mong:
        return []
    if "ok" not in py:
        return [f"mong đợi có kết quả nhưng Python lỗi: {py.get('thong_diep')}"]
    ra = []
    for k, v in mong.items():
        if isinstance(v, (int, float)) and not isinstance(v, bool) and k in py["ok"]:
            ng = LECH_TY_LE if k in TRUONG_TY_LE else LECH_TIEN
            if _lech_so(py["ok"][k], v, ng) is not None:
                ra.append(f"mong đợi P4 {k}={v} | Python {py['ok'][k]}")
    return ra


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Kiểm khớp máy tính lợi nhuận JS (app) ↔ Python (P4)")
    ap.add_argument("--so-ngau-nhien", type=int, default=400, help="số ví dụ tự sinh (mặc định 400)")
    ap.add_argument("--hat", type=int, default=20261112, help="hạt giống ngẫu nhiên")
    ap.add_argument("--app", default=str(APP), help="tệp app HTML")
    ap.add_argument("--chi-tiet", action="store_true", help="in mọi chỗ lệch")
    ap.add_argument("--tep-p4", default=str(VI_DU_P4), help="tệp ví dụ của P4")
    a = ap.parse_args(argv)

    try:
        tep_p4 = Path(a.tep_p4)
        ds_p4 = dung_sai_p4(tep_p4)
        nhom = [("kiểm ngược P4", vi_du_kiem_nguoc()), ("tự sinh (đơn)", vi_du_ngau_nhien(a.so_ngau_nhien, a.hat)),
                ("tự sinh (dropship, affiliate, vốn, sổ)", vi_du_dot1_ngau_nhien(max(1, a.so_ngau_nhien // 4), a.hat + 1)),
                ("tệp P4 vi-du-kiem-khop.json", vi_du_p4(tep_p4))]
        tat_ca = [v for _, ds in nhom for v in ds]
        py = chay_python(tat_ca)
        js = chay_js(tat_ca, Path(a.app))
    except (FileNotFoundError, RuntimeError, ValueError, json.JSONDecodeError) as e:
        print(f"KHÔNG CHẠY ĐƯỢC: {e}")
        return 2
    if len(js) != len(tat_ca):
        print(f"HỎNG: JS trả {len(js)} kết quả cho {len(tat_ca)} ví dụ")
        return 1

    hong = 0
    lon_nhat = 0.0
    so_loi = sum(1 for x in py if "ok" not in x)
    vi_tri = 0
    print("KIỂM KHỚP JS (app/daovang.html) ↔ Python (apps/finance)")
    for ten_nhom, ds in nhom:
        hong_nhom = 0
        for v in ds:
            lech, m = so_sanh(py[vi_tri], js[vi_tri], v.get("loai", "don"))
            if v.get("mong_doi") is not None:
                lech += (so_mong_doi_sau(py[vi_tri].get("ok"), v["mong_doi"], ds_p4) if "ok" in py[vi_tri]
                         else [f"mong đợi có kết quả nhưng Python lỗi: {py[vi_tri].get('thong_diep')}"])
            lon_nhat = max(lon_nhat, m)
            if lech:
                hong_nhom += 1
                if a.chi_tiet or hong + hong_nhom <= 10:
                    print(f"  HỎNG {v['ten']}:")
                    for l in (lech if a.chi_tiet else lech[:5]):
                        print(f"     - {l}")
            vi_tri += 1
        hong += hong_nhom
        trang_thai = "không có tệp (chưa có trên nhánh này)" if not ds else f"{len(ds) - hong_nhom}/{len(ds)} khớp"
        dem = {}
        for v in ds:
            dem[v.get("loai", "don")] = dem.get(v.get("loai", "don"), 0) + 1
        chi_tiet = " (" + ", ".join(f"{k} {n}" for k, n in dem.items()) + ")" if len(dem) > 1 else ""
        print(f"  {ten_nhom:40} {trang_thai}{chi_tiet}")
    print(f"Tổng {len(tat_ca)} ví dụ ({so_loi} ví dụ nhập sai — kiểm cả thông báo lỗi) · "
          f"lệch tiền lớn nhất {lon_nhat:.6f} đ (ngưỡng {LECH_TIEN:g} đ)")
    print("KẾT LUẬN:", "ĐẠT — 100% khớp" if not hong else f"HỎNG — {hong} ví dụ lệch")
    return 0 if not hong else 1


if __name__ == "__main__":
    raise SystemExit(main())
