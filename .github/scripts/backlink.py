# Tambah butang "Semua KB" terapung pada setiap KB dalam house (idempotent).
import json, pathlib
MARK = "<!--kb-house-back-->"
BTN = MARK + ('<a href="../" style="position:fixed;left:16px;bottom:calc(16px + env(safe-area-inset-bottom,0px));z-index:9999;'
  'background:#c8172b;color:#fff;font:800 13px Poppins,Trebuchet MS,sans-serif;padding:10px 16px;border-radius:999px;'
  'text-decoration:none;box-shadow:0 6px 20px rgba(0,0,0,.25)">&larr; Semua KB</a>')
for slug in json.load(open("destinations.json")):
    p = pathlib.Path(slug, "index.html")
    if not p.exists(): continue
    s = p.read_text(encoding="utf-8")
    if MARK in s: continue
    i = s.rfind("</body>")
    s = s[:i] + BTN + s[i:] if i != -1 else s + BTN
    p.write_text(s, encoding="utf-8")
