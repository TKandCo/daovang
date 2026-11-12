#!/usr/bin/env python3
"""Kiểm bảng Radar v1 (P1). Chỉ dùng thư viện chuẩn Python 3.

Chạy:  python3 apps/radar/kiem_tra.py
Kết quả: in "ĐẠT" (mã thoát 0) hoặc danh sách lỗi + "KHÔNG ĐẠT" (mã thoát 1).

Kiểm gì:
  1. Mỗi CSV trong mau/ và du-lieu/ có ĐÚNG các cột quy định (đúng tên, đúng thứ tự).
  2. Không ô nguồn trống: mọi dòng có source_id + captured_at (bảng source: url + captured_at).
  3. Mọi source_id được nhắc tới đều có trong du-lieu/source.csv; ngày dạng YYYY-MM-DD.
  4. Độ tin cậy thuộc {CAO, TB, THAP, CHUA_XAC_MINH}.
  5. Điểm từng tiêu chí là số trong [0, tối đa] hoặc "CHƯA ĐO"; tổng khớp.
  6. fee_ref trỏ tới dòng có thật trong bao-cao/dot0/bang-phi-v1.csv.
  7. Lô thử: tổng chi <= 300 USD/SKU và phải có chủ dự án duyệt.
  8. (audit KTS vòng 2) ngày phải là ngày thật; source_id có ít nhất 1 mã; fee_ref không trống
     ở score / nhom-ung-vien; mo_hinh / model thuộc danh sách; type / export_method của source
     thuộc danh sách; điểm cấp nhóm: demand <= 10, legal thuộc {6, 10}; nhóm có điểm nhu cầu > 0
     phải có ít nhất 1 nguồn ngoài nội bộ; do_tin_cay nhóm không cao hơn nguồn dữ liệu yếu nhất.
"""
import csv
import datetime
import os
import re
import sys

GOC = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(GOC, "..", ".."))
BANG_PHI = os.path.join(REPO, "bao-cao", "dot0", "bang-phi-v1.csv")

CHUA_DO = "CHƯA ĐO"
DO_TIN_CAY = {"CAO", "TB", "THAP", "CHUA_XAC_MINH"}
NGAY = re.compile(r"^\d{4}-\d{2}-\d{2}$")
THU_TU_TIN_CAY = ["CHUA_XAC_MINH", "THAP", "TB", "CAO"]
MO_HINH = {"nhap", "affiliate", "dropship", "ca_hai"}
LOAI_NGUON = {"paid_tool", "google_trends", "platform_public", "affiliate", "manual",
              "bao_chi_dan_metric", "metric_cong_khai", "metric_ereport", "san_tu_cong_bo",
              "blog_ban_hang", "noi_bo"}
CACH_LAY = {"chep_tay", "xuat_file", "api", "xem_tay", "doc_tep", "nhap_tay"}
# Điểm cấp NHÓM (README mục "Điểm sơ bộ cấp NHÓM")
NHOM_DEMAND_TOI_DA = 10
NHOM_LEGAL = {6, 10}


def ngay_that(v):
    """Ngày có thật và không ở tương lai (ngày ghi số không thể sau hôm nay)."""
    if not NGAY.match(v):
        return False
    try:
        return datetime.datetime.strptime(v, "%Y-%m-%d").date() <= datetime.date.today()
    except ValueError:
        return False


def tach_ma(v):
    return [x.strip() for x in v.split(";") if x.strip()]

# Thang điểm 100 (mục 5 báo cáo p1-radar.md)
DIEM_TOI_DA = {
    "demand": 20, "competition": 15, "margin": 25, "legal": 15,
    "returns": 10, "season": 5, "video": 10,
}

# Cột từng bảng (kiến trúc mục 6 báo cáo p1-radar.md + cột nguồn/ngày)
COT = {
    "source": ["source_id", "name", "type", "url", "published_at", "license_note",
               "export_method", "reliability", "cost_per_month_usd", "captured_at"],
    "product": ["product_id", "name", "category", "keywords", "sku_group", "brand",
                "regulated_flag", "ip_risk_flag", "season_tag", "model",
                "source_id", "captured_at"],
    "supplier": ["supplier_id", "name", "type", "public_contact_note", "docs_available",
                 "moq", "lead_time_days", "rating_note", "source_id", "captured_at"],
    "supplier_quote": ["quote_id", "product_id", "supplier_id", "unit_cost_vnd", "moq",
                       "ship_cost_per_unit_vnd", "currency", "fx_rate", "quoted_at",
                       "valid_until", "source_id", "captured_at"],
    "listing_price": ["listing_id", "product_id", "platform", "shop_ref", "price_vnd",
                      "sold_est_30d", "rating", "source_id", "captured_at"],
    "trend_signal": ["signal_id", "product_id", "metric", "value", "unit", "region",
                     "period_start", "period_end", "source_id", "captured_at"],
    "score": ["score_id", "product_id", "scored_at", "demand", "competition", "margin",
              "legal", "returns", "season", "video", "total", "fee_ref", "margin_note",
              "decision", "source_id", "captured_at"],
    "trial_batch": ["batch_id", "product_id", "supplier_id", "qty", "cost_total_usd",
                    "start_date", "end_date", "orders", "returns", "net_margin_real_pct",
                    "decision", "owner_approved", "source_id", "captured_at"],
    "affiliate_item": ["item_id", "product_id", "platform", "commission_rate_pct",
                       "valid_from", "valid_to", "source_id", "captured_at"],
    "nhom-ung-vien": ["nhom_id", "ten_nhom", "vi_du_mat_hang", "mo_hinh",
                      "tin_hieu_nhu_cau", "source_id", "captured_at", "do_tin_cay",
                      "phap_ly_ghi_chu", "fee_ref", "demand", "competition", "margin",
                      "legal", "returns", "season", "video", "diem_so_bo",
                      "diem_toi_da_da_cham", "ghi_chu"],
}

# Bảng mẫu (chỉ tiêu đề) và bảng dữ liệu thật của P1
THU_MUC = {"mau": ["source", "product", "supplier", "supplier_quote", "listing_price",
                   "trend_signal", "score", "trial_batch", "affiliate_item"],
           "du-lieu": ["source", "nhom-ung-vien"]}


def doc_csv(duong_dan):
    with open(duong_dan, encoding="utf-8-sig", newline="") as f:
        r = list(csv.reader(f))
    return (r[0] if r else []), r[1:]


def doc_bang_phi(duong_dan=BANG_PHI):
    with open(duong_dan, encoding="utf-8-sig", newline="") as f:
        return {f"{d['san']}|{d['loai_phi']}|{d['nganh']}" for d in csv.DictReader(f)}


def kiem_diem(dong, ten, loi, vi_tri):
    """Kiểm 7 tiêu chí; trả (tổng đã chấm, tối đa đã chấm)."""
    tong = toi_da = 0
    for cot, mx in DIEM_TOI_DA.items():
        v = dong[cot].strip()
        if v == CHUA_DO:
            continue
        try:
            x = float(v.replace(",", "."))
        except ValueError:
            loi.append(f"{vi_tri}: cột {cot}='{v}' không phải số hay '{CHUA_DO}'")
            continue
        if not 0 <= x <= mx:
            loi.append(f"{vi_tri}: cột {cot}={v} ngoài [0,{mx}]")
        tong += x
        toi_da += mx
    return tong, toi_da


def kiem_nhom(d, nguon, loi, vt):
    """Quy tắc riêng cấp nhóm (README)."""
    try:
        if float(d["demand"]) > NHOM_DEMAND_TOI_DA:
            loi.append(f"{vt}: demand cấp nhóm {d['demand']} > {NHOM_DEMAND_TOI_DA}")
    except ValueError:
        pass
    try:
        if int(float(d["legal"])) not in NHOM_LEGAL:
            loi.append(f"{vt}: legal cấp nhóm {d['legal']} phải thuộc {sorted(NHOM_LEGAL)}")
    except ValueError:
        pass
    du_lieu = [nguon[s] for s in tach_ma(d["source_id"])
               if s in nguon and nguon[s]["type"] != "noi_bo"]
    try:
        if float(d["demand"]) > 0 and not du_lieu:
            loi.append(f"{vt}: có điểm nhu cầu nhưng chỉ có nguồn nội bộ")
    except ValueError:
        pass
    if du_lieu and d["do_tin_cay"] in THU_TU_TIN_CAY:
        yeu_nhat = min((n["reliability"] for n in du_lieu if n["reliability"] in THU_TU_TIN_CAY),
                       key=THU_TU_TIN_CAY.index, default=None)
        if yeu_nhat and THU_TU_TIN_CAY.index(d["do_tin_cay"]) > THU_TU_TIN_CAY.index(yeu_nhat):
            loi.append(f"{vt}: do_tin_cay {d['do_tin_cay']} cao hơn nguồn yếu nhất ({yeu_nhat})")


def kiem_bang(ten, duong_dan, nguon, bang_phi, loi):
    tieu_de, dong_s = doc_csv(duong_dan)
    if tieu_de and tieu_de == COT[ten]:
        k = tieu_de.index(COT[ten][0])  # cột mã (cột đầu) không được trùng
        thay = set()
        for i, h in enumerate(dong_s, start=2):
            if h and h[k].strip():
                if h[k] in thay:
                    loi.append(f"{os.path.relpath(duong_dan, REPO)} dòng {i}: trùng mã {h[k]}")
                thay.add(h[k])
    if tieu_de != COT[ten]:
        loi.append(f"{duong_dan}: sai cột.\n   cần: {COT[ten]}\n   có : {tieu_de}")
        return
    for i, hang in enumerate(dong_s, start=2):
        vt = f"{os.path.relpath(duong_dan, REPO)} dòng {i}"
        if not any(c.strip() for c in hang):
            continue
        if len(hang) != len(tieu_de):
            loi.append(f"{vt}: có {len(hang)} ô, cần {len(tieu_de)}")
            continue
        d = dict(zip(tieu_de, hang))
        # ô nguồn / ngày
        bat_buoc = ["url", "captured_at"] if ten == "source" else ["source_id", "captured_at"]
        for c in bat_buoc:
            if not d[c].strip():
                loi.append(f"{vt}: ô nguồn '{c}' trống")
        if d["captured_at"].strip() and not ngay_that(d["captured_at"].strip()):
            loi.append(f"{vt}: captured_at '{d['captured_at']}' không phải ngày thật YYYY-MM-DD (hoặc ở tương lai)")
        if ten == "source":
            if d["reliability"] not in DO_TIN_CAY:
                loi.append(f"{vt}: reliability '{d['reliability']}' không hợp lệ")
            if d["type"] not in LOAI_NGUON:
                loi.append(f"{vt}: type '{d['type']}' ngoài danh sách {sorted(LOAI_NGUON)}")
            if d["export_method"] not in CACH_LAY:
                loi.append(f"{vt}: export_method '{d['export_method']}' ngoài danh sách")
            url = d["url"].strip()
            if re.match(r"^https?://[^/\s]+\.[^/\s]+", url):
                pass
            elif url and os.path.exists(os.path.join(REPO, url)):
                pass  # tệp trong repo (đường dẫn tương đối từ gốc repo)
            else:
                loi.append(f"{vt}: url '{url}' không phải link, cũng không phải tệp có trong repo")
        else:
            ma = tach_ma(d["source_id"])
            if d["source_id"].strip() and not ma:
                loi.append(f"{vt}: source_id chỉ có dấu ';', không có mã nào")
            for sid in ma:
                if sid not in nguon:
                    loi.append(f"{vt}: source_id '{sid}' không có trong du-lieu/source.csv")
        for c in ("mo_hinh", "model"):
            if c in d and d[c].strip() and d[c].strip() not in MO_HINH:
                loi.append(f"{vt}: {c} '{d[c]}' ngoài danh sách {sorted(MO_HINH)}")
        if ten in ("score", "nhom-ung-vien") and not d["fee_ref"].strip():
            loi.append(f"{vt}: fee_ref trống — phí phải trỏ về bang-phi-v1.csv")
        if "do_tin_cay" in d and d["do_tin_cay"] not in DO_TIN_CAY:
            loi.append(f"{vt}: do_tin_cay '{d['do_tin_cay']}' không hợp lệ")
        if "fee_ref" in d:
            for ref in [x.strip() for x in d["fee_ref"].split(";") if x.strip()]:
                if ref not in bang_phi:
                    loi.append(f"{vt}: fee_ref '{ref}' không có trong bang-phi-v1.csv")
        if ten in ("score", "nhom-ung-vien"):
            tong, toi_da = kiem_diem(d, ten, loi, vt)
            cot_tong = "total" if ten == "score" else "diem_so_bo"
            try:
                if abs(float(d[cot_tong]) - tong) > 0.01:
                    loi.append(f"{vt}: {cot_tong}={d[cot_tong]} khác tổng tính được {tong:g}")
            except ValueError:
                loi.append(f"{vt}: {cot_tong} '{d[cot_tong]}' không phải số")
            if ten == "nhom-ung-vien":
                kiem_nhom(d, nguon, loi, vt)
                try:
                    if int(d["diem_toi_da_da_cham"]) != toi_da:
                        loi.append(f"{vt}: diem_toi_da_da_cham={d['diem_toi_da_da_cham']} "
                                   f"khác {toi_da}")
                except ValueError:
                    loi.append(f"{vt}: diem_toi_da_da_cham không phải số")
        if ten == "trial_batch":
            try:
                if float(d["cost_total_usd"]) > 300:
                    loi.append(f"{vt}: lô thử {d['cost_total_usd']} USD > 300 USD/SKU")
            except ValueError:
                loi.append(f"{vt}: cost_total_usd không phải số")
            if d["owner_approved"].strip().upper() != "CO":
                loi.append(f"{vt}: lô thử chưa có chủ dự án duyệt (owner_approved phải 'CO')")


def kiem_tat_ca(goc=GOC, bang_phi_path=BANG_PHI):
    loi = []
    bang_phi = doc_bang_phi(bang_phi_path)
    p_nguon = os.path.join(goc, "du-lieu", "source.csv")
    nguon = {}
    if os.path.exists(p_nguon):
        tieu_de, ds = doc_csv(p_nguon)
        for h in ds:
            if len(h) == len(tieu_de):
                d = dict(zip(tieu_de, h))
                sid = d.get("source_id", "").strip()
                if sid:
                    if sid in nguon:
                        loi.append(f"du-lieu/source.csv: trùng source_id {sid}")
                    nguon[sid] = d
    so_tep = 0
    for thu_muc, ten_s in THU_MUC.items():
        for ten in ten_s:
            p = os.path.join(goc, thu_muc, ten + ".csv")
            if not os.path.exists(p):
                loi.append(f"thiếu tệp {thu_muc}/{ten}.csv")
                continue
            kiem_bang(ten, p, nguon, bang_phi, loi)
            so_tep += 1
    return so_tep, loi


def main():
    so_tep, loi = kiem_tat_ca()
    if loi:
        for x in loi:
            print("LỖI:", x)
        print(f"KHÔNG ĐẠT — {len(loi)} lỗi / {so_tep} tệp")
        return 1
    print(f"ĐẠT — {so_tep} tệp CSV đúng cột, không ô nguồn trống")
    return 0


if __name__ == "__main__":
    sys.exit(main())
