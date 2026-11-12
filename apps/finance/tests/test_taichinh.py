"""Kiểm thử P4. Chạy từ gốc repo: python3 -m unittest discover -s apps/finance -t apps/finance -v"""
import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from datetime import date
from pathlib import Path

from taichinh import BangPhi, DauVao, MayTinh, ThieuDuLieu, DONG_KHONG_DAM_BAO
from taichinh.bang_phi import tach_muc, tach_ngay
from taichinh import kiem_nguoc
from taichinh.__main__ import main as cli

NGAY = date(2026, 11, 12)
BP = BangPhi()
MT = MayTinh(BP)

TIEU_DE = "san,loai_phi,nganh,muc,don_vi,hieu_luc_tu,nguon,do_tin_cay,ghi_chu\n"
DONG_CHUNG = (
    "Shopee,phi_xu_ly_giao_dich,Tat ca (nguoi ban thuong),6.0,%,2026-05-01,src,CAO,\n"
    "Shopee,phi_ha_tang,Tat ca,3000,VND/don,,src,CAO,\n"
    "Shopee,phi_van_chuyen_tra_hang_nguoi_ban_chiu,Tat ca,toi da 40000 (20000 neu Hoa toc),VND/don,2025-04-01,src,CAO,\n"
    "Chung (san khau tru),thue_khau_tru_GTGT,Hang hoa (ca nhan cu tru),1.0,%,2025-07-01,src,CAO,\n"
    "Chung (san khau tru),thue_khau_tru_TNCN,Hang hoa (ca nhan cu tru),0.5,%,2025-07-01,src,CAO,\n"
)


def bang_tam(noi_dung: str) -> BangPhi:
    f = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8-sig")
    f.write(TIEU_DE + noi_dung)
    f.close()
    return BangPhi(f.name)


class TestTachMuc(unittest.TestCase):
    def test_mot_so(self):
        m = tach_muc("17.0")
        self.assertEqual((m.thap, m.cao), (17.0, 17.0))
        self.assertFalse(m.la_khoang)

    def test_khoang_thap_giua_cao(self):
        m = tach_muc("13.5-16.5")
        self.assertEqual(m.chon("thap"), 13.5)
        self.assertEqual(m.chon("cao"), 16.5)
        self.assertEqual(m.chon("giua"), 15.0)
        with self.assertRaises(ValueError):
            m.chon("xyz")

    def test_tran_va_trung_vi(self):
        self.assertEqual(tach_muc("5.5 (toi da 50000/san pham)").tran_vnd, 50000)
        m = tach_muc("14.0-15.0 (trung vi 15.0)")
        self.assertEqual((m.thap, m.cao, m.trung_vi), (14.0, 15.0, 15.0))
        self.assertEqual(tach_muc("toi da 40000 (20000 neu Hoa toc)").cao, 40000)

    def test_chua_xac_minh_va_chu(self):
        self.assertIsNone(tach_muc("CHUA XAC MINH"))
        self.assertIsNone(tach_muc(""))
        self.assertIsNone(tach_muc("nguoi ban tu dat ty le"))


class TestNgayHieuLuc(unittest.TestCase):
    def test_tach_ngay(self):
        self.assertEqual(tach_ngay("2026-05-23")[0], date(2026, 5, 23))
        tu, den, _ = tach_ngay("2025-07-01 den 2026-12-31")
        self.assertEqual((tu, den), (date(2025, 7, 1), date(2026, 12, 31)))
        tu, _, cb = tach_ngay("2026-09-01 hoac 2027-01-01")
        self.assertEqual(tu, date(2027, 1, 1))
        self.assertTrue(cb)
        self.assertEqual(tach_ngay("")[0], None)
        self.assertTrue(tach_ngay("")[2])

    def test_chon_muc_theo_ngay_tu_ghi_chu(self):
        # Bảng v1: Sắc đẹp 17% từ 23/05/2026, ghi chú "Truoc 23/05/2026: 14.0"
        self.assertEqual(BP.tra("Shopee", "phi_co_dinh", "Sac dep", date(2026, 5, 23)).muc.cao, 17.0)
        cu = BP.tra("Shopee", "phi_co_dinh", "Sac dep", date(2026, 5, 22))
        self.assertEqual(cu.muc.cao, 14.0)
        self.assertTrue(cu.suy_tu_ghi_chu)

    def test_truoc_do_tiktok_va_blog(self):
        self.assertEqual(BP.tra("TikTok Shop", "phi_giao_dich", "Tat ca", date(2026, 5, 8)).muc.cao, 5.0)
        self.assertEqual(BP.tra("TikTok Shop", "phi_giao_dich", "Tat ca", date(2026, 5, 9)).muc.cao, 6.0)
        cu = BP.tra("Shopee", "phi_xu_ly_giao_dich", "Tat ca (nguoi ban thuong)", date(2026, 4, 30))
        self.assertEqual(cu.muc.cao, 4.91)
        self.assertEqual(cu.do_tin_cay, "TB")  # ghi chú nói nguồn blog

    def test_nhieu_phien_ban_chon_moi_nhat(self):
        bp = bang_tam(DONG_CHUNG +
                      "Shopee,phi_co_dinh,X,10.0,%,2026-01-01,src,CAO,\n"
                      "Shopee,phi_co_dinh,X,12.0,%,2026-06-01,src,CAO,\n")
        self.assertEqual(bp.tra("Shopee", "phi_co_dinh", "X", date(2026, 5, 31)).muc.cao, 10.0)
        self.assertEqual(bp.tra("Shopee", "phi_co_dinh", "X", date(2026, 6, 1)).muc.cao, 12.0)
        with self.assertRaises(ThieuDuLieu):
            bp.tra("Shopee", "phi_co_dinh", "X", date(2025, 12, 31))

    def test_tiktok_truoc_hieu_luc_bao_thieu(self):
        with self.assertRaises(ThieuDuLieu):
            MT.tinh(DauVao(san="tiktok", nganh="Giay dep", gia_ban=200000, gia_von=80000,
                           ngay_ban=date(2026, 4, 1)))

    def test_canh_bao_gtgt_2027(self):
        kq = MT.tinh(DauVao(san="shopee", nganh="Sac dep", gia_ban=100000, gia_von=50000, ngay_ban=date(2027, 2, 1)))
        self.assertTrue(any("GTGT 8%" in c for c in kq.canh_bao))


class TestCongThuc(unittest.TestCase):
    def test_tinh_tay_shopee(self):
        kq = MT.tinh(DauVao(san="shopee", nganh="Sac dep", gia_ban=200000, gia_von=80000, dong_goi=2000,
                            ngay_ban=NGAY, quang_cao_pct=10))
        # 200000 − 80000 − 2000 − 17%·200000 − 6%·200000 − 3000 − 1,5%·200000
        cm = 200000 - 80000 - 2000 - 34000 - 12000 - 3000 - 3000
        self.assertAlmostEqual(kq.cm, cm)
        self.assertAlmostEqual(kq.ln, cm - 20000)
        self.assertAlmostEqual(kq.bien_rong, (cm - 20000) / 200000, places=5)
        self.assertAlmostEqual(kq.roas_hoa_von, 200000 / cm, places=3)

    def test_gia_hoa_von_cho_ln_bang_0(self):
        dv = DauVao(san="shopee", nganh="Sac dep", gia_ban=200000, gia_von=80000, dong_goi=2000,
                    ngay_ban=NGAY, quang_cao_pct=10, ty_le_hoan=5, giam_gia_shop=10000)
        kq = MT.tinh(dv)
        from dataclasses import replace
        self.assertAlmostEqual(MT.tinh(replace(dv, gia_ban=kq.gia_hoa_von)).ln, 0, delta=1)
        self.assertLess(kq.gia_hoa_von_truoc_qc, kq.gia_hoa_von)

    def test_tran_voucher_xtra(self):
        kq = MT.tinh(DauVao(san="shopee", nganh="Sac dep", gia_ban=2_000_000, gia_von=500000, ngay_ban=NGAY,
                            tham_gia_voucher_san=True))
        v = [c for c in kq.chi_phi if c.ten.startswith("Voucher")][0]
        self.assertEqual(v.so_tien, 50000)  # 5,5% × 2tr = 110.000 → trần 50.000

    def test_thue_la_tham_so(self):
        a = MT.tinh(DauVao(san="shopee", nganh="Sac dep", gia_ban=100000, gia_von=40000, ngay_ban=NGAY))
        b = MT.tinh(DauVao(san="shopee", nganh="Sac dep", gia_ban=100000, gia_von=40000, ngay_ban=NGAY,
                           thue_gtgt=0, thue_tncn=0))
        self.assertAlmostEqual(b.cm - a.cm, 1500)

    def test_hoan_hang(self):
        kq = MT.tinh(DauVao(san="shopee", nganh="Sac dep", gia_ban=100000, gia_von=40000, dong_goi=2000,
                            ngay_ban=NGAY, ty_le_hoan=10, ty_le_hong_hang_hoan=50))
        chi_hoan = 2000 + 40000 + 0.5 * 40000  # ship trả mặc định = trần 40.000 trong bảng phí
        self.assertAlmostEqual(kq.chi_phi_moi_don_hoan, chi_hoan)
        self.assertAlmostEqual(kq.ln_truoc_qc, 0.9 * kq.cm - 0.1 * chi_hoan)

    def test_tiktok_phi_don_mat_khi_hoan(self):
        kq = MT.tinh(DauVao(san="tiktok", nganh="Giay dep", gia_ban=200000, gia_von=80000, ngay_ban=NGAY,
                            ty_le_hoan=10, ship_tra_hang=30000, ty_le_hong_hang_hoan=0))
        self.assertAlmostEqual(kq.chi_phi_moi_don_hoan, 30000 + 3000)
        # Giày dép TikTok 14.0-15.0 → mặc định cao 15%
        f = [c for c in kq.chi_phi if c.ten.startswith("Phí ngành")][0]
        self.assertEqual(f.ty_le, 15.0)

    def test_tiktok_nganh_trong_dung_mac_dinh(self):
        kq = MT.tinh(DauVao(san="tiktok", nganh="", gia_ban=100000, gia_von=40000, ngay_ban=NGAY))
        self.assertIn("Muc mac dinh", kq.nganh)

    def test_lo_khong_co_roas(self):
        kq = MT.tinh(DauVao(san="shopee", nganh="Sac dep", gia_ban=50000, gia_von=45000, ngay_ban=NGAY))
        self.assertIsNone(kq.roas_hoa_von)
        self.assertLess(kq.ln, 0)

    def test_shop_moi_mien_phi_co_dinh(self):
        a = MT.tinh(DauVao(san="shopee", nganh="Sac dep", gia_ban=100000, gia_von=40000, ngay_ban=NGAY,
                           shop_moi_mien_phi_co_dinh=True))
        self.assertAlmostEqual([c for c in a.chi_phi if c.ten.startswith("Phí ngành")][0].so_tien, 0)

    def test_affiliate(self):
        kq = MT.tinh(DauVao(san="shopee", nganh="Sac dep", gia_ban=100000, gia_von=40000, ngay_ban=NGAY,
                            ty_le_hoan=10, quang_cao_pct=5, hoa_hong_aff_nhan=10, thue_aff=10))
        hh = 0.9 * 0.10 * 100000 * 0.9
        self.assertAlmostEqual(kq.affiliate["ln_affiliate"], hh - 5000)
        self.assertAlmostEqual(kq.affiliate["chenh_lech_nhap_truc_tiep_tru_affiliate"], kq.ln - (hh - 5000), places=1)


class TestMucKhoang(unittest.TestCase):
    def test_mac_dinh_cao(self):
        dv = dict(san="shopee", nganh="Thoi trang", gia_ban=100000, gia_von=40000, ngay_ban=NGAY)
        cao = MT.tinh(DauVao(**dv))
        thap = MT.tinh(DauVao(che_do_khoang="thap", **dv))
        self.assertAlmostEqual(thap.cm - cao.cm, 3000)  # (16,5 − 13,5)% × 100.000
        self.assertTrue(any("khoảng" in c for c in cao.canh_bao))

    def test_ghi_de_phi_nganh(self):
        kq = MT.tinh(DauVao(san="shopee", nganh="Thoi trang", gia_ban=100000, gia_von=40000, ngay_ban=NGAY,
                            phi_nganh_tu_nhap=14.0))
        self.assertEqual([c for c in kq.chi_phi if c.ten.startswith("Phí ngành")][0].so_tien, 14000)


class TestThieuDuLieu(unittest.TestCase):
    def test_nganh_khong_co(self):
        with self.assertRaises(ThieuDuLieu):
            MT.tinh(DauVao(san="shopee", nganh="khong ton tai", gia_ban=1, gia_von=1, ngay_ban=NGAY))

    def test_nganh_mo_ho(self):
        with self.assertRaises(ThieuDuLieu) as e:
            BP.khop_nganh("Shopee", "phi_co_dinh", "Nha cua")
        self.assertIn("nhiều", str(e.exception))

    def test_san_la(self):
        with self.assertRaises(ThieuDuLieu):
            MT.tinh(DauVao(san="lazada", nganh="x", gia_ban=1, gia_von=1))

    def test_muc_chua_xac_minh(self):
        bp = bang_tam(DONG_CHUNG + "Shopee,phi_co_dinh,Y,CHUA XAC MINH,%,2026-01-01,src,CHUA XAC MINH,\n")
        with self.assertRaises(ThieuDuLieu) as e:
            MayTinh(bp).tinh(DauVao(san="shopee", nganh="Y", gia_ban=100000, gia_von=1, ngay_ban=NGAY))
        self.assertIn("CHƯA XÁC MINH", str(e.exception))

    def test_dau_vao_sai(self):
        for kw in (dict(gia_ban=1000, giam_gia_shop=1000), dict(ty_le_hoan=150), dict(gia_von=-1)):
            base = dict(san="shopee", nganh="Sac dep", gia_ban=100000, gia_von=1, ngay_ban=NGAY)
            base.update(kw)
            with self.assertRaises(ThieuDuLieu):
                MT.tinh(DauVao(**base))

    def test_khong_co_tep(self):
        with self.assertRaises(ThieuDuLieu):
            BangPhi("/khong/co/tep.csv")

    def test_cli_thieu_tham_so(self):
        err = io.StringIO()
        with redirect_stderr(err):
            self.assertEqual(cli(["--san", "shopee"]), 2)
        self.assertIn("thiếu", err.getvalue())


class TestCanhBaoVaDauRa(unittest.TestCase):
    def test_canh_bao_ha_tang_mall(self):
        kq = MT.tinh(DauVao(san="shopee", nganh="Sac dep", gia_ban=100000, gia_von=40000, ngay_ban=NGAY))
        self.assertTrue(any("Shopee Mall" in c for c in kq.canh_bao))
        bo = MT.tinh(DauVao(san="shopee", nganh="Sac dep", gia_ban=100000, gia_von=40000, ngay_ban=NGAY,
                            tinh_phi_ha_tang=False))
        self.assertAlmostEqual(bo.cm - kq.cm, 3000)

    def test_dong_khong_dam_bao(self):
        out = io.StringIO()
        with redirect_stdout(out):
            cli(["--san", "shopee", "--nganh", "Sac dep", "--gia-ban", "100000", "--gia-von", "40000",
                 "--ngay-ban", "2026-11-12"])
        self.assertIn("không đảm bảo lợi nhuận", out.getvalue())
        self.assertIn("Shopee Mall", out.getvalue())
        out = io.StringIO()
        with redirect_stdout(out):
            cli(["--san", "tiktok", "--gia-ban", "100000", "--gia-von", "40000", "--json",
                 "--ngay-ban", "2026-11-12"])
        self.assertEqual(json.loads(out.getvalue())["khong_dam_bao"], DONG_KHONG_DAM_BAO)


class TestKiemNguoc(unittest.TestCase):
    """3 ví dụ p4-tai-chinh.md mục 5 (phí cố định giữa khoảng như báo cáo)."""

    def test_ba_vi_du(self):
        for x in kiem_nguoc.chay(MT):
            m = x["mong"]
            with self.subTest(x["ten"]):
                self.assertAlmostEqual(x["cm"], m["cm"], delta=0.5)
                self.assertAlmostEqual(x["roas0"], m["roas0"], delta=0.005)
                self.assertAlmostEqual(x["ln_hoan"], m["ln_hoan"], delta=1)
                self.assertAlmostEqual(x["roas_hoan"], m["roas_hoan"], delta=0.005)

    def test_vi_du_cot_loi(self):
        r = {x["ten"][0]: x for x in kiem_nguoc.chay(MT)}
        self.assertEqual(round(r["A"]["roas0"], 2), 2.99)
        self.assertEqual(round(r["C"]["roas_hoan"], 2), 10.76)


if __name__ == "__main__":
    unittest.main()
