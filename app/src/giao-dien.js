/* Giao diện app Đào Vàng — đọc ô nhập, gọi TaiChinh, hiện kết quả, lưu localStorage, sao lưu / nhập lại.
 * Không gọi mạng. Không lưu dữ liệu khách.
 */
(function () {
  "use strict";
  var TC = window.TaiChinh;
  var KHOA = "daovang.loi-nhuan.v1";
  var PHIEN_BAN_SAO_LUU = 1;
  var bp = new TC.BangPhi(JSON.parse(document.getElementById("bang-phi").textContent));
  var mt = new TC.MayTinh(bp);
  var $ = function (id) { return document.getElementById(id); };

  var O_SO = ["gia_ban", "gia_von", "giam_gia_shop", "dong_goi", "ty_le_hoan", "quang_cao_pct", "ship_shop_chiu",
    "hoa_hong_aff_shop_tra", "ship_tra_hang", "ty_le_hong_hang_hoan", "thue_gtgt", "thue_tncn", "phi_nganh_tu_nhap",
    "hoa_hong_aff_nhan", "thue_aff"];
  var O_CHON = ["san", "nganh", "ngay_ban", "che_do_khoang"];
  var O_TICK = ["tham_gia_voucher_san", "shop_moi_mien_phi_co_dinh", "bo_phi_ha_tang"];
  var DS_SO = ["ds_phi_ncc", "ds_ty_le_huy", "ds_chi_phi_moi_don_huy", "ds_ngay_giao", "ds_don_moi_ngay"];
  var AFF_SO = ["aff_gia_tri_don", "aff_ty_le_hoa_hong", "aff_so_don", "aff_ty_le_huy_hoan", "aff_chi_phi_noi_dung"];
  var MAC_DINH_CHON = { ds_loai_shop: "moi", aff_san: "shopee", aff_nguong: "truoc_phi" };
  // ô được lưu (localStorage, sổ SKU, bản sao lưu)
  var LUU_SO = O_SO.concat(DS_SO, AFF_SO);
  var LUU_CHON = O_CHON.concat(Object.keys(MAC_DINH_CHON));
  var LUU_TICK = O_TICK.concat(["la_dropship"]);

  // ---- lưu trữ (bọc try/catch: chế độ ẩn danh có thể chặn) ----
  function docKho() {
    try { var s = localStorage.getItem(KHOA); return s ? JSON.parse(s) : null; } catch (e) { return null; }
  }
  function ghiKho(obj) {
    try { localStorage.setItem(KHOA, JSON.stringify(obj)); return true; } catch (e) { return false; }
  }
  var kho = docKho() || {};
  if (!kho.so_sku) kho.so_sku = [];

  function thongBao(s) {
    var t = $("thong-bao");
    t.textContent = s;
    t.classList.add("hien");
    clearTimeout(thongBao.h);
    thongBao.h = setTimeout(function () { t.classList.remove("hien"); }, 2200);
  }

  // ---- định dạng ----
  function vnd(x) {
    if (x === null || x === undefined) return "—";
    var am = x < 0;
    var s = Math.round(Math.abs(x)).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    return (am ? "−" : "") + s + " đ";
  }
  function so(x, n) {
    if (x === null || x === undefined) return "—";
    return x.toFixed(n === undefined ? 2 : n).replace(".", ",");
  }
  function pct(x) { return so(x * 100, 2) + "%"; }
  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  // "150.000" → 150000 ; "0,5" → 0.5 ; "" → mặc định / null
  function docSo(el) {
    var s = el.value.trim().replace(/\s/g, "");
    if (s === "") return el.dataset.rong === "null" ? null : undefined;
    if (el.dataset.loai === "tien") s = s.replace(/\./g, "").replace(",", ".");
    else s = s.replace(",", ".");
    if (!/^-?\d*\.?\d+$/.test(s)) return NaN;
    return Number(s);
  }

  // ---- danh sách ngành ----
  function napNganh(giuLai) {
    var ma = $("san").value;
    var cfg = TC.SAN[ma];
    var ds = bp.nganhCua(cfg.ten, cfg.phi_nganh);
    var sel = $("nganh");
    sel.innerHTML = "";
    ds.forEach(function (n) {
      var o = document.createElement("option");
      o.value = n; o.textContent = n;
      sel.appendChild(o);
    });
    if (giuLai && ds.indexOf(giuLai) >= 0) sel.value = giuLai;
    else if (ma === "tiktok" && cfg.nganh_mac_dinh) sel.value = cfg.nganh_mac_dinh;
  }

  // ---- đọc / ghi form ----
  function layForm() {
    var f = {};
    LUU_CHON.forEach(function (k) { f[k] = $(k).value; });
    LUU_SO.forEach(function (k) { f[k] = $(k).value; });
    LUU_TICK.forEach(function (k) { f[k] = $(k).checked; });
    return f;
  }
  function datForm(f) {
    f = f || {};
    if (f.san) $("san").value = f.san;
    napNganh(f.nganh);
    $("ngay_ban").value = f.ngay_ban || TC.homNay();
    $("che_do_khoang").value = f.che_do_khoang || "cao";
    Object.keys(MAC_DINH_CHON).forEach(function (k) { $(k).value = f[k] || MAC_DINH_CHON[k]; });
    LUU_SO.forEach(function (k) { $(k).value = f[k] === undefined || f[k] === null ? "" : String(f[k]); });
    LUU_TICK.forEach(function (k) { $(k).checked = !!f[k]; });
  }

  function dauVaoTuForm() {
    var dv = { san: $("san").value, nganh: $("nganh").value, ngay_ban: $("ngay_ban").value || TC.homNay(),
      che_do_khoang: $("che_do_khoang").value };
    var loi = [];
    O_SO.forEach(function (k) {
      var v = docSo($(k));
      if (typeof v === "number" && isNaN(v)) loi.push($(k).labels[0].textContent);
      else if (v !== undefined) dv[k] = v;
    });
    dv.tham_gia_voucher_san = $("tham_gia_voucher_san").checked;
    dv.shop_moi_mien_phi_co_dinh = $("shop_moi_mien_phi_co_dinh").checked;
    dv.tinh_phi_ha_tang = !$("bo_phi_ha_tang").checked;
    return { dv: dv, loi: loi };
  }

  // ---- hiện kết quả ----
  function tomTat(ln, phu) {
    var e = $("tt-ln");
    e.textContent = ln === null ? "—" : vnd(ln);
    e.className = ln === null ? "" : (ln >= 0 ? "lai" : "lo");
    $("tt-phu").textContent = phu || "";
  }

  function veKetQua() {
    var o = $("ket-qua");
    tomTat(null, "");
    var x = dauVaoTuForm();
    if (x.loi.length) { o.innerHTML = '<div class="loi">Ô nhập chưa đúng số: ' + esc(x.loi.join(", ")) + "</div>"; return; }
    if (x.dv.gia_ban === undefined || x.dv.gia_von === undefined) {
      o.innerHTML = '<div class="loi">Nhập giá bán và giá vốn để tính.</div>'; return;
    }
    var kq, kqd = null, von = null;
    var ds = laDropship() ? docNhom(DS_SO, "ds_") : null;
    if (ds && ds.loi.length) { o.innerHTML = '<div class="loi">Ô nhập chưa đúng số: ' + esc(ds.loi.join(", ")) + "</div>"; return; }
    try {
      if (ds) {
        ds.v.loai_shop = $("ds_loai_shop").value;
        var donNgay = ds.v.don_moi_ngay === undefined ? 5 : ds.v.don_moi_ngay;
        delete ds.v.don_moi_ngay;
        kqd = mt.dropship(x.dv, ds.v);
        kq = kqd.don;
        von = TC.vonUngTruoc({ don_moi_ngay: donNgay, chi_ra_moi_don: kqd.chi_ra_moi_don_dat,
          tien_ve_moi_don: kqd.tien_ve_moi_don_dat, ngay_tre: kqd.ngay_tre, so_ngay: 56 });
        von.don_moi_ngay = donNgay;
      } else {
        kq = mt.tinh(x.dv);
      }
    } catch (e) {
      o.innerHTML = '<div class="loi">Thiếu dữ liệu / chưa tính được: ' + esc(e.message) + "</div>"; return;
    }
    var h = [];
    h.push('<div class="ghi">' + esc(kq.san) + " · " + esc(kq.nganh) + " · ngày " + esc(kq.ngay_ban) + "</div>");
    if (kqd) {
      tomTat(kqd.ln_moi_don_dat, "Dropship · tiền về sau " + kqd.ngay_tre + " ngày");
      h.push('<div>Dropship: lợi nhuận / đơn ĐẶT (sau hủy + hoàn)</div><div class="so-lon ' + (kqd.ln_moi_don_dat >= 0 ? "lai" : "lo") + '">' +
        vnd(kqd.ln_moi_don_dat) + "</div>");
      h.push('<div class="chi-so">' +
        "<div><b>" + vnd(kqd.chi_ra_moi_don_dat) + "</b><span>Tiền chi ra / đơn lúc đặt (NCC + QC)</span></div>" +
        "<div><b>" + vnd(kqd.tien_ve_moi_don_dat) + "</b><span>Tiền sàn trả về / đơn, sau " + kqd.ngay_tre + " ngày</span></div>" +
        "<div><b>" + vnd(von.von_ung_truoc_can) + "</b><span>Vốn ứng trước cần (" + so(von.don_moi_ngay, 0) + " đơn/ngày, 8 tuần)</span></div>" +
        "<div><b>" + vnd(kq.ln) + "</b><span>Lợi nhuận / đơn không hủy</span></div></div>");
      h.push('<div class="ghi" style="margin-top:6px">Vốn: ' + esc(von.ghi_chu.split(". Số đầu vào")[0]) + ".</div>");
    } else {
      tomTat(kq.ln, "ROAS hòa vốn " + so(kq.roas_hoa_von));
    }
    if (kqd) h.push('<div style="margin-top:12px;font-weight:600">Đơn không bị hủy (đã tính tỷ lệ hoàn)</div>');
    else h.push('<div>Lợi nhuận ròng / đơn</div><div class="so-lon ' + (kq.ln >= 0 ? "lai" : "lo") + '">' + vnd(kq.ln) + "</div>");
    h.push('<div class="chi-so">' +
      "<div><b>" + pct(kq.bien_rong) + "</b><span>Biên ròng (trên doanh thu đơn)</span></div>" +
      "<div><b>" + so(kq.roas_hoa_von) + "</b><span>ROAS hòa vốn (thực thấp hơn = QC lỗ)</span></div>" +
      "<div><b>" + vnd(kq.gia_hoa_von) + "</b><span>Giá bán hòa vốn (gồm QC)</span></div>" +
      "<div><b>" + vnd(kq.gia_hoa_von_truoc_qc) + "</b><span>Giá bán hòa vốn (không QC)</span></div></div>");

    h.push('<details style="margin-top:12px"><summary>Chi tiết từng khoản</summary><table>');
    h.push('<tr><td>Doanh thu đơn (giá bán − giảm giá shop)</td><td class="so">' + vnd(kq.rev) + "</td></tr>");
    kq.chi_phi.forEach(function (c) {
      var tl = c.ty_le !== null ? " (" + so(c.ty_le) + "%)" : "";
      var ng = c.do_tin_cay ? "<small>nguồn: " + esc(c.nguon) + " · " + esc(c.do_tin_cay) + " · " + esc(c.hieu_luc) + "</small>" : "";
      h.push("<tr><td>− " + esc(c.ten) + tl + ng + '</td><td class="so">' + vnd(c.so_tien) + "</td></tr>");
    });
    h.push('<tr class="tong"><td>Lợi nhuận đơn giao thành công</td><td class="so">' + vnd(kq.cm) + "</td></tr>");
    h.push("<tr><td>Chi phí mỗi đơn bị hoàn</td><td class=\"so\">" + vnd(kq.chi_phi_moi_don_hoan) + "</td></tr>");
    h.push("<tr><td>Lợi nhuận trước quảng cáo (đã tính tỷ lệ hoàn)</td><td class=\"so\">" + vnd(kq.ln_truoc_qc) + "</td></tr>");
    h.push("<tr><td>− Quảng cáo</td><td class=\"so\">" + vnd(kq.quang_cao) + "</td></tr>");
    h.push('<tr class="tong"><td>Lợi nhuận ròng / đơn</td><td class="so">' + vnd(kq.ln) + "</td></tr>");
    h.push("<tr><td>Thuế tạm khấu trừ kỳ vọng / đơn<small>có thể được hoàn nếu doanh thu năm ≤ 1 tỷ</small></td><td class=\"so\">" +
      vnd(kq.thue_tam_khau_tru) + "</td></tr>");
    h.push("</table></details>");

    if (kq.affiliate) {
      var a = kq.affiliate;
      h.push('<details open style="margin-top:8px"><summary>Nhập hàng vs làm affiliate</summary><table>' +
        "<tr><td>Nhập trực tiếp: lợi nhuận / đơn<small>vốn hàng " + vnd(a.von_hang_moi_don_nhap_truc_tiep) + " / đơn</small></td><td class=\"so\">" + vnd(kq.ln) + "</td></tr>" +
        "<tr><td>Affiliate (" + so(a.hoa_hong_nhan_pct) + "% hoa hồng)<small>vốn hàng 0 đ · ROAS hòa vốn " + so(a.roas_hoa_von_affiliate) + "</small></td><td class=\"so\">" + vnd(a.ln_affiliate) + "</td></tr>" +
        '<tr class="tong"><td>Chênh lệch (nhập − affiliate)</td><td class="so">' + vnd(a.chenh_lech_nhap_truc_tiep_tru_affiliate) + "</td></tr>" +
        "</table></details>");
    }
    var canh = kqd ? kqd.canh_bao.concat(kq.canh_bao) : kq.canh_bao;
    h.push('<details style="margin-top:8px"><summary>Cảnh báo (' + canh.length + ")</summary><ul class=\"canh\">" +
      canh.map(function (c) { return "<li>" + esc(c) + "</li>"; }).join("") + "</ul></details>");
    h.push('<div class="dam-bao">' + esc(kq.khong_dam_bao) + "</div>");
    o.innerHTML = h.join("");
  }

  function laDropship() { return $("la_dropship").checked; }

  // đọc một nhóm ô số; tiền tố bỏ khỏi tên khóa (ds_phi_ncc → phi_ncc)
  function docNhom(ids, tienTo) {
    var v = {}, loi = [];
    ids.forEach(function (k) {
      var x = docSo($(k));
      if (typeof x === "number" && isNaN(x)) loi.push($(k).labels[0].textContent);
      else if (x !== undefined) v[k.slice(tienTo.length)] = x;
    });
    return { v: v, loi: loi };
  }

  function veAffiliate() {
    var o = $("aff-ket-qua");
    var n = docNhom(AFF_SO, "aff_");
    if (n.loi.length) { o.innerHTML = '<div class="loi">Ô nhập chưa đúng số: ' + esc(n.loi.join(", ")) + "</div>"; return; }
    if (n.v.gia_tri_don === undefined || n.v.ty_le_hoa_hong === undefined) {
      o.innerHTML = '<div class="ghi">Nhập giá trị đơn và % hoa hồng để tính.</div>'; return;
    }
    n.v.san = $("aff_san").value;
    n.v.nguong_tinh_tren = $("aff_nguong").value;
    var k;
    try { k = TC.thucNhanTuDon(n.v); } catch (e) {
      o.innerHTML = '<div class="loi">Chưa tính được: ' + esc(e.message) + "</div>"; return;
    }
    o.innerHTML = '<div>Thực nhận cả kỳ</div><div class="so-lon ' + (k.thuc_nhan >= 0 ? "lai" : "lo") + '">' + vnd(k.thuc_nhan) + "</div>" +
      "<table>" +
      "<tr><td>Hoa hồng gốc (đơn không hủy / hoàn)</td><td class=\"so\">" + vnd(k.hoa_hong_goc) + "</td></tr>" +
      "<tr><td>− Phí nền tảng</td><td class=\"so\">" + vnd(k.phi_nen_tang) + "</td></tr>" +
      "<tr><td>− Thuế khấu trừ" + (k.co_khau_tru_thue ? "" : "<small>dưới ngưỡng — không bị trừ</small>") + "</td><td class=\"so\">" + vnd(k.thue_khau_tru) + "</td></tr>" +
      "<tr><td>− Chi phí nội dung</td><td class=\"so\">" + vnd(k.chi_phi_noi_dung) + "</td></tr>" +
      '<tr class="tong"><td>Thực nhận</td><td class="so">' + vnd(k.thuc_nhan) + "</td></tr></table>" +
      '<details style="margin-top:8px"><summary>Cảnh báo (' + k.canh_bao.length + ')</summary><ul class="canh">' +
      k.canh_bao.map(function (c) { return "<li>" + esc(c) + "</li>"; }).join("") + "</ul></details>" +
      '<div class="dam-bao">' + esc(k.khong_dam_bao) + "</div>";
  }

  // ---- lưu tự động ----
  function luu() {
    kho.phien_ban = PHIEN_BAN_SAO_LUU;
    kho.form = layForm();
    if (!ghiKho(kho)) thongBao("Trình duyệt chặn lưu — nhớ tải bản sao lưu");
  }
  function capNhat() {
    $("o-dropship").classList.toggle("an", !laDropship());
    veKetQua(); veAffiliate(); luu();
  }

  // ---- sổ SKU ----
  function veSoSku() {
    var ul = $("ds-sku");
    ul.innerHTML = "";
    if (!kho.so_sku.length) { ul.innerHTML = '<li class="ghi">Chưa có SKU nào.</li>'; return; }
    kho.so_sku.forEach(function (s, i) {
      var li = document.createElement("li");
      var ten = document.createElement("span");
      ten.textContent = s.ten + " · " + (s.form.san === "tiktok" ? "TikTok" : "Shopee");
      var nut = document.createElement("span");
      var mo = document.createElement("button"); mo.type = "button"; mo.textContent = "Mở";
      mo.onclick = function () { datForm(s.form); $("ten_sku").value = s.ten; capNhat(); thongBao("Đã mở " + s.ten); };
      var xoa = document.createElement("button"); xoa.type = "button"; xoa.textContent = "Xóa"; xoa.className = "xoa";
      xoa.onclick = function () {
        if (!confirm("Xóa SKU \"" + s.ten + "\" khỏi sổ?")) return;
        kho.so_sku.splice(i, 1); luu(); veSoSku();
      };
      nut.appendChild(mo); nut.appendChild(document.createTextNode(" ")); nut.appendChild(xoa);
      li.appendChild(ten); li.appendChild(nut);
      ul.appendChild(li);
    });
  }
  $("nut-luu-sku").onclick = function () {
    var ten = $("ten_sku").value.trim();
    if (!ten) { thongBao("Nhập tên SKU trước"); return; }
    var f = layForm();
    var cu = kho.so_sku.findIndex(function (s) { return s.ten === ten; });
    var muc = { ten: ten, form: f, luu_luc: new Date().toISOString() };
    if (cu >= 0) kho.so_sku[cu] = muc; else kho.so_sku.push(muc);
    luu(); veSoSku(); thongBao("Đã lưu " + ten);
  };

  // ---- sao lưu ----
  $("nut-tai").onclick = function () {
    luu();
    var goi = { ung_dung: "daovang", loai: "sao-luu-loi-nhuan", phien_ban: PHIEN_BAN_SAO_LUU,
      tao_luc: new Date().toISOString(), bang_phi_sha256: bp.sha256, form: kho.form, so_sku: kho.so_sku };
    var blob = new Blob([JSON.stringify(goi, null, 2)], { type: "application/json" });
    var a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "daovang-sao-luu-" + TC.homNay() + ".json";
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(function () { URL.revokeObjectURL(a.href); }, 1000);
    thongBao("Đã tạo bản sao lưu");
  };
  $("tep-nhap").onchange = function (ev) {
    var tep = ev.target.files && ev.target.files[0];
    if (!tep) return;
    var r = new FileReader();
    r.onload = function () {
      try {
        var g = JSON.parse(r.result);
        if (g.ung_dung !== "daovang" || g.loai !== "sao-luu-loi-nhuan") throw new Error("không phải bản sao lưu Đào Vàng");
        if (!confirm("Thay nhập liệu + sổ SKU hiện tại bằng bản sao lưu " + (g.tao_luc || "") + "?")) return;
        kho.form = g.form || {}; kho.so_sku = Array.isArray(g.so_sku) ? g.so_sku : [];
        datForm(kho.form); veSoSku(); capNhat(); thongBao("Đã nhập bản sao lưu");
      } catch (e) { thongBao("Không đọc được: " + e.message); }
      ev.target.value = "";
    };
    r.readAsText(tep);
  };
  $("nut-xoa").onclick = function () {
    if (!confirm("Xóa các ô nhập (sổ SKU giữ nguyên)?")) return;
    datForm({ san: $("san").value }); $("ten_sku").value = ""; capNhat();
  };

  // ---- khởi động ----
  $("dong-dam-bao").textContent = TC.DONG_KHONG_DAM_BAO;
  $("phien-ban-bang-phi").textContent = "Bảng phí: " + bp.nguon_tep + " · mã " + String(bp.sha256).slice(0, 12) +
    " · " + bp.dong.length + " dòng. Mỗi khoản phí có nguồn + độ tin cậy trong \"Chi tiết\".";
  datForm(kho.form);
  veSoSku();
  $("san").addEventListener("change", function () { napNganh(); capNhat(); });
  document.querySelectorAll("input:not([type=file]):not(#ten_sku),select").forEach(function (el) {
    el.addEventListener(el.tagName === "SELECT" || el.type === "checkbox" || el.type === "date" ? "change" : "input", capNhat);
  });
  $("o-dropship").classList.toggle("an", !laDropship());
  veKetQua();
  veAffiliate();
})();
