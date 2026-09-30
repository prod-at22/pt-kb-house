# Tambah bar navigasi terapung pada setiap KB dalam house: "Semua KB" (balik ke hub)
# dan "Katalog PT" (senarai katalog customer untuk destinasi itu, dari catalogs.json).
# Idempotent: blok lama dibuang dahulu, jadi selamat dijalankan setiap kali sync.
import html, json, pathlib, re

START, END = "<!--kb-house-nav-->", "<!--/kb-house-nav-->"
OLD = re.compile(r"<!--kb-house-back--><a [^>]*>&larr; Semua KB</a>")
CATALOGS = json.load(open("catalogs.json"))
PILL = ("background:#c8172b;color:#fff;font:800 13px Poppins,Trebuchet MS,sans-serif;padding:10px 16px;"
        "border-radius:999px;text-decoration:none;box-shadow:0 6px 20px rgba(0,0,0,.25);cursor:pointer;"
        "list-style:none;display:inline-block")

def nav(slug):
    items = "".join(
        f'<a href="{html.escape(c["url"])}" target="_blank" rel="noopener" style="display:block;padding:9px 14px;'
        f'color:#1c1c1c;text-decoration:none;font:600 13px Poppins,Trebuchet MS,sans-serif;border-top:1px solid #eee">'
        f'{html.escape(c["title"])} &#8599;</a>'
        for c in CATALOGS.get(slug, []))
    cat = ""
    if items:
        cat = (f'<details style="position:relative"><summary style="{PILL};background:#fff;color:#c8172b">Katalog PT &#9652;</summary>'
               f'<div style="position:absolute;left:0;bottom:calc(100% + 8px);min-width:260px;max-width:80vw;background:#fff;'
               f'border-radius:14px;box-shadow:0 10px 30px rgba(0,0,0,.2);overflow:hidden">'
               f'<div style="padding:10px 14px;font:800 11px Poppins,sans-serif;letter-spacing:.08em;color:#6b6b6b">KATALOG CUSTOMER</div>'
               f'{items}</div></details>')
    return (f'{START}<div style="position:fixed;left:16px;bottom:calc(16px + env(safe-area-inset-bottom,0px));z-index:9999;'
            f'display:flex;gap:8px;align-items:flex-end"><a href="../" style="{PILL}">&larr; Semua KB</a>{cat}</div>{END}')

for slug in json.load(open("destinations.json")):
    p = pathlib.Path(slug, "index.html")
    if not p.exists():
        continue
    s = p.read_text(encoding="utf-8")
    s = OLD.sub("", s)
    s = re.sub(re.escape(START) + ".*?" + re.escape(END), "", s, flags=re.S)
    block = nav(slug)
    i = s.rfind("</body>")
    s = s[:i] + block + s[i:] if i != -1 else s + block
    p.write_text(s, encoding="utf-8")
