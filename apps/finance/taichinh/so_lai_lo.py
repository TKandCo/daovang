"""Sổ lãi lỗ CỘNG DỒN cả dự án — đo cổng Đợt 1:
"lãi ròng cộng dồn CẢ DỰ ÁN trong 4 tuần cuối ≥ 0 sau MỌI phí, kể cả công cụ" (affiliate + dropship + chi chung).

Tệp CSV (UTF-8, có BOM cũng được), mỗi dòng một khoản thu hoặc chi:
    ngay,thu_chi,loai,mo_hinh,kenh,so_tien_vnd,phan_bo_tu,phan_bo_den,mo_ta,nguon
- thu_chi: thu | chi.  so_tien_vnd: số nguyên dương (VND).
- mo_hinh: affiliate | dropship | chung (công cụ, kế toán... dùng chung → chỉ vào tổng dự án).
- phan_bo_tu / phan_bo_den (tùy chọn, YYYY-MM-DD): rải đều khoản (vd. gói công cụ tháng) theo ngày trong kỳ đó,
  để khoản trả trước cửa sổ 4 tuần vẫn được tính phần thuộc cửa sổ. Bỏ trống = ghi nhận trọn vào `ngay`.
DỮ LIỆU THẬT ĐỂ NGOÀI REPO (vd. thư mục `du-lieu-that/` đã nằm trong .gitignore, hoặc ổ khác). Tệp mẫu:
`apps/finance/du-lieu-mau/so-lai-lo-mau.csv` (toàn số GIẢ ĐỊNH).

Chạy: python3 -m taichinh.so_lai_lo --so <đường dẫn CSV> --ngay-cuoi YYYY-MM-DD
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import dataclass, asdict
from datetime import date, timedelta
from pathlib import Path, PurePath
from typing import Iterable, Optional

from .bang_phi import GOC_REPO, ThieuDuLieu
from .tinh_loi_nhuan import DONG_KHONG_DAM_BAO

COT = ["ngay", "thu_chi", "loai", "mo_hinh", "kenh", "so_tien_vnd", "phan_bo_tu", "phan_bo_den", "mo_ta", "nguon"]
LOAI_THU = {"doanh_thu_don", "hoa_hong_affiliate", "hoan_thue", "thu_khac"}
LOAI_CHI = {"gia_von_ncc", "phi_ncc", "phi_san", "thue_khau_tru", "ship", "hoan_tien_khach", "chi_phi_huy_don",
            "quang_cao", "cong_cu", "hang_mau", "noi_dung", "ke_toan_phap_ly", "chi_khac"}
MO_HINH = {"affiliate", "dropship", "chung"}
KENH = {"shopee", "tiktok", "chung", "khac"}
THU_MUC_MAU = (GOC_REPO / "apps" / "finance" / "du-lieu-mau").resolve()


@dataclass
class DongSo:
    ngay: date
    thu_chi: str
    loai: str
    mo_hinh: str
    kenh: str
    so_tien_vnd: int
    phan_bo_tu: Optional[date] = None
    phan_bo_den: Optional[date] = None
    mo_ta: str = ""
    nguon: str = ""

    @property
    def dau(self) -> int:
        return 1 if self.thu_chi == "thu" else -1

    def phan_trong(self, tu: date, den: date) -> float:
        """Số tiền (có dấu) của dòng này rơi vào [tu, den] (gồm cả hai đầu)."""
        a, b = (self.phan_bo_tu, self.phan_bo_den) if self.phan_bo_tu else (self.ngay, self.ngay)
        so_ngay = (b - a).days + 1
        giao = (min(b, den) - max(a, tu)).days + 1
        if giao <= 0:
            return 0.0
        return self.dau * self.so_tien_vnd * giao / so_ngay

    def to_row(self) -> dict:
        d = asdict(self)
        for k in ("ngay", "phan_bo_tu", "phan_bo_den"):
            d[k] = d[k].isoformat() if d[k] else ""
        return d


def _ngay(s: str, ten: str, vt: str) -> date:
    try:
        return date.fromisoformat(s.strip())
    except ValueError:
        raise ThieuDuLieu(f"{vt}: {ten} '{s}' không đúng dạng YYYY-MM-DD")


def kiem_dong(row: dict, vt: str = "dòng") -> DongSo:
    """Đọc + kiểm một dòng (dict theo COT). Báo ThieuDuLieu nếu sai."""
    g = {k: str(row.get(k) if row.get(k) is not None else "").strip() for k in COT}
    tc = g["thu_chi"].lower()
    if tc not in ("thu", "chi"):
        raise ThieuDuLieu(f"{vt}: thu_chi phải là 'thu' hoặc 'chi', nhận '{g['thu_chi']}'")
    loai = g["loai"].lower()
    hop_le = LOAI_THU if tc == "thu" else LOAI_CHI
    if loai not in hop_le:
        raise ThieuDuLieu(f"{vt}: loai '{g['loai']}' không hợp lệ cho '{tc}'; chọn trong {sorted(hop_le)}")
    mh = g["mo_hinh"].lower()
    if mh not in MO_HINH:
        raise ThieuDuLieu(f"{vt}: mo_hinh phải trong {sorted(MO_HINH)}")
    kenh = g["kenh"].lower() or "chung"
    if kenh not in KENH:
        raise ThieuDuLieu(f"{vt}: kenh phải trong {sorted(KENH)}")
    st = g["so_tien_vnd"].replace(".", "").replace(",", "").replace("_", "")
    if not st.isdigit() or int(st) <= 0:
        raise ThieuDuLieu(f"{vt}: so_tien_vnd phải là số nguyên dương (VND), nhận '{g['so_tien_vnd']}'")
    tu = _ngay(g["phan_bo_tu"], "phan_bo_tu", vt) if g["phan_bo_tu"] else None
    den = _ngay(g["phan_bo_den"], "phan_bo_den", vt) if g["phan_bo_den"] else None
    if (tu is None) != (den is None):
        raise ThieuDuLieu(f"{vt}: cần cả phan_bo_tu và phan_bo_den (hoặc bỏ trống cả hai)")
    if tu and den < tu:
        raise ThieuDuLieu(f"{vt}: phan_bo_den trước phan_bo_tu")
    return DongSo(_ngay(g["ngay"], "ngay", vt), tc, loai, mh, kenh, int(st), tu, den, g["mo_ta"], g["nguon"])


def _trong_repo_ngoai_mau(p: PurePath, goc: PurePath, mau: PurePath) -> bool:
    # Path.is_relative_to chỉ so phần đầu đường dẫn: khác ổ đĩa (C:\ vs D:\) trả False, KHÔNG báo lỗi
    # như os.path.relpath → an toàn với thư mục tạm khác ổ trên Windows.
    return p.is_relative_to(goc) and not p.is_relative_to(mau)


def la_du_lieu_trong_repo(duong_dan) -> bool:
    """True nếu tệp nằm trong repo nhưng NGOÀI thư mục mẫu (nguy cơ commit dữ liệu thật)."""
    return _trong_repo_ngoai_mau(Path(duong_dan).resolve(), GOC_REPO, THU_MUC_MAU)


def doc_so(duong_dan) -> list[DongSo]:
    p = Path(duong_dan)
    if not p.is_file():
        raise ThieuDuLieu(f"không thấy sổ: {p}")
    with open(p, encoding="utf-8-sig", newline="") as f:
        r = csv.DictReader(f)
        thieu = [c for c in COT if c not in (r.fieldnames or [])]
        if thieu:
            raise ThieuDuLieu(f"sổ thiếu cột: {', '.join(thieu)}")
        ra = []
        for i, row in enumerate(r, start=2):
            if None in row:
                raise ThieuDuLieu(f"dòng {i}: thừa cột")
            if not any((v or "").strip() for v in row.values()):
                continue
            ra.append(kiem_dong(row, f"dòng {i}"))
    return ra


def ghi_dong(duong_dan, dong: DongSo | dict) -> None:
    """Thêm một dòng vào cuối sổ (tạo tệp + tiêu đề nếu chưa có). Kiểm dòng trước khi ghi."""
    if isinstance(dong, dict):
        dong = kiem_dong(dong)
    else:
        dong = kiem_dong(dong.to_row())
    p = Path(duong_dan)
    moi = not p.exists() or p.stat().st_size == 0
    with open(p, "a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COT)
        if moi:
            w.writeheader()
        w.writerow(dong.to_row())


def tong_hop(dong: Iterable[DongSo], tu: date, den: date) -> dict:
    """Lãi lỗ trong [tu, den] (đã phân bổ). Trả tổng, theo mô hình, theo loại. Tiền làm tròn đồng."""
    dong = list(dong)
    thu = chi = 0.0
    theo_mh = {m: 0.0 for m in sorted(MO_HINH)}
    theo_loai: dict[str, float] = {}
    for d in dong:
        v = d.phan_trong(tu, den)
        if not v:
            continue
        if v > 0:
            thu += v
        else:
            chi += -v
        theo_mh[d.mo_hinh] += v
        theo_loai[d.loai] = theo_loai.get(d.loai, 0.0) + v
    return {
        "tu": tu.isoformat(), "den": den.isoformat(),
        "thu": round(thu), "chi": round(chi), "lai_rong": round(thu - chi),
        "theo_mo_hinh": {k: round(v) for k, v in theo_mh.items()},
        "theo_loai": {k: round(v) for k, v in sorted(theo_loai.items())},
    }


def kiem_cong_dot1(dong: Iterable[DongSo], ngay_cuoi: date, so_ngay: int = 28) -> dict:
    """Cổng Đợt 1: lãi ròng cộng dồn cả dự án trong `so_ngay` (mặc định 28 = 4 tuần) kết thúc `ngay_cuoi` ≥ 0."""
    dong = list(dong)
    if not dong:
        raise ThieuDuLieu("sổ trống")
    tu = ngay_cuoi - timedelta(days=so_ngay - 1)
    dau = min((d.phan_bo_tu or d.ngay) for d in dong)
    cua_so = tong_hop(dong, tu, ngay_cuoi)
    tu_dau = tong_hop(dong, min(dau, tu), ngay_cuoi)
    cb = ["Cổng đo trên cửa sổ 4 tuần cuối; cũng in lãi cộng dồn TỪ ĐẦU dự án để chủ dự án thấy cả hai",
          "Thuế khấu trừ được tính là CHI (thận trọng) dù có thể được hoàn khi doanh thu năm ≤ 1 tỷ"]
    ngoai = [d for d in dong if d.thu_chi == "chi" and not d.phan_bo_tu and d.ngay < tu
             and d.loai in ("cong_cu", "hang_mau", "noi_dung", "ke_toan_phap_ly") and d.so_tien_vnd >= 1_000_000]
    for d in ngoai:
        cb.append(f"Khoản {d.loai} {_vnd(d.so_tien_vnd)} ngày {d.ngay} trước cửa sổ và KHÔNG phân bổ — nếu là gói dùng "
                  "trong cửa sổ, hãy điền phan_bo_tu / phan_bo_den để cổng không bị 'dễ' giả")
    muon = [d for d in dong if d.ngay > ngay_cuoi]
    if muon:
        cb.append(f"{len(muon)} dòng có ngày sau {ngay_cuoi} — không tính")
    return {
        "cua_so_4_tuan": cua_so,
        "tu_dau_du_an": tu_dau,
        "dat_cong_dot1": cua_so["lai_rong"] >= 0,
        "canh_bao": cb,
        "khong_dam_bao": DONG_KHONG_DAM_BAO,
    }


def theo_tuan(dong: Iterable[DongSo], ngay_dau: date, so_tuan: int) -> list[dict]:
    """Lãi từng tuần (7 ngày từ ngay_dau) và cộng dồn."""
    dong = list(dong)
    cong = 0
    ra = []
    for w in range(so_tuan):
        a = ngay_dau + timedelta(days=7 * w)
        t = tong_hop(dong, a, a + timedelta(days=6))
        cong += t["lai_rong"]
        ra.append({"tuan": w + 1, "tu": t["tu"], "den": t["den"], "lai_tuan": t["lai_rong"], "cong_don": cong,
                   "affiliate": t["theo_mo_hinh"]["affiliate"], "dropship": t["theo_mo_hinh"]["dropship"],
                   "chung": t["theo_mo_hinh"]["chung"]})
    return ra


def _vnd(x) -> str:
    return f"{x:,.0f}".replace(",", ".") + " đ"


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="python3 -m taichinh.so_lai_lo", description="Sổ lãi lỗ cộng dồn — cổng Đợt 1")
    p.add_argument("--so", required=True, help="đường dẫn CSV sổ (dữ liệu thật để NGOÀI repo)")
    p.add_argument("--ngay-cuoi", required=True, help="YYYY-MM-DD: ngày cuối cửa sổ 4 tuần")
    p.add_argument("--so-ngay", type=int, default=28)
    p.add_argument("--json", action="store_true")
    a = p.parse_args(argv)
    try:
        if la_du_lieu_trong_repo(a.so):
            print("CẢNH BÁO: sổ nằm TRONG repo — dữ liệu thật phải để ngoài repo (Quy tắc 1)", file=sys.stderr)
        dong = doc_so(a.so)
        kq = kiem_cong_dot1(dong, date.fromisoformat(a.ngay_cuoi), a.so_ngay)
    except (ThieuDuLieu, ValueError) as e:
        print(f"LỖI / THIẾU DỮ LIỆU: {e}", file=sys.stderr)
        return 2
    if a.json:
        print(json.dumps(kq, ensure_ascii=False, indent=2))
        return 0
    c, t = kq["cua_so_4_tuan"], kq["tu_dau_du_an"]
    print(f"=== Sổ lãi lỗ cộng dồn — cửa sổ {c['tu']} → {c['den']} ===")
    print(f"Thu {_vnd(c['thu'])} · Chi {_vnd(c['chi'])} · LÃI RÒNG 4 TUẦN: {_vnd(c['lai_rong'])}")
    for k, v in c["theo_mo_hinh"].items():
        print(f"  - {k}: {_vnd(v)}")
    print(f"Từ đầu dự án ({t['tu']}): lãi ròng cộng dồn {_vnd(t['lai_rong'])}")
    print(f">>> CỔNG ĐỢT 1: {'ĐẠT' if kq['dat_cong_dot1'] else 'CHƯA ĐẠT'} (lãi 4 tuần cuối ≥ 0)")
    for x in kq["canh_bao"]:
        print(f"  ! {x}")
    print(kq["khong_dam_bao"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
