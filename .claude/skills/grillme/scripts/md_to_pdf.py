"""Chuyển một tệp Markdown (tiếng Việt) thành PDF bằng Microsoft Edge chạy ẩn.

Cách dùng:  python md_to_pdf.py <vao.md> <ra.pdf>
Không cần cài thêm thư viện. Hỗ trợ: tiêu đề #, danh sách -, 1., bảng |, **đậm**, *nghiêng*, `mã`, ```khối mã```, ---.
"""
import html, os, re, subprocess, sys, tempfile

EDGE = [r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"]

CSS = """
body{font-family:'Segoe UI',Arial,sans-serif;font-size:10.5pt;line-height:1.45;color:#1a1a1a;margin:0}
h1{font-size:17pt;border-bottom:2px solid #333;padding-bottom:4px}
h2{font-size:13pt;margin-top:18px;border-bottom:1px solid #bbb}
h3{font-size:11.5pt}
table{border-collapse:collapse;width:100%;margin:8px 0;page-break-inside:auto}
th,td{border:1px solid #999;padding:4px 6px;vertical-align:top;font-size:9.5pt}
th{background:#eee}
tr{page-break-inside:avoid}
code{background:#f2f2f2;padding:0 3px;font-family:Consolas,monospace;font-size:9pt}
pre{background:#f6f6f6;border:1px solid #ddd;padding:6px;white-space:pre-wrap;font-size:9pt}
hr{border:0;border-top:1px solid #ccc}
@page{size:A4;margin:16mm 14mm}
"""

BASE = "."

def _img(src):
    if re.match(r"^[a-z]+:", src):
        return src
    return "file:///" + os.path.abspath(os.path.join(BASE, src)).replace("\\", "/")

def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)",
               lambda m: f'<img alt="{m.group(1)}" src="{_img(m.group(2))}" style="max-width:100%;border:1px solid #ccc">', t)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<![*\w])\*([^*\n]+)\*(?![*\w])", r"<i>\1</i>", t)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', t)
    return t

def cells(row):
    row = row.strip().strip("|")
    return [c.strip() for c in re.split(r"(?<!\\)\|", row)]

def convert(md):
    out, lines, i = [], md.splitlines(), 0
    stack = []  # danh sách đang mở: ('ul'|'ol', thụt lề)
    def close_lists(to=0):
        while len(stack) > to:
            out.append(f"</{stack.pop()[0]}>")
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("```"):
            close_lists(); buf = []; i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                buf.append(html.escape(lines[i])); i += 1
            out.append("<pre>" + "\n".join(buf) + "</pre>"); i += 1; continue
        if ln.strip().startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|?\s*:?-{3,}", lines[i + 1]):
            close_lists()
            head = cells(ln); i += 2
            out.append("<table><tr>" + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr>")
            while i < len(lines) and lines[i].strip().startswith("|"):
                out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in cells(lines[i])) + "</tr>"); i += 1
            out.append("</table>"); continue
        m = re.match(r"^(#{1,4})\s+(.*)", ln)
        if m:
            close_lists(); n = len(m.group(1)); out.append(f"<h{n}>{inline(m.group(2))}</h{n}>"); i += 1; continue
        if re.match(r"^\s*-{3,}\s*$", ln):
            close_lists(); out.append("<hr>"); i += 1; continue
        m = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)", ln)
        if m:
            ind, kind = len(m.group(1)), ("ol" if m.group(2)[0].isdigit() else "ul")
            while stack and stack[-1][1] > ind:
                out.append(f"</{stack.pop()[0]}>")
            if not stack or stack[-1][1] < ind:
                stack.append((kind, ind)); out.append(f"<{kind}>")
            out.append(f"<li>{inline(m.group(3))}</li>"); i += 1; continue
        if ln.strip().startswith(">"):
            close_lists(); out.append(f"<blockquote>{inline(ln.strip()[1:].strip())}</blockquote>"); i += 1; continue
        if not ln.strip():
            close_lists(); i += 1; continue
        close_lists(); out.append(f"<p>{inline(ln.strip())}</p>"); i += 1
    close_lists()
    return "\n".join(out)

def main(src, dst):
    global BASE
    BASE = os.path.dirname(os.path.abspath(src))
    md = open(src, encoding="utf-8").read()
    doc = f"<!doctype html><html lang='vi'><head><meta charset='utf-8'><style>{CSS}</style></head><body>{convert(md)}</body></html>"
    fd, tmp = tempfile.mkstemp(suffix=".html"); os.close(fd)
    open(tmp, "w", encoding="utf-8").write(doc)
    import shutil
    edge = next((e for e in EDGE if os.path.exists(e)), None) or next(
        (shutil.which(n) for n in ("microsoft-edge", "google-chrome", "google-chrome-stable",
                                   "chromium", "chromium-browser", "msedge", "chrome") if shutil.which(n)), None)
    if not edge:
        html_out = os.path.splitext(os.path.abspath(dst))[0] + ".html"
        os.replace(tmp, html_out)
        sys.exit("Không tìm thấy trình duyệt (Edge/Chrome/Chromium) để in PDF. Đã lưu bản HTML: " + html_out
                 + " — mở bằng trình duyệt rồi In → Lưu thành PDF, hoặc cài chromium.")
    dst = os.path.abspath(dst)
    profile = tempfile.mkdtemp(prefix="md2pdf-")  # hồ sơ riêng: không đụng trình duyệt đang mở
    for mode in ("--headless", "--headless=new"):  # tùy phiên bản trình duyệt, một trong hai chạy được
        extra = [] if os.name == "nt" else ["--no-sandbox"]  # Linux (máy chủ đám mây) thường cần cờ này
        subprocess.run([edge, mode, "--disable-gpu", "--no-pdf-header-footer", *extra,
                        f"--user-data-dir={profile}", f"--print-to-pdf={dst}", "file:///" + tmp.replace("\\", "/")],
                       check=False, timeout=120, capture_output=True)
        # Edge có thể thoát ngay và giao việc in cho tiến trình con: chờ tệp xuất hiện và ngừng lớn lên
        import time
        last = -1
        for _ in range(60):
            size = os.path.getsize(dst) if os.path.exists(dst) else 0
            if size > 0 and size == last:
                break
            last = size
            time.sleep(1)
        if os.path.exists(dst) and os.path.getsize(dst) > 0:
            break
    os.remove(tmp)
    shutil.rmtree(profile, ignore_errors=True)
    if not os.path.exists(dst) or os.path.getsize(dst) == 0:
        sys.exit("In PDF thất bại.")
    print(dst, os.path.getsize(dst), "byte")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
