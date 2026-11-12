"""Kiểm thử tools/quet-khoa.py. Chạy: python3 -m unittest discover -s tools/tests

Mọi khóa ở đây là GIẢ, được ghép chuỗi lúc chạy để chính tệp này không bị bộ quét bắt.
"""
import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

GOC = Path(__file__).resolve().parents[2]
CONG_CU = GOC / "tools" / "quet-khoa.py"
spec = importlib.util.spec_from_file_location("quet_khoa", CONG_CU)
qk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qk)

A = "A1b2C3d4E5f6G7h8"  # đoạn ký tự giả
KHOA_GIA = {
    "Khóa riêng (private key)": "-----BEGIN " + "RSA PRIVATE KEY-----",
    "AWS access key": "AK" + "IA" + "Q3ZJ7X2LMN4PRS6T",
    "GitHub token": "gh" + "p_" + A * 3,
    "Anthropic API key": "sk-" + "ant-api03-" + A * 3,
    "OpenAI API key": "sk-" + "proj-" + A * 3,
    "Google API key": "AI" + "za" + "Sy" + A * 2 + "a",
    "Slack token": "xo" + "xb-" + "1234567890-" + A,
    "Stripe live key": "sk" + "_live_" + A * 2,
    "Telegram bot token": "1234567890" + ":AA" + A * 2 + "z",
    "JWT": "ey" + "JhbGciOiJIUzI1NiJ9." + "ey" + "JzdWIiOiIxMjM0NTY3ODkwIn0." + A,
    "Chuỗi kết nối có mật khẩu": "postgres://" + "admin:" + "S3cretPassw0rd" + "@db.vidu.local/shop",
    "Gán bí mật dạng chữ": 'SHOPEE_API_' + 'KEY = "' + A + 'Zz"',
}

SACH = """# Tài liệu
Đặt khóa ở biến môi trường: export ANTHROPIC_API_KEY="<khoa-cua-ban>"
api_key = os.environ["SHOPEE_API_KEY"]
token: str = ""
password = "xxxxxxxxxxxxxxxx"
Mã đơn 241112ABCD1234, SKU AO-01, giá 150000 VND, phí 13.5%.
https://banhang.shopee.vn/edu/article/27540
def lay_token(ten): return os.getenv(ten)
"""


class TestMau(unittest.TestCase):
    def test_bat_duoc_moi_khoa_gia(self):
        for loai, khoa in KHOA_GIA.items():
            kq = qk.quet_noi_dung("x.py", f"cau_hinh = 1\n{khoa}\n")
            self.assertTrue(kq, f"không bắt được: {loai}")
            self.assertEqual(kq[0][1], 2)
            self.assertNotIn(khoa[6:], kq[0][3], "không được in nguyên khóa")

    def test_khong_bao_nham_tep_sach(self):
        self.assertEqual(qk.quet_noi_dung("README.md", SACH), [])

    def test_bo_qua(self):
        dong = KHOA_GIA["GitHub token"] + "  # " + qk.BO_QUA
        self.assertEqual(qk.quet_noi_dung("x", dong), [])

    def test_ten_tep_cam(self):
        for p in [".env", "app/.env.production", "khoa.pem", "data/don.csv", "a/secrets/x.txt", "kho.sqlite"]:
            self.assertIsNotNone(qk.ten_bi_cam(p), p)
        for p in [".env.example", "packages/core/README.md", "bao-cao/dot0/bang-phi-v1.csv"]:
            self.assertIsNone(qk.ten_bi_cam(p), p)


class TestGit(unittest.TestCase):
    def _repo(self, t):
        env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t",
                   GIT_COMMITTER_EMAIL="t@t")
        run = lambda *a: subprocess.run(a, cwd=t, env=env, capture_output=True, text=True)  # noqa: E731
        run("git", "init", "-q")
        return run

    def test_staged_va_pre_commit(self):
        with tempfile.TemporaryDirectory() as t:
            run = self._repo(t)
            (Path(t) / "tools").mkdir()
            (Path(t) / "tools" / "quet-khoa.py").write_bytes(CONG_CU.read_bytes())
            r = run(sys.executable, "tools/quet-khoa.py", "--cai-dat")
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

            (Path(t) / "sach.md").write_text(SACH, encoding="utf-8")
            run("git", "add", "-A")
            r = run(sys.executable, "tools/quet-khoa.py", "--staged")
            self.assertEqual(r.returncode, 0, r.stdout)
            self.assertEqual(run("git", "commit", "-qm", "sach").returncode, 0)

            (Path(t) / "cau_hinh.py").write_text(KHOA_GIA["GitHub token"] + "\n", encoding="utf-8")
            run("git", "add", "cau_hinh.py")
            r = run(sys.executable, "tools/quet-khoa.py", "--staged")
            self.assertEqual(r.returncode, 1)
            self.assertIn("cau_hinh.py:1", r.stdout)
            c = run("git", "commit", "-qm", "ban")
            self.assertNotEqual(c.returncode, 0, "pre-commit phải chặn commit có khóa")

    def test_khong_ghi_de_hook_khac(self):
        with tempfile.TemporaryDirectory() as t:
            run = self._repo(t)
            hook = Path(t) / ".git" / "hooks" / "pre-commit"
            hook.write_text("#!/bin/sh\necho khac\n")
            (Path(t) / "q.py").write_bytes(CONG_CU.read_bytes())
            r = run(sys.executable, "q.py", "--cai-dat")
            self.assertEqual(r.returncode, 2)
            self.assertIn("khac", hook.read_text())


class TestKhoHienTai(unittest.TestCase):
    def test_kho_daovang_sach(self):
        r = subprocess.run([sys.executable, str(CONG_CU), "--tat-ca"], cwd=GOC, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


if __name__ == "__main__":
    unittest.main()
