/* Lõi máy tính lợi nhuận mỗi đơn — bản JS chép 1:1 từ apps/finance/taichinh/tinh_loi_nhuan.py (P4).
 * KHÔNG sửa công thức ở đây trước khi P4 sửa bản Python: tools/kiem-khop.py so hai bản, lệch > 1 đ = HỎNG.
 * Bảng phí được Python (taichinh.bang_phi) đọc + tách sẵn, đóng gói vào app bởi tools/dong-goi-app.py.
 * Không gọi mạng, không đọc / ghi gì ngoài tham số truyền vào.
 */
(function (goc) {
  "use strict";

  var DONG_KHONG_DAM_BAO = "Số đầu vào (giá vốn, giá bán, tỷ lệ hoàn, quảng cáo…) là GIẢ ĐỊNH do người dùng nhập. " +
    "Không phải khuyến nghị đầu tư / không đảm bảo lợi nhuận.";

  var CANH_BAO_HA_TANG = "Phí hạ tầng Shopee 3.000đ/đơn: nguồn chính thức (Shopee Uni bài 25329) + Sapo + Báo Pháp Luật ghi " +
    "áp dụng; MỘT nguồn (ai-hay) nói CHỈ áp dụng Shopee Mall → mâu thuẫn, chưa kiểm trên Kênh Người Bán. " +
    "Công cụ vẫn tính 3.000đ (thận trọng).";

  var CHE_DO = ["thap", "giua", "cao"];

  var SAN = {
    shopee: {
      ten: "Shopee",
      phi_nganh: "phi_co_dinh",
      phi_gd: ["phi_xu_ly_giao_dich", "Tat ca (nguoi ban thuong)"],
      phi_don: ["phi_ha_tang", "Tat ca"],
      voucher_san: ["phi_dich_vu_goi_voucher_xtra", "Tat ca (neu tham gia)"],
      ship_tra: ["phi_van_chuyen_tra_hang_nguoi_ban_chiu", "Tat ca"],
      phi_don_mat_khi_hoan: false
    },
    tiktok: {
      ten: "TikTok Shop",
      phi_nganh: "phi_hoa_hong_nen_tang",
      nganh_mac_dinh: "Muc mac dinh (nganh cap 3 khong liet ke)",
      phi_gd: ["phi_giao_dich", "Tat ca"],
      phi_don: ["phi_xu_ly_don_hang", "Tat ca"],
      voucher_san: ["phi_dich_vu_Voucher_Extra_VXP", "Tat ca (neu tham gia)"],
      ship_tra: null,
      phi_don_mat_khi_hoan: true
    }
  };

  function ThieuDuLieu(msg) {
    var e = new Error(msg);
    e.name = "ThieuDuLieu";
    e.thieuDuLieu = true;
    return e;
  }

  function laNone(v) { return v === null || v === undefined; }

  // ---- giống Python ----
  function boDau(s) {
    s = String(s).replace(/đ/g, "d").replace(/Đ/g, "D");
    s = s.normalize("NFD").replace(/\p{Mn}/gu, "");
    return s.toLowerCase().split(/\s+/).filter(function (x) { return x; }).join(" ");
  }

  // round(x, n) của Python: làm tròn đúng giá trị nhị phân, hòa thì về số chẵn
  function pyRound(x, n) {
    if (!isFinite(x)) return x;
    var am = x < 0 || Object.is(x, -0);
    var a = Math.abs(x);
    var s = a.toFixed(n); // toFixed: gần nhất theo giá trị CHÍNH XÁC của số nhị phân; hòa thì lấy số lớn hơn
    // Hòa thật sự chỉ khi phần thập phân chính xác sau chữ số n là "5000…": khi đó Python lấy số chẵn.
    var day = a.toFixed(80);
    var cham = day.indexOf(".");
    var duoi = day.slice(cham + 1 + n);
    if (/^50*$/.test(duoi)) {
      var dau = day.slice(0, cham + 1 + n).replace(".", "");
      var cuoi = Number(dau.charAt(dau.length - 1));
      if (cuoi % 2 === 0) s = n > 0 ? day.slice(0, cham + 1 + n) : day.slice(0, cham);
    }
    var v = Number(s);
    return am ? -v : v;
  }

  // f"{x:g}" của Python (đủ cho các tỷ lệ % ở đây)
  function fmtG(x) {
    if (x === 0) return Object.is(x, -0) ? "-0" : "0";
    var v = Number(x.toPrecision(6));
    var e = Math.floor(Math.log10(Math.abs(v)));
    if (e < -4 || e >= 6) {
      var t = v.toExponential().replace(/\.?0+e/, "e");
      return t.replace(/e([+-])(\d)$/, "e$10$2");
    }
    return String(v);
  }

  // sum() của Python 3.12+ (cộng có bù — Neumaier)
  function pySum(ds) {
    var s = 0, c = 0;
    for (var i = 0; i < ds.length; i++) {
      var x = ds[i];
      var t = s + x;
      if (Math.abs(s) >= Math.abs(x)) c += (s - t) + x; else c += (x - t) + s;
      s = t;
    }
    if (c && isFinite(c)) s += c;
    return s;
  }

  // ---- bảng phí (đã tách sẵn bởi Python) ----
  function chonMuc(muc, cheDo) {
    if (CHE_DO.indexOf(cheDo) < 0) {
      var e = new Error("che_do phải là một trong ('thap', 'giua', 'cao'), nhận '" + cheDo + "'");
      e.name = "ValueError";
      throw e;
    }
    if (cheDo === "thap") return muc.thap;
    if (cheDo === "cao") return muc.cao;
    return (muc.thap + muc.cao) / 2;
  }

  function laKhoang(muc) { return muc.thap !== muc.cao; }

  function apDung(d, ngay) {
    if (d.tu_ngay && ngay < d.tu_ngay) return false;
    if (d.den_ngay && ngay > d.den_ngay) return false;
    return true;
  }

  function BangPhi(duLieu) {
    if (!duLieu || !duLieu.dong) throw ThieuDuLieu("không thấy bảng phí trong app");
    this.dong = duLieu.dong;
    this.nguon_tep = duLieu.nguon_tep;
    this.sha256 = duLieu.sha256;
  }

  BangPhi.prototype.nganhCua = function (san, loaiPhi) {
    var ra = [], bs = boDau(san);
    this.dong.forEach(function (d) {
      if (boDau(d.san) === bs && d.loai_phi === loaiPhi && ra.indexOf(d.nganh) < 0) ra.push(d.nganh);
    });
    return ra;
  };

  BangPhi.prototype.khopNganh = function (san, loaiPhi, nganh) {
    var ds = this.nganhCua(san, loaiPhi);
    if (!ds.length) throw ThieuDuLieu("bảng phí không có '" + loaiPhi + "' cho sàn '" + san + "'");
    var q = boDau(nganh);
    for (var i = 0; i < ds.length; i++) if (boDau(ds[i]) === q) return ds[i];
    var con = ds.filter(function (n) { return boDau(n).indexOf(q) >= 0; });
    if (con.length === 1) return con[0];
    if (!con.length) throw ThieuDuLieu("không có ngành '" + nganh + "' cho " + san + "/" + loaiPhi + ". Ngành có: " + ds.join(" | "));
    throw ThieuDuLieu("ngành '" + nganh + "' khớp nhiều dòng: " + con.join(" | ") + " — gõ cụ thể hơn");
  };

  BangPhi.prototype.tra = function (san, loaiPhi, nganh, ngay) {
    var n = this.khopNganh(san, loaiPhi, nganh), bs = boDau(san);
    var uv = this.dong.filter(function (d) {
      return boDau(d.san) === bs && d.loai_phi === loaiPhi && d.nganh === n && apDung(d, ngay);
    });
    if (!uv.length) throw ThieuDuLieu("không có mức '" + loaiPhi + "' (" + san + ", " + n + ") hiệu lực ngày " + ngay);
    uv = uv.map(function (d, i) { return { d: d, i: i }; });
    uv.sort(function (a, b) {
      var ka = a.d.tu_ngay || "0000-00-00", kb = b.d.tu_ngay || "0000-00-00";
      if (ka !== kb) return ka < kb ? -1 : 1;
      var ba = a.d.suy_tu_ghi_chu ? 0 : 1, bb = b.d.suy_tu_ghi_chu ? 0 : 1; // not suy_tu_ghi_chu
      if (ba !== bb) return ba - bb;
      return a.i - b.i;
    });
    var d = uv[uv.length - 1].d;
    if (!d.muc) throw ThieuDuLieu("mức '" + loaiPhi + "' (" + san + ", " + n + ") CHƯA XÁC MINH trong bảng phí");
    return d;
  };

  BangPhi.prototype.dongDau = function (san, loaiPhi) {
    var bs = boDau(san);
    for (var i = 0; i < this.dong.length; i++) {
      var d = this.dong[i];
      if (boDau(d.san) === bs && d.loai_phi === loaiPhi && !d.suy_tu_ghi_chu) return d;
    }
    return null;
  };

  // ---- máy tính ----
  function chuanSan(san) {
    var s = boDau(san).replace(/ /g, "");
    if (s.indexOf("shopee") === 0) return "shopee";
    if (s.indexOf("tiktok") === 0) return "tiktok";
    throw ThieuDuLieu("sàn '" + san + "' chưa hỗ trợ (chỉ Shopee, TikTok Shop)");
  }

  var MAC_DINH = {
    giam_gia_shop: 0, dong_goi: 0, ship_shop_chiu: 0, tham_gia_voucher_san: false, hoa_hong_aff_shop_tra: 0,
    quang_cao_pct: 0, ty_le_hoan: 0, ship_tra_hang: null, ty_le_hong_hang_hoan: 30, thue_gtgt: null,
    thue_tncn: null, che_do_khoang: "cao", phi_nganh_tu_nhap: null, shop_moi_mien_phi_co_dinh: false,
    tinh_phi_ha_tang: true, hoa_hong_aff_nhan: null, thue_aff: 0
  };

  function homNay() {
    var d = new Date();
    var p = function (x) { return (x < 10 ? "0" : "") + x; };
    return d.getFullYear() + "-" + p(d.getMonth() + 1) + "-" + p(d.getDate());
  }

  function dauVao(o) {
    var dv = {};
    Object.keys(MAC_DINH).forEach(function (k) { dv[k] = MAC_DINH[k]; });
    Object.keys(o || {}).forEach(function (k) { if (o[k] !== undefined) dv[k] = o[k]; });
    if (laNone(dv.ngay_ban) || dv.ngay_ban === "") dv.ngay_ban = homNay();
    if (laNone(dv.nganh)) dv.nganh = "";
    return dv;
  }

  function hieuLuc(d) {
    if (d.tu_ngay && d.den_ngay) return d.tu_ngay + " → " + d.den_ngay;
    if (d.tu_ngay) return "từ " + d.tu_ngay;
    if (d.den_ngay) return "đến " + d.den_ngay;
    return "CHƯA XÁC MINH";
  }

  function ghiCanhBao(cb, ten, d) {
    d.canh_bao.forEach(function (c) { cb.push(ten + ": " + c); });
    if (String(d.do_tin_cay).toUpperCase() !== "CAO") cb.push(ten + ": độ tin cậy " + (d.do_tin_cay || "không ghi"));
  }

  function MayTinh(bangPhi) { this.bp = bangPhi; }

  MayTinh.prototype._tyLe = function (sanCsv, loai, nganh, ngay, cheDo, ten, cb) {
    var d = this.bp.tra(sanCsv, loai, nganh, ngay);
    var v = chonMuc(d.muc, cheDo);
    if (laKhoang(d.muc)) {
      cb.push(ten + ": bảng phí ghi khoảng " + fmtG(d.muc.thap) + "–" + fmtG(d.muc.cao) + "% (ngành '" + d.nganh + "'), " +
        "đang dùng mức '" + cheDo + "' = " + fmtG(v) + "%. Tra PDF ngành cấp 3 để có mức chính xác.");
    }
    ghiCanhBao(cb, ten, d);
    return [v, d];
  };

  MayTinh.prototype.tinh = function (vao, timHoaVon) {
    if (timHoaVon === undefined) timHoaVon = true;
    var dv = dauVao(vao);
    var cb = [];
    var ma = chuanSan(dv.san);
    var cfg = SAN[ma];
    var sanCsv = cfg.ten;
    var ngay = dv.ngay_ban;
    if (laNone(dv.gia_ban) || laNone(dv.gia_von)) throw ThieuDuLieu("thiếu giá bán hoặc giá vốn");
    var am = [["giá bán", dv.gia_ban], ["giá vốn", dv.gia_von], ["giảm giá shop", dv.giam_gia_shop],
      ["đóng gói", dv.dong_goi], ["ship shop chịu", dv.ship_shop_chiu]];
    for (var i = 0; i < am.length; i++) if (am[i][1] < 0) throw ThieuDuLieu(am[i][0] + " không được âm");
    var pt = [["tỷ lệ hoàn", dv.ty_le_hoan], ["quảng cáo %", dv.quang_cao_pct],
      ["tỷ lệ hỏng hàng hoàn", dv.ty_le_hong_hang_hoan], ["hoa hồng affiliate", dv.hoa_hong_aff_shop_tra]];
    for (i = 0; i < pt.length; i++) {
      if (!(0 <= pt[i][1] && pt[i][1] <= 100)) throw ThieuDuLieu(pt[i][0] + " phải trong 0–100 (%), nhận " + soPy(pt[i][1]));
    }

    var rev = dv.gia_ban - dv.giam_gia_shop;
    if (rev <= 0) throw ThieuDuLieu("giá bán sau giảm giá shop phải > 0");

    // ---- phí ngành ----
    var nganhTra = dv.nganh;
    if (ma === "tiktok" && !dv.nganh.trim()) nganhTra = cfg.nganh_mac_dinh;
    var fPct, dF, tenNganh, r_;
    if (!laNone(dv.phi_nganh_tu_nhap)) {
      fPct = dv.phi_nganh_tu_nhap;
      dF = null;
      tenNganh = dv.nganh;
      cb.push("Phí ngành do người dùng nhập tay (" + fmtG(fPct) + "%) — không lấy từ bảng phí");
    } else {
      r_ = this._tyLe(sanCsv, cfg.phi_nganh, nganhTra, ngay, dv.che_do_khoang, "Phí ngành", cb);
      fPct = r_[0]; dF = r_[1];
      tenNganh = dF.nganh;
    }
    if (ma === "shopee" && dv.shop_moi_mien_phi_co_dinh) {
      var dUu = this.bp.dongDau("Shopee", "uu_dai_nguoi_ban_moi");
      if (dUu && apDung(dUu, ngay)) {
        fPct = 0.0;
        cb.push("Đang áp dụng miễn phí cố định shop mới (30 ngày, tối đa 200 đơn thành công, sản phẩm " +
          "đầu tiên đăng từ 01/11/2026). Hết ưu đãi thì lợi nhuận GIẢM — chạy lại không có cờ này.");
      } else {
        cb.push("Cờ miễn phí cố định shop mới bị bỏ qua: ngày bán trước 01/11/2026");
      }
    }

    var chiPhi = [];
    function them(ten, soTien, tyLe, d) {
      chiPhi.push({
        ten: ten, so_tien: pyRound(soTien, 2), ty_le: laNone(tyLe) ? null : tyLe,
        nguon: d ? d.nguon : "người dùng nhập (GIẢ ĐỊNH)",
        do_tin_cay: d ? d.do_tin_cay : "", hieu_luc: d ? hieuLuc(d) : ""
      });
    }

    them("Giá vốn", dv.gia_von);
    if (dv.dong_goi) them("Đóng gói", dv.dong_goi);
    if (dv.ship_shop_chiu) them("Ship shop chịu", dv.ship_shop_chiu);
    them("Phí ngành (" + cfg.phi_nganh + ")", fPct / 100 * rev, fPct, dF);

    r_ = this._tyLe(sanCsv, cfg.phi_gd[0], cfg.phi_gd[1], ngay, "cao", "Phí giao dịch", cb);
    var tPct = r_[0], dT = r_[1];
    them("Phí giao dịch (" + cfg.phi_gd[0] + ")", tPct / 100 * rev, tPct, dT);

    var dH = this.bp.tra(sanCsv, cfg.phi_don[0], cfg.phi_don[1], ngay);
    ghiCanhBao(cb, "Phí mỗi đơn", dH);
    var H = dH.muc.cao;
    if (ma === "shopee") {
      if (dv.tinh_phi_ha_tang) {
        cb.push(CANH_BAO_HA_TANG);
      } else {
        cb.push("Đang BỎ phí hạ tầng 3.000đ (kịch bản 'chỉ Mall mới thu' — CHƯA XÁC MINH, không thận trọng)");
        H = 0.0;
      }
    }
    them("Phí mỗi đơn (" + cfg.phi_don[0] + ")", H, null, dH);

    var vTien = 0.0;
    if (dv.tham_gia_voucher_san) {
      r_ = this._tyLe(sanCsv, cfg.voucher_san[0], cfg.voucher_san[1], ngay, "cao", "Voucher sàn", cb);
      var vPct = r_[0], dV = r_[1];
      vTien = vPct / 100 * rev;
      if (!laNone(dV.muc.tran_vnd)) vTien = Math.min(vTien, dV.muc.tran_vnd);
      them("Voucher sàn (" + cfg.voucher_san[0] + ")", vTien, vPct, dV);
      if (ma === "shopee") cb.push("Voucher Xtra: cơ sở tính (trước/sau KM người bán) CHƯA XÁC MINH — công cụ tính trên Rev");
    }

    var aTien = dv.hoa_hong_aff_shop_tra / 100 * rev;
    if (aTien) them("Hoa hồng affiliate shop trả", aTien, dv.hoa_hong_aff_shop_tra);

    var dGtgt = this.bp.tra("Chung (san khau tru)", "thue_khau_tru_GTGT", "Hang hoa", ngay);
    var dTncn = this.bp.tra("Chung (san khau tru)", "thue_khau_tru_TNCN", "Hang hoa", ngay);
    var g = laNone(dv.thue_gtgt) ? dGtgt.muc.cao : dv.thue_gtgt;
    var p = laNone(dv.thue_tncn) ? dTncn.muc.cao : dv.thue_tncn;
    var kPct = g + p;
    var kTien = kPct / 100 * rev;
    them("Thuế sàn khấu trừ (GTGT " + fmtG(g) + "% + TNCN " + fmtG(p) + "%)", kTien, kPct, dGtgt);

    var tong = pySum(chiPhi.map(function (c) { return c.so_tien; }));
    var cm = rev - tong;
    var phiSanAff = fPct / 100 * rev + tPct / 100 * rev + H + vTien + aTien;

    // ---- hoàn hàng ----
    var r = dv.ty_le_hoan / 100;
    var dd = dv.ty_le_hong_hang_hoan / 100;
    var sret;
    if (!laNone(dv.ship_tra_hang)) {
      sret = dv.ship_tra_hang;
    } else if (cfg.ship_tra) {
      sret = this.bp.tra(sanCsv, cfg.ship_tra[0], cfg.ship_tra[1], ngay).muc.cao;
    } else {
      sret = 0.0;
      if (r > 0) cb.push("TikTok: phí ship trả hàng shop chịu CHƯA XÁC MINH trong bảng phí — đang tính 0đ; " +
        "nhập --ship-tra-hang để thận trọng");
    }
    var chiHoan = dv.dong_goi + dv.ship_shop_chiu + sret + dd * dv.gia_von;
    if (cfg.phi_don_mat_khi_hoan) chiHoan += H;
    if (r > 0) cb.push("Hoàn hàng: tỷ lệ hoàn " + fmtG(dv.ty_le_hoan) + "% và hỏng " + fmtG(dv.ty_le_hong_hang_hoan) + "% là GIẢ ĐỊNH " +
      "(tỷ lệ hoàn điển hình CHƯA XÁC MINH)");
    var lnTruoc = (1 - r) * cm - r * chiHoan;
    var qc = dv.quang_cao_pct / 100 * rev;
    var ln = lnTruoc - qc;

    var roas = lnTruoc > 0 ? rev / lnTruoc : null;
    if (roas === null) cb.push("LỖ ngay cả trước quảng cáo → không có ROAS hòa vốn; không nên chạy quảng cáo SKU này");

    var giaHv = timHoaVon ? this._giaHoaVon(dv, true) : null;
    var giaHvTqc = timHoaVon ? this._giaHoaVon(dv, false) : null;

    var dVat = this.bp.dongDau("Shopee", "GTGT_tren_phi_san");
    if (dVat && dVat.den_ngay && ngay > dVat.den_ngay) {
      cb.push("Ngày bán sau " + dVat.den_ngay + ": GTGT 8% trên phí sàn hết hạn; nếu về 10% phí đã gồm " +
        "thuế có thể tăng ~×1,10/1,08 (+1,85% tương đối) — CHƯA XÁC MINH, cần bảng phí v2");
    }
    if (ma === "tiktok") cb.push("TikTok: cơ sở phí giao dịch gồm cả trợ giá sàn + ship khách trả; công cụ tính trên Rev " +
      "(ship khách trả coi như triệt tiêu)");
    cb.push("Thuế khấu trừ 1,5%: nếu doanh thu năm ≤ 1 tỷ thì là tiền TẠM khấu trừ, có thể được hoàn — " +
      "công cụ vẫn trừ (thận trọng). Hỏi kế toán (mục 7 p4-tai-chinh.md)");

    var aff = null;
    if (!laNone(dv.hoa_hong_aff_nhan)) {
      var hh = (1 - r) * dv.hoa_hong_aff_nhan / 100 * rev * (1 - dv.thue_aff / 100);
      var lnAff = hh - qc;
      aff = {
        hoa_hong_nhan_pct: dv.hoa_hong_aff_nhan,
        hoa_hong_ky_vong_moi_don: pyRound(hh, 2),
        quang_cao: pyRound(qc, 2),
        ln_affiliate: pyRound(lnAff, 2),
        roas_hoa_von_affiliate: hh > 0 ? pyRound(rev / hh, 4) : null,
        von_hang_moi_don_nhap_truc_tiep: dv.gia_von,
        von_hang_moi_don_affiliate: 0,
        chenh_lech_nhap_truc_tiep_tru_affiliate: pyRound(ln - lnAff, 2)
      };
      cb.push("So sánh affiliate: tỷ lệ hoa hồng nhận là GIẢ ĐỊNH; thuế khấu trừ trên thu nhập affiliate " +
        "CHƯA XÁC MINH (mặc định 0%, nhập --thue-aff). Hoa hồng chỉ tính cho đơn không hoàn.");
    }

    return {
      san: sanCsv, nganh: tenNganh, ngay_ban: ngay, rev: rev, chi_phi: chiPhi, cm: pyRound(cm, 2),
      chi_phi_moi_don_hoan: pyRound(chiHoan, 2), ln_truoc_qc: pyRound(lnTruoc, 2), quang_cao: pyRound(qc, 2),
      ln: pyRound(ln, 2), bien_rong: pyRound(ln / rev, 6), roas_hoa_von: roas ? pyRound(roas, 4) : null,
      gia_hoa_von: giaHv, gia_hoa_von_truoc_qc: giaHvTqc,
      thue_tam_khau_tru: pyRound((1 - r) * kTien, 2), affiliate: aff, canh_bao: cb,
      khong_dam_bao: DONG_KHONG_DAM_BAO,
      ty_le_phi_san_aff_chua_thue: pyRound(phiSanAff / rev, 6),
      ty_le_phi_gom_thue_khau_tru: pyRound((phiSanAff + kTien) / rev, 6)
    };
  };

  MayTinh.prototype._giaHoaVon = function (dv, qcOn) {
    var lo = dv.giam_gia_shop + 1.0;
    var hi = Math.max(dv.gia_ban, dv.gia_von, 1000.0) * 2;
    var self = this;
    var f = function (P) { return self._ln(dv, P, qcOn); };
    try {
      var co = false;
      for (var i = 0; i < 40; i++) {
        if (f(hi) > 0) { co = true; break; }
        hi *= 2;
      }
      if (!co) return null;
      if (f(lo) >= 0) return pyRound(lo, 0);
      while (hi - lo > 0.5) {
        var mid = (lo + hi) / 2;
        if (f(mid) >= 0) hi = mid; else lo = mid;
      }
      return pyRound(hi, 0);
    } catch (e) {
      if (e && e.thieuDuLieu) return null;
      throw e;
    }
  };

  MayTinh.prototype._ln = function (dv, gia, qcOn) {
    var x = {};
    Object.keys(dv).forEach(function (k) { x[k] = dv[k]; });
    x.gia_ban = gia;
    x.hoa_hong_aff_nhan = null;
    x.quang_cao_pct = qcOn ? dv.quang_cao_pct : 0.0;
    return this.tinh(x, false).ln;
  };

  // số trong thông báo lỗi: đầu vào luôn là float (như dòng lệnh P4) → Python in 120.0
  function soPy(v) {
    if (typeof v === "number" && Number.isInteger(v)) return v.toFixed(1);
    return String(v);
  }

  // ---- tiện ích giống Python (chuỗi / ngày) ----
  function pyStr(s) { // repr() của chuỗi
    s = String(s);
    var q = (s.indexOf("'") >= 0 && s.indexOf('"') < 0) ? '"' : "'";
    var t = s.replace(/\\/g, "\\\\");
    if (q === "'") t = t.replace(/'/g, "\\'");
    return q + t + q;
  }
  function pyList(ds) { return "[" + ds.map(pyStr).join(", ") + "]"; }
  function pyTuple(ds) { return "(" + ds.map(pyStr).join(", ") + ")"; }
  function phay0(x) { // f"{x:,.0f}"
    var v = pyRound(x, 0);
    var am = v < 0 || Object.is(v, -0);
    return (am ? "-" : "") + Math.abs(v).toFixed(0).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  }
  function vndCham(x) { return phay0(x).replace(/,/g, ".") + " đ"; } // _vnd() của so_lai_lo
  var NGAY_MS = 86400000;
  function soNgay(iso) { // date.fromisoformat (YYYY-MM-DD hoặc YYYYMMDD) → số ngày; null nếu sai
    var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(iso) || /^(\d{4})(\d{2})(\d{2})$/.exec(iso);
    if (!m) return null;
    var y = +m[1], mo = +m[2], d = +m[3];
    var t = Date.UTC(y, mo - 1, d);
    var k = new Date(t);
    if (y < 1 || k.getUTCFullYear() !== y || k.getUTCMonth() !== mo - 1 || k.getUTCDate() !== d) return null;
    return Math.round(t / NGAY_MS);
  }
  function isoTuSo(n) { return new Date(n * NGAY_MS).toISOString().slice(0, 10); }

  // ================= AFFILIATE (apps/finance/taichinh/affiliate.py) =================
  var AFF = {
    NGUON: "https://shopee.vn/blog/?p=190331 (bài Shopee 09/07/2026, qua p1-radar.md) [CAO]",
    PHI_PCT: 0.98, PHI_TU: "2025-05-16", THUE_PCT: 10.0, THUE_TU: "2025-11-20", NGUONG: 250000
  };

  function hoaHongGocTuDon(giaTriDon, tyLe, soDon, tyLeHuy) {
    if (laNone(soDon)) soDon = 1;
    if (laNone(tyLeHuy)) tyLeHuy = 0.0;
    if (giaTriDon < 0 || soDon < 0) throw ThieuDuLieu("giá trị đơn / số đơn không được âm");
    var ks = [["tỷ lệ hoa hồng", tyLe], ["tỷ lệ hủy/hoàn", tyLeHuy]];
    for (var i = 0; i < ks.length; i++) {
      if (!(0 <= ks[i][1] && ks[i][1] <= 100)) throw ThieuDuLieu(ks[i][0] + " phải trong 0–100 (%), nhận " + soPy(ks[i][1]));
    }
    return giaTriDon * tyLe / 100 * soDon * (1 - tyLeHuy / 100);
  }

  function thucNhan(o) {
    var hh = o.hoa_hong_goc, cnd = laNone(o.chi_phi_noi_dung) ? 0.0 : o.chi_phi_noi_dung;
    var san = laNone(o.san) ? "shopee" : o.san, ngay = laNone(o.ngay) ? null : o.ngay;
    var nguong = laNone(o.nguong_tinh_tren) ? "truoc_phi" : o.nguong_tinh_tren;
    if (hh < 0 || cnd < 0) throw ThieuDuLieu("hoa hồng / chi phí nội dung không được âm");
    if (nguong !== "truoc_phi" && nguong !== "sau_phi") throw ThieuDuLieu("nguong_tinh_tren phải là 'truoc_phi' hoặc 'sau_phi'");
    var s = String(san).toLowerCase().replace(/ /g, "");
    if (!(s.indexOf("shopee") === 0 || s.indexOf("tiktok") === 0)) throw ThieuDuLieu("sàn '" + san + "' chưa hỗ trợ");
    var cb = [];
    var phi = laNone(o.phi_nen_tang_pct) ? AFF.PHI_PCT : o.phi_nen_tang_pct;
    var thue = laNone(o.thue_pct) ? AFF.THUE_PCT : o.thue_pct;
    var tenSan;
    if (s.indexOf("tiktok") === 0) {
      tenSan = "TikTok Shop";
      if (laNone(o.phi_nen_tang_pct) || laNone(o.thue_pct)) {
        cb.push("TikTok Affiliate: phí nền tảng và thuế khấu trừ CHƯA XÁC MINH — đang dùng tạm luật Shopee " +
          "(0,98% + 10% khi ≥ 250.000đ) cho thận trọng; nhập phi_nen_tang_pct / thue_pct khi có nguồn");
      }
    } else {
      tenSan = "Shopee";
    }
    if (ngay !== null && (ngay < AFF.PHI_TU || ngay < AFF.THUE_TU)) {
      cb.push("Ngày trước 16/05/2025 / 20/11/2025: mức cũ CHƯA XÁC MINH — công cụ vẫn áp mức hiện hành");
    }
    var phiTien = hh * phi / 100;
    var sauPhi = hh - phiTien;
    var soNguong = nguong === "truoc_phi" ? hh : sauPhi;
    var coThue = soNguong >= AFF.NGUONG;
    var thueTien = coThue ? sauPhi * thue / 100 : 0.0;
    var sauThue = sauPhi - thueTien;
    var tn = sauThue - cnd;
    cb.push("Ngưỡng 250.000đ so với hoa hồng " + (nguong === "truoc_phi" ? "gốc (trước phí 0,98%)" : "sau phí 0,98%") +
      " — nguồn không nói rõ cơ sở, CHƯA XÁC MINH");
    if (coThue) {
      cb.push("Thuế 10% bị khấu trừ TRÊN TOÀN KHOẢN (không chỉ phần vượt). Hộ kinh doanh có được khấu trừ theo " +
        "mức khác / được hoàn hay không: CHƯA XÁC MINH — hỏi kế toán");
    } else if (soNguong >= 0.9 * AFF.NGUONG) {
      cb.push("Khoản sát ngưỡng 250.000đ: vượt ngưỡng thì bị khấu trừ 10% toàn khoản (thực nhận có thể GIẢM khi " +
        "hoa hồng tăng nhẹ). Đây là thuế tạm khấu trừ, không phải lý do để chia nhỏ khoản");
    }
    if (tn < 0) cb.push("Chi phí nội dung lớn hơn hoa hồng sau thuế → LỖ");
    cb.push("Nguồn phí / thuế affiliate: " + AFF.NGUON);
    return {
      san: tenSan, hoa_hong_goc: pyRound(hh, 2), phi_nen_tang: pyRound(phiTien, 2), sau_phi: pyRound(sauPhi, 2),
      co_khau_tru_thue: coThue, thue_khau_tru: pyRound(thueTien, 2), sau_thue: pyRound(sauThue, 2),
      chi_phi_noi_dung: pyRound(cnd, 2), thuc_nhan: pyRound(tn, 2), canh_bao: cb, khong_dam_bao: DONG_KHONG_DAM_BAO
    };
  }

  function thucNhanTuDon(o) {
    var goc0 = hoaHongGocTuDon(o.gia_tri_don, o.ty_le_hoa_hong, o.so_don, o.ty_le_huy_hoan);
    var x = {};
    Object.keys(o).forEach(function (k) { x[k] = o[k]; });
    x.hoa_hong_goc = goc0;
    var kq = thucNhan(x);
    kq.canh_bao.unshift("Tỷ lệ hoa hồng, tỷ lệ hủy/hoàn, số đơn là GIẢ ĐỊNH; lịch thanh toán hoa hồng (gộp theo tháng?) " +
      "CHƯA XÁC MINH — công cụ coi cả kỳ là MỘT khoản");
    return kq;
  }

  // ================= DROPSHIP (apps/finance/taichinh/dropship.py) =================
  var NGUON_TIEN_VE = "bao-cao/dot0/p4-tai-chinh.md §4 (Shopee Uni bài 234; TikTok knowledge_id=6091769578850065) [CAO]";
  var CHU_KY = [ // (sàn, loại shop) → [ngày chờ sau giao thành công, ngày rút về ngân hàng]
    ["shopee", "thuong", 4, 1], ["shopee", "moi", 4, 1], ["shopee", "rui_ro", 15, 1],
    ["tiktok", "moi", 8, 1], ["tiktok", "thuong", 3, 1], ["tiktok", "mall", 1, 1], ["tiktok", "rui_ro", 15, 1]
  ];
  var TRUONG_DROPSHIP = ["phi_ncc", "ty_le_huy", "chi_phi_moi_don_huy", "ngay_giao", "loai_shop"];

  function chuKyTienVe(san, loaiShop) {
    if (laNone(loaiShop)) loaiShop = "moi";
    var ma = chuanSan(san);
    for (var i = 0; i < CHU_KY.length; i++) if (CHU_KY[i][0] === ma && CHU_KY[i][1] === loaiShop) return [CHU_KY[i][2], CHU_KY[i][3]];
    var ds = CHU_KY.map(function (c) { return [c[0], c[1]]; }).sort(function (a, b) {
      return a[0] !== b[0] ? (a[0] < b[0] ? -1 : 1) : (a[1] < b[1] ? -1 : a[1] > b[1] ? 1 : 0);
    });
    throw ThieuDuLieu("chưa có chu kỳ tiền về cho " + pyTuple([ma, loaiShop]) + "; chọn trong [" + ds.map(pyTuple).join(", ") + "]");
  }

  MayTinh.prototype.dropship = function (vao, o, timHoaVon) {
    if (timHoaVon === undefined) timHoaVon = true;
    o = o || {};
    var dv = dauVao(vao);
    var phiNcc = laNone(o.phi_ncc) ? 0.0 : o.phi_ncc, tyLeHuy = laNone(o.ty_le_huy) ? 0.0 : o.ty_le_huy;
    var ngayGiao = laNone(o.ngay_giao) ? 3 : o.ngay_giao, loaiShop = laNone(o.loai_shop) ? "moi" : o.loai_shop;
    if (phiNcc < 0 || ngayGiao < 0) throw ThieuDuLieu("phí NCC / số ngày giao không được âm");
    if (!(0 <= tyLeHuy && tyLeHuy < 100)) throw ThieuDuLieu("tỷ lệ hủy phải trong 0–<100 (%), nhận " + soPy(tyLeHuy));
    var cHuy = laNone(o.chi_phi_moi_don_huy) ? phiNcc : o.chi_phi_moi_don_huy;
    if (cHuy < 0) throw ThieuDuLieu("chi phí đơn hủy không được âm");
    var x = {};
    Object.keys(dv).forEach(function (k) { x[k] = dv[k]; });
    x.dong_goi = dv.dong_goi + phiNcc;
    var kq = this.tinh(x, timHoaVon);
    var h = tyLeHuy / 100;
    var r = dv.ty_le_hoan / 100;
    var lnDat = (1 - h) * kq.ln - h * cHuy;
    var lnTqcDat = (1 - h) * kq.ln_truoc_qc - h * cHuy;
    var ck = chuKyTienVe(dv.san, loaiShop);
    var truKhiHoan = (kq.chi_phi_moi_don_hoan - (dv.dong_goi + phiNcc + dv.ship_shop_chiu) -
      dv.ty_le_hong_hang_hoan / 100 * dv.gia_von);
    var ngoaiSan = ["Giá vốn", "Đóng gói", "Ship shop chịu"];
    var tienSanTra = kq.rev - pySum(kq.chi_phi.filter(function (c) { return ngoaiSan.indexOf(c.ten) < 0; })
      .map(function (c) { return c.so_tien; }));
    var tienVe = (1 - h) * ((1 - r) * tienSanTra - r * truKhiHoan);
    var chiRa = (1 - h) * (dv.gia_von + phiNcc + dv.dong_goi + dv.ship_shop_chiu + kq.quang_cao) + h * cHuy;
    var cb = ["Dropship: giá NCC, phí NCC " + phay0(phiNcc) + "đ, tỷ lệ hủy " + fmtG(tyLeHuy) + "%, chi phí mỗi đơn hủy " +
      phay0(cHuy) + "đ, giao " + ngayGiao + " ngày là GIẢ ĐỊNH",
      "Tiền về: chờ " + ck[0] + " ngày sau giao + rút " + ck[1] + " ngày (shop '" + loaiShop + "') — " + NGUON_TIEN_VE,
      "Hàng bị trả về địa chỉ shop (không về NCC) — NCC có nhận lại / hoàn tiền hàng trả không: CHƯA XÁC MINH, " +
      "tùy hợp đồng NCC",
      "Quảng cáo tính trên đơn không hủy; tiền quảng cáo nạp trước được coi là chi lúc đặt đơn",
      "Tiền mặt ≠ lãi: hàng hoàn còn bán được nằm thành tồn kho (đã trả NCC, chưa thu lại tiền)"];
    if (lnDat < 0) cb.push("LỖ mỗi đơn đặt sau hủy / hoàn");
    return {
      don: kq, gia_ncc: dv.gia_von, phi_ncc: phiNcc, ty_le_huy: tyLeHuy, chi_phi_moi_don_huy: cHuy,
      ln_moi_don_dat: pyRound(lnDat, 2), ln_truoc_qc_moi_don_dat: pyRound(lnTqcDat, 2),
      chi_ra_moi_don_dat: pyRound(chiRa, 2), tien_ve_moi_don_dat: pyRound(tienVe, 2),
      ngay_cho: ck[0], ngay_rut: ck[1], ngay_giao: ngayGiao, ngay_tre: ngayGiao + ck[0] + ck[1],
      canh_bao: cb, khong_dam_bao: DONG_KHONG_DAM_BAO
    };
  };

  function vonUngTruoc(o) {
    var dmn = o.don_moi_ngay, cr = o.chi_ra_moi_don, tv = o.tien_ve_moi_don, tre = o.ngay_tre;
    var n = laNone(o.so_ngay) ? 56 : o.so_ngay;
    if (dmn < 0 || cr < 0 || tre < 0 || n < 1) throw ThieuDuLieu("đầu vào vốn ứng trước không hợp lệ");
    var soDu = 0.0, thapNhat = 0.0, ngayThap = null, ngayHoan = null;
    for (var t = 0; t < n; t++) {
      soDu -= dmn * cr;
      if (t >= tre) soDu += dmn * tv;
      if (soDu < thapNhat - 1e-9) { thapNhat = soDu; ngayThap = t; }
      if (ngayHoan === null && t > 0 && soDu >= 0 && thapNhat < 0) ngayHoan = t;
    }
    return {
      von_ung_truoc_can: pyRound(-thapNhat, 2), ngay_am_sau_nhat: ngayThap, ngay_so_du_cong_don_ve_0: ngayHoan,
      so_du_cuoi_ky: pyRound(soDu, 2), so_ngay_mo_phong: n,
      ghi_chu: "GIẢ ĐỊNH số đơn đều mỗi ngày; chưa tính chi phí cố định (công cụ, hàng mẫu). " + DONG_KHONG_DAM_BAO
    };
  }

  // ================= SỔ LÃI LỖ (apps/finance/taichinh/so_lai_lo.py) =================
  var COT_SO = ["ngay", "thu_chi", "loai", "mo_hinh", "kenh", "so_tien_vnd", "phan_bo_tu", "phan_bo_den", "mo_ta", "nguon"];
  var LOAI_THU = ["doanh_thu_don", "hoa_hong_affiliate", "hoan_thue", "thu_khac"];
  var LOAI_CHI = ["gia_von_ncc", "phi_ncc", "phi_san", "thue_khau_tru", "ship", "hoan_tien_khach", "chi_phi_huy_don",
    "quang_cao", "cong_cu", "hang_mau", "noi_dung", "ke_toan_phap_ly", "chi_khac"];
  var MO_HINH = ["affiliate", "dropship", "chung"];
  var KENH = ["shopee", "tiktok", "chung", "khac"];
  function xep(ds) { return ds.slice().sort(); }

  function docNgaySo(s, ten, vt) {
    var n = soNgay(s.trim());
    if (n === null) throw ThieuDuLieu(vt + ": " + ten + " '" + s + "' không đúng dạng YYYY-MM-DD");
    return n;
  }

  function kiemDong(row, vt) {
    if (laNone(vt)) vt = "dòng";
    var g = {};
    COT_SO.forEach(function (k) { g[k] = String(laNone(row[k]) ? "" : row[k]).trim(); });
    var tc = g.thu_chi.toLowerCase();
    if (tc !== "thu" && tc !== "chi") throw ThieuDuLieu(vt + ": thu_chi phải là 'thu' hoặc 'chi', nhận '" + g.thu_chi + "'");
    var loai = g.loai.toLowerCase();
    var hopLe = tc === "thu" ? LOAI_THU : LOAI_CHI;
    if (hopLe.indexOf(loai) < 0) throw ThieuDuLieu(vt + ": loai '" + g.loai + "' không hợp lệ cho '" + tc + "'; chọn trong " + pyList(xep(hopLe)));
    var mh = g.mo_hinh.toLowerCase();
    if (MO_HINH.indexOf(mh) < 0) throw ThieuDuLieu(vt + ": mo_hinh phải trong " + pyList(xep(MO_HINH)));
    var kenh = g.kenh.toLowerCase() || "chung";
    if (KENH.indexOf(kenh) < 0) throw ThieuDuLieu(vt + ": kenh phải trong " + pyList(xep(KENH)));
    var st = g.so_tien_vnd.replace(/[.,_]/g, "");
    if (!/^\d+$/.test(st) || Number(st) <= 0) throw ThieuDuLieu(vt + ": so_tien_vnd phải là số nguyên dương (VND), nhận '" + g.so_tien_vnd + "'");
    var tu = g.phan_bo_tu ? docNgaySo(g.phan_bo_tu, "phan_bo_tu", vt) : null;
    var den = g.phan_bo_den ? docNgaySo(g.phan_bo_den, "phan_bo_den", vt) : null;
    if ((tu === null) !== (den === null)) throw ThieuDuLieu(vt + ": cần cả phan_bo_tu và phan_bo_den (hoặc bỏ trống cả hai)");
    if (tu !== null && den < tu) throw ThieuDuLieu(vt + ": phan_bo_den trước phan_bo_tu");
    return { ngay: docNgaySo(g.ngay, "ngay", vt), thu_chi: tc, loai: loai, mo_hinh: mh, kenh: kenh, so_tien_vnd: Number(st),
      phan_bo_tu: tu, phan_bo_den: den, mo_ta: g.mo_ta, nguon: g.nguon };
  }

  function phanTrong(d, tu, den) {
    var a = d.phan_bo_tu !== null ? d.phan_bo_tu : d.ngay, b = d.phan_bo_tu !== null ? d.phan_bo_den : d.ngay;
    var so = (b - a) + 1;
    var giao = (Math.min(b, den) - Math.max(a, tu)) + 1;
    if (giao <= 0) return 0.0;
    return (d.thu_chi === "thu" ? 1 : -1) * d.so_tien_vnd * giao / so;
  }

  function tongHop(dong, tu, den) {
    var thu = 0.0, chi = 0.0, theoMh = {}, theoLoai = {};
    xep(MO_HINH).forEach(function (m) { theoMh[m] = 0.0; });
    dong.forEach(function (d) {
      var v = phanTrong(d, tu, den);
      if (!v) return;
      if (v > 0) thu += v; else chi += -v;
      theoMh[d.mo_hinh] += v;
      theoLoai[d.loai] = (theoLoai[d.loai] || 0.0) + v;
    });
    var mh = {}, lo = {};
    Object.keys(theoMh).forEach(function (k) { mh[k] = pyRound(theoMh[k], 0); });
    Object.keys(theoLoai).sort().forEach(function (k) { lo[k] = pyRound(theoLoai[k], 0); });
    return { tu: isoTuSo(tu), den: isoTuSo(den), thu: pyRound(thu, 0), chi: pyRound(chi, 0), lai_rong: pyRound(thu - chi, 0),
      theo_mo_hinh: mh, theo_loai: lo };
  }

  // o = {dong: [dòng thô theo cột sổ], ngay_cuoi: "YYYY-MM-DD", so_ngay: 28}
  function kiemCongDot1(o) {
    var dong = (o.dong || []).map(function (r) { return kiemDong(r); });
    var cuoi = soNgay(o.ngay_cuoi);
    if (cuoi === null) { var e = new Error("Invalid isoformat string: " + pyStr(o.ngay_cuoi)); e.name = "ValueError"; throw e; }
    var n = laNone(o.so_ngay) ? 28 : o.so_ngay;
    if (!dong.length) throw ThieuDuLieu("sổ trống");
    var tu = cuoi - (n - 1);
    var dau = Math.min.apply(null, dong.map(function (d) { return d.phan_bo_tu !== null ? d.phan_bo_tu : d.ngay; }));
    var cuaSo = tongHop(dong, tu, cuoi);
    var tuDau = tongHop(dong, Math.min(dau, tu), cuoi);
    var cb = ["Cổng đo trên cửa sổ 4 tuần cuối; cũng in lãi cộng dồn TỪ ĐẦU dự án để chủ dự án thấy cả hai",
      "Thuế khấu trừ được tính là CHI (thận trọng) dù có thể được hoàn khi doanh thu năm ≤ 1 tỷ"];
    dong.forEach(function (d) {
      if (d.thu_chi === "chi" && d.phan_bo_tu === null && d.ngay < tu &&
          ["cong_cu", "hang_mau", "noi_dung", "ke_toan_phap_ly"].indexOf(d.loai) >= 0 && d.so_tien_vnd >= 1000000) {
        cb.push("Khoản " + d.loai + " " + vndCham(d.so_tien_vnd) + " ngày " + isoTuSo(d.ngay) + " trước cửa sổ và KHÔNG phân bổ — nếu là gói dùng " +
          "trong cửa sổ, hãy điền phan_bo_tu / phan_bo_den để cổng không bị 'dễ' giả");
      }
    });
    var muon = dong.filter(function (d) { return d.ngay > cuoi; });
    if (muon.length) cb.push(muon.length + " dòng có ngày sau " + isoTuSo(cuoi) + " — không tính");
    return { cua_so_4_tuan: cuaSo, tu_dau_du_an: tuDau, dat_cong_dot1: cuaSo.lai_rong >= 0, canh_bao: cb,
      khong_dam_bao: DONG_KHONG_DAM_BAO };
  }

  // ---- chạy một ví dụ theo loại (dùng cho kiểm khớp và giao diện) ----
  function chayViDu(mt, loai, dv) {
    loai = loai || "don";
    if (loai === "don") return mt.tinh(dv);
    if (loai === "dropship") {
      var don = {}, ds = {};
      Object.keys(dv).forEach(function (k) { (TRUONG_DROPSHIP.indexOf(k) >= 0 ? ds : don)[k] = dv[k]; });
      return mt.dropship(don, ds);
    }
    if (loai === "affiliate") return thucNhan(dv);
    if (loai === "affiliate_tu_don") return thucNhanTuDon(dv);
    if (loai === "von_ung_truoc") return vonUngTruoc(dv);
    if (loai === "so_lai_lo") return kiemCongDot1(dv);
    throw new Error("loại ví dụ lạ: " + loai);
  }

  goc.TaiChinh = {
    BangPhi: BangPhi, MayTinh: MayTinh, ThieuDuLieu: ThieuDuLieu, SAN: SAN, chuanSan: chuanSan, boDau: boDau,
    pyRound: pyRound, fmtG: fmtG, pySum: pySum, DONG_KHONG_DAM_BAO: DONG_KHONG_DAM_BAO, MAC_DINH: MAC_DINH,
    homNay: homNay, thucNhan: thucNhan, thucNhanTuDon: thucNhanTuDon, hoaHongGocTuDon: hoaHongGocTuDon,
    chuKyTienVe: chuKyTienVe, CHU_KY: CHU_KY, vonUngTruoc: vonUngTruoc, kiemDong: kiemDong, kiemCongDot1: kiemCongDot1,
    chayViDu: chayViDu, phay0: phay0
  };
})(typeof globalThis !== "undefined" ? globalThis : this);
