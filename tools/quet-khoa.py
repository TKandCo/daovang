#!/usr/bin/env python3
"""Quét khóa bí mật trước khi commit / push (chỉ thư viện chuẩn).

Cách dùng:
  python3 tools/quet-khoa.py               # quét các tệp đã `git add` (mặc định)
  python3 tools/quet-khoa.py --tat-ca      # quét mọi tệp git đang theo dõi
  python3 tools/quet-khoa.py tep1 thu_muc  # quét tệp / thư mục chỉ định
  python3 tools/quet-khoa.py --cai-dat     # cài làm pre-commit (tự chạy mỗi lần commit)

Trả mã 0 = sạch, 1 = có nghi vấn (commit bị chặn), 2 = lỗi dùng.
Bỏ qua một dòng chắc chắn vô hại: thêm chú thích `quet-khoa: bo-qua` trên dòng đó.
Không in nguyên khóa ra màn hình: chỉ 4 ký tự đầu + "…".
"""
from __future__ import annotations

import argparse
import fnmatch
import os
import re
import subprocess
import sys
from pathlib import Path

MAU_KHOA: list[tuple[str, re.Pattern]] = [
    ("Khóa riêng (private key)", re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP |ENCRYPTED )?PRIVATE KEY")),
    ("AWS access key", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("GitHub token", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{50,})\b")),
    ("Anthropic API key", re.compile(r"\bsk-ant-[A-Za-z0-9_-]{20,}")),
    ("OpenAI API key", re.compile(r"\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{20,}")),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
    ("Slack token", re.compile(r"\bxox[abposr]-[A-Za-z0-9-]{10,}")),
    ("Stripe live key", re.compile(r"\b[sr]k_live_[A-Za-z0-9]{20,}")),
    ("Telegram bot token", re.compile(r"\b\d{8,10}:AA[A-Za-z0-9_-]{33}\b")),
    ("JWT", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}")),
    ("Chuỗi kết nối có mật khẩu", re.compile(r"\b[a-z][a-z0-9+.-]*://[^\s:/@]+:([^\s@/]{6,})@[^\s]+")),
    ("Gán bí mật dạng chữ", re.compile(
        r"(?i)\b[\w.-]*(?:api[_-]?key|secret|token|password|passwd|mat[_-]?khau|access[_-]?key)[\w.-]*"
        r"\s*[:=]\s*['\"]([^'\"\s]{12,})['\"]")),
]

# Tệp không bao giờ được commit dù nội dung là gì (khớp .gitignore).
TEN_TEP_CAM = [".env", ".env.*", "*.key", "*.pem", "*.secret.*", "*.p12", "*.pfx", "id_rsa", "id_ed25519"]
THU_MUC_CAM = ["secrets/", "data/", "du-lieu-that/", "exports/"]
TEP_DU_LIEU_CAM = ["*.sqlite", "*.sqlite3", "*.db"]

# Giá trị mẫu / giả rõ ràng -> không báo (tránh báo nhầm tài liệu).
GIA_TRI_MAU = re.compile(r"(?i)(x{6,}|\*{4,}|<[^>]+>|your[_-]|example|vi[_-]?du|placeholder|changeme|\.\.\.)")
BO_QUA = "quet-khoa: bo-qua"
GIOI_HAN_BYTE = 2_000_000


def _che(s: str) -> str:
    return s[:4] + "…" if len(s) > 4 else "…"


def quet_noi_dung(ten: str, noi_dung: str) -> list[tuple[str, int, str, str]]:
    """Trả [(tệp, dòng, loại, mẫu đã che)]."""
    ket_qua = []
    for so, dong in enumerate(noi_dung.splitlines(), start=1):
        if BO_QUA in dong:
            continue
        for loai, mau in MAU_KHOA:
            for m in mau.finditer(dong):
                gia_tri = m.group(1) if m.groups() else m.group(0)
                if GIA_TRI_MAU.search(gia_tri):
                    continue
                ket_qua.append((ten, so, loai, _che(gia_tri)))
    return ket_qua


def ten_bi_cam(duong_dan: str) -> str | None:
    p = duong_dan.replace("\\", "/")
    ten = p.rsplit("/", 1)[-1]
    if ten in (".env.example", ".env.mau"):
        return None
    for m in TEN_TEP_CAM + TEP_DU_LIEU_CAM:
        if fnmatch.fnmatch(ten, m):
            return f"tên tệp bị cấm ({m})"
    for d in THU_MUC_CAM:
        if p.startswith(d) or f"/{d}" in p:
            return f"nằm trong thư mục bị cấm ({d})"
    return None


def _git(*args: str) -> bytes:
    return subprocess.run(["git", *args], check=True, capture_output=True).stdout


def _la_nhi_phan(b: bytes) -> bool:
    return b"\0" in b[:8000]


def nguon_staged():
    ds = _git("diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z").decode().split("\0")
    for p in filter(None, ds):
        yield p, (lambda p=p: _git("show", f":{p}"))


def nguon_tat_ca():
    for p in filter(None, _git("ls-files", "-z").decode().split("\0")):
        yield p, (lambda p=p: Path(p).read_bytes())


def nguon_duong_dan(ds: list[str]):
    for goc in ds:
        g = Path(goc)
        tep = [g] if g.is_file() else [x for x in g.rglob("*") if x.is_file() and ".git" not in x.parts]
        for t in tep:
            yield str(t), (lambda t=t: t.read_bytes())


def quet(nguon) -> list[tuple[str, int, str, str]]:
    ket_qua = []
    for p, doc in nguon:
        ly_do = ten_bi_cam(p)
        if ly_do:
            ket_qua.append((p, 0, ly_do, ""))
        try:
            b = doc()
        except (OSError, subprocess.CalledProcessError):
            continue
        if len(b) > GIOI_HAN_BYTE or _la_nhi_phan(b):
            continue
        ket_qua.extend(quet_noi_dung(p, b.decode("utf-8", errors="replace")))
    return ket_qua


HOOK = """#!/bin/sh
# Cài bởi tools/quet-khoa.py --cai-dat. Chặn commit nếu thấy khóa bí mật.
python3 "$(git rev-parse --show-toplevel)/tools/quet-khoa.py" --staged || {
  echo "Commit bị chặn: xem các dòng trên. Gỡ khóa khỏi tệp (git restore --staged <tệp>) rồi thử lại."
  exit 1
}
"""


def cai_dat(ghi_de: bool) -> int:
    hooks = Path(_git("rev-parse", "--git-path", "hooks").decode().strip())
    hooks.mkdir(parents=True, exist_ok=True)
    dich = hooks / "pre-commit"
    if dich.exists() and not ghi_de and "quet-khoa.py" not in dich.read_text(errors="replace"):
        print(f"Đã có {dich} (của công cụ khác). Không ghi đè. Thêm --ghi-de nếu chắc chắn.")
        return 2
    dich.write_text(HOOK, encoding="utf-8")
    os.chmod(dich, 0o755)
    print(f"Đã cài pre-commit: {dich}. Từ giờ mỗi lần commit sẽ tự quét khóa.")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Quét khóa bí mật (Đào Vàng / P9)")
    ap.add_argument("duong_dan", nargs="*", help="tệp / thư mục cần quét")
    ap.add_argument("--staged", action="store_true", help="quét tệp đã git add (mặc định)")
    ap.add_argument("--tat-ca", action="store_true", help="quét mọi tệp git đang theo dõi")
    ap.add_argument("--cai-dat", action="store_true", help="cài làm git pre-commit")
    ap.add_argument("--ghi-de", action="store_true", help="ghi đè pre-commit có sẵn")
    a = ap.parse_args(argv)

    try:
        if a.cai_dat:
            return cai_dat(a.ghi_de)
        if a.duong_dan:
            nguon = nguon_duong_dan(a.duong_dan)
        elif a.tat_ca:
            nguon = nguon_tat_ca()
        else:
            nguon = nguon_staged()
        ket_qua = quet(nguon)
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Lỗi: cần chạy trong thư mục git và có lệnh git ({e}).", file=sys.stderr)
        return 2

    if not ket_qua:
        print("quet-khoa: SẠCH — không thấy khóa bí mật.")
        return 0
    print(f"quet-khoa: CÓ {len(ket_qua)} NGHI VẤN:")
    for tep, dong, loai, mau in ket_qua:
        vi_tri = f"{tep}:{dong}" if dong else tep
        print(f"  {vi_tri}  [{loai}] {mau}")
    print("Nếu là khóa thật: gỡ khỏi tệp, đổi (thu hồi) khóa ở nhà cung cấp. Nếu chắc chắn vô hại: "
          f"thêm chú thích '{BO_QUA}' trên dòng đó.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
