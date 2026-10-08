# PT HCM – Dalat – Mui Ne KB — Simple Calculator

Halaman live: **https://prod-at22.github.io/pt-kb-house/dalat/**

Repo ini ada dua fail yang penting:

| Fail | Apa dia | Boleh PO edit? |
|---|---|---|
| `calc-config.json` | **semua nombor dan itinerary kalkulator** — harga tier, single supplement, last minute, surcaj tarikh, upgrade hotel, blok itinerary, add-on | **Ya** — edit terus di sini |
| `index.html` | halaman KB penuh + enjin kalkulator | Tidak — perlu bina semula |

Halaman membaca `calc-config.json` **setiap kali dibuka**. Jadi ubah nombor dalam fail
itu, commit, refresh halaman — terus naik. Tak perlu bina semula `index.html`.

---

## Cara edit

1. Klik `calc-config.json` di atas.
2. Klik ikon pensel (**Edit this file**).
3. Ubah nombor yang perlu.
4. Scroll bawah → **Commit changes**.
5. Tunggu ~30 saat, refresh halaman KB.

### Jaring keselamatan

Kalau JSON tersalah tulis (koma tertinggal, kurungan tak tutup) atau bentuknya salah,
halaman **tidak** rosak. Ia guna balik config lama yang terbenam dalam `index.html`
dan papar notis merah di atas tab Simple Calculator. Kalau notis itu keluar, maksudnya
**suntingan tak terpakai** — betulkan JSON dan commit semula.

Semakan yang dibuat: JSON sah, ada `variants`, setiap varian ada `tiers` penuh
(`from`, `to`, `a`, `c`, `n`), dan bilangan hari dalam `itin` sama dengan `days`.

---

## Di mana benda yang biasa diubah

### Harga katalog (tier per pax)

`variants[].tiers` — `a` = adult, `c` = Child With Bed, `n` = Child No Bed.

```json
{"from": 2, "to": 3, "a": 2597, "c": 2397, "n": 2197}
```

Varian dalam repo ini: `v5d4n` HCM–Dalat–Mui Ne 5D4N · `v4d3n` HCM 4D3N Shopping Tour

### Single supplement

`variants[].single` — RM per pax, flat.

5D4N RM 320/pax (katalog) · 4D3N RM 240/pax (rate card ARBA — katalog 4D3N tulis *quoted upon request*).

### Last minute surcharge

`variants[].lastMinute` — `lt` = bilangan hari sebelum berlepas, `rate2` = kadar 2 pax,
`rate3` = kadar 3 pax ke atas (kedua-duanya RM per pax).

```json
"lastMinute": {"lt": 21, "rate2": 400, "rate3": 300}
```

### Late booking

`lateBooking` (peringkat atas) — `{"lt": 45, "amount": 50}` = RM50 **satu booking**
(bukan per pax) bila tempah kurang 45 hari sebelum berlepas.

### Upgrade hotel 4 bintang

`ext.rates.up4` — RM per pax **per malam**. Ada satu salinan di peringkat atas dan satu
dalam setiap `variants[].ext`. **Ubah kedua-duanya** kalau kadar berubah.

```json
"up4": {"_default": [{"from": 1, "to": 99, "normal": 160, "peak": 160}]}
```

### Surcaj tarikh (2027 dan seterusnya)

`extraSurcharge` — dikenakan bila **tarikh berlepas** jatuh dalam julat `dateIn`.

```json
{"label": "Travel date surcharge 2027 (January - February)", "dateIn": ["2027-01-01", "2027-02-28"], "perPax": 120}
```

### Add-on / optional tour

`addons` — senarai `["Nama", hargaDewasa, hargaKanak]`. Elemen keempat `"unit"`
bermakna harga itu untuk satu unit (per jeep, per pasangan), bukan per pax.

### Itinerary

`variants[].itin` — satu objek per hari. `t` / `act` Bahasa Melayu (papar dalam KB),
`en` / `eact` Bahasa Inggeris (papar dalam PDF quotation customer).

`library` ialah blok tambahan yang muncul dalam dropdown Itinerary setiap hari tetapi
bukan sebahagian itinerari default — TC boleh pilih untuk tukar susunan hari.

---

## Kadar yang SENGAJA dibiar kosong

**Tiada** — Rate Card Operasi (3 Sep 2026) melengkapkan semua kadar extension untuk produk ini. Satu-satunya yang masih kosong: **Day Tour Mekong River** (rate card tinggalkan ruang harga kosong), jadi ia tidak dimasukkan sebagai add-on.

Kalkulator **tidak** senyap-senyap letak RM 0 untuk benda ini. Ia papar cip merah
`kadar?` pada baris hari dan satu baris amaran dalam ringkasan, supaya TC nampak dan
tanya operator. Bila kadar sebenar dah ada, isi `ext.night` dan `ext.rates.day`
(peringkat atas **dan** dalam setiap `variants[].ext`).

---

## Nota sumber

- Tier, single supplement 5D4N, last minute, upgrade 4 bintang dan surcaj travel date 2027
  diambil terus dari katalog: **PT HCM-DALAT-MUINE 5D4N 2026 v2** (11 Mac 2026) dan
  **PT HCM 4D3N 2026 (3 Star, FB)** (8 Dis 2025).
- Single supplement 4D3N (RM 240) dari **R&D Sheet → tab Surcharges**, kerana katalog
  4D3N hanya tulis *quoted upon request*.
- Upgrade 4 bintang berbeza ikut varian: **5D4N RM 160**/pax/malam, **4D3N RM 130**/pax/malam.
- **Tidak dipakai:** baris R&D "Peak Feb-March 2027 +RM50/pax" (tiada dalam katalog mahupun KB)
  dan upgrade 5 bintang RM350 (katalog hanya senaraikan 4 bintang).
- **Blockout:** CNY 2026 16–22 Feb 2026 · CNY 2027 17–18 Feb 2027.

### Rate Card Operasi (PO, 3 Sep 2026) — semua kadar customisation

Kalkulator sekarang berlabuh pada rate card ini, bukan lagi RM 0.

| Perkara | Kadar | Medan config |
|---|---|---|
| Transport hari tambahan | Sedan 2–4 pax RM 300 · Van 5–13 RM 380 · Bus 14+ RM 450 **per transport** | `ext.rates.day` |
| Tolak transport (free & easy) | RM 150 / 190 / 230 per transport | `ext.rates.dayDed` |
| Airport transfer tambahan / tolak | sama seperti di atas | `ext.rates.air` / `airDed` |
| Malam tambahan | 3★ RM 120 · 4★ RM 240 · 5★ RM 320 **per pax per malam** | `ext.night` · `ext.rates.h4` · `h5` |
| Tolak 1 malam | 3★ RM 50 · 4★ RM 120 per pax per malam | `ext.rates.nightShort` · `nightShort4` |
| Upgrade hotel | 3★→4★ RM 160 (5D4N) / RM 130 (4D3N) · 3★→5★ RM 350 | `ext.rates.up4` · `up5` |
| Single supplement | **RM 80 per malam per pax** | `variants[].singlePerNight` |
| Meal | tambah RM 30 · tolak RM 20 per pax per meal | `mealDelta` |

**Single supplement kini per malam**, bukan flat. 4 malam × RM 80 = RM 320 (5D4N) dan
3 × RM 80 = RM 240 (4D3N) — padan katalog, dan ia melaras sendiri bila TC tambah hari.

### ⚠ Perlu keputusan PO — upgrade 4★ untuk 4D3N

Rate Card Operasi letak upgrade 3★→4★ **RM 160/pax/malam untuk kedua-dua produk**.
Tetapi katalog **PT HCM 4D3N** cetak **RM 130/pax/malam**.

Config sekarang ikut **katalog** (5D4N RM 160, 4D3N RM 130) kerana katalog itu dokumen
yang customer nampak. Kalau PO nak seragamkan ikut rate card, tukar `up4` dalam
`variants[1].ext.rates` daripada `130` kepada `160`.

### ⚠ JEEP / ATV — harga berubah

Tab Simple Customisation lama tulis RM 197 untuk kedua-dua. Rate card baharu:
**JEEP RM 200 / jeep** (max 6 pax, FREE waktu MATTA Fair) dan **ATV RM 180 / ATV** (max 2 pax).
Kalkulator dan tab KB kedua-duanya sudah guna kadar baharu.
