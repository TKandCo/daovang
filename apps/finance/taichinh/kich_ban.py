"""Bảng 3 kịch bản XẤU / VỪA / TỐT cho 8 tuần Đợt 1 + điểm hòa vốn theo số đơn (P12 mục 1.6).

MỌI SỐ Ở ĐÂY LÀ GIẢ ĐỊNH (số đơn, tỷ lệ hoàn / hủy, ROAS, hoa hồng, giá SKU mẫu) — không phải dự báo.
Phí sàn lấy từ bảng phí v1 (mức CAO = thận trọng); phí / thuế affiliate từ affiliate.py.
Chi phí cố định 8 tuần GIẢ ĐỊNH = các dòng Mức A trong `ban-thu-ky/so-ngan-sach.md` trừ quảng cáo và dự phòng:
P1 100 + P2 250 + P4 50 + P8 100 + hàng mẫu 200 + token 50 = 750 USD × 26.000 = 19,5 triệu đ, rải đều 8 tuần.
Quảng cáo: 150 USD = 3,9 triệu đ, rải đều tuần 3–8.

Chạy: python3 -m taichinh.kich_ban   [--json]
"""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from datetime import date

from .affiliate import PHI_NEN_TANG_PCT, THUE_TNCN_PCT
from .dropship import tinh_dropship
from .tinh_loi_nhuan import DauVao, MayTinh, DONG_KHONG_DAM_BAO

TY_GIA = 26_000  # đ/USD, tỷ giá tham chiếu sổ ngân sách
CO_DINH_8_TUAN = 750 * TY_GIA
QUANG_CAO_8_TUAN = 150 * TY_GIA
TUAN_QC = (3, 4, 5, 6, 7, 8)
NGAY = date(2026, 11, 12)

# SKU dropship mẫu — GIẢ ĐỊNH
SKU_MAU = dict(san="shopee", nganh="Sac dep", gia_ban=199_000, gia_von=80_000, ngay_ban=NGAY,
               ship_tra_hang=30_000, ty_le_hong_hang_hoan=50)
PHI_NCC = 5_000
GIA_TRI_DON_AFF = 150_000


@dataclass
class KichBan:
    ten: str
    ty_le_hoan: float
    ty_le_huy: float
    roas: float
    don_dropship_tuan: list[int]
    don_aff_tuan: list[int]
    hoa_hong_aff_pct: float
    huy_aff_pct: float
    ghi_chu: str = "GIẢ ĐỊNH"


KICH_BAN = [
    KichBan("XẤU", 12, 10, 2.0, [0, 0, 2, 3, 4, 5, 6, 6], [0, 2, 4, 5, 6, 6, 8, 8], 5, 15),
    KichBan("VỪA", 8, 6, 4.0, [0, 3, 6, 10, 14, 18, 22, 25], [3, 8, 12, 18, 24, 30, 35, 40], 8, 10),
    KichBan("TỐT", 5, 3, 6.0, [2, 6, 12, 20, 28, 35, 42, 50], [5, 12, 20, 30, 40, 50, 60, 70], 11, 8),
]


def hh_net_moi_don_aff(ty_le_pct: float, huy_pct: float, gia_tri: float = GIA_TRI_DON_AFF) -> float:
    """Hoa hồng thực nhận / đơn affiliate. Thận trọng: luôn coi khoản thanh toán ≥ 250.000đ (bị khấu trừ 10%)."""
    return gia_tri * ty_le_pct / 100 * (1 - huy_pct / 100) * (1 - PHI_NEN_TANG_PCT / 100) * (1 - THUE_TNCN_PCT / 100)


def chay_kich_ban(kb: KichBan, mt: MayTinh | None = None) -> dict:
    mt = mt or MayTinh()
    ds = tinh_dropship(DauVao(ty_le_hoan=kb.ty_le_hoan, **SKU_MAU), phi_ncc=PHI_NCC, ty_le_huy=kb.ty_le_huy, mt=mt,
                       tim_hoa_von=False)
    ln_don = ds.ln_truoc_qc_moi_don_dat          # LN trước QC / đơn đặt (đã trừ hoàn, hủy)
    rev = ds.don.rev
    hh = hh_net_moi_don_aff(kb.hoa_hong_aff_pct, kb.huy_aff_pct)
    co_dinh_tuan = CO_DINH_8_TUAN / 8
    qc_tuan = QUANG_CAO_8_TUAN / len(TUAN_QC)
    tuan, cong = [], 0.0
    for w in range(8):
        qc = qc_tuan if (w + 1) in TUAN_QC else 0.0
        don_qc = qc * kb.roas / rev
        lai = (kb.don_dropship_tuan[w] + don_qc) * ln_don - qc + kb.don_aff_tuan[w] * hh - co_dinh_tuan
        cong += lai
        tuan.append({"tuan": w + 1, "don_dropship_tu_nhien": kb.don_dropship_tuan[w], "don_tu_quang_cao": round(don_qc, 1),
                     "don_affiliate": kb.don_aff_tuan[w], "quang_cao": round(qc), "lai_tuan": round(lai),
                     "cong_don": round(cong)})
    lai_4_tuan_cuoi = sum(t["lai_tuan"] for t in tuan[4:])
    roas_hv = rev / ln_don if ln_don > 0 else None
    return {
        "ten": kb.ten,
        "gia_dinh": {"ty_le_hoan_pct": kb.ty_le_hoan, "ty_le_huy_pct": kb.ty_le_huy, "roas_thuc": kb.roas,
                     "hoa_hong_aff_pct": kb.hoa_hong_aff_pct, "huy_aff_pct": kb.huy_aff_pct},
        "ln_truoc_qc_moi_don_dropship": round(ln_don),
        "hoa_hong_thuc_nhan_moi_don_aff": round(hh),
        "roas_hoa_von": round(roas_hv, 2) if roas_hv else None,
        "quang_cao_lai": bool(roas_hv and kb.roas > roas_hv),
        "tuan": tuan,
        "tong_don_dropship": sum(kb.don_dropship_tuan) + round(sum(t["don_tu_quang_cao"] for t in tuan)),
        "tong_don_affiliate": sum(kb.don_aff_tuan),
        "lai_8_tuan": round(cong),
        "lai_4_tuan_cuoi": lai_4_tuan_cuoi,
        "dat_cong_dot1": lai_4_tuan_cuoi >= 0,
        # điểm hòa vốn theo số đơn
        "hoa_von_don_dropship_8_tuan": round(CO_DINH_8_TUAN / ln_don) if ln_don > 0 else None,
        "hoa_von_don_affiliate_8_tuan": round(CO_DINH_8_TUAN / hh) if hh > 0 else None,
        "hoa_von_don_dropship_moi_tuan": round(co_dinh_tuan / ln_don, 1) if ln_don > 0 else None,
        "hoa_von_don_affiliate_moi_tuan": round(co_dinh_tuan / hh, 1) if hh > 0 else None,
    }


def chay_tat_ca(mt: MayTinh | None = None) -> dict:
    mt = mt or MayTinh()
    return {
        "co_dinh_8_tuan": CO_DINH_8_TUAN, "quang_cao_8_tuan": QUANG_CAO_8_TUAN, "ty_gia": TY_GIA,
        "sku_mau": {**{k: (v.isoformat() if isinstance(v, date) else v) for k, v in SKU_MAU.items()},
                    "phi_ncc": PHI_NCC},
        "gia_tri_don_aff": GIA_TRI_DON_AFF,
        "kich_ban": [chay_kich_ban(kb, mt) for kb in KICH_BAN],
        "ghi_chu": "MỌI SỐ LÀ GIẢ ĐỊNH, không phải dự báo. " + DONG_KHONG_DAM_BAO,
    }


def _d(x) -> str:
    return "—" if x is None else f"{x:,.0f}".replace(",", ".")


def bang_markdown(kq: dict) -> str:
    L = ["| | " + " | ".join(k["ten"] for k in kq["kich_ban"]) + " |", "|---|---|---|---|"]
    def dong(nhan, f):
        L.append(f"| {nhan} | " + " | ".join(f(k) for k in kq["kich_ban"]) + " |")
    dong("Tỷ lệ hoàn / hủy (dropship)", lambda k: f"{k['gia_dinh']['ty_le_hoan_pct']:g}% / {k['gia_dinh']['ty_le_huy_pct']:g}%")
    dong("ROAS thực (GIẢ ĐỊNH) · ROAS hòa vốn", lambda k: f"{k['gia_dinh']['roas_thuc']:g} · {k['roas_hoa_von']:g}".replace(".", ","))
    dong("LN trước QC / đơn dropship đặt (đ)", lambda k: _d(k["ln_truoc_qc_moi_don_dropship"]))
    dong("Hoa hồng affiliate (% · thực nhận/đơn, đ)", lambda k: f"{k['gia_dinh']['hoa_hong_aff_pct']:g}% · {_d(k['hoa_hong_thuc_nhan_moi_don_aff'])}")
    dong("Tổng đơn 8 tuần: dropship · affiliate", lambda k: f"{k['tong_don_dropship']} · {k['tong_don_affiliate']}")
    dong("Lãi từng tuần 1→8 (nghìn đ)", lambda k: " / ".join(f"{t['lai_tuan'] / 1000:.0f}" for t in k["tuan"]))
    dong("**Lãi cộng dồn 8 tuần (đ)**", lambda k: f"**{_d(k['lai_8_tuan'])}**")
    dong("**Lãi 4 tuần cuối → cổng Đợt 1**", lambda k: f"**{_d(k['lai_4_tuan_cuoi'])} → {'ĐẠT' if k['dat_cong_dot1'] else 'KHÔNG ĐẠT'}**")
    dong("Hòa vốn 19,5 tr chỉ bằng dropship (đơn / 8 tuần · / tuần)", lambda k: f"{_d(k['hoa_von_don_dropship_8_tuan'])} · " + f"{k['hoa_von_don_dropship_moi_tuan']:g}".replace(".", ","))
    dong("Hòa vốn chỉ bằng affiliate (đơn / 8 tuần · / tuần)", lambda k: f"{_d(k['hoa_von_don_affiliate_8_tuan'])} · " + f"{k['hoa_von_don_affiliate_moi_tuan']:g}".replace(".", ","))
    return "\n".join(L)


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    kq = chay_tat_ca()
    if "--json" in argv:
        print(json.dumps(kq, ensure_ascii=False, indent=2))
    else:
        print("BẢNG 3 KỊCH BẢN 8 TUẦN — MỌI SỐ LÀ GIẢ ĐỊNH\n")
        print(bang_markdown(kq))
        print("\n" + kq["ghi_chu"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
