"""Kiểm thử script kiem_tra.py: dữ liệu thật phải ĐẠT, dữ liệu hỏng phải bị bắt.

Chạy:  python3 -m unittest apps/radar/test_kiem_tra.py   (từ thư mục gốc repo)
"""
import csv
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kiem_tra as kt  # noqa: E402


class KiemTra(unittest.TestCase):
    def setUp(self):
        self.tam = tempfile.mkdtemp()
        for d in ("mau", "du-lieu"):
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
        self.assertEqual(so_tep, 11)

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

    def test_score_hop_le(self):
        self.ghi_dong("mau/score.csv",
                      ["SC1", "P1", "2026-11-12", "10", "CHƯA ĐO", "CHƯA ĐO", "10",
                       "CHƯA ĐO", "CHƯA ĐO", "6", "26", "Shopee|phi_co_dinh|Van phong pham",
                       "", "theo_doi", "S04", "2026-11-12"])
        self.assertEqual(self.chay(), [])


if __name__ == "__main__":
    unittest.main()
