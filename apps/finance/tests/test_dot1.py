"""Kiểm thử P4 Đợt 1 (affiliate, dropship, sổ lãi lỗ, kịch bản, tệp kiểm khớp).
Chạy từ gốc repo: python3 -m unittest discover -s apps/finance -t apps/finance -v

Số "tính tay" trong tệp này viết thẳng bằng phép tính (không gọi công cụ) để kiểm ngược công thức.
Thư mục tạm dùng tempfile.TemporaryDirectory + đường dẫn tuyệt đối; KHÔNG dùng os.path.relpath
(trên Windows báo lỗi khi thư mục tạm ở ổ khác ổ chứa repo).
"""
import io
import json
import ntpath
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from datetime import date
from pathlib import Path, PureWindowsPath

from taichinh import DauVao, MayTinh, ThieuDuLieu
from taichinh import affiliate as aff
from taichinh import kich_ban, so_lai_lo, vi_du_kiem_khop
from taichinh.dropship import chu_ky_tien_ve, tinh_dropship, von_ung_truoc
from taichinh.so_lai_lo import (DongSo, doc_so, ghi_dong, kiem_cong_dot1, kiem_dong, tong_hop, theo_tuan,
                                _trong_repo_ngoai_mau, la_du_lieu_trong_repo)

NGAY = date(2026, 11, 12)
MT = MayTinh()
THU_MUC = Path(__file__).resolve().parents[1]
SO_MAU = THU_MUC / "du-lieu-mau" / "so-lai-lo-mau.csv"


class TestAffiliate(unittest.TestCase):
    def test_duoi_nguong(self):
        k = aff.thuc_nhan(200_000, chi_phi_noi_dung=20_000)
        self.assertAlmostEqual(k.thuc_nhan, 200_000 * (1 - 0.0098) - 20_000)   # 178.040
        self.assertFalse(k.co_khau_tru_thue)

    def test_dung_nguong_bi_khau_tru_toan_khoan(self):
        k = aff.thuc_nhan(250_000)
        self.assertTrue(k.co_khau_tru_thue)
        self.assertAlmostEqual(k.thuc_nhan, 250_000 * 0.9902 * 0.9)            # 222.795
        # vách ngưỡng: 249.999 nhận NHIỀU hơn 250.000
        self.assertGreater(aff.thuc_nhan(249_999).thuc_nhan, k.thuc_nhan)
        self.assertTrue(any("sát ngưỡng" in c for c in aff.thuc_nhan(240_000).canh_bao))

    def test_lon_co_noi_dung(self):
        self.assertAlmostEqual(aff.thuc_nhan(1_200_000, 300_000).thuc_nhan, 1_200_000 * 0.9902 * 0.9 - 300_000)

    def test_nguong_sau_phi(self):
        self.assertTrue(aff.thuc_nhan(251_000).co_khau_tru_thue)
        k = aff.thuc_nhan(251_000, nguong_tinh_tren="sau_phi")   # 251.000 × 0,9902 = 248.540,2 < 250.000
        self.assertFalse(k.co_khau_tru_thue)
        self.assertAlmostEqual(k.thuc_nhan, 248_540.2)

    def test_tu_don(self):
        k = aff.thuc_nhan_tu_don(150_000, 10, so_don=40, ty_le_huy_hoan=10, chi_phi_noi_dung=100_000)
        goc = 150_000 * 0.10 * 40 * 0.9                                         # 540.000
        self.assertAlmostEqual(k.hoa_hong_goc, goc)
        self.assertAlmostEqual(k.thuc_nhan, goc * 0.9902 * 0.9 - 100_000)

    def test_tiktok_canh_bao_va_tham_so(self):
        k = aff.thuc_nhan(500_000, san="tiktok")
        self.assertTrue(any("CHƯA XÁC MINH" in c for c in k.canh_bao))
        k2 = aff.thuc_nhan(500_000, san="tiktok", phi_nen_tang_pct=0, thue_pct=0)
        self.assertEqual(k2.thuc_nhan, 500_000)

    def test_lo_va_dau_vao_sai(self):
        self.assertTrue(any("LỖ" in c for c in aff.thuc_nhan(10_000, 50_000).canh_bao))
        for kw in (dict(hoa_hong_goc=-1), dict(hoa_hong_goc=1, nguong_tinh_tren="x"), dict(hoa_hong_goc=1, san="lazada")):
            with self.assertRaises(ThieuDuLieu):
                aff.thuc_nhan(**kw)
        with self.assertRaises(ThieuDuLieu):
            aff.hoa_hong_goc_tu_don(100, 120)


class TestDropship(unittest.TestCase):
    def dv(self, **kw):
        base = dict(san="shopee", nganh="Sac dep", gia_ban=200_000, gia_von=80_000, ngay_ban=NGAY, ty_le_hoan=10,
                    ship_tra_hang=30_000, ty_le_hong_hang_hoan=50)
        base.update(kw)
        return DauVao(**base)

    def test_tinh_tay_shopee(self):
        k = tinh_dropship(self.dv(), phi_ncc=5_000, ty_le_huy=10, mt=MT)
        phi_san = 0.17 * 200_000 + 0.06 * 200_000 + 3_000 + 0.015 * 200_000   # 52.000
        cm = 200_000 - 80_000 - 5_000 - phi_san                                 # 63.000
        chi_hoan = 5_000 + 30_000 + 0.5 * 80_000                                # 75.000
        ln = 0.9 * cm - 0.1 * chi_hoan                                          # 49.200
        self.assertAlmostEqual(k.don.cm, cm)
        self.assertAlmostEqual(k.don.ln, ln)
        self.assertAlmostEqual(k.ln_moi_don_dat, 0.9 * ln - 0.1 * 5_000)        # 43.780
        self.assertAlmostEqual(k.chi_ra_moi_don_dat, 0.9 * 85_000 + 0.1 * 5_000)  # 77.000
        self.assertAlmostEqual(k.tien_ve_moi_don_dat, 0.9 * (0.9 * (200_000 - phi_san) - 0.1 * 30_000))  # 117.180
        self.assertEqual(k.ngay_tre, 3 + 4 + 1)
        # tiền mặt − lãi = hàng hoàn còn bán được (tồn kho)
        self.assertAlmostEqual(k.ln_moi_don_dat - (k.tien_ve_moi_don_dat - k.chi_ra_moi_don_dat), 0.9 * 0.1 * 0.5 * 80_000)

    def test_tinh_tay_tiktok(self):
        dv = DauVao(san="tiktok", nganh="", gia_ban=150_000, gia_von=55_000, ngay_ban=NGAY, ty_le_hoan=8,
                    ship_tra_hang=25_000, ty_le_hong_hang_hoan=40, quang_cao_pct=10)
        k = tinh_dropship(dv, phi_ncc=4_000, ty_le_huy=5, chi_phi_moi_don_huy=8_000, ngay_giao=4, mt=MT)
        cm = 150_000 - 55_000 - 4_000 - (0.14 + 0.06 + 0.015) * 150_000 - 3_000  # 55.750
        chi_hoan = 4_000 + 25_000 + 0.4 * 55_000 + 3_000                         # 54.000 (phí đơn TikTok mất)
        ln_tqc = 0.92 * cm - 0.08 * chi_hoan                                     # 46.970
        self.assertAlmostEqual(k.ln_truoc_qc_moi_don_dat, 0.95 * ln_tqc - 0.05 * 8_000)            # 44.221,5
        self.assertAlmostEqual(k.ln_moi_don_dat, 0.95 * (ln_tqc - 15_000) - 0.05 * 8_000)          # 29.971,5
        self.assertEqual(k.ngay_tre, 4 + 8 + 1)

    def test_chu_ky(self):
        self.assertEqual(chu_ky_tien_ve("Shopee"), (4, 1))
        self.assertEqual(chu_ky_tien_ve("tiktok", "moi"), (8, 1))
        self.assertEqual(chu_ky_tien_ve("tiktok", "thuong"), (3, 1))
        with self.assertRaises(ThieuDuLieu):
            chu_ky_tien_ve("shopee", "mall")

    def test_dau_vao_sai(self):
        for kw in (dict(phi_ncc=-1), dict(ty_le_huy=100), dict(chi_phi_moi_don_huy=-5)):
            with self.assertRaises(ThieuDuLieu):
                tinh_dropship(self.dv(), mt=MT, **kw)

    def test_von_ung_truoc_on_dinh(self):
        v = von_ung_truoc(5, 77_000, 117_180, 8)
        self.assertEqual(v["von_ung_truoc_can"], 5 * 77_000 * 8)   # 3.080.000
        self.assertEqual(v["ngay_am_sau_nhat"], 7)
        v2 = von_ung_truoc(3, 100_000, 90_000, 5, so_ngay=30)
        self.assertIsNone(v2["ngay_so_du_cong_don_ve_0"])
        self.assertEqual(v2["von_ung_truoc_can"], 5 * 300_000 + 25 * 30_000)
        with self.assertRaises(ThieuDuLieu):
            von_ung_truoc(-1, 1, 1, 1)


def _d(**kw):
    base = dict(ngay="2026-12-01", thu_chi="chi", loai="cong_cu", mo_hinh="chung", kenh="chung", so_tien_vnd="1000")
    base.update(kw)
    return base


class TestSoLaiLo(unittest.TestCase):
    def test_so_mau_tinh_tay(self):
        dong = doc_so(SO_MAU)
        kq = kiem_cong_dot1(dong, date(2027, 1, 10))
        c = kq["cua_so_4_tuan"]
        self.assertEqual(c["tu"], "2026-12-14")
        self.assertEqual(c["thu"], 7_960_000 + 620_000 + 5_970_000)
        chi = (6_500_000 * 28 / 56 + 2_600_000 * 2 / 30 + 1_300_000 * 18 / 31
               + 3_200_000 + 200_000 + 2_066_800 + 119_400 + 120_000 + 15_000
               + 2_400_000 + 150_000 + 1_343_400 + 89_550 + 300_000)
        self.assertEqual(c["chi"], round(chi))                        # 14.182.322
        self.assertTrue(kq["dat_cong_dot1"])
        self.assertLess(kq["tu_dau_du_an"]["lai_rong"], 0)            # cổng ĐẠT nhưng cộng dồn từ đầu vẫn LỖ
        self.assertTrue(any("hang_mau" in x for x in kq["canh_bao"]))
        self.assertEqual(sum(c["theo_mo_hinh"].values()), c["lai_rong"])

    def test_phan_bo(self):
        d = kiem_dong(_d(so_tien_vnd="3000", phan_bo_tu="2026-12-01", phan_bo_den="2026-12-03"))
        self.assertAlmostEqual(d.phan_trong(date(2026, 12, 2), date(2026, 12, 2)), -1000)
        self.assertAlmostEqual(d.phan_trong(date(2026, 12, 4), date(2026, 12, 9)), 0)
        t = tong_hop([d], date(2026, 11, 1), date(2026, 12, 31))
        self.assertEqual(t["chi"], 3000)

    def test_theo_tuan(self):
        dong = doc_so(SO_MAU)
        w = theo_tuan(dong, date(2026, 11, 16), 8)
        self.assertEqual(len(w), 8)
        self.assertEqual(w[-1]["cong_don"], sum(x["lai_tuan"] for x in w))

    def test_dong_sai(self):
        for kw in (dict(thu_chi="x"), dict(loai="doanh_thu_don"), dict(mo_hinh="x"), dict(so_tien_vnd="-5"),
                   dict(so_tien_vnd="1.5e3"), dict(ngay="12/01/2026"), dict(phan_bo_tu="2026-12-01"),
                   dict(phan_bo_tu="2026-12-05", phan_bo_den="2026-12-01"), dict(kenh="lazada")):
            with self.subTest(kw), self.assertRaises(ThieuDuLieu):
                kiem_dong(_d(**kw))
        self.assertEqual(kiem_dong(_d(so_tien_vnd="1.500.000")).so_tien_vnd, 1_500_000)

    def test_ghi_va_doc_thu_muc_tam(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "so.csv"
            ghi_dong(p, _d(thu_chi="thu", loai="doanh_thu_don", mo_hinh="dropship", kenh="shopee", so_tien_vnd="5000"))
            ghi_dong(p, kiem_dong(_d()))
            dong = doc_so(p)
            self.assertEqual(len(dong), 2)
            self.assertEqual(tong_hop(dong, date(2026, 12, 1), date(2026, 12, 1))["lai_rong"], 4000)
            self.assertFalse(la_du_lieu_trong_repo(p))     # thư mục tạm nằm ngoài repo
            with self.assertRaises(ThieuDuLieu):
                ghi_dong(p, _d(thu_chi="?"))
            self.assertEqual(len(doc_so(p)), 2)              # dòng sai không bị ghi
            p2 = Path(td) / "thieu.csv"
            p2.write_text("ngay,thu_chi\n2026-12-01,chi\n", encoding="utf-8")
            with self.assertRaises(ThieuDuLieu):
                doc_so(p2)
        with self.assertRaises(ThieuDuLieu):
            doc_so(Path(tempfile.gettempdir()) / "khong-co-so-nay-123.csv")
        with self.assertRaises(ThieuDuLieu):
            kiem_cong_dot1([], date(2026, 12, 1))

    def test_khac_o_dia_windows(self):
        goc, mau = PureWindowsPath(r"C:\repo"), PureWindowsPath(r"C:\repo\apps\finance\du-lieu-mau")
        self.assertFalse(_trong_repo_ngoai_mau(PureWindowsPath(r"D:\Temp\so.csv"), goc, mau))  # không lỗi
        self.assertTrue(_trong_repo_ngoai_mau(PureWindowsPath(r"C:\repo\so.csv"), goc, mau))
        self.assertFalse(_trong_repo_ngoai_mau(PureWindowsPath(r"C:\repo\apps\finance\du-lieu-mau\a.csv"), goc, mau))
        with self.assertRaises(ValueError):   # lý do không dùng relpath
            ntpath.relpath(r"D:\Temp\so.csv", r"C:\repo")
        self.assertFalse(la_du_lieu_trong_repo(SO_MAU))
        self.assertTrue(la_du_lieu_trong_repo(THU_MUC / "so-that.csv"))

    def test_cli(self):
        out = io.StringIO()
        with redirect_stdout(out):
            self.assertEqual(so_lai_lo.main(["--so", str(SO_MAU), "--ngay-cuoi", "2027-01-10"]), 0)
        self.assertIn("CỔNG ĐỢT 1: ĐẠT", out.getvalue())
        self.assertIn("không đảm bảo lợi nhuận", out.getvalue())
        out = io.StringIO()
        with redirect_stdout(out):
            so_lai_lo.main(["--so", str(SO_MAU), "--ngay-cuoi", "2026-12-20", "--json"])
        self.assertIn("dat_cong_dot1", json.loads(out.getvalue()))
        err = io.StringIO()
        with redirect_stderr(err):
            self.assertEqual(so_lai_lo.main(["--so", "khong-co.csv", "--ngay-cuoi", "2027-01-10"]), 2)


class TestKichBan(unittest.TestCase):
    def test_tinh_tay_xau(self):
        kq = kich_ban.chay_tat_ca(MT)
        x = kq["kich_ban"][0]
        self.assertEqual(x["ten"], "XẤU")
        cm = 199_000 - 80_000 - 5_000 - (0.17 + 0.06 + 0.015) * 199_000 - 3_000   # 62.245
        ln_tqc = 0.88 * cm - 0.12 * (5_000 + 30_000 + 0.5 * 80_000)              # 45.775,6
        ln_dat = 0.9 * ln_tqc - 0.1 * 5_000                                       # 40.698,04
        self.assertEqual(x["ln_truoc_qc_moi_don_dropship"], round(ln_dat))
        hh = 150_000 * 0.05 * 0.85 * 0.9902 * 0.9                                 # 5.681,27
        self.assertEqual(x["hoa_hong_thuc_nhan_moi_don_aff"], round(hh))
        self.assertEqual(x["tuan"][0]["lai_tuan"], -19_500_000 / 8)               # tuần 1: chỉ chi cố định
        self.assertEqual(x["hoa_von_don_dropship_8_tuan"], round(19_500_000 / ln_dat))
        self.assertEqual(x["roas_hoa_von"], round(199_000 / ln_dat, 2))
        self.assertFalse(x["quang_cao_lai"])

    def test_ba_kich_ban_va_cong(self):
        kq = kich_ban.chay_tat_ca(MT)
        ten = [k["ten"] for k in kq["kich_ban"]]
        self.assertEqual(ten, ["XẤU", "VỪA", "TỐT"])
        lai = [k["lai_8_tuan"] for k in kq["kich_ban"]]
        self.assertTrue(lai[0] < lai[1] < lai[2])
        for k in kq["kich_ban"]:
            self.assertEqual(k["dat_cong_dot1"], k["lai_4_tuan_cuoi"] >= 0)
            self.assertAlmostEqual(k["tuan"][-1]["cong_don"], k["lai_8_tuan"], delta=1)
        self.assertIn("GIẢ ĐỊNH", kq["ghi_chu"])
        md = kich_ban.bang_markdown(kq)
        self.assertIn("KHÔNG ĐẠT", md)
        out = io.StringIO()
        with redirect_stdout(out):
            kich_ban.main([])
        self.assertIn("không đảm bảo lợi nhuận", out.getvalue())


class TestNhanPhi(unittest.TestCase):
    """P12 2.2: tách tỷ lệ phí CHƯA gồm / GỒM thuế khấu trừ."""

    def test_vi_du_a(self):
        kq = MT.tinh(DauVao(san="shopee", nganh="Thoi trang (tat ca)", gia_ban=150_000, gia_von=60_000,
                            dong_goi=3_000, ngay_ban=NGAY, che_do_khoang="giua"))
        self.assertAlmostEqual(kq.ty_le_phi_san_aff_chua_thue, (22_500 + 9_000 + 3_000) / 150_000, places=6)  # 23,0%
        self.assertAlmostEqual(kq.ty_le_phi_gom_thue_khau_tru, (22_500 + 9_000 + 3_000 + 2_250) / 150_000, places=6)

    def test_cli_nhan(self):
        from taichinh.__main__ import main as cli
        out = io.StringIO()
        with redirect_stdout(out):
            cli(["--san", "shopee", "--nganh", "Sac dep", "--gia-ban", "100000", "--gia-von", "40000",
                 "--ngay-ban", "2026-11-12"])
        self.assertIn("CHƯA gồm thuế khấu trừ", out.getvalue())


class TestViDuKiemKhop(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tep = json.loads(vi_du_kiem_khop.TEP.read_text(encoding="utf-8"))
        cls.vd = {v["id"]: v for v in cls.tep["vi_du"]}

    def test_du_va_phu(self):
        self.assertGreaterEqual(len(self.tep["vi_du"]), 10)
        loai = {v["loai"] for v in self.tep["vi_du"]}
        self.assertTrue({"don", "dropship", "affiliate", "von_ung_truoc", "so_lai_lo"} <= loai)
        san = {v["dau_vao"].get("san", "shopee") for v in self.tep["vi_du"]}
        self.assertTrue({"shopee", "tiktok"} <= san)
        self.assertEqual(len(self.vd), len(self.tep["vi_du"]))   # id không trùng

    def test_tep_dong_bo_voi_ma(self):
        moi = json.loads(json.dumps(vi_du_kiem_khop.tao(MT), ensure_ascii=False))
        self.assertEqual(self.tep, moi, "tệp lệch mã: chạy python3 -m taichinh.vi_du_kiem_khop rồi rà diff")

    def test_tinh_tay_5_vi_du(self):
        """Kiểm ngược ≥ 5 ví dụ trong tệp bằng phép tính tay (độc lập với mã)."""
        m = lambda i: self.vd[i]["mong_doi"]
        # don-03: 200.000 − 80.000 − 2.000 − 17%·200k − 6%·200k − 3.000 − 1,5%·200k = 66.000; QC 10% = 20.000
        self.assertAlmostEqual(m("don-03")["cm"], 66_000)
        self.assertAlmostEqual(m("don-03")["ln"], 46_000)
        # don-04: voucher 5,5%·2tr = 110.000 → trần 50.000
        self.assertAlmostEqual(m("don-04")["cm"], 2_000_000 - 500_000 - 340_000 - 120_000 - 3_000 - 50_000 - 30_000)
        # don-06 TikTok: CM = 200k − 80k − 15%·200k − 6%·200k − 3.000 − 1,5%·200k = 72.000;
        #   LN = 0,9·72.000 − 0,1·(30.000 + 3.000) = 61.500
        self.assertAlmostEqual(m("don-06")["ln_truoc_qc"], 0.9 * 72_000 - 0.1 * 33_000)
        # don-07 TikTok mặc định 14%, VXP 5%: Rev 170.000
        rev = 170_000
        cm = rev - 70_000 - 2_000 - (0.14 + 0.06 + 0.05 + 0.015) * rev - 3_000
        self.assertAlmostEqual(m("don-07")["cm"], cm)
        self.assertAlmostEqual(m("don-07")["ln"], 0.94 * cm - 0.06 * (2_000 + 25_000 + 0.3 * 70_000 + 3_000) - 0.08 * rev)
        # aff-02, aff-03, aff-don-01
        self.assertAlmostEqual(m("aff-02")["thuc_nhan"], 222_795)
        self.assertAlmostEqual(m("aff-03")["thuc_nhan"], 769_416)
        self.assertAlmostEqual(m("aff-don-01")["thuc_nhan"], 540_000 * 0.9902 * 0.9 - 100_000)
        # dropship-01, von-01
        self.assertAlmostEqual(m("dropship-01")["ln_moi_don_dat"], 43_780)
        self.assertEqual(m("von-01")["von_ung_truoc_can"], 3_080_000)
        # so-01: 5,6 tr công cụ / 57 ngày × 28 ngày trong cửa sổ
        c = m("so-01")["cua_so_4_tuan"]
        self.assertEqual(c["lai_rong"], round(6_000_000 + 400_000 - 2_400_000 - 5_600_000 * 28 / 57))
        self.assertTrue(m("so-01")["dat_cong_dot1"])
        self.assertEqual(m("so-01")["tu_dau_du_an"]["lai_rong"], 6_400_000 - 2_400_000 - 5_600_000 - 1_500_000)

    def test_phi_ap_dung_tai_tao_cm(self):
        """Bản JS chỉ có phi_ap_dung cũng phải dựng lại được CM / LN (kiểm công thức trong README)."""
        for v in self.tep["vi_du"]:
            if v["loai"] != "don":
                continue
            with self.subTest(v["id"]):
                d, f, m = v["dau_vao"], v["phi_ap_dung"], v["mong_doi"]
                rev = d["gia_ban"] - d.get("giam_gia_shop", 0)
                a = d.get("hoa_hong_aff_shop_tra", 0)
                vs = min(f["voucher_san_pct"] / 100 * rev, f["voucher_san_tran_vnd"]) if d.get("tham_gia_voucher_san") else 0
                dg, sx = d.get("dong_goi", 0), d.get("ship_shop_chiu", 0)
                cm = (rev - d["gia_von"] - dg - sx - (f["phi_nganh_pct"] + f["phi_giao_dich_pct"] + a
                      + f["thue_khau_tru_pct"]) / 100 * rev - f["phi_moi_don_vnd"] - vs)
                self.assertAlmostEqual(m["cm"], cm, delta=0.5)
                r = d.get("ty_le_hoan", 0) / 100
                hong = d.get("ty_le_hong_hang_hoan", 30) / 100
                chi_hoan = dg + sx + f["ship_tra_hang_vnd"] + hong * d["gia_von"] + (
                    f["phi_moi_don_vnd"] if f["phi_moi_don_mat_khi_hoan"] else 0)
                ln = (1 - r) * cm - r * chi_hoan - d.get("quang_cao_pct", 0) / 100 * rev
                self.assertAlmostEqual(m["ln"], ln, delta=0.5)


if __name__ == "__main__":
    unittest.main()
