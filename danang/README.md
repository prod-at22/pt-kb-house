# PT Danang – Hoi An KB — Simple Calculator

> **Mulai 9 Okt 2026 kandungan KB dan `calc-config.json` datang dari PT R&D Costing Hub** (`prod-at22/pt-rnd-hub`, `data/kb/danang.json`). Fail di sini ditulis semula oleh mirror — **jangan edit di GitHub repo ini**; edit di hub. Skema di bawah masih terpakai.

Halaman live: **https://prod-at22.github.io/pt-kb-house/danang/**

Repo ini ada dua fail yang penting:

| Fail | Apa dia | Boleh PO edit? |
|---|---|---|
| `calc-config.json` | **semua nombor dan itinerary kalkulator** — harga tier, single supplement, last minute, surcaj tarikh, upgrade hotel, malam tambahan, blok itinerary, add-on | **Ya** — edit terus di sini |
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

---

## Rate Card Operasi KB (PO, 3 Sep 2026) — semua kadar customisation

Kalkulator berlabuh pada rate card ini. Lajur **Peak** rate card semuanya `-` untuk
accommodation, jadi **kadar peak sama dengan normal** — tiada surcaj musim atas malam.

| Perkara | Kadar | Medan config |
|---|---|---|
| Hari tambahan | **RM 50 per pax per hari** | pilihan `ext` dalam `trpOptions` → `perPax` |
| Malam tambahan | 3★ RM 100 · 4★ RM 240 · 5★ RM 350 **per pax per malam** | `ext.night` · `ext.rates.h4` · `h5` |
| Tolak 1 malam | 3★ RM 50 · 4★ RM 120 per pax per malam | `ext.rates.nightShort` · `nightShort4` |
| Upgrade hotel | 3★→4★ RM 140 · 3★→5★ RM 320 per pax per malam | `ext.rates.up4` · `up5` |
| Meal | tambah RM 30 · tolak RM 20 per pax per meal | `mealDelta` |
| Hoi An Memories Show | RM 110 per pax (seat High Class) | `addons` |
| Alpine Coaster (Bana Hills) | RM 50 per pax | `addons` |

**Hari tambahan tiada kos transport berasingan** — PO sahkan Danang dan Hoi An dalam
kawasan yang sama, jadi tiada caj transfer jarak jauh. Sebab itu RM 50 itu duduk
sebagai `perPax` pada pilihan transport `ext`, **bukan** `ext.rates.day` (medan itu
dicaj *per kenderaan*, bukan per pax — jangan pindahkan ke sana).

Malam hotel dikira **berasingan** daripada RM 50 itu. Jadi satu hari tambahan penuh
dengan malam 3★ = RM 50 + RM 100 = **RM 150/pax**.

### Hotel

| Kelas | Danang | Hoi An |
|---|---|---|
| 3★ (dalam pakej) | LA Beach Hotel · Golden Rose Hotel | — |
| 4★ | RHM Hotel · Santa Luxury Hotel | — |
| 5★ | Nalod Hotel | Grand Sunrise Hotel |

---

## Di mana benda yang biasa diubah

### Harga katalog (tier per pax)

`variants[].tiers` — `a` = adult, `c` = Child With Bed, `n` = Child No Bed.

```json
{"from": 8, "to": 12, "a": 1677, "c": 1477, "n": 1277}
```

Varian dalam repo ini: `v4d3n` Danang–Hoi An 4D3N · `v5d4n` Danang–Hoi An 5D4N.

### Single supplement

`variants[].single` — RM per pax, **flat satu trip**: 4D3N RM 240 · 5D4N RM 320.

### Last minute surcharge

`variants[].lastMinute` — `lt` = hari sebelum berlepas, `rate2` = kadar 2 pax,
`rate3` = kadar 3 pax ke atas (RM per pax).

### Late booking

`lateBooking` — `{"lt": 45, "amount": 50}` = RM 50 **satu booking** (bukan per pax).

### Surcaj tarikh 2027

`extraSurcharge` — dikenakan bila **tarikh berlepas** jatuh dalam julat `dateIn`.
Sekarang: Jan–Feb 2027 **+RM 150/pax**.

### Kadar extension

`ext.night` dan `ext.rates` ada **dua salinan**: satu di peringkat atas dan satu dalam
**setiap** `variants[].ext`. **Ubah semua** kalau kadar berubah.

### Add-on / optional tour

`addons` — senarai `["Nama", hargaDewasa, hargaKanak]`.

### Itinerary

`variants[].itin` — satu objek per hari. `t` / `act` Bahasa Melayu (papar dalam KB),
`en` / `eact` Bahasa Inggeris (papar dalam PDF quotation customer).

---

## ⚠ Perlu keputusan PO

### 1. Single supplement — flat atau per malam?

Sekarang config guna **flat per trip**: 4D3N RM 240, 5D4N RM 320 (ikut R&D Sheet →
tab Surcharges; katalog sendiri hanya tulis *quoted upon request*).

Tapi perhatikan: **240 ÷ 3 malam = RM 80** dan **320 ÷ 4 malam = RM 80**. Kedua-dua
varian jatuh tepat pada RM 80 semalam — sama macam HCM–Dalat–Mui Ne, yang rate cardnya
memang tulis *single supplement RM 80 per malam*.

Kesannya: **sekarang, bila TC tambah satu hari, single supplement TIDAK naik.**
Kalau sepatutnya naik RM 80, tukar dalam setiap varian:

```json
"single": 240              →  buang baris ini
"singlePerNight": 80       →  ganti dengan baris ini
```

Enjin akan darab sendiri dengan bilangan malam yang dibina.

### 2. Rate card terpotong

Screenshot rate card yang diberi berakhir pada baris **Alpine Coaster**. Kalau ada
baris di bawah itu (contoh single supplement, transport, add-on lain), ia **belum
masuk** dalam kalkulator. Hantar baki rate card untuk dilengkapkan.

### 3. Breakfast

Rate card tulis breakfast *"Suggested makan di hotel saja"* tanpa harga dan tanpa kadar
tolak. R&D Sheet pula letak RM 30/pax. **PO pilih ikut R&D** — jadi breakfast boleh
ditambah RM 30/pax, tetapi **tiada kadar tolak** untuk breakfast (lunch dan dinner ada:
−RM 20).

### 4. Tolak malam 5★

Rate card tiada kadar tolak untuk 5★ (lajur tulis `-`), jadi pilihan itu **sengaja tidak
dibuat**. Kalau customer nak buang malam 5★, minta quote dari consultant.

---

## Nota sumber

- Tier, last minute dan surcaj travel date 2027 dari katalog **PT DANANG HOI AN 4D3N /
  5D4N 2026 v3** (6 Ogos 2026). Sah untuk travel hingga 31 Dis 2026.
- Single supplement dari **R&D Sheet → tab Surcharges** (katalog tulis *quoted upon request*).
- Semua kadar customisation dari **Rate Card Operasi KB** (3 Sep 2026).
- Upgrade 5★ RM 320 disahkan oleh **dua** sumber bebas: rate card dan R&D Surcharges.
- **Guide:** Local Driving Guide (English Speaking) — penduduk tempatan Vietnam,
  **bukan Muslim** dan tidak bertutur Melayu. Makanan halal tetap dijamin kerana
  restoran ditempah oleh operator. Jangan janji guide Muslim/Melayu.
- **Blockout:** CNY 2026 16–22 Feb 2026 · CNY 2027 17–18 Feb 2027.
