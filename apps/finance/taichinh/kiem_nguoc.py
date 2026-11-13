"""KIỂM NGƯỢC: tái tạo 3 ví dụ GIẢ ĐỊNH trong bao-cao/dot0/p4-tai-chinh.md mục 5.

Ví dụ trong báo cáo chọn phí cố định GIỮA khoảng ngành → chạy với che_do_khoang="giua".
Chạy: python3 -m taichinh.kiem_nguoc   (từ thư mục apps/finance)
"""
from __future__ import annotations

from datetime import date

from .tinh_loi_nhuan import DauVao, MayTinh

NGAY = date(2026, 11, 12)

# (tên, đầu vào, số trong báo cáo: CM, ROAS r=0, LN trước QC có hoàn, ROAS có hoàn,
#  % phí sàn + affiliate CHƯA gồm thuế khấu trừ (nhãn sửa theo P12 2.2), % GỒM thuế khấu trừ (P12 tính lại))
VI_DU = [
    ("A. Thời trang, Shopee",
     dict(san="Shopee", nganh="Thoi trang (tat ca)", gia_ban=150_000, gia_von=60_000, dong_goi=3_000,
          ty_le_hoan=10, ship_tra_hang=40_000, ty_le_hong_hang_hoan=30),
     dict(cm=50_250, roas0=2.99, ln_hoan=39_125, roas_hoan=3.83, phi_chua_thue=23.0, phi_gom_thue=24.5)),
    ("B. Làm đẹp, Shopee, VXtra + affiliate",
     dict(san="Shopee", nganh="Sac dep", gia_ban=250_000, giam_gia_shop=25_000, gia_von=95_000, dong_goi=3_500,
          tham_gia_voucher_san=True, hoa_hong_aff_shop_tra=5,
          ty_le_hoan=5, ship_tra_hang=40_000, ty_le_hong_hang_hoan=30),
     dict(cm=44_750, roas0=5.03, ln_hoan=38_912, roas_hoan=5.78, phi_chua_thue=34.8, phi_gom_thue=36.3)),
    ("C. Nhà cửa nhỏ, Shopee, freeship shop trợ",
     dict(san="Shopee", nganh="Nha cua & Doi song - con lai", gia_ban=90_000, gia_von=40_000, dong_goi=2_500,
          ship_shop_chiu=10_000, ty_le_hoan=8, ship_tra_hang=40_000, ty_le_hong_hang_hoan=30),
     dict(cm=14_700, roas0=6.12, ln_hoan=8_364, roas_hoan=10.76, phi_chua_thue=23.8, phi_gom_thue=25.3)),
]


def chay(mt: MayTinh | None = None, che_do: str = "giua") -> list[dict]:
    mt = mt or MayTinh()
    ra = []
    for ten, dv, mong in VI_DU:
        co_hoan = mt.tinh(DauVao(ngay_ban=NGAY, che_do_khoang=che_do, **dv))
        khong_hoan = mt.tinh(DauVao(ngay_ban=NGAY, che_do_khoang=che_do, **{**dv, "ty_le_hoan": 0}))
        ra.append(dict(ten=ten, mong=mong, cm=co_hoan.cm, roas0=khong_hoan.roas_hoa_von,
                       ln_hoan=co_hoan.ln_truoc_qc, roas_hoan=co_hoan.roas_hoa_von,
                       phi_chua_thue=co_hoan.ty_le_phi_san_aff_chua_thue * 100,
                       phi_gom_thue=co_hoan.ty_le_phi_gom_thue_khau_tru * 100))
    return ra


def main():
    print("KIỂM NGƯỢC 3 ví dụ p4-tai-chinh.md (phí cố định GIỮA khoảng, như báo cáo)\n")
    tat_ca_khop = True
    for x in chay():
        m = x["mong"]
        dong = [
            ("CM (đ)", x["cm"], m["cm"], abs(x["cm"] - m["cm"]) < 1),
            ("ROAS hòa vốn r=0", x["roas0"], m["roas0"], round(x["roas0"], 2) == m["roas0"]),
            ("LN trước QC có hoàn (đ)", x["ln_hoan"], m["ln_hoan"], abs(x["ln_hoan"] - m["ln_hoan"]) < 1),
            ("ROAS hòa vốn có hoàn", x["roas_hoan"], m["roas_hoan"], round(x["roas_hoan"], 2) == m["roas_hoan"]),
            ("% phí sàn+aff CHƯA gồm thuế", x["phi_chua_thue"], m["phi_chua_thue"],
             round(x["phi_chua_thue"], 1) == m["phi_chua_thue"]),
            ("% phí GỒM thuế khấu trừ", x["phi_gom_thue"], m["phi_gom_thue"],
             round(x["phi_gom_thue"], 1) == m["phi_gom_thue"]),
        ]
        print(x["ten"])
        for ten, tinh, bc, ok in dong:
            tat_ca_khop &= ok
            print(f"  {ten:28} công cụ {tinh:>12,.4f} | báo cáo {bc:>10,} | {'KHỚP' if ok else 'LỆCH'}")
    print("\nSo với mức CAO (mặc định công cụ, thận trọng):")
    for x in chay(che_do="cao"):
        print(f"  {x['ten']:42} CM {x['cm']:>10,.0f} đ · ROAS hòa vốn có hoàn {x['roas_hoan']:.2f}")
    print("\nKẾT LUẬN:", "TẤT CẢ KHỚP" if tat_ca_khop else "CÓ LỆCH — xem trên")
    print("Số ví dụ là GIẢ ĐỊNH. Không phải khuyến nghị đầu tư / không đảm bảo lợi nhuận.")
    return 0 if tat_ca_khop else 1


if __name__ == "__main__":
    raise SystemExit(main())
