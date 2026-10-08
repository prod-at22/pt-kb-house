# Bina index.html hub (senarai ringkas gaya PT Catalog House) dari hub.json.
# Tarikh "updated" diambil dari teks "Last updated" dalam setiap KB; kalau tiada,
# guna medan "updated" dalam hub.json, kemudian tarikh commit terakhir folder itu.
import datetime, html, json, pathlib, re, subprocess

MONTHS = {m: i for i, m in enumerate(
    "jan feb mar apr may jun jul aug sep oct nov dec".split(), 1)}
MONTHS.update({"mei": 5, "ogo": 8, "okt": 10, "dis": 12})

def updated(k):
    slug = k["slug"]
    s = pathlib.Path(slug, "index.html").read_text(encoding="utf-8")
    m = re.search(r"Last updated:?\s*(\d{1,2})\s+([A-Za-z]{3})[a-z]*\s+(\d{4})", s)
    if m and m.group(2).lower() in MONTHS:
        return datetime.date(int(m.group(3)), MONTHS[m.group(2).lower()], int(m.group(1))).isoformat()
    if k.get("updated"):
        return k["updated"]
    out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", slug],
                         capture_output=True, text=True).stdout.strip()
    return out or ""

LOGO = pathlib.Path(".github/scripts/logo.txt").read_text().strip()
kbs = sorted(json.load(open("hub.json", encoding="utf-8")), key=lambda k: (k["name"].lower(), k["flag"]))
rows = []
for k in kbs:
    e = {x: html.escape(k[x]) for x in k}
    search = " ".join([k["name"], k["name"].replace("-", " "), k["country"], k["code"], k["slug"], k["flag"]]).lower()
    country = f'<span class="tier">{e["country"]}</span>' if k["country"] != k["name"] else ""
    flag = f'<span class="tier old">{e["flag"]}</span>' if k["flag"] else ""
    upd = updated(k)
    rows.append(
        f'<a class="row" href="{e["slug"]}/" data-search="{html.escape(search)}">'
        f'<span class="dest">{e["name"]}{country}{flag}</span>'
        f'<span class="dur">{e["code"]}</span>'
        f'<span class="upd">{"updated " + upd if upd else ""}</span></a>')

page = f'''<!doctype html>
<html lang="ms">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>PT KB House | ARBA Travel</title>
<style>
body {{ margin:0; font-family:"Segoe UI",-apple-system,BlinkMacSystemFont,Roboto,Helvetica,Arial,sans-serif;
  background:#f4f6f8; color:#1b2430; line-height:1.5; }}
.page {{ max-width:720px; margin:0 auto; padding:2.5rem 1rem 3rem; }}
header {{ display:flex; justify-content:space-between; align-items:center; margin-bottom:1.25rem; }}
h1 {{ font-size:1.35rem; margin:0; }}
header img {{ height:30px; }}
.filter {{ width:100%; box-sizing:border-box; font:inherit; font-size:0.9rem; padding:0.6rem 0.9rem; margin-bottom:1rem;
  border:1px solid #e2e6ea; border-radius:10px; background:#fff; color:inherit; }}
.filter:focus {{ outline:none; border-color:#be1e2d; }}
.row {{ display:flex; align-items:baseline; gap:1rem; padding:0.9rem 1.1rem; margin-bottom:0.6rem;
  background:#fff; border:1px solid #e2e6ea; border-radius:10px; text-decoration:none; color:inherit; }}
.row:hover {{ border-color:#be1e2d; }}
.dest {{ font-weight:700; flex:1; }}
.tier {{ display:inline-block; margin-left:0.5rem; padding:0.05rem 0.5rem; border-radius:999px;
  background:#f7e2e4; color:#8f1620; font-size:0.72rem; font-weight:700; letter-spacing:0.03em;
  text-transform:uppercase; vertical-align:middle; }}
.tier.old {{ background:#eceff2; color:#4a5568; }}
.dur {{ color:#4a5568; font-size:0.88rem; }}
.upd {{ color:#4a5568; font-size:0.8rem; min-width:8.5em; text-align:right; }}
.empty {{ display:none; padding:1.5rem; text-align:center; color:#4a5568; font-size:0.9rem; }}
footer {{ text-align:center; font-size:0.78rem; color:#4a5568; padding-top:1.5rem; }}
footer a {{ color:#be1e2d; }}
@media (max-width:520px) {{
  .row {{ flex-wrap:wrap; gap:0.25rem 0.75rem; }}
  .dest {{ flex:1 1 100%; }}
  .upd {{ text-align:left; min-width:0; }}
}}
</style>
</head>
<body>
<div class="page">
<header><h1>PT KB House</h1>
<img src="{LOGO}" alt="ARBA Travel"></header>
<input class="filter" id="filter" type="search" placeholder="Filter by destination, country or code…" aria-label="Filter knowledge bases" autocomplete="off">
{chr(10).join(rows)}
<p class="empty" id="empty">Tiada KB yang sepadan.</p>
<footer>{len(kbs)} knowledge bases &middot; <a href="https://prod-at22.github.io/catalog-pt-public/">PT Catalog House</a> &middot; ARBA Travel</footer>
</div>
<script>
(function () {{
  var box = document.getElementById('filter'), empty = document.getElementById('empty');
  var rows = document.querySelectorAll('.row');
  box.addEventListener('input', function () {{
    var terms = box.value.toLowerCase().split(/\\s+/).filter(Boolean), shown = 0;
    rows.forEach(function (r) {{
      var s = r.getAttribute('data-search');
      var hit = terms.every(function (t) {{ return s.indexOf(t) !== -1; }});
      r.style.display = hit ? '' : 'none';
      if (hit) shown++;
    }});
    empty.style.display = shown ? 'none' : 'block';
  }});
  var q = new URLSearchParams(location.search).get('q');
  if (q) {{ box.value = q; box.dispatchEvent(new Event('input')); }}
}})();
</script>
</body>
</html>
'''
pathlib.Path("index.html").write_text(page, encoding="utf-8")
print(f"index.html: {len(kbs)} KB")
