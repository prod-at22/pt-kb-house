# ARBA Jogjakarta — KB (TC Reference) + Simple Calculator

> **Mulai 9 Okt 2026 kandungan KB dan `calc-config.json` datang dari PT R&D Costing Hub** (`prod-at22/pt-rnd-hub`, `data/kb/jogja.json`). Fail di sini ditulis semula oleh mirror — **jangan edit di GitHub repo ini**; edit di hub. Skema di bawah masih terpakai.

Halaman live: **https://prod-at22.github.io/pt-kb-house/jogja/**

Knowledge Base dalaman Travel Consultant untuk **Private Tour Jogjakarta 4D3N**,
kini dengan tab **Simple Calculator** yang mengira quotation dan menjana PDF rasmi ARBA.

Repo ini ada dua fail yang penting:

| Fail | Apa dia | Boleh PO edit? |
|---|---|---|
| `calc-config.json` | **semua nombor dan itinerary kalkulator** — harga tier, kadar peak, kadar transport ikut tempoh tour, blok itinerary, add-on, surcaj | **Ya** — edit terus di sini |
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

## Sumber nombor

| Bahagian | Sumber |
|---|---|
| Tier harga, single supplement, peak season, late booking, deposit, upgrade hotel 4 bintang, itinerari 4 hari, inclusions/exclusions | Katalog **PT JOGJA 4D3N 2026 v3** (Last Updated 27 April 2026) |
| Kadar transport ikut tempoh tour & kelas kenderaan (tambah / tolak), malam tambah / tolak ikut hotel, hidangan tambah RM 30 / tolak RM 20, entrance & activity tambah / tolak | **Rate Card Operasi PT Jogjakarta**, PO 3 September 2026 |
| Harga add-on kanak-kanak 60% daripada adult | Product FAQ Notion |

Rate card penuh dipapar dalam tab **Simple Customisation** halaman KB.

---

## Keputusan PO — 3 September 2026

Rate card baharu bercanggah dengan katalog V3 pada beberapa tempat. Keputusan PO:

| Item | Katalog V3 | Rate card | Dipakai |
|---|---|---|---|
| Borobudur entrance | RM 130/pax | RM 150 Ground / RM 185 Temple guided | **rate card** (dua pilihan) |
| Gondola Timang Beach | RM 60/pax | RM 80/pax | **rate card** |
| Goa Pindul & Cave Tubing | RM 75/pax | RM 100/pax | **rate card** |
| Gamplong Studio Alam | RM 10/pax | RM 25/pax | **rate card** |
| Lajur tolak Gondola RM 50 & Jambatan RM 30 | — | tertulis `/Jeep` | **per pax** (salah taip; lajur tambah per pax) |
| Tolak 1 malam 3 bintang RM 80 | — | tiada unit | **per pax per malam** |
| 13–15 pax | ada tier harga (11–15 pax) | transport berhenti di Hiace 7–12 pax | **ditanda gap** — kalkulator papar cip merah `kadar?`, minta sebut harga operasi |

Harga add-on dalam KB (tab Customisation, card attraction, FAQ) sudah diselaraskan
dengan keputusan ini. **Katalog V3 masih tertulis harga lama — perlu dikemas kini
supaya selari.**

---

## Perkara yang masih perlu disahkan operasi

- **Kadar transport 13 pax ke atas.** Rate card berhenti di Hiace 7–12 pax. KB tab
  Transport sebut 14 pax ke atas guna Bus, tetapi kadar Bus tiada dalam mana-mana sumber.
- **Kadar transport ke luar bandar Jogja** — Dieng, Kebumen, Nepal van Java (Magelang).
  Rate card beri kadar hotel di sana tetapi bukan kadar transport. Blok itinerari untuk
  destinasi itu sengaja ditanda gap.
- **Tolak malam untuk hotel 4 bintang** dan hotel luar bandar — rate card tulis `-`.
  Hanya 3 bintang ada kadar tolak (RM 80/pax/malam).
- **"Hotel Glamping In Nepal"** dalam rate card dibaca sebagai **Nepal van Java**
  (kampung Butuh, Magelang). Sahkan kalau maksudnya lain.

---

## Di mana benda yang biasa diubah

### Harga katalog (tier per pax)

`variants[0].tiers` — `a` = adult, `c` = Child With Bed, `n` = Child No Bed.

```json
{"from": 5, "to": 7, "a": 1297, "c": 1097, "n": 897}
```

Hanya satu varian: `s3` = PT Jogjakarta 4D3N (asas hotel 3 bintang).

### Kadar peak season

`variants[0].peak` — RM 120 per pax per malam peak (kadar hotel 3 bintang).

```json
"peak": {"mode": "perNight", "value": 120,
         "windows": [["2026-03-15","2026-03-30"],
                     ["2026-05-25","2026-06-05"],
                     ["2026-12-20","2027-01-05"],
                     ["2027-02-05","2027-02-25"],
                     ["2027-03-05","2027-04-15"]]}
```

Nak tambah tetingkap baharu: tambah satu baris `["2027-12-20","2028-01-05"]`.

### Upgrade hotel 4 bintang

Katalog mengenakan upgrade **per malam**, dan kadarnya berbeza ikut hari dalam minggu
**dan** musim. Sebab itu ada empat pilihan Accommodation pada baris hari:

| Pilihan | Bila | Kadar | Kunci dalam config |
|---|---|---|---|
| Upgrade 4★ — Ahad–Khamis (biasa) | malam biasa | RM 100/pax | `ext.rates.up4wd` |
| Upgrade 4★ — Jumaat–Sabtu (biasa) | malam biasa | RM 120/pax | `ext.rates.up4we` |
| Upgrade 4★ — Ahad–Khamis PEAK | malam peak | RM 160/pax | `ext.rates.up4wdp` |
| Upgrade 4★ — Jumaat–Sabtu PEAK | malam peak | RM 180/pax | `ext.rates.up4wep` |

Kadar PEAK ialah kadar upgrade **campur RM 60** — beza surcaj peak tersiar katalog
(4 bintang RM 180 tolak 3 bintang RM 120). Kalkulator sudah mengenakan RM 120 untuk
setiap malam peak di peringkat trip, jadi pilihan PEAK hanya menambah bakinya.
Kalau katalog mengubah surcaj peak, ubah **kedua-dua** `peak.value` dan keempat-empat
kadar `up4*` supaya kekal selari.

### Kadar transport (per kenderaan per hari)

`ext.rates.day` untuk **tambah**, `ext.rates.dayDed` untuk **tolak** (nombor negatif).
Kunci ialah tempoh tour; band `from`–`to` ialah bilangan pax → kelas kenderaan.

```json
"[Full Day]": [{"from":1,"to":4,"normal":250,"peak":250},
               {"from":5,"to":6,"normal":300,"peak":300},
               {"from":7,"to":12,"normal":500,"peak":500},
               {"from":13,"to":99,"normal":null,"peak":null}]
```

| Kunci | Tour |
|---|---|
| `[Full Day]` | Full Day Tour 12 jam |
| `[Half Day]` | Half Day Tour 5–6 jam |
| `[Airport + Half Day]` | Airport Transfer + Half Day Tour 6 jam |
| `[Airport]` | Airport Transfer sahaja |
| `[Dieng]`, `[Kebumen]`, `[Nepal van Java]` | luar bandar — **tiada kadar tersiar**, sengaja gap |

`null` bermaksud **tiada kadar tersiar** — kalkulator papar cip merah `kadar?`.
Jangan ganti dengan 0; 0 bermakna percuma.

Hiace VVIP ada kunci sendiri (`ext.rates.vvip` / `vvipDed`), hanya band 7–8 pax dan
hanya untuk `[Full Day]` — RM 950 tambah, RM 600 tolak.

### Kadar malam tambah / tolak

| Kunci | Hotel | Normal | Peak |
|---|---|---|---|
| `n3` | Luxury Malioboro / Emersia (3★) | 150 | 250 |
| `n4` | The 101 Tugu / Grand Zuri (4★) | 180 | 350 |
| `nDieng` | Villa Pintu Langit | 200 | 350 |
| `nGlamp` | Trianggulasi / Linggar Jati | 150 | 250 |
| `nKebumen` | Hotel Kebumen Maxolie | 210 | 350 |
| `nightShort` | tolak malam 3★ | −80 | −80 |

Semua per pax per malam.

### Hidangan

`mealDelta` — `{"add": 30, "drop": 20}` per pax per hidangan berbanding apa yang blok
itinerary itu isytiharkan. Pakej asal 3B / 3L / 3D; breakfast tiada harga tambah atau
tolak berasingan (sudah dalam kadar hotel).

### Add-on

`addons` — senarai `["Nama", hargaAdult, hargaKanak, asas]`.
`"pax"` = kuantiti auto ikut bilangan pax; `"unit"` = TC isi kuantiti sendiri
(jeep, ATV, carriage, dekorasi). Nombor **negatif** ialah item tolak.

```json
["Gondola Timang Beach", 80, 48, "pax"]
["Jeep Timang Beach - per jeep (4 pax/jeep)", 160, 0, "unit"]
["Buang Gondola Timang dari pakej", -50, -50, "pax"]
```

Harga kanak-kanak ialah 60% daripada adult (Product FAQ Notion).

### Blok itinerary

`variants[0].library` — blok yang TC boleh pilih pada mana-mana baris hari.
`region` menentukan kadar transport; `g` ialah kumpulan dalam dropdown.
Blok tour default kepada pilihan **dalam pakej** supaya menukar blok pada hari pakej
berharga RM 0; hari yang TC tambah sendiri dinaikkan ke pilihan berkos oleh
`extDefaults`.

---

## Ujian

Sebelum apa-apa pembinaan semula, empat suite mesti lulus:

| Suite | Liputan |
|---|---|
| `test_calc.js` | invarian am — grand = jumlah baris, quotation dijana, tiada ralat JS |
| `audit_invariants.js` | 201 keadaan (pax × tarikh × tukar blok / hotel / meal × tambah / buang hari) |
| `audit_pdf.js` | apa yang **dicaj** lawan apa yang PDF quotation **tulis** |
| `test_calc_jogja.js` | setiap nombor katalog & rate card — tier, 5 tetingkap peak, kadar setiap tempoh tour × kelas kenderaan, malam tambah/tolak, upgrade 4★, mealDelta, semua add-on |

---

## Nota

Repo ini **public** dan KB mengandungi harga dalaman serta nota operasi.

Sumber lain: PT Jogjakarta 4H3M Travel Map, Flight Recommendation, 2026/2027 Date
Surcharge, FreeGift Campaign MYP 6/26, Product FAQ Notion, FAQ Indonesia.
