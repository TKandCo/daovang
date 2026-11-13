"""Chạy TOÀN BỘ kiểm thử của repo bằng một lệnh — trên máy (Windows / macOS / Linux) và trên GitHub Actions.

    python3 tools/chay-kiem-thu.py            (Windows: py tools\\chay-kiem-thu.py)
    python3 tools/chay-kiem-thu.py --nhanh    (bỏ kiểm khớp JS ↔ Python, dùng khi chưa cài node)

Gồm: mọi bộ unittest đã biết, kiểm ngược P4, kiểm dữ liệu P1, app HTML khớp nguồn, kiểm khớp JS ↔ Python,
quét khóa toàn repo. Tệp test_*.py nằm ngoài các bộ đã biết → HỎNG ("mồ côi"), để không bộ nào bị bỏ sót.
Mã thoát 0 = tất cả ĐẠT. Chỉ thư viện chuẩn; không gọi mạng; không tính đường dẫn tương đối giữa các ổ đĩa.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

GOC = Path(__file__).resolve().parents[1]
PY = sys.executable

# (tên, lệnh, thư mục chạy, thư mục chứa kiểm thử mà bộ này phủ)
BO_UNITTEST = [
    ("unittest P4 tài chính", ["-m", "unittest", "discover", "-s", "apps/finance", "-t", "apps/finance"], ".", "apps/finance"),
    ("unittest P1 radar", ["-m", "unittest", "discover", "-s", "apps/radar", "-p", "test_*.py"], ".", "apps/radar"),
    ("unittest schema", ["-m", "unittest", "discover", "-s", "packages/schema/tests"], ".", "packages/schema"),
    ("unittest core", ["-m", "unittest", "discover", "-s", "packages/core/tests"], ".", "packages/core"),
    ("unittest tools + app", ["-m", "unittest", "discover", "-s", "tools/tests"], ".", "tools"),
]
KIEM_KHAC = [
    ("kiểm ngược P4 (3 ví dụ báo cáo)", ["-m", "taichinh.kiem_nguoc"], "apps/finance"),
    ("kiểm dữ liệu P1", ["apps/radar/kiem_tra.py"], "."),
    ("app/daovang.html khớp nguồn", ["tools/dong-goi-app.py", "--kiem"], "."),
    ("kiểm khớp JS ↔ Python", ["tools/kiem-khop.py"], "."),
    ("quét khóa toàn repo", ["tools/quet-khoa.py", "--tat-ca"], "."),
]
BO_QUA_THU_MUC = {".git", "node_modules", "__pycache__", ".venv"}


def tim_mo_coi() -> list[str]:
    phu = [(GOC / b[3]).resolve() for b in BO_UNITTEST]
    mo_coi = []
    for p in GOC.rglob("test_*.py"):
        if BO_QUA_THU_MUC & set(p.parts):
            continue
        rp = p.resolve()
        if not any(d == rp.parent or d in rp.parents for d in phu):
            mo_coi.append(p.as_posix().replace(GOC.as_posix() + "/", ""))
    return sorted(mo_coi)


def chay(ten: str, lenh: list[str], cwd: str) -> tuple[bool, float, str]:
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1")
    t0 = time.time()
    p = subprocess.run([PY, *lenh], cwd=str(GOC / cwd), env=env, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return p.returncode == 0, time.time() - t0, (p.stdout + p.stderr)


def main(argv=None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="Chạy toàn bộ kiểm thử Đào Vàng")
    ap.add_argument("--nhanh", action="store_true", help="bỏ kiểm khớp JS ↔ Python (không cần node)")
    ap.add_argument("--im", action="store_true", help="chỉ in chi tiết của bước HỎNG")
    a = ap.parse_args(argv)

    viec = [(t, l, c) for t, l, c, _ in BO_UNITTEST] + list(KIEM_KHAC)
    if a.nhanh:
        viec = [v for v in viec if not v[0].startswith("kiểm khớp")]
    hong = []
    mo_coi = tim_mo_coi()
    if mo_coi:
        hong.append("kiểm thử mồ côi")
        print("HỎNG  kiểm thử mồ côi (thêm vào BO_UNITTEST trong tools/chay-kiem-thu.py):")
        for m in mo_coi:
            print("      -", m)
    for ten, lenh, cwd in viec:
        ok, giay, ra = chay(ten, lenh, cwd)
        dong_cuoi = [x for x in ra.strip().splitlines() if x.strip()][-1:] or [""]
        print(f"{'ĐẠT ' if ok else 'HỎNG'}  {ten:34} {giay:5.1f}s  {dong_cuoi[0][:90]}")
        if not ok:
            hong.append(ten)
            print("      " + "\n      ".join(ra.strip().splitlines()[-40:]))
        elif not a.im and os.environ.get("GITHUB_ACTIONS"):
            print("::group::" + ten + "\n" + ra.strip() + "\n::endgroup::")
    if a.nhanh:
        print("CHÚ Ý: đã bỏ kiểm khớp JS ↔ Python (--nhanh) → CHƯA đủ điều kiện báo sẵn sàng")
    print("\nKẾT LUẬN:", "TẤT CẢ ĐẠT" if not hong else "HỎNG: " + ", ".join(hong))
    return 0 if not hong else 1


if __name__ == "__main__":
    raise SystemExit(main())
