# ARBA PT Knowledge Base House

Satu tempat untuk semua KB (TC Reference) Private Tour ARBA.

- Hub: https://prod-at22.github.io/pt-kb-house/
- Setiap destinasi: `https://prod-at22.github.io/pt-kb-house/<destinasi>/` (senarai dalam `destinations.json`)

## Sumber data: PT R&D Costing Hub (mulai 9 Okt 2026)
Kandungan setiap KB dan nombor Simple Calculator kini disimpan dalam **PT R&D Costing Hub**
(`prod-at22/pt-rnd-hub`, fail `data/kb/<destinasi>.json`) — hub ialah source of truth.
Repo ini ialah **mirror**: Action `mirror.yml` menjalankan `kb-build/build.py` dari hub dan menulis semula
blok data dalam setiap KB. **Jangan edit kandungan atau `calc-config.json` di sini** — ia akan ditimpa
pada mirror seterusnya. Edit di hub (Edit costs → Save).

```
<destinasi>/index.html        halaman KB (rupa, CSS, enjin, travel map) — blok data diisi oleh mirror
<destinasi>/assets.json       gambar KB (kosmetik, kekal di sini; hub rujuk sebagai @asset:<kunci>)
<destinasi>/calc-config.json  ditulis oleh mirror dari hub (jangan edit)
<destinasi>/README.md         nota kalkulator destinasi itu (skema calc-config)
```

Yang masih diedit dalam repo ini: rupa/enjin halaman (`index.html` di luar blok `kbdata` dan `CALC_CFG`),
gambar (`assets.json`), `hub.json`, `catalogs.json`.

Repo KB lama (`arba-bali-kb`, `korea-kb` dan lain-lain, senarai dalam `destinations.json`)
sudah **dipadam** (8 Okt 2026). Link lama seperti `prod-at22.github.io/korea-kb/` kini 404;
guna `https://prod-at22.github.io/pt-kb-house/<destinasi>/`.

Bar navigasi terapung (**← Semua KB** + **Katalog PT**) dipasang automatik oleh `nav.yml` (bila
`index.html` diubah di sini) dan oleh `mirror.yml` (selepas mirror), jadi fail tak perlu ada bar itu.

Halaman hub (`index.html`) dijana automatik oleh `.github/scripts/build_hub.py` dari `hub.json`
(nama, negara, kod) — jangan edit `index.html` hub dengan tangan. Tarikh "updated" diambil dari
teks "Last updated" dalam setiap KB.

Tambah destinasi baru: buat folder `<destinasi>/` dengan halaman KB, tambah `"<destinasi>": "-"` dalam
`destinations.json`, satu entri dalam `hub.json`, dan `data/kb/<destinasi>.json` dalam hub.

## Link ke PT Catalog House
Setiap KB ada bar terapung di bawah kiri: **← Semua KB** (balik ke hub) dan **Katalog PT**
(senarai katalog customer untuk destinasi tu). Senarai katalog datang dari `catalogs.json`; kad di hub pula ada butang **Buka Katalog** yang membuka PT Catalog House dengan tapisan `?q=` (lihat `CATQ` dalam `index.html`);
bila katalog baru ditambah di PT Catalog House, tambah juga di sini. Hub pula ada link terus
ke https://prod-at22.github.io/catalog-pt-public/.
