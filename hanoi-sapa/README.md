# PT Hanoi – Sapa KB — Simple Calculator

> **Mulai 9 Okt 2026 kandungan KB dan `calc-config.json` datang dari PT R&D Costing Hub** (`prod-at22/rnd-hub`, `data/kb/hanoi-sapa.json`). Fail di sini ditulis semula oleh mirror — **jangan edit di GitHub repo ini**; edit di hub. Skema di bawah masih terpakai.

Halaman live: **https://prod-at22.github.io/pt-kb-house/hanoi-sapa/**

Repo ini ada dua fail yang penting:

| Fail | Apa dia | Boleh PO edit? |
|---|---|---|
| `calc-config.json` | **semua nombor dan itinerary kalkulator** — harga tier, kadar malam, upgrade hotel, tolakan, blok itinerary, add-on, surcaj | **Ya** — edit terus di sini |
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

Kalau JSON tersalah tulis (koma tertinggal, kurungan tak tutup), halaman **tidak**
rosak. Ia guna balik config lama yang terbenam dalam `index.html` dan papar notis
merah di atas tab Simple Calculator. Kalau notis itu keluar, maksudnya **suntingan
tak terpakai** — betulkan JSON dan commit semula.

---

## Di mana benda yang biasa diubah

### Harga katalog (tier per pax)

`variants[].tiers` — `a` = adult, `c` = CWB (6–8 thn), `n` = CNB (2–5 thn).

```json
{"from": 4, "to": 5, "a": 2877, "c": 2677, "n": 2477}
```

Varian: `v5d4n` Hanoi–Sapa–Halong Bay 5D4N · `v4d3n` Hanoi–Sapa 4D3N.

### Kadar accommodation (Rate Card Operasi KB)

Semua kadar malam duduk dalam **satu tempat sahaja**: `ext.rates` di peringkat atas
config (kedua-dua varian guna kadar yang sama). Semua per pax per malam:

| Apa | Kunci | Nilai sekarang |
|---|---|---|
| Tambah 1 malam 3★ | `ext.night.normal` / `.peak` | 100 |
| Tambah 1 malam 4★ | `rates.h4` | 240 |
| Tambah 1 malam 5★ | `rates.h5` | 320 |
| Tambah 1 malam Rock Garden Homestay | `rates.homestay` | 80 |
| Upgrade 3★ → 4★ | `rates.up4` | 140 |
| Tolak 1 malam 3★ | `rates.nightShort` | **−50** |
| Tolak 1 malam 4★ | `rates.nightShort4` | **−120** |

Kadar tolak mesti **negatif**. Lajur Peak rate card semuanya "-", jadi
`normal` dan `peak` sengaja sama — Hanoi–Sapa tiada kadar peak accommodation.

### Tolakan tukar itinerari

| Apa | Kunci | Nilai |
|---|---|---|
| Halong Bay day cruise ganti overnight cruise (5D4N) | `rates.cruiseDed` | **−100** |
| Sapa 2 malam, itinerari diselaraskan (4D3N) | `rates.sapa2n` | **−50** |

Kedua-duanya dikenakan **sekali per pax** pada hari yang TC pilih pilihan itu, dan
**tidak** mengubah jumlah malam trip.

### Meals

`mealDelta` — `add` 30, `drop` 20 (per pax per hidangan, tidak simetri).
Breakfast datang bersama bilik, jadi tiada kadar tambah/tolak breakfast.

### Kadar transport hari tambahan — SENGAJA KOSONG

`ext.rates.day` = `0`. Rate Card Operasi KB **tiada** seksyen transport hari tambahan,
jadi kalkulator papar cip merah **`kadar?`** pada hari tambahan dan **tidak** mengecaj
apa-apa untuk transport. Itu betul — ia menandakan gap, bukan RM 0.

**Bila operator dah bagi kadar**, isi di sini (per kenderaan per hari, 25 pax/kenderaan):

```json
"day": {"_default": [{"from": 1, "to": 99, "normal": 0, "peak": 0}]}
```

### Surcaj tarikh perjalanan

`extraSurcharge` — sekarang +RM 100/pax untuk berlepas 1 Jan – 30 Jun 2027.

### Last minute & late booking

`variants[].lastMinute` — `rate2` (2 pax) / `rate3` (3+ pax), booking < 21 hari.
5D4N = 400/300, 4D3N = 300/200 (ikut katalog masing-masing).
`lateBooking` — RM 50 satu booking bila < 45 hari.

### Blok itinerary

`library[]` — setiap blok ada `t`/`act` (Melayu, untuk KB) dan `en`/`eact`
(Inggeris, untuk PDF quotation). `g` = kumpulan dalam dropdown.

Kumpulan yang ada: blok 5D4N, blok 4D3N, **Sapa 2 malam (4D3N)**,
**Halong Bay tanpa bermalam**, dan Umum (hari tambahan / free & easy).

---

## Perkara yang perlu diingat

- **Single supplement = 0.** Katalog dan rate card kedua-duanya tulis *quoted upon
  request*. Kalkulator tidak caj apa-apa untuk bilik single — ops kena tanya operator.
- **Blackout 17–18 Feb 2027** (Chinese New Year) — tiada operasi.
- Pilih **Halong Bay day cruise** untuk hari 3 bermakna hari 4 pakej
  ("Luon Cave by kayak / check out cruise") jadi mustahil — TC **wajib** tukar hari 4
  juga (contoh guna blok Hanoi city tour atau Free and easy).
- Kadar 5★ dan Rock Garden Homestay **tiada dalam katalog** — ia datang dari Rate Card
  Operasi KB sahaja. Tiada kadar *tolak* untuk 5★, jadi pilihan itu memang tidak wujud.
