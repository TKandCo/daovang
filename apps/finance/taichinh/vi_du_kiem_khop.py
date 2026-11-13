"""Sinh `apps/finance/vi-du-kiem-khop.json`: ví dụ đầu vào + đầu ra mong đợi để P9 kiểm khớp bản JavaScript.

Mỗi ví dụ "don" / "dropship" có thêm `phi_ap_dung` (mức phí đã tra từ bảng phí) để bản JS kiểm được CÔNG THỨC
mà không cần đọc CSV; và `dau_vao` gốc (sàn, ngành, ngày) để kiểm cả bước tra bảng phí nếu muốn.
Chạy (từ apps/finance): python3 -m taichinh.vi_du_kiem_khop        → ghi lại tệp
                         python3 -m taichinh.vi_du_kiem_khop --kiem → chỉ so tệp với kết quả hiện tại
Mọi số là GIẢ ĐỊNH.
"""
from __future__ import annotations

import json
import sys
from dataclasses import asdict
from datetime import date
from pathlib import Path

from . import affiliate as aff
from .dropship import tinh_dropship, von_ung_truoc
from .so_lai_lo import kiem_dong, kiem_cong_dot1
from .tinh_loi_nhuan import SAN, DauVao, KetQua, MayTinh, chuan_san, DONG_KHONG_DAM_BAO

TEP = Path(__file__).resolve().parents[1] / "vi-du-kiem-khop.json"
PHIEN_BAN = "1.0.0"
NGAY = "2026-11-12"

# ---- đầu vào (GIẢ ĐỊNH) ----
VI_DU_DON = [
    ("don-01", "Shopee thời trang (ví dụ A báo cáo Đợt 0, phí giữa khoảng)",
     dict(san="shopee", nganh="Thoi trang (tat ca)", gia_ban=150_000, gia_von=60_000, dong_goi=3_000,
          ty_le_hoan=10, ship_tra_hang=40_000, ty_le_hong_hang_hoan=30, che_do_khoang="giua")),
    ("don-02", "Shopee làm đẹp + Voucher Xtra + affiliate 5% (ví dụ B Đợt 0)",
     dict(san="shopee", nganh="Sac dep", gia_ban=250_000, giam_gia_shop=25_000, gia_von=95_000, dong_goi=3_500,
          tham_gia_voucher_san=True, hoa_hong_aff_shop_tra=5, ty_le_hoan=5, ship_tra_hang=40_000,
          ty_le_hong_hang_hoan=30, che_do_khoang="giua")),
    ("don-03", "Shopee làm đẹp, quảng cáo 10%, không hoàn",
     dict(san="shopee", nganh="Sac dep", gia_ban=200_000, gia_von=80_000, dong_goi=2_000, quang_cao_pct=10)),
    ("don-04", "Shopee Voucher Xtra chạm trần 50.000đ",
     dict(san="shopee", nganh="Sac dep", gia_ban=2_000_000, gia_von=500_000, tham_gia_voucher_san=True)),
    ("don-05", "Shopee shop mới miễn phí cố định, hoàn 10%, ship trả mặc định trần bảng phí",
     dict(san="shopee", nganh="Sac dep", gia_ban=100_000, gia_von=40_000, dong_goi=2_000, ty_le_hoan=10,
          ty_le_hong_hang_hoan=50, shop_moi_mien_phi_co_dinh=True)),
    ("don-06", "TikTok giày dép (mức cao 15%), hoàn 10%, phí xử lý đơn mất khi hoàn",
     dict(san="tiktok", nganh="Giay dep", gia_ban=200_000, gia_von=80_000, ty_le_hoan=10, ship_tra_hang=30_000,
          ty_le_hong_hang_hoan=0)),
    ("don-07", "TikTok ngành mặc định 14%, VXP 5%, quảng cáo 8%",
     dict(san="tiktok", nganh="", gia_ban=180_000, giam_gia_shop=10_000, gia_von=70_000, dong_goi=2_000,
          tham_gia_voucher_san=True, quang_cao_pct=8, ty_le_hoan=6, ship_tra_hang=25_000)),
]

VI_DU_DROPSHIP = [
    ("dropship-01", "Dropship Shopee làm đẹp, phí NCC 5.000, hủy 10%, hoàn 10%",
     dict(san="shopee", nganh="Sac dep", gia_ban=200_000, gia_von=80_000, ty_le_hoan=10, ship_tra_hang=30_000,
          ty_le_hong_hang_hoan=50),
     dict(phi_ncc=5_000, ty_le_huy=10, ngay_giao=3, loai_shop="moi")),
    ("dropship-02", "Dropship TikTok shop mới (chờ 8 ngày), hủy 5%, chi phí hủy 8.000, quảng cáo 10%",
     dict(san="tiktok", nganh="", gia_ban=150_000, gia_von=55_000, ty_le_hoan=8, ship_tra_hang=25_000,
          ty_le_hong_hang_hoan=40, quang_cao_pct=10),
     dict(phi_ncc=4_000, ty_le_huy=5, chi_phi_moi_don_huy=8_000, ngay_giao=4, loai_shop="moi")),
]

VI_DU_AFF = [
    ("aff-01", "Shopee: hoa hồng 200.000 < ngưỡng, chi phí nội dung 20.000",
     dict(hoa_hong_goc=200_000, chi_phi_noi_dung=20_000)),
    ("aff-02", "Shopee: hoa hồng đúng 250.000 → bị khấu trừ 10% (vách ngưỡng)",
     dict(hoa_hong_goc=250_000)),
    ("aff-03", "Shopee: 1.200.000, chi phí nội dung 300.000",
     dict(hoa_hong_goc=1_200_000, chi_phi_noi_dung=300_000)),
    ("aff-04", "Shopee: 251.000, ngưỡng so SAU phí 0,98% → 248.540 < 250.000, không khấu trừ",
     dict(hoa_hong_goc=251_000, nguong_tinh_tren="sau_phi")),
    ("aff-05", "TikTok: chưa xác minh → dùng tạm luật Shopee",
     dict(hoa_hong_goc=500_000, san="tiktok", chi_phi_noi_dung=50_000)),
]

VI_DU_AFF_DON = [
    ("aff-don-01", "40 đơn × 150.000 × 10%, hủy/hoàn 10%, nội dung 100.000 (gộp một kỳ)",
     dict(gia_tri_don=150_000, ty_le_hoa_hong=10, so_don=40, ty_le_huy_hoan=10, chi_phi_noi_dung=100_000)),
]

VI_DU_VON = [
    ("von-01", "Vốn ứng trước: 5 đơn/ngày × 77.000 chi ra, tiền về 117.180 sau 8 ngày",
     dict(don_moi_ngay=5, chi_ra_moi_don=77_000, tien_ve_moi_don=117_180, ngay_tre=8, so_ngay=56)),
    ("von-02", "Vốn ứng trước: tiền về < chi ra (lỗ) → số dư âm mãi",
     dict(don_moi_ngay=3, chi_ra_moi_don=100_000, tien_ve_moi_don=90_000, ngay_tre=5, so_ngay=30)),
]

VI_DU_SO = [
    ("so-01", "Sổ mini: cổng 4 tuần ĐẠT nhưng cộng dồn từ đầu LỖ (gói công cụ phân bổ)",
     dict(ngay_cuoi="2026-12-28", so_ngay=28, dong=[
         dict(ngay="2026-11-02", thu_chi="chi", loai="cong_cu", mo_hinh="chung", kenh="chung", so_tien_vnd="5600000",
              phan_bo_tu="2026-11-02", phan_bo_den="2026-12-28", mo_ta="GIA DINH", nguon="GIA DINH"),
         dict(ngay="2026-11-10", thu_chi="chi", loai="hang_mau", mo_hinh="dropship", kenh="shopee",
              so_tien_vnd="1500000", mo_ta="GIA DINH", nguon="GIA DINH"),
         dict(ngay="2026-12-10", thu_chi="thu", loai="doanh_thu_don", mo_hinh="dropship", kenh="shopee",
              so_tien_vnd="6000000", mo_ta="GIA DINH", nguon="GIA DINH"),
         dict(ngay="2026-12-10", thu_chi="chi", loai="gia_von_ncc", mo_hinh="dropship", kenh="shopee",
              so_tien_vnd="2400000", mo_ta="GIA DINH", nguon="GIA DINH"),
         dict(ngay="2026-12-20", thu_chi="thu", loai="hoa_hong_affiliate", mo_hinh="affiliate", kenh="shopee",
              so_tien_vnd="400000", mo_ta="GIA DINH", nguon="GIA DINH"),
     ])),
]


def _phi_ap_dung(dv: DauVao, kq: KetQua) -> dict:
    ma = chuan_san(dv.san)
    tim = lambda dau: next((c for c in kq.chi_phi if c.ten.startswith(dau)), None)
    v = tim("Voucher")
    H = tim("Phí mỗi đơn").so_tien
    sret = kq.chi_phi_moi_don_hoan - dv.dong_goi - dv.ship_shop_chiu - dv.ty_le_hong_hang_hoan / 100 * dv.gia_von
    if SAN[ma]["phi_don_mat_khi_hoan"]:
        sret -= H
    return {
        "phi_nganh_pct": tim("Phí ngành").ty_le,
        "phi_giao_dich_pct": tim("Phí giao dịch").ty_le,
        "phi_moi_don_vnd": H,
        "voucher_san_pct": v.ty_le if v else 0.0,
        "voucher_san_tran_vnd": 50_000,
        "thue_khau_tru_pct": tim("Thuế sàn").ty_le,
        "ship_tra_hang_vnd": round(sret, 2),
        "phi_moi_don_mat_khi_hoan": SAN[ma]["phi_don_mat_khi_hoan"],
    }


def _mong_doi_don(kq: KetQua) -> dict:
    return {
        "rev": kq.rev, "chi_phi": [{"ten": c.ten, "so_tien": c.so_tien} for c in kq.chi_phi], "cm": kq.cm,
        "chi_phi_moi_don_hoan": kq.chi_phi_moi_don_hoan, "ln_truoc_qc": kq.ln_truoc_qc, "quang_cao": kq.quang_cao,
        "ln": kq.ln, "bien_rong": kq.bien_rong, "roas_hoa_von": kq.roas_hoa_von, "gia_hoa_von": kq.gia_hoa_von,
        "gia_hoa_von_truoc_qc": kq.gia_hoa_von_truoc_qc, "thue_tam_khau_tru": kq.thue_tam_khau_tru,
        "ty_le_phi_san_aff_chua_thue": kq.ty_le_phi_san_aff_chua_thue,
        "ty_le_phi_gom_thue_khau_tru": kq.ty_le_phi_gom_thue_khau_tru,
    }


def tao(mt: MayTinh | None = None) -> dict:
    mt = mt or MayTinh()
    ngay = date.fromisoformat(NGAY)
    vd = []
    for id_, mo_ta, kw in VI_DU_DON:
        dv = DauVao(ngay_ban=ngay, **kw)
        kq = mt.tinh(dv)
        vd.append({"id": id_, "loai": "don", "mo_ta": mo_ta, "dau_vao": {**kw, "ngay_ban": NGAY},
                   "phi_ap_dung": _phi_ap_dung(dv, kq), "mong_doi": _mong_doi_don(kq)})
    for id_, mo_ta, kw, kw_ds in VI_DU_DROPSHIP:
        dv = DauVao(ngay_ban=ngay, **kw)
        k = tinh_dropship(dv, mt=mt, **kw_ds)
        dv_tinh = DauVao(ngay_ban=ngay, **{**kw, "dong_goi": kw.get("dong_goi", 0) + kw_ds["phi_ncc"]})
        vd.append({"id": id_, "loai": "dropship", "mo_ta": mo_ta,
                   "dau_vao": {**kw, "ngay_ban": NGAY, **kw_ds},
                   "phi_ap_dung": _phi_ap_dung(dv_tinh, k.don),
                   "mong_doi": {"don_khong_huy": _mong_doi_don(k.don), "ln_moi_don_dat": k.ln_moi_don_dat,
                                "ln_truoc_qc_moi_don_dat": k.ln_truoc_qc_moi_don_dat,
                                "chi_phi_moi_don_huy": k.chi_phi_moi_don_huy,
                                "chi_ra_moi_don_dat": k.chi_ra_moi_don_dat, "tien_ve_moi_don_dat": k.tien_ve_moi_don_dat,
                                "ngay_cho": k.ngay_cho, "ngay_rut": k.ngay_rut, "ngay_tre": k.ngay_tre}})
    for id_, mo_ta, kw in VI_DU_AFF:
        k = aff.thuc_nhan(**kw)
        d = asdict(k)
        for x in ("canh_bao", "khong_dam_bao"):
            d.pop(x)
        vd.append({"id": id_, "loai": "affiliate", "mo_ta": mo_ta, "dau_vao": kw, "mong_doi": d})
    for id_, mo_ta, kw in VI_DU_AFF_DON:
        k = aff.thuc_nhan_tu_don(**kw)
        d = asdict(k)
        for x in ("canh_bao", "khong_dam_bao"):
            d.pop(x)
        vd.append({"id": id_, "loai": "affiliate_tu_don", "mo_ta": mo_ta, "dau_vao": kw, "mong_doi": d})
    for id_, mo_ta, kw in VI_DU_VON:
        d = von_ung_truoc(**kw)
        d.pop("ghi_chu")
        vd.append({"id": id_, "loai": "von_ung_truoc", "mo_ta": mo_ta, "dau_vao": kw, "mong_doi": d})
    for id_, mo_ta, kw in VI_DU_SO:
        dong = [kiem_dong(r) for r in kw["dong"]]
        d = kiem_cong_dot1(dong, date.fromisoformat(kw["ngay_cuoi"]), kw["so_ngay"])
        vd.append({"id": id_, "loai": "so_lai_lo", "mo_ta": mo_ta, "dau_vao": kw,
                   "mong_doi": {"cua_so_4_tuan": d["cua_so_4_tuan"], "tu_dau_du_an": d["tu_dau_du_an"],
                                "dat_cong_dot1": d["dat_cong_dot1"]}})
    return {
        "phien_ban": PHIEN_BAN,
        "sinh_boi": "apps/finance/taichinh/vi_du_kiem_khop.py (bản Python là chuẩn)",
        "bang_phi": "bao-cao/dot0/bang-phi-v1.csv",
        "dung_sai": {"tien_vnd": 0.5, "ty_le": 1e-6, "roas": 1e-4, "gia_hoa_von_vnd": 2},
        "ghi_chu": ("Tiền VND, tỷ lệ nhập theo % (6 = 6%), tỷ lệ đầu ra (bien_rong, ty_le_phi_*) là phân số (0.23 = 23%). "
                    "Công thức: apps/finance/README.md. MỌI SỐ LÀ GIẢ ĐỊNH. " + DONG_KHONG_DAM_BAO),
        "vi_du": vd,
    }


def ghi(duong_dan: Path = TEP) -> dict:
    d = tao()
    duong_dan.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return d


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if "--kiem" in argv:
        cu = json.loads(TEP.read_text(encoding="utf-8"))
        moi = json.loads(json.dumps(tao(), ensure_ascii=False))
        ok = cu == moi
        print("KHỚP" if ok else "LỆCH — chạy lại không có --kiem để sinh tệp, rồi rà diff")
        return 0 if ok else 1
    d = ghi()
    print(f"Đã ghi {TEP.name}: {len(d['vi_du'])} ví dụ")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
