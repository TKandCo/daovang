"""Nhật ký che dữ liệu khách: số điện thoại, email, dãy số dài (CCCD / tài khoản), token."""
from __future__ import annotations

import logging
import re

_MAU = [
    # Token / khóa phổ biến (thô; quét kỹ hơn ở tools/quet-khoa.py)
    (re.compile(r"\b(?:sk-[A-Za-z0-9_-]{16,}|gh[pousr]_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{30,}"
                r"|xox[baprs]-[A-Za-z0-9-]{10,}|eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{5,})"),
     "[KHOA]"),
    (re.compile(r"(?i)\b(bearer)\s+[A-Za-z0-9._~+/=-]{12,}"), r"\1 [KHOA]"),
    (re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"), "[EMAIL]"),
    # Số điện thoại VN: 0xxxxxxxxx / +84xxxxxxxxx / 84xxxxxxxxx, cho phép dấu cách, chấm, gạch.
    (re.compile(r"(?<![\w])(?:\+?84|0)[\s.-]?[1-9](?:[\s.-]?\d){8}(?!\d)"), "[SDT]"),
    # Dãy số dài 9–19 chữ số (CCCD 12 số, số tài khoản, thẻ)
    (re.compile(r"(?<!\d)\d{9,19}(?!\d)"), "[SO-DAI]"),
]

# Khóa trong dict `extra` / tham số có tên nhạy cảm -> che toàn bộ giá trị.
TRUONG_NHAY_CAM = {"ho_ten", "ten_khach", "sdt", "so_dien_thoai", "email", "dia_chi",
                   "cccd", "so_tai_khoan", "mat_khau", "token", "api_key", "khoa"}


def che(van_ban: str) -> str:
    s = str(van_ban)
    for mau, thay in _MAU:
        s = mau.sub(thay, s)
    return s


def _che_gia_tri(v):
    if isinstance(v, dict):
        return {k: ("[CHE]" if str(k).lower() in TRUONG_NHAY_CAM else _che_gia_tri(x)) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return type(v)(_che_gia_tri(x) for x in v)
    if isinstance(v, str):
        return che(v)
    return v


class BoLocChe(logging.Filter):
    """Gắn vào handler: che thông điệp + tham số trước khi ghi."""

    def filter(self, record: logging.LogRecord) -> bool:
        if record.args:
            record.msg = record.getMessage()
            record.args = None
        record.msg = che(_che_gia_tri(record.msg) if not isinstance(record.msg, str) else record.msg)
        for k in list(record.__dict__):
            if k.lower() in TRUONG_NHAY_CAM:
                record.__dict__[k] = "[CHE]"
        return True


def tao_nhat_ky(ten: str = "daovang", muc: int = logging.INFO, handler: logging.Handler | None = None) -> logging.Logger:
    log = logging.getLogger(ten)
    log.setLevel(muc)
    h = handler or logging.StreamHandler()
    h.addFilter(BoLocChe())
    h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
    log.addHandler(h)
    log.propagate = False
    return log
