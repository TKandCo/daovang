"""Cấu trúc dữ liệu chung của Đào Vàng (bản tối thiểu, Đợt 0).

Chỉ dùng thư viện chuẩn Python. Mỗi bản ghi có trường nguồn + ngày để biết
con số lấy từ đâu, lúc nào (Quy tắc 5 trong CLAUDE.md).

Quy ước:
- Tiền: số nguyên, đơn vị VND (không dùng số thực cho tiền).
- Ngày: chuỗi ISO "YYYY-MM-DD".
- Độ tin cậy: CAO · TB · THAP · CHUA XAC MINH (không dấu, khớp bảng phí v1).
- Khách: KHÔNG lưu họ tên, số điện thoại, địa chỉ chi tiết, email.
"""

from __future__ import annotations

import csv
import re
import unicodedata
from dataclasses import asdict, dataclass, field, fields
from datetime import date
from pathlib import Path
from typing import Optional

PHIEN_BAN = "0.1.0"

DO_TIN_CAY = ("CAO", "TB", "THAP", "CHUA XAC MINH")
SAN = ("Shopee", "TikTok Shop", "Khac")

# Cột của bao-cao/dot0/bang-phi-v1.csv, đúng thứ tự.
COT_BANG_PHI = (
    "san", "loai_phi", "nganh", "muc", "don_vi",
    "hieu_luc_tu", "nguon", "do_tin_cay", "ghi_chu",
)

# Tên trường bị cấm trong bản ghi Khách (dữ liệu cá nhân trực tiếp).
TRUONG_CAM_KHACH = ("ho_ten", "ten", "sdt", "so_dien_thoai", "email",
                    "dia_chi", "cccd", "so_tai_khoan")


def chuan_hoa_do_tin_cay(gia_tri: str) -> str:
    """'THẤP' -> 'THAP', 'chưa xác minh' -> 'CHUA XAC MINH'."""
    g = (gia_tri or "").strip().upper().replace("Đ", "D")
    g = unicodedata.normalize("NFD", g)
    return "".join(c for c in g if not unicodedata.combining(c))


def _la_ngay(s: str) -> bool:
    try:
        date.fromisoformat(s)
        return True
    except (TypeError, ValueError):
        return False


class _BanGhi:
    """Phần chung: kiểm tra + chuyển sang dict."""

    def thanh_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def tu_dict(cls, d: dict):
        ten = {f.name for f in fields(cls)}
        la = set(d) - ten
        if la:
            raise ValueError(f"{cls.__name__}: trường lạ {sorted(la)}")
        return cls(**d)

    def kiem_tra(self) -> list[str]:
        """Trả danh sách lỗi (rỗng = hợp lệ)."""
        loi = []
        if not getattr(self, "nguon", "").strip():
            loi.append("thiếu nguồn")
        ngay = getattr(self, "ngay_nguon", "")
        if not _la_ngay(ngay):
            loi.append(f"ngay_nguon không phải YYYY-MM-DD: {ngay!r}")
        dtc = getattr(self, "do_tin_cay", None)
        if dtc is not None and chuan_hoa_do_tin_cay(dtc) not in DO_TIN_CAY:
            loi.append(f"do_tin_cay không hợp lệ: {dtc!r}")
        return loi + self._kiem_tra_rieng()

    def _kiem_tra_rieng(self) -> list[str]:
        return []


@dataclass
class SKU(_BanGhi):
    ma_sku: str
    ten: str
    gia_ban_vnd: int
    gia_von_vnd: int
    nguon: str                       # ví dụ "nhap tay", link báo giá NCC
    ngay_nguon: str                  # ngày lấy giá
    nganh: str = ""                  # khớp cột 'nganh' của bảng phí
    ma_ncc: str = ""
    can_nang_g: int = 0
    do_tin_cay: str = "CHUA XAC MINH"
    ghi_chu: str = ""

    def _kiem_tra_rieng(self):
        loi = []
        if not self.ma_sku.strip():
            loi.append("thiếu ma_sku")
        if self.gia_ban_vnd < 0 or self.gia_von_vnd < 0:
            loi.append("giá âm")
        return loi


@dataclass
class DongDon:
    ma_sku: str
    so_luong: int
    don_gia_vnd: int
    giam_gia_nguoi_ban_vnd: int = 0


@dataclass
class DonHang(_BanGhi):
    ma_don: str
    san: str
    ngay_dat: str
    trang_thai: str                  # cho_xac_nhan / dang_giao / da_giao / huy / tra_hang
    dong: list[DongDon]
    nguon: str                       # ví dụ "xuat file Shopee Seller Centre"
    ngay_nguon: str
    ma_khach: str = ""               # mã ẩn danh, KHÔNG phải SĐT/tên
    phi_van_chuyen_khach_tra_vnd: int = 0
    ghi_chu: str = ""

    def tong_hang_vnd(self) -> int:
        return sum(d.so_luong * d.don_gia_vnd - d.giam_gia_nguoi_ban_vnd
                   for d in self.dong)

    @classmethod
    def tu_dict(cls, d: dict):
        d = dict(d)
        d["dong"] = [x if isinstance(x, DongDon) else DongDon(**x)
                     for x in d.get("dong", [])]
        return super().tu_dict(d)

    def _kiem_tra_rieng(self):
        loi = []
        if self.san not in SAN:
            loi.append(f"san không hợp lệ: {self.san!r}")
        if not _la_ngay(self.ngay_dat):
            loi.append("ngay_dat không phải YYYY-MM-DD")
        if not self.dong:
            loi.append("đơn không có dòng hàng")
        return loi


@dataclass
class Khach(_BanGhi):
    """Tối thiểu dữ liệu cá nhân: chỉ mã ẩn danh + tỉnh/thành + số liệu gộp."""
    ma_khach: str                    # mã ẩn danh do công cụ sinh (không suy ra được SĐT)
    nguon: str
    ngay_nguon: str
    san: str = ""
    tinh_thanh: str = ""             # chỉ cấp tỉnh, không địa chỉ chi tiết
    so_don: int = 0
    lan_mua_dau: str = ""
    dong_y_nhan_tin: bool = False    # chỉ True khi khách đồng ý rõ ràng

    @classmethod
    def tu_dict(cls, d: dict):
        cam = [k for k in d if k in TRUONG_CAM_KHACH]
        if cam:
            raise ValueError(f"Khach: không được lưu dữ liệu cá nhân {cam}")
        return super().tu_dict(d)


@dataclass
class NhaCungCap(_BanGhi):
    ma_ncc: str
    ten: str                         # tên doanh nghiệp / gian hàng (không phải cá nhân)
    kenh: str                        # ví dụ "1688", "cho si", "affiliate"
    nguon: str
    ngay_nguon: str
    hinh_thuc: str = "chua_ro"       # nhap_truc_tiep / affiliate / dropship / chua_ro
    moq: int = 0
    thoi_gian_giao_ngay: int = 0
    do_tin_cay: str = "CHUA XAC MINH"
    ghi_chu: str = ""


@dataclass
class Video(_BanGhi):
    ma_video: str
    tieu_de: str
    nguon: str                       # công cụ tạo / người quay
    ngay_nguon: str
    ma_sku: str = ""
    san: str = ""
    co_ai: bool = False              # có dùng AI tạo ảnh/video/giọng
    da_gan_nhan_ai: bool = False     # Quy tắc 6
    co_nguoi_that: bool = False
    co_van_ban_dong_y: bool = False
    trang_thai: str = "nhap"         # nhap / cho_duyet / da_dang

    def _kiem_tra_rieng(self):
        loi = []
        if self.co_ai and not self.da_gan_nhan_ai and self.trang_thai != "nhap":
            loi.append("video AI chưa gắn nhãn nhưng không còn là nháp")
        if self.co_nguoi_that and not self.co_van_ban_dong_y:
            loi.append("có người thật nhưng chưa có văn bản đồng ý")
        return loi


_SO = r"\d+(?:\.\d+)?"
_MUC_SO = re.compile(rf"^\s*({_SO})(?:\s*-\s*({_SO}))?\s*(?:\(.*\))?\s*$")


@dataclass
class DongBangPhi(_BanGhi):
    """Một dòng của bảng phí (khớp cột bang-phi-v1.csv). Giữ chuỗi nguyên văn."""
    san: str
    loai_phi: str
    nganh: str
    muc: str
    don_vi: str
    hieu_luc_tu: str                 # có thể rỗng / "A den B" / "A hoac B"
    nguon: str                       # link + "(tra dd/mm/yyyy)"
    do_tin_cay: str
    ghi_chu: str = ""

    @property
    def ngay_nguon(self) -> str:
        """Ngày tra cứu lấy từ '(tra dd/mm/yyyy)' trong cột nguồn; rỗng nếu không có."""
        m = re.search(r"tra (\d{1,2})/(\d{1,2})/(\d{4})", self.nguon)
        if not m:
            return ""
        d, mth, y = (int(x) for x in m.groups())
        return date(y, mth, d).isoformat()

    def khoang_muc(self) -> Optional[tuple[float, float]]:
        """'13.5-16.5' -> (13.5, 16.5); '3000' -> (3000, 3000); chữ -> None."""
        m = _MUC_SO.match(self.muc)
        if not m:
            return None
        a = float(m.group(1))
        b = float(m.group(2)) if m.group(2) else a
        return (a, b)

    def kiem_tra(self) -> list[str]:
        loi = []
        if not self.nguon.strip():
            loi.append("thiếu nguồn")
        if chuan_hoa_do_tin_cay(self.do_tin_cay) not in DO_TIN_CAY:
            loi.append(f"do_tin_cay không hợp lệ: {self.do_tin_cay!r}")
        if not self.san.strip() or not self.loai_phi.strip():
            loi.append("thiếu san / loai_phi")
        return loi


def doc_bang_phi(duong_dan: str | Path) -> list[DongBangPhi]:
    """Đọc bảng phí CSV (chịu được BOM). Báo lỗi nếu cột không khớp."""
    with open(duong_dan, encoding="utf-8-sig", newline="") as f:
        doc = csv.DictReader(f)
        cot = tuple(c.strip() for c in (doc.fieldnames or ()))
        if cot != COT_BANG_PHI:
            raise ValueError(f"Cột bảng phí không khớp.\n  cần: {COT_BANG_PHI}\n  có:  {cot}")
        ket_qua = []
        for so_dong, hang in enumerate(doc, start=2):
            if not any((v or "").strip() for v in hang.values()):
                continue  # bỏ dòng trống
            if None in hang:
                raise ValueError(f"Dòng {so_dong}: thừa cột (dấu phẩy chưa bọc ngoặc kép?)")
            ket_qua.append(DongBangPhi(**{k: (hang[k] or "").strip() for k in COT_BANG_PHI}))
        return ket_qua


__all__ = [
    "PHIEN_BAN", "DO_TIN_CAY", "SAN", "COT_BANG_PHI", "TRUONG_CAM_KHACH",
    "SKU", "DongDon", "DonHang", "Khach", "NhaCungCap", "Video", "DongBangPhi",
    "doc_bang_phi", "chuan_hoa_do_tin_cay",
]
