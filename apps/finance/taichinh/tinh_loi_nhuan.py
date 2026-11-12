"""Máy tính lợi nhuận ròng mỗi đơn (1 SKU / đơn). Công thức theo `bao-cao/dot0/p4-tai-chinh.md` mục 5.

Ký hiệu: Rev = giá bán − giảm giá shop (voucher shop); CM = lợi nhuận đóng góp đơn giao thành công;
LN_truoc_QC = (1−r)·CM − r·(chi phí mỗi đơn hoàn); LN = LN_truoc_QC − quảng cáo% · Rev.
Tất cả số tiền là VND / đơn. Tỷ lệ nhập theo % (vd. 6 nghĩa là 6%).
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict, replace
from datetime import date
from typing import Optional

from .bang_phi import BangPhi, DongPhi, ThieuDuLieu, bo_dau

DONG_KHONG_DAM_BAO = ("Số đầu vào (giá vốn, giá bán, tỷ lệ hoàn, quảng cáo…) là GIẢ ĐỊNH do người dùng nhập. "
                      "Không phải khuyến nghị đầu tư / không đảm bảo lợi nhuận.")

CANH_BAO_HA_TANG = ("Phí hạ tầng Shopee 3.000đ/đơn: nguồn chính thức (Shopee Uni bài 25329) + Sapo + Báo Pháp Luật ghi "
                    "áp dụng; MỘT nguồn (ai-hay) nói CHỈ áp dụng Shopee Mall → mâu thuẫn, chưa kiểm trên Kênh Người Bán. "
                    "Công cụ vẫn tính 3.000đ (thận trọng).")

SAN = {
    "shopee": {
        "ten": "Shopee",
        "phi_nganh": "phi_co_dinh",
        "phi_gd": ("phi_xu_ly_giao_dich", "Tat ca (nguoi ban thuong)"),
        "phi_don": ("phi_ha_tang", "Tat ca"),
        "voucher_san": ("phi_dich_vu_goi_voucher_xtra", "Tat ca (neu tham gia)"),
        "ship_tra": ("phi_van_chuyen_tra_hang_nguoi_ban_chiu", "Tat ca"),
        # Shopee bài 10626: "Trả hàng & Hoàn tiền" không tính phí cố định / dịch vụ / xử lý giao dịch.
        # Phí hạ tầng khi trả hàng: CHƯA XÁC MINH -> theo công thức gốc, không tính.
        "phi_don_mat_khi_hoan": False,
    },
    "tiktok": {
        "ten": "TikTok Shop",
        "phi_nganh": "phi_hoa_hong_nen_tang",
        "nganh_mac_dinh": "Muc mac dinh (nganh cap 3 khong liet ke)",
        "phi_gd": ("phi_giao_dich", "Tat ca"),
        "phi_don": ("phi_xu_ly_don_hang", "Tat ca"),
        "voucher_san": ("phi_dich_vu_Voucher_Extra_VXP", "Tat ca (neu tham gia)"),
        "ship_tra": None,
        # Bảng phí dòng phi_xu_ly_don_hang: "KHONG hoan lai neu don da giao roi moi hoan/tra" [CAO]
        "phi_don_mat_khi_hoan": True,
    },
}


def chuan_san(san: str) -> str:
    s = bo_dau(san).replace(" ", "")
    if s.startswith("shopee"):
        return "shopee"
    if s.startswith("tiktok"):
        return "tiktok"
    raise ThieuDuLieu(f"sàn '{san}' chưa hỗ trợ (chỉ Shopee, TikTok Shop)")


@dataclass
class DauVao:
    san: str
    nganh: str
    gia_ban: float                      # giá niêm yết P (đ)
    gia_von: float                      # COGS gồm nhập + bao bì tiêu hao (đ)
    ngay_ban: date = field(default_factory=date.today)
    giam_gia_shop: float = 0.0          # voucher / mã giảm do shop chịu Ds (đ)
    dong_goi: float = 0.0               # B (đ)
    ship_shop_chiu: float = 0.0         # Sx: freeship shop tài trợ, vượt cân (đ)
    tham_gia_voucher_san: bool = False  # Voucher Xtra (Shopee) / VXP (TikTok)
    hoa_hong_aff_shop_tra: float = 0.0  # a: % shop trả cho affiliate / creator
    quang_cao_pct: float = 0.0          # % Rev chi quảng cáo
    ty_le_hoan: float = 0.0             # r: % đơn "Trả hàng & Hoàn tiền"
    ship_tra_hang: Optional[float] = None  # Sret (đ); None = trần trong bảng phí (Shopee 40.000)
    ty_le_hong_hang_hoan: float = 30.0  # d: % hàng hoàn không bán lại được — GIẢ ĐỊNH
    thue_gtgt: Optional[float] = None   # None = lấy bảng phí (1%)
    thue_tncn: Optional[float] = None   # None = lấy bảng phí (0,5%)
    che_do_khoang: str = "cao"          # thap / giua / cao cho mức dạng khoảng
    phi_nganh_tu_nhap: Optional[float] = None  # ghi đè phí ngành (%), vd. đã tra PDF cấp 3
    shop_moi_mien_phi_co_dinh: bool = False    # Shopee: miễn phí cố định 30 ngày / 200 đơn (từ 01/11/2026)
    tinh_phi_ha_tang: bool = True       # Shopee: False để xem kịch bản "chỉ Mall mới thu"
    # so sánh với làm affiliate (không nhập hàng, nhận hoa hồng trên Rev)
    hoa_hong_aff_nhan: Optional[float] = None  # % hoa hồng bạn NHẬN nếu làm affiliate — GIẢ ĐỊNH, người dùng nhập
    thue_aff: float = 0.0               # % thuế bị khấu trừ trên hoa hồng affiliate — CHƯA XÁC MINH


@dataclass
class DongChiPhi:
    ten: str
    so_tien: float
    ty_le: Optional[float] = None
    nguon: str = ""
    do_tin_cay: str = ""
    hieu_luc: str = ""


@dataclass
class KetQua:
    san: str
    nganh: str
    ngay_ban: str
    rev: float
    chi_phi: list[DongChiPhi]
    cm: float
    chi_phi_moi_don_hoan: float
    ln_truoc_qc: float
    quang_cao: float
    ln: float
    bien_rong: float
    roas_hoa_von: Optional[float]
    gia_hoa_von: Optional[float]
    gia_hoa_von_truoc_qc: Optional[float]
    thue_tam_khau_tru: float
    affiliate: Optional[dict]
    canh_bao: list[str]
    khong_dam_bao: str = DONG_KHONG_DAM_BAO

    def to_dict(self) -> dict:
        return asdict(self)


def _hieu_luc(d: DongPhi) -> str:
    if d.tu_ngay and d.den_ngay:
        return f"{d.tu_ngay.isoformat()} → {d.den_ngay.isoformat()}"
    if d.tu_ngay:
        return f"từ {d.tu_ngay.isoformat()}"
    if d.den_ngay:
        return f"đến {d.den_ngay.isoformat()}"
    return "CHƯA XÁC MINH"


def _ghi_canh_bao(cb: list[str], ten: str, d: DongPhi):
    for c in d.canh_bao:
        cb.append(f"{ten}: {c}")
    if d.do_tin_cay.upper() not in ("CAO",):
        cb.append(f"{ten}: độ tin cậy {d.do_tin_cay or 'không ghi'}")


class MayTinh:
    def __init__(self, bang_phi: Optional[BangPhi] = None):
        self.bp = bang_phi or BangPhi()

    def _ty_le(self, san_csv: str, loai: str, nganh: str, ngay: date, che_do: str,
               ten: str, cb: list[str]) -> tuple[float, DongPhi]:
        d = self.bp.tra(san_csv, loai, nganh, ngay)
        v = d.muc.chon(che_do)
        if d.muc.la_khoang:
            cb.append(f"{ten}: bảng phí ghi khoảng {d.muc.thap:g}–{d.muc.cao:g}% (ngành '{d.nganh}'), "
                      f"đang dùng mức '{che_do}' = {v:g}%. Tra PDF ngành cấp 3 để có mức chính xác.")
        _ghi_canh_bao(cb, ten, d)
        return v, d

    def tinh(self, dv: DauVao, tim_hoa_von: bool = True) -> KetQua:
        cb: list[str] = []
        ma = chuan_san(dv.san)
        cfg = SAN[ma]
        san_csv = cfg["ten"]
        ngay = dv.ngay_ban
        if dv.gia_ban is None or dv.gia_von is None:
            raise ThieuDuLieu("thiếu giá bán hoặc giá vốn")
        for ten, v in (("giá bán", dv.gia_ban), ("giá vốn", dv.gia_von), ("giảm giá shop", dv.giam_gia_shop),
                       ("đóng gói", dv.dong_goi), ("ship shop chịu", dv.ship_shop_chiu)):
            if v < 0:
                raise ThieuDuLieu(f"{ten} không được âm")
        for ten, v in (("tỷ lệ hoàn", dv.ty_le_hoan), ("quảng cáo %", dv.quang_cao_pct),
                       ("tỷ lệ hỏng hàng hoàn", dv.ty_le_hong_hang_hoan), ("hoa hồng affiliate", dv.hoa_hong_aff_shop_tra)):
            if not 0 <= v <= 100:
                raise ThieuDuLieu(f"{ten} phải trong 0–100 (%), nhận {v}")

        rev = dv.gia_ban - dv.giam_gia_shop
        if rev <= 0:
            raise ThieuDuLieu("giá bán sau giảm giá shop phải > 0")

        # ---- phí ngành ----
        nganh_tra = dv.nganh
        if ma == "tiktok" and not dv.nganh.strip():
            nganh_tra = cfg["nganh_mac_dinh"]
        if dv.phi_nganh_tu_nhap is not None:
            f_pct = dv.phi_nganh_tu_nhap
            d_f = None
            ten_nganh = dv.nganh
            cb.append(f"Phí ngành do người dùng nhập tay ({f_pct:g}%) — không lấy từ bảng phí")
        else:
            f_pct, d_f = self._ty_le(san_csv, cfg["phi_nganh"], nganh_tra, ngay, dv.che_do_khoang,
                                     "Phí ngành", cb)
            ten_nganh = d_f.nganh
        if ma == "shopee" and dv.shop_moi_mien_phi_co_dinh:
            d_uu = self.bp.dong_dau("Shopee", "uu_dai_nguoi_ban_moi")
            if d_uu and d_uu.ap_dung(ngay):
                f_pct = 0.0
                cb.append("Đang áp dụng miễn phí cố định shop mới (30 ngày, tối đa 200 đơn thành công, sản phẩm "
                          "đầu tiên đăng từ 01/11/2026). Hết ưu đãi thì lợi nhuận GIẢM — chạy lại không có cờ này.")
            else:
                cb.append("Cờ miễn phí cố định shop mới bị bỏ qua: ngày bán trước 01/11/2026")

        chi_phi: list[DongChiPhi] = []

        def them(ten, so_tien, ty_le=None, d: Optional[DongPhi] = None):
            chi_phi.append(DongChiPhi(ten, round(so_tien, 2), ty_le,
                                      d.nguon if d else "người dùng nhập (GIẢ ĐỊNH)",
                                      d.do_tin_cay if d else "", _hieu_luc(d) if d else ""))

        them("Giá vốn", dv.gia_von)
        if dv.dong_goi:
            them("Đóng gói", dv.dong_goi)
        if dv.ship_shop_chiu:
            them("Ship shop chịu", dv.ship_shop_chiu)
        them(f"Phí ngành ({cfg['phi_nganh']})", f_pct / 100 * rev, f_pct, d_f)

        t_pct, d_t = self._ty_le(san_csv, cfg["phi_gd"][0], cfg["phi_gd"][1], ngay, "cao", "Phí giao dịch", cb)
        them(f"Phí giao dịch ({cfg['phi_gd'][0]})", t_pct / 100 * rev, t_pct, d_t)

        d_h = self.bp.tra(san_csv, cfg["phi_don"][0], cfg["phi_don"][1], ngay)
        _ghi_canh_bao(cb, "Phí mỗi đơn", d_h)
        H = d_h.muc.cao
        if ma == "shopee":
            if dv.tinh_phi_ha_tang:
                cb.append(CANH_BAO_HA_TANG)
            else:
                cb.append("Đang BỎ phí hạ tầng 3.000đ (kịch bản 'chỉ Mall mới thu' — CHƯA XÁC MINH, không thận trọng)")
                H = 0.0
        them(f"Phí mỗi đơn ({cfg['phi_don'][0]})", H, None, d_h)

        v_tien = 0.0
        if dv.tham_gia_voucher_san:
            v_pct, d_v = self._ty_le(san_csv, cfg["voucher_san"][0], cfg["voucher_san"][1], ngay, "cao",
                                     "Voucher sàn", cb)
            v_tien = v_pct / 100 * rev
            if d_v.muc.tran_vnd is not None:
                v_tien = min(v_tien, d_v.muc.tran_vnd)
            them(f"Voucher sàn ({cfg['voucher_san'][0]})", v_tien, v_pct, d_v)
            if ma == "shopee":
                cb.append("Voucher Xtra: cơ sở tính (trước/sau KM người bán) CHƯA XÁC MINH — công cụ tính trên Rev")

        a_tien = dv.hoa_hong_aff_shop_tra / 100 * rev
        if a_tien:
            them("Hoa hồng affiliate shop trả", a_tien, dv.hoa_hong_aff_shop_tra)

        d_gtgt = self.bp.tra("Chung (san khau tru)", "thue_khau_tru_GTGT", "Hang hoa", ngay)
        d_tncn = self.bp.tra("Chung (san khau tru)", "thue_khau_tru_TNCN", "Hang hoa", ngay)
        g = d_gtgt.muc.cao if dv.thue_gtgt is None else dv.thue_gtgt
        p = d_tncn.muc.cao if dv.thue_tncn is None else dv.thue_tncn
        k_pct = g + p
        # Doanh thu tính thuế = giá hàng − mã người bán − phần đồng tài trợ của người bán (bảng phí dòng 77);
        # công cụ chưa tách phần đồng tài trợ -> dùng Rev.
        k_tien = k_pct / 100 * rev
        them(f"Thuế sàn khấu trừ (GTGT {g:g}% + TNCN {p:g}%)", k_tien, k_pct, d_gtgt)

        tong = sum(c.so_tien for c in chi_phi)
        cm = rev - tong

        # ---- hoàn hàng ----
        r = dv.ty_le_hoan / 100
        d_ = dv.ty_le_hong_hang_hoan / 100
        if dv.ship_tra_hang is not None:
            sret = dv.ship_tra_hang
        elif cfg["ship_tra"]:
            d_s = self.bp.tra(san_csv, cfg["ship_tra"][0], cfg["ship_tra"][1], ngay)
            sret = d_s.muc.cao
        else:
            sret = 0.0
            if r > 0:
                cb.append("TikTok: phí ship trả hàng shop chịu CHƯA XÁC MINH trong bảng phí — đang tính 0đ; "
                          "nhập --ship-tra-hang để thận trọng")
        chi_hoan = dv.dong_goi + dv.ship_shop_chiu + sret + d_ * dv.gia_von
        if cfg["phi_don_mat_khi_hoan"]:
            chi_hoan += H
        if r > 0:
            cb.append(f"Hoàn hàng: tỷ lệ hoàn {dv.ty_le_hoan:g}% và hỏng {dv.ty_le_hong_hang_hoan:g}% là GIẢ ĐỊNH "
                      "(tỷ lệ hoàn điển hình CHƯA XÁC MINH)")
        ln_truoc = (1 - r) * cm - r * chi_hoan
        qc = dv.quang_cao_pct / 100 * rev
        ln = ln_truoc - qc

        roas = rev / ln_truoc if ln_truoc > 0 else None
        if roas is None:
            cb.append("LỖ ngay cả trước quảng cáo → không có ROAS hòa vốn; không nên chạy quảng cáo SKU này")

        # ---- giá hòa vốn: tìm P để LN = 0, giữ nguyên giảm giá shop & các tỷ lệ ----
        gia_hv = self._gia_hoa_von(dv, qc_on=True) if tim_hoa_von else None
        gia_hv_tqc = self._gia_hoa_von(dv, qc_on=False) if tim_hoa_von else None

        # ---- cảnh báo theo ngày ----
        d_vat = self.bp.dong_dau("Shopee", "GTGT_tren_phi_san")
        if d_vat and d_vat.den_ngay and ngay > d_vat.den_ngay:
            cb.append(f"Ngày bán sau {d_vat.den_ngay.isoformat()}: GTGT 8% trên phí sàn hết hạn; nếu về 10% phí đã gồm "
                      "thuế có thể tăng ~×1,10/1,08 (+1,85% tương đối) — CHƯA XÁC MINH, cần bảng phí v2")
        if ma == "tiktok":
            cb.append("TikTok: cơ sở phí giao dịch gồm cả trợ giá sàn + ship khách trả; công cụ tính trên Rev "
                      "(ship khách trả coi như triệt tiêu)")
        cb.append("Thuế khấu trừ 1,5%: nếu doanh thu năm ≤ 1 tỷ thì là tiền TẠM khấu trừ, có thể được hoàn — "
                  "công cụ vẫn trừ (thận trọng). Hỏi kế toán (mục 7 p4-tai-chinh.md)")

        aff = None
        if dv.hoa_hong_aff_nhan is not None:
            hh = (1 - r) * dv.hoa_hong_aff_nhan / 100 * rev * (1 - dv.thue_aff / 100)
            ln_aff = hh - qc
            aff = {
                "hoa_hong_nhan_pct": dv.hoa_hong_aff_nhan,
                "hoa_hong_ky_vong_moi_don": round(hh, 2),
                "quang_cao": round(qc, 2),
                "ln_affiliate": round(ln_aff, 2),
                "roas_hoa_von_affiliate": round(rev / hh, 4) if hh > 0 else None,
                "von_hang_moi_don_nhap_truc_tiep": dv.gia_von,
                "von_hang_moi_don_affiliate": 0,
                "chenh_lech_nhap_truc_tiep_tru_affiliate": round(ln - ln_aff, 2),
            }
            cb.append("So sánh affiliate: tỷ lệ hoa hồng nhận là GIẢ ĐỊNH; thuế khấu trừ trên thu nhập affiliate "
                      "CHƯA XÁC MINH (mặc định 0%, nhập --thue-aff). Hoa hồng chỉ tính cho đơn không hoàn.")

        return KetQua(
            san=san_csv, nganh=ten_nganh, ngay_ban=ngay.isoformat(), rev=rev, chi_phi=chi_phi, cm=round(cm, 2),
            chi_phi_moi_don_hoan=round(chi_hoan, 2), ln_truoc_qc=round(ln_truoc, 2), quang_cao=round(qc, 2),
            ln=round(ln, 2), bien_rong=round(ln / rev, 6), roas_hoa_von=round(roas, 4) if roas else None,
            gia_hoa_von=gia_hv, gia_hoa_von_truoc_qc=gia_hv_tqc,
            thue_tam_khau_tru=round((1 - r) * k_tien, 2), affiliate=aff, canh_bao=cb,
        )

    def _gia_hoa_von(self, dv: DauVao, qc_on: bool) -> Optional[float]:
        lo = dv.giam_gia_shop + 1.0
        hi = max(dv.gia_ban, dv.gia_von, 1000.0) * 2
        f = lambda P: self._ln(dv, P, qc_on)
        try:
            for _ in range(40):
                if f(hi) > 0:
                    break
                hi *= 2
            else:
                return None  # tổng tỷ lệ phí ≥ 100% → không có giá hòa vốn
            if f(lo) >= 0:
                return round(lo, 0)
            for _ in range(100):
                mid = (lo + hi) / 2
                if f(mid) >= 0:
                    hi = mid
                else:
                    lo = mid
            return round(hi, 0)
        except ThieuDuLieu:
            return None

    def _ln(self, dv: DauVao, gia: float, qc_on: bool) -> float:
        """LN (sau / trước QC) tại giá `gia`, giữ nguyên mọi tham số khác."""
        x = replace(dv, gia_ban=gia, hoa_hong_aff_nhan=None,
                    quang_cao_pct=dv.quang_cao_pct if qc_on else 0.0)
        return self.tinh(x, tim_hoa_von=False).ln
