#!/usr/bin/env python3
"""Chấm điểm TÁCH affiliate / dropship (P1, Đợt 1, việc P1-D1A). Chỉ thư viện chuẩn Python 3.10+.

Phí sàn KHÔNG gõ tay, KHÔNG dùng "~24%": lấy từ máy tính P4 (`apps/finance/taichinh`), máy đó đọc
`bao-cao/dot0/bang-phi-v1.csv` theo ngành + ngày hiệu lực.

Chạy (đứng ở gốc repo):
  python3 apps/radar/cham_diem.py              # chấm các dòng chủ dự án đã điền trong nhap-tay/4-nhom.csv
  python3 apps/radar/cham_diem.py --phi        # in bảng phí theo nhóm (có / không voucher sàn)
  python3 apps/radar/cham_diem.py --ghi-phi    # ghi lại du-lieu/phi-theo-nhom.csv

Hai mô hình chấm KHÁC nhau ở tiêu chí "biên" (tối đa 25 điểm):
  - affiliate: hoa hồng THỰC NHẬN = giá × tỷ lệ hoa hồng × (1 − hoàn) × (1 − phí affiliate) × (1 − thuế khấu trừ).
    Không chịu phí sàn của người bán. Ngành không có hoa hồng → 0 điểm, loại.
  - dropship: biên ròng SAU PHÍ do máy P4 tính (phí ngành + giao dịch + phí đơn + voucher sàn + thuế + hoàn).
    Chấm theo kịch bản CÓ voucher sàn (thận trọng: shop mới thường phải vào voucher — P12 mục 2.1).

Không phải khuyến nghị đầu tư / không đảm bảo lợi nhuận. Ngưỡng điểm và mọi tỷ lệ mặc định là GIẢ ĐỊNH.
"""
from __future__ import annotations

import argparse
import csv
import os
import sys
from datetime import date

GOC = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(GOC, "..", ".."))
sys.path.insert(0, GOC)
sys.path.insert(0, os.path.join(REPO, "apps", "finance"))

import kiem_tra as kt  # noqa: E402
from taichinh.bang_phi import ThieuDuLieu, bo_dau  # noqa: E402
from taichinh.tinh_loi_nhuan import DauVao, MayTinh  # noqa: E402

# Ngày tính cố định để bảng phí-theo-nhóm tái lập được (đổi khi bảng phí có bản mới).
NGAY_TINH = date(2026, 11, 12)
GIA_THAM_CHIEU = (50_000, 100_000, 200_000)  # GIẢ ĐỊNH: 3 mức giá để thấy phí cố định/đơn ảnh hưởng thế nào
P_PHI_NHOM = os.path.join(GOC, "du-lieu", "phi-theo-nhom.csv")
P_NHAP_TAY = os.path.join(GOC, "nhap-tay", "4-nhom.csv")
LOAI_PHI_NGANH = {"Shopee": ("shopee", "phi_co_dinh"), "TikTok Shop": ("tiktok", "phi_hoa_hong_nen_tang")}

# ---- Affiliate ----
# Shopee Affiliate: phí 0,98% trên tổng hoa hồng (từ 16/05/2025); khấu trừ TNCN 10% mỗi khoản thanh toán
# ≥ 250.000đ (từ 20/11/2025). Nguồn S28 = https://shopee.vn/blog/?p=190331 (09/07/2026) [CAO theo P1 Đợt 0].
# Công cụ LUÔN trừ 10% (thận trọng — khoản nhỏ hơn 250.000đ/lần có thể không bị trừ).
# TikTok: phí nền tảng affiliate CHƯA XÁC MINH (tính 0%); thuế 10% là GIẢ ĐỊNH thận trọng.
AFF = {
    "shopee": {"phi_pct": 0.98, "thue_pct": 10.0, "nguon": "S28 [CAO]"},
    "tiktok": {"phi_pct": 0.0, "thue_pct": 10.0, "nguon": "CHƯA XÁC MINH (phí 0%, thuế 10% GIẢ ĐỊNH)"},
}
# Shopee Affiliate KHÔNG tính hoa hồng: Mẹ & Bé, sức khỏe nhạy cảm, rượu ≥ 15% (S18 [CAO]).
# So khớp thô theo tên ngành (không dấu) — trùng chữ "suc khoe" là CHẶN luôn, chủ dự án kiểm lại.
NGANH_KHONG_HOA_HONG = ("me & be", "me va be", "me be", "suc khoe", "ruou")

TY_LE_HOAN_MAC_DINH = 5.0  # GIẢ ĐỊNH — tỷ lệ hoàn thật CHƯA ĐO
QUANG_CAO_MAC_DINH = 0.0   # biên "sau phí" chưa trừ quảng cáo; ROAS hòa vốn xem máy P4


def khong_co_hoa_hong(nganh: str) -> bool:
    n = bo_dau(nganh)
    return any(k in n for k in NGANH_KHONG_HOA_HONG)


def nganh_tu_fee_ref(fee_ref: str) -> dict[str, str]:
    """'Shopee|phi_co_dinh|X;TikTok Shop|phi_hoa_hong_nen_tang|Y' → {'shopee': X, 'tiktok': Y} (lấy dòng đầu mỗi sàn)."""
    ra: dict[str, str] = {}
    for ref in kt.tach_ma(fee_ref):
        p = ref.split("|", 2)
        if len(p) == 3 and p[0] in LOAI_PHI_NGANH and p[1] == LOAI_PHI_NGANH[p[0]][1]:
            ra.setdefault(LOAI_PHI_NGANH[p[0]][0], p[2])
    return ra


def doc_nhom(goc: str = GOC) -> dict[str, dict]:
    tieu_de, ds = kt.doc_csv(os.path.join(goc, "du-lieu", "nhom-ung-vien.csv"))
    return {h[0]: dict(zip(tieu_de, h)) for h in ds if h and len(h) == len(tieu_de)}


def tong_phi(mt: MayTinh, san: str, nganh: str, gia: float, voucher: bool, ngay: date = NGAY_TINH):
    """% phí sàn + thuế khấu trừ trên doanh thu đơn (chưa có giá vốn, chưa hoàn, chưa quảng cáo)."""
    k = mt.tinh(DauVao(san=san, nganh=nganh, gia_ban=gia, gia_von=0, ngay_ban=ngay,
                       tham_gia_voucher_san=voucher), tim_hoa_von=False)
    phi_nganh = next(c.ty_le for c in k.chi_phi if c.ten.startswith("Phí ngành"))
    canh_bao = [c for c in k.canh_bao if "khoảng" in c or "Phí ngành: độ tin cậy" in c]
    return (k.rev - k.cm) / k.rev * 100, phi_nganh, canh_bao


COT_PHI = ["nhom_id", "ten_nhom", "san", "nganh_bang_phi", "voucher_san", "phi_nganh_pct",
           "tong_phi_pct_gia_50k", "tong_phi_pct_gia_100k", "tong_phi_pct_gia_200k",
           "ngay_tinh", "nguon", "ghi_chu"]


def bang_phi_theo_nhom(goc: str = GOC, mt: MayTinh | None = None) -> list[list[str]]:
    mt = mt or MayTinh()
    dong = []
    for nid, n in doc_nhom(goc).items():
        for san, nganh in nganh_tu_fee_ref(n["fee_ref"]).items():
            for voucher in (False, True):
                try:
                    ket = [tong_phi(mt, san, nganh, g, voucher) for g in GIA_THAM_CHIEU]
                    phi_nganh = f"{ket[0][1]:g}"
                    cot_phi = [f"{x[0]:.1f}" for x in ket]
                    ghi = "; ".join(dict.fromkeys(ket[0][2])) or ""
                except ThieuDuLieu as e:
                    phi_nganh, cot_phi, ghi = "CHƯA XÁC MINH", ["CHƯA XÁC MINH"] * 3, str(e)
                dong.append([nid, n["ten_nhom"], "Shopee" if san == "shopee" else "TikTok Shop", nganh,
                             "CO" if voucher else "KHONG", phi_nganh, *cot_phi, NGAY_TINH.isoformat(),
                             "apps/finance (P4) + bao-cao/dot0/bang-phi-v1.csv", ghi])
    return dong


def ghi_bang_phi(p: str = P_PHI_NHOM) -> int:
    dong = bang_phi_theo_nhom()
    with open(p, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(COT_PHI)
        w.writerows(dong)
    return len(dong)


# ---- Chấm tiêu chí "biên" theo từng mô hình ----
def cham_affiliate(san: str, nganh: str, gia: float, hoa_hong_pct: float,
                   ty_le_hoan: float = TY_LE_HOAN_MAC_DINH, mt: MayTinh | None = None) -> dict:
    """Hoa hồng thực nhận / đơn. Dùng công thức affiliate của máy P4 (hoa hồng × (1 − hoàn) × (1 − khấu trừ))."""
    if san not in AFF:
        raise ThieuDuLieu(f"sàn '{san}' chưa hỗ trợ affiliate")
    if san == "shopee" and khong_co_hoa_hong(nganh):
        return {"mo_hinh": "affiliate", "thuc_nhan_vnd": 0.0, "thuc_nhan_pct": 0.0, "diem_bien": 0,
                "loai": True, "ly_do": "ngành không có hoa hồng Shopee Affiliate (S18)"}
    a = AFF[san]
    khau_tru = (1 - (1 - a["phi_pct"] / 100) * (1 - a["thue_pct"] / 100)) * 100
    mt = mt or MayTinh()
    k = mt.tinh(DauVao(san=san, nganh=nganh, gia_ban=gia, gia_von=0, ngay_ban=NGAY_TINH,
                       ty_le_hoan=ty_le_hoan, hoa_hong_aff_nhan=hoa_hong_pct, thue_aff=khau_tru),
                tim_hoa_von=False)
    vnd = k.affiliate["hoa_hong_ky_vong_moi_don"]
    pct = vnd / k.rev * 100
    diem = kt.diem_bien("affiliate", pct)
    return {"mo_hinh": "affiliate", "thuc_nhan_vnd": round(vnd), "thuc_nhan_pct": round(pct, 2),
            "diem_bien": diem, "loai": diem == 0,
            "ly_do": f"khấu trừ {khau_tru:.2f}% ({a['nguon']}); hoàn {ty_le_hoan:g}% GIẢ ĐỊNH"}


def cham_dropship(san: str, nganh: str, gia: float, gia_nhap: float, voucher: bool = True,
                  ty_le_hoan: float = TY_LE_HOAN_MAC_DINH, quang_cao: float = QUANG_CAO_MAC_DINH,
                  mt: MayTinh | None = None) -> dict:
    """Biên ròng sau phí (máy P4). gia_nhap = giá nhà cung cấp gồm ship tới khách."""
    mt = mt or MayTinh()
    k = mt.tinh(DauVao(san=san, nganh=nganh, gia_ban=gia, gia_von=gia_nhap, ngay_ban=NGAY_TINH,
                       tham_gia_voucher_san=voucher, ty_le_hoan=ty_le_hoan, quang_cao_pct=quang_cao),
                tim_hoa_von=False)
    pct = k.bien_rong * 100
    diem = kt.diem_bien("dropship", pct)
    return {"mo_hinh": "dropship", "ln_vnd": round(k.ln), "bien_pct": round(pct, 2), "diem_bien": diem,
            "loai": diem == 0, "voucher_san": voucher,
            "ly_do": f"phí theo ngành '{k.nganh}' (P4); hoàn {ty_le_hoan:g}%, quảng cáo {quang_cao:g}% GIẢ ĐỊNH"}


def cham_nhap_tay(p: str = P_NHAP_TAY, goc: str = GOC) -> list[dict]:
    """Chấm mọi dòng đã điền: affiliate nếu có hoa_hong_pct, dropship nếu có gia_nhap_vnd."""
    nhom = doc_nhom(goc)
    tieu_de, ds = kt.doc_csv(p)
    mt = MayTinh()
    ra = []
    for i, h in enumerate(ds, start=2):
        if not any(c.strip() for c in h) or len(h) != len(tieu_de):
            continue
        d = dict(zip(tieu_de, h))
        san = d["san"].strip().lower()
        nganh = nganh_tu_fee_ref(nhom[d["nhom_id"]]["fee_ref"]).get(san, "")
        gia = kt.so_tien(d["gia_ban_vnd"])
        kq = {"dong": i, "nhom_id": d["nhom_id"], "san": san, "ten": d["ten_san_pham"], "gia": gia}
        kq["affiliate"] = (cham_affiliate(san, nganh, gia, float(d["hoa_hong_pct"].replace(",", ".")), mt=mt)
                           if d["hoa_hong_pct"].strip() else "CHƯA ĐO")
        if d["gia_nhap_vnd"].strip():
            kq["dropship_co_voucher"] = cham_dropship(san, nganh, gia, kt.so_tien(d["gia_nhap_vnd"]), True, mt=mt)
            kq["dropship_khong_voucher"] = cham_dropship(san, nganh, gia, kt.so_tien(d["gia_nhap_vnd"]), False, mt=mt)
        else:
            kq["dropship_co_voucher"] = kq["dropship_khong_voucher"] = "CHƯA ĐO"
        ra.append(kq)
    return ra


def _in_nhap_tay():
    ds = cham_nhap_tay()
    if not ds:
        print("Chưa có dòng nào trong apps/radar/nhap-tay/4-nhom.csv — xem nhap-tay/HUONG-DAN.md")
    for k in ds:
        print(f"\nDòng {k['dong']} · {k['nhom_id']} · {k['san']} · {k['ten']} · giá {k['gia']:,.0f}đ")
        a = k["affiliate"]
        print("  Affiliate :", a if isinstance(a, str) else
              f"thực nhận {a['thuc_nhan_vnd']:,}đ/đơn ({a['thuc_nhan_pct']}%) → điểm biên {a['diem_bien']}/25"
              f"{' — LOẠI' if a['loai'] else ''} ({a['ly_do']})")
        for nhan, key in (("Dropship (có voucher sàn)", "dropship_co_voucher"),
                          ("Dropship (không voucher) ", "dropship_khong_voucher")):
            x = k[key]
            print(f"  {nhan}:", x if isinstance(x, str) else
                  f"lãi {x['ln_vnd']:,}đ/đơn, biên {x['bien_pct']}% → điểm biên {x['diem_bien']}/25"
                  f"{' — LOẠI' if x['loai'] else ''}")
    print("\nĐiểm dropship chính thức = kịch bản CÓ voucher sàn (thận trọng). "
          "Không phải khuyến nghị đầu tư / không đảm bảo lợi nhuận.")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Chấm điểm affiliate / dropship (P1)")
    ap.add_argument("--phi", action="store_true", help="in bảng phí theo nhóm")
    ap.add_argument("--ghi-phi", action="store_true", help="ghi du-lieu/phi-theo-nhom.csv")
    a = ap.parse_args(argv)
    if a.ghi_phi:
        print(f"Đã ghi {ghi_bang_phi()} dòng vào {kt.ten_tep(P_PHI_NHOM)}")
    elif a.phi:
        for d in bang_phi_theo_nhom():
            print(f"{d[0]} {d[2]:<11} voucher={d[4]:<5} ngành {d[5]:>4}% → tổng phí "
                  f"{d[6]}% / {d[7]}% / {d[8]}% (giá 50k / 100k / 200k)")
    else:
        _in_nhap_tay()
    return 0


if __name__ == "__main__":
    sys.exit(main())
