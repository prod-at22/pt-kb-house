# PT Perth KB — Simple Calculator

> **Mulai 9 Okt 2026 kandungan KB dan `calc-config.json` datang dari PT R&D Costing Hub** (`prod-at22/pt-rnd-hub`, `data/kb/perth.json`). Fail di sini ditulis semula oleh mirror — **jangan edit di GitHub repo ini**; edit di hub. Skema di bawah masih terpakai.

Halaman live: **https://prod-at22.github.io/pt-kb-house/perth/**

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
semula.

---

## PENTING — bentuk `ext.rates`

Setiap kadar dalam `variants[].ext.rates` **mesti** dibalut `_default`:

```json
"tour8": {"_default": [{"from": 2,  "to": 10, "normal": 2300, "peak": 2300},
                       {"from": 11, "to": 23, "normal": 2800, "peak": 2800}]}
```

Kalau `_default` tertinggal (senarai band ditulis terus), **semua** kadar kunci itu
hilang dan setiap pilihan jadi cip merah `kadar?`. Ini pernah berlaku — kalau tiba-tiba
banyak pilihan jadi "kadar belum diisi", inilah yang perlu disemak dahulu.

`null` pada `normal` bermakna **tiada harga jual tersiar** — halaman akan papar cip merah
`kadar?` dan satu baris amaran. Itu memang niatnya. Isi nombor bila K&N sudah bagi.

---

## Di mana benda yang biasa diubah

### Harga katalog (tier per pax)

`variants[].tiers` — `a` = adult, `c` = CWB, `n` = CNB.

```json
{"from": 4, "to": 5, "a": 3397, "c": 3097, "n": 2797}
```

Varian: `std` PT Perth Standard 5D4N · `prem` PT Perth Premium 6D5N.

### Kadar peak season (Autumn & Winter)

`variants[].peak` — `value` = RM per pax **per malam** yang jatuh dalam tetingkap.
Perth caj peak ikut **tier hotel**: Standard 3★ Apartment RM 80, Premium 4★ Mercure RM 220.

```json
"peak": {"mode": "perNight", "value": 80,
         "windows": [["2026-03-19","2026-03-31"], ["2026-04-01","2026-04-20"],
                     ["2026-07-01","2026-07-15"], ["2026-08-19","2026-08-31"]]}
```

### Surcaj peratus (Spring/Summer & Christmas)

`extraSurcharge[]` — dikenakan ikut **departure date**, bukan per malam.
+5% Sep, Nov, 1–20 Dis 2026 · +10% 21–31 Dis 2026, Jan 2027, 1–20 Feb 2027.

> Oktober 2026 **bukan** peak mengikut **page 2** (yang dipakai), tetapi **page 4**
> katalog kata sebaliknya — lihat *Percanggahan dalam katalog v3* di bawah. Ada
> ujian yang menjaga kelakuan page 2, jadi jangan tukar tanpa kelulusan PO.

### Kadar transport

Perth **tiada** kadar ikut kawasan — kadarnya ikut **tempoh tour × kapasiti kenderaan**.
Jadi semua kunci hanya ada `_default` dengan dua band: **2–10 pax** (12-Seater Hiace) dan
**11–23 pax** (24-Seater bus).

| Kunci | Maksud | 2–10 | 11–23 |
|---|---|---|---|
| `day` | hari extension (asas 8 jam) | 2,300 | 2,800 |
| `dayDed` | auto-tolak bila hari berpandu jadi Free & Easy | −1,500 | −2,000 |
| `tour10` / `tour8` / `tour6` | tour ikut jam | 3,000 / 2,300 / 1,800 | 3,200 / 2,800 / *kosong* |
| `tour5` | tour 5 jam | *kosong* | *kosong* |
| `pinDay` | Pinnacles Day Tour 10 jam + entrance | 3,800 | *kosong* |
| `pinMid` | Pinnacles Stargazing midnight | *kosong* | *kosong* |
| `rotShut` | Rottnest shuttle CBD ↔ ferry terminal | 1,800 | *kosong* |
| `air1` / `air2` | airport transfer 1 hala siang / midnight | 800 / 1,000 | 1,200 / 1,300 |
| `*Cut` | versi tolak-dari-katalog | negatif | negatif |

`ext.shareVehicle: true` — kos kenderaan dibahagi bilangan pax dan dilipat ke harga per
pax, jadi kadar per pax dalam quotation betul tanpa TC kira sendiri.

**Kadar yang masih kosong** (`null`) dan sebabnya:

| Kunci | Sebab |
|---|---|
| `tour5` semua band | K&N ada SKU 5 jam (AUD 500 / 640) tetapi harga jual RM belum ditetapkan |
| `pinMid` semua band | Stargazing tiada dalam katalog; kos K&N AUD 1,100 / 1,500 |
| `tour6` / `pinDay` / `rotShut` band 11–23 | katalog hanya siar kadar sampai 10 pax |

### Hotel

Malam **tambahan** (per pax per malam) — `ext.rates`:
`hApt` 200 · `hCriterion` 250 · `hEuropean` 250 · `hMercure` 350 · `hDuxton` 500.

Upgrade pada **malam pakej** (per pax per malam) — `ext.rates`:
`upCrit` 180 · `upEuro` 200 · `upMerc` 300 · `upDux` 350.

Nilai `peak` pada kadar hotel **bukan** salah tulis. Surcaj peak varian sudah dicaj pada
setiap malam ikut tier defaultnya, jadi kadar `peak` hotel lain hanya menanggung **beza**
tier itu — kalau tidak peak dikira dua kali. Contoh Standard (default 3★ Apt, peak 80):

```
upMerc peak = 300 + (220 − 80) = 440
upCrit peak = 180 + (120 − 80) = 220
```

`nightShort` −180 = tolak per pax bila satu malam pakej dibuang (pilihan
*Tanpa hotel — tolak malam dari katalog*).

### Blok itinerary

`library[]` — 19 blok yang muncul dalam dropdown Itinerary setiap hari, dikumpulkan ikut `g`.

```json
{"v": "fr8", "g": "Fremantle & pantai", "region": "[Fremantle]",
 "t": "Fremantle Day Tour 8 jam", "en": "FREMANTLE DAY TOUR",
 "acc": "incl", "meal": "l", "trp": "i8",
 "act": ["Blue Boat House & Rainbow Containers (photostop)", "..."],
 "eact": ["Blue Boat House & Rainbow Containers (photo stop)", "..."]}
```

| Medan | Maksud |
|---|---|
| `v` | kunci unik — **jangan sama** dengan blok lain |
| `g` | kumpulan dalam dropdown |
| `region` | tag kawasan — di Perth ia **cip maklumat sahaja**, tidak mengubah kadar |
| `t` / `act` | nama & aktiviti **Bahasa Melayu** (dipapar dalam KB) |
| `en` / `eact` | nama & aktiviti **Bahasa Inggeris** (untuk PDF quotation) |
| `acc` / `meal` / `trp` | pilihan default bila blok ini dipilih |

`variants[].itin[]` = itinerary default pakej; bilangannya **mesti** sama dengan `days`.

> Dalam `t`, `en`, `g`, `region`, `act`, `eact`, `inclusions`, `exclusions` — tulis `&`
> biasa sahaja, **jangan** `&amp;`.

### Bagaimana kos berlabuh pada itinerary

- Tukar blok pada hari **pakej** = **RM 0** (harga katalog sudah termasuk hari itu).
- Hari berpandu → blok Free & Easy = **auto tolak** `dayDed` (−1,500).
- Hari Free & Easy → blok berpandu = jadi **hari berpandu tambahan**, berkos.
- `+ Tambah Hari` = `day` (2,300 kenderaan) + `ext.night` (200/pax Standard, 350 Premium).
- Bar itinerary papar kiraan `berpandu 2/2 dalam pakej + n tambahan` supaya TC tak
  terlepas pandang bila bilangan hari berpandu berubah.

### Tempoh tour pada kolum Transport quotation

Katalog p3 nyatakan tempoh setiap hari, dan klausa *validity* quotation merujuk
"the hours stated in the itinerary" — jadi jam **mesti** keluar dalam PDF. Ia dibawa
oleh pilihan Transport, bukan oleh teks hari:

| Pilihan | Label dalam PDF | Dipakai oleh |
|---|---|---|
| `i4` | Private Transport + Guide (4 hours) | PREM Day 4 |
| `i6` | Private Transport + Guide (6 hours) | PREM Day 2 |
| `i8` | Private Transport + Guide (8 hours) | STD Day 2 & 4 · PREM Day 3 |
| `i10` | Private Transport + Guide (10 hours) | PREM Day 5 |
| `air` | Private Airport Transfer (06:00 - 22:00) | hari ketibaan & pulang |

Semua `i*` berkos **RM 0** (hari pakej) — cuma labelnya berbeza. Kalau tambah blok
itinerary baharu yang katalog ada nyatakan jamnya, set `trp` kepada `i4`/`i6`/`i8`/`i10`,
bukan `incl` (yang tiada jam).

### Meal &mdash; hidangan & breakfast automatik

Semua hidangan duduk dalam dropdown **Meal** setiap hari (bukan dalam optional
activity), sebab hidangan itulah yang mengisi kolum *Meals* dalam PDF quotation.

| Kumpulan | Pilihan | Harga per pax |
|---|---|---|
| Dalam pakej | Tiada · Lunch · Dinner · Lunch & Dinner | RM 0 |
| Tambah lunch | Charcoal Chicken · Fish & Chips Kailis · Karache by Sani · halal umum | 75 · 75 · 85 · 90 |
| Tambah lunch (lobster) | Lobster at Kailis · Fish & Chips Lobster Shack · Lobster at Lobster Shack | 150 · 120 · 180 |
| Tambah dinner | Karache by Sani · halal umum | 85 · 120 |
| Tukar lunch pakej | &rarr; Lobster at Kailis · &rarr; Lobster at Lobster Shack | +100 · +100 |
| Tolak lunch pakej | Charcoal/Kailis · Lobster Shack | &minus;50 · &minus;80 |

Guna **Tambah** pada hari yang **tiada** lunch pakej (hari tambahan, hari Free &
Easy). Kalau hari itu sudah ada lunch pakej dan customer nak restoran lain, guna
**Tukar** &mdash; ia sudah tolak nilai lunch pakej (contoh 150 &minus; 50 = +100).
Kalau guna **Tambah** pada hari yang sudah ada lunch pakej, harga dikira dua kali.

#### Breakfast ikut pakej, automatik

`variants[].breakfast` menentukan breakfast, **bukan** blok itinerary:

| Varian | `breakfast` | Sebab (katalog) |
|---|---|---|
| `std` Standard | `false` | 3&#9733; Apartment berkitchenette &mdash; breakfast sendiri |
| `prem` Premium | `true` | Breakfast hotel setiap pagi selepas menginap |

Jadi blok itinerary **tidak** membawa breakfast sama sekali, dan blok yang sama
betul untuk kedua-dua pakej: pilih *Perth City Tour* pada Standard &rarr; Meals
"&ndash;", pada Premium &rarr; "Hotel Breakfast". Dulu blok dikongsi membawa kod
`b`/`bl`, jadi memilih blok pada Standard akan **menjanjikan breakfast yang tidak
dijual**.

Pilihan **Tiada makan (hari ketibaan)** dan **Lunch sahaja (hari ketibaan)** bertanda
`bfLock` &mdash; ia kekal tanpa breakfast walaupun pada Premium, sebab pagi hari
ketibaan customer belum menginap. Itu sebabnya Premium 5 malam = **5 breakfast**
(pagi Day 2 hingga Day 6), sama seperti katalog p3.

Nak tukar label breakfast: `breakfastLabel` (default `Hotel Breakfast`).

### Add-on / optional activity

`addons[]` — `["Nama", hargaAdult, hargaChild, asas]`. Nama masuk PDF quotation, jadi
**tulis dalam Bahasa Inggeris**. Elemen ke-4 menentukan kuantiti automatik:

| Asas | Maksud |
|---|---|
| `"pax"` | darab bilangan pax (kalkulator isi sendiri) |
| `"unit"` | satu unit (contoh extra tour hour) |
| `"share"` | satu unit, dibahagi bilangan pax |

Transport (Pinnacles, Rottnest shuttle, airport transfer) **tiada** dalam `addons` — ia
pilihan Transport per hari, supaya tidak dikira dua kali.

### Lain-lain

| Nak ubah | Di mana |
|---|---|
| Single supplement | `variants[].single` (STD 1,500 · PREM 2,500) |
| Harga infant | `variants[].infant` (0 = FOC) |
| Deposit per pax | `deposit` (1,000) |
| Late booking surcharge | `lateBooking` (<45 hari, RM 50 per booking) |
| Nota ikut saiz group | `paxNotes[]` |
| Inclusions / exclusions PDF | `variants[].inclusions`, `exclusions`, `exclusionsTail` |
| Teks bawah PDF quotation | `validity` |

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

⚠ **Nota data dalaman:** repo ini public. Halaman mengandungi harga jual dalaman,
analisis pesaing dan kod promo Free Gift (FPER3). Sesiapa yang ada link boleh lihat.

## Percanggahan dalam katalog v3 yang belum diselesaikan

Katalog Perth v3 bercanggah dengan dirinya sendiri di beberapa tempat. Kalkulator ikut
**page 2** (jadual peratus surcaj) kerana itulah muka yang beri angka pengiraan, tetapi
PO perlu sahkan dengan operator:

| Perkara | Page 2 (dipakai) | Page 4 / Page 5 |
|---|---|---|
| Hujung peak Mac 2026 | 31 Mac | **28 Mac** |
| Oktober 2026 | **bukan** peak | p4: "1 Sep – 31 Dis 2026" (termasuk Okt) |
| Mula peak Jan 2027 | 1 Jan (+10%) | p4: **15 Jan** |
| Breakfast Premium | p1: **4x** breakfast | p3 itinerary: breakfast Day 2–6 = **5x** (dipakai) |
| Asas jam transport STD | p3/p4: 8 jam | p5: **10 jam** |
| Tetingkap airport transfer STD | 06:00–22:00 | p4: 06:01–21:59 |

Kalau operator sahkan Oktober memang peak, tambah dalam `extraSurcharge`:

```json
{"label":"Peak Spring and Summer","dateIn":["2026-10-01","2026-10-31"],"percentOfTier":5}
```

Kalkulator juga **tidak** menghalang tarikh selepas 31 Mac 2027 walaupun PDF mencetak
"Package valid until 31 March 2027" — semak tarikh sendiri sebelum hantar quotation.

---

*Sumber nombor: katalog PT Perth Standard 5D4N 2026 v3 & Premium 6D5N 2026 v3
(last updated 12 Mac 2026), dan `PT Perth R&D - reformat.xlsx` (tab Raw Costing,
Surcharges, Hotels, Add-Ons). Perth tiada ProdReq.*
