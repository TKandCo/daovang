"""Affiliate: hoa hồng THỰC NHẬN sau phí nền tảng, thuế khấu trừ và chi phí nội dung.

Công thức (giao việc P4-D1A, nguồn `bao-cao/dot0/p1-radar.md` mục Shopee Affiliate):
    thực nhận = hoa hồng × (1 − 0,98%) × (1 − 10% nếu khoản thanh toán ≥ 250.000 đ) − chi phí nội dung

Nguồn [CAO]: bài Shopee 09/07/2026 https://shopee.vn/blog/?p=190331 —
phí 0,98% trên tổng hoa hồng từ 16/05/2025; khấu trừ TNCN 10% với mỗi khoản thanh toán ≥ 250.000 đ từ 20/11/2025.
TikTok Shop Affiliate: phí / thuế CHƯA XÁC MINH → công cụ dùng tạm luật Shopee (thận trọng) và cảnh báo.
Tiền: VND. Tỷ lệ nhập theo % (vd. 10 nghĩa là 10%).
"""
from __future__ import annotations

from dataclasses import dataclass, asdict, field
from datetime import date
from typing import Optional

from .bang_phi import ThieuDuLieu
from .tinh_loi_nhuan import DONG_KHONG_DAM_BAO

NGUON_SHOPEE_AFF = "https://shopee.vn/blog/?p=190331 (bài Shopee 09/07/2026, qua p1-radar.md) [CAO]"
PHI_NEN_TANG_PCT = 0.98           # % trên tổng hoa hồng, từ 16/05/2025
PHI_NEN_TANG_TU = date(2025, 5, 16)
THUE_TNCN_PCT = 10.0              # % khấu trừ khi một khoản thanh toán ≥ ngưỡng, từ 20/11/2025
THUE_TU = date(2025, 11, 20)
NGUONG_THUE_VND = 250_000


@dataclass
class KetQuaAffiliate:
    san: str
    hoa_hong_goc: float
    phi_nen_tang: float
    sau_phi: float
    co_khau_tru_thue: bool
    thue_khau_tru: float
    sau_thue: float
    chi_phi_noi_dung: float
    thuc_nhan: float
    canh_bao: list[str] = field(default_factory=list)
    khong_dam_bao: str = DONG_KHONG_DAM_BAO

    def to_dict(self) -> dict:
        return asdict(self)


def hoa_hong_goc_tu_don(gia_tri_don: float, ty_le_hoa_hong: float, so_don: int = 1,
                        ty_le_huy_hoan: float = 0.0) -> float:
    """Hoa hồng gốc kỳ vọng = giá trị đơn × tỷ lệ × số đơn × (1 − tỷ lệ hủy/hoàn). Đơn hủy / hoàn không có hoa hồng.

    Tỷ lệ hoa hồng và tỷ lệ hủy là GIẢ ĐỊNH do người dùng nhập (nguồn mức hoa hồng Shopee 11% / tới 20%: [THẤP]).
    """
    if gia_tri_don < 0 or so_don < 0:
        raise ThieuDuLieu("giá trị đơn / số đơn không được âm")
    for ten, v in (("tỷ lệ hoa hồng", ty_le_hoa_hong), ("tỷ lệ hủy/hoàn", ty_le_huy_hoan)):
        if not 0 <= v <= 100:
            raise ThieuDuLieu(f"{ten} phải trong 0–100 (%), nhận {v}")
    return gia_tri_don * ty_le_hoa_hong / 100 * so_don * (1 - ty_le_huy_hoan / 100)


def thuc_nhan(hoa_hong_goc: float, chi_phi_noi_dung: float = 0.0, san: str = "shopee",
              ngay: Optional[date] = None, nguong_tinh_tren: str = "truoc_phi",
              phi_nen_tang_pct: Optional[float] = None, thue_pct: Optional[float] = None) -> KetQuaAffiliate:
    """Hoa hồng thực nhận của MỘT khoản thanh toán.

    `nguong_tinh_tren`: "truoc_phi" (so 250.000 với hoa hồng gốc — mặc định, thận trọng) hoặc "sau_phi"
    (so với số sau 0,98%). Nguồn không nói rõ → CHƯA XÁC MINH.
    """
    if hoa_hong_goc < 0 or chi_phi_noi_dung < 0:
        raise ThieuDuLieu("hoa hồng / chi phí nội dung không được âm")
    if nguong_tinh_tren not in ("truoc_phi", "sau_phi"):
        raise ThieuDuLieu("nguong_tinh_tren phải là 'truoc_phi' hoặc 'sau_phi'")
    s = san.lower().replace(" ", "")
    if not (s.startswith("shopee") or s.startswith("tiktok")):
        raise ThieuDuLieu(f"sàn '{san}' chưa hỗ trợ")
    cb: list[str] = []
    phi = PHI_NEN_TANG_PCT if phi_nen_tang_pct is None else phi_nen_tang_pct
    thue = THUE_TNCN_PCT if thue_pct is None else thue_pct
    if s.startswith("tiktok"):
        ten_san = "TikTok Shop"
        if phi_nen_tang_pct is None or thue_pct is None:
            cb.append("TikTok Affiliate: phí nền tảng và thuế khấu trừ CHƯA XÁC MINH — đang dùng tạm luật Shopee "
                      "(0,98% + 10% khi ≥ 250.000đ) cho thận trọng; nhập phi_nen_tang_pct / thue_pct khi có nguồn")
    else:
        ten_san = "Shopee"
    if ngay is not None and (ngay < PHI_NEN_TANG_TU or ngay < THUE_TU):
        cb.append("Ngày trước 16/05/2025 / 20/11/2025: mức cũ CHƯA XÁC MINH — công cụ vẫn áp mức hiện hành")

    phi_tien = hoa_hong_goc * phi / 100
    sau_phi = hoa_hong_goc - phi_tien
    so_nguong = hoa_hong_goc if nguong_tinh_tren == "truoc_phi" else sau_phi
    co_thue = so_nguong >= NGUONG_THUE_VND
    thue_tien = sau_phi * thue / 100 if co_thue else 0.0
    sau_thue = sau_phi - thue_tien
    tn = sau_thue - chi_phi_noi_dung

    cb.append(f"Ngưỡng 250.000đ so với hoa hồng {'gốc (trước phí 0,98%)' if nguong_tinh_tren == 'truoc_phi' else 'sau phí 0,98%'}"
              " — nguồn không nói rõ cơ sở, CHƯA XÁC MINH")
    if co_thue:
        cb.append("Thuế 10% bị khấu trừ TRÊN TOÀN KHOẢN (không chỉ phần vượt). Hộ kinh doanh có được khấu trừ theo "
                  "mức khác / được hoàn hay không: CHƯA XÁC MINH — hỏi kế toán")
    elif so_nguong >= 0.9 * NGUONG_THUE_VND:
        cb.append("Khoản sát ngưỡng 250.000đ: vượt ngưỡng thì bị khấu trừ 10% toàn khoản (thực nhận có thể GIẢM khi "
                  "hoa hồng tăng nhẹ). Đây là thuế tạm khấu trừ, không phải lý do để chia nhỏ khoản")
    if tn < 0:
        cb.append("Chi phí nội dung lớn hơn hoa hồng sau thuế → LỖ")
    cb.append(f"Nguồn phí / thuế affiliate: {NGUON_SHOPEE_AFF}")
    return KetQuaAffiliate(
        san=ten_san, hoa_hong_goc=round(hoa_hong_goc, 2), phi_nen_tang=round(phi_tien, 2), sau_phi=round(sau_phi, 2),
        co_khau_tru_thue=co_thue, thue_khau_tru=round(thue_tien, 2), sau_thue=round(sau_thue, 2),
        chi_phi_noi_dung=round(chi_phi_noi_dung, 2), thuc_nhan=round(tn, 2), canh_bao=cb,
    )


def thuc_nhan_tu_don(gia_tri_don: float, ty_le_hoa_hong: float, so_don: int = 1, ty_le_huy_hoan: float = 0.0,
                     chi_phi_noi_dung: float = 0.0, **kw) -> KetQuaAffiliate:
    """Gộp các đơn của MỘT kỳ thanh toán thành một khoản rồi tính thực nhận."""
    goc = hoa_hong_goc_tu_don(gia_tri_don, ty_le_hoa_hong, so_don, ty_le_huy_hoan)
    kq = thuc_nhan(goc, chi_phi_noi_dung, **kw)
    kq.canh_bao.insert(0, "Tỷ lệ hoa hồng, tỷ lệ hủy/hoàn, số đơn là GIẢ ĐỊNH; lịch thanh toán hoa hồng (gộp theo tháng?) "
                          "CHƯA XÁC MINH — công cụ coi cả kỳ là MỘT khoản")
    return kq
