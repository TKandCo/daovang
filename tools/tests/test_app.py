"""Kiểm thử app HTML + đóng gói + kiểm khớp JS ↔ Python. Chạy: python3 -m unittest discover -s tools/tests

Cần node để chạy phần JS. Thiếu node: các kiểm thử JS bị BỎ QUA trên máy, nhưng HỎNG trên GitHub Actions
(biến môi trường GITHUB_ACTIONS hoặc DAOVANG_CAN_NODE=1).
"""
import importlib.util
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

GOC = Path(__file__).resolve().parents[2]
APP = GOC / "app" / "daovang.html"
CSV = GOC / "bao-cao" / "dot0" / "bang-phi-v1.csv"


def nap(ten, tep):
    spec = importlib.util.spec_from_file_location(ten, GOC / "tools" / tep)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


dg = nap("dong_goi_app", "dong-goi-app.py")
kk = nap("kiem_khop", "kiem-khop.py")
qk = nap("quet_khoa_app", "quet-khoa.py")
ckt = nap("chay_kiem_thu", "chay-kiem-thu.py")

NODE = kk.tim_node()
CAN_NODE = bool(os.environ.get("GITHUB_ACTIONS") or os.environ.get("DAOVANG_CAN_NODE"))


def can_node(test):
    def boc(self):
        if not NODE:
            if CAN_NODE:
                self.fail("thiếu node trên máy kiểm thử bắt buộc (Actions)")
            self.skipTest("thiếu node")
        return test(self)
    boc.__name__ = test.__name__
    return boc


def cam_duong_tuong_doi():
    """Giả lập Windows khi thư mục tạm khác ổ đĩa với repo: mọi phép tính đường dẫn tương đối đều nổ."""
    def no(*a, **k):
        raise ValueError("path is on mount 'C:', start on mount 'D:'")
    return [mock.patch("os.path.relpath", no), mock.patch.object(Path, "relative_to", no)]


class TestDongGoi(unittest.TestCase):
    def test_app_khop_nguon(self):
        f = io.StringIO()
        with redirect_stdout(f):
            self.assertEqual(dg.main(["--kiem"]), 0, "app/daovang.html cũ — chạy python3 tools/dong-goi-app.py")

    def test_kiem_bat_duoc_tep_cu(self):
        with tempfile.TemporaryDirectory() as t:
            cu = Path(t) / "daovang.html"
            cu.write_text(APP.read_text(encoding="utf-8").replace("Lợi nhuận mỗi đơn", "X", 1), encoding="utf-8")
            with redirect_stdout(io.StringIO()):
                self.assertEqual(dg.main(["--kiem", "--ra", str(cu)]), 1)

    def test_crlf_van_khop(self):
        # Windows có thể đổi xuống dòng thành CRLF khi checkout
        with tempfile.TemporaryDirectory() as t:
            p = Path(t) / "daovang.html"
            p.write_bytes(dg.chuan_xuong_dong(APP.read_bytes()).replace(b"\n", b"\r\n"))
            with redirect_stdout(io.StringIO()):
                self.assertEqual(dg.main(["--kiem", "--ra", str(p)]), 0)

    def test_moi_tep_nguon_crlf_van_dat(self):
        """KTS 13/11: mọi tệp nguồn (khung.html, *.js, bảng phí CSV) và tệp app đều CRLF → vẫn ĐẠT, cùng mã băm."""
        crlf = lambda b: dg.chuan_xuong_dong(b).replace(b"\n", b"\r\n")  # noqa: E731
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            (t / "src").mkdir()
            for f in (GOC / "app" / "src").iterdir():
                (t / "src" / f.name).write_bytes(crlf(f.read_bytes()))
            (t / "bp.csv").write_bytes(crlf(CSV.read_bytes()))
            (t / "app.html").write_bytes(crlf(APP.read_bytes()))
            self.assertIn(b"\r\n", (t / "bp.csv").read_bytes())
            self.assertEqual(dg.dung(t / "bp.csv", t / "src"), dg.doc(APP))
            self.assertEqual(dg.du_lieu_bang_phi(t / "bp.csv")["sha256"], dg.du_lieu_bang_phi()["sha256"])
            with mock.patch.object(dg, "NGUON", t / "src"):
                with redirect_stdout(io.StringIO()):
                    self.assertEqual(dg.main(["--kiem", "--bang-phi", str(t / "bp.csv"), "--ra", str(t / "app.html")]), 0)
            if NODE:  # lõi JS trong tệp app CRLF vẫn chạy và khớp Python
                with redirect_stdout(io.StringIO()):
                    self.assertEqual(kk.main(["--so-ngau-nhien", "10", "--app", str(t / "app.html")]), 0)

    def test_json_nhung_an_toan(self):
        s = dg.json_an_toan({"a": "</script><b>& "})
        self.assertNotIn("<", s)
        self.assertNotIn(" ", s)
        self.assertEqual(json.loads(s), {"a": "</script><b>& "})

    def test_bang_phi_du_dong(self):
        d = dg.du_lieu_bang_phi()
        so_dong_csv = len(CSV.read_text(encoding="utf-8-sig").strip().splitlines()) - 1
        self.assertEqual(d["so_dong_csv"], so_dong_csv)
        self.assertEqual(len(d["sha256"]), 64)
        self.assertTrue(any(x["suy_tu_ghi_chu"] for x in d["dong"]), "phải có dòng mức cũ suy từ ghi chú")

    def test_khac_o_dia_windows(self):
        """Thư mục tạm khác ổ: đóng gói từ CSV + nguồn chép sang thư mục tạm, ghi ra thư mục tạm."""
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            shutil.copytree(GOC / "app" / "src", t / "src")
            shutil.copy(CSV, t / "bp.csv")
            ps = cam_duong_tuong_doi()
            for p in ps:
                p.start()
            try:
                ra = dg.dung(t / "bp.csv", t / "src")
                (t / "out.html").write_text(ra, encoding="utf-8")
                with redirect_stdout(io.StringIO()):
                    self.assertEqual(dg.main(["--kiem", "--bang-phi", str(t / "bp.csv"), "--ra", str(t / "out.html")]), 0)
                    self.assertEqual(ckt.tim_mo_coi(), [])
            finally:
                for p in ps:
                    p.stop()


class TestAppAnToan(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = APP.read_text(encoding="utf-8")
        cls.ma = re.sub(r'<script id="bang-phi"[^>]*>.*?</script>', "", cls.html, flags=re.S)  # bỏ dữ liệu bảng phí

    def test_mot_tep_khong_goi_mang(self):
        self.assertIn("Content-Security-Policy", self.html)
        self.assertIn("default-src 'none'", self.html)
        self.assertIn("connect-src 'none'", self.html)
        for cam in (r"<script[^>]+src=", r"<link\b", r"<iframe", r"\bfetch\(", r"XMLHttpRequest", r"WebSocket",
                    r"sendBeacon", r"\bimport\(", r"@import", r"url\(\s*['\"]?https?:", r"src=['\"]https?:",
                    r"href=['\"]https?:", r"EventSource", r"navigator\.serviceWorker"):
            self.assertIsNone(re.search(cam, self.ma, re.I), f"app có '{cam}' — không được gọi mạng")

    def test_khong_du_lieu_khach(self):
        self.assertIsNone(re.search(r"(?<!\d)(?:\+?84|0)[35789]\d{8}(?!\d)", self.html), "nghi số điện thoại")
        self.assertIsNone(re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", self.html), "nghi email")

    def test_quet_khoa_sach(self):
        self.assertEqual(qk.quet_noi_dung("app/daovang.html", self.html), [])
        for ten in ("taichinh.js", "giao-dien.js", "khung.html"):
            p = GOC / "app" / "src" / ten
            self.assertEqual(qk.quet_noi_dung(ten, p.read_text(encoding="utf-8")), [])

    def test_dong_khong_dam_bao_va_kho_412(self):
        self.assertIn("không đảm bảo lợi nhuận", self.html)
        self.assertIn('name="viewport" content="width=device-width', self.html)
        self.assertIn("localStorage", self.html)
        self.assertIn("Tải bản sao lưu", self.html)

    def test_kich_thuoc(self):
        self.assertLess(APP.stat().st_size, 1_000_000)


class TestKiemKhop(unittest.TestCase):
    @can_node
    def test_dat_tren_app_that(self):
        f = io.StringIO()
        with redirect_stdout(f):
            ma = kk.main(["--so-ngau-nhien", "120"])
        self.assertEqual(ma, 0, f.getvalue())
        self.assertIn("12/12 khớp", f.getvalue())

    def _app_hong(self, cu, moi):
        t = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, t, True)
        html = APP.read_text(encoding="utf-8")
        self.assertIn(cu, html)
        p = Path(t) / "hong.html"
        p.write_text(html.replace(cu, moi, 1), encoding="utf-8")
        return p

    @can_node
    def test_bat_lech_cong_thuc(self):
        p = self._app_hong("var qc = dv.quang_cao_pct / 100 * rev;", "var qc = dv.quang_cao_pct / 100 * rev + 2;")
        with redirect_stdout(io.StringIO()):
            self.assertEqual(kk.main(["--so-ngau-nhien", "40", "--app", str(p)]), 1)

    @can_node
    def test_lech_duoi_1_dong_van_dat(self):
        p = self._app_hong("var qc = dv.quang_cao_pct / 100 * rev;", "var qc = dv.quang_cao_pct / 100 * rev + 0.3;")
        with redirect_stdout(io.StringIO()):
            self.assertEqual(kk.main(["--so-ngau-nhien", "40", "--app", str(p)]), 0)

    @can_node
    def test_bat_lech_canh_bao(self):
        p = self._app_hong("Hỏi kế toán (mục 7 p4-tai-chinh.md)", "Hỏi kế toán")
        with redirect_stdout(io.StringIO()):
            self.assertEqual(kk.main(["--so-ngau-nhien", "5", "--app", str(p)]), 1)

    @can_node
    def test_bat_lech_bang_phi(self):
        p = self._app_hong('"loai_phi":"phi_ha_tang","nganh":"Tat ca","muc":{"thap":3000.0,"cao":3000.0',
                           '"loai_phi":"phi_ha_tang","nganh":"Tat ca","muc":{"thap":3000.0,"cao":3002.0')
        with redirect_stdout(io.StringIO()):
            self.assertEqual(kk.main(["--so-ngau-nhien", "30", "--app", str(p)]), 1)

    @can_node
    def test_khac_o_dia_windows(self):
        ps = cam_duong_tuong_doi()
        for p in ps:
            p.start()
        try:
            t = tempfile.mkdtemp()
            self.addCleanup(shutil.rmtree, t, True)
            shutil.copy(APP, Path(t) / "app.html")
            with redirect_stdout(io.StringIO()):
                self.assertEqual(kk.main(["--so-ngau-nhien", "10", "--app", str(Path(t) / "app.html")]), 0)
        finally:
            for p in ps:
                p.stop()

    @can_node
    def test_lam_tron_giong_python(self):
        so = [0.125, 0.375, 2.675, 1.005, 15992.595, 2.5, 3.5, -2.5, -0.125, 0.0, 1e-7, 123456.785, 0.5, 1.5,
              42225.505, 1/3, 2/3, 1234.5678, 99999.995, 0.045, 7.0]
        so += [i / 8 for i in range(-40, 40)] + [i / 1000 for i in range(0, 3000, 7)]
        hop = []
        for n in (0, 2, 4, 6):
            hop += [[x, n] for x in so]
        js = ("const vm=require('vm');const fs=require('fs');const h=fs.readFileSync(process.argv[1],'utf8');"
              "const m=h.match(/<script id=\"loi-tinh\">([\\s\\S]*?)<\\/script>/);const c={};c.globalThis=c;"
              "vm.createContext(c);vm.runInContext(m[1],c);const v=JSON.parse(fs.readFileSync(0,'utf8'));"
              "process.stdout.write(JSON.stringify(v.map(([x,n])=>[c.TaiChinh.pyRound(x,n),c.TaiChinh.fmtG(x)])))")
        r = subprocess.run([NODE, "-e", js, str(APP)], input=json.dumps(hop), capture_output=True, text=True,
                           encoding="utf-8")
        self.assertEqual(r.returncode, 0, r.stderr)
        ra = json.loads(r.stdout)
        for (x, n), (tron, g) in zip(hop, ra):
            self.assertEqual(tron, round(x, n), f"round({x!r}, {n})")
            self.assertEqual(g, f"{x:g}", f"{x!r}:g")


class TestDocViDuP4(unittest.TestCase):
    def _tep(self, obj):
        t = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, t, True)
        p = Path(t) / "vi-du-kiem-khop.json"
        p.write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8")
        return p

    def test_khong_co_tep(self):
        self.assertEqual(kk.vi_du_p4(Path(tempfile.gettempdir()) / "khong-co-tep-nay.json"), [])

    def test_hai_dang(self):
        dv = {"san": "shopee", "nganh": "Sac dep", "gia_ban": 250000, "gia_von": 95000, "ngay_ban": "2026-11-12"}
        a = kk.vi_du_p4(self._tep([dv]))
        b = kk.vi_du_p4(self._tep({"vi_du": [{"ten": "x", "dau_vao": dv, "mong_doi": {"ln": 1}}]}))
        self.assertEqual(a[0]["dau_vao"], b[0]["dau_vao"])
        self.assertIsInstance(a[0]["dau_vao"]["gia_ban"], float)
        self.assertEqual(b[0]["mong_doi"], {"ln": 1})

    def test_dang_la_bao_loi(self):
        with self.assertRaises(ValueError):
            kk.vi_du_p4(self._tep({"khac": 1}))
        with self.assertRaises(ValueError):
            kk.vi_du_p4(self._tep([{"san": "shopee", "gia_ban": 1, "gia_von": 1, "ngay_ban": "2026-11-12", "la": 1}]))
        with self.assertRaises(ValueError):
            kk.vi_du_p4(self._tep([{"san": "shopee", "gia_ban": 1, "gia_von": 1}]))  # thiếu ngày

    def test_so_mong_doi(self):
        py = {"ok": {"ln": 100.0, "roas_hoa_von": 2.5}}
        self.assertEqual(kk.so_mong_doi(py, {"ln": 100.5, "roas_hoa_von": 2.5}), [])
        self.assertEqual(len(kk.so_mong_doi(py, {"ln": 102})), 1)
        self.assertEqual(len(kk.so_mong_doi({"loi": "ThieuDuLieu", "thong_diep": "x"}, {"ln": 1})), 1)

    def test_so_sanh_loi_va_ket_qua(self):
        lech, _ = kk.so_sanh({"loi": "ThieuDuLieu", "thong_diep": "a"}, {"ok": {}})
        self.assertTrue(lech)
        lech, _ = kk.so_sanh({"loi": "ThieuDuLieu", "thong_diep": "a"}, {"loi": "ThieuDuLieu", "thong_diep": "b"})
        self.assertTrue(lech)
        lech, _ = kk.so_sanh({"loi": "ThieuDuLieu", "thong_diep": "a"}, {"loi": "ThieuDuLieu", "thong_diep": "a"})
        self.assertFalse(lech)


class TestChayKiemThu(unittest.TestCase):
    def test_khong_mo_coi(self):
        self.assertEqual(ckt.tim_mo_coi(), [])

    def test_workflow(self):
        wf = (GOC / ".github" / "workflows" / "kiem-thu.yml").read_text(encoding="utf-8")
        self.assertIn("pull_request", wf)
        self.assertNotRegex(wf, r"(?m)^\s*push\s*:")
        self.assertIn("contents: read", wf)
        for dong in re.findall(r"uses:\s*(\S+)", wf):
            ten, _, ban = dong.partition("@")
            self.assertIn(ten, ("actions/checkout", "actions/setup-python", "actions/setup-node"), dong)
            self.assertRegex(ban, r"^[0-9a-f]{40}$", f"{dong}: phải ghim theo mã commit")
        self.assertIn("tools/chay-kiem-thu.py", wf)
        self.assertIn("timeout-minutes", wf)


if __name__ == "__main__":
    unittest.main()
