"""Kiểm thử lõi. Chạy: python3 -m unittest discover -s packages/core/tests"""
import io
import json
import logging
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from daovang_core import ThieuKhoa, che, doc_cau_hinh, lay_khoa, tao_nhat_ky  # noqa: E402

KHOA_GIA = "sk-" + "GIA" * 8  # khóa GIẢ, ghép chuỗi để không lọt bộ quét


class TestChe(unittest.TestCase):
    def test_sdt(self):
        for s in ["0912345678", "0912 345 678", "+84912345678", "84 912.345.678", "028 3822 1234"]:
            self.assertNotIn("345", che(f"khach goi {s} hoi hang"), s)

    def test_email_khoa_so_dai(self):
        r = che(f"mail a.b@vidu.vn key {KHOA_GIA} cccd 012345678901 Bearer abcdefghijklmnop")
        self.assertNotIn("a.b@vidu.vn", r)
        self.assertNotIn(KHOA_GIA, r)
        self.assertNotIn("012345678901", r)
        self.assertNotIn("abcdefghijklmnop", r)

    def test_khong_che_nham(self):
        s = "Don 2411ABCD SKU AO-01 so luong 2 gia 150000 VND ngay 2026-11-12 phi 13.5%"
        self.assertEqual(che(s), s)


class TestNhatKy(unittest.TestCase):
    def _log(self):
        buf = io.StringIO()
        log = tao_nhat_ky(f"test{id(buf)}", handler=logging.StreamHandler(buf))
        return log, buf

    def test_che_trong_log_va_tham_so(self):
        log, buf = self._log()
        log.info("khach %s dat don, sdt %s", "K1", "0987654321")
        log.info({"ma_don": "D1", "sdt": "0987654321", "dia_chi": "12 Le Loi"})
        out = buf.getvalue()
        self.assertNotIn("0987654321", out)
        self.assertNotIn("12 Le Loi", out)
        self.assertIn("D1", out)

    def test_che_truong_extra(self):
        buf = io.StringIO()
        log = tao_nhat_ky(f"extra{id(buf)}", handler=logging.StreamHandler(buf))
        log.handlers[0].setFormatter(logging.Formatter("%(message)s %(email)s"))
        log.info("x", extra={"email": "a@b.vn"})
        self.assertNotIn("a@b.vn", buf.getvalue())


class TestCauHinh(unittest.TestCase):
    def test_uu_tien_va_ep_kieu(self):
        with tempfile.TemporaryDirectory() as t:
            p = Path(t) / "c.json"
            p.write_text(json.dumps({"so_ngay": 7, "che_do_thu": True}), encoding="utf-8")
            c = doc_cau_hinh(p, {"so_ngay": 1, "che_do_thu": False, "san": "Shopee"},
                             {"DAOVANG_SO_NGAY": "30"})
            self.assertEqual(c, {"so_ngay": 30, "che_do_thu": True, "san": "Shopee"})

    def test_tu_choi_bi_mat_trong_tep(self):
        with tempfile.TemporaryDirectory() as t:
            p = Path(t) / "c.json"
            p.write_text(json.dumps({"api_key": "x"}), encoding="utf-8")
            with self.assertRaises(ValueError):
                doc_cau_hinh(p)

    def test_lay_khoa(self):
        self.assertEqual(lay_khoa("K", moi_truong={"K": " abc "}), "abc")
        self.assertIsNone(lay_khoa("K", bat_buoc=False, moi_truong={}))
        with self.assertRaises(ThieuKhoa) as e:
            lay_khoa("K", moi_truong={"K": ""})
        self.assertNotIn("abc", str(e.exception))


if __name__ == "__main__":
    unittest.main()
