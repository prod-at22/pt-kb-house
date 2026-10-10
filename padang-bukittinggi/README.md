# PT Padang–Bukittinggi KB — Simple Calculator

> **Mulai 9 Okt 2026 kandungan KB dan `calc-config.json` datang dari PT R&D Costing Hub** (`prod-at22/pt-rnd-hub`, `data/kb/padang-bukittinggi.json`). Fail di sini ditulis semula oleh mirror — **jangan edit di GitHub repo ini**; edit di hub. Skema di bawah masih terpakai.

Halaman live: **https://prod-at22.github.io/pt-kb-house/padang-bukittinggi/**

> Repo public. KB ini mengandungi data rujukan dalaman (harga, nota rate card, kod promo).
> Diterbitkan atas permintaan PO.

Repo ini ada dua fail penting:

| Fail | Apa dia | Boleh PO edit? |
|---|---|---|
| `calc-config.json` | **semua nombor dan itinerary kalkulator** — harga tier, kadar peak, naik taraf hotel, blok itinerary, add-on, surcaj | **Ya** — edit terus di sini |
| `index.html` | halaman KB penuh + enjin kalkulator | Tidak — perlu bina semula |

Halaman membaca `calc-config.json` **setiap kali dibuka**. Ubah nombor, commit,
refresh halaman — terus naik. Tak perlu bina semula `index.html`.

---

## Cara edit

1. Klik `calc-config.json` di atas.
2. Klik ikon pensel (**Edit this file**).
3. Ubah nombor yang perlu.
4. Scroll bawah → **Commit changes**.
5. Tunggu ~30 saat, refresh halaman KB.

### Jaring keselamatan

Kalau JSON tersalah tulis (koma tertinggal, kurungan tak tutup), halaman **tidak** rosak.
Ia guna balik config lama yang terbenam dalam `index.html` dan papar notis merah di atas
tab Simple Calculator:

> **Notis:** gagal guna calc-config.json (JSON tidak sah — …). Kalkulator sedang guna
> config terbenam, jadi angka mungkin bukan yang terbaru.

Kalau notis itu keluar, maksudnya **suntingan tak terpakai** — betulkan JSON dan commit semula.

---

## Di mana benda yang biasa diubah

### Harga katalog (tier per pax)

`variants[].tiers` — `a` = adult, `c` = Child With Bed, `n` = Child No Bed.
Dua varian: `optA` (Option A) dan `optB` (Option B) — **harga sama**, jadi kalau harga
naik, ubah kedua-duanya.

```json
{"from": 3, "to": 6, "a": 1157, "c": 1057, "n": 957}
```

### Tetingkap peak season

`peak.windows` — kadar `value` = **RM 50/pax/malam** (hotel 3★, katalog v7).

```json
"peak": {"mode": "perNight", "value": 50,
         "windows": [["2025-12-25","2026-01-05"],
                     ["2026-03-15","2026-03-31"],
                     ["2026-06-25","2026-07-12"],
                     ["2026-12-25","2027-01-05"]]}
```

Nak tambah tetingkap baharu: tambah satu baris `["2027-03-15","2027-03-31"]`.

### Peak untuk hotel 4★ (RM 60/pax/malam)

Katalog beri dua kadar peak: 3★ RM 50 dan 4★ RM 60 sepax semalam. Kalkulator kira
RM 50 asas untuk **semua** malam peak, kemudian TC pilih pada baris hari itu:

| Pilihan pada baris hari (Accommodation) | Kesan |
|---|---|
| `Naik taraf Hotel 4 bintang` | +RM 80/pax malam itu |
| `Naik taraf Hotel 4 bintang – malam peak season` | +RM 90/pax malam itu (RM 80 upgrade + RM 10 beza peak) |

Jadi malam peak dengan hotel 4★ = RM 50 + RM 90 = **RM 140/pax** = RM 80 + RM 60. ✔

Kalau kadar berubah, ubah `perPax` pada `accOptions` `up4` (80) dan `up4pk` (90).

### Single supplement / late booking / deposit

```json
"variants[].single": 300        // RM 300/pax, hotel 3★ sahaja
"lateBooking": {"lt": 45, "amount": 50}
"deposit": 250                  // RM 250/pax
```

### Optional tour (add-on)

`addons` — `["Nama", harga dewasa, harga kanak, "pax" | "unit"]`.
`"pax"` = kuantiti auto ikut bilangan pax; `"unit"` = satu unit sekali (contoh airport
transfer tambahan, dikira per hala).

### Itinerary

`variants[].itin` — `t`/`act` Bahasa Melayu (papar dalam KB), `en`/`eact` Bahasa Inggeris
(masuk PDF quotation). `library` = blok tambahan yang muncul dalam dropdown Itinerary
tetapi bukan sebahagian itinerari default — di sinilah blok Option A / Option B disimpan
supaya TC boleh mix-and-match.

---

## Yang **belum** diisi — sengaja

Katalog dan rate card tidak menerbitkan harga jual untuk **hari tambahan** dan
**malam tambahan** Padang–Bukittinggi. Jadi:

```json
"ext": {"night": {"normal": null, "peak": null},
        "rates": {"day": {"_default": [{"from":2,"to":20,"normal":null,"peak":null}]},
                  "h4":  {"_default": [{"from":2,"to":20,"normal":null,"peak":null}]},
                  "nightShort": {"_default": [{"from":2,"to":20,"normal":null,"peak":null}]}}}
```

Bila TC tambah hari, kalkulator papar cip merah **kadar?** dan baris amaran — bukan RM 0.
Itu memang niatnya: lebih baik nampak gap daripada quote percuma.

**Bila PO dapat kadar sebenar**, ganti `null` dengan nombor:

- `ext.night` — malam tambahan hotel 3★, RM per pax per malam
- `rates.h4` — malam tambahan hotel 4★, RM per pax per malam
- `rates.day` — hari tambahan (transport + driving guide), RM **per kenderaan** per hari
- `rates.nightShort` — tolakan bila malam kurang daripada 3 (tulis nombor **negatif**)

---

## Perkara yang masih perlu keputusan PO

1. **Surcaj peak 2027 +RM 150/pax** — ada dalam tab Surcharge KB (sumber: 2026/2027 Date
   Surcharge ARBA) tetapi **tiada** dalam katalog v7 dan tiada dalam tab Surcharges R&D
   sheet. **Belum dimasukkan** dalam kalkulator. Kalau betul, tambah:
   `"extraSurcharge": [{"label":"Peak season surcharge 2027","dateIn":["2026-12-25","2027-01-05"],"perPax":150}]`
2. **Baju Adat Minangkabau** — R&D sheet senaraikan ia sebagai *inclusion* di Istana
   Pagaruyung, sebagai *free gift* promo (kod FPDGB2), dan juga sebagai *add-on RM 50/pax*.
   Kalkulator ambil pendirian **add-on RM 50/pax** dan **tidak** menyebutnya dalam itinerary
   customer-facing. Sahkan mana yang betul.
3. **Holbung Tour (RM 150)** dan **Aek Manik Pool Sidamanik (RM 100)** dalam tab Add-Ons R&D
   **tidak dimasukkan** — kedua-duanya attraction kawasan Danau Toba, bukan Sumatera Barat.
   Nampak seperti tersalin dari R&D Medan–Lake Toba. Sahkan sebelum jual.
4. **Maksimum pax** — katalog beri tier sehingga 20 pax, operator (Pak Herman) quote
   maksimum 19 pax dan senarai kenderaan berhenti di Hiace 12 pax. Kalkulator papar nota
   amaran untuk 13+ dan 20 pax.
