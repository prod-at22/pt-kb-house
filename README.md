# ARBA PT Knowledge Base House

Satu tempat untuk semua KB (TC Reference) Private Tour ARBA.

- Hub: https://prod-at22.github.io/pt-kb-house/
- Setiap destinasi: `https://prod-at22.github.io/pt-kb-house/<destinasi>/` (senarai dalam `destinations.json`)

## Repo ini satu-satunya sumber
Mulai 8 Okt 2026 semua KB disunting **terus dalam repo ini**, satu folder setiap destinasi:

```
<destinasi>/index.html        halaman KB penuh + enjin kalkulator
<destinasi>/calc-config.json  nombor kalkulator (PO boleh edit terus di GitHub)
<destinasi>/README.md         panduan edit untuk destinasi itu
```

Repo KB lama (`arba-bali-kb`, `korea-kb` dan lain-lain, senarai dalam `destinations.json`)
sudah **dipadam** (8 Okt 2026). Link lama seperti `prod-at22.github.io/korea-kb/` kini 404;
guna `https://prod-at22.github.io/pt-kb-house/<destinasi>/`.

Bar navigasi terapung (**← Semua KB** + **Katalog PT**) dipasang automatik oleh Action
`nav.yml` setiap kali `index.html` berubah, jadi fail yang dimuat naik tak perlu ada bar itu.

Tambah destinasi baru: buat folder `<destinasi>/`, tambah `"<destinasi>": "-"` dalam
`destinations.json`, dan tambah kad dalam `index.html`.

## Link ke PT Catalog House
Setiap KB ada bar terapung di bawah kiri: **← Semua KB** (balik ke hub) dan **Katalog PT**
(senarai katalog customer untuk destinasi tu). Senarai katalog datang dari `catalogs.json`; kad di hub pula ada butang **Buka Katalog** yang membuka PT Catalog House dengan tapisan `?q=` (lihat `CATQ` dalam `index.html`);
bila katalog baru ditambah di PT Catalog House, tambah juga di sini. Hub pula ada link terus
ke https://prod-at22.github.io/catalog-pt-public/.
