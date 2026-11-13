"""Dòng lệnh: python3 -m taichinh --san shopee --nganh "Sac dep" --gia-ban 250000 --gia-von 95000 ...

Chạy từ thư mục apps/finance. Xem: python3 -m taichinh --help
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date

from .bang_phi import BANG_PHI_MAC_DINH, BangPhi, ThieuDuLieu
from .tinh_loi_nhuan import SAN, DauVao, KetQua, MayTinh, chuan_san


def _vnd(x) -> str:
    return "—" if x is None else f"{x:,.0f}".replace(",", ".") + " đ"


def _pct(x) -> str:
    return f"{x * 100:.2f}".replace(".", ",") + "%"


def _so(x, n=2) -> str:
    return "—" if x is None else f"{x:.{n}f}".replace(".", ",")


def in_ket_qua(kq: KetQua) -> str:
    L = []
    L.append(f"=== {kq.san} · ngành: {kq.nganh} · ngày bán {kq.ngay_ban} ===")
    L.append(f"Doanh thu đơn (giá bán − giảm giá shop): {_vnd(kq.rev)}")
    L.append("Chi phí mỗi đơn giao thành công:")
    for c in kq.chi_phi:
        tl = f" ({_so(c.ty_le)}%)" if c.ty_le is not None else ""
        ng = f"  [nguồn: {c.nguon} · {c.do_tin_cay} · {c.hieu_luc}]" if c.do_tin_cay else ""
        L.append(f"  - {c.ten}{tl}: {_vnd(c.so_tien)}{ng}")
    L.append(f"Tổng phí sàn + affiliate / doanh thu đơn (CHƯA gồm thuế khấu trừ): {_pct(kq.ty_le_phi_san_aff_chua_thue)}"
             f" · GỒM thuế khấu trừ: {_pct(kq.ty_le_phi_gom_thue_khau_tru)}")
    L.append(f"Lợi nhuận đóng góp đơn thành công (CM): {_vnd(kq.cm)}")
    L.append(f"Chi phí mỗi đơn bị hoàn: {_vnd(kq.chi_phi_moi_don_hoan)}")
    L.append(f"Lợi nhuận trước quảng cáo (đã tính tỷ lệ hoàn): {_vnd(kq.ln_truoc_qc)}")
    L.append(f"Quảng cáo: {_vnd(kq.quang_cao)}")
    L.append(f">>> LỢI NHUẬN RÒNG / ĐƠN: {_vnd(kq.ln)} · BIÊN RÒNG: {_pct(kq.bien_rong)} (trên doanh thu đơn)")
    L.append(f">>> ROAS HÒA VỐN: {_so(kq.roas_hoa_von)}  (ROAS thực thấp hơn số này = quảng cáo lỗ)")
    L.append(f">>> GIÁ BÁN HÒA VỐN: {_vnd(kq.gia_hoa_von)} (gồm quảng cáo) · {_vnd(kq.gia_hoa_von_truoc_qc)} (không quảng cáo)")
    L.append(f"Thuế tạm khấu trừ kỳ vọng / đơn (có thể được hoàn nếu doanh thu năm ≤ 1 tỷ): {_vnd(kq.thue_tam_khau_tru)}")
    if kq.affiliate:
        a = kq.affiliate
        L.append("--- So sánh: NHẬP TRỰC TIẾP vs LÀM AFFILIATE (cùng giá bán) ---")
        L.append(f"  Nhập trực tiếp: LN {_vnd(kq.ln)} / đơn · vốn hàng {_vnd(a['von_hang_moi_don_nhap_truc_tiep'])} / đơn")
        L.append(f"  Affiliate ({_so(a['hoa_hong_nhan_pct'])}% hoa hồng): LN {_vnd(a['ln_affiliate'])} / đơn · "
                 f"vốn hàng 0 đ · ROAS hòa vốn {_so(a['roas_hoa_von_affiliate'])}")
        L.append(f"  Chênh lệch (nhập trực tiếp − affiliate): {_vnd(a['chenh_lech_nhap_truc_tiep_tru_affiliate'])}")
    L.append("CẢNH BÁO:")
    for c in kq.canh_bao:
        L.append(f"  ! {c}")
    L.append(kq.khong_dam_bao)
    return "\n".join(L)


def tao_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="python3 -m taichinh",
                                description="Máy tính lợi nhuận mỗi đơn — Shopee / TikTok Shop (P4 Đào Vàng)")
    p.add_argument("--san", help="shopee | tiktok")
    p.add_argument("--nganh", default="", help="tên ngành trong bảng phí (gõ không dấu, một phần tên cũng được)")
    p.add_argument("--gia-ban", type=float, help="giá niêm yết (đ)")
    p.add_argument("--gia-von", type=float, help="giá vốn gồm bao bì tiêu hao (đ)")
    p.add_argument("--ngay-ban", default=None, help="YYYY-MM-DD (mặc định hôm nay)")
    p.add_argument("--voucher-shop", type=float, default=0, help="giảm giá / mã do shop chịu (đ)")
    p.add_argument("--dong-goi", type=float, default=0, help="đóng gói, in phiếu (đ)")
    p.add_argument("--ship-shop-chiu", type=float, default=0, help="ship shop chịu thêm (đ)")
    p.add_argument("--voucher-san", action="store_true", help="tham gia Voucher Xtra (Shopee) / VXP (TikTok)")
    p.add_argument("--aff-shop-tra", type=float, default=0, help="%% hoa hồng affiliate shop trả")
    p.add_argument("--quang-cao", type=float, default=0, help="%% doanh thu chi quảng cáo")
    p.add_argument("--ty-le-hoan", type=float, default=0, help="%% đơn trả hàng & hoàn tiền (GIẢ ĐỊNH)")
    p.add_argument("--ship-tra-hang", type=float, default=None, help="ship trả hàng shop chịu (đ); mặc định trần bảng phí")
    p.add_argument("--hong-hang-hoan", type=float, default=30, help="%% hàng hoàn không bán lại được (GIẢ ĐỊNH, mặc định 30)")
    p.add_argument("--thue-gtgt", type=float, default=None, help="%% GTGT sàn khấu trừ (mặc định theo bảng phí: 1)")
    p.add_argument("--thue-tncn", type=float, default=None, help="%% TNCN sàn khấu trừ (mặc định theo bảng phí: 0,5)")
    p.add_argument("--muc", choices=["thap", "giua", "cao"], default="cao",
                   help="chọn mức khi bảng phí ghi khoảng (mặc định cao = thận trọng)")
    p.add_argument("--phi-nganh", type=float, default=None, help="ghi đè phí ngành (%%) nếu đã tra PDF cấp 3")
    p.add_argument("--shop-moi", action="store_true", help="Shopee: miễn phí cố định shop mới (30 ngày / 200 đơn)")
    p.add_argument("--bo-phi-ha-tang", action="store_true", help="Shopee: bỏ phí hạ tầng 3.000đ (kịch bản chỉ Mall thu)")
    p.add_argument("--aff-nhan", type=float, default=None, help="%% hoa hồng bạn nhận nếu làm affiliate → so sánh")
    p.add_argument("--thue-aff", type=float, default=0, help="%% thuế khấu trừ trên hoa hồng affiliate (CHƯA XÁC MINH)")
    p.add_argument("--bang-phi", default=str(BANG_PHI_MAC_DINH), help="đường dẫn CSV bảng phí")
    p.add_argument("--liet-ke-nganh", action="store_true", help="in danh sách ngành của sàn rồi thoát")
    p.add_argument("--json", action="store_true", help="in kết quả dạng JSON")
    return p


def main(argv=None) -> int:
    a = tao_parser().parse_args(argv)
    try:
        bp = BangPhi(a.bang_phi)
        if a.liet_ke_nganh:
            if not a.san:
                raise ThieuDuLieu("cần --san")
            ma = chuan_san(a.san)
            for n in bp.nganh_cua(SAN[ma]["ten"], SAN[ma]["phi_nganh"]):
                print(n)
            return 0
        thieu = [ten for ten, v in (("--san", a.san), ("--gia-ban", a.gia_ban), ("--gia-von", a.gia_von)) if v is None]
        if thieu:
            raise ThieuDuLieu("thiếu " + ", ".join(thieu))
        if chuan_san(a.san) == "shopee" and not a.nganh and a.phi_nganh is None:
            raise ThieuDuLieu("Shopee cần --nganh (xem --liet-ke-nganh) hoặc --phi-nganh")
        ngay = date.fromisoformat(a.ngay_ban) if a.ngay_ban else date.today()
        dv = DauVao(
            san=a.san, nganh=a.nganh, gia_ban=a.gia_ban, gia_von=a.gia_von, ngay_ban=ngay,
            giam_gia_shop=a.voucher_shop, dong_goi=a.dong_goi, ship_shop_chiu=a.ship_shop_chiu,
            tham_gia_voucher_san=a.voucher_san, hoa_hong_aff_shop_tra=a.aff_shop_tra, quang_cao_pct=a.quang_cao,
            ty_le_hoan=a.ty_le_hoan, ship_tra_hang=a.ship_tra_hang, ty_le_hong_hang_hoan=a.hong_hang_hoan,
            thue_gtgt=a.thue_gtgt, thue_tncn=a.thue_tncn, che_do_khoang=a.muc, phi_nganh_tu_nhap=a.phi_nganh,
            shop_moi_mien_phi_co_dinh=a.shop_moi, tinh_phi_ha_tang=not a.bo_phi_ha_tang,
            hoa_hong_aff_nhan=a.aff_nhan, thue_aff=a.thue_aff,
        )
        kq = MayTinh(bp).tinh(dv)
    except (ThieuDuLieu, ValueError) as e:
        print(f"LỖI / THIẾU DỮ LIỆU: {e}", file=sys.stderr)
        return 2
    if a.json:
        print(json.dumps(kq.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(in_ket_qua(kq))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
