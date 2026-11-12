"""Kiểm thử script kiem_tra.py: dữ liệu thật phải ĐẠT, dữ liệu hỏng phải bị bắt.

Chạy:  python3 -m unittest apps/radar/test_kiem_tra.py   (từ thư mục gốc repo)
"""
import csv
import os
import shutil
import sys
import tempfile
import ntpath
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kiem_tra as kt  # noqa: E402


class KiemTra(unittest.TestCase):
    def setUp(self):
        self.tam = tempfile.mkdtemp()
        for d in ("mau", "du-lieu", "nhap-tay"):
            shutil.copytree(os.path.join(kt.GOC, d), os.path.join(self.tam, d))

    def tearDown(self):
        shutil.rmtree(self.tam)

    def ghi_dong(self, rel, dong):
        with open(os.path.join(self.tam, rel), "a", encoding="utf-8", newline="") as f:
            csv.writer(f).writerow(dong)

    def sua_o(self, rel, so_dong, cot, gia_tri):
        p = os.path.join(self.tam, rel)
        with open(p, encoding="utf-8", newline="") as f:
            r = list(csv.reader(f))
        r[so_dong][r[0].index(cot)] = gia_tri
        with open(p, "w", encoding="utf-8", newline="") as f:
            csv.writer(f).writerows(r)

    def chay(self):
        return kt.kiem_tat_ca(self.tam)[1]

    def test_du_lieu_that_dat(self):
        so_tep, loi = kt.kiem_tat_ca()
        self.assertEqual(loi, [])
        self.assertEqual(so_tep, 13)

    def test_du_20_nhom(self):
        _, ds = kt.doc_csv(os.path.join(kt.GOC, "du-lieu", "nhom-ung-vien.csv"))
        self.assertEqual(len([d for d in ds if any(d)]), 20)

    def test_sai_cot(self):
        p = os.path.join(self.tam, "mau", "product.csv")
        with open(p, "w", encoding="utf-8") as f:
            f.write("product_id,name\n")
        self.assertTrue(any("sai cột" in x for x in self.chay()))

    def test_o_nguon_trong(self):
        self.sua_o("du-lieu/nhom-ung-vien.csv", 1, "source_id", "")
        self.assertTrue(any("ô nguồn 'source_id' trống" in x for x in self.chay()))

    def test_ngay_trong(self):
        self.sua_o("du-lieu/source.csv", 1, "captured_at", "")
        self.assertTrue(any("captured_at" in x for x in self.chay()))

    def test_nguon_khong_ton_tai(self):
        self.sua_o("du-lieu/nhom-ung-vien.csv", 1, "source_id", "S99")
        self.assertTrue(any("S99" in x for x in self.chay()))

    def test_diem_vuot_toi_da(self):
        self.sua_o("du-lieu/nhom-ung-vien.csv", 1, "video", "11")
        self.assertTrue(any("ngoài [0,10]" in x for x in self.chay()))

    def test_tong_sai(self):
        self.sua_o("du-lieu/nhom-ung-vien.csv", 1, "diem_so_bo", "99")
        self.assertTrue(any("khác tổng" in x for x in self.chay()))

    def test_fee_ref_sai(self):
        self.sua_o("du-lieu/nhom-ung-vien.csv", 1, "fee_ref", "Shopee|phi_co_dinh|Khong co")
        self.assertTrue(any("fee_ref" in x for x in self.chay()))

    def test_lo_thu_qua_300_usd_va_chua_duyet(self):
        self.ghi_dong("mau/trial_batch.csv",
                      ["B1", "P1", "SUP1", "50", "350", "2026-12-01", "", "", "", "",
                       "", "KHONG", "S01", "2026-11-12"])
        loi = self.chay()
        self.assertTrue(any("> 300 USD" in x for x in loi))
        self.assertTrue(any("chủ dự án duyệt" in x for x in loi))

    # --- Các lỗ hổng KTS tìm ra ở audit vòng 2 (12/11/2026) ---
    def test_source_id_chi_co_dau_cham_phay(self):
        self.sua_o("du-lieu/nhom-ung-vien.csv", 1, "source_id", ";")
        self.assertTrue(any("chỉ có dấu ';'" in x for x in self.chay()))

    def test_chi_nguon_noi_bo_ma_co_diem_nhu_cau(self):
        self.sua_o("du-lieu/nhom-ung-vien.csv", 1, "source_id", "S21")
        self.assertTrue(any("chỉ có nguồn nội bộ" in x for x in self.chay()))

    def test_mo_hinh_ngoai_danh_sach(self):
        self.sua_o("du-lieu/nhom-ung-vien.csv", 1, "mo_hinh", "mua_dut")
        self.assertTrue(any("mo_hinh" in x for x in self.chay()))

    def test_legal_cap_nhom_15(self):
        # N04 (dòng 4): legal 6 -> 15, sửa tổng cho khớp để chỉ còn lỗi legal
        self.sua_o("du-lieu/nhom-ung-vien.csv", 4, "legal", "15")
        self.sua_o("du-lieu/nhom-ung-vien.csv", 4, "diem_so_bo", "31")
        loi = self.chay()
        self.assertTrue(any("legal cấp nhóm" in x for x in loi))
        self.assertFalse(any("khác tổng" in x for x in loi))

    def test_ngay_khong_that(self):
        self.sua_o("du-lieu/nhom-ung-vien.csv", 1, "captured_at", "2026-13-45")
        self.assertTrue(any("không phải ngày thật" in x for x in self.chay()))

    def test_fee_ref_trong(self):
        self.sua_o("du-lieu/nhom-ung-vien.csv", 1, "fee_ref", "")
        self.assertTrue(any("fee_ref trống" in x for x in self.chay()))

    def test_demand_cap_nhom_qua_10(self):
        self.sua_o("du-lieu/nhom-ung-vien.csv", 1, "demand", "20")
        self.sua_o("du-lieu/nhom-ung-vien.csv", 1, "diem_so_bo", "38")
        self.assertTrue(any("demand cấp nhóm" in x for x in self.chay()))

    def test_do_tin_cay_cao_hon_nguon(self):
        self.sua_o("du-lieu/nhom-ung-vien.csv", 1, "do_tin_cay", "CAO")
        self.assertTrue(any("cao hơn nguồn yếu nhất" in x for x in self.chay()))

    def test_type_nguon_ngoai_danh_sach(self):
        self.sua_o("du-lieu/source.csv", 1, "type", "la_lam")
        self.assertTrue(any("type 'la_lam'" in x for x in self.chay()))

    def test_url_tep_noi_bo_khong_ton_tai(self):
        self.sua_o("du-lieu/source.csv", 19, "url", "bao-cao/khong-co.md")
        self.assertTrue(any("không phải tệp có trong repo" in x for x in self.chay()))

    # --- Lỗ hổng KTS tìm ra khi kiểm lại (12/11/2026) ---
    def test_ngay_tuong_lai(self):
        self.sua_o("du-lieu/nhom-ung-vien.csv", 1, "captured_at", "2030-01-01")
        self.assertTrue(any("tương lai" in x for x in self.chay()))

    def test_url_rong(self):
        self.sua_o("du-lieu/source.csv", 1, "url", "http://")
        self.assertTrue(any("không phải link" in x for x in self.chay()))

    def test_ma_nhom_trung(self):
        self.sua_o("du-lieu/nhom-ung-vien.csv", 2, "nhom_id", "N01")
        self.assertTrue(any("trùng mã N01" in x for x in self.chay()))

    def test_score_hop_le(self):
        self.ghi_dong("mau/score.csv",
                      ["SC1", "P1", "dropship", "2026-11-12", "10", "CHƯA ĐO", "CHƯA ĐO", "10",
                       "CHƯA ĐO", "CHƯA ĐO", "6", "26", "Shopee|phi_co_dinh|Van phong pham",
                       "", "", "theo_doi", "S04", "2026-11-12"])
        self.assertEqual(self.chay(), [])

    # --- Đợt 1: chấm tách affiliate / dropship ---
    def dong_score(self, mo_hinh, margin, bien, fee="Shopee|phi_co_dinh|Van phong pham"):
        tong = 10 + 10 + 6 + (float(margin) if margin != "CHƯA ĐO" else 0)
        return ["SC9", "P1", mo_hinh, "2026-11-12", "10", "CHƯA ĐO", margin, "10",
                "CHƯA ĐO", "CHƯA ĐO", "6", f"{tong:g}", fee, bien, "", "theo_doi", "S04", "2026-11-12"]

    def test_score_ca_hai_bi_chan(self):
        self.ghi_dong("mau/score.csv", self.dong_score("ca_hai", "CHƯA ĐO", ""))
        self.assertTrue(any("HAI dòng riêng" in x for x in self.chay()))

    def test_score_dropship_dung_nguong(self):
        self.ghi_dong("mau/score.csv", self.dong_score("dropship", "15", "16.25"))
        self.assertEqual(self.chay(), [])

    def test_score_dropship_sai_nguong(self):
        self.ghi_dong("mau/score.csv", self.dong_score("dropship", "25", "16.25"))
        self.assertTrue(any("khác ngưỡng dropship" in x for x in self.chay()))

    def test_score_affiliate_khong_can_fee_ref(self):
        self.ghi_dong("mau/score.csv", self.dong_score("affiliate", "25", "8.47", fee=""))
        self.assertEqual(self.chay(), [])

    def test_score_affiliate_dung_nguong_rieng(self):
        # 6% thực nhận: affiliate = 15 điểm; nếu dùng ngưỡng dropship sẽ là 0 → phải báo lỗi
        self.ghi_dong("mau/score.csv", self.dong_score("affiliate", "0", "6", fee=""))
        self.assertTrue(any("phải 15" in x for x in self.chay()))

    def test_score_thieu_bien_pct(self):
        self.ghi_dong("mau/score.csv", self.dong_score("dropship", "8", ""))
        self.assertTrue(any("thiếu bien_pct" in x for x in self.chay()))

    def test_phi_theo_nhom_bi_sua_tay(self):
        self.sua_o("du-lieu/phi-theo-nhom.csv", 1, "tong_phi_pct_gia_100k", "24.0")
        self.assertTrue(any("không khớp phép tính lại" in x for x in self.chay()))

    # --- Bảng nhập tay 4 nhóm ---
    DONG_TOT = ["N18", "shopee", "2026-11-12", "Vòng cổ mèo có chuông", "https://shopee.vn/vi-du",
                "35.000", "1,2k", "4,8", "10", "18000", ""]

    def test_nhap_tay_dong_tot(self):
        self.ghi_dong("nhap-tay/4-nhom.csv", self.DONG_TOT)
        self.assertEqual(self.chay(), [])

    def test_nhap_tay_loi(self):
        for i, gia_tri, chu in ((0, "N03", "4 nhóm"), (1, "lazada", "shopee hoặc tiktok"),
                                (2, "2030-01-01", "ngay_xem"), (4, "", "link trống"),
                                (5, "ba mươi", "gia_ban_vnd"), (6, "nhiều", "da_ban"),
                                (7, "6", "so_sao"), (8, "120", "hoa_hong_pct"), (3, "", "ten_san_pham")):
            with self.subTest(cot=i):
                self.tearDown()
                self.setUp()
                d = list(self.DONG_TOT)
                d[i] = gia_tri
                self.ghi_dong("nhap-tay/4-nhom.csv", d)
                self.assertTrue(any(chu in x for x in self.chay()), (chu, self.chay()))

    def test_doc_so(self):
        self.assertEqual(kt.so_tien("35.000"), 35000)
        self.assertEqual(kt.so_tien("35 000đ"), 35000)
        self.assertEqual(kt.so_da_ban("1,2k"), 1200)
        self.assertEqual(kt.so_da_ban("1.234"), 1234)
        with self.assertRaises(ValueError):
            kt.so_tien("3,5tr")

    def test_nguong_bien(self):
        self.assertEqual([kt.diem_bien("dropship", x) for x in (25, 20, 19.9, 12, 8, 7.9)],
                         [25, 25, 15, 15, 8, 0])
        self.assertEqual([kt.diem_bien("affiliate", x) for x in (8, 7.9, 5, 3, 2.9)], [25, 15, 15, 8, 0])


class KhacO(unittest.TestCase):
    """Lỗi Windows (audit chuyến 1): repo ở D:, thư mục tạm ở C: → relpath báo ValueError.

    Mô phỏng trên mọi máy: ntpath (bản Windows của os.path) và vá os.path.relpath để báo đúng lỗi đó.
    """

    def test_ntpath_khac_o_khong_hong(self):
        # ntpath.relpath thật sự báo ValueError khi khác ổ — kiểm rằng hàm in đường dẫn đầy đủ
        with self.assertRaises(ValueError):
            ntpath.relpath("C:\\Temp\\x\\mau\\product.csv", "D:\\daovang")
        ra = kt.ten_tep("C:\\Temp\\x\\mau\\product.csv", "D:\\daovang", p=ntpath)
        self.assertEqual(ra, "C:\\Temp\\x\\mau\\product.csv")

    def test_ntpath_cung_o_van_tuong_doi(self):
        ra = kt.ten_tep("D:\\daovang\\apps\\radar\\mau\\a.csv", "D:\\daovang", p=ntpath)
        self.assertEqual(ra, "apps\\radar\\mau\\a.csv")

    def _relpath_khac_o(self, path, start=os.curdir):
        raise ValueError("path is on mount 'C:', start on mount 'D:'")

    def test_kiem_ca_bo_khi_khac_o(self):
        tam = tempfile.mkdtemp()
        try:
            for d in ("mau", "du-lieu", "nhap-tay"):
                shutil.copytree(os.path.join(kt.GOC, d), os.path.join(tam, d))
            with mock.patch.object(kt.os.path, "relpath", self._relpath_khac_o):
                so_tep, loi = kt.kiem_tat_ca(tam)
                self.assertEqual(loi, [])
                self.assertEqual(so_tep, 13)
                # dữ liệu hỏng vẫn phải được báo (không văng ValueError)
                p = os.path.join(tam, "du-lieu", "nhom-ung-vien.csv")
                with open(p, encoding="utf-8", newline="") as f:
                    r = list(csv.reader(f))
                r[1][r[0].index("diem_so_bo")] = "99"
                r[2][0] = r[1][0]
                with open(p, "w", encoding="utf-8", newline="") as f:
                    csv.writer(f).writerows(r)
                _, loi = kt.kiem_tat_ca(tam)
            self.assertTrue(any("khác tổng" in x for x in loi))
            self.assertTrue(any("trùng mã" in x for x in loi))
            self.assertTrue(all(os.path.isabs(x.split(" dòng ")[0]) for x in loi))
        finally:
            shutil.rmtree(tam)


if __name__ == "__main__":
    unittest.main()
