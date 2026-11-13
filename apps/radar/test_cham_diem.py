"""Kiểm thử cham_diem.py — kiểm ngược bằng phép tính tay (không chỉ so với chính máy P4).

Chạy:  python3 -m unittest apps/radar/test_cham_diem.py   (từ thư mục gốc repo)
"""
import csv
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cham_diem as cd  # noqa: E402
import kiem_tra as kt  # noqa: E402

N18_SHOPEE = "Cham soc thu cung"


class PhiTheoNganh(unittest.TestCase):
    def test_n18_shopee_tinh_tay(self):
        # phí cố định 14% + xử lý giao dịch 6% + thuế 1,5% + hạ tầng 3.000đ/100.000đ = 24,5%
        self.assertAlmostEqual(cd.tong_phi(cd.MayTinh(), "shopee", N18_SHOPEE, 100_000, False)[0], 24.5)
        # thêm Voucher Xtra 5,5% (dưới trần 50.000đ) = 30,0%
        self.assertAlmostEqual(cd.tong_phi(cd.MayTinh(), "shopee", N18_SHOPEE, 100_000, True)[0], 30.0)

    def test_tran_voucher_xtra(self):
        # giá 2.000.000đ: 5,5% = 110.000đ nhưng trần 50.000đ → voucher chỉ +2,5%
        k, c = (cd.tong_phi(cd.MayTinh(), "shopee", N18_SHOPEE, 2_000_000, v)[0] for v in (False, True))
        self.assertAlmostEqual(c - k, 2.5)

    def test_phi_khong_phai_24_co_dinh(self):
        """P12 2.1: mức phí khác nhau theo ngành / voucher / giá — không còn một số '~24%'."""
        _, ds = kt.doc_csv(cd.P_PHI_NHOM)
        cac_muc = {d[7] for d in ds}
        self.assertGreater(len(cac_muc), 5)

    def test_bang_phi_nhom_tai_lap(self):
        _, ds = kt.doc_csv(cd.P_PHI_NHOM)
        self.assertEqual(ds, cd.bang_phi_theo_nhom())
        nhom = {d[0] for d in ds}
        for n in kt.NHOM_DA_CHON:
            self.assertIn(n, nhom)

    def test_fee_ref(self):
        self.assertEqual(cd.nganh_tu_fee_ref("Shopee|phi_co_dinh|A;TikTok Shop|phi_hoa_hong_nen_tang|B;"
                                             "TikTok Shop|phi_hoa_hong_nen_tang|C"),
                         {"shopee": "A", "tiktok": "B"})


class Affiliate(unittest.TestCase):
    def test_tinh_tay_shopee(self):
        # 100.000 × 10% × (1 − 5% hoàn) × (1 − 0,98%) × (1 − 10%) = 8.466,21đ → 8,47% → 25 điểm
        a = cd.cham_affiliate("shopee", N18_SHOPEE, 100_000, 10)
        self.assertEqual(a["thuc_nhan_vnd"], 8466)
        self.assertAlmostEqual(a["thuc_nhan_pct"], 8.47)
        self.assertEqual(a["diem_bien"], 25)
        self.assertFalse(a["loai"])

    def test_hoa_hong_thap_bi_loai(self):
        a = cd.cham_affiliate("shopee", N18_SHOPEE, 100_000, 3)  # thực nhận ≈ 2,54% < 3%
        self.assertEqual(a["diem_bien"], 0)
        self.assertTrue(a["loai"])

    def test_nganh_khong_hoa_hong(self):
        a = cd.cham_affiliate("shopee", "Me & Be", 100_000, 20)
        self.assertEqual((a["thuc_nhan_vnd"], a["diem_bien"], a["loai"]), (0.0, 0, True))
        self.assertTrue(cd.khong_co_hoa_hong("Sức khỏe"))
        self.assertFalse(cd.khong_co_hoa_hong(N18_SHOPEE))

    def test_affiliate_khong_chiu_phi_san(self):
        """Hoa hồng thực nhận không đổi theo ngành có phí cố định cao / thấp."""
        a = cd.cham_affiliate("shopee", N18_SHOPEE, 100_000, 10)
        b = cd.cham_affiliate("shopee", "Nha cua & Doi song - con lai", 100_000, 10)
        self.assertEqual(a["thuc_nhan_vnd"], b["thuc_nhan_vnd"])


class Dropship(unittest.TestCase):
    def test_tinh_tay_co_voucher(self):
        # CM = 100.000 − 50.000 − 30.000 (24,5% + 5,5%) = 20.000
        # hoàn 5%: chi phí mỗi đơn hoàn = 40.000 ship trả + 30% × 50.000 hỏng = 55.000
        # LN = 0,95 × 20.000 − 0,05 × 55.000 = 16.250 → 16,25% → 15 điểm
        d = cd.cham_dropship("shopee", N18_SHOPEE, 100_000, 50_000, voucher=True)
        self.assertEqual(d["ln_vnd"], 16250)
        self.assertAlmostEqual(d["bien_pct"], 16.25)
        self.assertEqual(d["diem_bien"], 15)

    def test_khong_voucher_cao_hon(self):
        c = cd.cham_dropship("shopee", N18_SHOPEE, 100_000, 50_000, voucher=True)
        k = cd.cham_dropship("shopee", N18_SHOPEE, 100_000, 50_000, voucher=False)
        # chênh 5,5% × 100.000 × 0,95 (đơn không hoàn) = 5.225đ
        self.assertEqual(k["ln_vnd"] - c["ln_vnd"], 5225)

    def test_bien_thap_bi_loai(self):
        d = cd.cham_dropship("shopee", N18_SHOPEE, 100_000, 65_000)
        self.assertEqual(d["diem_bien"], 0)
        self.assertTrue(d["loai"])


class NhapTay(unittest.TestCase):
    def test_cham_dong_nhap_tay(self):
        tam = tempfile.mkdtemp()
        try:
            for d in ("mau", "du-lieu", "nhap-tay"):
                shutil.copytree(os.path.join(cd.GOC, d), os.path.join(tam, d))
            p = os.path.join(tam, "nhap-tay", "4-nhom.csv")
            with open(p, "a", encoding="utf-8", newline="") as f:
                w = csv.writer(f)
                w.writerow(["N18", "shopee", "2026-11-12", "Vòng cổ", "https://shopee.vn/x",
                            "100.000", "", "", "10", "50.000", ""])
                w.writerow(["N05", "tiktok", "2026-11-12", "Cây lau", "https://www.tiktok.com/x",
                            "120000", "", "", "", "", ""])
            self.assertEqual(kt.kiem_tat_ca(tam)[1], [])
            r = cd.cham_nhap_tay(p, tam)
            self.assertEqual(r[0]["affiliate"]["thuc_nhan_vnd"], 8466)
            self.assertEqual(r[0]["dropship_co_voucher"]["ln_vnd"], 16250)
            self.assertEqual(r[1]["affiliate"], "CHƯA ĐO")
            self.assertEqual(r[1]["dropship_co_voucher"], "CHƯA ĐO")
        finally:
            shutil.rmtree(tam)

    def test_bang_that_chi_co_tieu_de(self):
        tieu_de, ds = kt.doc_csv(cd.P_NHAP_TAY)
        self.assertEqual(tieu_de, kt.COT["4-nhom"])
        self.assertEqual([d for d in ds if any(d)], [])  # chưa có dữ liệu thật — không bịa


if __name__ == "__main__":
    unittest.main()
