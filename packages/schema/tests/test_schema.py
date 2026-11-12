"""Kiểm thử schema. Chạy: python3 -m unittest discover -s packages/schema/tests"""
import sys
import tempfile
import unittest
from pathlib import Path

GOC = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(GOC / "packages" / "schema"))

from daovang_schema import (COT_BANG_PHI, SKU, DonHang, DongDon, Khach,  # noqa: E402
                            NhaCungCap, Video, doc_bang_phi, chuan_hoa_do_tin_cay)

BANG_PHI_V1 = GOC / "bao-cao" / "dot0" / "bang-phi-v1.csv"


class TestBangPhiV1(unittest.TestCase):
    def setUp(self):
        self.dong = doc_bang_phi(BANG_PHI_V1)

    def test_doc_duoc_va_du_dong(self):
        so_dong_tep = sum(1 for d in BANG_PHI_V1.read_text(encoding="utf-8-sig").splitlines()[1:] if d.strip())
        self.assertEqual(len(self.dong), so_dong_tep)
        self.assertGreater(len(self.dong), 0)

    def test_moi_dong_hop_le_co_nguon(self):
        for i, d in enumerate(self.dong, start=2):
            self.assertEqual(d.kiem_tra(), [], f"dòng {i}: {d}")

    def test_co_ca_hai_san(self):
        san = {d.san for d in self.dong}
        self.assertIn("Shopee", san)
        self.assertIn("TikTok Shop", san)

    def test_khoang_muc(self):
        theo_muc = {d.muc: d.khoang_muc() for d in self.dong}
        self.assertEqual(theo_muc["13.5-16.5"], (13.5, 16.5))
        self.assertEqual(theo_muc["3000"], (3000.0, 3000.0))
        self.assertIsNone(theo_muc["CHUA XAC MINH"])

    def test_ngay_nguon_tu_cot_nguon(self):
        co_ngay = [d for d in self.dong if d.ngay_nguon]
        self.assertGreater(len(co_ngay), len(self.dong) // 2)

    def test_cot_sai_bao_loi(self):
        with tempfile.TemporaryDirectory() as t:
            p = Path(t) / "x.csv"
            p.write_text("san,muc\nShopee,1\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                doc_bang_phi(p)

    def test_bom_va_thu_tu_cot(self):
        with tempfile.TemporaryDirectory() as t:
            p = Path(t) / "x.csv"
            p.write_text("﻿" + ",".join(COT_BANG_PHI) + "\n"
                         "Shopee,phi_ha_tang,,3000,VND/don,,https://vd (tra 01/02/2026),CAO,\n",
                         encoding="utf-8")
            d = doc_bang_phi(p)[0]
            self.assertEqual(d.ngay_nguon, "2026-02-01")


class TestBanGhi(unittest.TestCase):
    def test_sku_hop_le_va_thieu_nguon(self):
        s = SKU("SKU1", "Ao thun", 150000, 60000, "nhap tay", "2026-11-12")
        self.assertEqual(s.kiem_tra(), [])
        s2 = SKU("SKU1", "Ao thun", 150000, 60000, "", "12/11/2026")
        self.assertEqual(len(s2.kiem_tra()), 2)

    def test_don_hang_tong_va_dict(self):
        d = DonHang("D1", "Shopee", "2026-11-12", "da_giao",
                    [DongDon("SKU1", 2, 100000, 10000)], "nhap tay", "2026-11-12")
        self.assertEqual(d.tong_hang_vnd(), 190000)
        d2 = DonHang.tu_dict(d.thanh_dict())
        self.assertEqual(d2, d)
        self.assertEqual(d.kiem_tra(), [])

    def test_don_hang_san_sai(self):
        d = DonHang("D1", "Lazada?", "2026-11-12", "da_giao", [], "x", "2026-11-12")
        self.assertEqual(len(d.kiem_tra()), 2)

    def test_khach_cam_du_lieu_ca_nhan(self):
        with self.assertRaises(ValueError):
            Khach.tu_dict({"ma_khach": "K1", "nguon": "x", "ngay_nguon": "2026-11-12",
                           "sdt": "0900000000"})
        k = Khach.tu_dict({"ma_khach": "K1", "nguon": "x", "ngay_nguon": "2026-11-12"})
        self.assertEqual(k.kiem_tra(), [])

    def test_truong_la_bi_tu_choi(self):
        with self.assertRaises(ValueError):
            NhaCungCap.tu_dict({"ma_ncc": "N1", "ten": "x", "kenh": "1688", "nguon": "x",
                                "ngay_nguon": "2026-11-12", "mat_khau": "x"})

    def test_video_nhan_ai_va_dong_y(self):
        v = Video("V1", "demo", "cong cu AI", "2026-11-12", co_ai=True,
                  trang_thai="cho_duyet", co_nguoi_that=True)
        self.assertEqual(len(v.kiem_tra()), 2)
        v.da_gan_nhan_ai = True
        v.co_van_ban_dong_y = True
        self.assertEqual(v.kiem_tra(), [])

    def test_chuan_hoa_do_tin_cay(self):
        self.assertEqual(chuan_hoa_do_tin_cay("Thấp"), "THAP")
        self.assertEqual(chuan_hoa_do_tin_cay("chưa xác minh"), "CHUA XAC MINH")


if __name__ == "__main__":
    unittest.main()
