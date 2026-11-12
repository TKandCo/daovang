"""Đọc bảng phí sàn (CSV) và chọn mức phí theo sàn / loại phí / ngành / ngày bán.

Chỉ dùng thư viện chuẩn. Cột CSV:
san,loai_phi,nganh,muc,don_vi,hieu_luc_tu,nguon,do_tin_cay,ghi_chu
"""
from __future__ import annotations

import csv
import re
import unicodedata
from functools import lru_cache
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path
from typing import Optional

# apps/finance/taichinh/bang_phi.py -> parents[3] = gốc repo
GOC_REPO = Path(__file__).resolve().parents[3]
BANG_PHI_MAC_DINH = GOC_REPO / "bao-cao" / "dot0" / "bang-phi-v1.csv"

CHE_DO = ("thap", "giua", "cao")


class ThieuDuLieu(Exception):
    """Bảng phí không có dòng phù hợp / mức chưa xác minh / đầu vào thiếu."""


@lru_cache(maxsize=4096)
def bo_dau(s: str) -> str:
    s = s.replace("đ", "d").replace("Đ", "D")
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return " ".join(s.lower().split())


_SO = r"\d+(?:\.\d+)?"


@dataclass
class Muc:
    """Mức phí đã tách: thap..cao (bằng nhau nếu là một số), trần VND nếu có."""
    thap: float
    cao: float
    tran_vnd: Optional[float] = None
    trung_vi: Optional[float] = None
    goc: str = ""

    @property
    def la_khoang(self) -> bool:
        return self.thap != self.cao

    def chon(self, che_do: str) -> float:
        if che_do not in CHE_DO:
            raise ValueError(f"che_do phải là một trong {CHE_DO}, nhận '{che_do}'")
        if che_do == "thap":
            return self.thap
        if che_do == "cao":
            return self.cao
        return (self.thap + self.cao) / 2


def tach_muc(chuoi: str) -> Optional[Muc]:
    """'13.5-16.5' -> Muc(13.5,16.5); '5.5 (toi da 50000/san pham)' -> trần 50000;
    '14.0-15.0 (trung vi 15.0)'; 'toi da 40000 (...)' -> 40000; 'CHUA XAC MINH' -> None."""
    s = (chuoi or "").strip()
    if not s or "CHUA XAC MINH" in s.upper():
        return None
    s_kd = bo_dau(s)
    m = re.match(rf"^(?:toi da\s+)?({_SO})\s*(?:-\s*({_SO}))?", s_kd)
    if not m:
        return None  # dạng chữ (vd. "nguoi ban tu dat") -> không dùng như số
    thap = float(m.group(1))
    cao = float(m.group(2)) if m.group(2) else thap
    tran = None
    mt = re.search(rf"toi da\s+({_SO})\s*/", s_kd)
    if mt:
        tran = float(mt.group(1))
    tv = None
    mv = re.search(rf"trung vi\s+({_SO})\s*\)", s_kd)
    if mv:
        tv = float(mv.group(1))
    return Muc(thap=thap, cao=cao, tran_vnd=tran, trung_vi=tv, goc=s)


def tach_ngay(chuoi: str) -> tuple[Optional[date], Optional[date], list[str]]:
    """Trả (từ ngày, đến ngày, cảnh báo). Rỗng -> (None, None, [cảnh báo])."""
    canh_bao: list[str] = []
    s = (chuoi or "").strip()
    if not s:
        return None, None, ["ngày bắt đầu hiệu lực CHƯA XÁC MINH (ô trống trong bảng phí)"]
    ngays = re.findall(r"(\d{4})-(\d{2})-(\d{2})", s)
    if not ngays:
        return None, None, [f"không đọc được ngày hiệu lực '{s}'"]
    ds = [date(int(y), int(m), int(d)) for y, m, d in ngays]
    s_kd = bo_dau(s)
    if " hoac " in s_kd:
        canh_bao.append(f"ngày hiệu lực mâu thuẫn giữa nguồn ('{s}'); lấy ngày muộn hơn")
        return max(ds), None, canh_bao
    if " den " in s_kd and len(ds) >= 2:
        return ds[0], ds[1], canh_bao
    if "(" in s:
        canh_bao.append(f"ngày '{s}' là ngày cập nhật trang, chưa chắc là ngày hiệu lực thật")
    return ds[0], None, canh_bao


@dataclass
class DongPhi:
    san: str
    loai_phi: str
    nganh: str
    muc: Optional[Muc]
    don_vi: str
    tu_ngay: Optional[date]
    den_ngay: Optional[date]
    nguon: str
    do_tin_cay: str
    ghi_chu: str
    canh_bao: list[str] = field(default_factory=list)
    suy_tu_ghi_chu: bool = False  # True: mức "trước ngày X" lấy từ cột ghi_chu

    def ap_dung(self, ngay: date) -> bool:
        if self.tu_ngay and ngay < self.tu_ngay:
            return False
        if self.den_ngay and ngay > self.den_ngay:
            return False
        return True


def _dong_truoc_tu_ghi_chu(d: DongPhi) -> Optional[DongPhi]:
    """Ghi chú 'Truoc 23/05/2026: 12.5-13.5' hoặc '(truoc do 5%)' -> dòng mức cũ."""
    if not d.tu_ngay:
        return None
    g = d.ghi_chu
    m = re.search(rf"Truoc (\d{{2}})/(\d{{2}})/(\d{{4}}):\s*({_SO}(?:-{_SO})?)", g)
    tin_cay = d.do_tin_cay
    if not m:
        m2 = re.search(rf"[Tt]ruoc do\s+({_SO})%\s*(\(([^)]*)\))?", g)
        if not m2:
            return None
        muc_cu = m2.group(1)
        if m2.group(3) and "blog" in m2.group(3).lower():
            tin_cay = "TB"
    else:
        muc_cu = m.group(4)
    muc = tach_muc(muc_cu)
    if muc is None:
        return None
    return DongPhi(
        san=d.san, loai_phi=d.loai_phi, nganh=d.nganh, muc=muc, don_vi=d.don_vi,
        tu_ngay=None, den_ngay=d.tu_ngay - timedelta(days=1), nguon=d.nguon,
        do_tin_cay=tin_cay, ghi_chu=f"Mức cũ suy từ ghi chú: {g}",
        canh_bao=["mức cũ lấy từ cột ghi_chu; không rõ ngày bắt đầu của mức cũ"],
        suy_tu_ghi_chu=True,
    )


class BangPhi:
    def __init__(self, duong_dan: Path | str = BANG_PHI_MAC_DINH):
        self.duong_dan = Path(duong_dan)
        if not self.duong_dan.exists():
            raise ThieuDuLieu(f"không thấy bảng phí: {self.duong_dan}")
        self.dong: list[DongPhi] = []
        with open(self.duong_dan, encoding="utf-8-sig", newline="") as f:
            for r in csv.DictReader(f):
                tu, den, cb = tach_ngay(r.get("hieu_luc_tu", ""))
                d = DongPhi(
                    san=r["san"].strip(), loai_phi=r["loai_phi"].strip(), nganh=r["nganh"].strip(),
                    muc=tach_muc(r["muc"]), don_vi=r.get("don_vi", "").strip(),
                    tu_ngay=tu, den_ngay=den, nguon=r.get("nguon", "").strip(),
                    do_tin_cay=r.get("do_tin_cay", "").strip(), ghi_chu=r.get("ghi_chu", "").strip(),
                    canh_bao=cb,
                )
                self.dong.append(d)
                cu = _dong_truoc_tu_ghi_chu(d)
                if cu:
                    self.dong.append(cu)

    # ---- tra cứu ----
    def nganh_cua(self, san: str, loai_phi: str) -> list[str]:
        ra: list[str] = []
        for d in self.dong:
            if bo_dau(d.san) == bo_dau(san) and d.loai_phi == loai_phi and d.nganh not in ra:
                ra.append(d.nganh)
        return ra

    def khop_nganh(self, san: str, loai_phi: str, nganh: str) -> str:
        """Khớp chính xác (không dấu, không phân biệt hoa thường) hoặc chuỗi con duy nhất."""
        ds = self.nganh_cua(san, loai_phi)
        if not ds:
            raise ThieuDuLieu(f"bảng phí không có '{loai_phi}' cho sàn '{san}'")
        q = bo_dau(nganh)
        for n in ds:
            if bo_dau(n) == q:
                return n
        con = [n for n in ds if q in bo_dau(n)]
        if len(con) == 1:
            return con[0]
        if not con:
            raise ThieuDuLieu(f"không có ngành '{nganh}' cho {san}/{loai_phi}. Ngành có: " + " | ".join(ds))
        raise ThieuDuLieu(f"ngành '{nganh}' khớp nhiều dòng: " + " | ".join(con) + " — gõ cụ thể hơn")

    def tra(self, san: str, loai_phi: str, nganh: str, ngay: date) -> DongPhi:
        """Chọn dòng hiệu lực tại `ngay` (dòng có ngày bắt đầu muộn nhất mà <= ngay)."""
        n = self.khop_nganh(san, loai_phi, nganh)
        ung_vien = [d for d in self.dong
                    if bo_dau(d.san) == bo_dau(san) and d.loai_phi == loai_phi and d.nganh == n
                    and d.ap_dung(ngay)]
        if not ung_vien:
            raise ThieuDuLieu(f"không có mức '{loai_phi}' ({san}, {n}) hiệu lực ngày {ngay.isoformat()}")
        ung_vien.sort(key=lambda d: (d.tu_ngay or date.min, not d.suy_tu_ghi_chu))
        d = ung_vien[-1]
        if d.muc is None:
            raise ThieuDuLieu(f"mức '{loai_phi}' ({san}, {n}) CHƯA XÁC MINH trong bảng phí")
        return d

    def dong_dau(self, san: str, loai_phi: str) -> Optional[DongPhi]:
        for d in self.dong:
            if bo_dau(d.san) == bo_dau(san) and d.loai_phi == loai_phi and not d.suy_tu_ghi_chu:
                return d
        return None
