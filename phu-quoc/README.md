# PT Phu Quoc KB — Simple Calculator

Halaman live: **https://prod-at22.github.io/pt-kb-house/phu-quoc/**

Repo ini ada dua fail yang penting:

| Fail | Apa dia | Boleh PO edit? |
|---|---|---|
| `calc-config.json` | **semua nombor dan itinerary kalkulator** — harga tier, kadar accommodation, meal, aktiviti, blok itinerary, add-on, surcaj | **Ya** — edit terus di sini |
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
semula.

---

## Di mana benda yang biasa diubah

### Harga katalog (tier per pax)

`variants[].tiers` — `a` = adult, `c` = CWB (6–8), `n` = CNB (2–5).

```json
{"from": 4, "to": 4, "a": 2437, "c": 2237, "n": 2037}
```

Varian: `v4d3n` PT Phu Quoc 4D3N · `v5d4n` PT Phu Quoc 5D4N. Kedua-duanya 3 bintang
fullboard, ground + tipping.

### Kadar Simple Customisation (accommodation / meal / aktiviti)

Semua datang dari **Rate Card Simple Customisation Phu Quoc**.

| Baris rate card | Di mana dalam JSON | Nilai sekarang |
|---|---|---|
| Upgrade 3★ → 4★ | `ext.rates.up4` | 140 |
| 3★ — tambah 1 malam | `ext.night` | 100 |
| 4★ — tambah 1 malam | `ext.rates.h4` | 240 |
| 5★ — tambah 1 malam | `ext.rates.h5` | 320 |
| 3★ — tolak 1 malam | `ext.rates.nightShort` | −50 |
| 4★ — tolak 1 malam | `ext.rates.nightShort4` | −120 |
| Meal — tambah / tolak 1 hidangan | `mealDelta` | `{"add": 30, "drop": 20}` |
| Add on / Exclude aktiviti | `addons[]` | lihat bawah |
| Hotel kawasan Grand World | `addons[]` | +50/pax |

Semua kadar accommodation ditulis dua kali, `normal` dan `peak`, dan nilainya **sama** —
lajur Peak rate card kosong sebab Phu Quoc tiada peak season. Kalau satu hari nanti ada
peak, ubah nilai `peak` sahaja.

```json
"h4": {"_default": [{"from": 1, "to": 99, "normal": 240, "peak": 240}]}
```

> **`ext.rates.day` sengaja 0.** Itu kadar transport untuk **hari tambahan**, dan rate
> card tiada baris itu. Jadi bila TC tambah hari, baris hari itu bertanda cip merah
> `kadar?` — itu **amaran, bukan RM 0**. Isi nombornya di sini bila operator dah bagi.

### Add-on dan tolakan aktiviti

`addons[]` — `["Nama", hargaAdult, hargaChild, basis, frasaEn]`.

```json
["Water Taxi at Grand World - per pax per ride", 50, 50, "pax"]
["Honeymoon bedroom decoration - per couple", 250, 0, "unit"]
["Less Hon Thom Cable Car + Aquatopia entrance - per pax", -110, -110, "pax",
 "Hon Thom Cable Car and Aquatopia"]
```

- `basis` — `"pax"` ikut bilangan pax · `"unit"` sekali sahaja (per pasangan / per bot).
- Nama masuk PDF quotation, jadi **tulis dalam Bahasa Inggeris**.
- **Amaun negatif = tolakan** (lajur *Exclude* rate card). Untuk yang negatif, elemen
  ke-5 ialah nama tiket dalam Bahasa Inggeris. Enjin guna nama itu untuk membuang baris
  `Entrance fee: …` daripada inclusions PDF dan menyebutnya dalam exclusions — jadi PDF
  tidak terus menjanjikan tiket yang customer tidak bayar. **Kalau tambah tolakan baharu,
  jangan lupa elemen ke-5**, dan pastikan ia sama dengan baris `Entrance fee:` dalam
  `variants[].inclusions`.

### Blok itinerary

`library[]` — blok yang muncul dalam dropdown Itinerary setiap hari.

| Medan | Maksud |
|---|---|
| `v` | kunci unik — **jangan sama** dengan blok lain |
| `g` | kumpulan dalam dropdown (`Blok 4D3N`, `Blok 5D4N`, `Umum`) |
| `region` | tag kawasan → kunci kadar dalam `ext.rates` |
| `t` / `act` | nama & aktiviti **Bahasa Melayu** — dipapar pada baris hari |
| `en` / `eact` | nama & aktiviti **Bahasa Inggeris** — untuk PDF quotation |
| `acc` / `meal` / `trp` | pilihan default bila blok ini dipilih |

`variants[].itin[]` = itinerary default pakej; bilangannya **mesti** sama dengan `days`.

> Kalau nak tulis simbol `&` dalam `t`, `en`, `act`, `eact`, `inclusions`,
> `exclusions` — tulis `&` biasa sahaja, jangan `&amp;`.

### Kod meal — breakfast dikendali khas

Rate card tulis lajur *Tolak 1 Meal* untuk breakfast sebagai `-`: breakfast datang
bersama bilik, jadi ia **tidak boleh dijual atau dikreditkan** satu-satu.

Sebab itu `mealOptions` **tidak** ada kod breakfast. Breakfast ditambah sendiri oleh
enjin kerana `variants[].breakfast` = `true`, dan kadar tambah/tolak RM30/RM20 hanya
berkenaan untuk lunch dan dinner.

| Kod | Maksud |
|---|---|
| `arr` / `arrl` / `nobf` | hari **ketibaan** — tiada breakfast (`bfLock`) |
| `ld` / `l` / `d` / `none` | hari lain — breakfast ditambah sendiri |

Jangan tulis "Breakfast" dalam `lbl` mana-mana kod, dan jangan set `b: 1` —
enjin yang uruskan.

### Lain-lain

| Nak ubah | Di mana |
|---|---|
| Single supplement | `variants[].single` (240 / 320) |
| Deposit per pax | `deposit` (250) |
| Late booking surcharge | `lateBooking` (<45 hari, RM50/booking) |
| Last minute surcharge | `variants[].lastMinute` (<21 hari) |
| Surcaj travel date 2027 | `extraSurcharge[]` |
| Inclusions / exclusions PDF | `variants[].inclusions`, `exclusions`, `exclusionsTail` |
| Teks bawah PDF quotation | `validity` |
| Nota ikut saiz group | `paxNotes[]` |
| Teks pengenalan atas kalkulator | `intro` |

---

## Yang masih perlu disahkan PO

1. **Upgrade 3★ → 5★ tiada kadar.** Rate card hanya bagi *malam tambahan* 5★ (RM320).
   R&D sheet tulis upgrade 3★→5★ RM350/pax/malam, tetapi 350 itu kadar malam 5★ Danang —
   nampak macam salin silang. Jadi kalkulator **tiada pilihan upgrade 5★** buat masa ini.
2. **Surcaj travel date 2027 berbeza antara sumber.** Kalkulator guna **+RM120/pax,
   Jan–Feb 2027** (dari R&D Surcharges). Tab Surcharge KB masih tulis **+RM100/pax,
   1 Jan – 30 Jun 2027**. Katalog v3 tiada kedua-duanya. Kalau RM100 yang betul, ubah
   `extraSurcharge[]` di sini **dan** tab Surcharge dalam KB.
3. **Kadar transport hari tambahan** — tiada dalam rate card, kekal 0 (cip `kadar?`).

---

## PENTING — elak kerja PO ditimpa

Selepas PO mula edit `calc-config.json` di sini, **fail ini jadi sumber sebenar**.
Kalau halaman dibina semula dari config lama, suntingan PO akan hilang.

Jadi bila minta apa-apa perubahan pada enjin atau tab lain, sebut sekali:
**"config sudah diedit dalam GitHub, ambil versi terbaru dari repo dahulu."**

---

*Sumber nombor: katalog PT PHU QUOC 4D3N & 5D4N 2026 v3 (11 Mac 2026),
Rate Card Simple Customisation Phu Quoc, dan `PT_PQC_RD_reformatted.xlsx`
(tab Surcharges, Add-Ons). Repo ini public — ia mengandungi harga dalaman.*
