# ARBA Semporna KB — panduan PO

> **Mulai 9 Okt 2026 kandungan KB dan `calc-config.json` datang dari PT R&D Costing Hub** (`prod-at22/rnd-hub`, `data/kb/semporna.json`). Fail di sini ditulis semula oleh mirror — **jangan edit di GitHub repo ini**; edit di hub. Skema di bawah masih terpakai.

KB TC Reference untuk PT Semporna, termasuk tab **Simple Calculator**.
Live: https://prod-at22.github.io/pt-kb-house/semporna/

Sumber harga: katalog **PAKEJ SEMPORNA BASIC (3D2N) 2026 V4** dan
**STANDARD (4D3N) 2026 V4** (last updated 24 Ogos 2026), rate card operasi
(Google Sheet Semporna) dan `R&D Sheet/Semporna new.xlsx` tab **RAW DATA**.

---

## Nak ubah harga? Edit `calc-config.json` sahaja

`calc-config.json` dibaca oleh kalkulator pada masa runtime. Ubah fail itu di
GitHub, commit, dan harga berubah dalam ~30 saat — **tiada rebuild diperlukan**.
Jangan sentuh `index.html` untuk perubahan harga.

Kalau JSON rosak (koma tertinggal, petik tak tutup), kalkulator jatuh balik ke
config terbenam dan papar **notis merah** di atas tab. Itu tandanya JSON perlu
dibetulkan.

### Medan yang paling kerap diubah

| Nak ubah | Cari medan | Nota |
|---|---|---|
| Harga tier pakej | `variants[].tiers` | `a` = adult, `c` = child with bed, `n` = child no bed. Ada dua baris: `from:1,to:1` (1 pax) dan `from:2,to:10`. |
| Single supplement | `variants[].single` | Basic 1200, Standard 1500 |
| Tarikh peak season | `variants[].peak.windows` | `["mula","tamat",null,0,"Peak Season"]` — elemen ke-4 ialah surcaj per malam pakej **asas** (sekarang `0`, lihat di bawah) |
| Surcaj travel 2027 | `extraSurcharge[0].perPax` | sekarang 150, untuk Jan–Jun 2027 |
| Late booking | `lateBooking` | `{"lt":45,"amount":50}` |
| Deposit | `deposit` | 500 |
| Surcaj upgrade akomodasi | `variants[].ext.rates.up*` | `normal` = kadar upgrade, `peak` = upgrade **campur** surcaj peak |
| Kadar malam tambahan | `variants[].ext.rates.n*` dan `ext.night` | per pax per malam |
| Harga add-on | `addons[]` | `["nama", dewasa, kanak, asas]` — asas: `pax` / `unit` / `share` |
| Kadar tambah/tolak meal | `mealDelta` | `{"add":65,"drop":20}` per pax per hidangan |

### Kunci kadar akomodasi

Setiap kunci di bawah ada dalam **kedua-dua** varian (`variants[0].ext.rates`
dan `variants[1].ext.rates`) — kalau ubah harga, **ubah kedua-dua** kecuali
memang nak berbeza ikut pakej.

**Surcaj upgrade** (`normal` = katalog, `peak` = katalog + surcaj peak):

| Kunci | Akomodasi | normal | peak |
|---|---|---|---|
| `upTownB` | Seafest Boutique | 0 | 30 |
| `upTown30` | Seafest Lepa Wing Sea View · Seafest Hotel | 30 | 60 |
| `upTown50` | Seafest Hotel Sea View | 50 | 100 |
| `upWc1a` | 1★ Nusakuya · Blue Ocean | 0 | 60 |
| `upWc1b` | 1★ Maglami-Lami · Aminah · Starz Standard | 150 | 210 |
| `upWc2a` | 2★ Danglai · Dayang | 450 | 515 |
| `upWc2b` | 2★ Royal Resort Standard Suite | 600 | 700 (Basic) / 680 (Standard) |
| `upWc3a` | 3★ Sipadan Kapalai Standard | 2050 | 2135 |
| `upWc3b` | 3★ Sipadan Water Village Sea View | 1350 | 1435 |

**Malam tambahan** (harga jual, per pax per malam): `ext.night` = Wingtat
(160 / 220 peak), dan kunci `nBoutique` 115/135 · `nLepaC` 175/205 ·
`nSeafest` 190/230 · `nLato` 360 · `nNusa` 410/380/330 ikut pax ·
`nDanglai` 710/610/510 · `nDayang` 680/580 (+60 peak) · `nRoyal` 860/760
(+100 Basic / +80 Standard peak).

---

## Dua perkara yang sengaja dibiar "kadar belum diisi"

Ini **bukan pepijat**. Rate card memang tiada kadar tersiar, jadi kalkulator
tandakan cip merah `kadar?` supaya TC sebut harga dengan operator, bukan quote
RM 0 secara senyap:

1. **Transport hari tambahan** (`ext.rates.day`) — charter dalam rate card
   ialah transfer bandar, bukan day tour.
2. **Tolak 1 malam** (`ext.rates.nightShort`) — lajur "Tolak 1 Night" dalam
   rate card kosong sepenuhnya.

Bila PO dapat kadar sebenar, tukar `normal` dan `peak` daripada `0` kepada
kadar itu dan cip merah hilang sendiri.

---

## Peak season pakej asas = RM 0

Katalog v4 **tidak** mengenakan surcaj peak pada akomodasi asas
(**Wingtat Hotel** dan **Lato Lato Water Chalet**). Surcaj peak hanya melekat
pada akomodasi yang di-**upgrade**. Jadi:

- tarikh peak + akomodasi asas → harga **sama** dengan normal season, dan
  quotation PDF **tidak** menulis baris surcaj RM 0 (baris `Season` tetap
  kata "Peak Season");
- tarikh peak + upgrade → surcaj peak masuk melalui kunci `up*` di atas.

**Perlu disahkan:** kos Wingtat naik RM260 → RM380/bilik (RM60/pax) dalam
peak, tetapi katalog v4 tidak mengenakan apa-apa. Katalog v3 dahulu mengenakan
RM30–60/pax/malam pada baris asas. Kalau ini silap katalog, letak kadar
sebenar pada elemen ke-4 setiap tetingkap dalam `variants[].peak.windows`.

---

## Senarai penuh "perlu disahkan"

Ada dalam KB sendiri: tab **Simple Customisation** → seksyen
**"Kadar yang PERLU DISAHKAN dengan PO"** (10 baris, termasuk Royal Resort
peak RM80 vs RM100, meal Standard 3B/2L/3D vs 3B/1L/2D, dan
"28–31 September" yang tidak wujud).

---

## Rebuild penuh (hanya bila itinerary / pilihan dropdown berubah)

```bash
python3 scripts/mkconfig_semporna.py
python3 scripts/build_calc.py --kb "<KB tanpa calc>.html" \
  --config references/config-semporna.json \
  --out pub/index.html --external-config calc-config.json
node test_calc.js pub/index.html
node test_calc_semporna.js pub/index.html
node audit_invariants.js pub/index.html
node audit_pdf.js pub/index.html
```

**Tarik `calc-config.json` terbaru dari GitHub dahulu** dan selaraskan
`references/config-semporna.json`, kalau tidak suntingan PO akan ditimpa.
