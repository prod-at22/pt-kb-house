# PT SEL Korea KB — Simple Calculator

> **Mulai 9 Okt 2026 kandungan KB dan `calc-config.json` datang dari PT R&D Costing Hub** (`prod-at22/pt-calculator-hub`, `data/kb/korea.json`). Fail di sini ditulis semula oleh mirror — **jangan edit di GitHub repo ini**; edit di hub. Skema di bawah masih terpakai.

Halaman live: **https://prod-at22.github.io/pt-kb-house/korea/**

Repo ini ada dua fail yang penting:

| Fail | Apa dia | Boleh PO edit? |
|---|---|---|
| `calc-config.json` | **semua nombor dan itinerary kalkulator** — harga tier, kadar peak, kadar transport, blok itinerary, add-on, surcaj | **Ya** — edit terus di sini |
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

### Harga katalog (tier per pax)

`variants[].tiers` — `a` = adult, `c` = CWB, `n` = CNB.

```json
{"from": 4, "to": 4, "a": 2697, "c": 2497, "n": 2297}
```

Varian: `sbasic` Seoul Basic · `sstd` Seoul Standard · `seljju` Seoul–Jeju ·
`jeju` Jeju · `jejuudo` Jeju–Udo.

### Kadar peak season

`variants[].peak` — `value` = kadar peak biasa (RM/malam/pax). Elemen **keempat**
dalam satu tetingkap = kadar khas tetingkap itu (dipakai untuk super peak).

```json
"peak": {"mode": "perNight", "value": 50,
         "windows": [["2026-04-01","2026-04-30"],
                     ["2026-12-16","2027-01-01", null, 90]]}
```

Nak tambah tetingkap baharu (contoh super peak Dis 2027): tambah satu baris
`["2027-12-16","2028-01-01", null, 90]`.

### Kadar transport ikut kawasan

`variants[].ext.rates.day` — kunci = tag kawasan, nilai = band pax.

```json
"[Nami]": [{"from":1,"to":8,"normal":1400,"peak":1400},
           {"from":9,"to":99,"normal":3094,"peak":3094}]
```

`_default` dipakai bila hari itu tiada tag kawasan. Kadar `0` bermakna "tiada harga
jual tersiar" — halaman akan papar cip merah `kadar?` pada hari itu. Isi nombornya
di sini bila operator dah bagi (contoh `[Paju]` untuk DMZ).

Kunci lain dalam `ext.rates`:

| Kunci | Maksud |
|---|---|
| `dayDed` | tolak dari katalog bila hari berpandu jadi free & easy |
| `airport` / `airportDed` | airport transfer tambahan / dibuang |
| `nightShort` | tolak per pax bila malam kurang dari pakej (−150) |
| `night4` | malam tambahan hotel 4 bintang (400) |
| `up4` | upgrade 4 bintang untuk malam pakej (100 Basic, 60 lain) |
| `ski` | menginap ski resort Vivaldi (500) |
| `bfDed` | tolak breakfast (−40) |

`ext.night` = malam tambahan hotel 3 bintang (250/pax).

### Blok itinerary

`library[]` — senarai blok yang muncul dalam dropdown Itinerary setiap hari.

```json
{"v": "sa1", "g": "Seoul - hari ketibaan", "region": "[Nami]",
 "t": "Airport pickup - Nami Island", "en": "NAMI ISLAND",
 "acc": "incl", "meal": "none", "trp": "incl",
 "act": ["Airport pickup", "Nami Island", "Check in hotel"],
 "eact": ["Airport pickup", "Nami Island", "Hotel check in"]}
```

| Medan | Maksud |
|---|---|
| `v` | kunci unik — **jangan sama** dengan blok lain |
| `g` | kumpulan dalam dropdown |
| `region` | tag kawasan → menentukan kadar transport hari itu |
| `t` / `act` | nama & senarai aktiviti **Bahasa Melayu** — `act` dipapar terus pada baris hari dalam kalkulator |
| `en` / `eact` | nama & senarai aktiviti **Bahasa Inggeris** (untuk PDF quotation) |
| `acc` / `meal` / `trp` | pilihan default bila blok ini dipilih |

`variants[].itin[]` = itinerary default pakej. Bentuknya sama, dan bilangannya
**mesti** sama dengan `days`.

Senarai `act` muncul sebagai pratonton di bawah nama hari, dan senarai penuh bila hari
itu dibuka. Jadi kalau nak tukar destinasi dalam satu hari, edit `act` (BM) **dan**
`eact` (Inggeris, untuk PDF) sekali.

> Kalau nak tulis simbol `&` dalam `t`, `en`, `act`, `eact`, `inclusions`,
> `exclusions` — tulis `&` biasa sahaja, jangan `&amp;`.

### Add-on / optional activity

`addons[]` — `["Nama", hargaAdult, hargaChild]`. Letak `0` untuk harga kanak-kanak
kalau tiada. Nama ini masuk PDF quotation, jadi **tulis dalam Bahasa Inggeris**.

### Lain-lain

| Nak ubah | Di mana |
|---|---|
| Single supplement | `variants[].single` |
| Harga infant | `variants[].infant` |
| Deposit per pax | `deposit` |
| Late booking surcharge | `lateBooking` |
| Surcaj travel date 2027 | `extraSurcharge[]` |
| Harga lunch / dinner | `meals` |
| Inclusions / exclusions PDF | `variants[].inclusions`, `exclusions`, `exclusionsTail` |
| Teks bawah PDF quotation | `validity` |
| Nota ikut saiz group | `paxNotes[]` |

---

## Yang masih perlu dibina semula (bukan dalam JSON)

- Isi tab lain: FAQ, Harga & Pakej, Surcharge, Travel Map, Accommodation, dan lain-lain
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

*Sumber nombor: katalog PT Seoul Basic / Standard / Seoul–Jeju / Jeju / Jeju–Udo 2026,
rate card `2026-2027 Date Surcharge.pdf`, dan `PT SEL ProdReq.md`.
Repo ini public — ia mengandungi harga dalaman.*
