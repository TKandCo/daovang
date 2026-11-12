"""KIỂM KHỚP JS ↔ Python: chạy cùng bộ ví dụ qua máy tính Python của P4 (apps/finance) và qua lõi JS nằm trong
app/daovang.html (bằng node). Tiền lệch > 1 đ = HỎNG; tỷ lệ lệch > 0,0001 = HỎNG; chữ (cảnh báo, tên khoản, nguồn)
phải giống hệt (biên ròng / ROAS: cho phép mức lệch tương ứng 1 đ lợi nhuận); ví dụ Python báo lỗi thì JS cũng phải báo lỗi cùng nội dung.

Bộ ví dụ:
  1. 3 ví dụ kiểm ngược của P4 (taichinh.kiem_nguoc.VI_DU) × (mức giữa, mức cao) × (có hoàn, không hoàn)
  2. ví dụ tự sinh ngẫu nhiên có hạt giống cố định (mọi ngành, cả hai sàn, mọi cờ, cả ví dụ nhập sai)
  3. apps/finance/vi-du-kiem-khop.json của P4 NẾU có (đọc thêm; có "mong_doi" thì so cả với số đó)

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

LECH_TIEN = 1.0      # đ
LECH_TY_LE = 1e-4    # cho biên ròng, ROAS, tỷ lệ %
TRUONG_TIEN = ("rev", "cm", "chi_phi_moi_don_hoan", "ln_truoc_qc", "quang_cao", "ln", "gia_hoa_von",
               "gia_hoa_von_truoc_qc", "thue_tam_khau_tru")
TRUONG_TY_LE = ("bien_rong", "roas_hoa_von")
TRUONG_CHU = ("san", "nganh", "ngay_ban", "khong_dam_bao")
AFF_TIEN = ("hoa_hong_ky_vong_moi_don", "quang_cao", "ln_affiliate", "von_hang_moi_don_nhap_truc_tiep",
            "von_hang_moi_don_affiliate", "chenh_lech_nhap_truc_tiep_tru_affiliate")
AFF_TY_LE = ("hoa_hong_nhan_pct", "roas_hoa_von_affiliate")

TEN_DAU_VAO = {f.name for f in fields(DauVao)}
TRUONG_SO = {"gia_ban", "gia_von", "giam_gia_shop", "dong_goi", "ship_shop_chiu", "hoa_hong_aff_shop_tra",
             "quang_cao_pct", "ty_le_hoan", "ship_tra_hang", "ty_le_hong_hang_hoan", "thue_gtgt", "thue_tncn",
             "phi_nganh_tu_nhap", "hoa_hong_aff_nhan", "thue_aff"}


# ---------------- bộ ví dụ ----------------
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
        ra.append({"ten": f"P4 · {m.get('ten', f'mục {i + 1}')}", "dau_vao": chuan_dau_vao(dv),
                   "mong_doi": m.get("mong_doi")})
    return ra


# ---------------- chạy ----------------
def chay_python(vi_du: list[dict]) -> list[dict]:
    mt = MayTinh(BangPhi())
    ra = []
    for v in vi_du:
        dv = dict(v["dau_vao"])
        dv["ngay_ban"] = date.fromisoformat(dv["ngay_ban"])
        try:
            ra.append({"ok": json.loads(json.dumps(mt.tinh(DauVao(**dv)).to_dict()))})
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


def so_sanh(py: dict, js: dict) -> tuple[list[str], float]:
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
    a = ap.parse_args(argv)

    try:
        nhom = [("kiểm ngược P4", vi_du_kiem_nguoc()), ("tự sinh", vi_du_ngau_nhien(a.so_ngau_nhien, a.hat)),
                ("tệp P4 vi-du-kiem-khop.json", vi_du_p4())]
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
            lech, m = so_sanh(py[vi_tri], js[vi_tri])
            lech += so_mong_doi(py[vi_tri], v.get("mong_doi"))
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
        print(f"  {ten_nhom:30} {trang_thai}")
    print(f"Tổng {len(tat_ca)} ví dụ ({so_loi} ví dụ nhập sai — kiểm cả thông báo lỗi) · "
          f"lệch tiền lớn nhất {lon_nhat:.6f} đ (ngưỡng {LECH_TIEN:g} đ)")
    print("KẾT LUẬN:", "ĐẠT — 100% khớp" if not hong else f"HỎNG — {hong} ví dụ lệch")
    return 0 if not hong else 1


if __name__ == "__main__":
    raise SystemExit(main())
