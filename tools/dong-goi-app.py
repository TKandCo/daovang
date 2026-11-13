"""Đóng gói app một tệp: app/src/* + bảng phí → app/daovang.html.

Bảng phí được đọc + tách bằng CHÍNH mã Python của P4 (apps/finance/taichinh/bang_phi.py), rồi nhúng vào tệp HTML
dạng JSON. Nhờ vậy bản JS không phải tự đọc CSV → một nguồn sự thật cho cách hiểu bảng phí.

Chạy (đứng ở gốc repo):
    python3 tools/dong-goi-app.py          # ghi lại app/daovang.html
    python3 tools/dong-goi-app.py --kiem   # chỉ kiểm tệp đang có có khớp nguồn không (dùng trong kiểm thử / Actions)
Chỉ dùng thư viện chuẩn. Không gọi mạng.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parents[1]
APP = GOC / "app"
NGUON = APP / "src"
DICH = APP / "daovang.html"
CSV_MAC_DINH = GOC / "bao-cao" / "dot0" / "bang-phi-v1.csv"

sys.path.insert(0, str(GOC / "apps" / "finance"))
from taichinh.bang_phi import BangPhi  # noqa: E402  (mã P4, chỉ đọc)

CHO_BANG_PHI = "/*__BANG_PHI__*/"
CHO_TAI_CHINH = "/*__TAI_CHINH__*/"
CHO_GIAO_DIEN = "/*__GIAO_DIEN__*/"


def _muc(m):
    if m is None:
        return None
    return {"thap": m.thap, "cao": m.cao, "tran_vnd": m.tran_vnd, "trung_vi": m.trung_vi, "goc": m.goc}


def du_lieu_bang_phi(csv_path: Path = CSV_MAC_DINH) -> dict:
    bp = BangPhi(csv_path)
    dong = []
    for d in bp.dong:
        dong.append({
            "san": d.san, "loai_phi": d.loai_phi, "nganh": d.nganh, "muc": _muc(d.muc), "don_vi": d.don_vi,
            "tu_ngay": d.tu_ngay.isoformat() if d.tu_ngay else None,
            "den_ngay": d.den_ngay.isoformat() if d.den_ngay else None,
            "nguon": d.nguon, "do_tin_cay": d.do_tin_cay, "ghi_chu": d.ghi_chu,
            "canh_bao": list(d.canh_bao), "suy_tu_ghi_chu": d.suy_tu_ghi_chu,
        })
    # băm trên nội dung đã chuẩn hóa xuống dòng (LF): Windows checkout ra CRLF vẫn cho cùng mã
    sha = hashlib.sha256(chuan_xuong_dong(Path(csv_path).read_bytes())).hexdigest()
    # đường dẫn ghi dạng chữ cố định (không tính đường dẫn tương đối → không lỗi khi khác ổ đĩa trên Windows)
    return {"nguon_tep": "bao-cao/dot0/bang-phi-v1.csv", "sha256": sha, "so_dong_csv": sum(1 for d in bp.dong if not d.suy_tu_ghi_chu),
            "dong": dong}


def chuan_xuong_dong(b: bytes) -> bytes:
    return b.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def json_an_toan(obj) -> str:
    """JSON nhúng được trong <script>: chặn '</script>' và ký tự xuống dòng đặc biệt."""
    s = json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
    return s.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026") \
            .replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")


def doc(p: Path) -> str:
    return chuan_xuong_dong(p.read_bytes()).decode("utf-8")


def dung(csv_path: Path = CSV_MAC_DINH, nguon: Path = NGUON) -> str:
    khung = doc(nguon / "khung.html")
    for cho in (CHO_BANG_PHI, CHO_TAI_CHINH, CHO_GIAO_DIEN):
        if khung.count(cho) != 1:
            raise SystemExit(f"khung.html phải có đúng 1 chỗ {cho}")
    js_tc = doc(nguon / "taichinh.js")
    js_gd = doc(nguon / "giao-dien.js")
    for ten, js in (("taichinh.js", js_tc), ("giao-dien.js", js_gd)):
        if "</script" in js.lower():
            raise SystemExit(f"{ten} không được chứa chuỗi </script")
    ra = khung.replace(CHO_BANG_PHI, json_an_toan(du_lieu_bang_phi(csv_path)))
    ra = ra.replace(CHO_TAI_CHINH, js_tc).replace(CHO_GIAO_DIEN, js_gd)
    return ra.replace("\r\n", "\n")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Đóng gói app/daovang.html")
    ap.add_argument("--kiem", action="store_true", help="chỉ kiểm app/daovang.html có khớp nguồn không")
    ap.add_argument("--bang-phi", default=str(CSV_MAC_DINH), help="CSV bảng phí")
    ap.add_argument("--ra", default=str(DICH), help="tệp ghi ra")
    a = ap.parse_args(argv)
    moi = dung(Path(a.bang_phi), NGUON)
    dich = Path(a.ra)
    if a.kiem:
        cu = doc(dich) if dich.exists() else ""
        if cu != moi:
            print("HỎNG: app/daovang.html CŨ so với app/src hoặc bảng phí. Chạy: python3 tools/dong-goi-app.py")
            return 1
        print("ĐẠT: app/daovang.html khớp nguồn + bảng phí")
        return 0
    dich.write_text(moi, encoding="utf-8", newline="\n")
    print(f"Đã ghi {dich.name} ({len(moi.encode('utf-8')) // 1024} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
