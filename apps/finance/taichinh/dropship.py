"""Dropship: shop của mình bán, nhà cung cấp (NCC) giao hàng. Thêm vào máy tính mỗi đơn:
phí NCC, chi phí đơn hủy, tiền ứng trước cho NCC và chu kỳ tiền sàn trả về.

Mô hình (mỗi ĐƠN ĐẶT, 1 SKU):
- Giá vốn = giá NCC (tiền hàng). Phí NCC (dịch vụ / đóng gói NCC thu mỗi đơn gửi đi) tính như đóng gói:
  mất cả khi đơn giao thành công lẫn khi bị trả hàng.
- h = tỷ lệ HỦY (trước khi giao — sàn không thu phí). Mỗi đơn hủy tốn `chi_phi_moi_don_huy`
  (mặc định = phí NCC: GIẢ ĐỊNH NCC hoàn tiền hàng nhưng giữ phí).
- LN mỗi đơn đặt = (1 − h)·LN_đơn_không_hủy − h·chi_phi_moi_don_huy  (LN_đơn_không_hủy lấy từ MayTinh, đã gồm hoàn r).

Chu kỳ tiền về (`bao-cao/dot0/p4-tai-chinh.md` §4, [CAO]):
- Shopee: tiền vào số dư khi khách bấm "Đã nhận hàng" hoặc NGÀY THỨ 4 sau giao thành công (công cụ dùng 4 — thận trọng);
  đơn nghi gian lận tới 15 ngày; rút tay về ngân hàng trong 24 giờ (1 ngày).
- TikTok Shop: chờ 8 ngày (shop mới), 3 ngày (đã qua giai đoạn shop mới), 1 ngày (Mall), 15 ngày (rủi ro); rút ~24 giờ.
Số ngày giao hàng là GIẢ ĐỊNH (người dùng nhập).
"""
from __future__ import annotations

from dataclasses import dataclass, asdict, field, replace
from typing import Optional

from .bang_phi import ThieuDuLieu
from .tinh_loi_nhuan import DauVao, KetQua, MayTinh, chuan_san, DONG_KHONG_DAM_BAO

NGUON_TIEN_VE = "bao-cao/dot0/p4-tai-chinh.md §4 (Shopee Uni bài 234; TikTok knowledge_id=6091769578850065) [CAO]"

# (ngày chờ sau giao thành công, ngày rút về ngân hàng)
CHU_KY = {
    ("shopee", "thuong"): (4, 1),
    ("shopee", "moi"): (4, 1),
    ("shopee", "rui_ro"): (15, 1),
    ("tiktok", "moi"): (8, 1),
    ("tiktok", "thuong"): (3, 1),
    ("tiktok", "mall"): (1, 1),
    ("tiktok", "rui_ro"): (15, 1),
}


def chu_ky_tien_ve(san: str, loai_shop: str = "moi") -> tuple[int, int]:
    """Trả (số ngày chờ sau giao thành công, số ngày rút về ngân hàng)."""
    k = (chuan_san(san), loai_shop)
    if k not in CHU_KY:
        raise ThieuDuLieu(f"chưa có chu kỳ tiền về cho {k}; chọn trong {sorted(CHU_KY)}")
    return CHU_KY[k]


@dataclass
class KetQuaDropship:
    don: KetQua                      # kết quả máy tính mỗi đơn KHÔNG hủy (đã gồm hoàn r)
    gia_ncc: float
    phi_ncc: float
    ty_le_huy: float
    chi_phi_moi_don_huy: float
    ln_moi_don_dat: float
    ln_truoc_qc_moi_don_dat: float
    chi_ra_moi_don_dat: float        # tiền trả NCC + quảng cáo, lúc đặt đơn
    tien_ve_moi_don_dat: float       # tiền sàn trả về (sau phí, thuế, ship trả hàng), sau chu kỳ tiền về
    ngay_cho: int
    ngay_rut: int
    ngay_giao: int
    ngay_tre: int                    # giao + chờ + rút
    canh_bao: list[str] = field(default_factory=list)
    khong_dam_bao: str = DONG_KHONG_DAM_BAO

    def to_dict(self) -> dict:
        return asdict(self)


def _tien_san_tra_moi_don_giao(kq: KetQua) -> float:
    """Tiền sàn trả cho 1 đơn giao thành công = Rev − phí sàn − voucher sàn − affiliate − thuế khấu trừ
    (= Rev − các dòng chi phí không phải giá vốn / đóng gói / ship shop chịu)."""
    ngoai_san = ("Giá vốn", "Đóng gói", "Ship shop chịu")
    return kq.rev - sum(c.so_tien for c in kq.chi_phi if c.ten not in ngoai_san)


def tinh_dropship(dv: DauVao, phi_ncc: float = 0.0, ty_le_huy: float = 0.0,
                  chi_phi_moi_don_huy: Optional[float] = None, ngay_giao: int = 3, loai_shop: str = "moi",
                  mt: Optional[MayTinh] = None, tim_hoa_von: bool = True) -> KetQuaDropship:
    """`dv.gia_von` = giá NCC (tiền hàng). Mọi số là GIẢ ĐỊNH người dùng nhập."""
    if phi_ncc < 0 or ngay_giao < 0:
        raise ThieuDuLieu("phí NCC / số ngày giao không được âm")
    if not 0 <= ty_le_huy < 100:
        raise ThieuDuLieu(f"tỷ lệ hủy phải trong 0–<100 (%), nhận {ty_le_huy}")
    mt = mt or MayTinh()
    c_huy = phi_ncc if chi_phi_moi_don_huy is None else chi_phi_moi_don_huy
    if c_huy < 0:
        raise ThieuDuLieu("chi phí đơn hủy không được âm")
    kq = mt.tinh(replace(dv, dong_goi=dv.dong_goi + phi_ncc), tim_hoa_von=tim_hoa_von)
    h = ty_le_huy / 100
    r = dv.ty_le_hoan / 100
    ln_dat = (1 - h) * kq.ln - h * c_huy
    ln_tqc_dat = (1 - h) * kq.ln_truoc_qc - h * c_huy

    ngay_cho, ngay_rut = chu_ky_tien_ve(dv.san, loai_shop)
    # Khoản sàn trừ vào số dư khi đơn bị trả = ship trả hàng (+ phí xử lý đơn TikTok không hoàn)
    #   = chi phí mỗi đơn hoàn − phần tự trả từ túi (đóng gói + phí NCC + ship shop chịu) − hàng hỏng (không phải tiền mặt)
    tru_khi_hoan = (kq.chi_phi_moi_don_hoan - (dv.dong_goi + phi_ncc + dv.ship_shop_chiu)
                    - dv.ty_le_hong_hang_hoan / 100 * dv.gia_von)
    tien_ve = (1 - h) * ((1 - r) * _tien_san_tra_moi_don_giao(kq) - r * tru_khi_hoan)
    chi_ra = (1 - h) * (dv.gia_von + phi_ncc + dv.dong_goi + dv.ship_shop_chiu + kq.quang_cao) + h * c_huy

    cb = [f"Dropship: giá NCC, phí NCC {phi_ncc:,.0f}đ, tỷ lệ hủy {ty_le_huy:g}%, chi phí mỗi đơn hủy {c_huy:,.0f}đ, "
          f"giao {ngay_giao} ngày là GIẢ ĐỊNH",
          f"Tiền về: chờ {ngay_cho} ngày sau giao + rút {ngay_rut} ngày (shop '{loai_shop}') — {NGUON_TIEN_VE}",
          "Hàng bị trả về địa chỉ shop (không về NCC) — NCC có nhận lại / hoàn tiền hàng trả không: CHƯA XÁC MINH, "
          "tùy hợp đồng NCC",
          "Quảng cáo tính trên đơn không hủy; tiền quảng cáo nạp trước được coi là chi lúc đặt đơn",
          "Tiền mặt ≠ lãi: hàng hoàn còn bán được nằm thành tồn kho (đã trả NCC, chưa thu lại tiền)"]
    if ln_dat < 0:
        cb.append("LỖ mỗi đơn đặt sau hủy / hoàn")
    return KetQuaDropship(
        don=kq, gia_ncc=dv.gia_von, phi_ncc=phi_ncc, ty_le_huy=ty_le_huy, chi_phi_moi_don_huy=c_huy,
        ln_moi_don_dat=round(ln_dat, 2), ln_truoc_qc_moi_don_dat=round(ln_tqc_dat, 2),
        chi_ra_moi_don_dat=round(chi_ra, 2), tien_ve_moi_don_dat=round(tien_ve, 2),
        ngay_cho=ngay_cho, ngay_rut=ngay_rut, ngay_giao=ngay_giao, ngay_tre=ngay_giao + ngay_cho + ngay_rut,
        canh_bao=cb,
    )


def von_ung_truoc(don_moi_ngay: float, chi_ra_moi_don: float, tien_ve_moi_don: float, ngay_tre: int,
                  so_ngay: int = 56) -> dict:
    """Mô phỏng tiền mặt theo ngày: mỗi ngày đặt `don_moi_ngay` đơn, trả ngay `chi_ra_moi_don`/đơn,
    nhận `tien_ve_moi_don`/đơn sau `ngay_tre` ngày. Trả vốn ứng trước cần có (âm sâu nhất của số dư cộng dồn).

    Trạng thái ổn định (tiền về ≥ chi ra): vốn cần = đơn/ngày × chi ra/đơn × ngày trễ.
    """
    if don_moi_ngay < 0 or chi_ra_moi_don < 0 or ngay_tre < 0 or so_ngay < 1:
        raise ThieuDuLieu("đầu vào vốn ứng trước không hợp lệ")
    so_du = 0.0
    thap_nhat = 0.0
    ngay_thap_nhat = None
    ngay_hoan_von = None
    for t in range(so_ngay):
        so_du -= don_moi_ngay * chi_ra_moi_don
        if t >= ngay_tre:
            so_du += don_moi_ngay * tien_ve_moi_don
        if so_du < thap_nhat - 1e-9:
            thap_nhat, ngay_thap_nhat = so_du, t
        if ngay_hoan_von is None and t > 0 and so_du >= 0 and thap_nhat < 0:
            ngay_hoan_von = t
    return {
        "von_ung_truoc_can": round(-thap_nhat, 2),
        "ngay_am_sau_nhat": ngay_thap_nhat,
        "ngay_so_du_cong_don_ve_0": ngay_hoan_von,
        "so_du_cuoi_ky": round(so_du, 2),
        "so_ngay_mo_phong": so_ngay,
        "ghi_chu": "GIẢ ĐỊNH số đơn đều mỗi ngày; chưa tính chi phí cố định (công cụ, hàng mẫu). " + DONG_KHONG_DAM_BAO,
    }
