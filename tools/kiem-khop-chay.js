// Chạy lõi tính JS NẰM TRONG app/daovang.html (đúng bản giao cho chủ dự án) trên bộ ví dụ.
// Dùng: node tools/kiem-khop-chay.js <đường dẫn daovang.html>   (ví dụ JSON đọc từ stdin, kết quả JSON ra stdout)
// Gọi bởi tools/kiem-khop.py. Không gọi mạng.
"use strict";
const fs = require("fs");
const vm = require("vm");

const html = fs.readFileSync(process.argv[2], "utf8");
const lay = (id) => {
  const m = html.match(new RegExp('<script id="' + id + '"[^>]*>([\\s\\S]*?)</script>'));
  if (!m) throw new Error("không thấy <script id=\"" + id + "\"> trong " + process.argv[2]);
  return m[1];
};
const hop = { };
hop.globalThis = hop;
vm.createContext(hop);
vm.runInContext(lay("loi-tinh"), hop, { filename: "daovang.html#loi-tinh" });
const TC = hop.TaiChinh;
const mt = new TC.MayTinh(new TC.BangPhi(JSON.parse(lay("bang-phi"))));

const viDu = JSON.parse(fs.readFileSync(0, "utf8"));
const ra = viDu.map((v) => {
  try {
    return { ok: JSON.parse(JSON.stringify(mt.tinh(v.dau_vao))) };
  } catch (e) {
    return { loi: (e && e.name) || "Error", thong_diep: String(e && e.message) };
  }
});
process.stdout.write(JSON.stringify(ra));
