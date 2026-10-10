# PT Aceh KB — Simple Calculator

> **Mulai 9 Okt 2026 kandungan KB dan `calc-config.json` datang dari PT R&D Costing Hub** (`prod-at22/rnd-hub`, `data/kb/aceh.json`). Fail di sini ditulis semula oleh mirror — **jangan edit di GitHub repo ini**; edit di hub. Skema di bawah masih terpakai.

Halaman live: **https://prod-at22.github.io/pt-kb-house/aceh/**

Repo ini ada dua fail yang penting:

| Fail | Apa dia | Boleh PO edit? |
|---|---|---|
| `calc-config.json` | **semua nombor dan itinerary kalkulator** — harga tier, kadar peak, upgrade hotel, kadar tambah/kurang hari, add-on, surcaj | **Ya** — edit terus di sini |
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
dan papar notis merah di atas tab Simple Calculator, contoh:

> **Notis:** gagal guna calc-config.json (JSON tidak sah — Unexpected token …).
> Kalkulator sedang guna config terbenam (versi terakhir yang dibina), jadi angka
> mungkin bukan yang terbaru.

Kalau notis itu keluar, maksudnya **suntingan tak terpakai** — betulkan JSON dan commit
semula. Semakan yang dibuat: JSON sah, ada `variants`, setiap varian ada `tiers` penuh
(`from`,`to`,`a`,`c`,`n`), dan bilangan hari dalam `itin` sama dengan `days`.

---

## Di mana benda yang biasa diubah

Dua varian: `aceh` = PT Aceh 4D3N · `sabang` = PT Aceh + Sabang 5D4N.

### Harga katalog (tier per pax)

`variants[].tiers` — `a` = adult, `c` = Child With Bed (6–10), `n` = Child No Bed (2–5).

```json
{"from": 6, "to": 10, "a": 1137, "c": 997, "n": 847}
```

> **Kanak-kanak dikira sebagai pax berbayar.** 2 adult + 1 child = *Group of 3*,
> jadi tier naik ke `3-5`. Ini memang betul ikut katalog ("Group of").

Tier `26-40` dan `41+` datang dari **Product Cheatsheet 2026 (Price Tier 4)**, bukan
katalog PDF. Cheatsheet hanya beri harga **adult** untuk tier itu — harga kanak-kanak
di sana adalah harga tier `11-25` yang disalin ke hadapan. Betulkan bila Ops bagi
angka sebenar.

**Aceh + Sabang tiada tier `41+`** — Cheatsheet tulis RM1,017, lebih rendah daripada
tier `26-40` (RM1,442), nampak salah taip. Kalkulator jatuh ke tier `26-40` dan papar
amaran. Isi tier `41+` di sini bila Ops sahkan angka betul.

### Kadar peak season

`peak` (peringkat atas, dipakai kedua-dua varian) — `mode: "perNight"`, RM50 setiap
malam yang jatuh dalam tetingkap.

```json
"peak": {"mode": "perNight", "value": 50,
         "windows": [["2026-12-20","2027-01-05", null, 50, "Peak Krismas & Tahun Baharu"]]}
```

Elemen: `[mula, tamat, variant_id atau null, kadar khas, label musim]`.
Nak tambah tetingkap baharu: tambah satu baris dalam `windows`.

### Upgrade hotel

`accOptions[]` — cari `up4` dan `up5`. Medan `perPax` = **RM per pax per malam**
(dikenakan pada setiap hari yang pilihan itu dipilih).

```json
{"v":"up4","t":"Upgrade 4 bintang · Grand Arabiya","cost":"incl","perPax":50, ...}
{"v":"up5","t":"Upgrade 5 bintang · Hermes Palace / Kyriad","cost":"incl","perPax":90, ...}
```

> **Percanggahan sumber yang masih terbuka.** Katalog PDF, rate card dan flyer MATTA
> semua meletakkan **Kyriad di 4 bintang (+RM50)**; KB dan R&D Sheet meletakkannya di
> 5 bintang (+RM90). Keputusan PO 3 Sep 2026: **kekal 5 bintang +RM90**. Kalau Ops
> tukar fikiran, alihkan "Kyriad" dari `up5` ke `up4`.

### Tambah / kurang hari

Rate card beri satu kadar rata **semua-dalam** (hotel + transport + aktiviti):

| Nak ubah | Di mana | Sekarang |
|---|---|---|
| Tambah 1 hari | `ext.night.normal` / `ext.night.peak` | +RM 90 /pax/hari |
| Kurang 1 hari | `ext.rates.nightShort._default[0].normal` | −RM 50 /pax/hari |

Sebab kadar itu sudah semua-dalam, **tiada** `ext.rates.day` dalam config ini —
transport hari tambahan sengaja tidak dicaj berasingan. Kalau Ops kemudian beri
kadar transport hari tambahan yang berasingan, barulah tambah kunci `day`.

### Upgrade Van (Hiace)

`trpOptions[]` → `van` → `perVehicle: 300` (RM/hari/transport, untuk group 5 pax
ke atas). `ext.paxPerVehicle: 15` bermakna 1 kenderaan sehingga 15 pax — itu had
band rate card (Medium Bus 10–15).

### Blok itinerary

`variants[].itin` = itinerary default pakej. `library` = blok tambahan yang muncul
dalam dropdown setiap hari (dikumpulkan ikut medan `g`).

- `t` / `act` — Bahasa Melayu, untuk dropdown dan baris hari dalam KB
- `en` / `eact` — Bahasa Inggeris, untuk PDF quotation (customer-facing)
- `acc` — `incl` (3★ Banda Aceh) · `sabang` (Freddies) · `up4` · `up5` · `none`
- `trp` — `air` · `priv` · `ferry` · `boat` · `van` · `none`
- `meal` — `nobf` `d1` `b` `bl` `bd` `bld` `ld` `none`

Kalau tukar destinasi dalam satu hari, edit `act` (BM) **dan** `eact` (Inggeris) sekali.

> Kalau nak tulis simbol `&` dalam `t`, `en`, `act`, `eact`, `inclusions`,
> `exclusions` — tulis `&` biasa sahaja, jangan `&amp;`.

### Add-on / optional activity

`addons[]` — `["Nama", hargaAdult, hargaChild]`. Elemen keempat `"share"` bermakna
kos itu **per transport / per group**, bukan per pax (contoh Ujung Kelindu RM277 max
4 pax). Nama masuk PDF quotation, jadi **tulis dalam Bahasa Inggeris**.

Nilai negatif = lajur "Tolak" rate card (contoh Dolphin dibuang dari pakej −RM100).

### Lain-lain

| Nak ubah | Di mana |
|---|---|
| Single supplement | `variants[].single` (RM250, kadar tersiar katalog 3★) |
| Harga infant | `variants[].infant` |
| Deposit per pax | `deposit` |
| Late booking surcharge | `lateBooking` |
| Surcaj travel date Sabang | `extraSurcharge[]` |
| Nota ikut saiz group (band kenderaan, amaran tier) | `paxNotes[]` |
| Inclusions / exclusions PDF | `variants[].inclusions`, `exclusions`, `exclusionsTail` |
| Teks bawah PDF quotation | `validity` |

`"{auto}"` dalam `inclusions` = tempat baris yang **dijana dari itinerary sebenar**
disisipkan (hotel, transport, upgrade — ikut hari yang betul-betul dipilih). Jangan
buang penanda itu, kalau tidak inclusions jadi basi bila TC ubah itinerary.

---

## Yang masih perlu dibina semula (bukan dalam JSON)

- Isi tab lain: FAQ, Harga & Pakej, Simple Customisation, Surcharge, Travel Map,
  Accommodation, dan lain-lain
- Logik enjin kalkulator (cara ia mengira)
- Susun atur / warna
- "Last updated" pada topbar

---

## PENTING — elak kerja PO ditimpa

Selepas PO mula edit `calc-config.json` di sini, **fail ini jadi sumber sebenar**.
Kalau halaman dibina semula dari config lama, suntingan PO akan hilang.

Jadi bila minta apa-apa perubahan pada enjin atau tab lain, sebut sekali:
**"config sudah diedit dalam GitHub, ambil versi terbaru dari repo dahulu."**

---

*Sumber nombor: katalog `PT ACEH (3 STAR) 4D3N 2026.pdf` dan
`PT ACEH SABANG 3 STAR (5D3N) 2026 v2.pdf` (kedua-dua last updated 8 Dis 2025, sah
untuk travel hingga 31 Jan 2027), `Product Cheatsheet 2026 - Aceh.pdf` (rate card),
dan `PT_ACHSBG_RD_reformatted.xlsx`.
Repo ini public — ia mengandungi harga dalaman dan analisis pesaing.*
