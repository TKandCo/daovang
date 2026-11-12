"""Cấu hình KHÔNG bí mật đọc từ tệp JSON; khóa bí mật CHỈ đọc từ biến môi trường.

Thứ tự ưu tiên: giá trị mặc định < tệp JSON < biến môi trường DAOVANG_<KHOA_IN_HOA>.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

TIEN_TO = "DAOVANG_"
# Từ khóa trong tên cấu hình gợi ý đó là bí mật -> không được nằm trong tệp JSON.
_GOI_Y_BI_MAT = ("key", "token", "secret", "password", "mat_khau", "khoa")


class ThieuKhoa(RuntimeError):
    pass


def doc_cau_hinh(duong_dan: str | Path | None = None, mac_dinh: dict | None = None,
                 moi_truong: dict | None = None) -> dict:
    cfg = dict(mac_dinh or {})
    if duong_dan and Path(duong_dan).exists():
        tu_tep = json.loads(Path(duong_dan).read_text(encoding="utf-8"))
        nghi = [k for k in tu_tep if any(g in k.lower() for g in _GOI_Y_BI_MAT)]
        if nghi:
            raise ValueError(f"Tệp cấu hình có vẻ chứa bí mật {nghi}. Bí mật phải để ở biến môi trường.")
        cfg.update(tu_tep)
    env = os.environ if moi_truong is None else moi_truong
    for k in list(cfg):
        bien = TIEN_TO + k.upper()
        if bien in env:
            cfg[k] = _ep_kieu(env[bien], cfg[k])
    return cfg


def _ep_kieu(chuoi: str, mau):
    if isinstance(mau, bool):
        return chuoi.strip().lower() in ("1", "true", "yes", "co", "có")
    if isinstance(mau, int):
        return int(chuoi)
    if isinstance(mau, float):
        return float(chuoi)
    return chuoi


def lay_khoa(ten: str, bat_buoc: bool = True, moi_truong: dict | None = None) -> str | None:
    """Đọc khóa bí mật từ biến môi trường. Không bao giờ in giá trị ra."""
    env = os.environ if moi_truong is None else moi_truong
    gia_tri = env.get(ten, "").strip()
    if not gia_tri:
        if bat_buoc:
            raise ThieuKhoa(
                f"Chưa có khóa '{ten}'. Đặt ở biến môi trường hoặc cài đặt môi trường cloud "
                f"(KHÔNG ghi vào repo, KHÔNG dán vào chat).")
        return None
    return gia_tri
