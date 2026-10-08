# PT Switzerland KB — Simple Calculator

Halaman live: **https://prod-at22.github.io/pt-kb-house/switzerland/**

Repo ini ada dua fail yang penting:

| Fail | Apa dia | Boleh PO edit? |
|---|---|---|
| `calc-config.json` | **semua nombor dan itinerary kalkulator** — harga tier, kadar peak, kadar extension, blok itinerary, add-on, surcaj | **Ya** — edit terus di sini |
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

`variants[0].tiers` — `a` = adult, `c` = Child With Bed, `n` = Child No Bed.

```json
{"from": 6, "to": 7, "a": 7997, "c": 7797, "n": 7597}
```

Hanya ada **satu varian**: `std` = PT Switzerland Standard 7D6N.

> Nota: tier 8 pax (RM 9,997) memang **lebih tinggi** daripada 6–7 pax (RM 7,997)
> kerana perlu 2 kenderaan, dan turun semula pada 9–10 pax. Itu betul ikut katalog —
> jangan "betulkan".

### Kadar peak season

`peak` — `mode: "perNight"` bermakna RM × bilangan malam yang jatuh dalam tetingkap.

```json
"peak": {"mode": "perNight", "value": 200,
         "windows": [["2026-07-15","2026-08-15"],
                     ["2026-12-20","2027-01-03"]]}
```

Nak tambah tetingkap 2028: tambah satu baris `["2028-02-01","2028-02-29"]`.

### Kadar extension / custom itinerary

`ext` — inilah kadar untuk hari yang TC tambah sendiri.

```json
"ext": {
  "night": {"normal": 500, "peak": 650},
  "marginPerPax": 1300,
  "paxPerVehicle": 7,
  "rates": {
    "day": {"_default": [{"from": 1, "to": 14, "normal": 3400, "peak": 3700}]},
    "dayDed":     {"_default": [{"from": 1, "to": 14, "normal": 0, "peak": 0}]},
    "nightShort": {"_default": [{"from": 1, "to": 14, "normal": 0, "peak": 0}]}
  }
}
```

| Medan | Maksud |
|---|---|
| `night` | accommodation, **per pax per malam** |
| `rates.day._default` | transport, **per kenderaan per hari** |
| `paxPerVehicle: 7` | maks 7 pax satu kenderaan — 8 pax jadi 2 kenderaan sendiri |
| `marginPerPax` | margin RM 1,300/pax, dikenakan **sekali** bila ada hari/malam tambahan |

**Switzerland tiada kadar transport ikut kawasan** (tiada ProdReq), jadi hanya ada
satu kunci `_default` yang dipakai untuk seluruh negara. Kalau nanti ada rate card
ikut kawasan, tambah kunci baharu di sebelah `_default`, contoh `"[Zermatt]": [...]`.

### Kadar yang sengaja dibiar `0`

`dayDed` (tolak driving guide bila TC jadikan satu hari Free & Easy) dan `nightShort`
(tolak malam bila TC buang satu malam katalog) **belum ada harga jual tersiar**.
Sebab itu ia `0`, dan halaman akan papar cip merah `kadar?` pada hari berkenaan
serta satu baris amaran dalam ringkasan — supaya TC nampak, bukan diam-diam RM 0.

**Isi nombornya di sini bila operator dah bagi.** Tolakan ditulis sebagai nombor
**negatif**, contoh `{"from": 1, "to": 14, "normal": -1200, "peak": -1200}`.

### Optional tour / add-on

`addons` — `["Nama", hargaDewasa, hargaKanak, "pax"]`.

```json
["Jungfraujoch - Top of Europe", 1577, 797, "pax"]
```

Elemen keempat `"pax"` bermakna bilangan diisi sendiri ikut bilangan pax berbayar.
Harga kanak `0` bermakna tiada harga kanak (contoh Skydiving).

### Blok itinerary (pustaka)

`library` — blok yang TC boleh pilih untuk mana-mana hari, dikumpul ikut `g`
(Zurich · Lucerne · Interlaken · Zermatt · panoramic train · hari tambahan).

```json
{"v":"lb_rigi","g":"Central Switzerland - Lucerne",
 "t":"Mount Rigi (optional)","en":"MOUNT RIGI",
 "acc":"incl","meal":"b","trp":"incl",
 "act":["... Bahasa Melayu, untuk KB ..."],
 "eact":["... English, untuk PDF quotation ..."]}
```

`t`/`act` = Melayu (papar dalam KB). `en`/`eact` = English (masuk PDF quotation
yang customer nampak). Kunci `v` mesti unik.

### Surcaj tarikh

```json
"extraSurcharge": [{"label": "Travel surcharge 2027",
                    "dateIn": ["2027-01-01","2027-06-30"], "perPax": 370}]
"lateBooking": {"lt": 45, "amount": 50}
```

Last minute ada dalam `variants[0].lastMinute`
(`{"lt": 21, "rate2": 700, "rate3": 500}` — `rate2` untuk 2 pax, `rate3` untuk 3+).

---

## Sumber nombor

- `Catalog/PT SWITZERLAND STANDARD 7D6N 2026.pdf` (last updated 8 Dis 2025, sah hingga 31 Dis 2026)
  — tier, infant, peak, last minute, surcaj 2027, inclusions/exclusions.
- Tab **Simple Customisation** dalam KB — optional tour dan kadar extension.

Dua perkara yang **katalog tidak beri**, jadi diambil dari rate card ARBA:

| Item | Nilai dipakai | Nota |
|---|---|---|
| Single supplement | RM 2,800/pax | Katalog tulis *"quoted upon request"* sahaja |
| Lunch / Dinner | RM 0 | Tiada harga jual tersiar — pilihan meal tidak menambah kos |

Repo ini **public** dan KB mengandungi harga dalaman serta perbandingan pesaing.
